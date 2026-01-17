"use client"

import * as React from "react"
import { useRouter } from "next/navigation"
import { useLanguage } from "@/components/layout/language-context"
import { api } from "@/services/api"
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { ArrowLeft, Trash2, Edit2, Folder } from "lucide-react"

export default function ProjectsPage() {
    const { t } = useLanguage()
    const router = useRouter()
    const [projects, setProjects] = React.useState<any[]>([])
    const [isLoading, setIsLoading] = React.useState(true)

    // Edit State
    const [editingProject, setEditingProject] = React.useState<any | null>(null)
    const [editName, setEditName] = React.useState("")
    const [editDesc, setEditDesc] = React.useState("")

    React.useEffect(() => {
        loadProjects()
    }, [])

    const loadProjects = async () => {
        setIsLoading(true)
        try {
            const data = await api.getProjects().catch(() => [])
            if (!data || data.length === 0) {
                // Try local storage for demo
                const local = localStorage.getItem("knu_mla_projects")
                if (local) {
                    setProjects(JSON.parse(local))
                } else {
                    setProjects([])
                }
            } else {
                setProjects(data)
            }
        } finally {
            setIsLoading(false)
        }
    }

    const handleDelete = async (id: number) => {
        if (confirm(t.confirm_delete_project)) {
            try {
                await api.deleteProject(id)
                // Update local state
                const newProjects = projects.filter(p => p.id !== id)
                setProjects(newProjects)
                localStorage.setItem("knu_mla_projects", JSON.stringify(newProjects))
            } catch (e) {
                console.error(e)
                // Mock delete even if API fails
                const newProjects = projects.filter(p => p.id !== id)
                setProjects(newProjects)
                localStorage.setItem("knu_mla_projects", JSON.stringify(newProjects))
            }
        }
    }

    // Delete from edit modal
    const handleDeleteFromModal = async () => {
        if (!editingProject) return
        await handleDelete(editingProject.id)
        setEditingProject(null)
    }

    const handleUpdate = async () => {
        if (!editingProject) return
        try {
            await api.updateProject(editingProject.id, { name: editName, description: editDesc })
            // Update local state
            const newProjects = projects.map(p => p.id === editingProject.id ? { ...p, name: editName, description: editDesc } : p)
            setProjects(newProjects)
            localStorage.setItem("knu_mla_projects", JSON.stringify(newProjects))

            setEditingProject(null)
        } catch (e) {
            console.error(e)
            const newProjects = projects.map(p => p.id === editingProject.id ? { ...p, name: editName, description: editDesc } : p)
            setProjects(newProjects)
            localStorage.setItem("knu_mla_projects", JSON.stringify(newProjects))
            setEditingProject(null)
        }
    }

    return (
        <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 p-4 md:p-8">
            <div className="max-w-4xl mx-auto space-y-6">
                <div className="flex items-center gap-4">
                    <Button variant="ghost" onClick={() => router.back()}>
                        <ArrowLeft className="h-5 w-5" />
                    </Button>
                    <h1 className="text-2xl font-bold">{t.manage_projects}</h1>
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {projects.map((proj) => (
                        <Card key={proj.id} className="group hover:shadow-lg transition-shadow bg-white dark:bg-zinc-900">
                            <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
                                <div className="p-2 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg text-indigo-600 dark:text-indigo-400">
                                    <Folder className="h-6 w-6" />
                                </div>
                                <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <Button size="sm" variant="ghost" onClick={() => {
                                        setEditingProject(proj)
                                        setEditName(proj.name || "")
                                        setEditDesc(proj.description || "")
                                    }}>
                                        <Edit2 className="h-4 w-4" />
                                    </Button>
                                    <Button size="sm" variant="ghost" className="text-red-500 hover:text-red-600" onClick={() => handleDelete(proj.id)}>
                                        <Trash2 className="h-4 w-4" />
                                    </Button>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <CardTitle className="text-lg mb-1">{proj.name}</CardTitle>
                                <CardDescription>{proj.description || "No description"}</CardDescription>
                                {proj.category && (
                                    <span className="inline-block mt-2 px-2 py-0.5 bg-zinc-100 dark:bg-zinc-800 text-xs rounded-full text-zinc-500">
                                        {proj.category}
                                    </span>
                                )}
                            </CardContent>
                        </Card>
                    ))}
                    {projects.length === 0 && !isLoading && (
                        <div className="col-span-full text-center py-12 text-zinc-500">
                            <p>No projects found.</p>
                        </div>
                    )}
                </div>
            </div>

            {/* Edit Modal */}
            {editingProject && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
                    <Card className="w-full max-w-sm bg-white dark:bg-zinc-900 shadow-xl animate-in zoom-in-95">
                        <CardHeader>
                            <CardTitle>{t.edit_project}</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-zinc-500">Name</label>
                                <Input value={editName} onChange={(e) => setEditName(e.target.value)} />
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-zinc-500">Description</label>
                                <Input value={editDesc} onChange={(e) => setEditDesc(e.target.value)} />
                            </div>
                            <div className="flex justify-end gap-2 pt-2">
                                <Button variant="ghost" onClick={() => setEditingProject(null)}>Cancel</Button>
                                <Button onClick={handleUpdate}>Save Changes</Button>
                                <Button variant="destructive" onClick={handleDeleteFromModal}>Delete Project</Button>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            )}
        </div>
    )
}
