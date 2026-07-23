# Proje Kuralları

## Web Sitesi Yönetimi

- "Web sitesini kapat", "durdur" veya benzeri bir kapatma komutu verildiğinde hem **frontend** (Vite - port 3000) hem de **backend** (Uvicorn - port 8000) sunucuları birlikte kapatılmalıdır.
- "Web sitesini başlat" veya "aç" komutu verildiğinde hem frontend hem backend birlikte başlatılmalıdır.

## Sunucu Bilgileri (AI_Agent_Web_v2.0)

- **Frontend**: `AI_Agent_Web_v2.0/frontend` dizininde `npm run dev` komutu ile başlatılır (port 3000).
- **Backend**: `AI_Agent_Web_v2.0/backend` dizininde `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload` komutu ile başlatılır.
