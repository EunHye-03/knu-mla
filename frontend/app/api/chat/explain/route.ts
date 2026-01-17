import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const { term } = await request.json();

        // Simulation Logic
        const explanation = `**${term}**\n\nDefinition: A specific concept or acronym often used in this context.\n\nContext: In the KNU system, this usually refers to the academic module or administrative process involving student registration.\n\nRelated: [Visa], [Course Schedule]`;

        return NextResponse.json({
            role: "ai",
            content: explanation
        });

    } catch (error) {
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
