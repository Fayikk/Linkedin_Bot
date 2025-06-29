#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Bot Launcher
Farklı arayüz seçenekleri ile bot başlatıcı
"""

import os
import sys
import subprocess

def show_menu():
    """Ana menüyü göster"""
    print("\n" + "="*60)
    print("🤖 LinkedIn Bot - Arayüz Seçici")
    print("="*60)
    print("1. 🖥️  Konsol Arayüzü (Terminal tabanlı)")
    print("2. 🖼️  Desktop GUI (Tkinter)")
    print("3. 🌐 Web GUI (Flask - Tarayıcı tabanlı)")
    print("4. ⚡ Hızlı Test (1 kişi)")
    print("5. 🧪 Kapsamlı Test (3 kişi)")
    print("6. 🚪 Çıkış")
    print("="*60)

def run_console():
    """Konsol arayüzünü çalıştır"""
    print("🖥️ Konsol arayüzü başlatılıyor...")
    os.system("python main.py")

def run_desktop_gui():
    """Desktop GUI'yi çalıştır"""
    try:
        print("🖼️ Desktop GUI başlatılıyor...")
        import tkinter
        subprocess.run([sys.executable, "gui_app.py"])
    except ImportError:
        print("❌ Tkinter bulunamadı! Windows'ta varsayılan olarak yüklü olmalı.")
        input("Enter'a basın...")

def run_web_gui():
    """Web GUI'yi çalıştır"""
    try:
        print("🌐 Web GUI başlatılıyor...")
        print("📱 Tarayıcınızda http://localhost:5000 adresini açın")
        subprocess.run([sys.executable, "web_gui.py"])
    except Exception as e:
        print(f"❌ Web GUI başlatılamadı: {e}")
        print("💡 Gerekli paketleri yüklemek için: pip install flask flask-socketio")
        input("Enter'a basın...")

def run_quick_test():
    """Hızlı test çalıştır"""
    print("⚡ Hızlı test başlatılıyor (1 kişiye mesaj)...")
    os.system("python quick_test.py")

def run_comprehensive_test():
    """Kapsamlı test çalıştır"""
    print("🧪 Kapsamlı test başlatılıyor (3 kişiye mesaj)...")
    os.system("python comprehensive_test.py")

def main():
    """Ana fonksiyon"""
    while True:
        show_menu()
        
        try:
            choice = input("\n🎯 Seçiminizi yapın (1-6): ").strip()
            
            if choice == "1":
                run_console()
            elif choice == "2":
                run_desktop_gui()
            elif choice == "3":
                run_web_gui()
            elif choice == "4":
                run_quick_test()
            elif choice == "5":
                run_comprehensive_test()
            elif choice == "6":
                print("👋 LinkedIn Bot kapatılıyor...")
                break
            else:
                print("❌ Geçersiz seçim! Lütfen 1-6 arasında bir sayı girin.")
                
        except KeyboardInterrupt:
            print("\n👋 LinkedIn Bot kapatılıyor...")
            break
        except Exception as e:
            print(f"❌ Hata: {e}")
            
        input("\nDevam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
