"use client"

import * as React from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/Card"
import { ArrowLeft, Mail, CheckCircle, AlertCircle } from "lucide-react"
import { useLanguage } from "@/components/layout/language-context"
import { api } from "@/services/api"

export default function ForgotPasswordPage() {
    const { t } = useLanguage()
    const router = useRouter()
    const [email, setEmail] = React.useState("")
    const [isLoading, setIsLoading] = React.useState(false)
    const [status, setStatus] = React.useState<"idle" | "success" | "error">("idle")
    const [errorMessage, setErrorMessage] = React.useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        if (!email || !email.includes("@")) {
            setStatus("error")
            setErrorMessage(t.signup_email_required || "Please enter a valid email address")
            return
        }

        setIsLoading(true)
        setStatus("idle")
        setErrorMessage("")

        try {
            console.log("[Forgot Password] Requesting reset for:", email)
            const response = await api.requestPasswordReset(email)
            console.log("[Forgot Password] Response:", response)

            setStatus("success")

            // Auto redirect to login after 3 seconds
            setTimeout(() => {
                router.push("/login")
            }, 10000)
        } catch (error) {
            console.error("[Forgot Password] Error:", error)
            // For security, we still show success message even on error
            // This prevents email enumeration attacks
            setStatus("success")
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-zinc-50 dark:bg-zinc-950">
            {/* Background Decoration */}
            <div className="absolute inset-0 z-0 opacity-50">
                <div className="absolute top-20 left-20 h-64 w-64 rounded-full bg-red-200/30 blur-[80px] dark:bg-red-900/20" />
                <div className="absolute bottom-20 right-20 h-64 w-64 rounded-full bg-blue-200/30 blur-[80px] dark:bg-blue-900/20" />
            </div>

            <Card className="z-10 w-full max-w-md border-zinc-200/50 bg-white/80 shadow-2xl backdrop-blur-xl dark:border-zinc-800/50 dark:bg-zinc-900/80 animate-in fade-in zoom-in duration-300">
                <CardHeader className="text-center pb-4">
                    <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br from-red-500 to-red-700 text-white shadow-lg">
                        <Mail className="h-7 w-7" />
                    </div>
                    <CardTitle className="text-2xl font-bold">{t.reset_password}</CardTitle>
                    <CardDescription className="text-base">
                        {status === "success"
                            ? t.reset_success || "Check your email for reset instructions"
                            : "Enter your email address and we'll send you a reset link"}
                    </CardDescription>
                </CardHeader>

                {status === "success" ? (
                    <CardContent className="pt-4">
                        <div className="flex flex-col items-center justify-center py-6 space-y-4">
                            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
                                <CheckCircle className="h-8 w-8 text-green-600 dark:text-green-400" />
                            </div>
                            <div className="text-center space-y-4">
                                <p className="text-sm font-medium text-green-600 dark:text-green-400">
                                    Reset link sent!
                                </p>
                                <p className="text-xs text-zinc-500 dark:text-zinc-400">
                                    If an account exists for <span className="font-semibold">{email}</span>, you will receive a password reset link shortly.
                                </p>

                                <div className="pt-2">
                                    <Link href={`/reset-password?token=demo_token_${Date.now()}`} className="text-xs text-blue-500 hover:text-blue-600 underline">
                                        (Demo) Click here to simulate email link
                                    </Link>
                                </div>

                                <p className="text-xs text-zinc-400 dark:text-zinc-500 pt-2">
                                    Redirecting to login in 5 seconds...
                                </p>
                            </div>
                        </div>
                    </CardContent>
                ) : (
                    <form onSubmit={handleSubmit}>
                        <CardContent className="space-y-4 pt-4">
                            {status === "error" && errorMessage && (
                                <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-900/50">
                                    <AlertCircle className="h-4 w-4 text-red-600 dark:text-red-400 flex-shrink-0" />
                                    <p className="text-sm text-red-600 dark:text-red-400">{errorMessage}</p>
                                </div>
                            )}

                            <div className="space-y-2">
                                <label className="text-xs font-medium text-zinc-500 uppercase tracking-wider">
                                    {t.email_label}
                                </label>
                                <Input
                                    type="email"
                                    placeholder={t.email_placeholder || "name@university.edu"}
                                    className="bg-zinc-50/50 border-zinc-200 focus:border-red-500 focus:ring-red-500/20 dark:bg-zinc-900/50 dark:border-zinc-800 transition-all"
                                    value={email}
                                    onChange={(e) => {
                                        setEmail(e.target.value)
                                        setStatus("idle")
                                        setErrorMessage("")
                                    }}
                                    required
                                    disabled={isLoading}
                                />
                            </div>

                            <Button
                                type="submit"
                                disabled={isLoading || !email}
                                className="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-lg shadow-red-500/20 h-11 text-base font-medium transition-all hover:scale-[1.02] active:scale-[0.98]"
                            >
                                {isLoading ? (
                                    <span className="flex items-center gap-2">
                                        <span className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                                        Sending...
                                    </span>
                                ) : (
                                    t.send_reset_link || "Send Reset Link"
                                )}
                            </Button>
                        </CardContent>
                    </form>
                )}

                <CardFooter className="flex justify-center pt-2 pb-6">
                    <Link
                        href="/login"
                        className="flex items-center text-sm text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors group"
                    >
                        <ArrowLeft className="mr-2 h-4 w-4 group-hover:-translate-x-1 transition-transform" />
                        {t.back_to_login || "Back to Login"}
                    </Link>
                </CardFooter>
            </Card>
        </div>
    )
}
