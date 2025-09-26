# app\services\llm.py

import aiohttp
import asyncio

class LLMService:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._session = None

    async def get_session(self) -> aiohttp.ClientSession:
        """Initializes and returns the aiohttp session, creating it if needed."""
        if self._session is None or self._session.closed:
            # You can configure timeouts and other settings here
            self._session = aiohttp.ClientSession()
        return self._session

    async def generate_answer(self, question: str) -> str:
        """
        (Mocked) Makes a call to an external LLM to get an answer.
        In the future, this will be a real API call.
        """
        # Simulate a network call
        await asyncio.sleep(0.5)
        
        # In a real implementation, you would use the session like this:
        # session = await self.get_session()
        # async with session.post(url, json=payload, headers=headers) as response:
        #     ...

        mock_answer = f"This is a mocked answer from the LLMService for your question: '{question}'"
        return mock_answer

    async def close_session(self):
        """Closes the aiohttp session if it exists."""
        if self._session and not self._session.closed:
            await self._session.close()

# --- Dependency Injection Setup ---
# This setup allows FastAPI to manage the lifecycle of our service.

# Global instance of the service
# Note: For a real app, you might manage this more robustly,
# but this is a common and effective pattern.
llm_service_instance = None

async def get_llm_service() -> LLMService:
    """
    FastAPI dependency that provides an LLMService instance.
    This ensures we use a single instance for the application's lifespan.
    """
    global llm_service_instance
    if llm_service_instance is None:
        # In a real app, the API key would come from settings
        # from app.core.config import settings
        # llm_service_instance = LLMService(api_key=settings.LLM_API_KEY)
        llm_service_instance = LLMService(api_key="dummy-key")
    return llm_service_instance

async def close_llm_service():
    """Application shutdown event handler to clean up the session."""
    service = await get_llm_service()
    await service.close_session()

