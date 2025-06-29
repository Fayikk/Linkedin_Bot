#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kapsamlı Test - 3 Kişiye Bağlantı İsteği Gönderme
"""

from linkedin_bot import LinkedInBot
import time

def comprehensive_test():
    """Kapsamlı test - 3 kişiye mesaj gönderme"""
    print("🚀 Kapsamlı Test Başlıyor...")
    print("📊 3 farklı kişiye bağlantı isteği göndereceğiz")
    
    with LinkedInBot() as bot:
        if not bot.setup_driver():
            return
        
        if not bot.login():
            return
        
        # Test: 3 kişiye mesaj gönderme
        print("\n📋 Test: 3 kişiye mesaj gönderme testi")
        
        try:
            success = bot.run_campaign(
                search_keywords="software developer",
                custom_message="Merhaba! Yazılım geliştirme alanında çalışıyorum ve networkümü genişletmek istiyorum. Bağlantı kurmak ister misiniz?",
                max_requests=3,
                start_page=1
            )
            
            if success:
                print("✅ Test başarılı! 3 mesaj gönderildi.")
                bot.save_report()
                
                # Gönderilen mesajları listele
                print("\n📋 Gönderilen mesajlar:")
                for i, msg in enumerate(bot.sent_messages, 1):
                    print(f"{i}. {msg['profile_url']} - {msg['timestamp']}")
                    
            else:
                print("❌ Test başarısız")
                
        except Exception as e:
            print(f"❌ Test hatası: {e}")
        
        # Manuel kontrol için bekle
        print("\n🔍 Manuel kontrol için 45 saniye bekle...")
        print("Tarayıcıda LinkedIn sayfasını inceleyip gönderilen mesajları kontrol edebilirsiniz")
        print("LinkedIn'de 'Mesajlar' veya 'Network' bölümünden gönderilen istekleri görebilirsiniz")
        time.sleep(45)

if __name__ == "__main__":
    comprehensive_test()
