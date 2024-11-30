from langchain.document_loaders import (
    CSVLoader, Docx2txtLoader, PyPDFLoader,
    TextLoader, UnstructuredExcelLoader
)


class DocumentProcessingService:
    @staticmethod
    def get_loader(file_path: str):
        file_type = file_path.split('.')[-1].lower()

        # Choose appropriate document loader
        loaders = {
            "pdf": PyPDFLoader,
            "docx": Docx2txtLoader,
            "csv": CSVLoader,
            "xlsx": UnstructuredExcelLoader
        }

        return loaders.get(file_type, TextLoader)(file_path)

    @staticmethod
    def process_document(file_path: str, vector_store_service):
        # Load document
        loader = DocumentProcessingService.get_loader(file_path)
        documents = loader.load()

        # Add to vector store
        return vector_store_service.add_documents(documents)
