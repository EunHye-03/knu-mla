"use client"

import * as React from "react"
import { useRouter, usePathname } from "next/navigation"

interface User {
    id: string
    name: string
    password?: string // In a real app, never store plain passwords on client
    avatar?: string
}

interface AuthContextType {
    user: User | null
    login: (id: string, password?: string) => boolean
    register: (name: string, id: string, password?: string) => void
    logout: () => void
    updateUser: (data: Partial<User>) => void
    isLoading: boolean
}

const AuthContext = React.createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = React.useState<User | null>(null)
    const [isLoading, setIsLoading] = React.useState(true)
    const router = useRouter()
    const pathname = usePathname()

    React.useEffect(() => {
        // Check local storage on mount
        const storedUser = localStorage.getItem("knu_mla_user")
        if (storedUser) {
            setUser(JSON.parse(storedUser))
        }
        setIsLoading(false)
    }, [])

    React.useEffect(() => {
        if (!isLoading && !user && pathname !== "/login" && pathname !== "/register") {
            router.push("/login")
        }
    }, [user, isLoading, pathname, router])

    const login = (id: string, password?: string) => {
        // 1. Try to find user in our mock "database"
        const usersDbStr = localStorage.getItem("knu_mla_users_db")
        let foundUser: User | null = null

        if (usersDbStr) {
            const usersDb = JSON.parse(usersDbStr) as User[]
            foundUser = usersDb.find(u => u.id === id) || null
        }

        // 2. If found, use that user's name. If not, default to ID (mock behavior for strictly prototyping)
        const userToLogin: User = foundUser || {
            id: id,
            name: id,
            avatar: "/mascot.jpg"
        }

        // 3. Set Session
        localStorage.setItem("knu_mla_user", JSON.stringify(userToLogin))
        setUser(userToLogin)
        router.push("/")
        return true
    }

    const register = (name: string, id: string, password?: string) => {
        const newUser: User = {
            id: id,
            name: name,
            avatar: "/mascot.jpg"
        }

        // 1. Save to Session
        localStorage.setItem("knu_mla_user", JSON.stringify(newUser))
        setUser(newUser)

        // 2. Save to Mock "Database" so login remembers the name later
        const usersDbStr = localStorage.getItem("knu_mla_users_db")
        const usersDb = usersDbStr ? JSON.parse(usersDbStr) as User[] : []

        // Remove existing if any (overwrite)
        const tempDb = usersDb.filter(u => u.id !== id)
        tempDb.push(newUser)

        localStorage.setItem("knu_mla_users_db", JSON.stringify(tempDb))

        router.push("/")
    }

    const logout = () => {
        localStorage.removeItem("knu_mla_user")
        setUser(null)
        router.push("/login")
    }

    const updateUser = (data: Partial<User>) => {
        if (user) {
            const updatedUser = { ...user, ...data }
            localStorage.setItem("knu_mla_user", JSON.stringify(updatedUser))
            setUser(updatedUser)
        }
    }

    if (isLoading) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-zinc-950">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-red-500 border-t-transparent" />
            </div>
        )
    }

    return (
        <AuthContext.Provider value={{ user, login, logout, updateUser, register, isLoading }}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = React.useContext(AuthContext)
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider")
    }
    return context
}
