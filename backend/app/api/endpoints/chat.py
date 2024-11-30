from fastapi import APIRouter, HTTPException
from app.models.chat import ChatMessage, ChatResponse
from app.services.audio_transcription import AudioTranscriptionService
from app.services.vector_store import VectorStoreService
from app.services.language_model import LanguageModelService
from app.services.plagiarism_detector import PlagiarismDetectorService
from app.core.config import settings

router = APIRouter()

# Initialize services
audio_service = AudioTranscriptionService(settings.WHISPER_MODEL)
vector_store_service = VectorStoreService()
language_model_service = LanguageModelService(settings.MODEL_NAME)
plagiarism_service = PlagiarismDetectorService()


@router.post("/chat", response_model=ChatResponse)
async def process_chat(message: ChatMessage):
    try:
        # Transcribe audio if provided
        if message.audio_data:
            message.message = audio_service.transcribe(message.audio_data)

        # Get context from vector store
        context = vector_store_service.query_context(message.message)

        # Generate response
        response = language_model_service.generate_response(
            message.message, context)

        # Check plagiarism
        ai_probability = plagiarism_service.check_plagiarism(response)

        return ChatResponse(response=response, ai_probability=ai_probability)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
