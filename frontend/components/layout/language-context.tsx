"use client"

import * as React from "react"

export type Language = "KR" | "EN" | "UZ"

interface Translations {
    welcome: string
    sub_welcome: string
    placeholder: string
    translate: string
    summarize: string
    term: string
    send: string
    analyzing: string
    error_empty: string
    disclaimer: string
}

const translations: Record<Language, Translations> = {
    KR: {
        welcome: "KNU 다국어 어시스턴트에 오신 것을 환영합니다! 👋",
        sub_welcome: "강의 자료를 쉽게 이해할 수 있도록 도와드립니다.",
        placeholder: "여기에 텍스트를 붙여넣거나 입력하세요...",
        translate: "번역",
        summarize: "요약",
        term: "용어 설명",
        send: "전송",
        analyzing: "AI가 분석 중입니다...",
        error_empty: "텍스트를 입력해주세요!",
        disclaimer: "KNU MLA는 AI를 기반으로 작동하며 오류가 발생할 수 있습니다."
    },
    EN: {
        welcome: "Welcome to KNU Multilingual Assistant! 👋",
        sub_welcome: "Helping you understand course materials easily.",
        placeholder: "Paste or type your text here...",
        translate: "Translate",
        summarize: "Summarize",
        term: "Explain Term",
        send: "Send",
        analyzing: "AI Analyzing...",
        error_empty: "Please enter some text!",
        disclaimer: "KNU MLA is powered by AI and may make mistakes."
    },
    UZ: {
        welcome: "KNU Multilingual Assistant'ga xush kelibsiz! 👋",
        sub_welcome: "Dars materiallarini oson tushunish uchun yordamchi.",
        placeholder: "Matnni shu yerga joylashtiring yoki yozing...",
        translate: "Tarjima",
        summarize: "Qisqartirish",
        term: "Termin",
        send: "Yuborish",
        analyzing: "AI tahlil qilmoqda...",
        error_empty: "Iltimos, avval matn kiriting!",
        disclaimer: "KNU MLA sun'iy intellekt asosida ishlaydi. Xatoliklar bo'lishi mumkin."
    }
}

interface LanguageContextType {
    language: Language
    setLanguage: (lang: Language) => void
    t: Translations
}

const LanguageContext = React.createContext<LanguageContextType | undefined>(undefined)

export function LanguageProvider({ children }: { children: React.ReactNode }) {
    const [language, setLanguage] = React.useState<Language>("EN")

    return (
        <LanguageContext.Provider value={{ language, setLanguage, t: translations[language] }}>
            {children}
        </LanguageContext.Provider>
    )
}

export function useLanguage() {
    const context = React.useContext(LanguageContext)
    if (context === undefined) {
        throw new Error("useLanguage must be used within a LanguageProvider")
    }
    return context
}
