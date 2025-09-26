
import os
import aiohttp
import asyncio
from typing import Dict, Tuple, List
from app.core.config import settings, get_provider_info_for_model
from app.repositories.knowledge_repo import KnowledgeRepository
from app.services.embedding_service import EmbeddingService
from app.services.embedding_service import get_embedding_service
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.db import get_db_session

class APIKeyNotFoundError(Exception):
    pass

class ResponseHandler:
    def __init__(self, repo: KnowledgeRepository, embed_svc: EmbeddingService):
        self._session = None
        self.repo = repo
        self.embed_svc = embed_svc

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=180.0))
        return self._session
    
    async def _build_rag_prompt(self, question: str) -> Tuple[str, List[Dict]]:
        """Builds the final prompt by retrieving context from the database."""
        print("Generating embedding for user query...")
        query_embedding = await self.embed_svc.get_embedding(question)

        print("Searching for similar documents in the database...")
        similar_docs = await self.repo.find_similar_documents(query_embedding)

        if not similar_docs:
            print("No relevant context found in the database.")
            return question, []

        context_str = "\\n\\n---\\n\\n".join([doc.content for doc in similar_docs])
        sources = [{"source": doc.source_document, "content": doc.content} for doc in similar_docs]
        
        final_prompt = f"""
        Based on the following context, please provide a comprehensive answer to the user's question.
        If the context does not contain the answer, state that you do not have enough information.

        CONTEXT:
        {context_str}

        QUESTION:
        {question}
        """
        print("Constructed final prompt with retrieved context.")
        return final_prompt.strip(), sources

    async def call_api(
        self,
        question: str,
        model: str = None,
        max_retries: int = 3,
    ) -> Tuple[str, List[Dict]]:
        """Performs the full RAG loop: retrieve context, build prompt, and call LLM."""
        final_prompt, sources = await self._build_rag_prompt(question)

        model_to_use = model or settings.app.ai.default_model
        provider_info = get_provider_info_for_model(model_to_use)
        
        if not provider_info:
            return f"Error: Model '{model_to_use}' is not configured.", sources

        provider_name = provider_info["provider_name"]
        provider_config = provider_info["config"]
        api_key = os.getenv(provider_config.api_key_env)

        if not api_key:
            raise APIKeyNotFoundError(f"API key env var '{provider_config.api_key_env}' not set.")

        for attempt in range(max_retries):
            try:
                print(f"Calling {provider_name} API (Model: {model_to_use}, Attempt: {attempt + 1}/{max_retries})...")
                if provider_name == "gemini":
                    # Pass the final_prompt, not the original question
                    llm_answer = await self._call_gemini(api_key, final_prompt, model_to_use)
                    return llm_answer, sources
                elif provider_name == "deepseek":
                    # Pass the final_prompt, not the original question
                    llm_answer = await self._call_openai_compatible(api_key, final_prompt, provider_config.api_endpoint)
                    return llm_answer, sources
                else:
                    return f"Error: Provider '{provider_name}' not supported.", sources

            except Exception as e:
                print(f"API call failed: {e}")
                if attempt >= max_retries - 1:
                    return f"Error: API call failed after {max_retries} attempts.", sources
                wait_time = 2 ** (attempt + 1)
                print(f"Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
        
        # This line is now unreachable, which is correct.
        return "Error: Unexpected exit from API call loop.", sources
        
    async def _call_gemini(self, api_key: str, prompt: str, model: str) -> str:
        session = await self.get_session()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {"Content-Type": "application/json"}

        async with session.post(url, json=payload, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    async def _call_openai_compatible(self, api_key: str, prompt: str, endpoint: str) -> str:
        session = await self.get_session()
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        # Ensure the model name is appropriate for the provider
        payload = {"model": "deepseek-coder", "messages": [{"role": "user", "content": prompt}]}

        async with session.post(endpoint, json=payload, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            return data["choices"][0]["message"]["content"].strip()
            
    async def close_session(self):
        # This method is now less critical as sessions are created per-request handler,
        # but it's good practice to keep for potential future use.
        if self._session and not self._session.closed:
            await self._session.close()

# --- CORRECT Dependency Injection Setup ---
def get_response_handler(
    db_session: AsyncSession = Depends(get_db_session)
) -> ResponseHandler:
    """FastAPI dependency to create a ResponseHandler with its own dependencies."""
    repo = KnowledgeRepository(db_session)
    embed_svc = get_embedding_service()
    return ResponseHandler(repo=repo, embed_svc=embed_svc)

async def close_response_handler():
    # The global instance logic is removed. A more robust session management
    # could be implemented on the app state if needed, but this is clean for now.
    pass