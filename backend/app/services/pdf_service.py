from __future__ import annotations

from io import BytesIO
from fastapi import UploadFile
from pypdf import PdfReader

MAX_PDF_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def extract_text_from_pdf(file: UploadFile) -> str:
    """
    주어진 PDF 파일에서 텍스트를 추출하는 함수

    Args:
        file (UploadFile): 텍스트를 추출할 PDF 파일

    Returns:
        str: 추출된 텍스트
    """
    
    # 파일 존재 확인
    if file is None or not file.filename:
        raise ValueError("No file provided.")
    
    # 파일 확장자 확인
    if not file.filename.lower().endswith(".pdf"):
        raise ValueError("The provided file is not a PDF.")
      
    # 파일 크기 확인
    file.file.seek(0, 2)  # Move to end of file
    file_size = file.file.tell() # Get current position
    if file_size > MAX_PDF_FILE_SIZE:
        raise ValueError("The provided PDF file is too large.")
    # Reset file pointer to the beginning
    file.file.seek(0)
    

    # PDF 파싱 & PDF에서 텍스트 추출
    try:
        reader = PdfReader(file.file)
        texts = list[str] = []
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                texts.append(page_text)

        merged_text = "\n\n".join(texts).strip()

        if not merged_text:
            raise ValueError("No text found in the provided PDF file.")

        return merged_text
      
    except Exception as e:
        raise ValueError("Failed to extract text from PDF file.") from e
      
    finally:
        file.file.close()
        