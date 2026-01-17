"use client"

import * as React from "react"

export type Language = "KR" | "EN" | "UZ"

interface Translations {
    // Main Chat
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
    confirm_clear_history: string
    delete_account_failed: string
    delete_account_success: string
    save: string

    // Sidebar
    new_chat: string
    search_chats: string
    history_title: string
    projects_title: string
    new_project: string
    no_projects: string
    guest_user: string

    // Auth (Login/Register)
    login_title: string
    login_subtitle: string
    login_id_label: string
    password_label: string
    login_button: string
    no_account: string
    register_link: string
    demo_link: string
    register_title: string
    name_label: string
    email_label: string
    register_button: string
    have_account: string
    login_link: string

    // Settings
    settings_title: string
    profile_section: string
    name_input_label: string
    name_help: string
    background_section: string
    appearance_section: string
    theme_light: string
    theme_dark: string
    theme_system: string
    language_section: string
    system_section: string
    clear_history: string
    logout: string

    // Create Project Dialog
    create_project_title: string
    project_name_placeholder: string
    project_desc: string
    create_button: string
    cat_homework: string
    cat_research: string
    cat_exam: string
    cat_group: string
    cat_language: string

    // Memo
    memo_title: string
    memo_placeholder: string
    save_memo: string
}


const translations: Record<Language, Translations> = {
    KR: {
        welcome: "KNU 다국어 어시스턴트에 오신 것을 환영합니다!",
        sub_welcome: "강의 자료를 쉽게 이해할 수 있도록 도와드립니다.",
        placeholder: "여기에 텍스트를 붙여넣거나 입력하세요...",
        translate: "번역",
        summarize: "요약",
        term: "용어 설명",
        send: "전송",
        analyzing: "AI가 분석 중입니다...",
        error_empty: "텍스트를 입력해주세요!",
        disclaimer: "KNU MLA는 AI를 기반으로 작동하며 오류가 발생할 수 있습니다.",
        confirm_clear_history: "정말로 계정을 탈퇴하시겠습니까? (이 작업은 되돌릴 수 없습니다)",
        delete_account_failed: "계정 삭제에 실패했습니다.",
        delete_account_success: "계정이 성공적으로 삭제되었습니다.",
        save: "저장",

        // Sidebar
        new_chat: "새 채팅",
        search_chats: "채팅 검색",
        history_title: "기록",
        projects_title: "프로젝트",
        new_project: "새 프로젝트",
        no_projects: "프로젝트 없음",
        guest_user: "게스트 사용자",

        // Auth
        login_title: "환영합니다",
        login_subtitle: "KNU 다국어 어시스턴트",
        login_id_label: "로그인 ID",
        password_label: "비밀번호",
        login_button: "로그인",
        no_account: "계정이 없으신가요?",
        register_link: "회원가입",
        demo_link: "데모 보기 (로그인 건너뛰기)",
        register_title: "회원가입",
        name_label: "이름",
        email_label: "이메일",
        register_button: "가입하기",
        have_account: "계정이 있으신가요?",
        login_link: "로그인",

        // Settings
        settings_title: "설정",
        profile_section: "프로필",
        name_input_label: "이름",
        name_help: "채팅에 표시될 이름입니다.",
        background_section: "배경화면",
        appearance_section: "화면 설정",
        theme_light: "lightmode",
        theme_dark: "darkmode",
        theme_system: "System",
        language_section: "언어",
        system_section: "시스템 관리",
        clear_history: "계정 탈퇴",
        logout: "로그아웃",

        // Create Project
        create_project_title: "프로젝트 만들기",
        project_name_placeholder: "프로젝트 이름 (예: 컴퓨터 구조 과제)",
        project_desc: "프로젝트는 채팅, 파일, 학습 자료를 한곳에 보관합니다. 진행 중인 과제나 시험 공부를 위해 사용하세요.",
        create_button: "프로젝트 생성",
        cat_homework: "과제",
        cat_research: "연구",
        cat_exam: "시험 공부",
        cat_group: "팀 프로젝트",
        cat_language: "어학 공부",

        // Memo
        memo_title: "메모",
        memo_placeholder: "여기에 메모를 작성하세요...",
        save_memo: "메모 저장"
    },
    EN: {
        welcome: "Welcome to KNU Multilingual Assistant!",
        sub_welcome: "Helping you understand course materials easily.",
        placeholder: "Paste or type your text here...",
        translate: "Translate",
        summarize: "Summarize",
        term: "Explain Term",
        send: "Send",
        analyzing: "AI Analyzing...",
        error_empty: "Please enter some text!",
        disclaimer: "KNU MLA is powered by AI and may make mistakes.",
        confirm_clear_history: "Are you sure you want to delete your account? (This cannot be undone)",
        delete_account_failed: "Failed to delete account.",
        delete_account_success: "Account deleted successfully.",
        save: "Save",

        // Sidebar
        new_chat: "New Chat",
        search_chats: "Search chats",
        history_title: "History",
        projects_title: "Projects",
        new_project: "New Project",
        no_projects: "No projects",
        guest_user: "Guest User",

        // Auth
        login_title: "Welcome Back",
        login_subtitle: "KNU Multilingual Assistant",
        login_id_label: "Login ID",
        password_label: "Password",
        login_button: "Sign In",
        no_account: "Don't have an account?",
        register_link: "Register",
        demo_link: "View Demo (Skip Login)",
        register_title: "Create Account",
        name_label: "Name",
        email_label: "Email",
        register_button: "Sign Up",
        have_account: "Already have an account?",
        login_link: "Login",

        // Settings
        settings_title: "Settings",
        profile_section: "Profile",
        name_input_label: "Name",
        name_help: "This name will appear in chat.",
        background_section: "Background Image",
        appearance_section: "Appearance",
        theme_light: "lightmode",
        theme_dark: "darkmode",
        theme_system: "System",
        language_section: "Language",
        system_section: "System",
        clear_history: "Delete Account",
        logout: "Logout",

        // Create Project
        create_project_title: "Create project",
        project_name_placeholder: "Project name (e.g. CS Lecture Notes)",
        project_desc: "Projects keep chats, files, and study materials in one place. Use them for ongoing homework or exam prep.",
        create_button: "Create project",
        cat_homework: "Homework",
        cat_research: "Research",
        cat_exam: "Exam Prep",
        cat_group: "Group Project",
        cat_language: "Language Study",

        // Memo
        memo_title: "Memo Pad",
        memo_placeholder: "Write your notes here...",
        save_memo: "Save Memo"
    },
    UZ: {
        welcome: "KNU Multilingual Assistant'ga xush kelibsiz!",
        sub_welcome: "Dars materiallarini oson tushunish uchun yordamchi.",
        placeholder: "Matnni shu yerga joylashtiring yoki yozing...",
        translate: "Tarjima",
        summarize: "Qisqartirish",
        term: "Termin",
        send: "Yuborish",
        analyzing: "AI tahlil qilmoqda...",
        error_empty: "Iltimos, avval matn kiriting!",
        disclaimer: "KNU MLA sun'iy intellekt asosida ishlaydi. Xatoliklar bo'lishi mumkin.",
        confirm_clear_history: "Haqiqatan ham hisobingizni o'chirmoqchimisiz? (Bu amalni bekor qilib bo'lmaydi)",
        delete_account_failed: "Hisobni o'chirish muvaffaqiyatsiz tugadi.",
        delete_account_success: "Hisob muvaffaqiyatli o'chirildi.",
        save: "Saqlash",

        // Sidebar
        new_chat: "Yangi Chat",
        search_chats: "Chatlarni qidirish",
        history_title: "Tarix",
        projects_title: "Loyihalar",
        new_project: "Yangi Loyiha",
        no_projects: "Loyihalar yo'q",
        guest_user: "Mehmon",

        // Auth
        login_title: "Xush Kelibsiz",
        login_subtitle: "KNU Multilingual Assistant",
        login_id_label: "Login ID",
        password_label: "Parol",
        login_button: "Kirish",
        no_account: "Hisobingiz yo'qmi?",
        register_link: "Ro'yxatdan o'tish",
        demo_link: "Demoni ko'rish (Loginni o'tkazib yuborish)",
        register_title: "Ro'yxatdan o'tish",
        name_label: "Ism",
        email_label: "Email",
        register_button: "Ro'yxatdan o'tish",
        have_account: "Hisobingiz bormi?",
        login_link: "Kirish",

        // Settings
        settings_title: "Sozlamalar",
        profile_section: "Profil",
        name_input_label: "Ism",
        name_help: "Ismingiz chatda ko'rinadi.",
        background_section: "Orqa fon",
        appearance_section: "Ko'rinish",
        theme_light: "lightmode",
        theme_dark: "darkmode",
        theme_system: "Tizim",
        language_section: "Til",
        system_section: "Tizim",
        clear_history: "Hisobni o'chirish",
        logout: "Tizimdan chiqish",

        // Create Project
        create_project_title: "Loyiha yaratish",
        project_name_placeholder: "Loyiha nomi (masalan, Kurs ishi)",
        project_desc: "Loyihalar chatlar, fayllar va o'quv materiallarini bir joyda saqlaydi. Uy vazifalari yoki imtihonga tayyorgarlik uchun foydalaning.",
        create_button: "Loyiha yaratish",
        cat_homework: "Uy vazifasi",
        cat_research: "Tadqiqot",
        cat_exam: "Imtihon",
        cat_group: "Jamoaviy ish",
        cat_language: "Til o'rganish",

        // Memo
        memo_title: "Eslatmalar",
        memo_placeholder: "Eslatmalaringizni shu yerga yozing...",
        save_memo: "Saqlash"
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
