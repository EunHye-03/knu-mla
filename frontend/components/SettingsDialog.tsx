"use client"

import * as React from "react"
import { useAuth } from "@/components/auth-provider"
import { useTheme } from "next-themes"
import { useLanguage } from "@/components/layout/language-context"
import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { X, User, Moon, Sun, Monitor, LogOut, Trash2 } from "lucide-react"

interface SettingsDialogProps {
    open: boolean
    onClose: () => void
}

export function SettingsDialog({ open, onClose }: SettingsDialogProps) {
    const { user, updateUser, logout } = useAuth()
    const { theme, setTheme } = useTheme()
    const { language, setLanguage, t } = useLanguage()

    // Local state for profile inputs to avoid excessive re-renders/writes
    const [name, setName] = React.useState(user?.name || "")

    React.useEffect(() => {
        if (user) setName(user.name)
    }, [user])

    const handleSaveProfile = () => {
        updateUser({ name })
    }

    if (!open) return null

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <Card className="w-full max-w-lg bg-white dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
                {/* Header */}
                <div className="flex items-center justify-between p-4 border-b border-zinc-100 dark:border-zinc-800">
                    <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">{t.settings_title}</h2>
                    <button onClick={onClose} className="p-2 rounded-md hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                        <X className="h-5 w-5 text-zinc-500" />
                    </button>
                </div>

                <div className="p-6 space-y-8">
                    {/* 1. Profile Settings */}
                    <div className="space-y-4">
                        <h3 className="text-sm font-medium text-zinc-500 uppercase tracking-wider">{t.profile_section}</h3>
                        <div className="flex items-start gap-4">
                            <div className="relative group">
                                <div
                                    className="h-16 w-16 rounded-full bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center border border-zinc-200 dark:border-zinc-700 overflow-hidden shrink-0 cursor-pointer hover:opacity-80 transition-opacity"
                                    onClick={() => document.getElementById('avatar-upload')?.click()}
                                >
                                    {user?.avatar ? (
                                        <img src={user.avatar} alt="Avatar" className="h-full w-full object-cover" />
                                    ) : (
                                        <User className="h-8 w-8 text-zinc-400" />
                                    )}
                                    <div className="absolute inset-0 bg-black/30 hidden group-hover:flex items-center justify-center">
                                        <span className="text-xs text-white font-medium">Edit</span>
                                    </div>
                                </div>
                                <input
                                    id="avatar-upload"
                                    type="file"
                                    accept="image/*"
                                    className="hidden"
                                    onChange={(e) => {
                                        const file = e.target.files?.[0];
                                        if (file) {
                                            const reader = new FileReader();
                                            reader.onloadend = () => {
                                                updateUser({ avatar: reader.result as string });
                                            };
                                            reader.readAsDataURL(file);
                                        }
                                    }}
                                />
                            </div>
                            <div className="flex-1 space-y-3">
                                <div>
                                    <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300">{t.name_input_label}</label>
                                    <Input
                                        value={name}
                                        onChange={(e) => setName(e.target.value)}
                                        onBlur={handleSaveProfile}
                                        className="mt-1.5"
                                    />
                                    <p className="text-xs text-zinc-500 mt-1">{t.name_help}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* 2. Appearance */}
                    <div className="space-y-4">
                        <h3 className="text-sm font-medium text-zinc-500 uppercase tracking-wider">{t.appearance_section}</h3>

                        {/* Theme */}
                        <div className="grid grid-cols-3 gap-2">
                            <button
                                onClick={() => setTheme("light")}
                                className={`flex flex-col items-center justify-center p-3 rounded-xl border transition-all ${theme === "light"
                                    ? "bg-red-50 border-red-200 text-red-600 dark:bg-red-900/20 dark:border-red-800 dark:text-red-400"
                                    : "border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700"
                                    }`}
                            >
                                <Sun className="h-5 w-5 mb-2" />
                                <span className="text-xs font-medium">{t.theme_light}</span>
                            </button>
                            <button
                                onClick={() => setTheme("dark")}
                                className={`flex flex-col items-center justify-center p-3 rounded-xl border transition-all ${theme === "dark"
                                    ? "bg-red-50 border-red-200 text-red-600 dark:bg-red-900/20 dark:border-red-800 dark:text-red-400"
                                    : "border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700"
                                    }`}
                            >
                                <Moon className="h-5 w-5 mb-2" />
                                <span className="text-xs font-medium">{t.theme_dark}</span>
                            </button>
                            <button
                                onClick={() => setTheme("system")}
                                className={`flex flex-col items-center justify-center p-3 rounded-xl border transition-all ${theme === "system"
                                    ? "bg-red-50 border-red-200 text-red-600 dark:bg-red-900/20 dark:border-red-800 dark:text-red-400"
                                    : "border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700"
                                    }`}
                            >
                                <Monitor className="h-5 w-5 mb-2" />
                                <span className="text-xs font-medium">{t.theme_system}</span>
                            </button>
                        </div>

                        {/* Language */}
                        <div className="pt-2">
                            <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2 block">{t.language_section}</label>
                            <div className="grid grid-cols-3 gap-2">
                                {['uz', 'en', 'kr'].map((lang) => (
                                    <button
                                        key={lang}
                                        onClick={() => setLanguage(lang.toUpperCase() as any)}
                                        className={`px-3 py-2 rounded-lg text-sm font-medium border transition-all ${language === lang.toUpperCase()
                                            ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900 border-zinc-900 dark:border-zinc-100"
                                            : "bg-transparent border-zinc-200 dark:border-zinc-800 text-zinc-600 dark:text-zinc-400"
                                            }`}
                                    >
                                        {lang.toUpperCase()}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* 3. System Actions */}
                    <div className="space-y-3 pt-2 border-t border-zinc-100 dark:border-zinc-800">
                        <Button
                            variant="ghost"
                            className="w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20"
                            onClick={() => {
                                if (confirm(t.confirm_clear_history)) {
                                    // Clear history logic here (if we had persistent history)
                                }
                            }}
                        >
                            <Trash2 className="h-4 w-4 mr-2" />
                            {t.clear_history}
                        </Button>
                        <Button
                            variant="ghost"
                            className="w-full justify-start text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                            onClick={logout}
                        >
                            <LogOut className="h-4 w-4 mr-2" />
                            {t.logout}
                        </Button>
                        <Button
                            variant="primary"
                            className="w-full justify-center bg-zinc-900 text-white hover:bg-zinc-800 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200 mt-4"
                            onClick={() => {
                                handleSaveProfile(); // Ensure name is saved
                                onClose();
                            }}
                        >
                            {t.save}
                        </Button>
                    </div>
                </div>
            </Card>
        </div>
    )
}
