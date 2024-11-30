import base64
import os
import tempfile
import whisper


class AudioTranscriptionService:
    def __init__(self, model_name: str = "base"):
        self.whisper_model = whisper.load_model(model_name)

    def transcribe(self, audio_data: str) -> str:
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
            raise Exception(f"Error transcribing audio: {str(e)}")
