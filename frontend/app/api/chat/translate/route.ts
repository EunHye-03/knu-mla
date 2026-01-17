import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const { text, target_lang } = await request.json();

        // Simulation Logic
        const translatedText = `[Translated to ${target_lang}]: ${text}`;

        return NextResponse.json({
            role: "ai",
            content: translatedText
        });

    } catch (error) {
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
