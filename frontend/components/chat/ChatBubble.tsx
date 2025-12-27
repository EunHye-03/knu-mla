"use client"

import * as React from "react"
import { Copy, RefreshCw, Bot, User, ThumbsUp, ThumbsDown, Share, MoreHorizontal } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/Card"
import { cn } from "@/lib/utils"

interface ChatBubbleProps {
    role: "user" | "ai"
    content: string
    onCopy?: () => void
    onRegenerate?: () => void
}

export function ChatBubble({
    role,
    content,
    onCopy,
    onRegenerate,
}: ChatBubbleProps) {
    const isUser = role === "user"

    if (isUser) {
        return (
            <div className="flex w-full justify-end mb-4">
                <div className="flex max-w-[80%] items-start gap-3 flex-row-reverse">
                    <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-full bg-zinc-200 text-zinc-500">
                        <User className="h-5 w-5" />
                    </div>
                    <div className="relative rounded-2xl bg-zinc-100 px-4 py-3 text-sm dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100">
                        {content}
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="flex w-full justify-start mb-6">
            <div className="flex max-w-[90%] items-start gap-4">
                <div className="overflow-hidden h-10 w-10 shrink-0 select-none items-center justify-center rounded-full bg-white border border-zinc-200 shadow-sm relative">
                    <img
                        src="/mascot.jpg"
                        alt="KNU Mascot"
                        className="h-full w-full object-cover"
                    />
                </div>
                <Card className="w-full border-zinc-200 shadow-sm dark:border-zinc-800 mt-1 bg-white dark:bg-zinc-900/50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-bold text-zinc-900 dark:text-white">
                            KNU Assistant
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm leading-relaxed text-zinc-800 dark:text-zinc-200">
                        {content}
                    </CardContent>
                    <CardFooter className="flex items-center gap-1 pt-2 pb-3 pl-6">
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-7 w-7 text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
                            onClick={onCopy}
                        >
                            <Copy className="h-4 w-4" />
                            <span className="sr-only">Copy</span>
                        </Button>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-7 w-7 text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
                        >
                            <ThumbsUp className="h-4 w-4" />
                            <span className="sr-only">Good response</span>
                        </Button>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-7 w-7 text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
                        >
                            <ThumbsDown className="h-4 w-4" />
                            <span className="sr-only">Bad response</span>
                        </Button>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-7 w-7 text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
                        >
                            <Share className="h-4 w-4" />
                            <span className="sr-only">Share</span>
                        </Button>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-7 w-7 text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
                            onClick={onRegenerate}
                        >
                            <RefreshCw className="h-4 w-4" />
                            <span className="sr-only">Regenerate</span>
                        </Button>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-7 w-7 text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
                        >
                            <MoreHorizontal className="h-4 w-4" />
                            <span className="sr-only">More</span>
                        </Button>
                    </CardFooter>
                </Card>
            </div>
        </div>
    )
}
