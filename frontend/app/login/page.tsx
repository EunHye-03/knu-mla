"use client"

import * as React from "react"
import Link from "next/link"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/Card"
import { ArrowRight, Sparkles } from "lucide-react"
import { useAuth } from "@/components/auth-provider"

import { useLanguage } from "@/components/layout/language-context"

export default function LoginPage() {
    const { login } = useAuth()
    const { t, language, setLanguage } = useLanguage()
    const [id, setId] = React.useState("")
    const [password, setPassword] = React.useState("")

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        if (id && password) {
            login(id, password)
        }
    }

    return (
        <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-zinc-50 dark:bg-zinc-950">
            {/* Background Gradients */}
            <div className="absolute inset-0 z-0">
                <div className="absolute -left-20 -top-20 h-[500px] w-[500px] rounded-full bg-red-200/40 blur-[100px] dark:bg-red-900/20" />
                <div className="absolute -bottom-20 -right-20 h-[500px] w-[500px] rounded-full bg-blue-200/40 blur-[100px] dark:bg-blue-900/20" />
            </div>

            {/* Language Switcher */}
            <div className="absolute top-4 right-4 z-20 flex gap-2">
                {['uz', 'en', 'kr'].map((lang) => (
                    <button
                        key={lang}
                        onClick={() => setLanguage(lang.toUpperCase() as any)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${language === lang.toUpperCase()
                            ? "bg-red-600 text-white shadow-md shadow-red-500/20"
                            : "bg-white/50 text-zinc-600 hover:bg-white dark:bg-zinc-900/50 dark:text-zinc-400 dark:hover:bg-zinc-900"
                            }`}
                    >
                        {lang.toUpperCase()}
                    </button>
                ))}
            </div>

            <Card className="z-10 w-full max-w-md border-zinc-200/50 bg-white/80 shadow-2xl backdrop-blur-xl dark:border-zinc-800/50 dark:bg-zinc-900/80 animate-in fade-in zoom-in duration-500">
                <CardHeader className="space-y-1 text-center pb-2">
                    <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-red-500 to-red-700 text-white shadow-lg shadow-red-500/30 transform transition-transform hover:scale-105 duration-300">
                        <span className="text-3xl font-extrabold tracking-tight">K</span>
                    </div>
                    <CardTitle className="text-2xl font-bold tracking-tight">{t.login_title}</CardTitle>
                    <CardDescription className="text-base">
                        {t.login_subtitle}
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent className="space-y-4 pt-4">
                        <div className="space-y-2 group">
                            <label className="text-xs font-medium text-zinc-500 uppercase tracking-wider group-focus-within:text-red-600 transition-colors">{t.login_id_label}</label>
                            <Input
                                type="text"
                                placeholder={t.login_id_label}
                                className="bg-zinc-50/50 border-zinc-200 focus:border-red-500 focus:ring-red-500/20 dark:bg-zinc-900/50 dark:border-zinc-800 transition-all duration-300"
                                value={id}
                                onChange={(e) => setId(e.target.value)}
                                required
                            />
                        </div>
                        <div className="space-y-2 group">
                            <div className="flex items-center justify-between">
                                <label className="text-xs font-medium text-zinc-500 uppercase tracking-wider group-focus-within:text-red-600 transition-colors">{t.password_label}</label>
                            </div>
                            <Input
                                type="password"
                                placeholder="••••••••"
                                className="bg-zinc-50/50 border-zinc-200 focus:border-red-500 focus:ring-red-500/20 dark:bg-zinc-900/50 dark:border-zinc-800 transition-all duration-300"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                            <div className="flex justify-end">
                                <Link
                                    href="/forgot-password"
                                    className="text-xs text-red-600 hover:text-red-700 hover:underline font-medium"
                                >
                                    {t.forgot_password}
                                </Link>
                            </div>
                        </div>
                        <Button type="submit" className="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-lg shadow-red-500/20 h-11 text-base font-medium transition-all hover:scale-[1.02] active:scale-[0.98]">
                            {t.login_button} <ArrowRight className="ml-2 h-4 w-4" />
                        </Button>
                    </CardContent>
                </form>
                <CardFooter className="flex flex-col space-y-4 pt-2">
                    <div className="text-center text-sm text-zinc-500">
                        {t.no_account}{" "}
                        <Link href="/register" className="font-semibold text-red-600 hover:text-red-700 hover:underline">
                            {t.register_link}
                        </Link>
                    </div>
                    <div className="relative w-full">
                        <div className="absolute inset-0 flex items-center">
                            <span className="w-full border-t border-zinc-200 dark:border-zinc-800" />
                        </div>
                        <div className="relative flex justify-center text-xs uppercase">
                            <span className="bg-white/80 px-2 text-zinc-400 dark:bg-zinc-900/80">OR</span>
                        </div>
                    </div>
                    <div className="text-center w-full">
                        <Link href="/" className="inline-flex items-center text-sm text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 transition-colors group">
                            <Sparkles className="mr-2 h-4 w-4 text-amber-500 group-hover:rotate-12 transition-transform" />
                            {t.demo_link}
                        </Link>
                    </div>
                </CardFooter>
            </Card>
        </div>
    )
}
