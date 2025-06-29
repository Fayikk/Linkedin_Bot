#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Bot - Otomatik Chrome/ChromeDriver Kurulum Scripti
Kullanıcının bilgisayarına gerekli bileşenleri otomatik kurar
"""

import os
import sys
import platform
import requests
import zipfile
import subprocess
import shutil
from pathlib import Path
import json

class AutoInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.architecture = platform.machine().lower()
        self.chrome_installed = False
        self.chromedriver_installed = False
        
    def log(self, message):
        print(f"🔧 {message}")
        
    def check_chrome_installation(self):
        """Chrome kurulu mu kontrol et"""
        try:
            if self.system == "windows":
                # Windows Chrome yolları
                chrome_paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
                ]
                for path in chrome_paths:
                    if os.path.exists(path):
                        self.log(f"✅ Chrome bulundu: {path}")
                        self.chrome_installed = True
                        return True
                        
            elif self.system == "darwin":  # macOS
                chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
                if os.path.exists(chrome_path):
                    self.log(f"✅ Chrome bulundu: {chrome_path}")
                    self.chrome_installed = True
                    return True
                    
            elif self.system == "linux":
                # Linux Chrome kontrol
                result = subprocess.run(["which", "google-chrome"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.log(f"✅ Chrome bulundu: {result.stdout.strip()}")
                    self.chrome_installed = True
                    return True
                    
        except Exception as e:
            self.log(f"Chrome kontrol hatası: {e}")
            
        self.log("❌ Chrome bulunamadı")
        return False
        
    def get_chrome_version(self):
        """Chrome sürümünü öğren"""
        try:
            if self.system == "windows":
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   r"Software\Google\Chrome\BLBeacon")
                version, _ = winreg.QueryValueEx(key, "version")
                return version
                
            elif self.system == "darwin":
                result = subprocess.run([
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", 
                    "--version"
                ], capture_output=True, text=True)
                return result.stdout.strip().split()[-1]
                
            elif self.system == "linux":
                result = subprocess.run(["google-chrome", "--version"], 
                                      capture_output=True, text=True)
                return result.stdout.strip().split()[-1]
                
        except Exception as e:
            self.log(f"Chrome sürüm öğrenme hatası: {e}")
            return None
            
    def install_chrome(self):
        """Chrome'u otomatik kur"""
        try:
            self.log("🔄 Chrome kuruluyor...")
            
            if self.system == "windows":
                # Windows Chrome indirme ve kurma
                chrome_url = "https://dl.google.com/chrome/install/375.126/chrome_installer.exe"
                installer_path = "chrome_installer.exe"
                
                self.log("📥 Chrome indiriliyor...")
                response = requests.get(chrome_url)
                with open(installer_path, 'wb') as f:
                    f.write(response.content)
                    
                self.log("⚙️ Chrome kuruluyor (yönetici izni gerekebilir)...")
                subprocess.run([installer_path, "/silent", "/install"], check=True)
                os.remove(installer_path)
                
            elif self.system == "darwin":
                # macOS Chrome kurulum
                self.log("📱 macOS için Chrome'u manuel kurmanız gerekiyor")
                self.log("🌐 https://www.google.com/chrome/ adresinden indirin")
                return False
                
            elif self.system == "linux":
                # Linux Chrome kurulum
                self.log("📥 Chrome APT deposu ekleniyor...")
                subprocess.run([
                    "wget", "-q", "-O", "-", 
                    "https://dl.google.com/linux/linux_signing_key.pub"
                ], check=True)
                subprocess.run([
                    "sudo", "apt-key", "add", "-"
                ], check=True)
                subprocess.run([
                    "sudo", "sh", "-c", 
                    'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
                ], check=True)
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "google-chrome-stable"], check=True)
                
            self.log("✅ Chrome kurulumu tamamlandı")
            return True
            
        except Exception as e:
            self.log(f"❌ Chrome kurulum hatası: {e}")
            return False
            
    def download_chromedriver(self, chrome_version):
        """ChromeDriver'ı indir ve kur"""
        try:
            self.log("🔄 ChromeDriver indiriliyor...")
            
            # Chrome sürümüne uygun ChromeDriver URL'si
            major_version = chrome_version.split('.')[0]
            
            # Platform ve mimari belirleme
            if self.system == "windows":
                platform_name = "win64" if "64" in self.architecture else "win32"
                driver_name = "chromedriver.exe"
            elif self.system == "darwin":
                platform_name = "mac-arm64" if "arm" in self.architecture else "mac-x64"
                driver_name = "chromedriver"
            else:  # linux
                platform_name = "linux64"
                driver_name = "chromedriver"
                
            # ChromeDriver indirme URL'si
            base_url = "https://storage.googleapis.com/chrome-for-testing-public"
            driver_url = f"{base_url}/{chrome_version}/{platform_name}/chromedriver-{platform_name}.zip"
            
            # Chromedriver klasörü oluştur
            driver_dir = Path("chromedriver")
            driver_dir.mkdir(exist_ok=True)
            
            # ZIP dosyasını indir
            self.log(f"📥 {driver_url} indiriliyor...")
            response = requests.get(driver_url)
            response.raise_for_status()
            
            zip_path = driver_dir / "chromedriver.zip"
            with open(zip_path, 'wb') as f:
                f.write(response.content)
                
            # ZIP'i aç
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(driver_dir)
                
            # ChromeDriver binary'sini doğru yere taşı
            extracted_dir = driver_dir / f"chromedriver-{platform_name}"
            driver_src = extracted_dir / driver_name
            driver_dest = driver_dir / driver_name
            
            if driver_src.exists():
                shutil.move(str(driver_src), str(driver_dest))
                
            # Temizlik
            zip_path.unlink()
            if extracted_dir.exists():
                shutil.rmtree(extracted_dir)
                
            # Linux/macOS için execute permission
            if self.system != "windows":
                os.chmod(driver_dest, 0o755)
                
            self.log(f"✅ ChromeDriver kuruldu: {driver_dest}")
            self.chromedriver_installed = True
            return True
            
        except Exception as e:
            self.log(f"❌ ChromeDriver kurulum hatası: {e}")
            return False
            
    def install_python_requirements(self):
        """Python gereksinimlerini kur"""
        try:
            self.log("🔄 Python paketleri kuruluyor...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            self.log("✅ Python paketleri kuruldu")
            return True
        except Exception as e:
            self.log(f"❌ Python paket kurulum hatası: {e}")
            return False
            
    def run_installation(self):
        """Tam kurulum işlemini çalıştır"""
        self.log("🚀 LinkedIn Bot Otomatik Kurulum Başlatılıyor...")
        self.log(f"💻 Sistem: {self.system} ({self.architecture})")
        
        # Chrome kontrol et
        if not self.check_chrome_installation():
            self.log("🔄 Chrome kurulacak...")
            if not self.install_chrome():
                self.log("❌ Chrome kurulumu başarısız!")
                return False
                
        # Chrome sürümünü öğren
        chrome_version = self.get_chrome_version()
        if not chrome_version:
            self.log("❌ Chrome sürümü öğrenilemedi!")
            return False
            
        self.log(f"📋 Chrome sürümü: {chrome_version}")
        
        # ChromeDriver kur
        if not self.download_chromedriver(chrome_version):
            self.log("❌ ChromeDriver kurulumu başarısız!")
            return False
            
        # Python paketleri kur
        if not self.install_python_requirements():
            self.log("❌ Python paketleri kurulumu başarısız!")
            return False
            
        self.log("🎉 Kurulum başarıyla tamamlandı!")
        self.log("🚀 Artık LinkedIn Bot'u çalıştırabilirsiniz:")
        self.log("   • Web arayüzü için: python web_gui.py")
        self.log("   • Masaüstü arayüzü için: python gui_app.py")
        
        return True

if __name__ == "__main__":
    installer = AutoInstaller()
    success = installer.run_installation()
    
    if success:
        print("\n" + "="*50)
        print("✅ KURULUM TAMAMLANDI!")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("❌ KURULUM BAŞARISIZ!")
        print("="*50)
        sys.exit(1)
