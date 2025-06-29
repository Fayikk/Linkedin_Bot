#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Bot - Sayfalama Testi
URL tabanlı sayfalama mantığını test eder

Bu script:
1. Birden fazla sayfayı test eder
2. Her sayfa için bağlanabilir profil sayısını raporlar
3. Toplam profil toplama kapasitesini test eder
4. Mesaj göndermez, sadece analiz yapar
"""

import time
from linkedin_bot import LinkedInBot

def test_pagination():
    """Sayfalama mantığını test eder"""
    print("🧪 Sayfalama Testi Başlıyor...")
    print("=" * 50)
    
    # Test parametreleri
    keywords = input("🔍 Arama anahtar kelimeleri (varsayılan: 'software engineer'): ").strip()
    if not keywords:
        keywords = "software engineer"
    
    try:
        start_page = int(input("📄 Başlangıç sayfası (varsayılan: 1): ") or "1")
    except ValueError:
        start_page = 1
        
    try:
        page_count = int(input("📊 Kaç sayfa test edilsin? (varsayılan: 3): ") or "3")
    except ValueError:
        page_count = 3
    
    print(f"\n📋 Test Parametreleri:")
    print(f"🔍 Anahtar kelimeler: {keywords}")
    print(f"📄 Başlangıç sayfası: {start_page}")
    print(f"📊 Test edilecek sayfa sayısı: {page_count}")
    
    try:
        with LinkedInBot() as bot:
            print("\n🔧 WebDriver başlatılıyor...")
            if not bot.setup_driver():
                print("❌ WebDriver başlatılamadı!")
                return
            
            print("🔑 LinkedIn'e giriş yapılıyor...")
            if not bot.login():
                print("❌ LinkedIn giriş başarısız!")
                return
            
            print(f"\n🌐 Sayfalama testi başlıyor...")
            print("-" * 50)
            
            total_profiles = 0
            page_results = []
            
            for page_num in range(start_page, start_page + page_count):
                print(f"\n📄 Sayfa {page_num} test ediliyor...")
                print("-" * 30)
                
                # URL ile sayfaya git
                if bot.search_people(keywords, page_num):
                    print(f"✅ Sayfa {page_num} yüklendi")
                    
                    # Mevcut URL'yi göster
                    current_url = bot.driver.current_url
                    print(f"📍 URL: {current_url}")
                    
                    # Biraz bekle
                    time.sleep(3)
                    
                    # Bu sayfadaki bağlanabilir profilleri bul
                    connectable_profiles = bot.find_connectable_profiles()
                    profile_count = len(connectable_profiles)
                    total_profiles += profile_count
                    
                    page_results.append({
                        'page': page_num,
                        'profile_count': profile_count,
                        'url': current_url
                    })
                    
                    print(f"🎯 Sayfa {page_num}: {profile_count} bağlanabilir profil")
                    
                    # İlk birkaç profili göster
                    if connectable_profiles:
                        print("   İlk profiller:")
                        for i, profile in enumerate(connectable_profiles[:3], 1):
                            name = profile.get('name', 'Unknown')
                            print(f"   {i}. {name}")
                    
                    # Sayfa geçişi için kısa bekleme
                    if page_num < start_page + page_count - 1:
                        print("⏳ Sonraki sayfaya geçiliyor...")
                        time.sleep(2)
                else:
                    print(f"❌ Sayfa {page_num} yüklenemedi!")
                    page_results.append({
                        'page': page_num,
                        'profile_count': 0,
                        'url': 'Failed to load'
                    })
            
            # Sonuçları özetle
            print(f"\n📊 Sayfalama Testi Sonuçları:")
            print("=" * 50)
            print(f"🔍 Arama: {keywords}")
            print(f"📄 Test edilen sayfalar: {start_page} - {start_page + page_count - 1}")
            print(f"👥 Toplam bağlanabilir profil: {total_profiles}")
            print(f"📈 Sayfa başına ortalama: {total_profiles/page_count:.1f}")
            print()
            
            print("📋 Sayfa detayları:")
            for result in page_results:
                page = result['page']
                count = result['profile_count']
                status = "✅" if count > 0 else "❌"
                print(f"  {status} Sayfa {page}: {count} profil")
            
            # En iyi sayfayı bul
            if page_results:
                best_page = max(page_results, key=lambda x: x['profile_count'])
                worst_page = min(page_results, key=lambda x: x['profile_count'])
                
                print(f"\n🏆 En çok profil: Sayfa {best_page['page']} ({best_page['profile_count']} profil)")
                print(f"📉 En az profil: Sayfa {worst_page['page']} ({worst_page['profile_count']} profil)")
            
            # Öneriler
            print(f"\n💡 Öneriler:")
            if total_profiles > 0:
                print(f"✅ Sayfalama sistemi çalışıyor")
                print(f"🎯 {keywords} araması için {start_page}-{start_page+page_count-1} sayfaları uygun")
                if total_profiles < page_count * 5:  # Sayfa başına 5'ten az profil varsa
                    print("⚠️ Düşük profil sayısı - arama terimlerini değiştirmeyi deneyin")
            else:
                print("❌ Hiç bağlanabilir profil bulunamadı")
                print("💡 Arama terimlerini değiştirin veya farklı sayfalar deneyin")
            
            # Manual kontrol için bekle
            print(f"\n🔍 Manual kontrol için tarayıcı açık bırakılıyor...")
            input("✅ İncelemeyi bitirdiğinizde Enter'a basın...")
    
    except KeyboardInterrupt:
        print("\n⏹️ Kullanıcı tarafından durduruldu")
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_pagination()
