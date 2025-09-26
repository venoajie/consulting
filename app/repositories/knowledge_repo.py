# app\repositories\knowledge_repo.py

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.models.knowledge_document import KnowledgeDocument

class KnowledgeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_document(
        self,
        content: str,
        embedding: list[float],
        source_document: str,
        attributes: dict | None = None,
    ) -> KnowledgeDocument:
        new_doc = KnowledgeDocument(
            content=content,
            embedding=embedding,
            source_document=source_document,
            attributes=attributes,
        )
        self.session.add(new_doc)
        await self.session.commit()
        await self.session.refresh(new_doc)
        return new_doc

    async def find_similar_documents(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[KnowledgeDocument]:
        """
        Finds documents with embeddings similar to the query embedding.
        Uses the cosine distance operator (<=>) from pgvector.
        """
        # The '<=>' operator calculates cosine distance (0=exact match, 1=opposite)
        # We find the 'limit' number of documents with the smallest distance.
        stmt = select(KnowledgeDocument).order_by(
            KnowledgeDocument.embedding.l2_distance(query_embedding)
        ).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()