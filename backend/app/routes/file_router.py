from fastapi import APIRouter, UploadFile, File, Depends, Request
from app.dependencies.auth import get_current_user
from app.models.users import User
from app.services.pdf_service import extract_text_from_pdf
from app.services.summarize_service import summarize_text
from app.exceptions.error import AppError, ErrorCode
from app.core.logging import get_logger
import uuid

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    log = get_logger(request)
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    log.info(
        "FILE_UPLOAD_REQUEST",
        extra={
            "filename": file.filename,
            "content_type": file.content_type,
            "user_idx": current_user.user_idx
        }
    )

    try:
        filename = file.filename or "unknown"
        content = ""

        if filename.lower().endswith(".pdf"):
            content = extract_text_from_pdf(file)
        elif filename.lower().endswith(".txt"):
            content_bytes = await file.read()
            # Try multiple encodings
            for encoding in ["utf-8", "cp1252", "euc-kr", "latin-1"]:
                try:
                    content = content_bytes.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if not content:
                raise AppError(
                    error_code=ErrorCode.FILE_PARSE_FAILED,
                    message="Could not decode the text file with supported encodings."
                )
        else:
            raise AppError(
                error_code=ErrorCode.UNSUPPORTED_FILE_TYPE,
                message="Only .pdf and .txt files are supported."
            )

        if not content.strip():
            raise AppError(
                error_code=ErrorCode.INVALID_TEXT,
                message="The uploaded file is empty or contains no readable text."
            )

        # Summarize the content
        summary = summarize_text(text=content)

        return {
            "request_id": request_id,
            "success": True,
            "fileId": str(uuid.uuid4()),
            "summary": summary
        }

    except AppError as e:
        log.warning("FILE_UPLOAD_FAILED", extra={"error_code": e.error_code, "message": str(e)})
        raise e
    except Exception as e:
        log.exception("FILE_UPLOAD_INTERNAL_ERROR")
        raise AppError(
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=f"File upload failed: {str(e)}"
        )
