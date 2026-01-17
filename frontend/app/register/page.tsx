"use client"

import * as React from "react"
import Link from "next/link"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/Card"
import { ArrowRight } from "lucide-react"
import { useAuth } from "@/components/auth-provider"

import { useLanguage } from "@/components/layout/language-context"

export default function RegisterPage() {
    const { register } = useAuth()
    const { t } = useLanguage()
    const [name, setName] = React.useState("")
    const [email, setEmail] = React.useState("")
    const [id, setId] = React.useState("")
    const [password, setPassword] = React.useState("")

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        if (name && id && password && email) {
            register(name, id, password, email)
        }
    }

    return (
        <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-zinc-50 dark:bg-zinc-950">
            {/* Background Gradients */}
            <div className="absolute inset-0 z-0">
                <div className="absolute -left-20 -top-20 h-[500px] w-[500px] rounded-full bg-red-200/40 blur-[100px] dark:bg-red-900/20" />
                <div className="absolute -bottom-20 -right-20 h-[500px] w-[500px] rounded-full bg-blue-200/40 blur-[100px] dark:bg-blue-900/20" />
            </div>

            <Card className="z-10 w-full max-w-md border-zinc-200/50 bg-white/80 shadow-2xl backdrop-blur-xl dark:border-zinc-800/50 dark:bg-zinc-900/80 animate-in fade-in zoom-in duration-500">
                <CardHeader className="space-y-1 text-center pb-2">
                    <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-red-500 to-red-700 text-white shadow-lg shadow-red-500/30">
                        <span className="text-3xl font-extrabold tracking-tight">K</span>
                    </div>
                    <CardTitle className="text-2xl font-bold tracking-tight">{t.register_title}</CardTitle>
                    <CardDescription className="text-base">
                        KNU Multilingual Assistant
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent className="space-y-4 pt-4">
                        <div className="space-y-2 group">
                            <label className="text-xs font-medium text-zinc-500 uppercase tracking-wider group-focus-within:text-red-600 transition-colors">{t.name_label}</label>
                            <Input
                                type="text"
                                placeholder={t.name_label}
                                className="bg-zinc-50/50 border-zinc-200 focus:border-red-500 focus:ring-red-500/20 dark:bg-zinc-900/50 dark:border-zinc-800 transition-all duration-300"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required
                            />
                        </div>

                        <div className="space-y-2 group">
                            <label className="text-xs font-medium text-zinc-500 uppercase tracking-wider group-focus-within:text-red-600 transition-colors">{t.email_label}</label>
                            <Input
                                type="email"
                                placeholder={t.email_label}
                                className="bg-zinc-50/50 border-zinc-200 focus:border-red-500 focus:ring-red-500/20 dark:bg-zinc-900/50 dark:border-zinc-800 transition-all duration-300"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
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
                            <label className="text-xs font-medium text-zinc-500 uppercase tracking-wider group-focus-within:text-red-600 transition-colors">{t.password_label}</label>
                            <Input
                                type="password"
                                placeholder={t.password_label}
                                className="bg-zinc-50/50 border-zinc-200 focus:border-red-500 focus:ring-red-500/20 dark:bg-zinc-900/50 dark:border-zinc-800 transition-all duration-300"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                minLength={8}
                            />
                        </div>
                        <Button type="submit" className="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-lg shadow-red-500/20 h-11 text-base font-medium transition-all hover:scale-[1.02] active:scale-[0.98]">
                            {t.register_button} <ArrowRight className="ml-2 h-4 w-4" />
                        </Button>
                    </CardContent>
                </form>
                <CardFooter className="flex flex-col space-y-4 pt-2">
                    <div className="text-center text-sm text-zinc-500">
                        {t.have_account}{" "}
                        <Link href="/login" className="font-semibold text-red-600 hover:text-red-700 hover:underline">
                            {t.login_link}
                        </Link>
                    </div>
                </CardFooter>
            </Card>
        </div>
    )
}
