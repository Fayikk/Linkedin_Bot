@echo off
title LinkedIn Bot - Web GUI
echo.
echo ========================================
echo   🌐 LinkedIn Bot - Web Arayüzü
echo ========================================
echo.
echo 🔧 Sistem kontrol ediliyor...

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Lütfen Python'u yükleyin.
    pause
    exit /b 1
)

REM Gerekli paketleri yükle
echo 📦 Gerekli paketler kontrol ediliyor...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo 📥 Flask ve gerekli paketler yükleniyor...
    pip install flask flask-socketio
)

echo.
echo 🚀 LinkedIn Bot Web Arayüzü başlatılıyor...
echo.
echo 🌐 Tarayıcınızda şu adresi açın: http://localhost:5000
echo.
echo 💡 Bu pencereyi kapatmayın!
echo ⚠️  Web arayüzü çalışmaya devam edecek...
echo.

python web_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Web arayüzü başlatılamadı!
    echo 🔧 Manuel çalıştırın: python web_gui.py
    pause
)
