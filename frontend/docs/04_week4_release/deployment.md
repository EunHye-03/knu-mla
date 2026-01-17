# Deployment Plan

## Infrastructure
- **Frontend**: Vercel (Auto-deploy from Main).
- **Backend**: Railway / AWS EC2.
- **Database**: Supabase / MongoDB Atlas.

## Steps
1. Push final code to GitHub.
2. Verify Build Pipeline passes.
3. Check Environment Variables (`API_URL`, `OPENAI_KEY`).
4. Smoke test formatting on live URL.
