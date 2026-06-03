# FlashStudio Pro - Fotoğraf Stüdyosu Otomasyon Sistemi

FlashStudio Pro, bir fotoğraf stüdyosunun müşteri yönetimini, ekipman kiralamalarını, fotoğrafçı kadrosunu ve rezervasyon planlamalarını uçtan uca yönetmek için geliştirilmiş katmanlı mimariye (N-Tier Architecture) sahip bir otomasyon sistemidir. 

Bu proje, **BTS304 Veritabanı Yönetim Sistemleri** dersi final uygulaması olarak geliştirilmiştir.

---

## 🛠️ Kullanılan Teknolojiler

* **Frontend (Sunum Katmanı):** HTML5, CSS3, Bootstrap 5, FontAwesome (Arayüz bileşenleri için)
* **Backend (İş Mantığı Katmanı):** Python 3.13 & Flask Framework
* **Veritabanı Katmanı:** Microsoft SQL Server (MS SQL) & `pyodbc` sürücüsü

---

## 📐 Proje Mimarisi (N-Tier Architecture)

Proje, kodun sürdürülebilirliği ve güvenliği açısından 3 temel katmana ayrılmıştır:

1.  **Presentation Layer (Sunum Katmanı - `presentation_layer`):** Flask rotalarının (`app.py`) ve HTML şablonlarının (`templates/`) yer aldığı, kullanıcı etkileşimini yöneten katman.
2.  **Business Layer (İş Mantığı Katmanı - `business_layer`):** Verilerin iş kurallarına göre kontrol edildiği ve DAL katmanı ile sunum katmanı arasında köprü görevi gören servis katmanı (`musteri_service.py`, `rezervasyon_service.py` vb.).
3.  **Data Access Layer (Veri Erişim Katmanı - `data_access_layer`):** Veritabanı bağlantısının kurulduğu (`db_connection.py`) ve SQL sorgularının/Stored Procedure'lerin ham olarak çalıştırıldığı katman (`rezervasyon_dal.py`, `cekim_paketi_dal.py` vb.).

---

## 🗄️ Gelişmiş Veritabanı Özellikleri (Advanced DB Features)

Projenin temel amacı olan veritabanı yönetim sistemleri yetkinliklerini göstermek adına SQL Server tarafında şu gelişmiş yapılar aktif olarak entegre edilmiştir:

### 1. Stored Procedures (Saklı Yordamlar)
Uygulama içerisindeki tüm CRUD ve listeleme işlemleri ham SQL sorguları yerine güvenli ve optimize edilmiş Stored Procedure'ler üzerinden yürütülür:
* `sp_RezervasyonEkle`: Formdan gelen verilerle yeni rezervasyon kaydeder.
* `sp_RezervasyonDetay`: İlişkili tabloları (Müşteri, Fotoğrafçı, Paket) `JOIN` ile birleştirerek detaylı analiz tablosunu besler.
* `sp_CekimPaketiEkle`: Dinamik çekim paketlerini sisteme dahil eder.

### 2. Database Triggers (Tetikleyiciler)
* `trg_EkipmanDurumGuncelle`: Bir ekipman kiralama işlemi başlatıldığında (`Kiralama İşlemleri`), ilgili ekipmanın durumunu otomatik olarak veritabanı seviyesinde **'Kirada'** moduna çeker.
* `trg_FotografciCakismaKontrol`: Aynı fotoğrafçının aynı tarih ve saatte iki farklı rezervasyona atanmasını engelleyen iş kuralı tetikleyicisi.

---

## 🚀 Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone [https://github.com/USERNAME_KAMU/FlashStudioProject.git](https://github.com/USERNAME_KAMU/FlashStudioProject.git)
    cd FlashStudioProject
    ```

2.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Veritabanı Bağlantısını Yapılandırın:**
    `data_access_layer/db_connection.py` dosyası içerisindeki `SERVER`, `DATABASE` ve bağlantı dizesini yerel SQL Server (SSMS) bilgilerinize göre güncelleyin.

4.  **Uygulamayı Başlatın:**
    ```bash
    python presentation_layer/app.py
    ```
    Uygulama başlatıldıktan sonra tarayıcınızdan `http://127.0.0.1:5000` adresine giderek otomasyon sistemini test edebilirsiniz.
