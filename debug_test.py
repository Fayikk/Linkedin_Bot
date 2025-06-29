"""
LinkedIn Bot Debug Tester
Bu script bot'un her adımını test eder ve sorunları tespit eder
"""

from linkedin_bot import LinkedInBot
from selenium.webdriver.common.by import By
import time

def debug_test():
    """Bot'u debug modunda test et"""
    print("🐛 LinkedIn Bot Debug Testi")
    print("=" * 50)
    
    with LinkedInBot() as bot:
        # 1. WebDriver Testi
        print("\n1️⃣ WebDriver Test:")
        if not bot.setup_driver():
            print("❌ WebDriver testi başarısız!")
            return False
        
        # 2. LinkedIn Ana Sayfa Testi
        print("\n2️⃣ LinkedIn Ana Sayfa Testi:")
        try:
            bot.driver.get("https://www.linkedin.com")
            print(f"✅ Ana sayfa yüklendi: {bot.driver.title}")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Ana sayfa yüklenemedi: {e}")
            return False
        
        # 3. Login Sayfası Testi
        print("\n3️⃣ Login Sayfası Testi:")
        try:
            bot.driver.get("https://www.linkedin.com/login")
            print(f"✅ Login sayfası yüklendi: {bot.driver.title}")
            time.sleep(3)
            
            # Sayfanın HTML'ini kontrol et
            print("🔍 Sayfa elementi kontrolü:")
            
            # Email alanı kontrolü
            email_selectors = ["username", "session_key", "login-email"]
            email_found = False
            for selector in email_selectors:
                try:
                    element = bot.driver.find_element(By.ID, selector)
                    print(f"   ✅ Email alanı bulundu: {selector}")
                    email_found = True
                    break
                except:
                    continue
            
            if not email_found:
                print("   ❌ Email alanı bulunamadı")
            
            # Şifre alanı kontrolü
            password_selectors = ["password", "session_password", "login-password"]
            password_found = False
            for selector in password_selectors:
                try:
                    element = bot.driver.find_element(By.ID, selector)
                    print(f"   ✅ Şifre alanı bulundu: {selector}")
                    password_found = True
                    break
                except:
                    continue
            
            if not password_found:
                print("   ❌ Şifre alanı bulunamadı")
                
        except Exception as e:
            print(f"❌ Login sayfası testi başarısız: {e}")
            return False
        
        # 4. Giriş Testi
        print("\n4️⃣ LinkedIn Giriş Testi:")
        if not bot.login():
            print("❌ Giriş testi başarısız!")
            print("💡 Lütfen .env dosyasındaki bilgileri kontrol edin")
            return False
        
        # 5. Ana Sayfa Kontrolü
        print("\n5️⃣ Ana Sayfa Navigasyon Kontrolü:")
        try:
            current_url = bot.driver.current_url
            print(f"📍 Mevcut URL: {current_url}")
            
            if "feed" in current_url or "home" in current_url:
                print("✅ Ana sayfaya başarıyla yönlendirildi")
            else:
                print("⚠️ Beklenmeyen sayfa")
                
        except Exception as e:
            print(f"❌ Ana sayfa kontrolü başarısız: {e}")
        
        # 6. Arama Testi
        print("\n6️⃣ Arama Fonksiyonu Testi:")
        search_result = bot.search_people("developer")
        if search_result:
            print("✅ Arama testi başarılı!")
            
            # 7. Profil Linklerini Test Et
            print("\n7️⃣ Profil Linkleri Testi:")
            profile_links = bot.get_profile_links(max_results=3)
            if profile_links:
                print(f"✅ {len(profile_links)} profil linki bulundu!")
                for i, link in enumerate(profile_links, 1):
                    print(f"   {i}. {link}")
            else:
                print("❌ Profil linkleri bulunamadı")
        else:
            print("❌ Arama testi başarısız!")
        
        print("\n🎉 Debug testi tamamlandı!")
        print("⏳ 10 saniye bekleyip tarayıcı kapatılacak...")
        time.sleep(10)
        
        return True

if __name__ == "__main__":
    debug_test()
