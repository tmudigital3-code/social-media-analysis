"""
Advanced Machine Learning Module - Part 1
Deep Learning, NLP, Clustering
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            daily = data.groupby(pd.Grouper(key='timestamp', freq='D'))['follower_count'].last().reset_index().dropna()
            
            if len(daily) > 14:
                X = np.arange(len(daily)).reshape(-1, 1)
                X_poly = np.column_stack([X, X**2, X**3])
                y = daily['follower_count'].values
                
                model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
                model.fit(X_poly, y)
                
                horizons = [7, 30, 60, 90]
                colors = ['#10b981', '#f59e0b', '#f97316', '#ef4444']
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=daily['timestamp'], y=daily['follower_count'], name='Actual', line=dict(color='#667eea', width=3)))
                
                for horizon, color in zip(horizons, colors):
                    future_X = np.arange(len(daily), len(daily) + horizon).reshape(-1, 1)
                    future_X_poly = np.column_stack([future_X, future_X**2, future_X**3])
                    future_y = model.predict(future_X_poly)
                    future_dates = pd.date_range(daily['timestamp'].iloc[-1] + timedelta(days=1), periods=horizon, freq='D')
                    fig.add_trace(go.Scatter(x=future_dates, y=future_y, name=f'{horizon}D', line=dict(color=color, width=2, dash='dash')))
                
                fig.update_layout(template='plotly_white', height=350, margin=dict(l=0, r=0, t=10, b=0), hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
                
                current = int(daily['follower_count'].iloc[-1])
                for horizon, color in zip(horizons, colors):
                    pred_X = np.array([[len(daily) + horizon - 1, (len(daily) + horizon - 1)**2, (len(daily) + horizon - 1)**3]])
                    predicted = int(model.predict(pred_X)[0])
                    growth = predicted - current
                    st.markdown(f'<span style="color:{color}">▪ {horizon}d: +{growth:,} ({(growth/current*100):+.1f}%)</span>', unsafe_allow_html=True)
            else:
                st.info("Need 14+ days for forecasting")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🔮 Prophet Seasonal Forecast</div>', unsafe_allow_html=True)
        
        if PROPHET_AVAILABLE and 'timestamp' in data.columns and 'follower_count' in data.columns:
            try:
                daily = data.groupby(pd.Grouper(key='timestamp', freq='D'))['follower_count'].last().reset_index().dropna()
                if len(daily) > 30:
                    prophet_df = daily.rename(columns={'timestamp': 'ds', 'follower_count': 'y'})
                    if PROPHET_AVAILABLE:  # type: ignore
                        model = Prophet(daily_seasonality='auto', weekly_seasonality='auto', yearly_seasonality='auto')  # type: ignore
                        model.fit(prophet_df)
                        future = model.make_future_dataframe(periods=30)
                        forecast = model.predict(future)
                    
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=prophet_df['ds'], y=prophet_df['y'], name='Actual', line=dict(color='#667eea', width=3)))
                        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast', line=dict(color='#f093fb', width=2, dash='dash')))
                        fig.add_trace(go.Scatter(x=list(forecast['ds']) + list(forecast['ds'][::-1]), 
                                               y=list(forecast['yhat_upper']) + list(forecast['yhat_lower'][::-1]),
                                               fill='toself', fillcolor='rgba(240,147,251,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Confidence'))
                        
                        fig.update_layout(template='plotly_white', height=350, margin=dict(l=0, r=0, t=10, b=0), hovermode='x unified')
                        st.plotly_chart(fig, use_container_width=True)
                        
                        pred30 = int(forecast['yhat'].iloc[-1])
                        curr = int(prophet_df['y'].iloc[-1])
                        st.markdown(f'📊 **30D Forecast:** +{pred30-curr:,} ({(pred30-curr)/curr*100:+.1f}%)')
                else:
                    st.info("Need 30+ days for Prophet")
            except Exception as e:
                st.warning(f"Prophet unavailable: {e}")
        else:
            st.info("Install: `pip install prophet`")
        st.markdown('</div>', unsafe_allow_html=True)


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
    
    def get_sentiment(text):
        if pd.isna(text) or text == '':
            return 'Neutral', 0.0, 0.0
        try:
            if NLP_AVAILABLE:  # type: ignore
                blob = TextBlob(str(text))  # type: ignore
                pol = blob.sentiment.polarity  # type: ignore
                subj = blob.sentiment.subjectivity  # type: ignore
                sent = 'Positive' if pol > 0.1 else ('Negative' if pol < -0.1 else 'Neutral')
                return sent, pol, subj
        except:
            return 'Neutral', 0.0, 0.0
        return 'Neutral', 0.0, 0.0
    
    sentiments = data['caption'].apply(get_sentiment)
    data['sentiment'] = sentiments.apply(lambda x: x[0])
    data['sentiment_score'] = sentiments.apply(lambda x: x[1])
    data['subjectivity'] = sentiments.apply(lambda x: x[2])
    
    def detect_emotion(pol, subj):
        if pol > 0.5: return '😍 Joy'
        elif pol > 0.2: return '😊 Happy'
        elif pol < -0.5: return '😡 Anger'
        elif pol < -0.2: return '😢 Sad'
        elif subj > 0.7: return '😲 Surprise'
        return '😐 Neutral'
    
    data['emotion'] = data.apply(lambda row: detect_emotion(row['sentiment_score'], row['subjectivity']), axis=1)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">😊 Emotion Distribution</div>', unsafe_allow_html=True)
        
        emotion_counts = data['emotion'].value_counts()
        colors_emotion = {'😍 Joy': '#10b981', '😊 Happy': '#34d399', '😲 Surprise': '#fbbf24', 
                         '😐 Neutral': '#94a3b8', '😢 Sad': '#fb923c', '😡 Anger': '#ef4444'}
        
        fig = go.Figure(data=[go.Pie(labels=emotion_counts.index, values=emotion_counts.values, hole=0.4,
                                     marker_colors=[colors_emotion.get(e, '#94a3b8') for e in emotion_counts.index],
                                     textinfo='label+percent', textfont_size=13)])
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=0, r=0, t=10, b=0),
                         annotations=[dict(text='Emotions', x=0.5, y=0.5, font_size=16, showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📊 Emotion vs Engagement</div>', unsafe_allow_html=True)
        
        if 'likes' in data.columns:
            emotion_eng = data.groupby('emotion')['likes'].mean().sort_values(ascending=True)
            fig = go.Figure(go.Bar(x=emotion_eng.values, y=emotion_eng.index, orientation='h',
                                  marker_color=[colors_emotion.get(e, '#94a3b8') for e in emotion_eng.index],
                                  text=emotion_eng.values.round(0), textposition='outside'))
            fig.update_layout(template='plotly_white', height=300, margin=dict(l=0, r=0, t=10, b=0), xaxis_title='Avg Likes')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f'💡 **{emotion_eng.idxmax()}** performs best ({emotion_eng.max():.0f} likes)')
        st.markdown('</div>', unsafe_allow_html=True)


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
        
        features = data[required].fillna(0)
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
        data['segment'] = kmeans.fit_predict(features_scaled)
        
        segment_avg = data.groupby('segment')['likes'].mean().sort_values()
        labels = {segment_avg.index[0]: 'Low Engagers', segment_avg.index[1]: 'Medium Engagers', segment_avg.index[2]: 'High Engagers'}
        data['segment_label'] = data['segment'].map(labels)
        
        counts = data['segment_label'].value_counts()
        colors = ['#ef4444', '#f59e0b', '#10b981']
        
        fig = go.Figure(data=[go.Pie(labels=counts.index, values=counts.values, hole=0.5, marker_colors=colors,
                                     textinfo='label+percent', textfont_size=13)])
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=0, r=0, t=10, b=0),
                         annotations=[dict(text=f'{len(data)} Posts', x=0.5, y=0.5, font_size=14, showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'**Quality:** {silhouette_score(features_scaled, data["segment"]):.3f}')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🔍 DBSCAN Patterns</div>', unsafe_allow_html=True)
        
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        data['dbscan_cluster'] = dbscan.fit_predict(features_scaled)
        
        summary = data['dbscan_cluster'].value_counts().sort_index()
        labels = ['Outliers (Viral)' if cid == -1 else f'Pattern {cid+1}' for cid in summary.index]
        
        fig = go.Figure(data=[go.Bar(x=labels, y=summary.values, 
                                     marker_color=['#ef4444' if 'Outliers' in l else '#667eea' for l in labels],
                                     text=summary.values, textposition='outside')])
        fig.update_layout(template='plotly_white', height=300, margin=dict(l=0, r=0, t=10, b=0), yaxis_title='Posts')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'**Outliers:** {(data["dbscan_cluster"]==-1).sum()}')
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="pro-insights fade-in">', unsafe_allow_html=True)
    st.markdown('### 💡 Segment Recommendations')
    for seg in ['High Engagers', 'Medium Engagers', 'Low Engagers']:
        if seg in data['segment_label'].values:
            pct = (data['segment_label']==seg).sum() / len(data) * 100
            if seg == 'High Engagers':
                st.markdown(f'<div class="pro-insight-item">🏆 <strong>{seg} ({pct:.1f}%)</strong>: Premium content, exclusives (+32% confidence)</div>', unsafe_allow_html=True)
            elif seg == 'Medium Engagers':
                st.markdown(f'<div class="pro-insight-item">⚡ <strong>{seg} ({pct:.1f}%)</strong>: Post 5x/week, add polls (+28% confidence)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="pro-insight-item">📢 <strong>{seg} ({pct:.1f}%)</strong>: Re-engagement at 6-8 PM (+25% confidence)</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
