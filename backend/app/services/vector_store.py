import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter


class VectorStoreService:
    def __init__(self, collection_name: str = "document_context"):
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(
            collection_name)

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def add_documents(self, documents):
        # Split documents
        texts = self.text_splitter.split_documents(documents)

        # Add to vector store
        text_contents = [doc.page_content for doc in texts]
        self.collection.add(
            documents=text_contents,
            ids=[f"doc_{i}" for i in range(len(text_contents))]
        )
        return text_contents

    def query_context(self, query: str, n_results: int = 2) -> str:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return "\n".join(results["documents"][0]) if results["documents"] else ""
