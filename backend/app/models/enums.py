from enum import Enum


class Role(str, Enum):
    user = "user"
    assistant = "assistant"


class FeatureType(str, Enum):
    translate = "translate"
    summarize = "summarize"
    term = "term"
    speech = "speech"
    pdf_summarize = "pdf_summarize"
    pdf_translate = "pdf_translate"


class Lang(str, Enum):
    ko = "ko"
    en = "en"
    uz = "uz"
