"use client"

import * as React from "react"
import { X, StickyNote, Save, Trash2 } from "lucide-react"
import { useLanguage } from "@/components/layout/language-context"
import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"

interface MemoDialogProps {
    open: boolean
    onClose: () => void
}

export function MemoDialog({ open, onClose }: MemoDialogProps) {
    const { t } = useLanguage()
    const [note, setNote] = React.useState("")

    // Load from local storage on mount
    React.useEffect(() => {
        const savedNote = localStorage.getItem("knu_mla_memo")
        if (savedNote) {
            setNote(savedNote)
        }
    }, [])

    const handleSave = () => {
        localStorage.setItem("knu_mla_memo", note)
        onClose()
    }



    const handleDelete = () => {
        localStorage.removeItem("knu_mla_memo")
        setNote("")
        onClose()
    }


    if (!open) return null

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <Card className="w-full max-w-lg bg-amber-50 dark:bg-amber-950/30 border-amber-200 dark:border-amber-800 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
                {/* Header */}
                <div className="flex items-center justify-between p-4 border-b border-amber-100 dark:border-amber-800/50 bg-amber-100/50 dark:bg-amber-900/20">
                    <div className="flex items-center gap-2">
                        <StickyNote className="h-5 w-5 text-amber-600 dark:text-amber-400" />
                        <h2 className="text-lg font-semibold text-amber-900 dark:text-amber-100">{t.memo_title}</h2>
                    </div>
                    <button onClick={onClose} className="p-2 rounded-md hover:bg-amber-100 dark:hover:bg-amber-900/50 transition-colors">
                        <X className="h-5 w-5 text-amber-500 dark:text-amber-400" />
                    </button>
                </div>

                <div className="p-4">
                    <textarea
                        value={note}
                        onChange={(e) => setNote(e.target.value)}
                        placeholder={t.memo_placeholder}
                        className="w-full h-64 p-4 rounded-lg bg-amber-50/50 dark:bg-transparent resize-none outline-none text-amber-900 dark:text-amber-50 placeholder-amber-400 text-lg leading-relaxed font-handwriting"
                        style={{ fontFamily: 'var(--font-geist-mono)' }}
                        autoFocus
                    />

                    <div className="flex justify-end pt-4 space-x-2">
                        <Button
                            className="bg-amber-500 hover:bg-amber-600 text-white border-none shadow-amber-200 dark:shadow-none"
                            onClick={handleSave}
                        >
                            <Save className="h-4 w-4 mr-2" />
                            {t.save_memo}
                        </Button>

                        <Button
                            variant="destructive"
                            className="bg-red-500 hover:bg-red-600 text-white border-none"
                            onClick={handleDelete}
                        >
                            <Trash2 className="h-4 w-4 mr-2" />
                            Delete
                        </Button>
                    </div>
                </div>
            </Card>
        </div>
    )
}
