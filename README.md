Finiş Bankası - Kapsamlı Türk Bankacılık Uygulaması
React TypeScript • Firebase • Python AI • Test Otomasyonu

📋 İçindekiler
🏦 Proje Genel Bakış
🚀 Özellikler
⚙️ Teknoloji Stack
🏗️ Sistem Mimarisi
🧪 Test Otomasyon Projesi
📁 Proje Yapısı
🔧 Kurulum
🌐 Canlı Demo
📊 Test Raporları
🏦 Proje Genel Bakış
Finiş Bankası, React TypeScript ve Vite ile geliştirilmiş kapsamlı bir Türk bankacılık uygulamasıdır. Uygulama Firebase authentication, varsayılan dark mode, otomatik banka hesabı oluşturma ve Türkçe dil desteği ile tam bir kullanıcı yönetim sistemi sunar.

✨ Temel Özellikler
🔐 Güvenli Giriş Sistemi - Firebase Authentication
📝 Detaylı Kayıt - Finansal profilleme ile
💳 Hesap Yönetimi - Banka hesap detayları
🏠 Bankacılık Ana Sayfası - Temalı tasarım
🤖 AI Destekli Kredi Başvurusu - Gerçek zamanlı hesaplamalar
📊 Risk Değerlendirmesi - Machine learning algoritmaları
🌙 Dark Mode - Varsayılan olarak aktif
🇹🇷 Türkçe Arayüz - Tam Türkçe dil desteği
🚀 Özellikler
💰 Kredi Sistemi
Sabit %4.09 Faiz Oranı - Türk bankacılık standartlarına uygun
8 Kategorili Skorlama - Kapsamlı risk analizi
DTI Analizi - Borç/gelir oranı hesaplaması
KKDF & BSMV Vergileri - Otomatik hesaplama
Gerçek Zamanlı Sonuçlar - Anında karar mekanizması
👤 Kullanıcı Yönetimi
Otomatik Hesap Numarası - XXXX-XXXXXX formatında
TL Para Birimi - Türk Lirası desteği
Güvenli Oturum Yönetimi - Firebase tabanlı
Profil Yönetimi - Detaylı kullanıcı bilgileri
⚙️ Teknoloji Stack
🎨 Frontend
Teknoloji Versiyon Açıklama
React 18.2.0 UI kütüphanesi
TypeScript 4.7.4 Type güvenliği
Vite 3.0.4 Build aracı
React Router 7.8.2 Yönlendirme
Firebase 12.2.1 Authentication & Storage
🐍 Backend
Teknoloji Versiyon Açıklama
Python 3.13 Backend dili
FastAPI Latest Modern API framework
Pandas Latest Veri analizi
NumPy Latest Sayısal hesaplamalar
Scikit-learn Latest Machine learning
Uvicorn Latest ASGI server
🧪 Test Otomasyonu
Teknoloji Versiyon Açıklama
Java 19 Test dili
Selenium 4.1 Web otomasyon
TestNG 7.4 Test framework
Maven 3.9+ Build yönetimi
ExtentReports 5.1.1 HTML raporlar
🏗️ Sistem Mimarisi
🌐 Multi-Service Mimarisi
┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ React App │ │ Python API │ │ Firebase │
│ Port: 5000 │◄──►│ Port: 8000 │ │ Auth & DB │
│ Frontend │ │ AI Engine │ │ Cloud │
└─────────────────┘ └──────────────────┘ └─────────────────┘
🔄 Veri Akışı
Kullanıcı Girişi → Firebase Authentication
Form Verileri → React State Management
AI Analizi → Python FastAPI + Pandas
Kredi Kararı → Machine Learning Modelleri
Sonuç Gösterimi → Real-time UI Updates
🧪 Test Otomasyon Projesi
📊 Test Kapsamı
Bu proje, Finis Bankası Web arayüzü üzerinde kapsamlı test otomasyonu sağlar. Modern test mühendisliği yaklaşımları kullanılarak BDD (Behavior Driven Development) metodolojisi ile geliştirilmiştir.

🎯 Test Senaryoları
✅ Mevduat Hesaplama Testleri - Otomatik hesaplama doğrulama
✅ Kredi Hesaplama Testleri - Kapsamlı kredi hesaplama testleri
✅ Ana Sayfa Navigasyonu - UI ve navigasyon akışı testleri
✅ End-to-End Senaryolar - Giriş'ten işlem tamamlamaya kadar
🏗️ Test Mimarisi
Design Patterns
Page Object Model (POM) - Sayfa aksiyonları modüler yapıda
Helper Classes - Yeniden kullanılabilir bileşenler
Configuration Management - Esnek ayarlar yönetimi
Test Yetenekleri
Çapraz Tarayıcı Testleri - Chrome ve Firefox desteği
Görsel Test Raporları - ExtentReports ile HTML çıktılar
Otomatik Ekran Görüntüsü - Her test adımında screenshot
Akıllı Bekleme Stratejileri - WaitHelper sınıfı ile
Scroll Yönetimi - Otomatik sayfa kaydırma
Bankacılık Hesaplamaları - Kredi hesaplama doğrulamaları
📁 Proje Yapısı
🎨 Frontend Yapısı
src/
├── components/ # Yeniden kullanılabilir bileşenler
├── pages/ # Ana sayfa bileşenleri
│ ├── Home.tsx # Ana sayfa
│ ├── Login.tsx # Giriş sayfası
│ ├── Register.tsx # Kayıt sayfası
│ ├── Account.tsx # Hesap yönetimi
│ └── CreditApplication.tsx # Kredi başvurusu
├── services/ # İş mantığı katmanı
│ ├── creditService.ts # Kredi hesaplamaları
│ ├── formService.ts # Form yönetimi
│ └── userService.ts # Kullanıcı işlemleri
├── utils/ # Yardımcı fonksiyonlar
├── hooks/ # Custom React hooks
├── context/ # React Context API
└── config/ # Konfigürasyon dosyaları
🧪 Test Yapısı
src/
├── main/java/
│ ├── Base/ # Temel sınıflar
│ │ ├── BasePage.java
│ │ ├── ExtentManager.java
│ │ └── WebDriverInstance.java
│ ├── helpers/ # Yardımcı sınıflar
│ │ ├── LoanCalculator.java
│ │ ├── ScrollHelper.java
│ │ └── WaitHelper.java
│ ├── pageObjects/ # Sayfa nesneleri
│ │ ├── Homepage.java
│ │ ├── DepositCalculationPage.java
│ │ └── LoanCalculationPage.java
│ └── drivers/ # WebDriver dosyaları
└── test/java/test/ # Test sınıfları
├── DepositCalculationTest.java
└── LoanCalculationTest.java
🔧 Kurulum
📦 Gereksinimler
Node.js 18+
Python 3.13+
Java 19+ (Test için)
Maven 3.9+ (Test için)
Firebase CLI
⚡ Hızlı Başlangıç
1️⃣ Proje Klonlama
git clone [proje-url]
cd finisbank
2️⃣ Frontend Kurulumu
npm install
npm run dev
3️⃣ Backend Kurulumu
cd functions
pip install -r requirements.txt
python main.py
4️⃣ Firebase Deploy
firebase deploy --only hosting
🧪 Test Çalıştırma

# Maven ile test çalıştırma

mvn clean test

# Belirli test sınıfı çalıştırma

mvn test -Dtest=LoanCalculationTest
🌐 Canlı Demo
🔗 Canlı Site: https://finisbank.web.app

🔑 Demo Hesapları
Email: demo@finisbank.com
Şifre: demo123456
💳 Test Verileri
TCKN: 12345678901
Gelir: 15000 TL
Kredi Tutarı: 50000 TL
📊 Test Raporları
📈 Test Metrikleri
✅ Başarı Oranı: %95+
🧪 Test Senaryoları: 25+ adet
📱 Desteklenen Tarayıcılar: Chrome, Firefox
⏱️ Ortalama Test Süresi: 3-5 dakika
📄 Rapor Formatları
HTML Raporları - ExtentReports ile detaylı görsel raporlar
Screenshot Dokümantasyonu - Her test adımında görsel kanıt
Test Execution Analytics - Kapsamlı analiz verileri
🤝 Katkı Sağlama
Fork edin
Feature branch oluşturun (git checkout -b feature/YeniOzellik)
Commit yapın (git commit -m 'Yeni özellik eklendi')
Push edin (git push origin feature/YeniOzellik)
Pull Request açın
📧 İletişim
Proje Sahibi: Burak Kalaycı
Email: burakkalayci6718@gmail.com

📄 Lisans
Bu proje MIT Lisansı altında lisanslanmıştır.

⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın! ⭐
