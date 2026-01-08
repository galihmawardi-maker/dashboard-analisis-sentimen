# Dashboard Analisis Sentimen

Dashboard interaktif untuk visualisasi analisis sentimen menggunakan Streamlit.

## Fitur

- Upload file CSV hasil analisis sentimen
- Visualisasi distribusi sentimen (Pie Chart & Bar Chart)
- Word Cloud untuk sentimen positif dan negatif
- Statistik lengkap data sentimen
- Download hasil analisis

## Cara Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/galihmawardi-maker/dashboard-analisis-sentimen.git
cd dashboard-analisis-sentimen
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Cara Menjalankan

Jalankan perintah berikut di terminal:

```bash
streamlit run app.py
```

Dashboard akan terbuka di browser pada alamat `http://localhost:8501`

## Format File CSV

File CSV yang diupload harus memiliki kolom:
- **sentiment** atau **Sentiment** atau **sentimen**: Kolom yang berisi label sentimen (contoh: positive, negative)
- **text** atau **komentar** (opsional): Kolom yang berisi teks untuk membuat Word Cloud

## Cara Menggunakan

1. Buka dashboard di browser
2. Upload file CSV melalui sidebar kiri
3. Dashboard akan otomatis menampilkan:
   - Preview data
   - Statistik sentimen
   - Grafik distribusi sentimen
   - Word Cloud (jika ada kolom text)
4. Anda bisa download hasil analisis dalam format CSV

## Requirements

- streamlit
- pandas
- plotly
- wordcloud
- matplotlib
