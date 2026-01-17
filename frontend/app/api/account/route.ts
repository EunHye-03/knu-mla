import { NextResponse } from 'next/server';

export async function DELETE(request: Request) {
    try {
        // Mock logic: Always succeed
        console.log(`[Mock API] Account deleted.`);

        return NextResponse.json({
            success: true,
            message: 'Account deleted successfully.'
        });
    } catch (error) {
        return NextResponse.json(
            { success: false, message: 'Internal Server Error' },
            { status: 500 }
        );
    }
}
