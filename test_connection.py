#!/usr/bin/env python3
"""
LinkedIn Bot - Bağlantı Kurma Testi
Bu script sadece bağlantı kurma fonksiyonunu test eder.
"""

import os
import sys
import time
from dotenv import load_dotenv
from linkedin_bot import LinkedInBot

def test_connection():
    """Bağlantı kurma fonksiyonunu test et"""
    print("🔗 LinkedIn Bot - Bağlantı Kurma Testi")
    print("=" * 50)
    
    # .env dosyasını yükle
    load_dotenv()
    
    # Bot oluştur
    bot = LinkedInBot()
    
    try:
        # 1. WebDriver başlat
        print("1️⃣ WebDriver başlatılıyor...")
        if not bot.setup_driver():
            print("❌ WebDriver başlatılamadı")
            return
        
        # 2. LinkedIn'e giriş yap
        print("2️⃣ LinkedIn'e giriş yapılıyor...")
        if not bot.login():
            print("❌ Giriş başarısız")
            return
        
        # 3. Arama yap
        print("3️⃣ Kişi araması yapılıyor...")
        bot.search_people("software developer")
        
        # 4. Profil linkleri al
        print("4️⃣ Profil linkleri alınıyor...")
        profiles = bot.get_profile_links(max_results=2)
        
        if not profiles:
            print("❌ Hiç profil bulunamadı")
            return
        
        # 5. İlk profile bağlantı isteği gönder (TEST)
        print("5️⃣ Bağlantı kurma fonksiyonu test ediliyor...")
        test_profile = profiles[0]
        print(f"📋 Test profili: {test_profile}")
        
        # Kullanıcıdan onay al
        user_input = input("Bu profile gerçekten bağlantı isteği göndermek istiyor musunuz? (y/N): ")
        if user_input.lower() != 'y':
            print("❌ Test iptal edildi")
            return
        
        # Bağlantı isteği gönder
        success = bot.send_connection_request(test_profile)
        
        if success:
            print("✅ Bağlantı isteği başarıyla gönderildi!")
        else:
            print("❌ Bağlantı isteği gönderilemedi")
        
        print("⏳ 5 saniye bekleyip tarayıcı kapatılacak...")
        time.sleep(5)
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
    finally:
        # Bot'u kapat
        bot.close()
        print("🔚 Test tamamlandı")

if __name__ == "__main__":
    test_connection()
