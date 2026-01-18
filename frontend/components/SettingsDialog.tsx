"use client"

import * as React from "react"
import { useAuth } from "@/components/auth-provider"
import { useTheme } from "next-themes"
import { api } from "@/services/api"
import { useLanguage } from "@/components/layout/language-context"
import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { X, User, Moon, Sun, LogOut, Trash2 } from "lucide-react"
import { useBackground } from "@/components/layout/background-provider"
import { Switch } from "@/components/ui/Switch"

interface SettingsDialogProps {
    open: boolean
    onClose: () => void
}

export function SettingsDialog({ open, onClose }: SettingsDialogProps) {
    const { user, updateUser, logout } = useAuth()
    const { theme, setTheme } = useTheme()
    const { language, setLanguage, t } = useLanguage()
    const { settings, updateSettings, availableImages } = useBackground()

    // Local state for profile inputs to avoid excessive re-renders/writes
    const [name, setName] = React.useState(user?.name || "")
    const [deleteConfirm, setDeleteConfirm] = React.useState("")
    const [isDeleting, setIsDeleting] = React.useState(false)
    const [showDeleteModal, setShowDeleteModal] = React.useState(false)

    React.useEffect(() => {
        if (user) setName(user.name)
    }, [user])

    const handleSaveProfile = () => {
        updateUser({ name })
    }

    const handleDeleteAccount = async () => {
        if (deleteConfirm === "DELETE") {
            setIsDeleting(true)
            try {
                // Use the real API service
                await api.deleteAccount()
                alert(t.account_deleted || "Account deleted successfully.")
                logout()
            } catch (error) {
                console.error("Delete account failed", error)
                alert("Failed to delete account.")
                setIsDeleting(false)
            }
        }
    }

    if (!open) return null

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <Card className="w-full max-w-sm max-h-[85vh] flex flex-col bg-white dark:bg-zinc-900 border-2 border-zinc-200 dark:border-zinc-800 shadow-[8px_8px_0px_0px_rgba(0,0,0,0.1)] dark:shadow-[8px_8px_0px_0px_rgba(255,255,255,0.05)] overflow-hidden animate-in zoom-in-95 duration-200 rounded-xl">
                {/* Header */}
                <div className="flex items-center justify-between p-3 border-b-2 border-zinc-100 dark:border-zinc-800 shrink-0">
                    <h2 className="text-base font-bold text-zinc-900 dark:text-zinc-100 uppercase tracking-wide">{t.settings_title}</h2>
                    <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                        <X className="h-4 w-4 text-zinc-500" />
                    </button>
                </div>

                <div className="p-4 space-y-4 overflow-y-auto">
                    {/* 1. Profile Settings */}
                    <div className="space-y-3">
                        <h3 className="text-xs font-bold text-zinc-400 uppercase tracking-widest">{t.profile_section}</h3>
                        <div className="flex items-center gap-3">
                            <div className="relative group">
                                <div
                                    className="h-12 w-12 rounded-xl bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center border-2 border-zinc-200 dark:border-zinc-700 overflow-hidden shrink-0 cursor-pointer hover:scale-105 transition-transform shadow-sm"
                                    onClick={() => document.getElementById('avatar-upload')?.click()}
                                >
                                    {user?.avatar ? (
                                        <img src={user.avatar} alt="Avatar" className="h-full w-full object-cover" />
                                    ) : (
                                        <User className="h-5 w-5 text-zinc-400" />
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
                    <div className="space-y-2">
                        <h3 className="text-xs font-bold text-zinc-400 uppercase tracking-widest">{t.appearance_section}</h3>

                        <div className="grid grid-cols-2 gap-2">
                            <button
                                onClick={() => setTheme("light")}
                                className={`flex flex-col items-center justify-center p-2 rounded-xl border-2 transition-all active:scale-95 ${theme === "light"
                                    ? "bg-red-50 border-red-200 text-red-600 shadow-[0_2px_0_0_rgba(239,68,68,0.2)]"
                                    : "border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700"
                                    }`}
                            >
                                <Sun className="h-4 w-4 mb-1" />
                                <span className="text-[10px] font-bold uppercase">{t.theme_light}</span>
                            </button>
                            <button
                                onClick={() => setTheme("dark")}
                                className={`flex flex-col items-center justify-center p-2 rounded-xl border-2 transition-all active:scale-95 ${theme === "dark"
                                    ? "bg-zinc-800 border-zinc-700 text-zinc-100 shadow-[0_2px_0_0_rgba(255,255,255,0.1)]"
                                    : "border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700"
                                    }`}
                            >
                                <Moon className="h-4 w-4 mb-1" />
                                <span className="text-[10px] font-bold uppercase">{t.theme_dark}</span>
                            </button>

                        </div>

                        {/* Background Settings */}
                        <div className="pt-4 mt-2 border-t border-zinc-100 dark:border-zinc-800">
                            <div className="flex items-center justify-between mb-3">
                                <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300">{t.enable_bg}</label>
                                <Switch
                                    checked={settings.enabled}
                                    onCheckedChange={(checked) => updateSettings({ enabled: checked })}
                                />
                            </div>

                            {settings.enabled && (
                                <div className="grid grid-cols-2 gap-2 animate-in slide-in-from-top-2">
                                    {availableImages.map((img) => (
                                        <button
                                            key={img.id}
                                            onClick={() => updateSettings({ image: img.src })}
                                            className={`relative aspect-video rounded-lg overflow-hidden border-2 transition-all ${settings.image === img.src
                                                ? "border-red-500 ring-2 ring-red-200"
                                                : "border-zinc-200 dark:border-zinc-700 opacity-70 hover:opacity-100"
                                                }`}
                                        >
                                            <div className="absolute inset-0">
                                                <img src={img.src} alt={img.name} className="w-full h-full object-cover" />
                                            </div>
                                            {settings.image === img.src && (
                                                <div className="absolute inset-0 bg-red-500/10 flex items-center justify-center">
                                                    <div className="bg-white rounded-full p-1 shadow-sm">
                                                        <div className="w-2 h-2 bg-red-600 rounded-full" />
                                                    </div>
                                                </div>
                                            )}
                                        </button>
                                    ))}
                                </div>
                            )}
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

                    {/* Danger Zone */}
                    <div className="pt-2 border-t border-zinc-100 dark:border-zinc-800">
                        <h3 className="text-sm font-medium text-red-600 uppercase tracking-wider mb-2">{t.delete_account}</h3>
                        <Button
                            variant="outline"
                            className="w-full justify-start text-red-600 border-red-200 hover:bg-red-50 dark:border-red-900/50 dark:hover:bg-red-900/20"
                            onClick={() => setShowDeleteModal(true)}
                        >
                            <Trash2 className="h-4 w-4 mr-2" />
                            {t.delete_account_button}
                        </Button>
                    </div>

                    {/* 3. System Actions */}
                    <div className="space-y-3 pt-2 border-t border-zinc-100 dark:border-zinc-800">

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

            {/* Delete Confirmation Modal */}
            {
                showDeleteModal && (
                    <div className="absolute inset-0 z-[60] flex items-center justify-center bg-black/60 p-4">
                        <Card className="w-full max-w-sm bg-white dark:bg-zinc-900 shadow-2xl animate-in zoom-in-95">
                            <div className="p-6 space-y-4">
                                <h3 className="text-lg font-bold text-red-600">{t.delete_account}</h3>
                                <p className="text-sm text-zinc-600 dark:text-zinc-400">{t.delete_account_warning}</p>

                                <div className="space-y-2">
                                    <label className="text-xs font-bold text-zinc-500">{t.delete_account_confirm_label}</label>
                                    <Input
                                        value={deleteConfirm}
                                        onChange={(e) => setDeleteConfirm(e.target.value)}
                                        placeholder="DELETE"
                                        className="border-red-200 focus:border-red-500"
                                    />
                                </div>

                                <div className="flex gap-2 pt-2">
                                    <Button
                                        variant="ghost"
                                        className="flex-1"
                                        onClick={() => {
                                            setShowDeleteModal(false)
                                            setDeleteConfirm("")
                                        }}
                                    >
                                        Cancel
                                    </Button>
                                    <Button
                                        className="flex-1 bg-red-600 hover:bg-red-700 text-white"
                                        disabled={deleteConfirm !== "DELETE" || isDeleting}
                                        onClick={handleDeleteAccount}
                                    >
                                        {isDeleting ? "Deleting..." : t.delete_account_button}
                                    </Button>
                                </div>
                            </div>
                        </Card>
                    </div>
                )
            }
        </div >
    )
}
