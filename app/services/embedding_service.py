# app\services\embedding_service.py

import random

class EmbeddingService:
    async def get_embedding(self, text: str) -> list[float]:
        """
        (Mocked) Creates a random vector of the correct dimension.
        This simulates the query-time embedding process.
        """
        # Our DB schema expects 384 dimensions
        return [random.uniform(-1, 1) for _ in range(384)]

embedding_service_instance = EmbeddingService()

def get_embedding_service() -> EmbeddingService:
    return embedding_service_instance