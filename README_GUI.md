# 🤖 LinkedIn Bot - Gelişmiş GUI Versiyonu

URL tabanlı sayfalama ile gelişmiş LinkedIn otomasyonu. **3 farklı arayüz seçeneği** ile kullanıcı dostu deneyim.

## 🚀 Özellikler

### 🎯 Bot Özellikleri:
- ✅ **URL tabanlı sayfalama** - Her sayfada doğrudan arama
- ✅ **Gelişmiş profil tespiti** - "Bağlantı kur" butonlarını akıllıca bulur
- ✅ **Özel mesajlar** - Kişiselleştirilmiş bağlantı istekleri
- ✅ **Duplikasyon önleme** - Aynı kişiye birden fazla istek gönderme engeli
- ✅ **CSV raporlama** - Detaylı sonuç raporları
- ✅ **1000 kişiye kadar** - Yüksek kapasiteli işlem

### 🖥️ Arayüz Seçenekleri:

#### 1. 🖼️ **Desktop GUI (Tkinter)**
- Modern masaüstü arayüzü
- Gerçek zamanlı loglar
- Görsel durum takibi
- Form tabanlı kolay ayarlama

#### 2. 🌐 **Web GUI (Flask)**
- Tarayıcı tabanlı arayüz
- Responsive tasarım
- Canlı güncellemeler (Socket.IO)
- Modern Bootstrap tasarımı
- Uzaktan erişim desteği

#### 3. 🖥️ **Konsol Arayüzü**
- Terminal tabanlı klasik arayüz
- Hafif ve hızlı
- Server ortamları için ideal

## 📦 Kurulum

### 1. Depoyu İndirin
```bash
git clone <repository-url>
cd Linkedin_Bot
```

### 2. Gereksinimler
```bash
pip install -r requirements.txt
```

### 3. Chrome WebDriver
Bot otomatik olarak Chrome WebDriver'ı indirir ve kurar.

## 🎮 Kullanım

### Launcher ile Başlat (Önerilen)
```bash
python launcher.py
```
Bu size tüm arayüz seçeneklerini sunar.

### Ayrı Ayrı Başlatma

#### Desktop GUI:
```bash
python gui_app.py
# veya
start_gui.bat
```

#### Web GUI:
```bash
python web_gui.py
# veya
start_web_gui.bat
```

#### Konsol:
```bash
python main.py
```

## ⚙️ Konfigürasyon

### .env Dosyası:
```env
# LinkedIn Bot Konfigürasyonu
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# Mesaj şablonu
DEFAULT_MESSAGE=Merhaba! Bağlantı kurmak istiyorum.

# Bot ayarları
SEARCH_KEYWORDS=software engineer,developer,programmer
MAX_PROFILES_PER_SESSION=1000
DELAY_BETWEEN_MESSAGES=10
DELAY_BETWEEN_SEARCHES=5
```

## 📊 Arayüz Karşılaştırması

| Özellik | Desktop GUI | Web GUI | Konsol |
|---------|-------------|---------|--------|
| **Kullanım Kolaylığı** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Görsel Arayüz** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| **Uzaktan Erişim** | ❌ | ✅ | ❌ |
| **Sistem Kaynakları** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Canlı Updates** | ✅ | ✅ | ✅ |
| **Mobil Uyumlu** | ❌ | ✅ | ❌ |

## 🌐 Web GUI Özellikleri

### 🎨 Modern Tasarım:
- Bootstrap 5 tabanlı responsive arayüz
- Gradient renkler ve animasyonlar
- Font Awesome ikonları
- Karanlık tema log alanı

### 📊 Gerçek Zamanlı İzleme:
- Canlı durum güncellemeleri
- Progress bar ile ilerleme takibi
- İstatistik kartları
- Socket.IO ile anlık mesajlaşma

### 📱 Çok Platform Desteği:
- Windows, Mac, Linux
- Masaüstü tarayıcıları
- Mobil tarayıcılar
- Tablet optimizasyonu

## 🧪 Test Seçenekleri

### Hızlı Test:
```bash
python quick_test.py
```
1 kişiye mesaj gönderir - bot fonksiyonlarını test eder.

### Kapsamlı Test:
```bash
python comprehensive_test.py
```
3 kişiye mesaj gönderir - tam operasyon testi.

## 📋 Raporlar

Tüm bot aktiviteleri CSV formatında raporlanır:
- Tarih/saat damgaları
- Profil bilgileri
- Başarı/başarısızlık durumu
- Gönderilen mesajlar

## 🔒 Güvenlik

- Şifreler lokal olarak saklanır
- Rate limiting ile LinkedIn kurallarına uyum
- Captcha tespiti ve manuel müdahale
- Güvenli bağlantı istekleri

## 🚀 Deployment (Canlıya Alma)

### Web GUI için Server Deployment:

1. **VPS/Server Kurulumu:**
```bash
# Server'da
git clone <repository>
cd Linkedin_Bot
pip install -r requirements.txt
```

2. **Production Çalıştırma:**
```bash
# Güvenli port ve host ile
python web_gui.py
```

3. **SSL ve Domain:**
- Nginx reverse proxy
- SSL sertifikası
- Domain bağlama

### 🌍 Uzaktan Erişim:
Web GUI sayesinde botunuzu:
- Evden ofisteki bilgisayarda çalıştırabilir
- Sunucuda 7/24 çalıştırabilir
- Mobil cihazdan kontrol edebilirsiniz

## 🛠️ Hata Giderme

### Chrome Driver Sorunları:
```bash
python fix_chrome137.py
```

### Port Çakışması (Web GUI):
`web_gui.py` dosyasında port değiştirin:
```python
socketio.run(app, debug=False, host='0.0.0.0', port=5001)
```

### Gereksinimler Hatası:
```bash
pip install --upgrade -r requirements.txt
```

## 📞 Destek

- 🐛 Bug raporları: GitHub Issues
- 💡 Öneriler: GitHub Discussions
- 📖 Dokümantasyon: README.md

## 📄 Lisans

MIT License - Kişisel ve ticari kullanım için serbest.

---

**🎉 LinkedIn Bot artık 3 farklı arayüzle hazır!**
**En iyi deneyim için Web GUI'yi deneyin: `python launcher.py` → Seçenek 3**
