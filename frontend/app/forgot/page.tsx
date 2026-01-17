"use client"

import * as React from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/Card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ArrowLeft, Search, RefreshCw } from "lucide-react"
import { api } from "@/services/api"
import { useLanguage } from "@/components/layout/language-context"

export default function ForgotPage() {
    const { t } = useLanguage()
    const router = useRouter()

    // Find ID States
    const [findIdEmail, setFindIdEmail] = React.useState("")
    const [foundedId, setFoundedId] = React.useState("")
    const [isFinding, setIsFinding] = React.useState(false)

    // Reset Password States
    const [resetId, setResetId] = React.useState("")
    const [resetEmail, setResetEmail] = React.useState("")
    const [newPassword, setNewPassword] = React.useState("")
    const [isResetting, setIsResetting] = React.useState(false)

    const handleFindId = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            setIsFinding(true)
            const id = await api.findId(findIdEmail)
            setFoundedId(id)
            alert(`Your User ID is: ${id}`)
        } catch (error) {
            alert("Failed to find ID: " + (error as Error).message)
            setFoundedId("")
        } finally {
            setIsFinding(false)
        }
    }

    const handleResetPassword = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            setIsResetting(true)
            await api.resetPassword(resetId, resetEmail, newPassword)
            alert("Password reset successful! Please login with your new password.")
            router.push("/login")
        } catch (error) {
            alert("Failed to reset password: " + (error as Error).message)
        } finally {
            setIsResetting(false)
        }
    }

    return (
        <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-zinc-50 dark:bg-zinc-950">
            {/* Background Gradients */}
            <div className="absolute inset-0 z-0">
                <div className="absolute -left-20 -top-20 h-[500px] w-[500px] rounded-full bg-red-200/40 blur-[100px] dark:bg-red-900/20" />
                <div className="absolute -bottom-20 -right-20 h-[500px] w-[500px] rounded-full bg-blue-200/40 blur-[100px] dark:bg-blue-900/20" />
            </div>

            <Card className="z-10 w-full max-w-md border-zinc-200/50 bg-white/80 shadow-2xl backdrop-blur-xl dark:border-zinc-800/50 dark:bg-zinc-900/80">
                <CardHeader className="text-center">
                    <CardTitle className="text-2xl font-bold">Account Recovery</CardTitle>
                    <CardDescription>Find your ID or reset your password</CardDescription>
                </CardHeader>
                <CardContent>
                    <Tabs defaultValue="find-id" className="w-full">
                        <TabsList className="grid w-full grid-cols-2 mb-4">
                            <TabsTrigger value="find-id">Find ID</TabsTrigger>
                            <TabsTrigger value="reset-pass">Reset Password</TabsTrigger>
                        </TabsList>

                        <TabsContent value="find-id">
                            <form onSubmit={handleFindId} className="space-y-4">
                                <div className="space-y-2">
                                    <label className="text-xs font-medium text-zinc-500 uppercase">Registered Email</label>
                                    <Input
                                        type="email"
                                        placeholder="Enter your email"
                                        value={findIdEmail}
                                        onChange={(e) => setFindIdEmail(e.target.value)}
                                        required
                                        className="bg-zinc-50/50 dark:bg-zinc-900/50"
                                    />
                                </div>
                                {foundedId && (
                                    <div className="p-3 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-md text-center text-sm font-medium">
                                        Your ID: {foundedId}
                                    </div>
                                )}
                                <Button type="submit" className="w-full bg-red-600 hover:bg-red-700 text-white" disabled={isFinding}>
                                    {isFinding ? "Searching..." : "Find ID"} <Search className="ml-2 h-4 w-4" />
                                </Button>
                            </form>
                        </TabsContent>

                        <TabsContent value="reset-pass">
                            <form onSubmit={handleResetPassword} className="space-y-4">
                                <div className="space-y-2">
                                    <label className="text-xs font-medium text-zinc-500 uppercase">User ID</label>
                                    <Input
                                        type="text"
                                        placeholder="Enter your ID"
                                        value={resetId}
                                        onChange={(e) => setResetId(e.target.value)}
                                        required
                                        className="bg-zinc-50/50 dark:bg-zinc-900/50"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs font-medium text-zinc-500 uppercase">Email</label>
                                    <Input
                                        type="email"
                                        placeholder="Enter your email"
                                        value={resetEmail}
                                        onChange={(e) => setResetEmail(e.target.value)}
                                        required
                                        className="bg-zinc-50/50 dark:bg-zinc-900/50"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs font-medium text-zinc-500 uppercase">New Password</label>
                                    <Input
                                        type="password"
                                        placeholder="New password (min 8 chars)"
                                        value={newPassword}
                                        onChange={(e) => setNewPassword(e.target.value)}
                                        required
                                        minLength={8}
                                        className="bg-zinc-50/50 dark:bg-zinc-900/50"
                                    />
                                </div>
                                <Button type="submit" className="w-full bg-red-600 hover:bg-red-700 text-white" disabled={isResetting}>
                                    {isResetting ? "Resetting..." : "Reset Password"} <RefreshCw className="ml-2 h-4 w-4" />
                                </Button>
                            </form>
                        </TabsContent>
                    </Tabs>
                </CardContent>
                <CardFooter className="justify-center pt-2">
                    <Link href="/login" className="flex items-center text-sm font-medium text-zinc-500 hover:text-red-600 transition-colors">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Login
                    </Link>
                </CardFooter>
            </Card>
        </div>
    )
}
