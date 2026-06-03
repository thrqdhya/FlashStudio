import sys
import os

# 1. Biarkan baris penambah path ini berada di atas terlebih dahulu
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, redirect, flash

# 2. PINDAHKAN semua import business_layer ke bawah baris sys.path.append
from business_layer.cekim_paketi_service import CekimPaketiService
from business_layer.musteri_service import MusteriService
from business_layer.ekipman_service import EkipmanService
from business_layer.kiralama_service import KiralamaService
from business_layer.rezervasyon_service import RezervasyonService
from business_layer.fotografci_service import FotografciService

app = Flask(__name__)
app.secret_key = "flash_studio_secret_key"

@app.route('/')
def index():
    return redirect('/musteri')

# --- MÜŞTERİ ---
@app.route('/musteri')
def musteri_sayfasi():
    tum_musteriler = MusteriService.tum_musterileri_listele()
    return render_template('musteri.html', musteriler=tum_musteriler)

@app.route('/musteri/ekle', methods=['POST'])
def musteri_ekle_aksiyon():
    ad = request.form.get('ad')
    soyad = request.form.get('soyad')
    telefon = request.form.get('telefon')
    eposta = request.form.get('eposta')
    adres = request.form.get('adres')
    basarili, mesaj = MusteriService.yeni_musteri_kaydet(ad, soyad, telefon, eposta, adres)
    flash(mesaj, "success" if basarili else "danger")
    return redirect('/musteri')

# --- EKİPMAN ---
@app.route('/ekipman')
def ekipman_sayfasi():
    list_ekipman = EkipmanService.tum_ekipmanlari_listele()
    return render_template('ekipman.html', ekipmanlar=list_ekipman)

@app.route('/ekipman/ekle', methods=['POST'])
def ekipman_ekle_aksiyon():
    ad = request.form.get('ad')
    kategori = request.form.get('kategori')
    fiyat = request.form.get('fiyat')
    stok = request.form.get('stok')
    birim = request.form.get('birim')
    detay = request.form.get('detay')
    basarili, mesaj = EkipmanService.yeni_ekipman_kaydet(ad, kategori, fiyat, stok, birim, detay)
    flash(mesaj, "success" if basarili else "danger")
    return redirect('/ekipman')

@app.route('/ekipman/sil/<int:id>')
def ekipman_sil_aksiyon(id):
    basarili, mesaj = EkipmanService.m_ekipman_sil(id)
    flash(mesaj, "success" if basarili else "danger")
    return redirect('/ekipman')

# --- KİRALAMA ---
@app.route('/kiralama')
def kiralama_sayfasi():
    # Mengambil data pelanggan dari Service Layer
    list_musteri = MusteriService.tum_musterileri_listele()
    
    # Mengirimkan variabel 'musteriler' ke file kiralama.html
    return render_template('kiralama.html', musteriler=list_musteri)

@app.route('/kiralama/ekle', methods=['POST'])
def kiralama_ekle_aksiyon():
    musteri_id = request.form.get('musteri_id') or request.form.get('musteri_seci')
    baslangic_tarihi = request.form.get('baslangic_tarihi')
    bitis_tarihi = request.form.get('bitis_tarihi')
    toplam_tutar = request.form.get('toplam_tutar') or request.form.get('kira_bedeli')

    try:
        # Memanggil service penyewaan kamu
        KiralamaService.kiralama_ekle(musteri_id, baslangic_tarihi, bitis_tarihi, toplam_tutar)
        flash("Kiralama işlemi başarıyla başlatıldı.", "success")
    except Exception as e:
        flash(f"Hata oluştu: {str(e)}", "danger")

    return redirect('/kiralama')  # Mengembalikan pengguna ke halaman utama sewa

# --- REZERVASYON ---
@app.route('/rezervasyon')
def rezervasyon_sayfasi():
    # 1. Ambil data pelanggan
    list_musteri = MusteriService.tum_musterileri_listele()
    
    # 2. Ambil data fotografer
    list_fotografci = FotografciService.tum_fotografcilari_listele()
    
    # KUNCI PERBAIKAN: Ambil data paket pemotretan asli dari database!
    # (Sesuaikan nama Service dan fungsinya dengan yang ada di proyekmu, misal: CekimPaketiService)
    list_paket = CekimPaketiService.tum_cekim_paketlerini_listele() 
    
    # 3. Ambil data rencana reservasi
    list_rezervasyon = RezervasyonService.tum_rezervasyonlari_getir()
    
    # 4. Kirim semua data ke file HTML (Pastikan variabel 'paketler' ikut dikirim)
    return render_template(
        'rezervasyon.html', 
        musteriler=list_musteri, 
        fotografcilar=list_fotografci,
        paketler=list_paket, # Mengirimkan data paket ke dropdown Çekim Paketi
        rezervasyonlar=list_rezervasyon
    )

@app.route('/rezervasyon/ekle', methods=['POST'])
def rezervasyon_ekle_aksiyon():
    musteri_id = request.form.get('musteri_id')
    fotografci_id = request.form.get('fotografci_id')
    paket_id = request.form.get('paket_id')
    tarih = request.form.get('tarih')
    toplam = request.form.get('toplam')
    odenen = request.form.get('odenen')

    # PENANGANAN TEGAS: Jika opsi default '-- İsteğe Bağlı Fotoğrafçı --' dipilih, 
    # atau nilainya kosong, kita paksa diubah menjadi None (NULL)
    if not fotografci_id or fotografci_id.strip() == "" or fotografci_id == "None" or "seçiniz" in fotografci_id.lower() or "isteğe" in fotografci_id.lower():
        fotografci_id = None

    basarili, mesaj = RezervasyonService.yeni_rezervasyon_kaydet(
        musteri_id, fotografci_id, paket_id, tarih, toplam, odenen
    )
    
    flash(mesaj, "success" if basarili else "danger")
    return redirect('/rezervasyon')

# --- FOTOĞRAFÇI (YENİ) ---
@app.route('/fotografci')
def fotografci_sayfasi():
    list_fotografci = FotografciService.tum_fotografcilari_listele()
    return render_template('fotografci.html', fotografcilar=list_fotografci)

@app.route('/fotografci/ekle', methods=['POST'])
def fotografci_ekle_aksiyon():
    ad = request.form.get('ad')
    soyad = request.form.get('soyad')
    uzmanlik = request.form.get('uzmanlik')
    telefon = request.form.get('telefon')
    basarili, mesaj = FotografciService.yeni_fotografci_kaydet(ad, soyad, uzmanlik, telefon)
    flash(mesaj, "success" if basarili else "danger")
    return redirect('/fotografci')

if __name__ == '__main__':
    app.run(debug=True)