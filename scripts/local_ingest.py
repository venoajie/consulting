
import asyncio
from sentence_transformers import SentenceTransformer
from app.core.db import AsyncSessionFactory
from app.repositories.knowledge_repo import KnowledgeRepository

# --- Configuration ---
# In a real app, this model name would come from a config file.
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" # A small, fast model for local testing

async def main():
    """
    Simulates the core logic of our future OCI Ingestion Function.
    It takes a sample document, creates an embedding, and saves it to the DB.
    """
    print("--- Starting local ingestion script ---")

    # 1. Load the embedding model
    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    print("Model loaded successfully.")

    # 2. Prepare sample data
    sample_content = "The standard deduction for 2024 is $14,600 for single filers."
    sample_source = "IRS Publication 501"
    sample_attributes = {"year": 2024, "category": "deductions"}
    print(f"Prepared sample document from: {sample_source}")

    # 3. Create the embedding
    print("Generating embedding for sample content...")
    embedding = model.encode(sample_content).tolist()
    print(f"Embedding generated with dimension: {len(embedding)}")

    # 4. Use the repository to save to the database
    print("Connecting to the database and saving document...")
    async with AsyncSessionFactory() as session:
        repo = KnowledgeRepository(session)
        new_document = await repo.create_document(
            content=sample_content,
            embedding=embedding,
            source_document=sample_source,
            attributes=sample_attributes,
        )
    
    print("--- Document saved successfully! ---")
    print(f"Document ID: {new_document.id}")
    print(f"Content: {new_document.content[:50]}...")
    print("------------------------------------")


if __name__ == "__main__":
    asyncio.run(main())