import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Sentimen",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dark Glassmorphism
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(26, 26, 46, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Cards with Glass Effect */
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 0 0 20px rgba(123, 47, 247, 0.5);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(120deg, #00d4ff, #7b2ff7);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(123, 47, 247, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(123, 47, 247, 0.6);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px 20px;
        color: #fff;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(120deg, #00d4ff, #7b2ff7);
</style>
""", unsafe_allow_html=True)


# Judul
st.markdown('<h1 class="main-header">📊 Dashboard Analisis Sentimen Program MBG</h1>', unsafe_allow_html=True)
st.markdown("---")

# Upload file
st.sidebar.header("📁 Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload file CSV hasil analisis sentimen",
    type=['csv'],
    help="File CSV harus memiliki kolom sentiment atau sentiment_label"
)

if uploaded_file is not None:
    # Baca data
    df = pd.read_csv(uploaded_file)
    
    # Sidebar info
    st.sidebar.success(f"✅ File berhasil diupload!")
    st.sidebar.metric("📄 Total Data", f"{len(df):,} baris")
    
    # Cek kolom sentimen
    sentiment_col = None
    for col in ['sentiment', 'Sentiment', 'sentimen', 'Sentimen', 'label', 'Label', 'sentiment_label']:
        if col in df.columns:
            sentiment_col = col
            break
    
    if sentiment_col:
        # Convert timestamp jika ada
        if 'timestamp' in df.columns:
            try:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['date'] = df['timestamp'].dt.date
                df['hour'] = df['timestamp'].dt.hour
            except:
                pass
        
        # Tabs untuk organisasi konten
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Overview",
            "📊 Visualisasi",
            "☁️ Word Cloud",
            "🔍 Analisis Detail",
            "📄 Data"
        ])
        
        with tab1:
            st.header("📈 Overview Sentimen")
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            sentiment_counts = df[sentiment_col].value_counts()
            total = len(df)
            
            with col1:
                st.metric("📄 Total Data", f"{total:,}")
            
            with col2:
                pos = sentiment_counts.get('positive', sentiment_counts.get('Positive', 0))
                pct = (pos/total*100) if total > 0 else 0
                st.metric("✅ Sentimen Positif", f"{pos:,}", f"{pct:.1f}%")
            
            with col3:
                neg = sentiment_counts.get('negative', sentiment_counts.get('Negative', 0))
                pct = (neg/total*100) if total > 0 else 0
                st.metric("❌ Sentimen Negatif", f"{neg:,}", f"{pct:.1f}%")
            
            with col4:
                if 'confidence_score' in df.columns:
                    avg_conf = df['confidence_score'].mean()
                    st.metric("🎯 Confidence Avg", f"{avg_conf:.2%}")
                else:
                    st.metric("📊 Unique Users", f"{df['user_handle'].nunique():,}" if 'user_handle' in df.columns else "N/A")
            
            st.markdown("---")
            
            # Pie chart dan bar chart side by side
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🥧 Proporsi Sentimen")
                fig_pie = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    title="Distribusi Sentimen",
                    color_discrete_sequence=['#2ecc71', '#e74c3c'],
                    hole=0.4
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.subheader("📊 Jumlah per Sentimen")
                fig_bar = px.bar(
                    x=sentiment_counts.index,
                    y=sentiment_counts.values,
                    labels={'x': 'Sentimen', 'y': 'Jumlah'},
                    title="Komparasi Sentimen",
                    color=sentiment_counts.index,
                    color_discrete_sequence=['#2ecc71', '#e74c3c']
                )
                fig_bar.update_layout(showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
        
        with tab2:
            st.header("📊 Visualisasi Lanjutan")
            
            # Time series jika ada timestamp
            if 'date' in df.columns:
                st.subheader("📅 Trend Sentimen Harian")
                daily_sentiment = df.groupby(['date', sentiment_col]).size().reset_index(name='count')
                fig_time = px.line(
                    daily_sentiment,
                    x='date',
                    y='count',
                    color=sentiment_col,
                    title="Trend Sentimen dari Waktu ke Waktu",
                    labels={'date': 'Tanggal', 'count': 'Jumlah Tweet'},
                    color_discrete_map={'positive': '#2ecc71', 'negative': '#e74c3c'}
                )
                st.plotly_chart(fig_time, use_container_width=True)
            
            # Top users jika ada
            if 'user_handle' in df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("👥 Top 10 Users Paling Aktif")
                    top_users = df['user_handle'].value_counts().head(10)
                    fig_users = px.bar(
                        x=top_users.values,
                        y=top_users.index,
                        orientation='h',
                        labels={'x': 'Jumlah Tweet', 'y': 'User'},
                        title="Users Ter aktif",
                        color=top_users.values,
                        color_continuous_scale='Blues'
                    )
                    fig_users.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_users, use_container_width=True)
                
                with col2:
                    if 'likes' in df.columns:
                        st.subheader("❤️ Top 10 Tweet Terpopuler")
                        top_tweets = df.nlargest(10, 'likes')[['user_handle', 'likes', sentiment_col]]
                        fig_likes = px.bar(
                            top_tweets,
                            x='likes',
                            y='user_handle',
                            orientation='h',
                            color=sentiment_col,
                            labels={'likes': 'Likes', 'user_handle': 'User'},
                            title="Tweet dengan Likes Terbanyak",
                            color_discrete_map={'positive': '#2ecc71', 'negative': '#e74c3c'}
                        )
                        fig_likes.update_layout(yaxis={'categoryorder':'total ascending'})
                        st.plotly_chart(fig_likes, use_container_width=True)
            
            # Confidence score distribution
            if 'confidence_score' in df.columns:
                st.subheader("🎯 Distribusi Confidence Score")
                fig_conf = px.histogram(
                    df,
                    x='confidence_score',
                    color=sentiment_col,
                    nbins=50,
                    title="Distribusi Confidence Score per Sentimen",
                    labels={'confidence_score': 'Confidence Score'},
                    color_discrete_map={'positive': '#2ecc71', 'negative': '#e74c3c'}
                )
                st.plotly_chart(fig_conf, use_container_width=True)
        
        with tab3:
            st.header("☁️ Word Cloud Analisis")
            
            text_col = None
            for col in ['text_clean', 'text', 'Text', 'komentar', 'Komentar', 'review', 'Review', 'text_raw']:
                if col in df.columns:
                    text_col = col
                    break
            
            if text_col:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("✅ Word Cloud - Sentimen Positif")
                    positive_data = df[df[sentiment_col].str.lower().str.contains('positive', na=False)]
                    if len(positive_data) > 0:
                        text_positive = ' '.join(positive_data[text_col].astype(str).tolist())
                        if text_positive.strip():
                            wordcloud_pos = WordCloud(
                                width=800,
                                height=400,
                                background_color='white',
                                colormap='Greens',
                                max_words=100
                            ).generate(text_positive)
                            fig_pos, ax_pos = plt.subplots(figsize=(10, 5))
                            ax_pos.imshow(wordcloud_pos, interpolation='bilinear')
                            ax_pos.axis('off')
                            st.pyplot(fig_pos)
                    else:
                            ax_pos.imshow(wordcloud_pos.to_array(), interpolation='bilinear')                
                with col2:
                    st.subheader("❌ Word Cloud - Sentimen Negatif")
                    negative_data = df[df[sentiment_col].str.lower().str.contains('negative', na=False)]
                    if len(negative_data) > 0:
                        text_negative = ' '.join(negative_data[text_col].astype(str).tolist())
                        if text_negative.strip():
                            wordcloud_neg = WordCloud(
                                width=800,
                                height=400,
                                background_color='white',
                                colormap='Reds',
                                max_words=100
                            ).generate(text_negative)
                            fig_neg, ax_neg = plt.subplots(figsize=(10, 5))
                            ax_neg.imshow(wordcloud_neg, interpolation='bilinear')
                            ax_neg.axis('off')
                            st.pyplot(fig_neg)
                    else:
                            ax_neg.imshow(wordcloud_neg.to_array(), interpolation='bilinear')                st.warning("⚠️ Kolom teks tidak ditemukan untuk membuat Word Cloud")
        
        with tab4:
            st.header("🔍 Analisis Detail")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'likes' in df.columns and 'retweets' in df.columns:
                    st.subheader("📊 Engagement Metrics")
                    engagement = df.groupby(sentiment_col)[['likes', 'retweets', 'replies']].mean()
                    fig_eng = go.Figure(data=[
                        go.Bar(name='Likes', x=engagement.index, y=engagement['likes']),
                        go.Bar(name='Retweets', x=engagement.index, y=engagement['retweets']),
                        go.Bar(name='Replies', x=engagement.index, y=engagement['replies'] if 'replies' in df.columns else [0]*len(engagement))
                    ])
                    fig_eng.update_layout(barmode='group', title="Rata-rata Engagement per Sentimen")
                    st.plotly_chart(fig_eng, use_container_width=True)
            
            with col2:
                if 'hour' in df.columns:
                    st.subheader("🕒 Aktifitas per Jam")
                    hourly = df.groupby('hour').size().reset_index(name='count')
                    fig_hour = px.bar(
                        hourly,
                        x='hour',
                        y='count',
                        labels={'hour': 'Jam', 'count': 'Jumlah Tweet'},
                        title="Distribusi Tweet per Jam",
                        color='count',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig_hour, use_container_width=True)
            
            # Sample tweets
            st.subheader("💬 Sample Tweets")
            sentiment_filter = st.selectbox("Pilih Sentimen", ['All'] + list(df[sentiment_col].unique()))
            
            if sentiment_filter == 'All':
                sample_df = df.sample(min(10, len(df)))
            else:
                sample_df = df[df[sentiment_col] == sentiment_filter].sample(min(10, len(df[df[sentiment_col] == sentiment_filter])))
            
            if text_col:
                for idx, row in sample_df.iterrows():
                    with st.expander(f"{row['user_handle'] if 'user_handle' in df.columns else 'User'} - {row[sentiment_col]}"):
                        st.write(row[text_col])
                        if 'likes' in df.columns:
                            col1, col2, col3 = st.columns(3)
                            col1.metric("❤️ Likes", row['likes'])
                            col2.metric("🔁 Retweets", row['retweets'] if 'retweets' in df.columns else 0)
                            col3.metric("💬 Replies", row['replies'] if 'replies' in df.columns else 0)
        
        with tab5:
            st.header("📄 Data Lengkap")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                sentiment_filter_data = st.multiselect(
                    "Filter Sentimen",
                    options=list(df[sentiment_col].unique()),
                    default=list(df[sentiment_col].unique())
                )
            
            with col2:
                n_rows = st.slider("Jumlah Baris", 10, len(df), min(100, len(df)))
            
            # Filtered data
            filtered_df = df[df[sentiment_col].isin(sentiment_filter_data)].head(n_rows)
            st.dataframe(filtered_df, use_container_width=True, height=400)
            
            # Download
            st.subheader("💾 Download Data")
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📄 Download Full CSV",
                    data=csv,
                    file_name="sentiment_analysis_full.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                filtered_csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📊 Download Filtered CSV",
                    data=filtered_csv,
                    file_name="sentiment_analysis_filtered.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    else:
        st.warning("⚠️ Kolom sentimen tidak ditemukan!")
        st.info(f"Kolom yang tersedia: {', '.join(df.columns.tolist())}")
        st.markdown("""
        File CSV harus memiliki salah satu kolom berikut:
        - `sentiment`
        - `Sentiment`
        - `sentiment_label`
        - `label`
        """)
else:
    st.info("👈 Silakan upload file CSV di sidebar untuk memulai analisis.")
    
    st.markdown("""
    ## 📚 Panduan Penggunaan
    
    ### 1. Format File CSV
    File CSV yang diupload harus memiliki minimal kolom berikut:
    - **sentiment** / **sentiment_label**: Kolom berisi label sentimen (positive/negative)
    - **text** / **text_clean** (opsional): Teks untuk Word Cloud
    
    ### 2. Kolom Opsional untuk Fitur Tambahan:
    - **timestamp**: Untuk analisis trend waktu
    - **user_handle**: Untuk analisis user
    - **likes, retweets, replies**: Untuk analisis engagement
    - **confidence_score**: Untuk analisis kepercayaan model
    
    ### 3. Fitur Dashboard:
    - 📈 **Overview**: Statistik umum dan distribusi sentimen
    - 📊 **Visualisasi**: Trend, top users, engagement
    - ☁️ **Word Cloud**: Visualisasi kata paling sering muncul
    - 🔍 **Analisis Detail**: Metrics dan sample data
    - 📄 **Data**: Tabel lengkap dan download
    
    ### 4. Tips:
    - Gunakan file CSV hasil dari analisis sentimen
    - Pastikan encoding UTF-8 untuk karakter Indonesia
    - Maksimal ukuran file 200MB
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📊 Dashboard Analisis Sentimen Program MBG | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

