import uuid, openai
from typing import Optional, Any
from sqlalchemy.orm import Session

from app.models.term import Term
from app.models.term_explanation import TermExplanation
from app.schemas.term import TermExplainData, TermExplainRequest, TermExplainResponse

from app.models.enums import Source

from app.services.openai_service import call_llm
from app.services.translate_service import translate_text
from app.exceptions.error import AppError, ErrorCode

class TermService:
    # ---------- translate_text/call_llm -> str or dict -> 문자열만 반환 ----------
    
    def _to_text(self, x: Any) -> str:
        if isinstance(x, str):
            return x.strip()

        if isinstance(x, dict):
            for key in ("translated_text", "text", "result", "content", "message"):
                v = x.get(key)
                if isinstance(v, str):
                    return v.strip()
            return str(x).strip()

        return str(x).strip()

    # ---------- DB 조회 ----------

    def find_term_by_name(self, db: Session, term_name: str) -> Term | None:
        return db.query(Term).filter(Term.term_name == term_name).first()

    def create_term(self, db: Session, term_name: str) -> Term:
        term = Term(term_name=term_name)
        db.add(term)
        db.commit()
        db.refresh(term)
        return term

    def find_explanation(self, db: Session, term_id: int) -> TermExplanation | None:
        return db.query(TermExplanation).filter(TermExplanation.term_id == term_id).first()

    def upsert_explanation(self, db: Session, term_id: int, explanation: str) -> TermExplanation:
        row = db.query(TermExplanation).filter(TermExplanation.term_id == term_id).first()
        if row:
            row.explanation = explanation
        else:
            row = TermExplanation(term_id=term_id, explanation=explanation)
            db.add(row)

        db.commit()
        db.refresh(row)
        return row

    # ---------- LLM ----------

    def explain_by_llm(
        self,
        term_text: str,
        context: Optional[str],
    ) -> str:
        try:
            system_prompt = "\n".join([
                "You are a reliable assistant for Korean university students and international students.",
                "Explain Korean university terms accurately and concisely.",
                "You MUST follow the output rules exactly.",
            ])

            user_prompt = "\n".join([
                "Task:",
                "Explain the meaning of the given Korean university term in Korean.",
                "",
                f"Term: {term_text}",
                f"Context: {context or ''}",
                "",
                "Output rules (MUST follow exactly):",
                "- Output Korean only.",
                "- Output ONLY the explanation text.",
                "- Exactly 2 sentences.",
                "- No quotes, no code blocks, no JSON, no labels, no headings.",
                "- No line breaks (single line).",
                "- Do NOT repeat the term itself in the explanation.",
                "- Do NOT mention specific universities unless the context explicitly mentions them.",
                "",
                "Now write the explanation:",
            ])

            return call_llm(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model="gpt-4o-mini",
                temperature=0.3,
                max_tokens=512,
            )

        except openai.RateLimitError as e:
            raise AppError(
                error_code=ErrorCode.RATE_LIMITED,
                message="Rate limit exceeded when calling OpenAI API.",
                detail={"reason":str(e)}
            )

        except (openai.APIConnectionError, openai.APIStatusError) as e:
            raise AppError(
                error_code=ErrorCode.SERVICE_UNAVAILABLE,
                message="Upstream error occurred when calling OpenAI API.",
                detail={"reason":str(e)}
            )
            
        except Exception as e:
            raise AppError(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                detail={"reason":str(e)}
            )

    # ---------- Main Service ----------

    def explain_term(
        self,
        db: Session,
        request: TermExplainRequest,
    ) -> TermExplainResponse:

        request_id = str(uuid.uuid4())

        term_row = self.find_term_by_name(db, request.term)
        if not term_row:
            term_row = self.create_term(db, request.term)

        explanation_row = self.find_explanation(db, term_row.term_id)

        if explanation_row:
            explanation_text = explanation_row.explanation
            source = Source.db
        else:
            # db에 없으면 LLM로 ko 설명 생성 후 db 저장
            explanation_text = self.explain_by_llm(
                term_text=request.term,
                context=request.context,
            ).strip()

            self.upsert_explanation(db, term_row.term_id, explanation_text)
            source = Source.ai_guess
        
        target_lang = getattr(request.target_lang, "value", request.target_lang)
        
        # 응답용, DB 저장 안 함
        translated_term_raw = translate_text(
            text=request.term,
            source_lang="ko",
            target_lang=target_lang,
        )

        if target_lang == "ko":
            translated_explanation_raw = explanation_text
        else:
            translated_explanation_raw = translate_text(
                text=explanation_text,
                source_lang="ko",
                target_lang=target_lang,
            )
        
        translated_term = self._to_text(translated_term_raw)
        translated_explanation = self._to_text(translated_explanation_raw)
        
        return TermExplainResponse(
            request_id=request_id,
            success=True,
            data=TermExplainData(
                term=request.term,
                source=source,
                translated_term=translated_term,
                explanation=explanation_text,
                translated_explanation=translated_explanation,
            ),
        )


term_service = TermService()
