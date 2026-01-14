"use client"

import * as React from "react"
import Link from "next/link"
import {
    SquarePen,
    MessageSquare,
    User,
    Settings2,
    MoreHorizontal,
    Search,
    FolderPlus,
    Briefcase,
    StickyNote
} from "lucide-react"
import { cn } from "@/lib/utils"
import { useAuth } from "@/components/auth-provider"
import { SettingsDialog } from "@/components/SettingsDialog"
import { useLanguage } from "@/components/layout/language-context"

import { CreateProjectDialog } from "@/components/CreateProjectDialog"
import { MemoDialog } from "@/components/MemoDialog"

// Sidebar Props
interface SidebarProps {
    history?: { id: number, title: string }[]
}

export function Sidebar({ history = [] }: SidebarProps) {
    const { user, logout } = useAuth()
    const { t } = useLanguage()
    const [settingsOpen, setSettingsOpen] = React.useState(false)
    const [projectDialogOpen, setProjectDialogOpen] = React.useState(false)
    const [memoOpen, setMemoOpen] = React.useState(false)
    const [isSearchOpen, setIsSearchOpen] = React.useState(false)
    const [searchQuery, setSearchQuery] = React.useState("")
    const [projects, setProjects] = React.useState<{ id: number, title: string, color: string }[]>([])

    const handleCreateProject = (project: { title: string, category: string }) => {
        const colors: Record<string, string> = {
            homework: "text-blue-500",
            research: "text-purple-500",
            exam: "text-red-500",
            group: "text-green-500",
            language: "text-orange-500",
            default: "text-gray-500"
        }

        const newProject = {
            id: Date.now(),
            title: project.title,
            color: colors[project.category] || colors.default
        }

        setProjects([...projects, newProject])
    }


    const filteredHistory = history.filter(chat =>
        chat.title.toLowerCase().includes(searchQuery.toLowerCase())
    )

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
                            <Link href="/" className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-all font-medium border border-transparent shadow-sm hover:shadow-md
                                bg-white text-zinc-900 ring-1 ring-zinc-200 hover:ring-red-200
                                dark:bg-zinc-900 dark:text-white dark:ring-zinc-800 dark:hover:ring-red-900/50 group mb-2">
                                <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-red-100 text-red-600 group-hover:bg-red-600 group-hover:text-white transition-colors dark:bg-red-900/30 dark:text-red-400">
                                    <SquarePen className="h-3.5 w-3.5" />
                                </div>
                                <span className="group-hover:text-red-600 dark:group-hover:text-red-400 transition-colors">{t.new_chat}</span>
                            </Link>

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
                                <button key={project.id} className="group flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors
                                    text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900
                                    dark:text-zinc-400 dark:hover:bg-zinc-900 dark:hover:text-zinc-200">
                                    <Briefcase className={cn("h-4 w-4 shrink-0 transition-colors", project.color)} />
                                    <span className="truncate text-left flex-1">{project.title}</span>
                                </button>
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

                            {/* History List */}
                            {filteredHistory.length > 0 ? (
                                filteredHistory.map((chat) => (
                                    <button key={chat.id} className="group flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors
                                        text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900
                                        dark:text-zinc-400 dark:hover:bg-zinc-900 dark:hover:text-zinc-200">
                                        <MessageSquare className="h-4 w-4 shrink-0 transition-colors
                                            text-zinc-400 group-hover:text-red-500
                                            dark:text-zinc-500 dark:group-hover:text-zinc-300" />
                                        <span className="truncate text-left flex-1" dangerouslySetInnerHTML={{
                                            __html: searchQuery ? chat.title.replace(new RegExp(`(${searchQuery})`, 'gi'), '<span class="bg-yellow-200 dark:bg-yellow-900 text-black dark:text-white">$1</span>') : chat.title
                                        }} />
                                    </button>
                                ))
                            ) : (
                                <div className="px-3 py-4 text-center text-xs text-zinc-400 italic">
                                    {searchQuery ? "No results found" : "No history"}
                                </div>
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
        </>
    )
}
