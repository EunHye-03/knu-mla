"use client"

import * as React from "react"
import { Copy, Bot, User, ThumbsUp, ThumbsDown, Share, FileText, Globe } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/Card"
import { cn } from "@/lib/utils"

interface ChatBubbleProps {
    role: "user" | "ai"
    content: string
    onCopy?: () => void
    onRegenerate?: () => void
    onAction?: (action: 'translate' | 'summarize' | 'feedback_positive' | 'feedback_negative' | 'share', text: string) => void
}

export function ChatBubble({
    role,
    content,
    onCopy,
    onRegenerate,
    onAction
}: ChatBubbleProps) {
    const isUser = role === "user"

    // Helper to parse content if it's JSON
    const parsedContent = React.useMemo(() => {
        if (isUser) return null;
        try {
            return JSON.parse(content);
        } catch (e) {
            return null;
        }
    }, [content, isUser]);

    const isStructured = parsedContent && parsedContent.summary && Array.isArray(parsedContent.key_points);

    if (isUser) {
        return (
            <div className="flex w-full justify-end mb-4">
                <div className="flex max-w-[80%] items-start gap-3 flex-row-reverse">
                    <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-full bg-zinc-200 text-zinc-500">
                        <User className="h-5 w-5" />
                    </div>
                    <div className="relative rounded-2xl bg-gradient-to-br from-red-600 to-red-700 px-5 py-3.5 text-sm text-white shadow-md shadow-red-500/10">
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
                <Card className="w-full border-zinc-100 shadow-sm dark:border-zinc-800 mt-1 bg-white/80 backdrop-blur-sm dark:bg-zinc-900/80 ring-1 ring-zinc-200/50 dark:ring-zinc-800/50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-bold text-zinc-900 dark:text-white">
                            KNU Assistant
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm leading-relaxed text-zinc-800 dark:text-zinc-200 space-y-3">
                        {isStructured ? (
                            <div className="space-y-4">
                                <div className="bg-zinc-50 dark:bg-zinc-800/50 p-4 rounded-xl border border-zinc-100 dark:border-zinc-800">
                                    <h4 className="font-semibold text-red-600 mb-2 flex items-center gap-2">
                                        <FileText className="h-4 w-4" /> Summary
                                    </h4>
                                    <p>{parsedContent.summary}</p>
                                </div>

                                {parsedContent.key_points && parsedContent.key_points.length > 0 && (
                                    <div>
                                        <h4 className="font-semibold mb-2 text-zinc-700 dark:text-zinc-300">Key Points</h4>
                                        <ul className="list-disc pl-5 space-y-1 text-zinc-600 dark:text-zinc-400">
                                            {parsedContent.key_points.map((point: string, i: number) => (
                                                <li key={i}>{point}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {parsedContent.keywords && parsedContent.keywords.length > 0 && (
                                    <div className="flex flex-wrap gap-2 pt-2">
                                        {parsedContent.keywords.map((keyword: string, i: number) => (
                                            <span key={i} className="px-2 py-1 bg-zinc-100 dark:bg-zinc-800 rounded-md text-xs font-medium text-zinc-500">
                                                #{keyword}
                                            </span>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ) : (
                            <div className="whitespace-pre-wrap">{content}</div>
                        )}
                    </CardContent>

                    <CardFooter className="flex flex-col gap-2 pt-2 pb-3 px-4">
                        {/* Action Buttons Row */}
                        <div className="flex w-full items-center gap-2 border-b border-zinc-100 dark:border-zinc-800 pb-2 mb-1">
                            <Button
                                variant="outline"
                                size="sm"
                                className="h-7 text-xs gap-1.5 rounded-full"
                                onClick={() => onAction?.('summarize', isStructured ? parsedContent.summary : content)}
                            >
                                <FileText className="h-3 w-3" /> Summarize this
                            </Button>
                            <Button
                                variant="outline"
                                size="sm"
                                className="h-7 text-xs gap-1.5 rounded-full"
                                onClick={() => onAction?.('translate', isStructured ? parsedContent.summary : content)}
                            >
                                <Globe className="h-3 w-3" /> Translate this
                            </Button>
                        </div>

                        {/* Feedback Actions */}
                        <div className="flex w-full items-center gap-1">
                            <Button
                                variant="ghost"
                                size="icon"
                                className="h-7 w-7 text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
                                onClick={onCopy}
                                title="Copy"
                            >
                                <Copy className="h-4 w-4" />
                                <span className="sr-only">Copy</span>
                            </Button>
                            <Button
                                variant="ghost"
                                size="icon"
                                className="h-7 w-7 text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
                                onClick={() => onAction?.('feedback_positive', content)}
                                title="Good response"
                            >
                                <ThumbsUp className="h-4 w-4" />
                                <span className="sr-only">Good response</span>
                            </Button>
                            <Button
                                variant="ghost"
                                size="icon"
                                className="h-7 w-7 text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
                                onClick={() => onAction?.('feedback_negative', content)}
                                title="Bad response"
                            >
                                <ThumbsDown className="h-4 w-4" />
                                <span className="sr-only">Bad response</span>
                            </Button>
                            <Button
                                variant="ghost"
                                size="icon"
                                className="h-7 w-7 text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
                                onClick={() => onAction?.('share', content)}
                                title="Share"
                            >
                                <Share className="h-4 w-4" />
                                <span className="sr-only">Share</span>
                            </Button>
                        </div>
                    </CardFooter>
                </Card>
            </div>
        </div>
    )
}

