"use client"

import * as React from "react"
import Link from "next/link"
import {
    SquarePen,
    MessageSquare,
    User,
    Settings2,
    Search,
    FolderPlus,
    Briefcase,
    StickyNote,
    Edit2,
    Share2,
    MoreHorizontal,
    Pin,
    Folder,
    Trash,
    Trash2
} from "lucide-react"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
    DropdownMenuSub,
    DropdownMenuSubTrigger,
    DropdownMenuSubContent
} from "@/components/ui/DropdownMenu"
import { api } from "@/services/api"
import { Input } from "@/components/ui/Input"
import { Button } from "@/components/ui/Button"
import { cn } from "@/lib/utils"
import { useAuth } from "@/components/auth-provider"
import { SettingsDialog } from "@/components/SettingsDialog"
import { useLanguage } from "@/components/layout/language-context"

import { CreateProjectDialog } from "@/components/CreateProjectDialog"
import { MemoDialog } from "@/components/MemoDialog"

// Sidebar Props
interface SidebarProps {
    history?: { id: number, title: string, pinned?: boolean, projectId?: string | number }[]
    onNewChat?: () => void
    onPinChat?: (id: number) => void
    onDeleteChat?: (id: number) => void
    onRenameChat?: (id: number, newTitle: string) => void
    onMoveChat?: (id: number, projectId: string | number) => void
}

export function Sidebar({ history = [], onNewChat, onPinChat, onDeleteChat, onRenameChat, onMoveChat }: SidebarProps) {
    const { user, logout } = useAuth()
    const { t } = useLanguage()
    const [settingsOpen, setSettingsOpen] = React.useState(false)
    const [projectDialogOpen, setProjectDialogOpen] = React.useState(false)
    const [memoOpen, setMemoOpen] = React.useState(false)
    const [isSearchOpen, setIsSearchOpen] = React.useState(false)
    const [searchQuery, setSearchQuery] = React.useState("")
    const [projects, setProjects] = React.useState<{ id: number, name: string, description: string, category: string, color?: string }[]>([])
    const [expandedProjects, setExpandedProjects] = React.useState<Set<number>>(new Set())

    const toggleProject = (e: React.MouseEvent, id: number) => {
        e.stopPropagation()
        const newExpanded = new Set(expandedProjects)
        if (newExpanded.has(id)) {
            newExpanded.delete(id)
        } else {
            newExpanded.add(id)
        }
        setExpandedProjects(newExpanded)
    }

    // Filter history for "Unsorted" (not in a project) main list
    const filteredHistory = history.filter(chat =>
        // Must match search query AND (not be in a project OR allow searching everything when searching)
        chat.title.toLowerCase().includes(searchQuery.toLowerCase()) &&
        (!chat.projectId || searchQuery !== "") // Show all if searching, otherwise only unassigned
    )

    // Edit State
    const [editingProject, setEditingProject] = React.useState<{ id: number, name: string, description: string } | null>(null)
    const [editName, setEditName] = React.useState("")
    const [editDesc, setEditDesc] = React.useState("")

    // Load projects on mount
    React.useEffect(() => {
        loadProjects()
    }, [])

    const loadProjects = async () => {
        try {
            const data = await api.getProjects().catch(() => [])
            if (!data || data.length === 0) {
                const local = localStorage.getItem("knu_mla_projects")
                if (local) {
                    setProjects(JSON.parse(local))
                }
            } else {
                setProjects(data)
            }
        } catch (e) {
            console.error("Failed to load projects", e)
        }
    }

    const handleCreateProject = async (project: { title: string, category: string }) => {
        const colors: Record<string, string> = {
            homework: "text-blue-500",
            research: "text-purple-500",
            exam: "text-red-500",
            group: "text-green-500",
            language: "text-orange-500",
            default: "text-gray-500"
        }

        try {
            const res = await api.createProject({ name: project.title, category: project.category })

            // Add to local state & storage for persistence (Mock Mode)
            const newProject = {
                id: res.id || Date.now(),
                name: project.title,
                description: "",
                category: project.category,
                color: colors[project.category] || colors.default
            }

            const updated = [...projects, newProject]
            setProjects(updated)
            localStorage.setItem("knu_mla_projects", JSON.stringify(updated))

        } catch (e) {
            // Fallback for demo if API fails completely
            const newProject = {
                id: Date.now(),
                name: project.title,
                description: "",
                category: project.category,
                color: colors[project.category] || colors.default
            }
            const updated = [...projects, newProject]
            setProjects(updated)
            localStorage.setItem("knu_mla_projects", JSON.stringify(updated))
        }
    }

    const handleDeleteProject = async (e: React.MouseEvent, id: number) => {
        e.stopPropagation() // Prevent navigation
        if (confirm(t.confirm_delete_project || "Are you sure you want to delete this project?")) {
            try {
                await api.deleteProject(id)
            } catch (e) {
                console.error("API delete failed, removing locally", e)
            } finally {
                // Always remove locally for better UX in mock mode
                const updated = projects.filter(p => p.id !== id)
                setProjects(updated)
                localStorage.setItem("knu_mla_projects", JSON.stringify(updated))
            }
        }
    }

    const handleUpdateProject = async () => {
        if (!editingProject) return
        try {
            await api.updateProject(editingProject.id.toString(), { name: editName, description: editDesc })
        } catch (e) {
            console.error("API update failed, updating locally", e)
        } finally {
            // Always update locally
            const updated = projects.map(p => p.id === editingProject.id ? { ...p, name: editName, description: editDesc } : p)
            setProjects(updated)
            localStorage.setItem("knu_mla_projects", JSON.stringify(updated))
            setEditingProject(null)
        }
    }

    const openEditModal = (e: React.MouseEvent, project: any) => {
        e.stopPropagation()
        setEditingProject(project)
        setEditName(project.name || "")
        setEditDesc(project.description || "")
    }

    const handleShare = (e: React.MouseEvent, type: 'project' | 'chat', id: string | number) => {
        e.stopPropagation()
        const url = `${window.location.origin}/share/${type}/${id}`
        navigator.clipboard.writeText(url).then(() => {
            alert(t.link_copied || "Link copied to clipboard")
        })
    }



    return (
        <>
            <div className="hidden md:flex h-screen w-[260px] flex-col border-r transition-colors duration-300
                bg-white text-zinc-900 border-zinc-200
                dark:bg-zinc-950 dark:text-zinc-300 dark:border-zinc-800">

                {/* Header / Brand */}
                <div className="p-3">
                    <div className="flex items-center justify-between px-2 py-2">
                        <Link href="/" className="flex items-center gap-2 rounded-md p-2 transition-colors flex-1
                            hover:bg-zinc-100 dark:hover:bg-zinc-900">
                            <div className="h-6 w-6 rounded-full overflow-hidden border border-red-100 dark:border-red-900 shrink-0">
                                <img src="/mascot.jpg" alt="Logo" className="w-full h-full object-cover" />
                            </div>
                            <span className="font-bold text-sm text-zinc-800 dark:text-zinc-100">KNU MLA</span>
                        </Link>
                    </div>
                </div>

                {/* Navigation */}
                <div className="flex-1 overflow-y-auto px-3 py-2 scrollbar-thin scrollbar-thumb-zinc-300 dark:scrollbar-thumb-zinc-800 scrollbar-track-transparent">
                    <nav className="space-y-6">
                        {/* Main Actions */}
                        <div className="space-y-1">
                            <button
                                onClick={onNewChat}
                                className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-all font-medium border border-transparent shadow-sm hover:shadow-md
                                bg-white text-zinc-900 ring-1 ring-zinc-200 hover:ring-red-200
                                dark:bg-zinc-900 dark:text-white dark:ring-zinc-800 dark:hover:ring-red-900/50 group mb-2"
                            >
                                <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-red-100 text-red-600 group-hover:bg-red-600 group-hover:text-white transition-colors dark:bg-red-900/30 dark:text-red-400">
                                    <SquarePen className="h-3.5 w-3.5" />
                                </div>
                                <span className="group-hover:text-red-600 dark:group-hover:text-red-400 transition-colors">{t.new_chat}</span>
                            </button>

                            <button
                                onClick={() => setIsSearchOpen(!isSearchOpen)}
                                className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-all font-medium border border-transparent shadow-sm hover:shadow-md
                                bg-white text-zinc-900 ring-1 ring-zinc-200 hover:ring-blue-200
                                dark:bg-zinc-900 dark:text-white dark:ring-zinc-800 dark:hover:ring-blue-900/50 group mb-2"
                            >
                                <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-blue-100 text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors dark:bg-blue-900/30 dark:text-blue-400">
                                    <Search className="h-3.5 w-3.5" />
                                </div>
                                <span className="group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{t.search_chats}</span>
                            </button>

                            <button
                                onClick={() => setMemoOpen(true)}
                                className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-all font-medium border border-transparent shadow-sm hover:shadow-md
                                bg-white text-zinc-900 ring-1 ring-zinc-200 hover:ring-amber-200
                                dark:bg-zinc-900 dark:text-white dark:ring-zinc-800 dark:hover:ring-amber-900/50 group mb-2"
                            >
                                <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-amber-100 text-amber-600 group-hover:bg-amber-600 group-hover:text-white transition-colors dark:bg-amber-900/30 dark:text-amber-400">
                                    <StickyNote className="h-3.5 w-3.5" />
                                </div>
                                <span className="group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors">{t.memo_title}</span>
                            </button>

                            {/* Projects Section */}
                            <div className="flex items-center justify-between px-3 pt-6 pb-2">
                                <span className="text-xs font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">{t.projects_title}</span>
                            </div>

                            <button
                                onClick={() => setProjectDialogOpen(true)}
                                className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-all font-medium border border-transparent shadow-sm hover:shadow-md
                                bg-white text-zinc-900 ring-1 ring-zinc-200 hover:ring-purple-200
                                dark:bg-zinc-900 dark:text-white dark:ring-zinc-800 dark:hover:ring-purple-900/50 group"
                            >
                                <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-purple-100 text-purple-600 group-hover:bg-purple-600 group-hover:text-white transition-colors dark:bg-purple-900/30 dark:text-purple-400">
                                    <FolderPlus className="h-3.5 w-3.5" />
                                </div>
                                <span className="group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">{t.new_project}</span>
                            </button>

                            {projects.length > 0 && projects.map((project) => (
                                <div key={project.id} className="flex flex-col select-none">
                                    <div
                                        className="group relative flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors
                                        text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900
                                        dark:text-zinc-400 dark:hover:bg-zinc-900 dark:hover:text-zinc-200 cursor-pointer"
                                        onClick={(e) => toggleProject(e, project.id)}>

                                        <div className="flex items-center gap-2 flex-1 overflow-hidden">
                                            <span className={`transition-transform duration-200 text-zinc-400 ${expandedProjects.has(project.id) ? 'rotate-90' : ''}`}>
                                                ▶
                                            </span>
                                            <Briefcase className={cn("h-4 w-4 shrink-0 transition-colors", project.color || "text-zinc-500")} />
                                            <span className="truncate text-left flex-1">{project.name}</span>
                                            {/* Count badge */}
                                            {history.filter(h => h.projectId === project.id).length > 0 && (
                                                <span className="text-[10px] bg-zinc-100 dark:bg-zinc-800 px-1.5 py-0.5 rounded-full text-zinc-500 font-medium">
                                                    {history.filter(h => h.projectId === project.id).length}
                                                </span>
                                            )}
                                        </div>

                                        {/* Action Buttons */}
                                        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity absolute right-2 bg-zinc-100 dark:bg-zinc-900 shadow-sm rounded-md px-1" onClick={e => e.stopPropagation()}>
                                            <button
                                                onClick={(e) => handleShare(e, 'project', project.id)}
                                                className="p-1.5 text-zinc-500 hover:text-green-600 hover:bg-zinc-200 dark:hover:bg-zinc-800 rounded-md transition-colors"
                                                title={t.share || "Share"}
                                            >
                                                <Share2 className="h-3 w-3" />
                                            </button>
                                            <button
                                                onClick={(e) => openEditModal(e, project)}
                                                className="p-1.5 text-zinc-500 hover:text-blue-600 hover:bg-zinc-200 dark:hover:bg-zinc-800 rounded-md transition-colors"
                                                title={t.edit || "Edit"}
                                            >
                                                <Edit2 className="h-3 w-3" />
                                            </button>
                                            <button
                                                onClick={(e) => handleDeleteProject(e, project.id)}
                                                className="p-1.5 text-zinc-500 hover:text-red-600 hover:bg-zinc-200 dark:hover:bg-zinc-800 rounded-md transition-colors"
                                                title={t.delete || "Delete"}
                                            >
                                                <Trash2 className="h-3 w-3" />
                                            </button>
                                        </div>
                                    </div>

                                    {/* Render Chats inside Project */}
                                    {expandedProjects.has(project.id) && (
                                        <div className="pl-4 mt-1 space-y-0.5 border-l-2 border-zinc-100 dark:border-zinc-800 ml-4 mb-2 animate-in slide-in-from-top-2 duration-200">
                                            {history.filter(chat => chat.projectId === project.id).length > 0 ? (
                                                history.filter(chat => chat.projectId === project.id).map(chat => (
                                                    <ChatListItem
                                                        key={chat.id}
                                                        chat={chat}
                                                        searchQuery={searchQuery}
                                                        handleShare={handleShare}
                                                        onPin={() => onPinChat?.(chat.id)}
                                                        onDelete={() => onDeleteChat?.(chat.id)}
                                                        onRename={(newTitle) => onRenameChat?.(chat.id, newTitle)}
                                                        onMove={(projectId) => onMoveChat?.(chat.id, projectId)}
                                                        projects={projects}
                                                        t={t}
                                                    />
                                                ))
                                            ) : (
                                                <div className="px-3 py-2 text-[10px] text-zinc-400 italic">
                                                    Empty project
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            ))}

                            {projects.length === 0 && (
                                <div className="px-3 py-2 text-xs text-zinc-400 italic">
                                    {t.no_projects}
                                </div>
                            )}

                            {/* History Section */}{isSearchOpen && (
                                <div className="px-1 py-2 animate-in fade-in slide-in-from-top-2 duration-200">
                                    <input
                                        type="text"
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        placeholder={t.search_chats + "..."}
                                        className="w-full rounded-md border border-zinc-200 bg-zinc-50 px-3 py-1.5 text-sm outline-none focus:border-red-300 focus:ring-2 focus:ring-red-100 dark:border-zinc-800 dark:bg-zinc-900 dark:focus:border-red-900"
                                        autoFocus
                                    />
                                </div>
                            )}

                            <div className="flex items-center justify-between px-3 pt-4 pb-2">
                                <span className="text-xs font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">{t.history_title}</span>
                            </div>

                            {/* Pinned Chats */}
                            {filteredHistory.filter(c => c.pinned).length > 0 && (
                                <div className="mb-2">
                                    <div className="px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-zinc-400 flex items-center gap-1">
                                        <Pin className="h-3 w-3" /> Pinned
                                    </div>
                                    {filteredHistory.filter(c => c.pinned).map(chat => (
                                        <ChatListItem
                                            key={chat.id}
                                            chat={chat}
                                            searchQuery={searchQuery}
                                            handleShare={handleShare}
                                            onPin={() => onPinChat?.(chat.id)}
                                            onDelete={() => onDeleteChat?.(chat.id)}
                                            onRename={(newTitle) => onRenameChat?.(chat.id, newTitle)}
                                            onMove={(projectId) => onMoveChat?.(chat.id, projectId)}
                                            projects={projects}
                                            t={t}
                                        />
                                    ))}
                                </div>
                            )}

                            {/* Recent (Unpinned) Chats */}
                            {filteredHistory.filter(c => !c.pinned).length > 0 ? (
                                filteredHistory.filter(c => !c.pinned).map((chat) => (
                                    <ChatListItem
                                        key={chat.id}
                                        chat={chat}
                                        searchQuery={searchQuery}
                                        handleShare={handleShare}
                                        onPin={() => onPinChat?.(chat.id)}
                                        onDelete={() => onDeleteChat?.(chat.id)}
                                        onRename={(newTitle) => onRenameChat?.(chat.id, newTitle)}
                                        onMove={(projectId) => onMoveChat?.(chat.id, projectId)}
                                        projects={projects}
                                        t={t}
                                    />
                                ))
                            ) : (
                                filteredHistory.length === 0 && (
                                    <div className="px-3 py-4 text-center text-xs text-zinc-400 italic">
                                        {searchQuery ? "No results found" : "No history"}
                                    </div>
                                )
                            )}
                        </div>
                    </nav>
                </div>

                {/* User Profile */}
                <div className="border-t p-3
                    border-zinc-200 bg-zinc-50
                    dark:border-zinc-900 dark:bg-transparent">
                    <button
                        onClick={() => setSettingsOpen(true)}
                        className="flex w-full items-center gap-3 rounded-md px-3 py-3 text-sm transition-colors text-left
                        hover:bg-zinc-200 dark:hover:bg-zinc-900 group relative">
                        <div className="h-8 w-8 rounded-full flex items-center justify-center shrink-0 border shadow-sm
                            bg-white border-zinc-200 text-zinc-600
                            dark:bg-zinc-800 dark:border-zinc-700 dark:text-zinc-400 overflow-hidden">
                            {user?.avatar ? (
                                <img src={user.avatar} alt="User" className="h-full w-full object-cover" />
                            ) : (
                                <User className="h-5 w-5" />
                            )}
                        </div>
                        <div className="flex-1 overflow-hidden">
                            <div className="truncate font-bold text-zinc-900 dark:text-zinc-100">{user?.name || t.guest_user}</div>
                            <div className="truncate text-xs text-zinc-500 font-medium group-hover:text-red-600 transition-colors">@{user?.id || "student"}</div>
                        </div>

                        <Settings2 className="h-4 w-4 text-zinc-400 dark:text-zinc-500 group-hover:text-zinc-600 dark:group-hover:text-zinc-300 transition-colors" />
                    </button>
                </div>
            </div>



            <SettingsDialog open={settingsOpen} onClose={() => setSettingsOpen(false)} />
            <CreateProjectDialog
                open={projectDialogOpen}
                onClose={() => setProjectDialogOpen(false)}
                onCreate={handleCreateProject}
            />
            <MemoDialog open={memoOpen} onClose={() => setMemoOpen(false)} />

            {/* Edit Project Modal */}
            {editingProject && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in">
                    <div className="w-full max-w-sm bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-xl rounded-lg p-6 space-y-4 animate-in zoom-in-95">
                        <div className="flex justify-between items-center">
                            <h3 className="font-semibold text-lg">{t.edit_project}</h3>
                            <button onClick={() => setEditingProject(null)}><div className="h-4 w-4" /></button>
                        </div>
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-zinc-500">Name</label>
                            <Input value={editName} onChange={(e) => setEditName(e.target.value)} />
                        </div>

                        <div className="flex justify-end gap-2 pt-2">
                            <Button variant="ghost" onClick={() => setEditingProject(null)}>Cancel</Button>
                            <Button onClick={handleUpdateProject}>Save</Button>
                        </div>
                    </div>
                </div>
            )}
        </>
    )
}

// Sub-component for Chat List Item to cleaner code
function ChatListItem({ chat, searchQuery, handleShare, onPin, onDelete, onRename, onMove, projects, t }: any) {
    return (
        <div className="group relative flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors
            text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900
            dark:text-zinc-400 dark:hover:bg-zinc-900 dark:hover:text-zinc-200 cursor-pointer">
            <MessageSquare className="h-4 w-4 shrink-0 transition-colors
                text-zinc-400 group-hover:text-red-500
                dark:text-zinc-500 dark:group-hover:text-zinc-300" />
            <span className="truncate text-left flex-1" dangerouslySetInnerHTML={{
                __html: searchQuery ? chat.title.replace(new RegExp(`(${searchQuery})`, 'gi'), '<span class="bg-yellow-200 dark:bg-yellow-900 text-black dark:text-white">$1</span>') : chat.title
            }} />

            <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity absolute right-2 bg-zinc-100 dark:bg-zinc-900 shadow-sm rounded-md px-1" onClick={(e) => e.stopPropagation()}>
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <button className="p-1.5 text-zinc-500 hover:text-zinc-900 hover:bg-zinc-200 dark:hover:bg-zinc-800 rounded-md transition-colors">
                            <MoreHorizontal className="h-3.5 w-3.5" />
                        </button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-48">
                        <DropdownMenuItem onClick={() => onPin()}>
                            <Pin className="mr-2 h-3.5 w-3.5" /> {chat.pinned ? "Unpin" : "Pin Chat"}
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={(e) => handleShare(e, 'chat', chat.id)}>
                            <Share2 className="mr-2 h-3.5 w-3.5" /> {t.share || "Share"}
                        </DropdownMenuItem>

                        <DropdownMenuSub>
                            <DropdownMenuSubTrigger>
                                <Folder className="mr-2 h-3.5 w-3.5" /> Move to Project
                            </DropdownMenuSubTrigger>
                            <DropdownMenuSubContent className="w-48">
                                <DropdownMenuLabel>Select Project</DropdownMenuLabel>
                                <DropdownMenuSeparator />
                                {projects.length > 0 ? projects.map((p: any) => (
                                    <DropdownMenuItem key={p.id} onClick={() => onMove(p.id)}>
                                        {p.name}
                                    </DropdownMenuItem>
                                )) : (
                                    <div className="px-2 py-1.5 text-xs text-zinc-500">No projects</div>
                                )}
                            </DropdownMenuSubContent>
                        </DropdownMenuSub>

                        <DropdownMenuSeparator />
                        <DropdownMenuItem onClick={() => {
                            const newName = prompt("New chat name:", chat.title)
                            if (newName) onRename(newName)
                        }}>
                            <Edit2 className="mr-2 h-3.5 w-3.5" /> Rename
                        </DropdownMenuItem>
                        <DropdownMenuItem className="text-red-600 focus:text-red-600 focus:bg-red-50 dark:focus:bg-red-900/10" onClick={() => onDelete()}>
                            <Trash className="mr-2 h-3.5 w-3.5" /> Delete
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
        </div>
    )
}
