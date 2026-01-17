import { NextResponse } from 'next/server';

export async function GET() {
    return NextResponse.json([
        { id: "1", title: "Meeting Notes", emoji: "📅", content: "Discuss project roadmap." },
        { id: "2", title: "Ideas", emoji: "💡", content: "AI integration concepts." },
        { id: "3", title: "Shopping", emoji: "🛒", content: "Milk, Bread, Eggs." },
    ]);
}

export async function POST(request: Request) {
    const body = await request.json();
    return NextResponse.json({ id: Date.now().toString(), ...body });
}
