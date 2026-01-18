# 🚀 KNU MLA: Demo Loyihani Deploy Qilish Qo‘llanmasi

Ushbu qo‘llanma loyihani **Render** (Backend) va **Vercel** (Frontend) platformalariga joylashtirish bosqichlarini tushuntiradi.

---

## 1. Backend (Render) - Python FastAPI

Backend qismini Render platformasiga joylashtirish uchun quyidagi amallarni bajaring:

1. **GitHub Repositoriyasi:** Backend kodlaringiz GitHub'ga yuklangan bo'lishi kerak.
2. **Render'da Yangi Xizmat:**
   - [Render Dashboard](https://dashboard.render.com/)'ga kiring.
   - **"New +"** tugmasini bosing va **"Web Service"**ni tanlang.
   - GitHub repositoriyangizni ulash orqali loyihani tanlang.
3. **Sozlamalar (Settings):**
   - **Environment:** `Python 3` (Loyiha Python'da yozilgan).
   - **Runtime:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app` (Yoki `uvicorn app.main:app --host 0.0.0.0 --port $PORT`)
   - **Eslatma:** Men siz uchun `render.yaml` faylini yaratdim. Render'da "Blueprint" tanlasangiz, hamma sozlamalar avtomatik yuklanadi.
4. **Environment Variables:**
   - **"Environment"** bo'limiga o'ting va quyidagi o'zgaruvchilarni qo'shing:
     - `DATABASE_URL`: Ma'lumotlar bazasi manzili (SQLite yoki PostgreSQL).
     - `JWT_SECRET`: Maxfiy kalit (xohlagan uzun matn).
     - `CORS_ORIGINS`: `*` yoki Vercel'dagi frontend URL manzilingiz.
5. **Deploy:** "Create Web Service" tugmasini bosing. Deploy tugagandan so'ng Render sizga `https://knu-mla-backend.onrender.com` kabi backend URL manzilini beradi. **Buni nusxalab oling.**

---

## 2. Frontend (Vercel) - Next.js

Frontend qismini Vercel platformasiga joylashtirish:

1. **Vercel'da Yangi Proyekt:**
   - [Vercel Dashboard](https://vercel.com/dashboard)'ga kiring.
   - **"Add New..."** -> **"Project"**ni tanlang.
   - GitHub repositoriyangizdan `frontend` papkasini tanlang.
2. **Environment Variables:**
   - **"Environment Variables"** bo'limida quyidagini qo'shing:
     - `NEXT_PUBLIC_API_URL`: Render'dan olgan backend URL manzilingiz (masalan: `https://knu-mla-backend.onrender.com`).
3. **Deploy:** **"Deploy"** tugmasini bosing. Vercel sizga frontend uchun maxsus URL (masalan: `https://knu-mla.vercel.app`) beradi.

---

## 3. Yakuniy Test Qilish

Hammasi to'g'ri ishlayotganini tekshirish:

1. **Frontend'ga kiring:** Vercel bergan URL'ni oching.
2. **Login/Register:** Yangi akkount yarating yoki kirib ko'ring.
3. **Chatni tekshiring:** AI bilan suhbatlashib ko'ring.
4. **Hujjatlar:** PDF yoki PPTX yuklab, uning natijasini kuting.

### ❓ Mumkin bo‘lgan xatolar (Troubleshooting):
- **API Xatoligi (Network Error):** `NEXT_PUBLIC_API_URL` manzili oxirida `/` belgisi bor-yo'qligini va manzil to'g'riligini tekshiring.
- **CORS Muammosi:** Backend'da `CORS_ORIGINS` o'zgaruvchisi frontend URL manzilingizga ruxsat berganiga ishonch hosil qiling.
- **Database Error:** Agar SQLite foydalanayotgan bo'lsangiz, Render'da ma'lumotlar saqlanib qolmaydi (Disk ulanishi kerak). Real foydalanish uchun PostgreSQL (masalan, Neon yoki Railway) tavsiya etiladi.

---
✅ **Deploy Tayyor!** Loyihangiz endi hamma uchun onlayn!
