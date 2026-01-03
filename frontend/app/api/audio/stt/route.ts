import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const formData = await request.formData();
        const file = formData.get('file') as Blob;

        if (!file) {
            return NextResponse.json({ error: 'No audio file uploaded' }, { status: 400 });
        }

        // Logic to send to real STT service would go here.
        // For now, we return a mock transcription.

        return NextResponse.json({
            text: "This is a simulated transcription of the voice message. The user asked about the dormitory opening hours."
        });

    } catch (error) {
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
