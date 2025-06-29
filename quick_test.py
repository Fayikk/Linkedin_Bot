#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hızlı Test - URL Tabanlı Arama ve Profil Tespiti
"""

from linkedin_bot import LinkedInBot
import time

def quick_test():
    """Hızlı test"""
    print("🚀 Hızlı URL Testi Başlıyor...")
    
    with LinkedInBot() as bot:
        if not bot.setup_driver():
            return
        
        if not bot.login():
            return
        
        # Test 1: Basit kampanya (1 kişi)
        print("\n📋 Test 1: 1 kişiye mesaj gönderme testi")
        
        try:
            success = bot.run_campaign(
                search_keywords="software engineer",
                custom_message="Test mesajı - LinkedIn Bot URL tabanlı test",
                max_requests=1,
                start_page=1
            )
            
            if success:
                print("✅ Test başarılı! Mesaj gönderildi.")
                bot.save_report()
            else:
                print("❌ Test başarısız")
                
        except Exception as e:
            print(f"❌ Test hatası: {e}")
        
        # Manuel kontrol için bekle
        print("\n🔍 Manuel kontrol için 30 saniye bekle...")
        print("Tarayıcıda LinkedIn sayfasını inceleyebilirsiniz")
        time.sleep(30)

if __name__ == "__main__":
    quick_test()
