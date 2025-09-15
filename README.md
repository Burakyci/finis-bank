# Finiş Bankası - Kapsamlı Türk Bankacılık Uygulaması

**React TypeScript • Firebase • Python • Test Otomasyonu**

---

## İçindekiler

- [Proje Genel Bakış](#proje-genel-bakış)
- [Özellikler](#özellikler)
- [Teknoloji Stack](#teknoloji-stack)
- [Sistem Mimarisi](#sistem-mimarisi)
- [Test Otomasyon Projesi](#test-otomasyon-projesi)
- [Proje Yapısı](#proje-yapısı)
- [Kurulum](#kurulum)
- [Canlı Demo](#canlı-demo)
- [Test Raporları](#test-raporları)

---

## Proje Genel Bakış

**Finiş Bankası**, React TypeScript ve Vite ile geliştirilmiştir.

### Temel Özellikler

- **Güvenli Giriş Sistemi** - Firebase Authentication
- **Detaylı Kayıt** - Finansal profilleme ile
- **Hesap Yönetimi** - Banka hesap detayları
- **Bankacılık Ana Sayfası** - Temalı tasarım
- **AI Destekli Kredi Başvurusu** - Gerçek zamanlı hesaplamalar
- **Risk Değerlendirmesi** - Pure Python algoritmaları

---

## Özellikler

### Kredi Sistemi

- **Sabit %4.09 Faiz Oranı** - Türk bankacılık standartlarına uygun
- **8 Kategorili Skorlama** - Kapsamlı risk analizi
- **DTI Analizi** - Borç/gelir oranı hesaplaması
- **KKDF & BSMV Vergileri** - Otomatik hesaplama
- **Gerçek Zamanlı Sonuçlar** - Anında karar mekanizması

### Kullanıcı Yönetimi

- **Otomatik Hesap Numarası** - XXXX-XXXXXX formatında
- **Güvenli Oturum Yönetimi** - Firebase tabanlı

---

## Teknoloji Stack

### Frontend

| Teknoloji    | Versiyon | Açıklama                 |
| ------------ | -------- | ------------------------ |
| React        | 18.2.0   | UI kütüphanesi           |
| TypeScript   | 4.7.4    | Type güvenliği           |
| Vite         | 3.0.4    | Build aracı              |
| React Router | 7.8.2    | Yönlendirme              |
| Firebase     | 12.2.1   | Authentication & Storage |

### Backend

| Teknoloji          | Versiyon | Açıklama             |
| ------------------ | -------- | -------------------- |
| Python             | 3.13     | Backend dili         |
| Firebase Functions | Latest   | Serverless functions |
| Firebase Admin     | 6.4.0    | Backend Firebase SDK |
| Pure Python Math   | Native   | Risk hesaplamaları   |

### Test Otomasyonu

| Teknoloji     | Versiyon | Açıklama       |
| ------------- | -------- | -------------- |
| Java          | 19       | Test dili      |
| Selenium      | 4.1      | Web otomasyon  |
| TestNG        | 7.4      | Test framework |
| Maven         | 3.9+     | Build yönetimi |
| ExtentReports | 5.1.1    | HTML raporlar  |

---

## Sistem Mimarisi

### Multi-Service Mimarisi

```
┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│   React App     │ │   Python API     │ │    Firebase     │
│   Port: 5000    │◄──►│   Functions      │ │   Auth & DB     │
│   Frontend      │ │   AI Engine      │ │     Cloud       │
└─────────────────┘ └──────────────────┘ └─────────────────┘
```

### Veri Akışı

1. **Kullanıcı Girişi** → Firebase Authentication
2. **Form Verileri** → React State Management
3. **AI Analizi** → Python Firebase Functions
4. **Kredi Kararı** → Pure Python Mathematical Models
5. **Sonuç Gösterimi** → Real-time UI Updates

---

## Test Otomasyon Projesi

### Test Kapsamı

Bu proje, **Finis Bankası Web arayüzü** üzerinde kapsamlı test otomasyonu sağlar. Modern test mühendisliği yaklaşımları kullanılarak **BDD (Behavior Driven Development)** metodolojisi ile geliştirilmiştir.

### Test Senaryoları

- **Mevduat Hesaplama Testleri** - Otomatik hesaplama doğrulama
- **Kredi Hesaplama Testleri** - Kapsamlı kredi hesaplama testleri
- **Ana Sayfa Navigasyonu** - UI ve navigasyon akışı testleri
- **End-to-End Senaryolar** - Giriş'ten işlem tamamlamaya kadar

### Test Mimarisi

#### Design Patterns

- **Page Object Model (POM)** - Sayfa aksiyonları modüler yapıda
- **Helper Classes** - Yeniden kullanılabilir bileşenler
- **Configuration Management** - Esnek ayarlar yönetimi

#### Test Yetenekleri

- **Çapraz Tarayıcı Testleri** - Chrome ve Firefox desteği
- **Görsel Test Raporları** - ExtentReports ile HTML çıktılar
- **Otomatik Ekran Görüntüsü** - Her test adımında screenshot
- **Akıllı Bekleme Stratejileri** - WaitHelper sınıfı ile
- **Scroll Yönetimi** - Otomatik sayfa kaydırma
- **Bankacılık Hesaplamaları** - Kredi hesaplama doğrulamaları

---

## Proje Yapısı

### Frontend Yapısı

```
src/
├── components/           # Yeniden kullanılabilir bileşenler
├── pages/               # Ana sayfa bileşenleri
│   ├── Home.tsx         # Ana sayfa
│   ├── Login.tsx        # Giriş sayfası
│   ├── Register.tsx     # Kayıt sayfası
│   ├── Account.tsx      # Hesap yönetimi
│   └── CreditApplication.tsx # Kredi başvurusu
├── services/            # İş mantığı katmanı
│   ├── creditService.ts # Kredi hesaplamaları
│   ├── formService.ts   # Form yönetimi
│   └── userService.ts   # Kullanıcı işlemleri
├── utils/               # Yardımcı fonksiyonlar
├── hooks/               # Custom React hooks
├── context/             # React Context API
└── config/              # Konfigürasyon dosyaları
```

### Backend Yapısı

```
functions/
├── main.py                    # Ana Firebase Functions
├── models/
│   ├── advanced_scoring.py   # Gelişmiş kredi skorlama
│   └── credit_scoring.py     # Kredi risk analizi
├── utils/
│   └── security.py           # Güvenlik araçları
└── requirements.txt          # Python dependencies
```

### Test Yapısı

```
src/
├── main/java/
│   ├── Base/                    # Temel sınıflar
│   │   ├── BasePage.java
│   │   ├── ExtentManager.java
│   │   └── WebDriverInstance.java
│   ├── helpers/                 # Yardımcı sınıflar
│   │   ├── LoanCalculator.java
│   │   ├── ScrollHelper.java
│   │   └── WaitHelper.java
│   ├── pageObjects/             # Sayfa nesneleri
│   │   ├── Homepage.java
│   │   ├── DepositCalculationPage.java
│   │   └── LoanCalculationPage.java
│   └── drivers/                 # WebDriver dosyaları
└── test/java/test/              # Test sınıfları
    ├── DepositCalculationTest.java
    └── LoanCalculationTest.java
```

---

## Kurulum

### Gereksinimler

- Node.js 18+
- Python 3.13+
- Java 19+ (Test için)
- Maven 3.9+ (Test için)
- Firebase CLI

### Hızlı Başlangıç

#### 1. Proje Klonlama

```bash
git clone [proje-url]
cd finisbank
```

#### 2. Frontend Kurulumu

```bash
npm install
npm run dev
```

#### 3. Backend Kurulumu

```bash
cd functions
pip install -r requirements.txt
```

#### 4. Firebase Deploy

```bash
firebase deploy --only hosting
```

### Test Çalıştırma

```bash
# Maven ile test çalıştırma
mvn clean test

# Belirli test sınıfı çalıştırma
mvn test -Dtest=LoanCalculationTest
```

---

## Canlı Demo

**Canlı Site:** https://finisbank.web.app

### Demo Hesapları

- **Email:** test@test.com
- **Şifre:** asdasd

## Test Raporları

### Test Metrikleri

### Rapor Formatları

- **HTML Raporları** - ExtentReports ile detaylı görsel raporlar
- **Screenshot Dokümantasyonu** - Her test adımında görsel kanıt
- **Test Execution Analytics** - Kapsamlı analiz verileri
