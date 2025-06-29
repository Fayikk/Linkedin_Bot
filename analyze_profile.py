#!/usr/bin/env python3
"""
LinkedIn Bot - Manuel Profil Analizi
Bu script bir profil sayfasını açar ve butonları analiz eder.
"""

import os
import sys
import time
from dotenv import load_dotenv
from linkedin_bot import LinkedInBot

def analyze_profile_page():
    """Bir profil sayfasını analiz et"""
    print("🔍 LinkedIn Profil Analiz Aracı")
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
        
        # 3. Kullanıcıdan profil URL'si al
        profile_url = input("🔗 Analiz edilecek profil URL'sini girin: ").strip()
        if not profile_url:
            print("❌ Geçersiz URL")
            return
        
        # 4. Profile git
        print(f"📍 Profile gidiliyor: {profile_url}")
        bot.driver.get(profile_url)
        time.sleep(5)
        
        # 5. Sayfadaki tüm butonları analiz et
        print("🔍 Sayfa analizi...")
        print("-" * 30)
        
        # Tüm butonları bul
        buttons = bot.driver.find_elements("tag name", "button")
        
        print(f"📊 Toplam {len(buttons)} buton bulundu")
        print("\n🎯 Buton Analizi:")
        
        connection_related = []
        
        for i, btn in enumerate(buttons):
            try:
                btn_text = btn.text.strip()
                btn_aria_label = btn.get_attribute('aria-label') or ''
                btn_class = btn.get_attribute('class') or ''
                
                # Boş butonları atla
                if not btn_text and not btn_aria_label:
                    continue
                
                print(f"\n   🔹 Buton #{i+1}:")
                print(f"      Text: '{btn_text}'")
                print(f"      Aria-label: '{btn_aria_label}'")
                print(f"      Class: '{btn_class[:60]}...' " if len(btn_class) > 60 else f"      Class: '{btn_class}'")
                
                # Bağlantı ile ilgili butonları tespit et
                connection_keywords = ['bağlantı', 'bağlan', 'connect', 'follow', 'takip']
                text_lower = btn_text.lower()
                aria_lower = btn_aria_label.lower()
                
                if any(keyword in text_lower or keyword in aria_lower for keyword in connection_keywords):
                    connection_related.append({
                        'index': i+1,
                        'text': btn_text,
                        'aria_label': btn_aria_label,
                        'element': btn
                    })
                
            except Exception as e:
                print(f"      ❌ Buton analiz hatası: {e}")
        
        # Bağlantı ile ilgili butonları özetle
        print(f"\n🎯 Bağlantı İle İlgili Butonlar ({len(connection_related)} adet):")
        print("-" * 40)
        
        for btn_info in connection_related:
            print(f"   #{btn_info['index']} - Text: '{btn_info['text']}', Aria: '{btn_info['aria_label']}'")
        
        # Manuel test seçeneği
        if connection_related:
            print(f"\n🤖 Bu butonlardan birini test etmek ister misiniz?")
            choice = input("Buton numarasını girin (boş bırakırsanız çıkış): ").strip()
            
            if choice.isdigit():
                choice_num = int(choice)
                selected_btn = None
                
                for btn_info in connection_related:
                    if btn_info['index'] == choice_num:
                        selected_btn = btn_info['element']
                        break
                
                if selected_btn:
                    confirm = input(f"'{btn_info['text']}' butonuna tıklamak istediğinizden emin misiniz? (y/N): ")
                    if confirm.lower() == 'y':
                        print("🖱️ Butona tıklanıyor...")
                        selected_btn.click()
                        time.sleep(3)
                        print("✅ Tıklama tamamlandı")
        
        print("\n⏳ 10 saniye bekleyip tarayıcı kapatılacak...")
        time.sleep(10)
        
    except Exception as e:
        print(f"❌ Analiz hatası: {e}")
    finally:
        # Bot'u kapat
        bot.close()
        print("🔚 Analiz tamamlandı")

if __name__ == "__main__":
    analyze_profile_page()
