"use client"
import * as React from "react"
import { SendHorizontal, Globe, FileText, BookOpen, Paperclip, Mic, StopCircle, MessageSquare } from "lucide-react"
import { Button } from "@/components/ui/Button"
import { api } from "@/services/api"
import { cn } from "@/lib/utils"
import { useLanguage } from "@/components/layout/language-context"

interface ChatInputProps {
    onSend: (message: string, mode: string, options?: { targetLang?: string }) => void
    isLoading?: boolean
}

type Mode = "chat" | "translate" | "summarize" | "term"

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
    const { t, language } = useLanguage()
    const [input, setInput] = React.useState("")
    const [mode, setMode] = React.useState<Mode>("chat")  // Default to chat for general conversation
    const [targetLang, setTargetLang] = React.useState<string>("uz") // Default target
    const [isRecording, setIsRecording] = React.useState(false)
    const [isUploading, setIsUploading] = React.useState(false)
    const fileInputRef = React.useRef<HTMLInputElement>(null)
    const mediaRecorderRef = React.useRef<MediaRecorder | null>(null)

    // Sync default target lang with app language if needed, or keep independent
    // For now independent is better for translation tasks.

    const handleSend = () => {
        if (!input.trim() || isLoading) return
        onSend(input, mode, { targetLang })
        setInput("")
    }

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    const handleFileClick = () => {
        fileInputRef.current?.click()
    }

    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (!file) return

        if (file.size > 5 * 1024 * 1024) {
            alert("File size must be less than 5MB")
            return
        }

        try {
            setIsUploading(true)
            const result = await api.uploadFile(file)
            // If summary exists, set it as input or append
            if (result.summary) {
                setInput((prev) => prev ? `${prev}\n\n[File Summary]: ${result.summary}` : `[File Summary]: ${result.summary}`)
            } else {
                setInput((prev) => prev ? `${prev}\n\n[File Uploaded]: ${file.name}` : `[File Uploaded]: ${file.name}`)
            }
        } catch (error) {
            console.error("File upload error:", error)
            alert("Failed to upload file")
        } finally {
            setIsUploading(false)
            if (fileInputRef.current) fileInputRef.current.value = ""
        }
    }

    const handleMicClick = async () => {
        if (isRecording) {
            // Stop recording
            mediaRecorderRef.current?.stop()
            setIsRecording(false)
        } else {
            // Start recording
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
                const mediaRecorder = new MediaRecorder(stream)
                mediaRecorderRef.current = mediaRecorder
                const chunks: BlobPart[] = []

                mediaRecorder.ondataavailable = (e) => {
                    if (e.data.size > 0) chunks.push(e.data)
                }

                mediaRecorder.onstop = async () => {
                    const blob = new Blob(chunks, { type: "audio/webm" })
                    // Stop all tracks
                    stream.getTracks().forEach(track => track.stop())

                    try {
                        // Indicate processing if needed, maybe simple text
                        setInput((prev) => prev + " (Processing Audio...)")
                        const result = await api.voiceToText(blob)
                        // Replace processing text or just append
                        setInput((prev) => prev.replace(" (Processing Audio...)", "") + " " + result.text)
                    } catch (err) {
                        console.error("STT Error:", err)
                        setInput((prev) => prev.replace(" (Processing Audio...)", "") + " [Audio Error]")
                    }
                }

                mediaRecorder.start()
                setIsRecording(true)
            } catch (err) {
                console.error("Mic access denied:", err)
                alert("Microphone access required")
            }
        }
    }

    const [showLangDropdown, setShowLangDropdown] = React.useState(false)

    // ... existing handlers ...

    const toggleTranslateMode = () => {
        if (mode !== "translate") {
            setMode("translate")
            setShowLangDropdown(true)
        } else {
            setShowLangDropdown(!showLangDropdown)
        }
    }

    const selectLanguage = (lang: string) => {
        setTargetLang(lang)
        setShowLangDropdown(false)
    }

    return (
        <div className="relative flex flex-col gap-2 rounded-2xl border bg-white/50 backdrop-blur-sm p-4 shadow-sm ring-1 ring-inset ring-zinc-200/50 transition-all duration-300 focus-within:ring-2 focus-within:ring-red-500/50 focus-within:shadow-lg focus-within:shadow-red-500/5 dark:bg-zinc-900/50 dark:ring-zinc-800">
            <textarea
                className="min-h-[60px] w-full resize-none border-0 bg-transparent p-0 text-sm focus:ring-0 placeholder:text-muted-foreground focus-visible:outline-none text-foreground"
                placeholder={isRecording ? "Listening..." : t.placeholder}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={isLoading || isUploading}
            />

            <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                accept=".txt,.pdf"
                onChange={handleFileChange}
            />

            <div className="flex items-center justify-between">
                <div className="flex gap-2 relative">
                    <Button
                        variant="ghost"
                        size="icon"
                        className="h-7 w-7 text-zinc-500 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-200"
                        onClick={handleFileClick}
                        disabled={isLoading || isUploading}
                        title="Upload File (PDF/TXT)"
                    >
                        <Paperclip className="h-4 w-4" />
                    </Button>
                    <Button
                        variant="ghost"
                        size="icon"
                        className={cn(
                            "h-7 w-7 text-zinc-500 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-200",
                            isRecording && "text-red-500 animate-pulse hover:text-red-600"
                        )}
                        onClick={handleMicClick}
                        disabled={isLoading || isUploading}
                        title="Voice Input"
                    >
                        {isRecording ? <StopCircle className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                    </Button>

                    <div className="w-px h-4 bg-zinc-200 dark:bg-zinc-700 mx-1 self-center" />

                    <Button
                        variant={mode === "chat" ? "secondary" : "ghost"}
                        size="sm"
                        className={cn(
                            "h-7 text-xs gap-1.5",
                            mode === "chat" && "bg-green-100 text-green-700 hover:bg-green-200 dark:bg-green-900/30 dark:text-green-300"
                        )}
                        onClick={() => setMode("chat")}
                    >
                        <MessageSquare className="h-3.5 w-3.5" />
                        Chat
                    </Button>

                    <div className="relative">
                        <Button
                            variant={mode === "translate" ? "secondary" : "ghost"}
                            size="sm"
                            className={cn(
                                "h-7 text-xs gap-1.5",
                                mode === "translate" && "bg-blue-100 text-blue-700 hover:bg-blue-200 dark:bg-blue-900/30 dark:text-blue-300"
                            )}
                            onClick={toggleTranslateMode}
                        >
                            <Globe className="h-3.5 w-3.5" />
                            {mode === "translate" ? `Translate (${targetLang.toUpperCase()})` : t.translate}
                        </Button>

                        {/* Dropdown Menu */}
                        {showLangDropdown && mode === "translate" && (
                            <div className="absolute bottom-full left-0 mb-2 w-24 rounded-lg border border-zinc-200 bg-white p-1 shadow-lg shadow-zinc-500/10 dark:border-zinc-800 dark:bg-zinc-900 animate-in fade-in zoom-in-95 duration-200 z-50">
                                <div className="space-y-0.5">
                                    {['uz', 'en', 'kr'].map((lang) => (
                                        <button
                                            key={lang}
                                            onClick={() => selectLanguage(lang)}
                                            className={cn(
                                                "w-full px-2 py-1.5 text-left text-xs font-medium rounded-md transition-colors",
                                                targetLang === lang
                                                    ? "bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400"
                                                    : "text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800"
                                            )}
                                        >
                                            {lang.toUpperCase()}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
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
        </div >
    )
}
