from typing import Optional
from io import BytesIO

from fastapi import UploadFile

from app.services.openai_service import get_openai_client

# 허용 확장자
ALLOWED_EXTENSIONS = {'.mp3', '.m4a', '.wav'}


def _validate_audio_file(file: UploadFile):
    if not file.filename:
        raise ValueError("Filename is missing.")

    ext = '.' + file.filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension. Allowed extensions: {ALLOWED_EXTENSIONS}")

def transcribe(
    file: UploadFile,
    auto_detect: bool = True,
    lang: Optional[str] = None
  ) -> str:
    """
    Transcribe audio file to text using OpenAI Whisper.

    Args:
        file (UploadFile): The uploaded audio file.
        auto_detect (bool): Whether to auto-detect language.
        lang (Optional[str]): Language code if auto_detect is False.

    Returns:
        str: Transcribed text.
    """
    
    _validate_audio_file(file)

    if not auto_detect and not lang:
        raise ValueError("Language must be specified when auto_detect is False.")

    try:
      audio_bytes = file.file.read()
      audio_file = BytesIO(audio_bytes)
      audio_file.name = file.filename  # Set filename for OpenAI API
      
      client = get_openai_client()

      # Whisper(STT) 호출
      response = client.audio.transcriptions.create(
          model="gpt-4o-mini-transcribe",
          file=audio_file,
          language=None if auto_detect else lang,
      )
      
      return response.text.strip()
    
    except Exception as e:
        raise ValueError(f"Error during transcription: {str(e)}")