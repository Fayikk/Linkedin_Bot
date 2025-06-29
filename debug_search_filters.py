#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LinkedIn Bot - Hızlı Debug Testi
Sadece arama ve filtreleme işlemlerini test eder (mesaj göndermez).
"""

import time
from linkedin_bot import LinkedInBot

def debug_search_only():
    """Sadece arama ve filtreleme işlemlerini debug eder"""
    
    bot = LinkedInBot()
    
    try:
        print("🚀 LinkedIn Bot debug başlatılıyor...")
        
        # WebDriver'ı başlat
        if not bot.setup_driver():
            print("❌ WebDriver başlatılamadı")
            return False
        
        print("🔐 LinkedIn'e giriş yapılıyor...")
        if not bot.login():
            print("❌ Giriş başarısız")
            return False
        
        # Farklı arama terimleri ile test
        search_terms = [
            "cloud engineer",
            "python developer", 
            "data scientist"
        ]
        
        for term in search_terms:
            print(f"\n{'='*30}")
            print(f"🔍 '{term}' araması test ediliyor...")
            print(f"{'='*30}")
            
            # Arama yap
            if bot.search_people(term):
                print(f"✅ '{term}' araması başarılı!")
                
                # 3 saniye bekle
                time.sleep(3)
                
                # Sayfa yapısını analiz et
                print("📋 Sayfa yapısı analiz ediliyor...")
                
                # Kişiler filtresi durumunu kontrol et
                try:
                    people_filters = bot.driver.find_elements(
                        "xpath", 
                        "//button[contains(text(), 'Kişiler') or contains(text(), 'People')]"
                    )
                    print(f"🔍 Bulunan 'Kişiler' filtreleri: {len(people_filters)}")
                    
                    for i, btn in enumerate(people_filters[:3], 1):
                        try:
                            text = btn.text.strip()
                            classes = btn.get_attribute('class')
                            aria_label = btn.get_attribute('aria-label')
                            print(f"   {i}. Text: '{text}' | Classes: '{classes}' | Aria: '{aria_label}'")
                        except:
                            pass
                            
                except Exception as e:
                    print(f"⚠️ Kişiler filtresi analizi hatası: {e}")
                
                # Profil linklerini kontrol et (sadece sayı)
                try:
                    profile_links = bot.driver.find_elements(
                        "xpath", 
                        "//a[contains(@href, '/in/')]"
                    )
                    print(f"👥 Bulunan profil linkleri: {len(profile_links)}")
                    
                    # İlk 3 profile ait bilgileri göster
                    for i, link in enumerate(profile_links[:3], 1):
                        try:
                            href = link.get_attribute('href')
                            text = link.text.strip()[:50] + "..." if len(link.text.strip()) > 50 else link.text.strip()
                            print(f"   {i}. {text} -> {href}")
                        except:
                            pass
                            
                except Exception as e:
                    print(f"⚠️ Profil linkleri analizi hatası: {e}")
                
                # Sayfalama butonlarını kontrol et
                try:
                    pagination_buttons = bot.driver.find_elements(
                        "xpath", 
                        "//button[contains(@aria-label, 'Sayfa') or contains(@aria-label, 'Page')]"
                    )
                    print(f"📄 Bulunan sayfalama butonları: {len(pagination_buttons)}")
                    
                    for i, btn in enumerate(pagination_buttons[:5], 1):
                        try:
                            aria_label = btn.get_attribute('aria-label')
                            text = btn.text.strip()
                            print(f"   {i}. Aria: '{aria_label}' | Text: '{text}'")
                        except:
                            pass
                            
                except Exception as e:
                    print(f"⚠️ Sayfalama analizi hatası: {e}")
                    
            else:
                print(f"❌ '{term}' araması başarısız!")
            
            # Sonraki arama için bekleme
            time.sleep(2)
        
        print(f"\n🎉 Debug testi tamamlandı!")
        return True
        
    except Exception as e:
        print(f"❌ Debug testi hatası: {e}")
        return False
        
    finally:
        # WebDriver'ı kapat
        if bot.driver:
            print("🔚 Tarayıcı kapatılıyor...")
            time.sleep(3)  # Kapatmadan önce biraz bekle
            bot.driver.quit()

def main():
    """Ana debug fonksiyonu"""
    print("=" * 60)
    print("LinkedIn Bot - Hızlı Debug Testi")
    print("Sadece arama ve filtreleme test edilir")
    print("=" * 60)
    
    success = debug_search_only()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Debug testi başarıyla tamamlandı!")
    else:
        print("❌ Debug testi başarısız!")
    print("=" * 60)

if __name__ == "__main__":
    main()
