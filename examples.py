"""
LinkedIn Bot - Basit örnek kullanım
Bu dosya bot'un nasıl kullanılacağını gösterir
"""

from linkedin_bot import LinkedInBot
import time

def example_usage():
    """Örnek kullanım senaryoları"""
    
    print("🤖 LinkedIn Bot - Örnek Kullanım")
    print("="*40)
    
    # Bot'u context manager ile kullan (önerilen)
    with LinkedInBot() as bot:
        
        # 1. Driver'ı başlat
        if not bot.setup_driver():
            print("❌ WebDriver başlatılamadı!")
            return
        
        print("✅ WebDriver başlatıldı")
        
        # 2. LinkedIn'e giriş yap
        if not bot.login():
            print("❌ Giriş başarısız!")
            return
        
        print("✅ LinkedIn'e giriş yapıldı")
        
        # 3. Kampanya çalıştır - Senaryo 1: Yazılım Mühendisleri
        print("\n📋 Senaryo 1: Yazılım Mühendisleri")
        bot.run_campaign(
            search_keywords="yazılım mühendisi",
            custom_message="Merhaba! Yazılım geliştirme alanında çalışıyorum ve networkinizi genişletmek istiyorum.",
            max_requests=3
        )
        
        time.sleep(5)  # Kampanyalar arası bekleme
        
        # 4. Kampanya çalıştır - Senaryo 2: Frontend Developerlar
        print("\n📋 Senaryo 2: Frontend Developerlar")
        bot.run_campaign(
            search_keywords="frontend developer",
            custom_message="Merhaba! Frontend geliştirme deneyimlerinizi öğrenmek istiyorum.",
            max_requests=2
        )
        
        # 5. Rapor kaydet
        bot.save_report()
        print("✅ Tüm işlemler tamamlandı!")

def quick_test():
    """Hızlı test için tek mesaj gönder"""
    
    print("🧪 Hızlı Test Modu")
    print("="*30)
    
    with LinkedInBot() as bot:
        if bot.setup_driver() and bot.login():
            
            # Sadece 1 kişiye test mesajı gönder
            bot.run_campaign(
                search_keywords="software engineer",
                custom_message="Bu bir test mesajıdır. Merhaba!",
                max_requests=1
            )
            
            bot.save_report()

def custom_search_example():
    """Özel arama örnekleri"""
    
    print("🔍 Özel Arama Örnekleri")
    print("="*35)
    
    search_examples = [
        ("Python developer", "Python ile çalışan geliştiriciler"),
        ("React developer", "React uzmanları"),
        ("DevOps engineer", "DevOps mühendisleri"),
        ("Data scientist", "Veri bilimciler"),
        ("Machine learning engineer", "ML mühendisleri")
    ]
    
    with LinkedInBot() as bot:
        if bot.setup_driver() and bot.login():
            
            for keywords, description in search_examples:
                print(f"\n🎯 Aranıyor: {description}")
                
                # Her kategori için 1 kişiye mesaj gönder
                bot.run_campaign(
                    search_keywords=keywords,
                    custom_message=f"Merhaba! {description} alanında çalışıyorum ve deneyimlerinizi öğrenmek istiyorum.",
                    max_requests=1
                )
                
                time.sleep(10)  # Kategoriler arası bekleme
            
            bot.save_report()

if __name__ == "__main__":
    
    print("LinkedIn Bot Örnekleri")
    print("="*50)
    print("1. Tam örnek kullanım")
    print("2. Hızlı test")
    print("3. Özel arama örnekleri")
    print("="*50)
    
    choice = input("Seçiminizi yapın (1-3): ").strip()
    
    try:
        if choice == "1":
            example_usage()
        elif choice == "2":
            quick_test()
        elif choice == "3":
            custom_search_example()
        else:
            print("❌ Geçersiz seçim!")
            
    except KeyboardInterrupt:
        print("\n👋 Program sonlandırıldı!")
    except Exception as e:
        print(f"❌ Hata: {e}")
