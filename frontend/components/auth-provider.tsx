"use client"

import * as React from "react"
import { useRouter, usePathname } from "next/navigation"
import { api } from "@/services/api"

interface User {
    id: string
    name: string
    email?: string
    avatar?: string
    background_image_url?: string
}

interface AuthContextType {
    user: User | null
    login: (id: string, password?: string) => Promise<boolean>
    register: (name: string, id: string, password?: string, email?: string) => Promise<boolean>
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
        const storedToken = localStorage.getItem("knu_mla_token")
        if (storedUser && storedToken) {
            setUser(JSON.parse(storedUser))
        }
        setIsLoading(false)

        const handleAuthError = () => {
            logout();
        };
        window.addEventListener('auth-error', handleAuthError);
        return () => window.removeEventListener('auth-error', handleAuthError);
    }, [])

    React.useEffect(() => {
        if (!isLoading && !user && pathname !== "/login" && pathname !== "/register") {
            router.push("/login")
        }
    }, [user, isLoading, pathname, router])

    const login = async (id: string, password?: string): Promise<boolean> => {
        try {
            setIsLoading(true)
            // Call API
            const tokenData = await api.login(id, password || "");

            // Save Token
            localStorage.setItem("knu_mla_token", tokenData.access_token);

            // Get User Info
            const userData = await api.getMe();

            const loggedUser: User = {
                id: userData.user_id,
                name: userData.nickname,
                email: userData.email,
                avatar: userData.profile_image_url || "/mascot.jpg",
            };

            localStorage.setItem("knu_mla_user", JSON.stringify(loggedUser))
            setUser(loggedUser)
            router.push("/")
            return true
        } catch (error) {
            console.error("Login failed", error);
            alert("Login Failed: " + (error as Error).message);
            return false;
        } finally {
            setIsLoading(false);
        }
    }

    const register = async (name: string, id: string, password?: string, email?: string): Promise<boolean> => {
        try {
            setIsLoading(true)
            await api.register({
                user_id: id,
                nickname: name,
                password: password || "",
                email: email || `${id}@example.com`,
                user_lang: "ko" // Default to Korean
            })
            alert("Registration successful! Please login.")
            router.push("/login")
            return true
        } catch (error) {
            console.error("Registration failed", error);
            alert("Registration Failed: " + (error as Error).message)
            return false
        } finally {
            setIsLoading(false)
        }
    }

    const logout = () => {
        localStorage.removeItem("knu_mla_user")
        localStorage.removeItem("knu_mla_token")
        setUser(null)
        router.push("/login")
    }



    const updateUser = async (data: Partial<User>) => {
        if (user) {
            try {
                // Optimistic update
                const updatedUser = { ...user, ...data }
                setUser(updatedUser)
                localStorage.setItem("knu_mla_user", JSON.stringify(updatedUser))

                // Persist to backend
                await api.updateProfile(data);
            } catch (e) {
                console.error("Failed to update profile", e);
                // Revert on failure? Or just log. For now just log.
            }
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
