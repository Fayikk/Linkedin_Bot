#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Bot - URL Tabanlı Arama Testi
Yeni URL tabanlı arama ve sayfalama mantığını test eder

Bu script:
1. Direkt LinkedIn arama URL'sine gider
2. Belirli bir sayfadaki sonuçları analiz eder  
3. "Bağlantı kur" butonlu profilleri tespit eder
4. Mesaj göndermez, sadece analiz yapar
"""

import time
from linkedin_bot import LinkedInBot

def test_url_based_search():
    """URL tabanlı arama ve profil tespiti testi"""
    print("🧪 URL Tabanlı Arama Testi Başlıyor...")
    print("=" * 50)
    
    # Test parametreleri
    keywords = input("🔍 Arama anahtar kelimeleri (varsayılan: 'software engineer'): ").strip()
    if not keywords:
        keywords = "software engineer"
    
    try:
        test_page = int(input("📄 Test edilecek sayfa numarası (varsayılan: 1): ") or "1")
    except ValueError:
        test_page = 1
    
    print(f"\n📋 Test Parametreleri:")
    print(f"🔍 Anahtar kelimeler: {keywords}")
    print(f"📄 Test sayfası: {test_page}")
    
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
            
            print(f"\n🌐 URL tabanlı arama testi - Sayfa {test_page}")
            print("-" * 40)
            
            # URL tabanlı arama testi
            if bot.search_people(keywords, test_page):
                print("✅ Sayfa başarıyla yüklendi")
                
                # Mevcut URL'yi göster
                current_url = bot.driver.current_url
                print(f"📍 Mevcut URL: {current_url}")
                
                # Biraz bekle
                time.sleep(3)
                
                # Bağlanabilir profilleri bul
                print(f"\n🔍 Sayfa {test_page}'de bağlanabilir profiller aranıyor...")
                connectable_profiles = bot.find_connectable_profiles()
                
                if connectable_profiles:
                    print(f"\n✅ {len(connectable_profiles)} bağlanabilir profil bulundu:")
                    print("-" * 40)
                    
                    for i, profile in enumerate(connectable_profiles, 1):
                        name = profile.get('name', 'Unknown')
                        url = profile.get('url', 'No URL')
                        card_index = profile.get('card_index', 'Unknown')
                        
                        print(f"{i:2d}. 👤 {name}")
                        print(f"    🔗 {url}")
                        print(f"    📋 Kart indeksi: {card_index}")
                        print()
                        
                        # İlk 3 profil için buton detayını göster
                        if i <= 3:
                            try:
                                button = profile.get('button')
                                if button:
                                    button_text = button.text.strip()
                                    button_aria = button.get_attribute('aria-label') or ''
                                    print(f"    🔘 Buton: '{button_text}' (aria: '{button_aria}')")
                                    print(f"    🎯 Görünür: {button.is_displayed()}, Etkin: {button.is_enabled()}")
                                    print()
                            except Exception as e:
                                print(f"    ⚠️ Buton bilgisi alınamadı: {e}")
                                print()
                else:
                    print("❌ Bu sayfada bağlanabilir profil bulunamadı")
                    
                    # Debug: Sayfadaki tüm butonları listele
                    print("\n🔍 Debug: Sayfadaki mevcut butonlar:")
                    all_buttons = bot.driver.find_elements("tag name", "button")
                    connection_buttons = []
                    
                    for i, btn in enumerate(all_buttons[:30]):  # İlk 30 butonu kontrol et
                        try:
                            btn_text = btn.text.strip()
                            btn_aria = btn.get_attribute('aria-label') or ''
                            
                            # Bağlantı ile ilgili butonları tespit et
                            if any(keyword in btn_text.lower() or keyword in btn_aria.lower() 
                                   for keyword in ['bağlantı', 'bağlan', 'connect']):
                                connection_buttons.append(f"  {len(connection_buttons)+1}. '{btn_text}' (aria: '{btn_aria}')")
                        except:
                            continue
                    
                    if connection_buttons:
                        print("🎯 Bağlantı ile ilgili butonlar:")
                        for btn_info in connection_buttons[:10]:  # İlk 10'unu göster
                            print(btn_info)
                    else:
                        print("❌ Hiç bağlantı butonu bulunamadı")
                
                # Manuel kontrol için kullanıcıya fırsat ver
                print(f"\n🔍 Manual kontrol için tarayıcı açık bırakılıyor...")
                print("📋 Sayfayı inceleyebilir, gerekirse düzeltmeler yapabilirsiniz.")
                input("✅ İncelemeyi bitirdiğinizde Enter'a basın...")
                
            else:
                print("❌ Sayfa yüklenemedi!")
    
    except KeyboardInterrupt:
        print("\n⏹️ Kullanıcı tarafından durduruldu")
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_url_based_search()
