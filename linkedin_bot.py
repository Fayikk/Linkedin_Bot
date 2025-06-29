from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import sys

class LinkedInBot:
    def __init__(self, log_callback=None):
        load_dotenv()
        self.email = os.getenv('LINKEDIN_EMAIL')
        self.password = os.getenv('LINKEDIN_PASSWORD')
        self.default_message = os.getenv('DEFAULT_MESSAGE')
        self.max_profiles = int(os.getenv('MAX_PROFILES_PER_SESSION', 50))
        self.message_delay = int(os.getenv('DELAY_BETWEEN_MESSAGES', 10))
        self.search_delay = int(os.getenv('DELAY_BETWEEN_SEARCHES', 5))
        
        self.driver = None
        self.sent_messages = []
        self.searched_profiles = []
        self.log_callback = log_callback

    def log(self, message):
        print(message)
        if self.log_callback:
            try:
                self.log_callback(message)
            except Exception as e:
                print(f"[LogCallbackError] {e}")

    def setup_driver(self):
        """Chrome WebDriver'ı başlatır"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            # Platforma göre chromedriver uzantısı
            if sys.platform.startswith('win'):
                chromedriver_filename = "chromedriver.exe"
            else:
                chromedriver_filename = "chromedriver"

            # .env'den chromedriver path al (varsa)
            env_driver_path = os.getenv('CHROMEDRIVER_PATH')
            if env_driver_path and os.path.exists(env_driver_path):
                self.log(f"🔧 .env'den ChromeDriver kullanılıyor: {env_driver_path}")
                service = Service(env_driver_path)
            else:
                # Önce manuel driver yolunu dene (chromedriver klasörü içinde)
                manual_driver_path = os.path.join(os.getcwd(), "chromedriver", chromedriver_filename)
                if os.path.exists(manual_driver_path):
                    self.log(f"🔧 Manuel ChromeDriver kullanılıyor: {manual_driver_path}")
                    service = Service(manual_driver_path)
                else:
                    self.log("🔧 ChromeDriverManager kullanılıyor...")
                    driver_path = ChromeDriverManager().install()
                    # Eğer yol THIRD_PARTY_NOTICES dosyasını işaret ediyorsa, doğru chromedriver dosyasını bul
                    if "THIRD_PARTY_NOTICES" in driver_path:
                        driver_dir = os.path.dirname(driver_path)
                        driver_path = os.path.join(driver_dir, chromedriver_filename)
                        if not os.path.exists(driver_path):
                            parent_dir = os.path.dirname(driver_dir)
                            driver_path = os.path.join(parent_dir, chromedriver_filename)
                    self.log(f"🔧 ChromeDriver yolu: {driver_path}")
                    service = Service(driver_path)

            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.log("✅ WebDriver başarıyla başlatıldı")
            return True
        except Exception as e:
            self.log(f"❌ WebDriver başlatılamadı: {e}")
            self.log("💡 Çözüm önerileri:")
            self.log("   1. Chrome tarayıcısını güncelleyin")
            self.log("   2. python fix_chrome137.py çalıştırın")
            self.log("   3. Yönetici olarak çalıştırın")
            return False
    
    def login(self):
        """LinkedIn'e giriş yapar"""
        try:
            self.log("🔐 LinkedIn'e giriş yapılıyor...")
            self.log(f"📧 Email: {self.email}")
            self.log(f"🔐 Şifre uzunluğu: {len(self.password) if self.password else 0}")

            if not self.email or not self.password:
                self.log("❌ Email veya şifre boş!")
                return False

            self.driver.get("https://www.linkedin.com/login")
            time.sleep(3)

            # Email girişi - birden fazla seçenek dene
            email_field = None
            email_selectors = [
                "//input[@id='username']",
                "//input[@name='session_key']",
                "//input[contains(@placeholder, 'E-posta')]",
                "//input[contains(@placeholder, 'Email')]"
            ]
            for selector in email_selectors:
                try:
                    email_field = self.driver.find_element(By.XPATH, selector)
                    break
                except Exception as e:
                    self.log(f"⚠️ Email alanı bulunamadı: {selector} ({e})")
                    continue

            if not email_field:
                self.log("❌ Email alanı hiç bulunamadı!")
                return False

            # Şifre girişi - birden fazla seçenek dene
            password_field = None
            password_selectors = [
                "//input[@id='password']",
                "//input[@name='session_password']",
                "//input[contains(@placeholder, 'Şifre')]",
                "//input[contains(@placeholder, 'Password')]"
            ]
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.XPATH, selector)
                    break
                except Exception as e:
                    self.log(f"⚠️ Şifre alanı bulunamadı: {selector} ({e})")
                    continue

            if not password_field:
                self.log("❌ Şifre alanı hiç bulunamadı!")
                return False

            # Sadece alanlar bulunduysa devam et!
            email_field.clear()
            email_field.send_keys(self.email)
            password_field.clear()
            password_field.send_keys(self.password)

            # Giriş butonuna tıkla
            login_selectors = [
                "//button[@type='submit']",
                "//button[contains(text(), 'Sign in')]",
                "//button[contains(text(), 'Giriş')]",
                ".login__form_action_container button"
            ]
            
            login_button = None
            for selector in login_selectors:
                try:
                    if selector.startswith("//"):
                        login_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not login_button:
                self.log("❌ Giriş butonu bulunamadı")
                return False
            
            login_button.click()
            self.log("⏳ Giriş işlemi kontrol ediliyor...")
            
            # Ana sayfanın yüklenmesini bekle - birden fazla seçenek dene
            success_indicators = [
                (By.CLASS_NAME, "global-nav"),
                (By.CSS_SELECTOR, ".global-nav"),
                (By.XPATH, "//nav[@class='global-nav']"),
                (By.CSS_SELECTOR, "[data-test-global-nav]"),
                (By.XPATH, "//div[@class='feed-container']")
            ]
            
            login_successful = False
            for locator_type, locator_value in success_indicators:
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((locator_type, locator_value))
                    )
                    login_successful = True
                    break
                except:
                    continue
            
            if login_successful:
                self.log("✅ Giriş başarılı!")
                time.sleep(3)
                return True
            else:
                # Captcha veya güvenlik kontrolü var mı?
                if "challenge" in self.driver.current_url or "captcha" in self.driver.current_url:
                    self.log("⚠️ LinkedIn güvenlik kontrolü tespit edildi")
                    self.log("💡 Lütfen tarayıcıda manuel olarak captcha'yı çözün")
                    input("Çözdükten sonra Enter'a basın...")
                    return True
                else:
                    self.log("❌ Giriş başarısız - sayfada beklenmeyen durum")
                    return False
            
        except TimeoutException:
            self.log("❌ Giriş zaman aşımına uğradı")
            self.log("💡 LinkedIn hesap bilgilerinizi kontrol edin")
            return False
        except Exception as e:
            self.log(f"❌ Giriş hatası: {e}")
            return False
    
    def search_people(self, keywords="software engineer", page=1):
        """Belirtilen anahtar kelimelerle direkt LinkedIn arama URL'sine gider"""
        try:
            self.log(f"🔍 '{keywords}' için sayfa {page} aranıyor...")
            
            # Direkt LinkedIn arama URL'sini oluştur
            # Keywords'u URL encoding yap
            import urllib.parse
            encoded_keywords = urllib.parse.quote_plus(keywords)
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={encoded_keywords}&page={page}"
            
            self.log(f"🌐 URL'ye gidiliyor: {search_url}")
            self.driver.get(search_url)
            
            # Sayfanın yüklenmesi için bekle
            time.sleep(5)
            
            # Sayfa yüklenme kontrolü - arama sonuçları var mı?
            page_indicators = [
                "//div[contains(@class, 'search-results-container')]",
                "//div[contains(@class, 'search-results')]",
                "//ul[contains(@class, 'reusable-search__entity-result-list')]",
                "//div[contains(@class, 'entity-result')]",
                "//div[@class='search-results-container']"
            ]
            
            page_loaded = False
            for indicator in page_indicators:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, indicator))
                    )
                    page_loaded = True
                    self.log("✅ Arama sonuçları yüklendi")
                    break
                except:
                    continue
            
            if not page_loaded:
                self.log("❌ Arama sonuçları yüklenemedi - manuel kontrol gerekli")
                self.log("� Lütfen tarayıcıda sayfayı kontrol edin")
                return False
            
            # Sayfayı biraz aşağı kaydır
            self.driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(2)
            
            self.log(f"📋 Sayfa {page} başarıyla yüklendi")
            return True
            
        except Exception as e:
            self.log(f"❌ Arama hatası: {e}")
            self.log("💡 Lütfen LinkedIn'e manuel giriş yapıp sayfayı kontrol edin")
            return False
    
    def get_profile_links(self, keywords="software engineer", max_results=10, start_page=1):
        """URL tabanlı sayfalama ile profil linklerini toplar"""
        profile_links = []
        current_page = start_page
        max_pages = start_page + 80  # Maksimum 50 sayfa kontrolü
        
        try:
            self.log(f"📋 Profil linkleri toplanıyor (hedef: {max_results} profil, başlangıç sayfa: {start_page})...")
            
            while len(profile_links) < max_results and current_page <= max_pages:
                self.log(f"\n📄 Sayfa {current_page} işleniyor...")
                
                # URL ile direkt sayfaya git
                if not self.search_people(keywords, current_page):
                    self.log(f"❌ Sayfa {current_page} yüklenemedi, devam ediliyor...")
                    current_page += 1
                    continue
                
                time.sleep(3)  # Sayfanın tam yüklenmesi için bekle
                
                # Bu sayfadaki "Bağlantı kur" butonlu kullanıcıları bul
                connect_profiles = self.find_connectable_profiles()
                
                if not connect_profiles:
                    self.log(f"⚠️ Sayfa {current_page}'de bağlantı kurulabilir profil bulunamadı")
                    current_page += 1
                    continue
                
                # Bu sayfadaki profilleri profile_links listesine ekle
                new_profiles_count = 0
                for profile_data in connect_profiles:
                    if len(profile_links) >= max_results:
                        break
                    
                    profile_url = profile_data.get('url')
                    if profile_url and profile_url not in [p.get('url') for p in profile_links]:
                        profile_links.append(profile_data)
                        new_profiles_count += 1
                
                self.log(f"📊 Sayfa {current_page}'den {new_profiles_count} bağlanabilir profil eklendi (Toplam: {len(profile_links)})")
                
                # Eğer hedef sayıya ulaştıysak dur
                if len(profile_links) >= max_results:
                    self.log(f"✅ Hedef profil sayısına ulaşıldı: {len(profile_links)}")
                    break
                
                # Sonraki sayfaya geç
                current_page += 1
                time.sleep(2)  # Sayfa geçişi için bekle
            
            self.log(f"📋 Toplam {len(profile_links)} bağlanabilir profil toplandı")
            return profile_links[:max_results]  # İstenenden fazla varsa kırp
            
        except Exception as e:
            self.log(f"❌ Profil toplama hatası: {e}")
            return profile_links
    
    def find_connectable_profiles(self):
        """Mevcut sayfada 'Bağlantı kur' butonu olan profilleri bulur"""
        connectable_profiles = []
        seen_urls = set()  # Aynı profillerin tekrarlanmasını önle
        
        try:
            # Sayfayı aşağı kaydır
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            
            # Önce tüm "Bağlantı kur" butonlarını bul
            connect_button_selectors = [
                "//button[contains(@aria-label, 'bağlantı kurmak için davet et')]",
                "//button[contains(@aria-label, 'adlı kullanıcıyı bağlantı kurmak')]",
                "//button[@class='artdeco-button artdeco-button--2 artdeco-button--secondary ember-view']",
                "//button[contains(@class, 'artdeco-button--secondary')]//span[text()='Bağlantı kur']",
                "//span[text()='Bağlantı kur']/parent::button",
                "//button[contains(text(), 'Bağlantı kur')]",
                "//button[contains(@class, 'artdeco-button--secondary')]"
            ]
            
            all_connect_buttons = []
            for selector in connect_button_selectors:
                try:
                    buttons = self.driver.find_elements(By.XPATH, selector)
                    for btn in buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            all_connect_buttons.append(btn)
                except:
                    continue
            
            self.log(f"🔍 Toplam {len(all_connect_buttons)} 'Bağlantı kur' butonu bulundu")
            
            # Her buton için en yakın profil kartını ve profil linkini bul
            for i, button in enumerate(all_connect_buttons):
                try:
                    # Butonun parent container'ını bul (profil kartı)
                    parent_selectors = [
                        ".//ancestor::div[contains(@class, 'entity-result')]",
                        ".//ancestor::li[contains(@class, 'reusable-search__result-container')]",
                        ".//ancestor::div[contains(@class, 'search-result')]",
                        ".//ancestor::div[contains(@class, 'result-card')]"
                    ]
                    
                    profile_card = None
                    for selector in parent_selectors:
                        try:
                            profile_card = button.find_element(By.XPATH, selector)
                            break
                        except:
                            continue
                    
                    if not profile_card:
                        self.log(f"  ⚠️ Buton {i+1}: Profil kartı bulunamadı")
                        continue
                    
                    # Profil linkini ve ismini bul - daha geniş seçici kullan
                    profile_link_selectors = [
                        ".//a[contains(@href, '/in/') and contains(@class, 'app-aware-link')]",
                        ".//h3//a[contains(@href, '/in/')]",
                        ".//span[@class='entity-result__title-text']//a[contains(@href, '/in/')]",
                        ".//div[contains(@class, 'entity-result__title')]//a[contains(@href, '/in/')]",
                        ".//a[contains(@href, '/in/')]"
                    ]
                    
                    profile_url = None
                    profile_name = "Unknown"
                    
                    for link_selector in profile_link_selectors:
                        try:
                            link_element = profile_card.find_element(By.XPATH, link_selector)
                            profile_url = link_element.get_attribute('href')
                            if profile_url:
                                # İsim bulma için daha detaylı arama
                                name_text = link_element.text.strip()
                                if name_text:
                                    profile_name = name_text
                                else:
                                    # Alt elementlerde isim ara
                                    try:
                                        name_spans = link_element.find_elements(By.XPATH, ".//span")
                                        for span in name_spans:
                                            span_text = span.text.strip()
                                            if span_text and len(span_text) > 2:
                                                profile_name = span_text
                                                break
                                    except:
                                        pass
                                break
                        except:
                            continue
                    
                    if not profile_url:
                        self.log(f"  ⚠️ Buton {i+1}: Profil linki bulunamadı")
                        continue
                    
                    # URL'yi temizle ve tekrar kontrolü yap
                    clean_url = profile_url.split('?')[0]
                    if clean_url in seen_urls:
                        self.log(f"  ⚠️ Buton {i+1}: Zaten işlenmiş profil - atlanıyor")
                        continue
                    
                    seen_urls.add(clean_url)
                    
                    # Başarılı eşleştirme
                    connectable_profiles.append({
                        'url': clean_url,
                        'name': profile_name,
                        'button': button,
                        'card_index': i
                    })
                    self.log(f"  ✅ Buton {i+1}: {profile_name} - {clean_url}")
                    
                except Exception as e:
                    self.log(f"  ⚠️ Buton {i+1} işlenirken hata: {e}")
                    continue
            
            self.log(f"📊 Toplam {len(connectable_profiles)} benzersiz bağlanabilir profil eşleştirildi")
            return connectable_profiles
            
        except Exception as e:
            self.log(f"❌ Bağlanabilir profil arama hatası: {e}")
            return connectable_profiles
    
    def send_connection_request(self, profile_url, custom_message=None):
        """Bir profile bağlantı isteği gönderir"""
        try:
            self.log(f"📩 Bağlantı isteği gönderiliyor: {profile_url}")
            
            # Profile git
            self.driver.get(profile_url)
            time.sleep(random.uniform(3, 6))
            
            # Sayfayı biraz aşağı kaydır - butonun görünür olması için
            self.driver.execute_script("window.scrollTo(0, 300);")
            time.sleep(2)
            
            # Bağlan/Bağlantı Kur butonunu bul - birden fazla seçenek dene
            connect_button_selectors = [
                "//button[contains(text(), 'Bağlantı kur')]",
                "//button[contains(text(), 'Bağlantı Kur')]",
                "//button[contains(text(), 'bağlantı kur')]",
                "//button[contains(text(), 'Bağlan')]", 
                "//button[contains(text(), 'Connect')]",
                "//button[contains(@aria-label, 'bağlantı kurmak için davet et')]",
                "//button[contains(@aria-label, 'Connect')]",
                "//button[contains(@aria-label, 'Bağlan')]",
                "//button[contains(@aria-label, 'Bağlantı')]",
                "//span[contains(text(), 'Bağlantı kur')]/parent::button",
                "//span[contains(text(), 'Bağlan')]/parent::button",
                "//span[contains(text(), 'Connect')]/parent::button"
            ]
            
            connect_button = None
            for selector in connect_button_selectors:
                try:
                    # Element'i bul
                    buttons = self.driver.find_elements(By.XPATH, selector)
                    
                    for button in buttons:
                        # Element görünür ve etkin mi kontrol et
                        if button.is_displayed():
                            # Butona scroll yap
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                            time.sleep(1)
                            
                            connect_button = button
                            self.log(f"✅ Bağlantı butonu bulundu: {selector}")
                            break
                    
                    if connect_button:
                        break
                        
                except Exception as ex:
                    continue
            
            # Eğer hiç buton bulunamazsa, sayfadaki tüm butonları listele (debug için)
            if not connect_button:
                self.log("🔍 Sayfadaki mevcut butonlar:")
                all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                connection_related = []
                
                for i, btn in enumerate(all_buttons[:20]):  # İlk 20 butonu kontrol et
                    try:
                        btn_text = btn.text.strip()
                        btn_aria = btn.get_attribute('aria-label') or ''
                        
                        if btn_text or btn_aria:
                            # Bağlantı ile ilgili butonları tespit et
                            if any(keyword in btn_text.lower() or keyword in btn_aria.lower() 
                                   for keyword in ['bağlantı', 'bağlan', 'connect']):
                                connection_related.append(f"   {i+1}. Text: '{btn_text}', Aria: '{btn_aria}'")
                            elif btn_text and len(btn_text) < 50:  # Diğer kısa metinli butonlar
                                self.log(f"   {i+1}. '{btn_text}'")
                    except:
                        continue
                
                if connection_related:
                    self.log("🎯 Bağlantı ile ilgili butonlar:")
                    for btn_info in connection_related:
                        self.log(btn_info)
                
                self.log("⚠️ Tıklanabilir bağlantı butonu bulunamadı")
                return False
            
            # Butona tıkla
            try:
                # Önce normal tıklama dene
                try:
                    connect_button.click()
                    self.log("✅ Bağlantı butonuna tıklandı (normal click)")
                except:
                    # JavaScript ile tıklama dene
                    self.driver.execute_script("arguments[0].click();", connect_button)
                    self.log("✅ Bağlantı butonuna tıklandı (JavaScript click)")
                
                time.sleep(3)
            except Exception as e:
                self.log(f"❌ Butona tıklanamadı: {e}")
                return False
            
            # Mesaj ekle seçeneği varsa tıkla (opsiyonel)
            message_sent = False
            try:
                # Not ekle/Add note butonunu ara
                add_note_selectors = [
                    "//button[contains(text(), 'Not ekle')]",
                    "//button[contains(text(), 'Add a note')]",
                    "//button[contains(text(), 'Mesaj ekle')]",
                    "//button[contains(@aria-label, 'Not ekle')]",
                    "//button[contains(@aria-label, 'Add note')]"
                ]
                
                add_note_button = None
                for selector in add_note_selectors:
                    try:
                        add_note_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        break
                    except:
                        continue
                
                if add_note_button:
                    add_note_button.click()
                    time.sleep(2)
                    self.log("✅ Mesaj ekleme modalı açıldı")
                    
                    # Mesaj kutusunu bul ve mesajı yaz
                    message_box_selectors = [
                        "//textarea[@name='message']",
                        "//textarea[@id='custom-message']",
                        "//textarea[contains(@placeholder, 'mesaj')]",
                        "//textarea[contains(@placeholder, 'message')]"
                    ]
                    
                    message_box = None
                    for selector in message_box_selectors:
                        try:
                            message_box = self.driver.find_element(By.XPATH, selector)
                            break
                        except:
                            continue
                    
                    if message_box:
                        message = custom_message if custom_message else self.default_message
                        message_box.clear()
                        message_box.send_keys(message)
                        time.sleep(2)  # Mesaj yazıldıktan sonra biraz bekle
                        self.log(f"✅ Mesaj yazıldı: {message[:30]}...")
                        
                        # Mesaj yazıldıktan sonra hemen gönder butonunu ara
                        self.log("🔍 Mesaj yazıldı, gönder butonu aranıyor...")
                        
                        # Mesaj modalındaki gönder butonunu bul
                        modal_send_selectors = [
                            "//button[@aria-label='Davetiye gönder']",
                            "//button[contains(@aria-label, 'Davetiye')]",
                            "//button[contains(@id, 'ember') and contains(text(), 'Gönder')]",
                            "//button[contains(@class, 'artdeco-button--primary') and contains(text(), 'Gönder')]",
                            "//span[text()='Gönder']/parent::button",
                            "//button[contains(text(), 'Gönder')]",
                            "//button[contains(text(), 'Send')]",
                            "//button[contains(text(), 'İlet')]",
                            "//div[contains(@class, 'modal')]//button[contains(text(), 'Gönder')]",
                            "//div[contains(@class, 'modal')]//button[contains(text(), 'Send')]",
                            "//form//button[contains(text(), 'Gönder')]",
                            "//form//button[contains(text(), 'Send')]",
                            "//button[@type='submit']",
                            "//span[contains(text(), 'Gönder')]/parent::button",
                            "//span[contains(text(), 'Send')]/parent::button"
                        ]
                        
                        modal_send_button = None
                        for selector in modal_send_selectors:
                            try:
                                buttons = WebDriverWait(self.driver, 3).until(
                                    EC.presence_of_all_elements_located((By.XPATH, selector))
                                )
                                for btn in buttons:
                                    if btn.is_displayed() and btn.is_enabled():
                                        modal_send_button = btn
                                        self.log(f"✅ Modal gönder butonu bulundu: {selector}")
                                        break
                                if modal_send_button:
                                    break
                            except:
                                continue
                        
                        if modal_send_button:
                            try:
                                # JavaScript ile tıkla
                                self.driver.execute_script("arguments[0].click();", modal_send_button)
                                self.log("✅ Modal gönder butonuna tıklandı")
                                message_sent = True
                                time.sleep(3)
                                
                                # Başarı kontrolü - modal kapandı mı?
                                try:
                                    WebDriverWait(self.driver, 5).until_not(
                                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'modal')]"))
                                    )
                                    self.log("✅ Modal kapandı - mesaj gönderildi")
                                except:
                                    self.log("ℹ️ Modal durumu belirsiz")
                                
                            except Exception as e:
                                self.log(f"❌ Modal gönder butonuna tıklanamadı: {e}")
                                return False
                        else:
                            self.log("❌ Modal gönder butonu bulunamadı")
                            # Debug için modal içindeki tüm butonları listele
                            try:
                                all_modal_buttons = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'modal')]//button")
                                self.log(f"🔍 Modal'da {len(all_modal_buttons)} buton bulundu:")
                                for i, btn in enumerate(all_modal_buttons[:5]):
                                    try:
                                        btn_text = btn.text.strip()
                                        btn_aria = btn.get_attribute('aria-label') or ''
                                        self.log(f"   {i+1}. Text: '{btn_text}', Aria: '{btn_aria}', Displayed: {btn.is_displayed()}, Enabled: {btn.is_enabled()}")
                                    except:
                                        pass
                            except:
                                pass
                            return False
                    else:
                        self.log("❌ Mesaj kutusu bulunamadı")
                else:
                    self.log("ℹ️ Mesaj ekleme modalı bulunamadı, mesajsız gönderiliyor")
                        
            except Exception as e:
                self.log(f"ℹ️ Mesaj ekleme işlemi atlandı: {e}")
            
            # Eğer mesaj başarıyla gönderildiyse, genel gönder butonunu arama
            if message_sent:
                self.log("✅ Mesajlı bağlantı isteği zaten gönderildi")
            else:
                # Kısa bekleme sonrası gönder butonunu ara (mesajsız gönderim için)
                time.sleep(2)
                
                # Gönder/Send butonunu bul ve tıkla
                send_button_selectors = [
                    "//button[@aria-label='Davetiye gönder']",
                    "//button[contains(@aria-label, 'Davetiye')]",
                    "//button[contains(@id, 'ember') and contains(text(), 'Gönder')]",
                    "//button[contains(@class, 'artdeco-button--primary') and contains(text(), 'Gönder')]",
                    "//span[text()='Gönder']/parent::button",
                    "//button[contains(text(), 'Gönder')]",
                    "//button[contains(text(), 'Send')]",
                    "//button[contains(text(), 'Davet gönder')]",
                    "//button[contains(text(), 'Send invitation')]",
                    "//button[contains(text(), 'İlet')]",
                    "//button[contains(text(), 'Submit')]",
                    "//button[contains(@aria-label, 'Gönder')]",
                    "//button[contains(@aria-label, 'Send')]",
                    "//button[contains(@aria-label, 'davet gönder')]",
                    "//button[contains(@aria-label, 'Send invitation')]",
                    "//button[@type='submit']",
                    "//button[@data-control-name='invite']",
                    "//span[contains(text(), 'Gönder')]/parent::button",
                    "//span[contains(text(), 'Send')]/parent::button"
                ]
                
                send_button = None
                self.log("🔍 Mesajsız gönder butonu aranıyor...")
                
                for selector in send_button_selectors:
                    try:
                        buttons = self.driver.find_elements(By.XPATH, selector)
                        for button in buttons:
                            if button.is_displayed() and button.is_enabled():
                                # Butona scroll yap
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                                time.sleep(1)
                                send_button = button
                                self.log(f"✅ Mesajsız gönder butonu bulundu: {selector}")
                                break
                        if send_button:
                            break
                    except Exception as ex:
                        continue
                
                if send_button:
                    try:
                        # JavaScript ile güvenli tıklama
                        self.driver.execute_script("arguments[0].click();", send_button)
                        self.log("✅ Mesajsız gönder butonuna tıklandı")
                        message_sent = True
                        time.sleep(3)
                    except Exception as e:
                        self.log(f"❌ Mesajsız gönder butonuna tıklanamadı: {e}")
                        return False
                else:
                    self.log("ℹ️ Mesajsız gönder butonu bulunamadı - bağlantı isteği otomatik gönderilmiş olabilir")
                    message_sent = True
            
            # Başarı kaydı
            self.sent_messages.append({
                'profile_url': profile_url,
                'message': custom_message if custom_message else self.default_message,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            self.log("✅ Bağlantı isteği gönderildi!")
            time.sleep(random.uniform(self.message_delay, self.message_delay + 5))
            return True
            
        except Exception as e:
            self.log(f"❌ Bağlantı isteği gönderilemedi: {e}")
            return False
    
    def run_campaign(self, search_keywords, custom_message=None, max_requests=10, start_page=1):
        """URL tabanlı sayfalama ile otomatik kampanya çalıştırır"""
        try:
            self.log(f"🚀 Kampanya başlatılıyor: '{search_keywords}'")
            self.log(f"📊 Maksimum istek sayısı: {max_requests}")
            self.log(f"📄 Başlangıç sayfası: {start_page}")
            
            # URL tabanlı profil toplama ve bağlantı istekleri gönderme
            connectable_profiles = self.get_profile_links(
                keywords=search_keywords, 
                max_results=max_requests,
                start_page=start_page
            )
            
            if not connectable_profiles:
                self.log("❌ Bağlanabilir profil bulunamadı")
                return False
            
            self.log(f"\n📋 Toplam {len(connectable_profiles)} bağlanabilir profil bulundu")
            
            sent_count = 0
            failed_count = 0
            
            for i, profile_data in enumerate(connectable_profiles, 1):
                if sent_count >= max_requests:
                    self.log(f"✅ Maksimum istek sayısına ulaşıldı: {max_requests}")
                    break
                
                profile_url = profile_data.get('url')
                profile_name = profile_data.get('name', 'Unknown')
                
                self.log(f"\n👤 {i}/{len(connectable_profiles)}: {profile_name}")
                self.log(f"🔗 {profile_url}")
                
                # Bağlantı isteği gönder
                if self.send_connection_request(profile_url, custom_message):
                    sent_count += 1
                    self.log(f"✅ Başarılı - Toplam: {sent_count}/{max_requests}")
                else:
                    failed_count += 1
                    self.log(f"❌ Başarısız - Toplam başarısız: {failed_count}")
                
                # İstekler arası rastgele bekleme
                if sent_count < max_requests:  # Son istekten sonra bekleme yok
                    wait_time = random.uniform(self.message_delay, self.message_delay + 5)
                    self.log(f"⏳ {wait_time:.1f} saniye bekleniyor...")
                    time.sleep(wait_time)
            
            self.log(f"\n🎉 Kampanya tamamlandı!")
            self.log(f"📊 Toplam {sent_count} bağlantı isteği gönderildi")
            self.log(f"📊 {failed_count} başarısız istek")
            self.log(f"📊 Başarı oranı: {(sent_count/(sent_count+failed_count)*100):.1f}%" if (sent_count+failed_count) > 0 else "")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Kampanya hatası: {e}")
            return False
    
    def send_connection_from_search_page(self, profile_data, custom_message=None):
        """Arama sayfasındaki 'Bağlantı kur' butonuna doğrudan tıklar"""
        try:
            profile_name = profile_data.get('name', 'Unknown')
            profile_url = profile_data.get('url')
            connect_button = profile_data.get('button')
            
            self.log(f"📩 Arama sayfasından bağlantı isteği: {profile_name}")
            
            if not connect_button:
                self.log("❌ Bağlantı butonu bulunamadı")
                return False
                
            # Butona scroll yap
            self.driver.execute_script("arguments[0].scrollIntoView(true);", connect_button)
            time.sleep(1)
            
            # Butona tıkla
            try:
                self.driver.execute_script("arguments[0].click();", connect_button)
                self.log("✅ Bağlantı butonuna tıklandı")
                time.sleep(3)
            except Exception as e:
                self.log(f"❌ Butona tıklanamadı: {e}")
                return False
            
            # Mesaj ekleme modalı açıldı mı kontrol et
            message_sent = False
            try:
                # "Not ekle" butonu var mı?
                add_note_selectors = [
                    "//button[contains(text(), 'Not ekle')]",
                    "//button[contains(text(), 'Add a note')]",
                    "//button[contains(text(), 'Mesaj ekle')]",
                    "//button[contains(@aria-label, 'Not ekle')]",
                    "//button[contains(@aria-label, 'Add note')]"
                ]
                
                add_note_button = None
                for selector in add_note_selectors:
                    try:
                        add_note_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        break
                    except:
                        continue
                
                if add_note_button and custom_message:
                    add_note_button.click()
                    time.sleep(2)
                    self.log("✅ Mesaj ekleme modalı açıldı")
                    
                    # Mesaj kutusunu bul ve mesajı yaz
                    message_box_selectors = [
                        "//textarea[@name='message']",
                        "//textarea[@id='custom-message']", 
                        "//textarea[contains(@placeholder, 'mesaj')]",
                        "//textarea[contains(@placeholder, 'message')]"
                    ]
                    
                    message_box = None
                    for selector in message_box_selectors:
                        try:
                            message_box = self.driver.find_element(By.XPATH, selector)
                            break
                        except:
                            continue
                    
                    if message_box:
                        message = custom_message if custom_message else self.default_message
                        message_box.clear()
                        message_box.send_keys(message)
                        time.sleep(2)
                        self.log(f"✅ Mesaj yazıldı: {message[:30]}...")
                        
                        # Modal gönder butonunu bul ve tıkla
                        modal_send_selectors = [
                            "//button[@aria-label='Davetiye gönder']",
                            "//button[contains(@aria-label, 'Davetiye')]",
                            "//button[contains(text(), 'Gönder')]",
                            "//button[contains(text(), 'Send')]",
                            "//span[text()='Gönder']/parent::button",
                            "//span[text()='Send']/parent::button"
                        ]
                        
                        modal_send_button = None
                        for selector in modal_send_selectors:
                            try:
                                buttons = self.driver.find_elements(By.XPATH, selector)
                                for btn in buttons:
                                    if btn.is_displayed() and btn.is_enabled():
                                        modal_send_button = btn
                                        break
                                if modal_send_button:
                                    break
                            except:
                                continue
                        
                        if modal_send_button:
                            self.driver.execute_script("arguments[0].click();", modal_send_button)
                            self.log("✅ Mesajlı bağlantı isteği gönderildi")
                            message_sent = True
                            time.sleep(3)
                        else:
                            self.log("❌ Modal gönder butonu bulunamadı")
                            return False
                    else:
                        self.log("❌ Mesaj kutusu bulunamadı")
                        return False
            except Exception as e:
                self.log(f"ℹ️ Mesaj ekleme atlandı: {e}")
            
            # Eğer mesaj gönderilmemişse, standart gönder butonunu ara
            if not message_sent:
                send_button_selectors = [
                    "//button[@aria-label='Davetiye gönder']",
                    "//button[contains(@aria-label, 'Davetiye')]",
                    "//button[contains(text(), 'Gönder')]",
                    "//button[contains(text(), 'Send')]",
                    "//span[text()='Gönder']/parent::button"
                ]
                
                send_button = None
                for selector in send_button_selectors:
                    try:
                        buttons = self.driver.find_elements(By.XPATH, selector)
                        for button in buttons:
                            if button.is_displayed() and button.is_enabled():
                                send_button = button
                                break
                        if send_button:
                            break
                    except:
                        continue
                
                if send_button:
                    self.driver.execute_script("arguments[0].click();", send_button)
                    self.log("✅ Mesajsız bağlantı isteği gönderildi")
                    message_sent = True
                    time.sleep(3)
                else:
                    self.log("ℹ️ Gönder butonu bulunamadı - otomatik gönderilmiş olabilir")
                    message_sent = True
            
            # Başarı kaydı
            if message_sent:
                self.sent_messages.append({
                    'profile_url': profile_url,
                    'profile_name': profile_name,
                    'message': custom_message if custom_message else self.default_message,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'method': 'search_page'
                })
                
                self.log("✅ Bağlantı isteği başarıyla gönderildi!")
                return True
            else:
                return False
                
        except Exception as e:
            self.log(f"❌ Arama sayfasından bağlantı isteği gönderilemedi: {e}")
            return False
    
    def save_report(self):
        """Gönderilen mesajların raporunu kaydeder"""
        if self.sent_messages:
            df = pd.DataFrame(self.sent_messages)
            filename = f"linkedin_bot_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False, encoding='utf-8')
            self.log(f"📄 Rapor kaydedildi: {filename}")
        else:
            self.log("ℹ️ Kaydedilecek veri yok")
    
    def close(self):
        """Bot'u kapatır"""
        if self.driver:
            self.driver.quit()
            self.log("🔚 Bot kapatıldı")
    
    def __enter__(self):
        self.log("🔧 Bot context manager başlatılıyor...")
        if not self.setup_driver():
            raise Exception("WebDriver başlatılamadı!")
        self.log("✅ Bot hazır!")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == "__main__":
    # Örnek kullanım
    with LinkedInBot() as bot:
        if bot.setup_driver():
            if bot.login():
                # Yazılım mühendisliği ile ilgili kişilere mesaj gönder
                bot.run_campaign(
                    search_keywords="software engineer",
                    custom_message="Merhaba! Yazılım geliştirme alanında çalışıyorum ve networkinizi genişletmek istiyorum. Bağlantı kurmak ister misiniz?",
                    max_requests=5
                )
                bot.save_report()
