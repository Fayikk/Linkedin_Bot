#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Bot - Ana Dosya
Web arayüzünü başlatır
"""

import subprocess
import sys
import os

def main():
    """Ana fonksiyon - Web GUI'yi başlat"""
    print("🤖 LinkedIn Bot")
    print("=" * 50)
    print("🌐 Web arayüzü başlatılıyor...")
    print("📱 Tarayıcınızda http://localhost:5000 adresini açın")
    print("=" * 50)
    
    try:
        # Web GUI'yi çalıştır
        subprocess.run([sys.executable, "web_gui.py"])
    except FileNotFoundError:
        print("❌ web_gui.py dosyası bulunamadı!")
        print("💡 Dosyanın mevcut dizinde olduğundan emin olun.")
    except KeyboardInterrupt:
        print("\n👋 LinkedIn Bot kapatılıyor...")
    except Exception as e:
        print(f"❌ Hata: {e}")
        print("💡 Manuel çalıştırın: python web_gui.py")

if __name__ == "__main__":
    main()
