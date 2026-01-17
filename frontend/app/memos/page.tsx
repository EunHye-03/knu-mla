"use client"

import * as React from "react"
import { useRouter } from "next/navigation"
import { useLanguage } from "@/components/layout/language-context"
import { api } from "@/services/api"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { ArrowLeft, MoreVertical, Trash2, Edit2, Smile } from "lucide-react"

// Simple mock for emoji picker if no library is available, or just a list
const EMOJIS = ["📝", "⭐", "💡", "🔥", "✅", "📅", "🚀", "❤️", "🎓", "📚"]

export default function MemosPage() {
    const { t } = useLanguage()
    const router = useRouter()
    const [memos, setMemos] = React.useState<any[]>([])
    const [isLoading, setIsLoading] = React.useState(true)

    // Edit State
    const [editingMemo, setEditingMemo] = React.useState<any | null>(null)
    const [editTitle, setEditTitle] = React.useState("")
    const [editEmoji, setEditEmoji] = React.useState("")

    React.useEffect(() => {
        loadMemos()
    }, [])

    const loadMemos = async () => {
        setIsLoading(true)
        try {
            // Mock or Real API
            const data = await api.getMemos().catch(() => [])
            // Fallback for demo if API fails/is empty
            if (!data || data.length === 0) {
                const local = localStorage.getItem("knu_mla_memo")
                if (local) {
                    setMemos([{ id: "1", title: "My Notes", emoji: "📝", content: local }])
                } else {
                    setMemos([])
                }
            } else {
                setMemos(data)
            }
        } finally {
            setIsLoading(false)
        }
    }

    const handleDelete = async (id: string) => {
        if (confirm(t.confirm_delete_memo)) {
            try {
                await api.deleteMemo(id)
                setMemos(prev => prev.filter(m => m.id !== id))
            } catch (e) {
                console.error(e)
                // If API fails (mock), just update local state
                setMemos(prev => prev.filter(m => m.id !== id))
            }
        }
    }

    const handleUpdate = async () => {
        if (!editingMemo) return
        try {
            await api.updateMemo(editingMemo.id, { title: editTitle, emoji: editEmoji })
            setMemos(prev => prev.map(m => m.id === editingMemo.id ? { ...m, title: editTitle, emoji: editEmoji } : m))
            setEditingMemo(null)
        } catch (e) {
            console.error(e)
            // Mock update
            setMemos(prev => prev.map(m => m.id === editingMemo.id ? { ...m, title: editTitle, emoji: editEmoji } : m))
            setEditingMemo(null)
        }
    }

    return (
        <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 p-4 md:p-8">
            <div className="max-w-4xl mx-auto space-y-6">
                <div className="flex items-center gap-4">
                    <Button variant="ghost" onClick={() => router.back()}>
                        <ArrowLeft className="h-5 w-5" />
                    </Button>
                    <h1 className="text-2xl font-bold">{t.manage_memos}</h1>
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {memos.map((memo) => (
                        <Card key={memo.id} className="relative group hover:shadow-lg transition-shadow bg-white dark:bg-zinc-900">
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <span className="text-3xl">{memo.emoji || "📝"}</span>
                                <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <Button size="sm" variant="ghost" onClick={() => {
                                        setEditingMemo(memo)
                                        setEditTitle(memo.title || "Untitled")
                                        setEditEmoji(memo.emoji || "📝")
                                    }}>
                                        <Edit2 className="h-4 w-4" />
                                    </Button>
                                    <Button size="sm" variant="ghost" className="text-red-500 hover:text-red-600" onClick={() => handleDelete(memo.id)}>
                                        <Trash2 className="h-4 w-4" />
                                    </Button>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <CardTitle className="text-lg mb-2">{memo.title || "Untitled"}</CardTitle>
                                <p className="text-sm text-zinc-500 truncate">{memo.content || "No content"}</p>
                            </CardContent>
                        </Card>
                    ))}
                    {memos.length === 0 && !isLoading && (
                        <div className="col-span-full text-center py-12 text-zinc-500">
                            <p>No memos found.</p>
                        </div>
                    )}
                </div>
            </div>

            {/* Edit Modal */}
            {editingMemo && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
                    <Card className="w-full max-w-sm bg-white dark:bg-zinc-900 shadow-xl animate-in zoom-in-95">
                        <CardHeader>
                            <CardTitle>Edit Memo</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-zinc-500">Emoji</label>
                                <div className="flex flex-wrap gap-2 p-2 border rounded-md">
                                    {EMOJIS.map(e => (
                                        <button
                                            key={e}
                                            onClick={() => setEditEmoji(e)}
                                            className={`text-xl p-1 rounded hover:bg-zinc-100 dark:hover:bg-zinc-800 ${editEmoji === e ? "bg-red-50 ring-1 ring-red-500" : ""}`}
                                        >
                                            {e}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-zinc-500">Title</label>
                                <Input value={editTitle} onChange={(e) => setEditTitle(e.target.value)} />
                            </div>
                            <div className="flex justify-end gap-2 pt-2">
                                <Button variant="ghost" onClick={() => setEditingMemo(null)}>Cancel</Button>
                                <Button onClick={handleUpdate}>Save Changes</Button>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            )}
        </div>
    )
}
