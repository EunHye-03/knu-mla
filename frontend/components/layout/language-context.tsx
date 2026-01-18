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
        background_section: string // Kept from HEAD
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
        cat_finance: string
        cat_travel: string
        cat_coding: string

        // Memo
        memo_title: string
        memo_placeholder: string
        save_memo: string

        // New Features Update (Week 4) - Upstream
        // Auth
        forgot_password: string
        reset_password: string
        email_placeholder: string
        send_reset_link: string
        back_to_login: string
        new_password_label: string
        confirm_password_label: string
        reset_success: string
        reset_error: string
        signup_email_required: string

        // Account
        delete_account: string
        delete_account_warning: string
        delete_account_confirm_label: string
        delete_account_button: string
        account_deleted: string

        // Memos Management
        manage_memos: string
        memo_renamed: string
        memo_deleted: string
        confirm_delete_memo: string

        // Projects Management
        manage_projects: string
        edit_project: string
        project_updated: string
        project_deleted: string
        confirm_delete_project: string
        edit: string
        delete: string

        // Background Settings
        bg_settings: string
        enable_bg: string
        select_bg: string

        // Share
        share: string
        link_copied: string
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
                confirm_clear_history: "정말로 모든 채팅 기록을 삭제하시겠습니까?",
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
                theme_light: "라이트",
                theme_dark: "다크",
                theme_system: "시스템",
                language_section: "언어",
                system_section: "시스템 관리",
                clear_history: "채팅 기록 삭제",
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
                cat_finance: "금융/자산",
                cat_travel: "여행 계획",
                cat_coding: "프로그래밍",

                // Memo
                memo_title: "메모",
                memo_placeholder: "여기에 메모를 작성하세요...",
                save_memo: "메모 저장",

                // Update Week 4
                forgot_password: "비밀번호를 잊으셨나요?",
                reset_password: "비밀번호 재설정",
                email_placeholder: "name@example.com",
                send_reset_link: "재설정 링크 보내기",
                back_to_login: "로그인으로 돌아가기",
                new_password_label: "새 비밀번호",
                confirm_password_label: "비밀번호 확인",
                reset_success: "비밀번호가 성공적으로 변경되었습니다.",
                reset_error: "비밀번호 변경 중 오류가 발생했습니다.",
                signup_email_required: "학교 이메일을 입력해주세요.",

                delete_account: "계정 탈퇴",
                delete_account_warning: "계정을 탈퇴하시면 모든 데이터가 영구적으로 삭제됩니다. 이 작업은 되돌릴 수 없습니다.",
                delete_account_confirm_label: "탈퇴를 확인하려면 DELETE를 입력하세요",
                delete_account_button: "계정 탈퇴",
                account_deleted: "계정 탈퇴가 완료되었습니다.",

                manage_memos: "메모 관리",
                memo_renamed: "메모 이름이 변경되었습니다.",
                memo_deleted: "메모가 삭제되었습니다.",
                confirm_delete_memo: "이 메모를 삭제하시겠습니까?",

                manage_projects: "프로젝트 관리",
                edit_project: "프로젝트 수정",
                project_updated: "프로젝트가 업데이트되었습니다.",
                project_deleted: "프로젝트가 삭제되었습니다.",
                confirm_delete_project: "이 프로젝트를 삭제하시겠습니까?",
                edit: "수정",
                delete: "삭제",

                // Background Settings
                bg_settings: "배경 설정",
                enable_bg: "대학 배경 화면 켜기",
                select_bg: "배경 이미지 선택",
                share: "공유",
                link_copied: "링크가 복사되었습니다."
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
                confirm_clear_history: "Are you sure you want to clear all chat history?",
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
                theme_light: "Light",
                theme_dark: "Dark",
                theme_system: "System",
                language_section: "Language",
                system_section: "System",
                clear_history: "Clear Chat History",
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
                cat_finance: "Finance",
                cat_travel: "Travel",
                cat_coding: "Coding",

                // Memo
                memo_title: "Memo Pad",
                memo_placeholder: "Write your notes here...",
                save_memo: "Save Memo",

                // Update Week 4
                forgot_password: "Forgot password?",
                reset_password: "Reset Password",
                email_placeholder: "name@example.com",
                send_reset_link: "Send Reset Link",
                back_to_login: "Back to Login",
                new_password_label: "New Password",
                confirm_password_label: "Confirm Password",
                reset_success: "Password successfully reset.",
                reset_error: "Error resetting password.",
                signup_email_required: "Please enter your university email.",

                delete_account: "Delete Account",
                delete_account_warning: "Deleting your account will permanently remove all data. This action cannot be undone.",
                delete_account_confirm_label: "Type DELETE to confirm",
                delete_account_button: "Permanently Delete Account",
                account_deleted: "Account deleted.",

                manage_memos: "Manage Memos",
                memo_renamed: "Memo renamed.",
                memo_deleted: "Memo deleted.",
                confirm_delete_memo: "Are you sure you want to delete this memo?",

                manage_projects: "Manage Projects",
                edit_project: "Edit Project",
                project_updated: "Project updated.",
                project_deleted: "Project deleted.",
                confirm_delete_project: "Are you sure you want to delete this project?",
                edit: "Edit",
                delete: "Delete",

                // Background Settings
                bg_settings: "Background Settings",
                enable_bg: "Enable University Background",
                select_bg: "Select Background Image",
                share: "Share",
                link_copied: "Link copied to clipboard."
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
                confirm_clear_history: "Haqiqatan ham barcha chat tarixini o'chirib tashlamoqchimisiz?",
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
                theme_light: "Yorug'",
                theme_dark: "Tungi",
                theme_system: "Tizim",
                language_section: "Til",
                system_section: "Tizim",
                clear_history: "Chat tarixini tozalash",
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
                cat_finance: "Moliya",
                cat_travel: "Sayohat",
                cat_coding: "Dasturlash",

                // Memo
                memo_title: "Eslatmalar",
                memo_placeholder: "Eslatmalaringizni shu yerga yozing...",
                save_memo: "Saqlash",

                // Update Week 4
                forgot_password: "Parolni unutdingizmi?",
                reset_password: "Parolni tiklash",
                email_placeholder: "name@example.com",
                send_reset_link: "Tiklash havolasini yuborish",
                back_to_login: "Kirishga qaytish",
                new_password_label: "Yangi parol",
                confirm_password_label: "Parolni tasdiqlash",
                reset_success: "Parol muvaffaqiyatli o'zgartirildi.",
                reset_error: "Parolni o'zgartirishda xatolik yuz berdi.",
                signup_email_required: "Universitet emailini kiriting.",

                delete_account: "Hisobni o'chirish",
                delete_account_warning: "Hisobingizni o'chirsangiz, barcha ma'lumotlar butunlay yo'qoladi. Bu amalni qaytarib bo'lmaydi.",
                delete_account_confirm_label: "Tasdiqlash uchun DELETE deb yozing",
                delete_account_button: "Hisobni butunlay o'chirish",
                account_deleted: "Hisob o'chirildi.",

                manage_memos: "Eslatmalarni boshqarish",
                memo_renamed: "Eslatma nomi o'zgartirildi.",
                memo_deleted: "Eslatma o'chirildi.",
                confirm_delete_memo: "Bu eslatmani o'chirishga ishonchingiz komilmi?",

                manage_projects: "Loyihalarni boshqarish",
                edit_project: "Loyihani tahrirlash",
                project_updated: "Loyiha yangilandi.",
                project_deleted: "Loyiha o'chirildi.",
                confirm_delete_project: "Bu loyihani o'chirishga ishonchingiz komilmi?",
                edit: "Tahrirlash",
                delete: "O'chirish",

                // Background Settings
                bg_settings: "Orqa Fon Sozlamalari",
                enable_bg: "Universitet Fonini Yoqish",
                select_bg: "Fon Rasmini Tanlash",
                share: "Ulashish",
                link_copied: "Havola nusxalandi."
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
