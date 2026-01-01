import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.term import Term
from app.models.term_explanation import TermExplanation
from app.schemas.term import TermExplainData, TermExplainRequest, TermExplainResponse

from app.services.openai_service import call_llm
from app.services.translate_service import translate_text


class TermService:

    # ---------- DB 조회 ----------

    def get_term_by_id(self, db: Session, term_id: int) -> Term:
        term_row = db.query(Term).filter(Term.term_id == term_id).first()
        if not term_row:
            raise NotFoundException(f"Term with id {term_id} not found")
        return term_row

    def find_explanation(
        self, db: Session, term_id: int, target_lang: str
    ) -> Optional[TermExplanation]:
        return (
            db.query(TermExplanation)
            .filter(
                TermExplanation.term_id == term_id,
                TermExplanation.term_lang == target_lang,
            )
            .first()
        )

    # ---------- LLM ----------

    def explain_by_llm(
        self,
        term_text: str,
        target_lang: str,
        context: Optional[str],
    ) -> str:
        system_prompt = (
            "You are a helpful assistant designed for university students. "
            "You provide accurate, concise, and neutral explanations of academic "
            "and campus-related terms. "
            "You strictly follow formatting instructions."
        )

        user_prompt = (
            "You are helping an international student at Kyungpook National University (KNU).\n"
            "The term below appears in Korean university life (course registration, grades, notices, student community).\n\n"
            f"Term:\n{term_text}\n\n"
            f"Context:\n{context or 'Not provided'}\n\n"
            "Tasks:\n"
            f"1) Translate the term into {target_lang}.\n"
            "2) Explain what it means in a Korean university setting (especially KNU-style academic/campus context).\n"
            "   - If the term is slang/abbreviation used by students, explain that.\n"
            "   - If the term relates to course registration, graduation requirements, grades, or major requirements, reflect that.\n"
            "   - If the meaning is uncertain, give the most likely interpretation and keep confidence modest.\n\n"
            "Output format (follow exactly):\n"
            "Line 1: ONLY the translated term.\n"
            "Line 2: (blank)\n"
            "Lines 3-5: Explanation in 2–3 complete sentences in a clear, neutral tone.\n"
            f"Line 6: (blank)\n"
            f"Lines 7-9: The same explanation translated into {target_lang} (2–3 sentences).\n\n"
            "Constraints:\n"
            "- Do NOT add labels or headings (no 'Translation:', 'Explanation:', etc.).\n"
            "- Do NOT include pronunciation/romanization.\n"
            "- Do NOT invent specific KNU-only facts (numbers, official policies) unless you are sure.\n"
            "- Keep it helpful for a university student.\n"
        )

        return call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=512,
        )

    # ---------- Main Service ----------

    def explain_term(
        self,
        db: Session,
        request: TermExplainRequest,
    ) -> TermExplainResponse:
        request_id = str(uuid.uuid4())

        # DB에서 term 조회 (이름 기준)
        term_row = (
            db.query(Term)
            .filter(Term.term_name == request.term)
            .first()
        )

        # DB에 term 존재
        if term_row:
            explanation_row = self.find_explanation(
                db, term_row.term_id, request.target_lang
            )

            return TermExplainResponse(
                request_id=request_id,
                success=True,
                data=TermExplainData(
                    term=request.term,
                    source="db",
                    explanation=explanation_row.explanation,
                    translated_explanation=translate_text(explanation_row.explanation),
                ),
            )

        # DB에 term 자체가 없음 → AI 추정
        explanation_text = self.explain_by_llm(
            term_text=request.term,
            target_lang=request.target_lang,
            context=request.context,
        )

        return TermExplainResponse(
            request_id=request_id,
            success=True,
            data=TermExplainData(
                term=request.term,
                source="ai_guess",
                explanation=explanation_text,
                translated_explanation=translate_text(explanation_text),
            ),
        )


class NotFoundException(Exception):
    pass


term_service = TermService()
