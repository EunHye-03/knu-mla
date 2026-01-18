import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { email } = body;

        console.log(`[Mock API - Forgot Password] Request received`);
        console.log(`[Mock API - Forgot Password] Email: ${email}`);

        // Basic validation
        if (!email || !email.includes('@')) {
            console.log(`[Mock API - Forgot Password] Invalid email format`);
            return NextResponse.json(
                { success: false, message: 'Invalid email address' },
                { status: 400 }
            );
        }

        // Simulate successful password reset email sent
        console.log(`[Mock API - Forgot Password] ✓ Reset link sent to: ${email}`);

        // In a real implementation, you would:
        // 1. Check if user exists
        // 2. Generate a secure reset token
        // 3. Store token with expiration
        // 4. Send email with reset link

        return NextResponse.json({
            success: true,
            message: 'If an account exists, a reset link has been sent.',
            email: email // For debugging only, remove in production
        });
    } catch (error) {
        console.error('[Mock API - Forgot Password] Error:', error);
        return NextResponse.json(
            { success: false, message: 'Internal Server Error' },
            { status: 500 }
        );
    }
}
