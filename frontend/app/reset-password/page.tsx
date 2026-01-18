"use client"

import * as React from "react"
import Link from "next/link"
import { useSearchParams, useRouter } from "next/navigation"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/Card"
import { Lock, ArrowLeft, CheckCircle, AlertCircle } from "lucide-react"
import { useLanguage } from "@/components/layout/language-context"
import { api } from "@/services/api"

export default function ResetPasswordPage() {
    const { t } = useLanguage()
    const router = useRouter()
    const searchParams = useSearchParams()
    const token = searchParams.get('token')

    const [password, setPassword] = React.useState("")
    const [confirmPassword, setConfirmPassword] = React.useState("")
    const [isLoading, setIsLoading] = React.useState(false)
    const [status, setStatus] = React.useState<'idle' | 'success' | 'error'>('idle')

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (password !== confirmPassword) {
            alert("Passwords do not match")
            return
        }
        if (!token) {
            alert("Invalid reset token")
            return
        }

        setIsLoading(true)
        try {
            await api.resetPasswordWithToken(token, password)
            setStatus('success')
            setTimeout(() => {
                router.push('/login')
            }, 3000)
        } catch (error) {
            console.error("Reset failed", error)
            setStatus('error')
        } finally {
            setIsLoading(false)
        }
    }

    if (!token) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-zinc-950 p-4">
                <Card className="w-full max-w-md">
                    <CardContent className="pt-6 text-center">
                        <AlertCircle className="mx-auto h-12 w-12 text-red-500 mb-4" />
                        <p className="text-zinc-900 dark:text-zinc-100 mb-4">Invalid or missing reset token.</p>
                        <Link href="/login" className="text-red-600 hover:underline">Return to Login</Link>
                    </CardContent>
                </Card>
            </div>
        )
    }

    return (
        <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-zinc-50 dark:bg-zinc-950">
            <Card className="z-10 w-full max-w-md border-zinc-200/50 bg-white/80 shadow-2xl backdrop-blur-xl dark:border-zinc-800/50 dark:bg-zinc-900/80">
                <CardHeader className="text-center pb-2">
                    <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400">
                        <Lock className="h-6 w-6" />
                    </div>
                    <CardTitle className="text-xl font-bold">{t.reset_password}</CardTitle>
                </CardHeader>

                {status === 'success' ? (
                    <CardContent className="text-center space-y-4 pt-4">
                        <CheckCircle className="mx-auto h-16 w-16 text-green-500 animate-in zoom-in duration-300" />
                        <p className="text-lg font-medium text-zinc-900 dark:text-zinc-100">{t.reset_success}</p>
                        <p className="text-sm text-zinc-500">Redirecting to login...</p>
                    </CardContent>
                ) : (
                    <form onSubmit={handleSubmit}>
                        <CardContent className="space-y-4 pt-4">
                            <div className="space-y-2">
                                <label className="text-xs font-medium text-zinc-500 uppercase tracking-wider">{t.new_password_label}</label>
                                <Input
                                    type="password"
                                    placeholder="••••••••"
                                    className="bg-zinc-50/50 border-zinc-200 focus:border-red-500 focus:ring-red-500/20 dark:bg-zinc-900/50 dark:border-zinc-800"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    minLength={8}
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs font-medium text-zinc-500 uppercase tracking-wider">{t.confirm_password_label}</label>
                                <Input
                                    type="password"
                                    placeholder="••••••••"
                                    className="bg-zinc-50/50 border-zinc-200 focus:border-red-500 focus:ring-red-500/20 dark:bg-zinc-900/50 dark:border-zinc-800"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    required
                                    minLength={8}
                                />
                            </div>

                            {status === 'error' && (
                                <p className="text-sm text-red-600 text-center">{t.reset_error}</p>
                            )}

                            <Button
                                type="submit"
                                disabled={isLoading}
                                className="w-full bg-red-600 hover:bg-red-700 text-white"
                            >
                                {isLoading ? "Resetting..." : t.reset_password}
                            </Button>
                        </CardContent>
                    </form>
                )}

                {status !== 'success' && (
                    <CardFooter className="flex justify-center pt-2">
                        <Link href="/login" className="flex items-center text-sm text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors">
                            <ArrowLeft className="mr-2 h-4 w-4" />
                            {t.back_to_login}
                        </Link>
                    </CardFooter>
                )}
            </Card>
        </div>
    )
}
