#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Bot GUI - Tkinter Arayüzü
Basit ve kullanıcı dostu arayüz ile LinkedIn bot operasyonları

Özellikler:
- Kolay konfigürasyon ayarları
- Gerçek zamanlı log görüntüleme
- Kampanya başlatma/durdurma
- Rapor görüntüleme
- Profil bilgilerini görsel olarak takip
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import os
import csv
import sys
from datetime import datetime
import queue
import time
from linkedin_bot import LinkedInBot
from dotenv import load_dotenv, set_key

class LinkedInBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 LinkedIn Bot - Gelişmiş GUI v2.0")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Bot durumu
        self.bot_running = False
        self.bot_thread = None
        self.current_bot = None
        
        # Log queue
        self.log_queue = queue.Queue()
        
        # .env dosyasını yükle
        load_dotenv()
        
        self.create_widgets()
        self.load_config()
        self.update_logs()
        
    def create_widgets(self):
        """Ana widget'ları oluştur"""
        
        # Ana container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Sol panel - Konfigürasyon
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Konfigürasyon", padding="10")
        config_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # LinkedIn bilgileri
        ttk.Label(config_frame, text="📧 LinkedIn Email:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(config_frame, textvariable=self.email_var, width=30)
        self.email_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(config_frame, text="🔐 LinkedIn Şifre:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(config_frame, textvariable=self.password_var, show="*", width=30)
        self.password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Arama ayarları
        ttk.Label(config_frame, text="🔍 Anahtar Kelimeler:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.keywords_var = tk.StringVar()
        self.keywords_entry = ttk.Entry(config_frame, textvariable=self.keywords_var, width=30)
        self.keywords_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(config_frame, text="👥 Maksimum Profil:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.max_profiles_var = tk.StringVar()
        self.max_profiles_spinbox = ttk.Spinbox(config_frame, from_=1, to=1000, textvariable=self.max_profiles_var, width=10)
        self.max_profiles_spinbox.grid(row=3, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(config_frame, text="📄 Başlangıç Sayfası:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.start_page_var = tk.StringVar()
        self.start_page_spinbox = ttk.Spinbox(config_frame, from_=1, to=50, textvariable=self.start_page_var, width=10)
        self.start_page_spinbox.grid(row=4, column=1, sticky=tk.W, pady=2)
        
        # Mesaj ayarları
        ttk.Label(config_frame, text="💬 Mesaj Şablonu:").grid(row=5, column=0, sticky=tk.W, pady=(10, 2))
        self.message_text = scrolledtext.ScrolledText(config_frame, height=6, width=40)
        self.message_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Timing ayarları
        timing_frame = ttk.LabelFrame(config_frame, text="⏱️ Timing Ayarları", padding="5")
        timing_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(timing_frame, text="Mesajlar arası bekleme (saniye):").grid(row=0, column=0, sticky=tk.W)
        self.delay_messages_var = tk.StringVar()
        ttk.Spinbox(timing_frame, from_=1, to=60, textvariable=self.delay_messages_var, width=10).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(timing_frame, text="Sayfa arası bekleme (saniye):").grid(row=1, column=0, sticky=tk.W)
        self.delay_searches_var = tk.StringVar()
        ttk.Spinbox(timing_frame, from_=1, to=30, textvariable=self.delay_searches_var, width=10).grid(row=1, column=1, sticky=tk.W)
        
        # Butonlar
        button_frame = ttk.Frame(config_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=(15, 0))
        
        self.save_config_btn = ttk.Button(button_frame, text="💾 Ayarları Kaydet", command=self.save_config)
        self.save_config_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.start_btn = ttk.Button(button_frame, text="🚀 Kampanya Başlat", command=self.start_campaign)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="⏹️ Durdur", command=self.stop_campaign, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Sağ panel - Logs ve durum
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Durum bilgisi
        status_frame = ttk.LabelFrame(right_panel, text="📊 Durum Bilgisi", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="⚪ Bot durumu: Hazır", font=("Arial", 10, "bold"))
        self.status_label.pack(anchor=tk.W)
        
        self.progress_var = tk.StringVar(value="İşlem: Beklemede")
        self.progress_label = ttk.Label(status_frame, textvariable=self.progress_var)
        self.progress_label.pack(anchor=tk.W, pady=(5, 0))
        
        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # İstatistikler
        stats_frame = ttk.LabelFrame(right_panel, text="📈 İstatistikler", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_text = tk.Text(stats_frame, height=6, width=50, font=("Consolas", 9))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Log alanı
        log_frame = ttk.LabelFrame(right_panel, text="📝 Canlı Loglar", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Alt panel - Raporlar
        report_frame = ttk.LabelFrame(main_frame, text="📋 Raporlar", padding="10")
        report_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(report_frame, text="📂 Rapor Klasörünü Aç", command=self.open_reports_folder).pack(side=tk.LEFT)
        ttk.Button(report_frame, text="📊 Son Raporu Görüntüle", command=self.view_last_report).pack(side=tk.LEFT, padx=(10, 0))
        
        # Grid weight ayarları
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
    def load_config(self):
        """Mevcut konfigürasyonu yükle"""
        # .env dosyasını yeniden yükle
        load_dotenv(override=True)
        
        # Tırnak işaretlerini temizle
        def clean_env_value(value):
            if value:
                return value.strip().strip("'").strip('"')
            return value
        
        self.email_var.set(clean_env_value(os.getenv('LINKEDIN_EMAIL', '')))
        self.password_var.set(clean_env_value(os.getenv('LINKEDIN_PASSWORD', '')))
        self.keywords_var.set(clean_env_value(os.getenv('SEARCH_KEYWORDS', 'software engineer')))
        self.max_profiles_var.set(clean_env_value(os.getenv('MAX_PROFILES_PER_SESSION', '50')))
        self.delay_messages_var.set(clean_env_value(os.getenv('DELAY_BETWEEN_MESSAGES', '10')))
        self.delay_searches_var.set(clean_env_value(os.getenv('DELAY_BETWEEN_SEARCHES', '5')))
        self.start_page_var.set('1')
        
        # Mesaj şablonunu yükle
        message = clean_env_value(os.getenv('DEFAULT_MESSAGE', 'Merhaba! LinkedIn üzerinden bağlantı kurmak istiyorum.'))
        self.message_text.delete(1.0, tk.END)
        self.message_text.insert(1.0, message)
        
        self.log_message("✅ Konfigürasyon yüklendi")
        
        # Debug için değerleri yazdır
        self.log_message(f"📧 Email: {self.email_var.get()}")
        self.log_message(f"🔍 Keywords: {self.keywords_var.get()}")
        
    def save_config(self):
        """Konfigürasyonu .env dosyasına kaydet"""
        try:
            env_file = '.env'
            
            set_key(env_file, 'LINKEDIN_EMAIL', self.email_var.get())
            set_key(env_file, 'LINKEDIN_PASSWORD', self.password_var.get())
            set_key(env_file, 'SEARCH_KEYWORDS', self.keywords_var.get())
            set_key(env_file, 'MAX_PROFILES_PER_SESSION', self.max_profiles_var.get())
            set_key(env_file, 'DELAY_BETWEEN_MESSAGES', self.delay_messages_var.get())
            set_key(env_file, 'DELAY_BETWEEN_SEARCHES', self.delay_searches_var.get())
            set_key(env_file, 'DEFAULT_MESSAGE', self.message_text.get(1.0, tk.END).strip())
            
            messagebox.showinfo("Başarılı", "✅ Konfigürasyon başarıyla kaydedildi!")
            self.log_message("💾 Konfigürasyon kaydedildi")
            
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Konfigürasyon kaydedilemedi:\n{e}")
            
    def validate_config(self):
        """Konfigürasyonu doğrula"""
        if not self.email_var.get().strip():
            messagebox.showerror("Hata", "❌ LinkedIn email adresi gerekli!")
            return False
            
        if not self.password_var.get().strip():
            messagebox.showerror("Hata", "❌ LinkedIn şifresi gerekli!")
            return False
            
        if not self.keywords_var.get().strip():
            messagebox.showerror("Hata", "❌ Anahtar kelimeler gerekli!")
            return False
            
        try:
            max_profiles = int(self.max_profiles_var.get())
            if max_profiles < 1 or max_profiles > 1000:
                messagebox.showerror("Hata", "❌ Maksimum profil sayısı 1-1000 arasında olmalı!")
                return False
        except ValueError:
            messagebox.showerror("Hata", "❌ Geçerli bir profil sayısı girin!")
            return False
            
        return True
        
    def start_campaign(self):
        """Kampanyayı başlat"""
        if not self.validate_config():
            return
            
        if self.bot_running:
            messagebox.showwarning("Uyarı", "⚠️ Bot zaten çalışıyor!")
            return
            
        # Önce ayarları kaydet
        self.save_config()
        
        # Onay al
        confirm = messagebox.askyesno(
            "Kampanya Başlat", 
            f"🚀 Kampanya başlatılsın?\n\n"
            f"🔍 Anahtar kelimeler: {self.keywords_var.get()}\n"
            f"👥 Hedef profil sayısı: {self.max_profiles_var.get()}\n"
            f"📄 Başlangıç sayfası: {self.start_page_var.get()}"
        )
        
        if not confirm:
            return
            
        # Bot durumunu güncelle
        self.bot_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="🟢 Bot durumu: Çalışıyor")
        self.progress_bar.start()
        
        # Bot thread'ini başlat
        self.bot_thread = threading.Thread(target=self.run_bot_campaign, daemon=True)
        self.bot_thread.start()
        
        self.log_message("🚀 Kampanya başlatıldı!")
        
    def stop_campaign(self):
        """Kampanyayı durdur"""
        self.bot_running = False
        
        # Bot varsa kapat
        if self.current_bot:
            try:
                self.current_bot.close()
            except:
                pass
                
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="🔴 Bot durumu: Durduruldu")
        self.progress_bar.stop()
        
        self.log_message("⏹️ Kampanya durduruldu!")
        
    def run_bot_campaign(self):
        """Bot kampanyasını arka planda çalıştır"""
        try:
            # Parametreleri al
            keywords = self.keywords_var.get()
            max_profiles = int(self.max_profiles_var.get())
            start_page = int(self.start_page_var.get())
            custom_message = self.message_text.get(1.0, tk.END).strip()
            
            # LinkedIn bilgilerini al
            email = self.email_var.get().strip()
            password = self.password_var.get().strip()
            
            if not email or not password:
                self.log_message("❌ LinkedIn email ve şifre gerekli!")
                return
            
            self.progress_var.set("İşlem: Bot başlatılıyor...")
            
            # Bot'u başlat - email ve password parametreleriyle
            with LinkedInBot(email=email, password=password) as bot:
                self.current_bot = bot
                
                if not self.bot_running:
                    return
                    
                self.progress_var.set("İşlem: LinkedIn'e giriş yapılıyor...")
                self.log_message("🔐 LinkedIn'e giriş yapılıyor...")
                
                if not bot.login():
                    self.log_message("❌ LinkedIn girişi başarısız!")
                    return
                    
                if not self.bot_running:
                    return
                    
                self.progress_var.set("İşlem: Profiller aranıyor...")
                self.log_message(f"🔍 '{keywords}' için profiller aranıyor...")
                
                # Profilleri topla
                profile_links = bot.get_profile_links(keywords, max_profiles, start_page)
                
                if not self.bot_running:
                    return
                    
                if not profile_links:
                    self.log_message("❌ Hiç profil bulunamadı!")
                    return
                    
                self.log_message(f"📋 {len(profile_links)} profil bulundu")
                self.update_stats(f"Bulunan Profiller: {len(profile_links)}")
                
                # Mesaj gönderme
                success_count = 0
                total_profiles = len(profile_links)
                
                for i, profile_data in enumerate(profile_links):
                    if not self.bot_running:
                        break
                        
                    profile_url = profile_data.get('url')
                    profile_name = profile_data.get('name', 'Unknown')
                    
                    self.progress_var.set(f"İşlem: {i+1}/{total_profiles} - {profile_name}")
                    self.log_message(f"📩 {i+1}/{total_profiles}: {profile_name}")
                    
                    try:
                        if bot.send_connection_request(profile_url, custom_message):
                            success_count += 1
                            self.log_message(f"✅ Başarılı: {profile_name}")
                        else:
                            self.log_message(f"❌ Başarısız: {profile_name}")
                    except Exception as e:
                        self.log_message(f"⚠️ Hata ({profile_name}): {e}")
                        
                    # İstatistikleri güncelle
                    success_rate = (success_count / (i + 1)) * 100
                    self.update_stats(
                        f"Bulunan Profiller: {total_profiles}\n"
                        f"İşlenen: {i+1}\n"
                        f"Başarılı: {success_count}\n"
                        f"Başarı Oranı: {success_rate:.1f}%"
                    )
                    
                    if not self.bot_running:
                        break
                        
                # Sonuçları rapor et
                self.log_message(f"🎉 Kampanya tamamlandı!")
                self.log_message(f"📊 Toplam: {total_profiles}, Başarılı: {success_count}")
                
                messagebox.showinfo(
                    "Kampanya Tamamlandı", 
                    f"🎉 Kampanya başarıyla tamamlandı!\n\n"
                    f"📊 Toplam profil: {total_profiles}\n"
                    f"✅ Başarılı mesaj: {success_count}\n"
                    f"📈 Başarı oranı: {(success_count/total_profiles)*100:.1f}%"
                )
                
        except Exception as e:
            self.log_message(f"❌ Kampanya hatası: {e}")
            messagebox.showerror("Hata", f"❌ Kampanya sırasında hata:\n{e}")
            
        finally:
            # Bot durumunu sıfırla
            self.bot_running = False
            self.current_bot = None
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="⚪ Bot durumu: Hazır")
            self.progress_bar.stop()
            self.progress_var.set("İşlem: Tamamlandı")
            
    def log_message(self, message):
        """Log mesajını queue'ya ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_queue.put(formatted_message)
        
    def update_logs(self):
        """Log queue'dan mesajları al ve görüntüle"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
            
        # 100ms sonra tekrar kontrol et
        self.root.after(100, self.update_logs)
        
    def update_stats(self, stats_text):
        """İstatistik alanını güncelle"""
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
    def open_reports_folder(self):
        """Rapor klasörünü aç"""
        try:
            os.startfile(os.getcwd())
        except:
            messagebox.showerror("Hata", "❌ Rapor klasörü açılamadı!")
            
    def view_last_report(self):
        """En son raporu görüntüle"""
        try:
            # CSV dosyalarını bul
            csv_files = [f for f in os.listdir('.') if f.startswith('linkedin_bot_report_') and f.endswith('.csv')]
            if not csv_files:
                messagebox.showinfo("Bilgi", "ℹ️ Henüz rapor dosyası bulunamadı!")
                return
                
            # En son dosyayı bul
            latest_file = max(csv_files, key=os.path.getctime)
            
            # Raporu göster
            self.show_report(latest_file)
            
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Rapor görüntülenemedi:\n{e}")
            
    def show_report(self, filename):
        """Rapor dosyasını yeni pencerede göster"""
        try:
            report_window = tk.Toplevel(self.root)
            report_window.title(f"📊 Rapor: {filename}")
            report_window.geometry("800x600")
            
            # Treeview ile tablo oluştur
            tree_frame = ttk.Frame(report_window)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            tree = ttk.Treeview(tree_frame)
            scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # CSV dosyasını oku
            with open(filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                headers = next(csv_reader)
                
                # Kolonları ayarla
                tree['columns'] = headers
                tree['show'] = 'headings'
                
                for header in headers:
                    tree.heading(header, text=header)
                    tree.column(header, width=150)
                
                # Verileri ekle
                for row in csv_reader:
                    tree.insert('', tk.END, values=row)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        except Exception as e:
            messagebox.showerror("Hata", f"❌ Rapor okunamadı:\n{e}")

def main():
    """Ana fonksiyon"""
    root = tk.Tk()
    app = LinkedInBotGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("🔚 Uygulama kapatıldı")

if __name__ == "__main__":
    main()
