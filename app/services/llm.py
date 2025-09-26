# app\services\llm.py


import os
import aiohttp
import asyncio
import time
from typing import Dict, Tuple
from app.core.config import settings, get_provider_info_for_model

class APIKeyNotFoundError(Exception):
    pass

class ResponseHandler:
    def __init__(self):
        self._session = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=180.0))
        return self._session

    async def call_api(
        self,
        question: str,
        model: str = None,
        max_retries: int = 3,
    ) -> str:
        """Calls the specified AI model with robust error handling and retries."""
        model_to_use = model or settings.ai.default_model
        provider_info = get_provider_info_for_model(model_to_use)
        
        if not provider_info:
            return f"Error: Model '{model_to_use}' is not configured."

        provider_name = provider_info["provider_name"]
        provider_config = provider_info["config"]
        api_key = os.getenv(provider_config.api_key_env)

        if not api_key:
            raise APIKeyNotFoundError(f"API key env var '{provider_config.api_key_env}' not set.")

        for attempt in range(max_retries):
            try:
                print(f"Calling {provider_name} API (Model: {model_to_use}, Attempt: {attempt + 1}/{max_retries})...")
                if provider_name == "gemini":
                    return await self._call_gemini(api_key, question, model_to_use)
                elif provider_name == "deepseek":
                    return await self._call_openai_compatible(api_key, question, provider_config.api_endpoint)
                else:
                    return f"Error: Provider '{provider_name}' not supported."

            except Exception as e:
                print(f"API call failed: {e}")
                if attempt >= max_retries - 1:
                    return f"Error: API call failed after {max_retries} attempts."
                wait_time = 2 ** (attempt + 1)
                print(f"Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
        return "Error: Should not be reached."

    async def _call_gemini(self, api_key: str, question: str, model: str) -> str:
        session = await self.get_session()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": question}]}]}
        headers = {"Content-Type": "application/json"}

        async with session.post(url, json=payload, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    async def _call_openai_compatible(self, api_key: str, question: str, endpoint: str) -> str:
        session = await self.get_session()
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": "deepseek-coder", "messages": [{"role": "user", "content": question}]}

        async with session.post(endpoint, json=payload, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            return data["choices"][0]["message"]["content"].strip()
            
    async def close_session(self):
        if self._session and not self._session.closed:
            await self._session.close()

# --- Dependency Injection Setup ---
response_handler_instance = None

async def get_response_handler() -> ResponseHandler:
    global response_handler_instance
    if response_handler_instance is None:
        response_handler_instance = ResponseHandler()
    return response_handler_instance

async def close_response_handler():
    global response_handler_instance
    if response_handler_instance:
        await response_handler_instance.close_session()

