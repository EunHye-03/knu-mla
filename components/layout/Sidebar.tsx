"use client"

import * as React from "react"
import Link from "next/link"
import {
    SquarePen,
    MessageSquare,
    User,
    MoreHorizontal
} from "lucide-react"
import { cn } from "@/lib/utils"

// Mock History Data
const history = [
    { id: 1, title: "Computer Science Lecture 1" },
    { id: 2, title: "Korean Grammar Terms" },
    { id: 3, title: "Visa Application Steps" },
    { id: 4, title: "Dormitory Rules Translation" },
]

export function Sidebar() {
    return (
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
                        <Link href="/" className="flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors font-medium
                            text-zinc-700 hover:bg-zinc-100 hover:text-red-600
                            dark:text-zinc-300 dark:hover:bg-zinc-900 dark:hover:text-white">
                            <SquarePen className="h-4 w-4" />
                            <span>New chat</span>
                        </Link>

                        <div className="flex items-center justify-between px-3 pt-4 pb-2">
                            <span className="text-xs font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">History</span>
                        </div>

                        {/* History List */}
                        {history.map((chat) => (
                            <button key={chat.id} className="group flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors
                                text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900
                                dark:text-zinc-400 dark:hover:bg-zinc-900 dark:hover:text-zinc-200">
                                <MessageSquare className="h-4 w-4 shrink-0 transition-colors
                                    text-zinc-400 group-hover:text-red-500
                                    dark:text-zinc-500 dark:group-hover:text-zinc-300" />
                                <span className="truncate text-left flex-1">{chat.title}</span>
                            </button>
                        ))}
                    </div>
                </nav>
            </div>

            {/* User Profile */}
            <div className="border-t p-3
                border-zinc-200 bg-zinc-50
                dark:border-zinc-900 dark:bg-transparent">
                <button className="flex w-full items-center gap-3 rounded-md px-3 py-3 text-sm transition-colors text-left
                    hover:bg-zinc-200 dark:hover:bg-zinc-900">
                    <div className="h-8 w-8 rounded-full flex items-center justify-center shrink-0 border shadow-sm
                        bg-white border-zinc-200 text-zinc-600
                        dark:bg-zinc-800 dark:border-zinc-700 dark:text-zinc-400">
                        <User className="h-5 w-5" />
                    </div>
                    <div className="flex-1 overflow-hidden">
                        <div className="truncate font-bold text-zinc-900 dark:text-zinc-100">Student User</div>
                        <div className="truncate text-xs text-zinc-500 font-medium">Free Plan</div>
                    </div>
                    <MoreHorizontal className="h-4 w-4 text-zinc-400 dark:text-zinc-500" />
                </button>
            </div>
        </div>
    )
}
