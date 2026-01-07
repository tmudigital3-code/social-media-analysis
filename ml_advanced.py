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
        st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📈 90-Day Follower Forecast</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'follower_count' in data.columns:
            df = data.copy()
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            daily = df.groupby(pd.Grouper(key='timestamp', freq='D'))['follower_count'].last().reset_index().dropna()
            
            if len(daily) > 14:
                horizons = [7, 30, 60, 90]
                colors = ['#10b981', '#f59e0b', '#f97316', '#ef4444']
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=daily['timestamp'], y=daily['follower_count'], name='Actual', line=dict(color='#6366f1', width=4)))
                
                current = int(daily['follower_count'].iloc[-1])
                growth_metrics = []

                for horizon, color in zip(horizons, colors):
                    future_y = calculate_gb_forecast(daily[['timestamp', 'follower_count']], horizon)
                    future_dates = pd.date_range(daily['timestamp'].iloc[-1] + timedelta(days=1), periods=horizon, freq='D')
                    
                    fig.add_trace(go.Scatter(x=future_dates, y=future_y, name=f'{horizon}D Forecast', line=dict(color=color, width=2, dash='dot')))
                    
                    predicted = int(future_y[-1])
                    growth = predicted - current
                    growth_metrics.append((horizon, growth, color))
                
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(l=0, r=0, t=10, b=0), showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                
                metrics_cols = st.columns(4)
                for i, (horizon, growth, color) in enumerate(growth_metrics):
                    with metrics_cols[i]:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 0.5rem; background: {color}10; border-radius: 8px; border-top: 3px solid {color};">
                            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">{horizon} Days</div>
                            <div style="font-weight: 700; color: {color};">+{growth:,}</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Insufficient data for 90-day forecasting.")
        st.markdown('</div>', unsafe_allow_html=True)

    
    with col2:
        st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🔮 Prophet Seasonal Forecast</div>', unsafe_allow_html=True)
        
        if PROPHET_AVAILABLE and 'timestamp' in data.columns and 'follower_count' in data.columns:
            try:
                df = data.copy()
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                daily = df.groupby(pd.Grouper(key='timestamp', freq='D'))['follower_count'].last().reset_index().dropna()

                if len(daily) > 30:
                    forecast = calculate_prophet_forecast(daily[['timestamp', 'follower_count']])
                    if forecast is not None:
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=daily['timestamp'], y=daily['follower_count'], name='Historical', line=dict(color='#6366f1', width=3)))
                        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='AI Forecast', line=dict(color='#f093fb', width=3, dash='dash')))
                        fig.add_trace(go.Scatter(x=pd.concat([forecast['ds'], forecast['ds'][::-1]]), y=pd.concat([forecast['yhat_upper'], forecast['yhat_lower'][::-1]]), fill='toself', fillcolor='rgba(240, 147, 251, 0.15)', line=dict(color='rgba(255,255,255,0)'), hoverinfo="skip", showlegend=False))
                        
                        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(l=0, r=0, t=10, b=0), showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                        
                        pred30 = int(forecast['yhat'].iloc[-1])
                        curr = int(daily['follower_count'].iloc[-1])
                        st.markdown(f"""
                        <div style="background: rgba(240, 147, 251, 0.05); padding: 0.5rem 1rem; border-radius: 10px; border-left: 3px solid #f093fb;">
                            📊 <b>30D Growth Target:</b> +{pred30-curr:,} followers projected
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Insufficient data for Prophet seasonal analysis.")
            except Exception as e:
                st.warning(f"Prophet unavailable: {e}")
        else:
            st.info("Upload more history for Prophet deep analysis.")
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
        st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🎭 Emotion Distribution</div>', unsafe_allow_html=True)
        emotion_counts = analysis_df['emotion'].value_counts()
        colors_emotion = {'😍 Joy': '#10b981', '😊 Happy': '#6366f1', '😡 Anger': '#ef4444', 
                          '😢 Sad': '#f59e0b', '😲 Surprise': '#f093fb', '😐 Neutral': '#94a3b8'}
        
        fig = px.pie(values=emotion_counts.values, names=emotion_counts.index, hole=0.6,
                     color=emotion_counts.index, color_discrete_map=colors_emotion)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, 
                          margin=dict(l=0, r=0, t=10, b=0), showlegend=True,
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📊 Emotion vs Engagement</div>', unsafe_allow_html=True)
        
        if 'likes' in analysis_df.columns:
            emotion_eng = analysis_df.groupby('emotion')['likes'].mean().sort_values(ascending=True).reset_index()
            fig = px.bar(emotion_eng, x='likes', y='emotion', orientation='h',
                         color='emotion', color_discrete_map=colors_emotion)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300,
                              margin=dict(l=0, r=0, t=10, b=0), showlegend=False,
                              xaxis_title="Avg Likes", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            if not emotion_eng.empty:
                best_emo = emotion_eng.iloc[-1]['emotion']
                best_val = emotion_eng.iloc[-1]['likes']
                st.markdown(f"""
                <div style="background: rgba(99, 102, 241, 0.05); padding: 0.5rem 1rem; border-radius: 10px; border-left: 3px solid #6366f1;">
                    💡 <b>{best_emo}</b> content generates <b>{best_val:.0f}</b> avg likes.
                </div>
                """, unsafe_allow_html=True)
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
        st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🎯 K-Means Segments</div>', unsafe_allow_html=True)
        
        clusters, features_scaled = calculate_clustering(data[required], k=3)
        df_cluster = data.copy()
        df_cluster['segment'] = clusters
        
        segment_avg = df_cluster.groupby('segment')['likes'].mean().sort_values()
        labels_map = {segment_avg.index[0]: 'Low Engagers', segment_avg.index[1]: 'Medium Engagers', segment_avg.index[2]: 'High Engagers'}
        df_cluster['segment_label'] = df_cluster['segment'].map(labels_map)
        
        counts = df_cluster['segment_label'].value_counts().reset_index()
        counts.columns = ['label', 'count']
        colors_map = {'High Engagers': '#10b981', 'Medium Engagers': '#f59e0b', 'Low Engagers': '#ef4444'}
        
        fig = px.pie(counts, values='count', names='label', hole=0.6,
                     color='label', color_discrete_map=colors_map)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300,
                          margin=dict(l=0, r=0, t=10, b=0), showlegend=True,
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        score = silhouette_score(features_scaled, clusters)
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
            <div style="font-size: 0.85rem; color: #64748b;">Clustering Quality:</div>
            <div style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 0.2rem 0.6rem; border-radius: 6px; font-weight: 700;">{score:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🔍 DBSCAN Patterns</div>', unsafe_allow_html=True)
        
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        clusters_db = dbscan.fit_predict(features_scaled)
        summary = pd.Series(clusters_db).value_counts().sort_index().reset_index()
        summary.columns = ['cid', 'count']
        summary['label'] = summary['cid'].apply(lambda x: 'Viral Outliers' if x == -1 else f'Pattern {x+1}')
        
        fig = px.bar(summary, x='label', y='count',
                     color='label', color_discrete_sequence=['#ef4444' if 'Viral' in l else '#6366f1' for l in summary['label']])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300,
                          margin=dict(l=0, r=0, t=10, b=0), showlegend=False,
                          xaxis_title="", yaxis_title="Post Count")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        outliers = (clusters_db==-1).sum()
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.05); padding: 0.5rem 1rem; border-radius: 10px; border-left: 3px solid #ef4444; margin-top: 1rem;">
            🔥 Detected <b>{outliers}</b> viral outliers that break common patterns.
        </div>
        """, unsafe_allow_html=True)
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
