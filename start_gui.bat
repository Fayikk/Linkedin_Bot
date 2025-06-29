@echo off
title LinkedIn Bot GUI Launcher
echo.
echo ========================================
echo   🤖 LinkedIn Bot GUI Launcher
echo ========================================
echo.
echo 🔧 Python ve gereksinimler kontrol ediliyor...

REM Python'un yüklü olduğunu kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Lütfen Python'u yükleyin.
    pause
    exit /b 1
)

REM Gereksinimler yüklendi mi kontrol et
echo 📦 Paketler kontrol ediliyor...
pip show selenium >nul 2>&1
if errorlevel 1 (
    echo 📥 Gerekli paketler yükleniyor...
    pip install -r requirements.txt
)

REM GUI uygulamasını başlat
echo.
echo 🚀 LinkedIn Bot GUI başlatılıyor...
echo.
python gui_app.py

if errorlevel 1 (
    echo.
    echo ❌ Uygulama çalıştırılamadı!
    echo 🔧 Hata ayıklama için manuel çalıştırın: python gui_app.py
    pause
)
