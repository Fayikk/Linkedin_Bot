#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Bot Web GUI - Local Client Arayüzü
Kullanıcının bilgisayarında çalışan tarayıcı tabanlı arayüz

Özellikler:
- Kullanıcının bilgisayarında çalışır
- Otomatik Chrome/ChromeDriver kurulumu
- Gerçek zamanlı güncellemeler
- Kolay kurulum ve kullanım
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import os
import sys
import threading
import time
import csv
import webbrowser
from datetime import datetime
from linkedin_bot import LinkedInBot
from dotenv import load_dotenv, set_key
import json
import subprocess
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'linkedin_bot_secret_key_2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global değişkenler
bot_status = {
    'running': False,
    'current_task': 'Hazır',
    'progress': 0,
    'installation_complete': False,
    'stats': {
        'found_profiles': 0,
        'processed': 0,
        'successful': 0,
        'failed': 0
    }
}

def check_installation():
    """Kurulum durumunu kontrol et"""
    try:
        # Chrome kontrol
        chrome_installed = False
        chromedriver_installed = False
        
        # ChromeDriver kontrol
        chromedriver_path = Path("chromedriver/chromedriver.exe" if sys.platform.startswith('win') else "chromedriver/chromedriver")
        if chromedriver_path.exists():
            chromedriver_installed = True
            
        # Chrome kontrol (basit)
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            if chromedriver_installed:
                service = Service(str(chromedriver_path))
                driver = webdriver.Chrome(service=service, options=options)
                driver.quit()
                chrome_installed = True
            else:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                driver.quit()
                chrome_installed = True
                
        except Exception:
            chrome_installed = False
            
        bot_status['installation_complete'] = chrome_installed and chromedriver_installed
        return bot_status['installation_complete']
        
    except Exception as e:
        print(f"Kurulum kontrol hatası: {e}")
        return False

@app.route('/')
def index():
    """Ana sayfa"""
    check_installation()
    return render_template('index.html')

@app.route('/install')
def install_page():
    """Kurulum sayfası"""
    return render_template('install.html')

@socketio.on('check_installation')
def handle_check_installation():
    """Kurulum durumunu kontrol et"""
    installation_ok = check_installation()
    emit('installation_status', {
        'complete': installation_ok,
        'message': 'Kurulum tamamlandı' if installation_ok else 'Kurulum gerekli'
    })

@socketio.on('start_installation')
def handle_start_installation():
    """Otomatik kurulumu başlat"""
    def run_installation():
        try:
            emit('log_message', {'message': '🚀 Otomatik kurulum başlatılıyor...'})
            
            # auto_installer.py çalıştır
            process = subprocess.Popen([
                sys.executable, 'auto_installer.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
               universal_newlines=True, bufsize=1)
            
            # Çıktıları gerçek zamanlı gönder
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    socketio.emit('log_message', {'message': line.strip()})
                    
            process.wait()
            
            if process.returncode == 0:
                bot_status['installation_complete'] = True
                socketio.emit('installation_status', {
                    'complete': True,
                    'message': '✅ Kurulum başarıyla tamamlandı!'
                })
                socketio.emit('log_message', {'message': '🎉 Kurulum tamamlandı! Sayfayı yenileyin.'})
            else:
                socketio.emit('log_message', {'message': '❌ Kurulum başarısız oldu!'})
                
        except Exception as e:
            socketio.emit('log_message', {'message': f'❌ Kurulum hatası: {e}'})
            
    threading.Thread(target=run_installation, daemon=True).start()

@app.route('/save_config', methods=['POST'])
def save_config():
    """Konfigürasyonu kaydet"""
    try:
        data = request.json
        env_file = '.env'
        
        set_key(env_file, 'LINKEDIN_EMAIL', data.get('email', ''))
        set_key(env_file, 'LINKEDIN_PASSWORD', data.get('password', ''))
        set_key(env_file, 'SEARCH_KEYWORDS', data.get('keywords', ''))
        set_key(env_file, 'MAX_PROFILES_PER_SESSION', str(data.get('max_profiles', 50)))
        set_key(env_file, 'DELAY_BETWEEN_MESSAGES', str(data.get('delay_messages', 10)))
        set_key(env_file, 'DELAY_BETWEEN_SEARCHES', str(data.get('delay_searches', 5)))
        set_key(env_file, 'DEFAULT_MESSAGE', data.get('message', ''))
        
        return jsonify({'success': True, 'message': 'Konfigürasyon kaydedildi!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Hata: {str(e)}'})

@app.route('/start_campaign', methods=['POST'])
def start_campaign():
    """Kampanyayı başlat"""
    global bot_status
    
    if bot_status['running']:
        return jsonify({'success': False, 'message': 'Bot zaten çalışıyor!'})
    
    try:
        data = request.json
        keywords = data.get('keywords', 'software engineer')
        max_profiles = int(data.get('max_profiles', 50))
        start_page = int(data.get('start_page', 1))
        message = data.get('message', '')
        
        # Bot durumunu güncelle
        bot_status['running'] = True
        bot_status['current_task'] = 'Başlatılıyor...'
        bot_status['progress'] = 0
        bot_status['stats'] = {'found_profiles': 0, 'processed': 0, 'successful': 0, 'failed': 0}
        
        # Bot thread'ini başlat
        thread = threading.Thread(
            target=run_bot_campaign,
            args=(keywords, max_profiles, start_page, message),
            daemon=True
        )
        thread.start()
        
        return jsonify({'success': True, 'message': 'Kampanya başlatıldı!'})
        
    except Exception as e:
        bot_status['running'] = False
        return jsonify({'success': False, 'message': f'Hata: {str(e)}'})

@app.route('/stop_campaign', methods=['POST'])
def stop_campaign():
    """Kampanyayı durdur"""
    global bot_status, current_bot
    
    bot_status['running'] = False
    bot_status['current_task'] = 'Durduruluyor...'
    
    if current_bot:
        try:
            current_bot.close()
        except:
            pass
    
    return jsonify({'success': True, 'message': 'Kampanya durduruldu!'})

@app.route('/status')
def get_status():
    """Bot durumunu döndür"""
    return jsonify(bot_status)

@app.route('/reports')
def get_reports():
    """Rapor listesini döndür"""
    try:
        csv_files = [f for f in os.listdir('.') if f.startswith('linkedin_bot_report_') and f.endswith('.csv')]
        reports = []
        
        for file in csv_files:
            stat = os.stat(file)
            reports.append({
                'filename': file,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            })
            
        # En son dosyayı başa al
        reports.sort(key=lambda x: x['created'], reverse=True)
        return jsonify({'reports': reports})
        
    except Exception as e:
        return jsonify({'reports': [], 'error': str(e)})

@app.route('/download_report/<filename>')
def download_report(filename):
    """Raporu indir"""
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

def run_bot_campaign(keywords, max_profiles, start_page, custom_message):
    """Bot kampanyasını çalıştır"""
    global bot_status, current_bot

    def log_callback(msg):
        socketio.emit('log_message', {'message': msg})

    try:
        print(f"🔧 DEBUG: Bot kampanyası başlatılıyor...")
        print(f"🔧 DEBUG: Parametreler - keywords:{keywords}, max:{max_profiles}")
        
        # .env dosyasını yeniden yükle
        load_dotenv(override=True)
        
        print(f"🔧 DEBUG: .env yüklendi")
        print(f"🔧 DEBUG: Email: {os.getenv('LINKEDIN_EMAIL')}")
        print(f"🔧 DEBUG: Şifre var mı: {bool(os.getenv('LINKEDIN_PASSWORD'))}")
        
        print(f"🔧 DEBUG: LinkedInBot() çağrılacak (parametre yok)")
        
        # Bot'u başlat (parametre gerektirmez, .env'den yükler)
        with LinkedInBot(log_callback=log_callback) as bot:
            current_bot = bot
            
            print(f"🔧 DEBUG: Bot oluşturuldu, giriş yapılacak...")
            
            # Durum güncellemeleri
            bot_status['current_task'] = 'LinkedIn\'e giriş yapılıyor...'
            socketio.emit('status_update', bot_status)
            
            if not bot.login():
                bot_status['running'] = False
                bot_status['current_task'] = 'Giriş başarısız!'
                socketio.emit('log_message', {'message': '❌ LinkedIn girişi başarısız!'})
                return
            
            if not bot_status['running']:
                return
            
            socketio.emit('log_message', {'message': '✅ LinkedIn girişi başarılı!'})
            
            # Profilleri topla
            bot_status['current_task'] = f'Profiller aranıyor: {keywords}'
            socketio.emit('status_update', bot_status)
            
            profile_links = bot.get_profile_links(keywords, max_profiles, start_page)
            
            if not bot_status['running']:
                return
            
            if not profile_links:
                bot_status['current_task'] = 'Profil bulunamadı!'
                socketio.emit('log_message', {'message': '❌ Hiç profil bulunamadı!'})
                return
            
            bot_status['stats']['found_profiles'] = len(profile_links)
            socketio.emit('log_message', {'message': f'📋 {len(profile_links)} profil bulundu'})
            
            # Mesaj gönderme
            success_count = 0
            failed_count = 0
            total_profiles = len(profile_links)
            
            for i, profile_data in enumerate(profile_links):
                if not bot_status['running']:
                    break
                
                profile_url = profile_data.get('url')
                profile_name = profile_data.get('name', 'Unknown')
                
                bot_status['current_task'] = f'İşleniyor: {profile_name} ({i+1}/{total_profiles})'
                bot_status['progress'] = int((i / total_profiles) * 100)
                bot_status['stats']['processed'] = i + 1
                
                socketio.emit('status_update', bot_status)
                socketio.emit('log_message', {'message': f'📩 {i+1}/{total_profiles}: {profile_name}'})
                
                try:
                    if bot.send_connection_request(profile_url, custom_message):
                        success_count += 1
                        bot_status['stats']['successful'] = success_count
                        socketio.emit('log_message', {'message': f'✅ Başarılı: {profile_name}'})
                    else:
                        failed_count += 1
                        bot_status['stats']['failed'] = failed_count
                        socketio.emit('log_message', {'message': f'❌ Başarısız: {profile_name}'})
                        
                except Exception as e:
                    failed_count += 1
                    bot_status['stats']['failed'] = failed_count
                    socketio.emit('log_message', {'message': f'⚠️ Hata ({profile_name}): {e}'})
                
                if not bot_status['running']:
                    break
            
            # Kampanya tamamlandı
            bot_status['current_task'] = 'Tamamlandı!'
            bot_status['progress'] = 100
            socketio.emit('status_update', bot_status)
            socketio.emit('log_message', {'message': f'🎉 Kampanya tamamlandı! Başarılı: {success_count}/{total_profiles}'})
            
    except Exception as e:
        print(f"🔧 DEBUG: Kampanya hatası - {type(e).__name__}: {e}")
        
        if "WebDriver başlatılamadı" in str(e):
            socketio.emit('log_message', {'message': '❌ ChromeDriver hatası! WebDriver başlatılamadı.'})
            socketio.emit('log_message', {'message': '💡 Çözüm: python fix_chrome137.py çalıştırın'})
        else:
            socketio.emit('log_message', {'message': f'❌ Kampanya hatası: {e}'})
        
    finally:
        bot_status['running'] = False
        current_bot = None
        socketio.emit('status_update', bot_status)

if __name__ == '__main__':
    print("🚀 LinkedIn Bot Web GUI başlatılıyor...")
    print("🌐 Tarayıcınızda şu adresi açın: http://localhost:5000")
    try:
        import eventlet
        import eventlet.wsgi
        socketio.run(app, debug=False, host='0.0.0.0', port=5000)
    except ImportError:
        print("⚠️ eventlet yüklü değil! Lütfen requirements.txt ile yükleyin.")
        print("pip install eventlet")
        socketio.run(app, debug=False, host='0.0.0.0', port=5000)
