"use client"

import * as React from "react"
import { useTheme } from "next-themes"
import { Sun, Moon } from "lucide-react"

import { Button } from "@/components/ui/Button"
import { useLanguage } from "@/components/layout/language-context"

export function Header() {
    const { language, setLanguage } = useLanguage()
    const { setTheme, theme } = useTheme()

    return (
        <header className="sticky top-0 z-50 w-full pointer-events-none p-4 flex justify-end">
            {/* Floating Control Island */}
            <div className="pointer-events-auto flex items-center gap-1 rounded-full bg-white/80 backdrop-blur-md p-1.5 shadow-lg border border-zinc-200/50 dark:bg-zinc-900/80 dark:border-zinc-800 transition-all hover:scale-105 duration-300 mr-4">

                <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
                    className="h-8 w-8 rounded-full hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-600 dark:text-zinc-400"
                >
                    <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                    <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                    <span className="sr-only">Toggle theme</span>
                </Button>

                <div className="h-4 w-px bg-zinc-200 dark:bg-zinc-800 mx-1" />

                <div className="flex bg-zinc-100 dark:bg-zinc-800/50 rounded-full p-0.5">
                    <Button
                        variant={language === "KR" ? "default" : "ghost"}
                        size="sm"
                        onClick={() => setLanguage("KR")}
                        className={`h-7 px-3 rounded-full text-xs font-medium transition-all ${language === "KR"
                                ? "bg-white text-zinc-900 shadow-sm dark:bg-zinc-700 dark:text-white"
                                : "hover:bg-transparent text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-300"
                            }`}
                    >
                        KR
                    </Button>
                    <Button
                        variant={language === "EN" ? "default" : "ghost"}
                        size="sm"
                        onClick={() => setLanguage("EN")}
                        className={`h-7 px-3 rounded-full text-xs font-medium transition-all ${language === "EN"
                                ? "bg-white text-zinc-900 shadow-sm dark:bg-zinc-700 dark:text-white"
                                : "hover:bg-transparent text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-300"
                            }`}
                    >
                        EN
                    </Button>
                    <Button
                        variant={language === "UZ" ? "default" : "ghost"}
                        size="sm"
                        onClick={() => setLanguage("UZ")}
                        className={`h-7 px-3 rounded-full text-xs font-medium transition-all ${language === "UZ"
                                ? "bg-white text-zinc-900 shadow-sm dark:bg-zinc-700 dark:text-white"
                                : "hover:bg-transparent text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-300"
                            }`}
                    >
                        UZ
                    </Button>
                </div>
            </div>
        </header>
    )
}
