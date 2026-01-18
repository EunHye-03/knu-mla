"use client"

import * as React from "react"
import { Sparkles, BookOpen, GraduationCap, Users, Languages, DollarSign, Plane, Code, Briefcase, Plus } from "lucide-react"
import { cn } from "@/lib/utils"
import { ChatInput } from "@/components/chat/ChatInput"

interface ProjectDashboardProps {
    project: { id: number | string, name: string, category: string, color?: string }
    chats: any[]
    onNewChat: (text: string, mode: string, options?: { targetLang?: string }) => void
    onSelectChat: (id: number) => void
    isLoading?: boolean
}

export function ProjectDashboard({ project, chats, onNewChat, onSelectChat, isLoading }: ProjectDashboardProps) {
    const getIcon = () => {
        const iconProps = { className: cn("h-6 w-6", project.color || "text-amber-500") };
        switch (project.category) {
            case "homework": return <BookOpen {...iconProps} />;
            case "research": return <Sparkles {...iconProps} />;
            case "exam": return <GraduationCap {...iconProps} />;
            case "group": return <Users {...iconProps} />;
            case "language": return <Languages {...iconProps} />;
            case "finance": return <DollarSign {...iconProps} />;
            case "travel": return <Plane {...iconProps} />;
            case "coding": return <Code {...iconProps} />;
            default: return <Briefcase {...iconProps} />;
        }
    }

    return (
        <div className="flex flex-1 flex-col items-center p-4 md:p-10 w-full max-w-4xl mx-auto space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
            {/* Header */}
            <div className="flex w-full items-center justify-between">
                <div className="flex items-center gap-4">
                    <div className="h-12 w-12 rounded-2xl bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center shadow-sm border border-zinc-200 dark:border-zinc-700">
                        {getIcon()}
                    </div>
                    <h1 className="text-4xl font-black tracking-tight text-zinc-900 dark:text-zinc-50 font-sans italic uppercase">
                        {project.name}
                    </h1>
                </div>
            </div>

            {/* Input Bar - NOW USING STANDARDIZED CHAT INPUT */}
            <div className="w-full">
                <ChatInput onSend={onNewChat} isLoading={isLoading} />
            </div>

            {/* Chat List */}
            <div className="w-full space-y-1 mt-6">
                {chats.length > 0 ? (
                    <div className="divide-y divide-zinc-100 dark:divide-zinc-800/50">
                        {chats.map((chat) => (
                            <div
                                key={chat.id}
                                onClick={() => {
                                    console.log("DEBUG: Dashboard chat item clicked, id:", chat.id);
                                    onSelectChat(chat.id);
                                }}
                                className="group flex items-center justify-between py-6 px-4 rounded-2xl hover:bg-zinc-50/50 dark:hover:bg-zinc-900/30 cursor-pointer transition-all"
                            >
                                <div className="flex flex-col gap-1.5 flex-1 overflow-hidden mr-8">
                                    <h3 className="text-lg font-bold text-zinc-900 dark:text-zinc-100 truncate group-hover:text-red-500 transition-colors">{chat.title}</h3>
                                    <p className="text-sm text-zinc-500 dark:text-zinc-400 truncate font-medium leading-relaxed opacity-80">
                                        {chat.lastMessage || "Click to open conversation..."}
                                    </p>
                                </div>
                                <div className="flex items-center gap-6 text-sm text-zinc-400 dark:text-zinc-500 font-bold">
                                    <span className="whitespace-nowrap tabular-nums">
                                        {chat.createdAt ? new Date(chat.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : "Jan 18"}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="flex flex-col items-center justify-center py-24 text-center space-y-4">
                        <div className="h-16 w-16 rounded-full bg-zinc-50 dark:bg-zinc-900 flex items-center justify-center border border-zinc-100 dark:border-zinc-800">
                            <Plus className="h-8 w-8 text-zinc-300" />
                        </div>
                        <div className="space-y-1">
                            <p className="text-zinc-900 dark:text-zinc-100 font-bold">No chats yet</p>
                            <p className="text-zinc-500 dark:text-zinc-500 text-sm">Start your first conversation in this project above.</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
