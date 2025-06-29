"""
LinkedIn Bot - WebDriver Sorun Giderici
Bu script WebDriver sorunlarını tespit eder ve çözer
"""

import os
import sys
import requests
import zipfile
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def check_chrome_version():
    """Chrome versiyonunu kontrol et"""
    try:
        import subprocess
        result = subprocess.run([
            'reg', 'query', 
            'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', 
            '/v', 'version'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[2]
            version = version_line.split()[-1]
            print(f"🌐 Chrome versiyonu: {version}")
            return version
        else:
            print("❌ Chrome versiyonu bulunamadı")
            return None
    except Exception as e:
        print(f"❌ Chrome versiyon kontrolü hatası: {e}")
        return None

def download_chromedriver_manually(version=None):
    """ChromeDriver'ı manuel olarak indir"""
    try:
        if not version:
            # En son stable sürümü al
            url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
            response = requests.get(url)
            version = response.text.strip()
        
        # ChromeDriver'ı indir
        driver_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
        print(f"📥 ChromeDriver indiriliyor: {driver_url}")
        
        response = requests.get(driver_url)
        if response.status_code == 200:
            # Klasör oluştur
            driver_dir = os.path.join(os.getcwd(), "chromedriver")
            os.makedirs(driver_dir, exist_ok=True)
            
            # ZIP dosyasını kaydet
            zip_path = os.path.join(driver_dir, "chromedriver.zip")
            with open(zip_path, "wb") as f:
                f.write(response.content)
            
            # ZIP'i aç
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(driver_dir)
            
            # ZIP dosyasını sil
            os.remove(zip_path)
            
            driver_path = os.path.join(driver_dir, "chromedriver.exe")
            if os.path.exists(driver_path):
                print(f"✅ ChromeDriver başarıyla indirildi: {driver_path}")
                return driver_path
            else:
                print("❌ ChromeDriver dosyası bulunamadı")
                return None
        else:
            print(f"❌ ChromeDriver indirilemedi. HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Manual indirme hatası: {e}")
        return None

def test_webdriver(driver_path=None):
    """WebDriver'ı test et"""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Test için gizli mod
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        if driver_path:
            service = Service(driver_path)
        else:
            service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ WebDriver testi başarılı! Sayfa başlığı: {title}")
        return True
        
    except Exception as e:
        print(f"❌ WebDriver testi başarısız: {e}")
        return False

def fix_webdriver_issues():
    """WebDriver sorunlarını çöz"""
    print("🔧 WebDriver Sorun Giderici")
    print("=" * 50)
    
    # 1. Chrome versiyonunu kontrol et
    chrome_version = check_chrome_version()
    
    # 2. Mevcut ChromeDriver'ı test et
    print("\n📋 Mevcut WebDriver test ediliyor...")
    if test_webdriver():
        print("✅ WebDriver sorunsuz çalışıyor!")
        return True
    
    # 3. ChromeDriver'ı temizle ve yeniden indir
    print("\n🧹 ChromeDriver cache temizleniyor...")
    try:
        import shutil
        cache_dir = os.path.expanduser("~/.wdm")
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            print("✅ Cache temizlendi")
    except Exception as e:
        print(f"⚠️ Cache temizleme hatası: {e}")
    
    # 4. Yeniden test et
    print("\n🔄 WebDriver yeniden test ediliyor...")
    if test_webdriver():
        print("✅ WebDriver düzeltildi!")
        return True
    
    # 5. Manuel indirme
    print("\n📥 ChromeDriver manuel olarak indiriliyor...")
    manual_path = download_chromedriver_manually()
    if manual_path and test_webdriver(manual_path):
        print("✅ Manuel indirme başarılı!")
        print(f"💡 Bot'unuzda bu yolu kullanın: {manual_path}")
        return True
    
    print("❌ WebDriver sorunu çözülemedi!")
    print("💡 Çözüm önerileri:")
    print("   1. Chrome tarayıcısını güncelleyin")
    print("   2. Antivirüs programını kontrol edin")
    print("   3. Windows Defender'ı kontrol edin")
    print("   4. Yönetici olarak çalıştırın")
    
    return False

if __name__ == "__main__":
    fix_webdriver_issues()
