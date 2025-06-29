@echo off
title LinkedIn Bot - Kolay Başlatma
color 0A

echo.
echo  ==========================================
echo  🤖 LinkedIn Bot - Kolay Başlatma
echo  ==========================================
echo.

REM Python yüklü mü kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı!
    echo 📥 Python'u indirmek için: https://python.org
    pause
    exit /b 1
)

echo ✅ Python bulundu
echo.

REM requirements.txt var mı kontrol et
if not exist "requirements.txt" (
    echo ❌ requirements.txt bulunamadı!
    pause
    exit /b 1
)

echo 🔧 Python paketleri kontrol ediliyor...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Bazı paketler eksik, yükleniyor...
    pip install -r requirements.txt
)

echo ✅ Python paketleri hazır
echo.

REM .env dosyası var mı kontrol et
if not exist ".env" (
    echo ⚠️ .env dosyası bulunamadı, oluşturuluyor...
    echo LINKEDIN_EMAIL=your_email@example.com> .env
    echo LINKEDIN_PASSWORD=your_password>> .env
    echo DEFAULT_MESSAGE=Merhaba! LinkedIn'de bağlantı kurmak isterim.>> .env
    echo MAX_PROFILES_PER_SESSION=50>> .env
    echo DELAY_BETWEEN_MESSAGES=10>> .env
    echo DELAY_BETWEEN_SEARCHES=5>> .env
    echo.
    echo 📝 .env dosyası oluşturuldu. Lütfen email ve şifrenizi düzenleyin!
    pause
)

echo 🚀 Web arayüzü başlatılıyor...
echo 🌐 Tarayıcınızda http://localhost:5000 açılacak
echo.
echo 💡 Durdurmak için Ctrl+C tuşlarına basın
echo.

REM Web GUI'yi başlat
start http://localhost:5000
python web_gui.py

pause
