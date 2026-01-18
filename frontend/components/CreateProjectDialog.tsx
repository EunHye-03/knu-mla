"use client"

import * as React from "react"
import { X, BookOpen, GraduationCap, PenTool, Users, Languages, Sparkles, Plane, DollarSign, Code } from "lucide-react"
import { useLanguage } from "@/components/layout/language-context"
import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { cn } from "@/lib/utils"

interface CreateProjectDialogProps {
    open: boolean
    onClose: () => void
    onCreate: (project: { title: string, category: string }) => void
}

export function CreateProjectDialog({ open, onClose, onCreate }: CreateProjectDialogProps) {
    const { t } = useLanguage()
    const [name, setName] = React.useState("")
    const [selectedCategory, setSelectedCategory] = React.useState<string | null>(null)

    if (!open) return null

    const handleCreate = () => {
        if (!name.trim()) return
        onCreate({
            title: name,
            category: selectedCategory || 'homework'
        })
        setName("")
        setSelectedCategory(null)
        onClose()
    }

    const categories = [
        { id: "homework", label: t.cat_homework, icon: BookOpen, color: "text-blue-500 border-blue-200 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-800" },
        { id: "research", label: t.cat_research, icon: Sparkles, color: "text-purple-500 border-purple-200 bg-purple-50 dark:bg-purple-900/20 dark:border-purple-800" },
        { id: "exam", label: t.cat_exam, icon: GraduationCap, color: "text-red-500 border-red-200 bg-red-50 dark:bg-red-900/20 dark:border-red-800" },
        { id: "group", label: t.cat_group, icon: Users, color: "text-green-500 border-green-200 bg-green-50 dark:bg-green-900/20 dark:border-green-800" },
        { id: "language", label: t.cat_language, icon: Languages, color: "text-orange-500 border-orange-200 bg-orange-50 dark:bg-orange-900/20 dark:border-orange-800" },
        { id: "finance", label: t.cat_finance, icon: DollarSign, color: "text-emerald-500 border-emerald-200 bg-emerald-50 dark:bg-emerald-900/20 dark:border-emerald-800" },
        { id: "travel", label: t.cat_travel, icon: Plane, color: "text-sky-500 border-sky-200 bg-sky-50 dark:bg-sky-900/20 dark:border-sky-800" },
        { id: "coding", label: t.cat_coding, icon: Code, color: "text-amber-500 border-amber-200 bg-amber-50 dark:bg-amber-900/20 dark:border-amber-800" },
    ]

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <Card className="w-full max-w-lg bg-white dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
                {/* Header */}
                <div className="flex items-center justify-between p-4 border-b border-zinc-100 dark:border-zinc-800">
                    <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">{t.create_project_title}</h2>
                    <button onClick={onClose} className="p-2 rounded-md hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                        <X className="h-5 w-5 text-zinc-500" />
                    </button>
                </div>

                <div className="p-6 space-y-6">
                    {/* Input */}
                    <div className="space-y-2">
                        <div className="relative">
                            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500">
                                {selectedCategory ? (
                                    categories.find(c => c.id === selectedCategory)?.icon &&
                                    React.createElement(categories.find(c => c.id === selectedCategory)!.icon, { className: "h-5 w-5" })
                                ) : (
                                    <PenTool className="h-5 w-5" />
                                )}
                            </div>
                            <Input
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder={t.project_name_placeholder}
                                className="pl-10 h-12 text-base"
                                autoFocus
                            />
                        </div>
                    </div>

                    {/* Categories */}
                    <div className="flex flex-wrap gap-2">
                        {categories.map((cat) => (
                            <button
                                key={cat.id}
                                onClick={() => setSelectedCategory(cat.id)}
                                className={cn(
                                    "flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium border transition-all",
                                    selectedCategory === cat.id
                                        ? cat.color
                                        : "bg-white dark:bg-zinc-900 border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800"
                                )}
                            >
                                <cat.icon className="h-4 w-4" />
                                {cat.label}
                            </button>
                        ))}
                    </div>

                    {/* Description Box */}
                    <div className="bg-zinc-50 dark:bg-zinc-800/50 rounded-lg p-4 flex gap-3 text-sm text-zinc-600 dark:text-zinc-400">
                        <Sparkles className="h-5 w-5 text-yellow-500 shrink-0 mt-0.5" />
                        <p>{t.project_desc}</p>
                    </div>

                    {/* Footer Actions */}
                    <div className="flex justify-end pt-2">
                        <Button
                            className="bg-zinc-900 text-white hover:bg-zinc-800 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200 rounded-full px-6"
                            disabled={!name.trim()}
                            onClick={handleCreate}
                        >
                            {t.create_button}
                        </Button>
                    </div>
                </div>
            </Card>
        </div>
    )
}
