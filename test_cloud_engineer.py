#!/usr/bin/env python3
"""
LinkedIn Bot - Cloud Engineer Test
Cloud engineer araması ve sayfalama testi.
"""

from linkedin_bot import LinkedInBot

def main():
    print("☁️ LinkedIn Bot - Cloud Engineer Test")
    print("=" * 50)
    
    with LinkedInBot() as bot:
        if bot.setup_driver():
            if bot.login():
                # Cloud engineer araması yap
                print("🔍 Cloud engineer araması yapılıyor...")
                if bot.search_people("cloud engineer"):
                    
                    # 10 profil almaya çalış (sayfalama testi için)
                    profiles = bot.get_profile_links(max_results=10)
                    
                    if profiles:
                        print(f"✅ {len(profiles)} cloud engineer profili bulundu!")
                        
                        # İlk profile test mesajı gönder
                        user_input = input(f"İlk profile ({profiles[0]}) Udemy kurs mesajı göndermek ister misiniz? (y/N): ")
                        if user_input.lower() == 'y':
                            success = bot.send_connection_request(profiles[0])
                            if success:
                                print("✅ Udemy kurs mesajı başarıyla gönderildi!")
                            else:
                                print("❌ Mesaj gönderilemedi")
                    else:
                        print("❌ Hiç profil bulunamadı")
                else:
                    print("❌ Arama başarısız")
            else:
                print("❌ LinkedIn'e giriş yapılamadı")
        else:
            print("❌ WebDriver başlatılamadı")

if __name__ == "__main__":
    main()
