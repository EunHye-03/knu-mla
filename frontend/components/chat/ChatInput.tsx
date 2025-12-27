"use client"

import * as React from "react"
import { SendHorizontal, Globe, FileText, BookOpen } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { cn } from "@/lib/utils"
import { useLanguage } from "@/components/layout/language-context"

interface ChatInputProps {
    onSend: (message: string, mode: string) => void
    isLoading?: boolean
}

type Mode = "translate" | "summarize" | "term"

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
    const { t } = useLanguage()
    const [input, setInput] = React.useState("")
    const [mode, setMode] = React.useState<Mode>("translate")

    const handleSend = () => {
        if (!input.trim() || isLoading) return
        onSend(input, mode)
        setInput("")
    }

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    return (
        <div className="relative flex flex-col gap-2 rounded-2xl border bg-white/50 backdrop-blur-sm p-4 shadow-sm ring-1 ring-inset ring-zinc-200/50 transition-all duration-300 focus-within:ring-2 focus-within:ring-red-500/50 focus-within:shadow-lg focus-within:shadow-red-500/5 dark:bg-zinc-900/50 dark:ring-zinc-800">
            <textarea
                className="min-h-[60px] w-full resize-none border-0 bg-transparent p-0 text-sm focus:ring-0 placeholder:text-muted-foreground focus-visible:outline-none text-foreground"
                placeholder={t.placeholder}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
            />
            <div className="flex items-center justify-between">
                <div className="flex gap-2">
                    <Button
                        variant={mode === "translate" ? "secondary" : "ghost"}
                        size="sm"
                        className={cn(
                            "h-7 text-xs gap-1.5",
                            mode === "translate" && "bg-blue-100 text-blue-700 hover:bg-blue-200 dark:bg-blue-900/30 dark:text-blue-300"
                        )}
                        onClick={() => setMode("translate")}
                    >
                        <Globe className="h-3.5 w-3.5" />
                        {t.translate}
                    </Button>
                    <Button
                        variant={mode === "summarize" ? "secondary" : "ghost"}
                        size="sm"
                        className={cn(
                            "h-7 text-xs gap-1.5",
                            mode === "summarize" && "bg-purple-100 text-purple-700 hover:bg-purple-200 dark:bg-purple-900/30 dark:text-purple-300"
                        )}
                        onClick={() => setMode("summarize")}
                    >
                        <FileText className="h-3.5 w-3.5" />
                        {t.summarize}
                    </Button>
                    <Button
                        variant={mode === "term" ? "secondary" : "ghost"}
                        size="sm"
                        className={cn(
                            "h-7 text-xs gap-1.5",
                            mode === "term" && "bg-amber-100 text-amber-700 hover:bg-amber-200 dark:bg-amber-900/30 dark:text-amber-300"
                        )}
                        onClick={() => setMode("term")}
                    >
                        <BookOpen className="h-3.5 w-3.5" />
                        {t.term}
                    </Button>
                </div>
                <div className="flex items-center gap-2">
                    <span className="text-xs text-muted-foreground mr-2">{input.length} / 1000</span>
                    <Button
                        size="icon"
                        className="h-8 w-8 rounded-full"
                        onClick={handleSend}
                        disabled={!input.trim() || isLoading}
                    >
                        <SendHorizontal className="h-4 w-4" />
                        <span className="sr-only">{t.send}</span>
                    </Button>
                </div>
            </div>
        </div>
    )
}
