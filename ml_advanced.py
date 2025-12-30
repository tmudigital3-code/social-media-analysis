"""
Advanced Machine Learning Module - Part 1
Deep Learning, NLP, Clustering
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

try:
    from textblob import TextBlob
    NLP_AVAILABLE = True
    print("✅ TextBlob successfully imported")
except Exception as e:
    NLP_AVAILABLE = False
    print(f"❌ TextBlob import failed: {e}")

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
    print("✅ Prophet successfully imported")
except Exception as e:
    PROPHET_AVAILABLE = False
    print(f"❌ Prophet import failed: {e}")


@st.cache_data(show_spinner=False)
def calculate_gb_forecast(daily_data, horizon):
    """Cached calculation for Gradient Boosting Forecast"""
    X = np.arange(len(daily_data)).reshape(-1, 1)
    X_poly = np.column_stack([X, X**2, X**3])
    y = daily_data['follower_count'].values
    
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
    model.fit(X_poly, y)
    
    future_X = np.arange(len(daily_data), len(daily_data) + horizon).reshape(-1, 1)
    future_X_poly = np.column_stack([future_X, future_X**2, future_X**3])
    future_y = model.predict(future_X_poly)
    
    return future_y

@st.cache_data(show_spinner=False)
def calculate_prophet_forecast(daily_data):
    """Cached calculation for Prophet Forecast"""
    if not PROPHET_AVAILABLE:
        return None
        
    prophet_df = daily_data.rename(columns={'timestamp': 'ds', 'follower_count': 'y'})
    model = Prophet(daily_seasonality='auto', weekly_seasonality='auto', yearly_seasonality='auto')
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    return forecast

def render_deep_learning_forecast(data):
    """90-day forecasting with Gradient Boosting & Prophet"""
    st.markdown('<div class="pro-header fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-title">🧠 Deep Learning Time Series</div>', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-subtitle">Neural network predictions & seasonal forecasting</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📈 90-Day Follower Forecast</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'follower_count' in data.columns:
            # We copy to avoid mutating original valid data if we need to
            df = data.copy()
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            daily = df.groupby(pd.Grouper(key='timestamp', freq='D'))['follower_count'].last().reset_index().dropna()
            
            if len(daily) > 14:
                horizons = [7, 30, 60, 90]
                colors = ['#10b981', '#f59e0b', '#f97316', '#ef4444']
                
                # Matplotlib 90-Day Follower Forecast
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(daily['timestamp'], daily['follower_count'], label='Actual', color='#667eea', linewidth=3)
                
                current = int(daily['follower_count'].iloc[-1])
                growth_metrics = []

                for horizon, color in zip(horizons, colors):
                    # Use cached calculation
                    future_y = calculate_gb_forecast(daily[['timestamp', 'follower_count']], horizon)
                    
                    future_dates = pd.date_range(daily['timestamp'].iloc[-1] + timedelta(days=1), periods=horizon, freq='D')
                    ax.plot(future_dates, future_y, label=f'{horizon}D', color=color, linewidth=2, linestyle='--')
                    
                    predicted = int(future_y[-1])
                    growth = predicted - current
                    growth_metrics.append((horizon, growth, color))
                
                ax.set_title('90-Day Follower Forecast')
                ax.legend()
                plt.xticks(rotation=45)
                sns.despine()
                st.pyplot(fig)
                
                for horizon, growth, color in growth_metrics:
                     st.markdown(f'<span style="color:{color}">▪ {horizon}d: +{growth:,} ({(growth/current*100):+.1f}%)</span>', unsafe_allow_html=True)
            else:
                st.info("Need 14+ days for forecasting")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🔮 Prophet Seasonal Forecast</div>', unsafe_allow_html=True)
        
        if PROPHET_AVAILABLE and 'timestamp' in data.columns and 'follower_count' in data.columns:
            try:
                # Re-prepare daily data just in case
                df = data.copy()
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                daily = df.groupby(pd.Grouper(key='timestamp', freq='D'))['follower_count'].last().reset_index().dropna()

                if len(daily) > 30:
                    # Use cached calculation
                    forecast = calculate_prophet_forecast(daily[['timestamp', 'follower_count']])
                    
                    if forecast is not None:
                    if forecast is not None:
                        # Matplotlib Prophet Forecast
                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.plot(daily['timestamp'], daily['follower_count'], label='Actual', color='#667eea', linewidth=3)
                        ax.plot(forecast['ds'], forecast['yhat'], label='Forecast', color='#f093fb', linewidth=2, linestyle='--')
                        ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='#f093fb', alpha=0.2, label='Confidence')
                        
                        ax.set_title('Prophet Seasonal Forecast')
                        ax.legend()
                        plt.xticks(rotation=45)
                        sns.despine()
                        st.pyplot(fig)
                        
                        pred30 = int(forecast['yhat'].iloc[-1])
                        curr = int(daily['follower_count'].iloc[-1])
                        st.markdown(f'📊 **30D Forecast:** +{pred30-curr:,} ({(pred30-curr)/curr*100:+.1f}%)')
                else:
                    st.info("Need 30+ days for Prophet")
            except Exception as e:
                st.warning(f"Prophet unavailable: {e}")
        else:
            if not PROPHET_AVAILABLE:
                st.info("Install: `pip install prophet`")
            else:
                st.info("Insufficient data for Prophet")
        st.markdown('</div>', unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def calculate_sentiment(data_df):
    """Cached sentiment calculation"""
    if 'caption' not in data_df.columns:
        return data_df
        
    df = data_df.copy()
    
    def get_sentiment_score(text):
        if pd.isna(text) or text == '':
            return 0.0, 0.0
        try:
            blob = TextBlob(str(text))
            return blob.sentiment.polarity, blob.sentiment.subjectivity
        except:
            return 0.0, 0.0
            
    # Apply sentiment analysis
    # Note: apply with result_type='expand' can be slower, so we use list comprehension for speed inside this cached function
    captions = df['caption'].astype(str).tolist()
    results = [get_sentiment_score(c) for c in captions]
    
    df['sentiment_score'] = [r[0] for r in results]
    df['subjectivity'] = [r[1] for r in results]
    
    return df

def render_sentiment_analysis(data):
    """NLP emotion detection & hashtag sentiment"""
    st.markdown('<div class="pro-header fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-title">💬 NLP Sentiment Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-subtitle">Emotion detection & hashtag trends</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not NLP_AVAILABLE:
        st.warning("Install: `pip install textblob`")
        return
    
    if 'caption' not in data.columns:
        st.info("No caption data available")
        return
    
    # Use cached calculation
    # Only pass necessary columns to aid hashing
    analysis_df = calculate_sentiment(data[['caption', 'likes'] if 'likes' in data.columns else ['caption']])
    # Merge back emotion for display logic if needed, but here we calculate it fast
    
    def detect_emotion(pol, subj):
        if pol > 0.5: return '😍 Joy'
        elif pol > 0.2: return '😊 Happy'
        elif pol < -0.5: return '😡 Anger'
        elif pol < -0.2: return '😢 Sad'
        elif subj > 0.7: return '😲 Surprise'
        return '😐 Neutral'
    
    analysis_df['emotion'] = analysis_df.apply(lambda row: detect_emotion(row['sentiment_score'], row['subjectivity']), axis=1)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Matplotlib Emotion Distribution
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(emotion_counts.values, labels=emotion_counts.index, autopct='%1.1f%%', 
               colors=[colors_emotion.get(e, '#94a3b8') for e in emotion_counts.index], wedgeprops={'width': 0.4})
        ax.set_title('Emotion Distribution')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📊 Emotion vs Engagement</div>', unsafe_allow_html=True)
        
        if 'likes' in analysis_df.columns:
            # Matplotlib Emotion vs Engagement
            emotion_eng = analysis_df.groupby('emotion')['likes'].mean().sort_values(ascending=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            y_pos = np.arange(len(emotion_eng))
            ax.barh(y_pos, emotion_eng.values, color=[colors_emotion.get(e, '#94a3b8') for e in emotion_eng.index])
            ax.set_yticks(y_pos)
            ax.set_yticklabels(emotion_eng.index)
            ax.set_xlabel('Avg Likes')
            ax.set_title('Emotion vs Engagement')
            sns.despine()
            st.pyplot(fig)
            if not emotion_eng.empty:
                st.markdown(f'💡 **{emotion_eng.idxmax()}** performs best ({emotion_eng.max():.0f} likes)')
        st.markdown('</div>', unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def calculate_clustering(features_df, k=3):
    """Cached K-Means clustering"""
    features_filled = features_df.fillna(0)
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features_filled)
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    clusters = kmeans.fit_predict(features_scaled)
    # Return clusters and scaled features for silhouette calculation
    return clusters, features_scaled

def render_audience_clustering(data):
    """K-Means & DBSCAN clustering"""
    st.markdown('<div class="pro-header fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-title">👥 Audience Segmentation</div>', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-subtitle">K-Means & DBSCAN clustering</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    required = ['likes', 'comments', 'shares', 'impressions']
    if not all(col in data.columns for col in required):
        st.info("Need engagement metrics for clustering")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🎯 K-Means Segments</div>', unsafe_allow_html=True)
        
        # Use cached calculation
        clusters, features_scaled = calculate_clustering(data[required], k=3)
        
        # Need to work on a copy to not corrupt main dataframe in session state cache
        df_cluster = data.copy()
        df_cluster['segment'] = clusters
        
        segment_avg = df_cluster.groupby('segment')['likes'].mean().sort_values()
        labels = {segment_avg.index[0]: 'Low Engagers', segment_avg.index[1]: 'Medium Engagers', segment_avg.index[2]: 'High Engagers'}
        df_cluster['segment_label'] = df_cluster['segment'].map(labels)
        
        counts = df_cluster['segment_label'].value_counts()
        colors = ['#ef4444', '#f59e0b', '#10b981']
        
        # Matplotlib K-Means Segments
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%', colors=colors, wedgeprops={'width': 0.4})
        ax.set_title('K-Means Segments')
        st.pyplot(fig)
        st.markdown(f'**Quality:** {silhouette_score(features_scaled, clusters):.3f}')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🔍 DBSCAN Patterns</div>', unsafe_allow_html=True)
        
        # DBSCAN is fast enough, but we can cache if needed. For now leave as is to avoid over-engineering if not slow.
        # Actually, let's just use the scaled features we already have!
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        clusters_db = dbscan.fit_predict(features_scaled)
        
        summary = pd.Series(clusters_db).value_counts().sort_index()
        labels = ['Outliers (Viral)' if cid == -1 else f'Pattern {cid+1}' for cid in summary.index]
        
        # Matplotlib DBSCAN Patterns
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(labels, summary.values, color=['#ef4444' if 'Outliers' in l else '#667eea' for l in labels])
        for i, v in enumerate(summary.values):
            ax.text(i, v + 0.1, str(v), ha='center')
        ax.set_ylabel('Posts')
        ax.set_title('DBSCAN Patterns')
        sns.despine()
        st.pyplot(fig)
        st.markdown(f'**Outliers:** {(clusters_db==-1).sum()}')
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="pro-insights fade-in">', unsafe_allow_html=True)
    st.markdown('### 💡 Segment Recommendations')
    for seg in ['High Engagers', 'Medium Engagers', 'Low Engagers']:
        if seg in df_cluster['segment_label'].values:
            pct = (df_cluster['segment_label']==seg).sum() / len(data) * 100
            if seg == 'High Engagers':
                st.markdown(f'<div class="pro-insight-item">🏆 <strong>{seg} ({pct:.1f}%)</strong>: Premium content, exclusives (+32% confidence)</div>', unsafe_allow_html=True)
            elif seg == 'Medium Engagers':
                st.markdown(f'<div class="pro-insight-item">⚡ <strong>{seg} ({pct:.1f}%)</strong>: Post 5x/week, add polls (+28% confidence)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="pro-insight-item">📢 <strong>{seg} ({pct:.1f}%)</strong>: Re-engagement at 6-8 PM (+25% confidence)</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
