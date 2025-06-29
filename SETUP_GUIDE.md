# 🤖 LinkedIn Bot Kurulum Rehberi

LinkedIn bot'unuzu kullanmaya başlamadan önce aşağıdaki adımları takip edin:

## 1. Kurulum Kontrolü ✅
- Python 3.7+ yüklü olmalı
- Chrome tarayıcısı yüklü olmalı
- Gerekli paketler yüklendi ✅

## 2. LinkedIn Hesap Ayarları 🔐

### Önemli Güvenlik Ayarları:
1. LinkedIn hesabınızda **iki faktörlü kimlik doğrulamayı KAPATIN**
2. **Email/şifre** girişini tercih edin
3. Güçlü bir şifre kullanın

### .env Dosyasını Düzenleyin:
```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
DEFAULT_MESSAGE=Merhaba! Yazılım geliştirme alanında çalışıyorum ve deneyimlerinizi öğrenmek istiyorum.
```

## 3. Bot'u Çalıştırın 🚀

### Basit Kullanım:
```bash
python main.py
```

### Test Modu:
```bash
python examples.py
```

## 4. Güvenlik Önerileri ⚠️

- **Günlük Limit**: Maksimum 20-30 bağlantı isteği
- **Bekleme Süreleri**: Bot otomatik olarak 10-15 saniye bekler
- **Kişisel Mesajlar**: Her kampanya için özel mesaj yazın
- **Hedef Kitle**: Sadece alakalı profillere mesaj gönderin

## 5. Sorun Giderme 🔧

### ChromeDriver Sorunu:
Bot otomatik olarak Chrome driver'ı indirir. Chrome güncel olmalı.

### Giriş Sorunu:
- Email/şifre kontrolü yapın
- LinkedIn'de captcha var mı kontrol edin
- 2FA kapalı olduğundan emin olun

### Captcha Problemi:
- Bot'u yavaşlatın (bekleme sürelerini artırın)
- Manuel giriş yapıp captcha'yı çözün

## 6. Örnek Kullanım Senaryoları 📝

### Yazılım Mühendisleri:
```python
bot.run_campaign(
    search_keywords="software engineer",
    custom_message="Merhaba! Yazılım geliştirme alanında çalışıyorum.",
    max_requests=10
)
```

### Frontend Developerlar:
```python
bot.run_campaign(
    search_keywords="frontend developer",
    custom_message="Frontend teknolojileri hakkında konuşmak isterim.",
    max_requests=5
)
```

## 7. Etik Kullanım 🤝

- **Spam yapmayın**: Kaliteli, kişisel mesajlar gönderin
- **Sınırları aşmayın**: LinkedIn'in kullanım şartlarına uyun
- **Saygılı olun**: Reddedileni tekrar mesaj atmayın
- **İçerik kalitesi**: Değerli bağlantılar kurmaya odaklanın

## 8. Bot Özellikleri 🎯

✅ Otomatik giriş
✅ Anahtar kelime bazlı arama
✅ Özelleştirilebilir mesajlar
✅ Anti-detection önlemleri
✅ Detaylı raporlama
✅ Rastgele bekleme süreleri
✅ Context manager desteği

## 9. Sonuç Raporları 📊

Bot her çalıştıktan sonra CSV raporu oluşturur:
- Gönderilen mesajların listesi
- Profil URL'leri
- Zaman damgaları

## 10. Desteklenen Arama Terimleri 🔍

- "software engineer"
- "yazılım mühendisi" 
- "frontend developer"
- "backend developer"
- "full stack developer"
- "data scientist"
- "DevOps engineer"
- "machine learning engineer"

---

⚠️ **DİKKAT**: Bu bot'u kullanırken LinkedIn'in kullanım şartlarına uygun davranın. Hesabınızın askıya alınması riski vardır.

✅ **BAŞARILAR**: Professional networkinizi genişletmek için bu bot'u akıllıca kullanın!
