import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Sentimen",
    page_icon="📊",
    layout="wide"
)

# Judul
st.title("📊 Dashboard Analisis Sentimen")
st.markdown("---")

# Upload file
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload file CSV hasil analisis sentimen",
    type=['csv']
)

if uploaded_file is not None:
    # Baca data
    df = pd.read_csv(uploaded_file)
    
    # Sidebar info
    st.sidebar.success(f"✅ File berhasil diupload!")
    st.sidebar.info(f"Total data: {len(df)} baris")
    
    # Tampilkan data
    st.subheader("📋 Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Cek kolom sentimen
    sentiment_col = None
    for col in ['sentiment', 'Sentiment', 'sentimen', 'Sentimen', 'label', 'Label']:
        if col in df.columns:
            sentiment_col = col
            break
    
    if sentiment_col:
        # Statistik sentimen
        st.subheader("📈 Statistik Sentimen")
        
        col1, col2, col3 = st.columns(3)
        
        sentiment_counts = df[sentiment_col].value_counts()
        
        with col1:
            st.metric("Total Data", len(df))
        
        with col2:
            if 'positive' in sentiment_counts.index or 'Positive' in sentiment_counts.index:
                pos = sentiment_counts.get('positive', sentiment_counts.get('Positive', 0))
                st.metric("Sentimen Positif", pos)
        
        with col3:
            if 'negative' in sentiment_counts.index or 'Negative' in sentiment_counts.index:
                neg = sentiment_counts.get('negative', sentiment_counts.get('Negative', 0))
                st.metric("Sentimen Negatif", neg)
        
        # Grafik pie chart
        st.subheader("🥧 Distribusi Sentimen")
        fig_pie = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Proporsi Sentimen",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Grafik bar chart
        st.subheader("📊 Grafik Batang Sentimen")
        fig_bar = px.bar(
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            labels={'x': 'Sentimen', 'y': 'Jumlah'},
            title="Jumlah per Sentimen",
            color=sentiment_counts.index,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # WordCloud (jika ada kolom text)
        text_col = None
        for col in ['text', 'Text', 'komentar', 'Komentar', 'review', 'Review', 'full_text', 'clean_text']:
            if col in df.columns:
                text_col = col
                break
        
        if text_col:
            st.subheader("☁️ Word Cloud")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Positive wordcloud
                positive_data = df[df[sentiment_col].str.lower().str.contains('positive', na=False)]
                if len(positive_data) > 0:
                    text_positive = ' '.join(positive_data[text_col].astype(str).tolist())
                    if text_positive.strip():
                        wordcloud_pos = WordCloud(width=800, height=400, background_color='white').generate(text_positive)
                        fig_pos, ax_pos = plt.subplots(figsize=(10, 5))
                        ax_pos.imshow(wordcloud_pos, interpolation='bilinear')
                        ax_pos.axis('off')
                        ax_pos.set_title('Word Cloud - Sentimen Positif')
                        st.pyplot(fig_pos)
            
            with col2:
                # Negative wordcloud
                negative_data = df[df[sentiment_col].str.lower().str.contains('negative', na=False)]
                if len(negative_data) > 0:
                    text_negative = ' '.join(negative_data[text_col].astype(str).tolist())
                    if text_negative.strip():
                        wordcloud_neg = WordCloud(width=800, height=400, background_color='white').generate(text_negative)
                        fig_neg, ax_neg = plt.subplots(figsize=(10, 5))
                        ax_neg.imshow(wordcloud_neg, interpolation='bilinear')
                        ax_neg.axis('off')
                        ax_neg.set_title('Word Cloud - Sentimen Negatif')
                        st.pyplot(fig_neg)
        
        # Tabel lengkap
        st.subheader("📄 Data Lengkap")
        st.dataframe(df, use_container_width=True)
        
        # Download hasil
        st.subheader("💾 Download Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="hasil_analisis_sentimen.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Kolom sentimen tidak ditemukan. Pastikan file CSV memiliki kolom 'sentiment' atau 'Sentiment'.")
        st.info("Kolom yang tersedia: " + ", ".join(df.columns.tolist()))
else:
    st.info("👈 Silakan upload file CSV di sidebar untuk memulai analisis.")
    st.markdown("""
    ### Cara Menggunakan:
    1. Upload file CSV hasil analisis sentimen dari sidebar
    2. Dashboard akan otomatis menampilkan visualisasi data
    3. File CSV harus memiliki minimal kolom 'sentiment' atau 'Sentimen'
    4. Untuk Word Cloud, file harus memiliki kolom text/komentar
    """)
