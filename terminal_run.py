import base64
import os
import tempfile
from typing import List, Optional

import chromadb
import torch
import whisper
from langchain.document_loaders import (
    CSVLoader, Docx2txtLoader, PyPDFLoader,
    TextLoader, UnstructuredExcelLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


class VoiceRAGChatbot:
    def __init__(self):
        try:
            print("Initializing Voice RAG Chatbot...")

            # Speech-to-Text
            print("Loading Whisper model...")
            self.whisper_model = whisper.load_model("base")

            # Language Model
            print("Loading Language Model...")
            self.model = AutoModelForCausalLM.from_pretrained(
                "homebrewltd/Ichigo-llama3.1-s-instruct-v0.4",
                torch_dtype=torch.float16,
                device_map="auto"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(
                "homebrewltd/Ichigo-llama3.1-s-instruct-v0.4")

            # Vector Store
            print("Setting up Vector Database...")
            self.chroma_client = chromadb.Client()
            self.collection = self.chroma_client.get_or_create_collection(
                "document_context")

            # Text Splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            # Plagiarism Detector
            print("Loading Plagiarism Detector...")
            self.plag_detector = pipeline(
                "text-classification",
                model="roberta-base-openai-detector"
            )

            print("Chatbot initialized successfully!")
        except Exception as e:
            print(f"Error during initialization: {e}")
            raise

    def transcribe_audio(self, audio_data: str) -> str:
        try:
            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_data)

            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio_path = temp_audio.name

            try:
                # Transcribe audio
                result = self.whisper_model.transcribe(temp_audio_path)
                return result["text"]
            finally:
                # Clean up temporary file
                os.unlink(temp_audio_path)

        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return ""

    def process_document(self, file_path: str) -> List[str]:
        try:
            file_type = file_path.split('.')[-1].lower()

            # Choose appropriate document loader
            if file_type == "pdf":
                loader = PyPDFLoader(file_path)
            elif file_type == "docx":
                loader = Docx2txtLoader(file_path)
            elif file_type == "csv":
                loader = CSVLoader(file_path)
            elif file_type == "xlsx":
                loader = UnstructuredExcelLoader(file_path)
            else:
                loader = TextLoader(file_path)

            # Load and split documents
            documents = loader.load()
            texts = self.text_splitter.split_documents(documents)

            # Add to vector store
            text_contents = [doc.page_content for doc in texts]
            self.collection.add(
                documents=text_contents,
                ids=[f"doc_{i}" for i in range(len(text_contents))]
            )

            print(f"Processed {len(text_contents)} document chunks.")
            return text_contents
        except Exception as e:
            print(f"Error processing document: {e}")
            return []

    def get_context(self, query: str) -> str:
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=2
            )
            return "\n".join(results["documents"][0]) if results["documents"] else ""
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return ""

    def generate_response(self, message: str, context: str) -> str:
        try:
            # Prepare prompt with context
            prompt = f"""Context: {context}
User: {message}
Assistant: """

            # Generate response
            inputs = self.tokenizer(
                prompt, return_tensors="pt").to(self.model.device)
            outputs = self.model.generate(
                **inputs,
                max_length=512,
                temperature=0.7,
                num_return_sequences=1
            )

            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I couldn't generate a response."

    def check_plagiarism(self, text: str) -> float:
        try:
            result = self.plag_detector(text)
            return result[0]["score"] if result[0]["label"] == "fake" else 1 - result[0]["score"]
        except Exception as e:
            print(f"Error checking plagiarism: {e}")
            return 0.5


def main():
    chatbot = VoiceRAGChatbot()

    while True:
        print("\n--- Voice RAG Chatbot Menu ---")
        print("1. Chat")
        print("2. Upload Document")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            # Chat mode
            while True:
                try:
                    message = input("\nYou (type 'back' to return to menu): ")

                    if message.lower() == 'back':
                        break

                    # Check if it's an audio transcription request
                    if message.lower().startswith('transcribe:'):
                        audio_path = message.split(':', 1)[1].strip()
                        try:
                            with open(audio_path, 'rb') as audio_file:
                                audio_data = base64.b64encode(
                                    audio_file.read()).decode('utf-8')
                            message = chatbot.transcribe_audio(audio_data)
                            print(f"Transcribed: {message}")
                        except Exception as e:
                            print(f"Error processing audio file: {e}")
                            continue

                    # Get context
                    context = chatbot.get_context(message)

                    # Generate response
                    response = chatbot.generate_response(message, context)

                    # Check AI probability
                    ai_probability = chatbot.check_plagiarism(response)

                    print("\nAssistant:", response)
                    print(f"AI Probability: {ai_probability:.2f}")

                except Exception as e:
                    print(f"An error occurred during chat: {e}")

        elif choice == '2':
            # Document upload
            file_path = input("Enter the full path to the document: ")
            if os.path.exists(file_path):
                chatbot.process_document(file_path)
            else:
                print("File not found. Please check the path.")

        elif choice == '3':
            print("Exiting Voice RAG Chatbot. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
