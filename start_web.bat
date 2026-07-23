@echo off
title OpenPlexus AI Agent Web Suite Launcher
echo ===================================================
echo   OpenPlexus AI Agent Web Suite'ini Baslatiliyor...
echo ===================================================
echo.

:: Backend Baslatiliyor
echo [1/2] Arka Uç (Backend FastAPI) yeni pencerede baslatiliyor...
start "OpenPlexus Backend (FastAPI)" cmd /k "cd /d "%~dp0AI_Agent_Web_v2.0\backend" && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

:: Frontend Baslatiliyor
echo [2/2] Ön Yüz (Frontend Vite) yeni pencerede baslatiliyor...
start "OpenPlexus Frontend (Vite)" cmd /k "cd /d "%~dp0AI_Agent_Web_v2.0\frontend" && npm run dev"

echo.
echo ===================================================
echo   Her iki servis de ayri pencerelerde baslatildi!
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:80
echo ===================================================
echo.
pause
