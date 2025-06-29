# 🤖 LinkedIn Bot - URL Tabanlı Gelişmiş Versiyon

Bu LinkedIn botu, **URL tabanlı sayfalama** ile gelişmiş LinkedIn otomasyonu sağlar. Bot direkt LinkedIn arama URL'lerine giderek her sayfada "Bağlantı kur" butonlu kullanıcıları tespit eder ve özel mesajlarla bağlantı istekleri gönderir.

## 🌟 Yeni Özellikler

### ✨ URL Tabanlı Sayfalama
- Direkt LinkedIn arama URL'sine gidiş (`/search/results/people/?keywords=...&page=N`)
- Sayfa numarasıyla istenen sayfaya doğrudan erişim
- Daha stabil ve hızlı sayfa geçişi

### 🎯 Akıllı Profil Tespiti
- Her sayfada "Bağlantı kur" butonlu kullanıcıları otomatik tespit
- Çoklu dil desteği (Türkçe/İngilizce)
- Profil bilgilerini (isim, URL) otomatik toplama

### 📨 Gelişmiş Mesaj Sistemi
- Hem arama sayfasından hem de profil sayfasından mesaj gönderme
- "Not ekle" modalı ile özel mesaj ekleme
- Mesajsız hızlı bağlantı isteği seçeneği

### 🔧 Kapsamlı Test Araçları
- URL tabanlı arama testi (`test_url_search.py`)
- Sayfalama mantığı testi (`test_pagination.py`) 
- Debug modu ile sayfa analizi
- Profil toplama testi (mesaj göndermez)

## 📁 Dosya Yapısı

```
linkedin_bot/
├── linkedin_bot.py           # Ana bot sınıfı (URL tabanlı)
├── main.py                   # Gelişmiş ana arayüz
├── requirements.txt          # Python paketleri
├── .env                     # Konfigürasyon
├── README.md                # Bu dosya
├── SETUP_GUIDE.md          # Kurulum rehberi
├── test_url_search.py       # URL arama testi
├── test_pagination.py       # Sayfalama testi
├── debug_test.py           # Debug araçları
├── final_test.py           # Toplu test
└── webdriver_fixer.py      # Driver otomatik düzeltme
```

## 🚀 Hızlı Başlangıç

### 1. Kurulum
```bash
pip install -r requirements.txt
```

### 2. Konfigürasyon
`.env` dosyasını düzenleyin:
```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
DEFAULT_MESSAGE=Merhaba! Yazılım geliştirme alanında çalışıyorum. Udemy kurslarım: https://www.udemy.com/user/your-profile/
SEARCH_KEYWORDS=software engineer,cloud engineer,developer
MAX_PROFILES_PER_SESSION=1000
DELAY_BETWEEN_MESSAGES=30
```

### 3. Çalıştırma
```bash
python main.py
```

## 🎮 Ana Menü Seçenekleri

```
🤖 LinkedIn Bot - URL Tabanlı Gelişmiş Versiyon
1. 🚀 Normal kampanya (URL tabanlı sayfalama)
2. 📄 Belirli sayfadan başlayarak kampanya  
3. 🧪 Test modu (1 kişiye mesaj)
4. 📋 Konfigürasyon ayarlarını görüntüle
5. 🔧 Debug modu (sayfa analizi)
6. 📊 Sadece profil toplama (mesaj göndermez)
7. 🚪 Çıkış
```

### 🔥 Seçenek 1: Normal Kampanya
- URL tabanlı arama ile sayfalama
- İstenen sayıda kişiye otomatik mesaj
- Ayrıntılı ilerleme raporlama

### 📄 Seçenek 2: Belirli Sayfadan Başlama
- 3. sayfa, 5. sayfa gibi belirli bir sayfadan başlama
- Daha önce işlenmiş sayfaları atlama
- Hedefli kampanya yürütme

### 🔧 Seçenek 5: Debug Modu
- Sayfa analizi ve profil tespiti
- Buton durumlarını kontrol etme
- Sorun giderme için ayrıntılı bilgi

### 📊 Seçenek 6: Profil Toplama
- Sadece profil bilgilerini toplama
- Mesaj göndermeden test etme
- Kampanya öncesi profil kalitesi kontrolü

## 🧪 Test Araçları

### URL Arama Testi
```bash
python test_url_search.py
```
- Tek sayfa URL tabanlı arama testi
- Bağlanabilir profil tespiti
- Buton analizi ve debug bilgileri

### Sayfalama Testi  
```bash
python test_pagination.py
```
- Çoklu sayfa test etme
- Her sayfa için profil sayısı raporlama
- Sayfa kalitesi analizi

### Debug Test
```bash
python debug_test.py
```
- Kapsamlı sistem testi
- Adım adım işlem kontrolü
- Hata ayıklama araçları

## ⚙️ Yeni Bot Mantığı

### 1. URL Tabanlı Arama
```python
# Eski yöntem: Arama kutusuna yazma
# bot.search_people("software engineer")

# Yeni yöntem: Direkt URL'ye gitme
bot.search_people("software engineer", page=3)
# https://www.linkedin.com/search/results/people/?keywords=software+engineer&page=3
```

### 2. Akıllı Profil Tespiti
```python
# Her sayfada "Bağlantı kur" butonlu profilleri bul
connectable_profiles = bot.find_connectable_profiles()

# Profil verisi:
{
    'name': 'Ahmet Yılmaz',
    'url': 'https://linkedin.com/in/ahmet-yilmaz',
    'button': selenium_button_element,
    'card_index': 2
}
```

### 3. Gelişmiş Kampanya
```python
# URL tabanlı sayfalı kampanya
bot.run_campaign(
    search_keywords="cloud engineer",
    custom_message="Merhaba! Cloud teknolojileri...",
    max_requests=15,
    start_page=2  # 2. sayfadan başla
)
```

## 📊 Raporlama

Bot, gönderilen her mesaj için ayrıntılı rapor oluşturur:

```csv
profile_url,profile_name,message,timestamp,method
https://linkedin.com/in/user1,John Doe,Custom message here,2024-01-15 14:30:25,search_page
https://linkedin.com/in/user2,Jane Smith,Custom message here,2024-01-15 14:32:10,profile_page
```

## 🔒 Güvenlik Özellikleri

- **Rastgele Beklemeler**: İnsan benzeri davranış
- **Captcha Tespiti**: Güvenlik kontrolü algılama
- **Rate Limiting**: LinkedIn limitlerini aşmama
- **Error Handling**: Robust hata yönetimi

## 🚨 Önemli Notlar

1. **LinkedIn Politikaları**: LinkedIn'in kullanım şartlarına uygun kullanın
2. **Günlük Limitler**: Günde maksimum 50-100 bağlantı isteği önerilir
3. **Kişisel Hesap**: Profesyonel LinkedIn hesabı kullanın
4. **Mesaj Kalitesi**: Spam olmayan, değerli içerik gönderin

## 🔧 Sorun Giderme

### Chrome 137+ Uyumluluk
```bash
python webdriver_fixer.py
```

### Manuel Driver Ayarlama
`.env` dosyasına ekleyin:
```env
CHROME_DRIVER_PATH=C:\path\to\chromedriver.exe
USE_MANUAL_DRIVER=true
```

### Hata Ayıklama
1. `debug_test.py` çalıştırın
2. Browser'da manuel kontrol yapın
3. Console loglarını kontrol edin
4. `.env` konfigürasyonunu doğrulayın

## 📈 Performans İpuçları

1. **Arama Terimleri**: Spesifik ve hedefli terimler kullanın
2. **Sayfa Seçimi**: 1-5 sayfalar genelde en iyi sonuçları verir
3. **Mesaj Kalitesi**: Kişiselleştirilmiş, değerli mesajlar gönderin
4. **Zamanlama**: İş saatleri dışında çalıştırın

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Yeni feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Pull request gönderin

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. README ve SETUP_GUIDE'ı kontrol edin
2. Test scriptlerini çalıştırın
3. Debug modu ile analiz yapın
4. Issue açın (GitHub üzerinde)

---

**⚡ URL Tabanlı LinkedIn Otomasyonu ile Daha Hızlı ve Etkili Networking!**
