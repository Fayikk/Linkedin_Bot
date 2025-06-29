# LinkedIn Bot

Bu bot, LinkedIn'de yazılım mühendisliği ile ilgili profilleri bulup otomatik olarak bağlantı istekleri göndermenizi sağlar.

## Özellikler

- ✅ LinkedIn'e otomatik giriş
- 🔍 Anahtar kelimeler ile kişi arama
- 📩 Otomatik bağlantı isteği gönderme
- 💬 Özelleştirilebilir mesajlar
- 📊 Detaylı raporlama
- 🛡️ Anti-detection önlemleri
- ⏱️ Rastgele bekleme süreleri

## Kurulum

1. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

2. **Chrome tarayıcısının yüklü olduğundan emin olun**

3. **.env dosyasını düzenleyin:**
```
LINKEDIN_EMAIL=sizin_email@example.com
LINKEDIN_PASSWORD=sizin_sifreniz
DEFAULT_MESSAGE=Merhaba! Yazılım geliştirme alanında çalışıyorum ve deneyimlerinizi öğrenmek istiyorum.
```

## Kullanım

### Basit Kullanım:
```bash
python main.py
```

### Debug ve Test Araçları:

1. **Genel Debug Testi:**
```bash
python debug_test.py
```

2. **Bağlantı Kurma Testi:**
```bash
python test_connection.py
```

3. **Profil Sayfa Analizi:**
```bash
python analyze_profile.py
```

### Programatik Kullanım:
```python
from linkedin_bot import LinkedInBot

with LinkedInBot() as bot:
    if bot.setup_driver():
        if bot.login():
            bot.run_campaign(
                search_keywords="software engineer",
                custom_message="Özel mesajınız",
                max_requests=10
            )
            bot.save_report()
```

## Güvenlik ve Etik Kullanım

⚠️ **ÖNEMLI UYARILAR:**

1. **LinkedIn Kullanım Şartları:** Bu bot'u kullanırken LinkedIn'in kullanım şartlarını ihlal etmediğinizden emin olun.

2. **Oran Sınırları:** Günde çok fazla bağlantı isteği göndermekten kaçının (önerilen: günde max 20-30).

3. **Kişisel Veriler:** Bot, kişisel verileri toplamaz veya saklamaz.

4. **Sorumluluk:** Bu bot'un kullanımından doğacak sorumluluk tamamen kullanıcıya aittir.

## Özelleştirme

### Mesaj Şablonları:
- Varsayılan mesajı `.env` dosyasından değiştirebilirsiniz
- Her kampanya için özel mesaj belirleyebilirsiniz

### Arama Kriterleri:
- Anahtar kelimeler: "software engineer", "developer", "programmer"
- Konum bazlı arama (geliştirilmesi gerekli)

### Bekleme Süreleri:
- Mesajlar arası: 10-15 saniye (önerilen)
- Arama arası: 5-8 saniye

## Dosya Yapısı

```
linkedin_bot/
├── linkedin_bot.py     # Ana bot sınıfı
├── main.py            # Kullanıcı arayüzü
├── requirements.txt   # Gerekli paketler
├── .env              # Konfigürasyon dosyası
└── README.md         # Bu dosya
```

## Rapor Çıktıları

Bot her çalıştırıldığında CSV formatında rapor oluşturur:
- `linkedin_bot_report_YYYYMMDD_HHMMSS.csv`

Rapor içeriği:
- Profil URL'leri
- Gönderilen mesajlar
- Zaman damgaları

## Sorun Giderme

### Chrome Driver Hataları:
- Bot otomatik olarak ChromeDriver'ı indirir
- Chrome tarayıcısının güncel olduğundan emin olun

### Giriş Sorunları:
- `.env` dosyasındaki email/şifre bilgilerini kontrol edin
- LinkedIn'de iki faktörlü kimlik doğrulama kapalı olmalı

### Captcha Sorunları:
- Bot çok hızlı çalışıyorsa bekleme sürelerini artırın
- Manuel olarak giriş yapıp captcha'yı çözün

## Güncelleme Notları

- v1.0: İlk sürüm
- Selenium 4.x ile uyumlu
- Anti-detection özellikleri

## Katkıda Bulunma

Bu proje açık kaynak olarak geliştirilmiştir. Katkılarınızı bekliyoruz!

## Lisans

Bu proje MIT lisansı altında yayınlanmıştır.
