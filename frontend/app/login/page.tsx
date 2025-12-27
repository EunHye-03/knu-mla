"use client"

import Link from "next/link"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/Card"

export default function LoginPage() {
    return (
        <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-zinc-950">
            <Card className="w-full max-w-md border-zinc-200 shadow-lg dark:border-zinc-800">
                <CardHeader className="space-y-1 text-center">
                    <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-red-600 text-white font-bold text-xl">
                        K
                    </div>
                    <CardTitle className="text-2xl font-bold tracking-tight">Xush Kelibsiz</CardTitle>
                    <CardDescription>
                        KNU Multilingual Assistant hisobingizga kiring
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Input
                            type="email"
                            placeholder="Email manzil"
                            className="bg-white dark:bg-zinc-900"
                        />
                    </div>
                    <div className="space-y-2">
                        <Input
                            type="password"
                            placeholder="Parol"
                            className="bg-white dark:bg-zinc-900"
                        />
                    </div>
                    <Button className="w-full bg-red-600 hover:bg-red-700 text-white">
                        Kirish
                    </Button>
                </CardContent>
                <CardFooter className="flex flex-col space-y-2">
                    <div className="text-center text-sm text-zinc-500">
                        Hisobingiz yo'qmi?{" "}
                        <Link href="#" className="underline hover:text-red-600">
                            Ro'yxatdan o'tish
                        </Link>
                    </div>
                    <div className="text-center text-xs text-zinc-400">
                        <Link href="/" className="hover:text-zinc-600">
                            Demoni ko'rish (Loginni o'tkazib yuborish)
                        </Link>
                    </div>
                </CardFooter>
            </Card>
        </div>
    )
}
