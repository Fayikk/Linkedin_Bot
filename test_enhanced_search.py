#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LinkedIn Bot - Gelişmiş Arama Testi
HTML örneklerinden alınan yeni selektörlerle arama ve sayfalama test edilir.
"""

import time
from linkedin_bot import LinkedInBot

def test_enhanced_search():
    """Gelişmiş arama ve sayfalama fonksiyonlarını test eder"""
    
    bot = LinkedInBot()
    
    try:
        print("🚀 LinkedIn Bot başlatılıyor...")
        
        # WebDriver'ı başlat
        if not bot.setup_driver():
            print("❌ WebDriver başlatılamadı")
            return False
        
        print("🔐 LinkedIn'e giriş yapılıyor...")
        if not bot.login():
            print("❌ Giriş başarısız")
            return False
        
        # Arama parametreleri
        search_keywords = "software engineer"
        max_profiles = 15  # 15 profil bulalım (birkaç sayfa gerekebilir)
        
        print(f"\n🔍 '{search_keywords}' araması başlatılıyor...")
        print(f"📊 Hedef profil sayısı: {max_profiles}")
        
        # Arama yap ve kişiler filtresini uygula
        if not bot.search_people(search_keywords):
            print("❌ Arama başarısız")
            return False
        
        # 5 saniye bekle - arama sonuçlarının tam yüklenmesi için
        print("⏳ Arama sonuçları yükleniyor...")
        time.sleep(5)
        
        # Profil linklerini topla (sayfalama ile)
        print(f"\n📋 Profil linkleri toplanıyor...")
        profile_links = bot.get_profile_links(max_results=max_profiles)
        
        if not profile_links:
            print("❌ Hiç profil linki bulunamadı")
            return False
        
        print(f"\n✅ Toplam {len(profile_links)} profil bulundu!")
        print("\n📋 Bulunan profiller:")
        
        # İlk 10 profili listele
        for i, link in enumerate(profile_links[:10], 1):
            print(f"   {i:2d}. {link}")
        
        if len(profile_links) > 10:
            print(f"   ... ve {len(profile_links)-10} profil daha")
        
        # Her bir sayfada ortalama kaç profil bulunduğunu hesapla
        avg_profiles_per_page = len(profile_links) / max(1, (len(profile_links) // 10 + 1))
        print(f"\n📊 İstatistikler:")
        print(f"   • Toplam profil: {len(profile_links)}")
        print(f"   • Sayfa başına ortalama: {avg_profiles_per_page:.1f} profil")
        
        # Test profili için mesaj göndermeyi dene (sadece 1 tane)
        if profile_links:
            test_profile = profile_links[0]
            print(f"\n📩 Test mesajı gönderiliyor: {test_profile}")
            
            success = bot.send_connection_request(
                test_profile, 
                "Merhaba! Python geliştirme konusunda deneyim paylaşımı yapmak isterim. 🐍"
            )
            
            if success:
                print("✅ Test mesajı başarıyla gönderildi!")
            else:
                print("⚠️ Test mesajı gönderilemedi (normal - zaten bağlı olabilir)")
        
        print(f"\n🎉 Test tamamlandı!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        return False
        
    finally:
        # WebDriver'ı kapat
        if bot.driver:
            print("🔚 Tarayıcı kapatılıyor...")
            bot.driver.quit()

def main():
    """Ana test fonksiyonu"""
    print("=" * 50)
    print("LinkedIn Bot - Gelişmiş Arama Testi")
    print("=" * 50)
    
    success = test_enhanced_search()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Test başarıyla tamamlandı!")
    else:
        print("❌ Test başarısız!")
    print("=" * 50)

if __name__ == "__main__":
    main()
