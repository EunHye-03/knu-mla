import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        // Mock logic: Always succeed
        console.log(`[Mock API] Reset password request:`, body);

        return NextResponse.json({
            success: true,
            message: 'Password reset successfully.'
        });
    } catch (error) {
        return NextResponse.json(
            { success: false, message: 'Internal Server Error' },
            { status: 500 }
        );
    }
}
