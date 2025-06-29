# 🤖 LinkedIn Bot - Gelişmiş Otomatik Bağlantı Sistemi

LinkedIn'de otomatik arama, profil bulma ve bağlantı isteği gönderme işlemlerini gerçekleştiren gelişmiş Python botu.

## ✨ Özellikler

### 🔧 Otomatik Kurulum
- **Chrome ve ChromeDriver otomatik kurulumu**
- **Python paketlerinin otomatik yüklenmesi**  
- **Tek tıkla kurulum sistemi**
- **Platform bağımsız çalışma (Windows, macOS, Linux)**

### 🤖 Bot Özellikleri
- **Akıllı arama**: Anahtar kelimelerle kişi arama
- **Filtreli profil tarama**: Sadece "Bağlantı kur" butonlu profiller
- **Özel mesaj desteği**: Kişiselleştirilmiş bağlantı istekleri
- **Güvenli gecikme sistemi**: LinkedIn limitlerine uygun bekleme
- **Captcha ve güvenlik kontrol desteği**

### 🖥️ Kullanıcı Arayüzleri
- **Modern Web GUI**: Tarayıcı tabanlı şık arayüz
- **Gerçek zamanlı loglar**: Canlı durum takibi  
- **İstatistik paneli**: Başarı/başarısızlık oranları
- **Ayar yönetimi**: Kolay konfigürasyon
- **Rapor indirme**: CSV formatında sonuç raporları

## 🚀 Hızlı Başlangıç

### 1. Otomatik Kurulum (Önerilen)

```bash
# 1. Projeyi indirin
git clone [repository-url]
cd Linkedin_Bot

# 2. Otomatik kurulumu başlatın
start_bot.bat  # Windows için
# veya
python auto_installer.py  # Tüm platformlar için
```

### 2. Manuel Kurulum

```bash
# Python paketlerini yükle
pip install -r requirements.txt

# .env dosyasını düzenle
cp .env.example .env
# Email, şifre ve diğer ayarları .env'e ekleyin

# Web arayüzünü başlat
python web_gui.py
```

## ⚙️ Konfigürasyon

`.env` dosyasında aşağıdaki ayarları düzenleyin:

```env
# LinkedIn Giriş Bilgileri
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# Bot Ayarları  
DEFAULT_MESSAGE=Merhaba! LinkedIn'de bağlantı kurmak isterim.
MAX_PROFILES_PER_SESSION=50
DELAY_BETWEEN_MESSAGES=10
DELAY_BETWEEN_SEARCHES=5

# ChromeDriver (Opsiyonel)
CHROMEDRIVER_PATH=/path/to/chromedriver
```

## 🌐 Web Arayüzü Kullanımı

1. **Kurulum Kontrolü**: Bot otomatik olarak Chrome/ChromeDriver kurulumunu kontrol eder
2. **Ayar Girişi**: Arama anahtar kelimeleri, mesaj ve limit belirleyin  
3. **Kampanya Başlatma**: "Başlat" butonuyla otomatik süreci başlatın
4. **Canlı Takip**: Gerçek zamanlı loglar ve istatistikleri izleyin
5. **Rapor İndirme**: İşlem tamamlandığında sonuçları CSV olarak indirin

## 📱 Platform Desteği

### Windows
- Otomatik Chrome kurulumu
- .bat dosyası ile kolay başlatma
- ChromeDriver otomatik sürüm yönetimi

### macOS  
- Manuel Chrome kurulum rehberi
- Homebrew desteği (gelecek güncellemede)
- Terminal tabanlı kurulum

### Linux/Ubuntu
- APT tabanlı Chrome kurulumu  
- Headless mod optimizasyonları
- Server deployment desteği

## 🔒 Güvenlik ve Limitler

### LinkedIn Güvenlik Önlemleri
- **Captcha Desteği**: Otomatik captcha algılama ve bekletme
- **IP Kontrolü**: Farklı IP'lerden giriş uyarıları
- **Email Doğrulama**: Güvenlik email'lerinin algılanması

### Bot Güvenlik Özellikleri
- **Akıllı Gecikmeler**: İnsan benzeri davranış simülasyonu
- **Anti-Detection**: Tarayıcı parmak izi gizleme
- **Rate Limiting**: LinkedIn API limitlerini aşmama

### Önerilen Limitler
- **Günlük Bağlantı**: En fazla 100-150 kişi
- **Saatlik Limit**: En fazla 20-30 kişi  
- **Mesaj Arası Bekleme**: 8-15 saniye
- **Arama Arası Bekleme**: 3-7 saniye

## 🚨 Önemli Uyarılar

⚠️ **LinkedIn Kullanım Şartları**: Bu bot eğitim amaçlıdır. Ticari kullanımdan önce LinkedIn'in Terms of Service'ini inceleyin.

⚠️ **Hesap Güvenliği**: Botunuzu makul limitlerde kullanın. Aşırı kullanım hesap kısıtlaması yaratabilir.

⚠️ **Kişisel Veriler**: .env dosyanızda hassas bilgiler bulunur. Bu dosyayı paylaşmayın.

## 📊 İstatistikler ve Raporlama

Bot aşağıdaki metrikleri takip eder:
- **Bulunan Profiller**: Arama sonuçlarında çıkan toplam profil sayısı
- **İşlenen Profiller**: Detay sayfası ziyaret edilen profil sayısı  
- **Başarılı Bağlantılar**: Mesaj gönderilen profil sayısı
- **Başarısız Denemeler**: Hata alan veya bağlantı kurulamayan profiller
- **Süre**: Toplam kampanya süresi

## 🛠️ Gelişmiş Özellikler

### Profil Filtreleme
- Sadece "Bağlantı kur" butonlu profiller
- Premium hesap sahipleri önceliği
- Lokasyon bazlı filtreleme (gelecek)
- Sektör bazlı filtreleme (gelecek)

### Mesaj Kişiselleştirme  
- Profil adı otomatik ekleme
- Şirket bilgisi entegrasyonu (gelecek)
- A/B test mesaj sistemi (gelecek)

### Raporlama ve Analiz
- CSV export desteği
- Grafik tabanlı istatistikler (gelecek)
- Kampanya performans analizi (gelecek)

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 📞 Destek

Sorularınız için:
- GitHub Issues: Bug raporları ve özellik istekleri
- Discussions: Genel sorular ve tartışmalar

---

**Son Güncelleme**: 29 Aralık 2025  
**Sürüm**: 2.0.0 (Client-Side Edition)
