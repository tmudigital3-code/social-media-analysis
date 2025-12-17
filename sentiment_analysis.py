"""
Comprehensive Sentiment Analysis Module
Advanced NLP for social media content analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Try importing NLP libraries
try:
    from textblob import TextBlob
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False


def analyze_sentiment(text):
    """Analyze sentiment with polarity and subjectivity"""
    if pd.isna(text) or text == '':
        return {'sentiment': 'Neutral', 'polarity': 0.0, 'subjectivity': 0.0, 'emotion': '😐 Neutral'}
    
    try:
        blob = TextBlob(str(text))
        # Access sentiment attributes directly to avoid type checking issues
        polarity = float(blob.sentiment.polarity)
        subjectivity = float(blob.sentiment.subjectivity)
        
        # Determine sentiment
        if polarity > 0.1:
            sentiment = 'Positive'
        elif polarity < -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        # Determine emotion based on polarity and subjectivity
        if polarity > 0.6:
            emotion = '😍 Joy'
        elif polarity > 0.3:
            emotion = '😊 Happy'
        elif polarity < -0.6:
            emotion = '😡 Anger'
        elif polarity < -0.3:
            emotion = '😢 Sad'
        elif subjectivity > 0.7:
            emotion = '😲 Surprise'
        elif polarity > 0:
            emotion = '😌 Content'
        else:
            emotion = '😐 Neutral'
        
        return {
            'sentiment': sentiment,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'emotion': emotion
        }
    except:
        return {'sentiment': 'Neutral', 'polarity': 0.0, 'subjectivity': 0.0, 'emotion': '😐 Neutral'}


def render_sentiment_analysis(data):
    """Main sentiment analysis dashboard"""
    
    if not NLP_AVAILABLE:
        st.error("❌ TextBlob not installed.")
        st.code("pip install textblob", language="bash")
        st.code("python -m textblob.download_corpora", language="bash")
        st.info("💡 After installation, restart the dashboard.")
        return
    
    # Test if TextBlob is working
    try:
        test_blob = TextBlob("test")
        _ = test_blob.sentiment
    except Exception as e:
        st.error("❌ TextBlob corpora not downloaded.")
        st.code("python -m textblob.download_corpora", language="bash")
        st.info(f"Error: {str(e)}")
        return
    
    # Header
    st.markdown('<div class="pro-header fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-title">💬 Sentiment Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-subtitle">AI-powered emotion detection and sentiment insights</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Check for caption column
    text_column = None
    if 'caption' in data.columns:
        text_column = 'caption'
    elif 'text' in data.columns:
        text_column = 'text'
    elif 'content' in data.columns:
        text_column = 'content'
    elif 'message' in data.columns:
        text_column = 'message'
    elif 'description' in data.columns:
        text_column = 'description'
    
    if text_column is None:
        st.warning("⚠️ No text/caption data found.")
        st.info(f"📊 Available columns: {', '.join(data.columns.tolist())}")
        st.info("💡 Please upload data with one of these columns: caption, text, content, message, or description")
        
        # Show sample data structure
        st.markdown("### 📋 Sample Data Structure Needed:")
        sample = pd.DataFrame({
            'caption': ['Great post!', 'Love this content', 'Not sure about this'],
            'likes': [100, 150, 50],
            'comments': [10, 15, 5]
        })
        st.dataframe(sample, use_container_width=True)
        return
    
    st.success(f"✅ Analyzing text from column: **{text_column}**")
    
    # Analyze all captions
    with st.spinner('🔍 Analyzing sentiment...'):
        sentiments = data[text_column].apply(analyze_sentiment)
        data['sentiment'] = sentiments.apply(lambda x: x['sentiment'])
        data['polarity'] = sentiments.apply(lambda x: x['polarity'])
        data['subjectivity'] = sentiments.apply(lambda x: x['subjectivity'])
        data['emotion'] = sentiments.apply(lambda x: x['emotion'])
    
    # Summary Metrics
    st.markdown("### 📊 Sentiment Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        positive_pct = (data['sentiment'] == 'Positive').sum() / len(data) * 100
        st.metric("Positive Posts", f"{positive_pct:.1f}%", "🟢")
    
    with col2:
        negative_pct = (data['sentiment'] == 'Negative').sum() / len(data) * 100
        st.metric("Negative Posts", f"{negative_pct:.1f}%", "🔴")
    
    with col3:
        avg_polarity = data['polarity'].mean()
        st.metric("Avg Polarity", f"{avg_polarity:.2f}", "📈")
    
    with col4:
        avg_subjectivity = data['subjectivity'].mean()
        st.metric("Avg Subjectivity", f"{avg_subjectivity:.2f}", "📊")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 1: Sentiment Distribution & Emotion Breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">😊 Sentiment Distribution</div>', unsafe_allow_html=True)
        
        sentiment_counts = data['sentiment'].value_counts()
        colors = {'Positive': '#10b981', 'Neutral': '#f59e0b', 'Negative': '#ef4444'}
        
        fig = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=0.5,
            marker_colors=[colors.get(s, '#94a3b8') for s in sentiment_counts.index],
            textinfo='label+percent',
            textfont_size=14
        )])
        
        fig.update_layout(
            template='plotly_white',
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            annotations=[dict(text=f'{len(data)}<br>Posts', x=0.5, y=0.5, font_size=16, showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🎭 Emotion Breakdown</div>', unsafe_allow_html=True)
        
        emotion_counts = data['emotion'].value_counts()
        emotion_colors = {
            '😍 Joy': '#10b981',
            '😊 Happy': '#34d399',
            '😌 Content': '#6ee7b7',
            '😲 Surprise': '#fbbf24',
            '😐 Neutral': '#94a3b8',
            '😢 Sad': '#fb923c',
            '😡 Anger': '#ef4444'
        }
        
        fig = go.Figure(data=[go.Bar(
            x=emotion_counts.values,
            y=emotion_counts.index,
            orientation='h',
            marker_color=[emotion_colors.get(e, '#94a3b8') for e in emotion_counts.index],
            text=emotion_counts.values,
            textposition='outside'
        )])
        
        fig.update_layout(
            template='plotly_white',
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title='Post Count',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Sentiment vs Engagement & Polarity Timeline
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📈 Sentiment vs Engagement</div>', unsafe_allow_html=True)
        
        if 'likes' in data.columns:
            sentiment_engagement = data.groupby('sentiment').agg({
                'likes': 'mean',
                'comments': 'mean' if 'comments' in data.columns else 'count',
                'shares': 'mean' if 'shares' in data.columns else 'count'
            }).round(0)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Likes', x=sentiment_engagement.index, y=sentiment_engagement['likes'],
                                marker_color='#667eea'))
            if 'comments' in data.columns:
                fig.add_trace(go.Bar(name='Comments', x=sentiment_engagement.index, y=sentiment_engagement['comments'],
                                    marker_color='#f093fb'))
            if 'shares' in data.columns:
                fig.add_trace(go.Bar(name='Shares', x=sentiment_engagement.index, y=sentiment_engagement['shares'],
                                    marker_color='#10b981'))
            
            fig.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                barmode='group',
                yaxis_title='Average Count'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            best_sentiment = sentiment_engagement['likes'].idxmax()
            best_likes = sentiment_engagement['likes'].max()
            st.markdown(f"💡 **{best_sentiment} posts** perform best with {best_likes:.0f} avg likes")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📊 Polarity Over Time</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            daily_polarity = data.groupby(pd.Grouper(key='timestamp', freq='D')).agg({
                'polarity': 'mean',
                'subjectivity': 'mean'
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_polarity.index,
                y=daily_polarity['polarity'],
                name='Polarity',
                line=dict(color='#667eea', width=3),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.2)'
            ))
            
            fig.add_hline(y=0, line_dash="dash", line_color="#94a3b8", 
                         annotation_text="Neutral", annotation_position="right")
            
            fig.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                yaxis_title='Polarity Score',
                yaxis_range=[-1, 1],
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Hashtag Sentiment & Word Analysis
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🏷️ Top Hashtags by Sentiment</div>', unsafe_allow_html=True)
        
        if 'hashtags' in data.columns:
            hashtag_data = []
            for idx, row in data.iterrows():
                if pd.notna(row['hashtags']):
                    tags = str(row['hashtags']).split(',')
                    for tag in tags[:5]:
                        tag = tag.strip()
                        if tag:
                            hashtag_data.append({
                                'hashtag': tag,
                                'sentiment': row['sentiment'],
                                'polarity': row['polarity'],
                                'likes': row.get('likes', 0)
                            })
            
            if hashtag_data:
                ht_df = pd.DataFrame(hashtag_data)
                top_hashtags = ht_df.groupby(['hashtag', 'sentiment']).size().unstack(fill_value=0)
                top_hashtags['total'] = top_hashtags.sum(axis=1)
                top_hashtags = top_hashtags.nlargest(10, 'total')
                
                fig = go.Figure()
                if 'Positive' in top_hashtags.columns:
                    fig.add_trace(go.Bar(name='Positive', x=top_hashtags.index, y=top_hashtags['Positive'],
                                        marker_color='#10b981'))
                if 'Neutral' in top_hashtags.columns:
                    fig.add_trace(go.Bar(name='Neutral', x=top_hashtags.index, y=top_hashtags['Neutral'],
                                        marker_color='#f59e0b'))
                if 'Negative' in top_hashtags.columns:
                    fig.add_trace(go.Bar(name='Negative', x=top_hashtags.index, y=top_hashtags['Negative'],
                                        marker_color='#ef4444'))
                
                fig.update_layout(
                    template='plotly_white',
                    height=300,
                    margin=dict(l=0, r=0, t=10, b=0),
                    barmode='stack',
                    xaxis_tickangle=-45,
                    yaxis_title='Post Count'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hashtag data available")
        else:
            st.info("No hashtag column found")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📝 Caption Length vs Sentiment</div>', unsafe_allow_html=True)
        
        data['caption_length'] = data[text_column].astype(str).str.len()
        
        fig = px.scatter(
            data,
            x='caption_length',
            y='polarity',
            color='sentiment',
            color_discrete_map=colors,
            hover_data=['emotion'],
            opacity=0.6
        )
        
        fig.update_layout(
            template='plotly_white',
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title='Caption Length (chars)',
            yaxis_title='Polarity Score'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        avg_length_by_sentiment = data.groupby('sentiment')['caption_length'].mean()
        optimal_sentiment = avg_length_by_sentiment.idxmax()
        st.markdown(f"💡 **{optimal_sentiment}** posts avg {avg_length_by_sentiment[optimal_sentiment]:.0f} characters")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Emotion Timeline
    st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-chart-title">🎭 Emotion Timeline</div>', unsafe_allow_html=True)
    
    if 'timestamp' in data.columns:
        emotion_timeline = data.groupby([pd.Grouper(key='timestamp', freq='D'), 'emotion']).size().reset_index(name='count')
        
        fig = px.area(
            emotion_timeline,
            x='timestamp',
            y='count',
            color='emotion',
            color_discrete_map=emotion_colors
        )
        
        fig.update_layout(
            template='plotly_white',
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            yaxis_title='Post Count',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Top Posts by Sentiment
    st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-chart-title">🏆 Top Performing Posts by Sentiment</div>', unsafe_allow_html=True)
    
    sentiment_tabs = st.tabs(['Positive 😊', 'Neutral 😐', 'Negative 😢'])
    
    for idx, (sentiment_name, tab) in enumerate(zip(['Positive', 'Neutral', 'Negative'], sentiment_tabs)):
        with tab:
            sentiment_posts = data[data['sentiment'] == sentiment_name]
            if len(sentiment_posts) > 0 and 'likes' in sentiment_posts.columns:
                top_posts = sentiment_posts.nlargest(5, 'likes')[['timestamp', 'caption', 'likes', 'emotion', 'polarity']]
                top_posts['caption'] = top_posts['caption'].str[:80] + '...'
                st.dataframe(top_posts, use_container_width=True, hide_index=True)
            else:
                st.info(f"No {sentiment_name.lower()} posts found")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Insights
    st.markdown('<div class="pro-insights fade-in">', unsafe_allow_html=True)
    st.markdown('### 💡 AI-Powered Sentiment Insights')
    
    # Calculate insights
    dominant_sentiment = data['sentiment'].mode()[0] if len(data['sentiment'].mode()) > 0 else 'Neutral'
    dominant_emotion = data['emotion'].mode()[0] if len(data['emotion'].mode()) > 0 else '😐 Neutral'
    
    # Initialize variables to avoid unbound errors
    best_performing_sentiment = 'Neutral'
    sentiment_lift = 0.0
    
    if 'likes' in data.columns:
        best_performing_sentiment = data.groupby('sentiment')['likes'].mean().idxmax()
        sentiment_lift = ((data[data['sentiment'] == best_performing_sentiment]['likes'].mean() / 
                          data['likes'].mean() - 1) * 100)
    
    st.markdown(f'<div class="pro-insight-item">📊 <strong>Dominant Sentiment:</strong> {dominant_sentiment} ({(data["sentiment"]==dominant_sentiment).sum()}/{len(data)} posts, {(data["sentiment"]==dominant_sentiment).sum()/len(data)*100:.1f}%)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pro-insight-item">🎭 <strong>Most Common Emotion:</strong> {dominant_emotion}</div>', unsafe_allow_html=True)
    
    if 'likes' in data.columns:
        st.markdown(f'<div class="pro-insight-item">🚀 <strong>Best Performing:</strong> {best_performing_sentiment} posts get {sentiment_lift:+.1f}% more engagement</div>', unsafe_allow_html=True)
    
    avg_polarity = data['polarity'].mean()
    if avg_polarity > 0.2:
        st.markdown('<div class="pro-insight-item">✅ <strong>Overall Tone:</strong> Your content has a positive tone! Keep it up!</div>', unsafe_allow_html=True)
    elif avg_polarity < -0.2:
        st.markdown('<div class="pro-insight-item">⚠️ <strong>Overall Tone:</strong> Content leans negative. Consider more uplifting messages.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="pro-insight-item">ℹ️ <strong>Overall Tone:</strong> Balanced neutral tone. Mix in more emotional content for engagement.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)