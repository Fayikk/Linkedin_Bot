#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Bot - Ana Çalıştırma Dosyası
URL tabanlı sayfalama ile gelişmiş LinkedIn otomasyonu

Özellikler:
- Direkt LinkedIn arama URL'siyle sayfa sayfa arama
- Her sayfada "Bağlantı kur" butonlu kullanıcıları tespit
- Özel mesajla bağlantı istekleri gönderme
- Ayrıntılı raporlama ve hata yönetimi
"""

import sys
import os
from linkedin_bot import LinkedInBot

def display_menu():
    """Ana menüyü gösterir"""
    print("\n" + "="*60)
    print("🤖 LinkedIn Bot - URL Tabanlı Gelişmiş Versiyon")
    print("="*60)
    print("1. 🚀 Normal kampanya (URL tabanlı sayfalama)")
    print("2. 📄 Belirli sayfadan başlayarak kampanya")
    print("3. 🧪 Test modu (1 kişiye mesaj)")
    print("4. 📋 Konfigürasyon ayarlarını görüntüle") 
    print("5. 🔧 Debug modu (sayfa analizi)")
    print("6. 📊 Sadece profil toplama (mesaj göndermez)")
    print("7. 🚪 Çıkış")
    print("="*60)

def show_config():
    """Mevcut konfigürasyonu gösterir"""
    from dotenv import load_dotenv
    load_dotenv()
    
    print("\n📋 Mevcut Konfigürasyon:")
    print(f"📧 Email: {os.getenv('LINKEDIN_EMAIL', 'Ayarlanmamış')}")
    print(f"💬 Varsayılan Mesaj: {os.getenv('DEFAULT_MESSAGE', 'Ayarlanmamış')[:50]}...")
    print(f"🔍 Arama Anahtar Kelimeleri: {os.getenv('SEARCH_KEYWORDS', 'Ayarlanmamış')}")
    print(f"👥 Maksimum Profil: {os.getenv('MAX_PROFILES_PER_SESSION', 'Ayarlanmamış')}")
    print(f"⏱️ Mesajlar Arası Bekleme: {os.getenv('DELAY_BETWEEN_MESSAGES', 'Ayarlanmamış')} saniye")

def get_user_input():
    """Kullanıcıdan girdi alır"""
    print("\n📝 Kampanya Bilgileri:")
    
    keywords = input("🔍 Arama anahtar kelimeleri (örn: software engineer, cloud engineer): ").strip()
    if not keywords:
        keywords = "software engineer"
    
    try:
        max_requests = int(input("👥 Kaç kişiye mesaj göndermek istiyorsunuz? (1-1000): "))
        if max_requests < 1 or max_requests > 1000:
            max_requests = 10
    except ValueError:
        max_requests = 10
    
    try:
        start_page = int(input("📄 Hangi sayfadan başlamak istiyorsunuz? (varsayılan: 1): ") or "1")
    except ValueError:
        start_page = 1
    
    custom_message = input("💬 Özel mesaj (boş bırakırsanız varsayılan kullanılır): ").strip()
    if not custom_message:
        custom_message = None
    
    return keywords, max_requests, start_page, custom_message

def run_campaign():
    """Normal kampanya çalıştırır"""
    keywords, max_requests, start_page, custom_message = get_user_input()
    
    print(f"\n🚀 Kampanya başlatılıyor...")
    print(f"🔍 Arama: {keywords}")
    print(f"📊 Hedef: {max_requests} kişi")
    print(f"📄 Başlangıç sayfası: {start_page}")
    print(f"💬 Mesaj: {'Özel mesaj' if custom_message else 'Varsayılan mesaj'}")
    
    confirm = input("\nDevam etmek istiyor musunuz? (e/h): ").lower()
    if confirm != 'e':
        print("❌ Kampanya iptal edildi")
        return
    
    with LinkedInBot() as bot:
        if bot.setup_driver():
            if bot.login():
                success = bot.run_campaign(keywords, custom_message, max_requests, start_page)
                if success:
                    bot.save_report()
                    print("✅ Kampanya başarıyla tamamlandı!")
                else:
                    print("❌ Kampanya başarısız!")
            else:
                print("❌ Giriş başarısız! .env dosyasındaki bilgileri kontrol edin.")
        else:
            print("❌ WebDriver başlatılamadı!")

def run_specific_page_campaign():
    """Belirli sayfadan başlayarak kampanya"""
    print("\n📄 Belirli Sayfadan Başlayarak Kampanya")
    
    keywords = input("🔍 Arama anahtar kelimeleri: ").strip()
    if not keywords:
        keywords = "software engineer"
        
    try:
        start_page = int(input("📄 Başlangıç sayfası (örn: 3): "))
    except ValueError:
        start_page = 1
        
    try:
        max_requests = int(input("👥 Hedef kişi sayısı: "))
    except ValueError:
        max_requests = 5
    
    custom_message = input("💬 Özel mesaj: ").strip()
    if not custom_message:
        custom_message = None
    
    print(f"\n📊 Sayfa {start_page}'den başlayarak {max_requests} kişiye mesaj gönderilecek")
    confirm = input("Devam edilsin mi? (e/h): ").lower()
    if confirm != 'e':
        return
    
    with LinkedInBot() as bot:
        if bot.setup_driver():
            if bot.login():
                bot.run_campaign(keywords, custom_message, max_requests, start_page)
                bot.save_report()

def run_test_mode():
    """Test modu - sadece 1 kişiye mesaj"""
    print("\n🧪 Test Modu - Sadece 1 kişiye mesaj gönderilecek")
    
    keywords = input("🔍 Arama anahtar kelimeleri: ").strip()
    if not keywords:
        keywords = "software engineer"
    
    custom_message = input("💬 Test mesajı: ").strip()
    if not custom_message:
        custom_message = "Bu bir test mesajıdır."
    
    with LinkedInBot() as bot:
        if bot.setup_driver():
            if bot.login():
                bot.run_campaign(keywords, custom_message, 1, 1)
                bot.save_report()

def run_debug_mode():
    """Debug modu - sayfa analizi"""
    print("\n🔧 Debug Modu - Sayfa Analizi")
    
    keywords = input("🔍 Arama anahtar kelimeleri: ").strip()
    if not keywords:
        keywords = "software engineer"
    
    try:
        page = int(input("📄 Hangi sayfayı analiz etmek istiyorsunuz? (varsayılan: 1): ") or "1")
    except ValueError:
        page = 1
    
    with LinkedInBot() as bot:
        if bot.setup_driver():
            if bot.login():
                if bot.search_people(keywords, page):
                    connectable_profiles = bot.find_connectable_profiles()
                    print(f"\n📊 Sayfa {page} Analiz Sonucu:")
                    print(f"🎯 Toplam {len(connectable_profiles)} bağlanabilir profil bulundu")
                    
                    for i, profile in enumerate(connectable_profiles[:10], 1):
                        print(f"  {i}. {profile.get('name')} - {profile.get('url')}")
                    
                    if len(connectable_profiles) > 10:
                        print(f"  ... ve {len(connectable_profiles)-10} profil daha")

def run_profile_collection():
    """Sadece profil toplama - mesaj göndermez"""
    print("\n📊 Profil Toplama Modu - Mesaj Gönderilmez")
    
    keywords = input("🔍 Arama anahtar kelimeleri: ").strip()
    if not keywords:
        keywords = "software engineer"
    
    try:
        max_profiles = int(input("👥 Kaç profil toplamak istiyorsunuz? (1-1000): "))
    except ValueError:
        max_profiles = 20
        
    try:
        start_page = int(input("📄 Başlangıç sayfası (varsayılan: 1): ") or "1")
    except ValueError:
        start_page = 1
    
    with LinkedInBot() as bot:
        if bot.setup_driver():
            if bot.login():
                print(f"\n📋 {keywords} için profil toplama başlıyor...")
                profiles = bot.get_profile_links(keywords, max_profiles, start_page)
                
                if profiles:
                    print(f"\n✅ Toplam {len(profiles)} profil toplandı:")
                    for i, profile in enumerate(profiles, 1):
                        print(f"  {i}. {profile.get('name')} - {profile.get('url')}")
                else:
                    print("❌ Hiç profil bulunamadı")

def main():
    """Ana fonksiyon"""
    print("🤖 LinkedIn Bot'a Hoş Geldiniz!")
    print("📈 URL Tabanlı Gelişmiş Versiyon")
    
    # .env dosyası kontrolü
    if not os.path.exists('.env'):
        print("⚠️ .env dosyası bulunamadı!")
        print("Lütfen .env dosyasını düzenleyip LinkedIn bilgilerinizi girin.")
        return
    
    while True:
        display_menu()
        
        try:
            choice = input("\nSeçiminizi yapın (1-7): ").strip()
            
            if choice == '1':
                run_campaign()
            elif choice == '2':
                run_specific_page_campaign()
            elif choice == '3':
                run_test_mode()
            elif choice == '4':
                show_config()
            elif choice == '5':
                run_debug_mode()
            elif choice == '6':
                run_profile_collection()
            elif choice == '7':
                print("👋 Görüşmek üzere!")
                break
            else:
                print("❌ Geçersiz seçim! Lütfen 1-7 arası bir sayı girin.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Program sonlandırıldı!")
            break
        except Exception as e:
            print(f"❌ Hata oluştu: {e}")

if __name__ == "__main__":
    main()
