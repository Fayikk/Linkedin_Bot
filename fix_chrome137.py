"""
Chrome 137 için doğru ChromeDriver'ı indir
"""
import os
import requests
import zipfile
import shutil

def download_chrome137_driver():
    """Chrome 137 için uyumlu ChromeDriver'ı indir"""
    try:
        # Chrome 137 için ChromeDriver URL'si
        driver_url = "https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.120/win64/chromedriver-win64.zip"
        
        print(f"📥 Chrome 137 için ChromeDriver indiriliyor...")
        print(f"URL: {driver_url}")
        
        response = requests.get(driver_url)
        if response.status_code == 200:
            # Eski driver'ı temizle
            driver_dir = os.path.join(os.getcwd(), "chromedriver")
            if os.path.exists(driver_dir):
                shutil.rmtree(driver_dir)
            
            os.makedirs(driver_dir, exist_ok=True)
            
            # ZIP dosyasını kaydet
            zip_path = os.path.join(driver_dir, "chromedriver137.zip")
            with open(zip_path, "wb") as f:
                f.write(response.content)
            
            # ZIP'i aç
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(driver_dir)
            
            # ZIP dosyasını sil
            os.remove(zip_path)
            
            # chromedriver.exe dosyasını doğru konuma taşı
            extracted_path = os.path.join(driver_dir, "chromedriver-win64", "chromedriver.exe")
            final_path = os.path.join(driver_dir, "chromedriver.exe")
            
            if os.path.exists(extracted_path):
                shutil.move(extracted_path, final_path)
                # Boş klasörü temizle
                shutil.rmtree(os.path.join(driver_dir, "chromedriver-win64"))
                
                print(f"✅ ChromeDriver 137 başarıyla indirildi: {final_path}")
                return final_path
            else:
                print("❌ ChromeDriver dosyası bulunamadı")
                return None
        else:
            print(f"❌ İndirme başarısız. HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ İndirme hatası: {e}")
        return None

def test_driver(driver_path):
    """Driver'ı test et"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Test başarılı! Sayfa: {title}")
        return True
        
    except Exception as e:
        print(f"❌ Test başarısız: {e}")
        return False

if __name__ == "__main__":
    driver_path = download_chrome137_driver()
    if driver_path:
        test_driver(driver_path)
