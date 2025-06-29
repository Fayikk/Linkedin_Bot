#!/usr/bin/env python3
"""
LinkedIn Bot - Final Test
Son test için kısa bir kampanya çalıştırır.
"""

from linkedin_bot import LinkedInBot

def main():
    print("🚀 LinkedIn Bot - Final Test")
    print("=" * 50)
    
    with LinkedInBot() as bot:
        if bot.setup_driver():
            if bot.login():
                # Kısa bir test kampanyası çalıştır
                result = bot.run_campaign(
                    search_keywords="software engineer",
                    custom_message="Merhaba! Yazılım geliştirme alanında çalışıyorum ve ağımı genişletmek istiyorum. Bağlantı kurmak ister misiniz?",
                    max_requests=2  # Sadece 2 kişiye gönder
                )
                
                if result:
                    print("🎉 Test kampanyası başarıyla tamamlandı!")
                    bot.save_report()
                else:
                    print("❌ Test kampanyası başarısız")
            else:
                print("❌ LinkedIn'e giriş yapılamadı")
        else:
            print("❌ WebDriver başlatılamadı")

if __name__ == "__main__":
    main()
