"""
Social Listening & Brand Monitoring Module
Inspired by Brandwatch - Monitor brand mentions, sentiment, and conversations
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
from collections import Counter
import re

def generate_brand_mentions(days=30, brand_name="TMU"):
    """Generate simulated brand mentions across platforms"""
    mentions = []
    platforms = ['Twitter', 'Instagram', 'Facebook', 'LinkedIn', 'TikTok', 'Reddit', 'YouTube']
    sentiments = ['Positive', 'Neutral', 'Negative']
    sentiment_weights = [0.6, 0.3, 0.1]  # 60% positive, 30% neutral, 10% negative
    
    topics = [
        'Admissions', 'Campus Life', 'Placements', 'Faculty', 'Infrastructure',
        'Events', 'Research', 'Sports', 'Hostel', 'Fees', 'Scholarships'
    ]
    
    sample_mentions = [
        f"Just got admitted to {brand_name}! So excited! 🎉",
        f"The campus facilities at {brand_name} are amazing",
        f"Great placement opportunities at {brand_name}",
        f"Loving the campus life at {brand_name}",
        f"The faculty at {brand_name} is very supportive",
        f"{brand_name} has excellent infrastructure",
        f"Amazing cultural fest at {brand_name}!",
        f"Proud to be a {brand_name} student",
        f"The hostel facilities at {brand_name} need improvement",
        f"Waiting for admission results from {brand_name}"
    ]
    
    for day in range(days):
        date = datetime.now() - timedelta(days=days-day)
        daily_mentions = random.randint(50, 200)
        
        for _ in range(daily_mentions):
            platform = random.choice(platforms)
            sentiment = random.choices(sentiments, weights=sentiment_weights)[0]
            topic = random.choice(topics)
            
            # Adjust engagement based on platform and sentiment
            if platform == 'Instagram':
                engagement = random.randint(50, 500)
            elif platform == 'Twitter':
                engagement = random.randint(20, 300)
            elif platform == 'TikTok':
                engagement = random.randint(100, 1000)
            else:
                engagement = random.randint(10, 200)
            
            # Boost engagement for positive sentiment
            if sentiment == 'Positive':
                engagement = int(engagement * 1.5)
            elif sentiment == 'Negative':
                engagement = int(engagement * 1.2)  # Negative content often gets more engagement
            
            mentions.append({
                'date': date,
                'platform': platform,
                'sentiment': sentiment,
                'topic': topic,
                'engagement': engagement,
                'reach': engagement * random.randint(5, 20),
                'text': random.choice(sample_mentions),
                'author_followers': random.randint(100, 50000),
                'is_influencer': random.random() > 0.9,
                'has_media': random.random() > 0.4
            })
    
    return pd.DataFrame(mentions)

def calculate_sentiment_score(mentions_df):
    """Calculate overall sentiment score (0-100)"""
    sentiment_values = {
        'Positive': 100,
        'Neutral': 50,
        'Negative': 0
    }
    
    if len(mentions_df) == 0:
        return 50
    
    total_score = sum(sentiment_values[s] for s in mentions_df['sentiment'])
    return round(total_score / len(mentions_df), 1)

def detect_trending_topics(mentions_df, top_n=10):
    """Detect trending topics from mentions"""
    topic_counts = mentions_df['topic'].value_counts().head(top_n)
    return topic_counts

def detect_crisis_signals(mentions_df):
    """Detect potential PR crises"""
    alerts = []
    
    # Check for spike in negative mentions
    recent_mentions = mentions_df[mentions_df['date'] >= datetime.now() - timedelta(days=1)]
    negative_ratio = len(recent_mentions[recent_mentions['sentiment'] == 'Negative']) / max(len(recent_mentions), 1)
    
    if negative_ratio > 0.3:
        alerts.append({
            'severity': 'High',
            'type': 'Negative Sentiment Spike',
            'message': f'⚠️ {round(negative_ratio*100, 1)}% of mentions in last 24h are negative',
            'action': 'Review recent negative mentions and prepare response'
        })
    
    # Check for sudden volume spike
    avg_daily_mentions = len(mentions_df) / 30
    recent_daily = len(recent_mentions)
    
    if recent_daily > avg_daily_mentions * 2:
        alerts.append({
            'severity': 'Medium',
            'type': 'Mention Volume Spike',
            'message': f'📈 Mention volume is {round(recent_daily/avg_daily_mentions, 1)}x higher than average',
            'action': 'Investigate cause of increased mentions'
        })
    
    # Check for influencer negative mentions
    influencer_negative = recent_mentions[
        (recent_mentions['is_influencer'] == True) & 
        (recent_mentions['sentiment'] == 'Negative')
    ]
    
    if len(influencer_negative) > 0:
        alerts.append({
            'severity': 'High',
            'type': 'Influencer Negative Mention',
            'message': f'🚨 {len(influencer_negative)} influencer(s) posted negative content',
            'action': 'Immediate response required - high visibility risk'
        })
    
    return alerts

def render_social_listening():
    """Main rendering function for social listening dashboard"""
    
    st.markdown("## 👂 Social Listening & Brand Monitoring")
    st.markdown("Real-time monitoring of brand mentions, sentiment, and conversations across platforms")
    
    # Configuration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        brand_name = st.text_input("Brand Name", value="TMU")
    
    with col2:
        time_range = st.selectbox("Time Range", ["Last 7 Days", "Last 30 Days", "Last 90 Days"], index=1)
    
    with col3:
        auto_refresh = st.checkbox("Auto-refresh (Live)", value=False)
    
    # Generate mention data
    days = 7 if time_range == "Last 7 Days" else 30 if time_range == "Last 30 Days" else 90
    mentions_df = generate_brand_mentions(days=days, brand_name=brand_name)
    
    # Crisis Detection
    crisis_alerts = detect_crisis_signals(mentions_df)
    
    if crisis_alerts:
        st.markdown("### 🚨 Crisis Alerts")
        for alert in crisis_alerts:
            if alert['severity'] == 'High':
                st.error(f"**{alert['type']}**: {alert['message']}\n\n💡 {alert['action']}")
            else:
                st.warning(f"**{alert['type']}**: {alert['message']}\n\n💡 {alert['action']}")
    
    # Key Metrics
    st.markdown("### 📊 Key Listening Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_mentions = len(mentions_df)
    sentiment_score = calculate_sentiment_score(mentions_df)
    total_reach = mentions_df['reach'].sum()
    avg_engagement = mentions_df['engagement'].mean()
    
    # Calculate changes
    half_point = len(mentions_df) // 2
    recent_half = mentions_df.iloc[half_point:]
    older_half = mentions_df.iloc[:half_point]
    
    mention_change = ((len(recent_half) - len(older_half)) / max(len(older_half), 1)) * 100
    sentiment_change = calculate_sentiment_score(recent_half) - calculate_sentiment_score(older_half)
    
    with col1:
        st.metric("Total Mentions", f"{total_mentions:,}", delta=f"{round(mention_change, 1)}%")
    
    with col2:
        st.metric("Sentiment Score", f"{sentiment_score}/100", delta=f"{round(sentiment_change, 1)}")
    
    with col3:
        st.metric("Total Reach", f"{total_reach:,}", delta="12.5%")
    
    with col4:
        st.metric("Avg Engagement", f"{round(avg_engagement)}", delta="8.2%")
    
    with col5:
        influencer_mentions = len(mentions_df[mentions_df['is_influencer'] == True])
        st.metric("Influencer Mentions", influencer_mentions, delta="+3")
    
    # Sentiment Over Time
    st.markdown("### 📈 Sentiment Trends Over Time")
    
    # Group by date and sentiment
    daily_sentiment = mentions_df.groupby([mentions_df['date'].dt.date, 'sentiment']).size().reset_index(name='count')
    daily_sentiment = daily_sentiment.pivot(index='date', columns='sentiment', values='count').fillna(0)
    
    fig_sentiment = go.Figure()
    
    fig_sentiment.add_trace(go.Scatter(
        x=daily_sentiment.index,
        y=daily_sentiment.get('Positive', [0]*len(daily_sentiment)),
        name='Positive',
        fill='tozeroy',
        line=dict(color='#43e97b', width=2),
        stackgroup='one'
    ))
    
    fig_sentiment.add_trace(go.Scatter(
        x=daily_sentiment.index,
        y=daily_sentiment.get('Neutral', [0]*len(daily_sentiment)),
        name='Neutral',
        fill='tonexty',
        line=dict(color='#94a3b8', width=2),
        stackgroup='one'
    ))
    
    fig_sentiment.add_trace(go.Scatter(
        x=daily_sentiment.index,
        y=daily_sentiment.get('Negative', [0]*len(daily_sentiment)),
        name='Negative',
        fill='tonexty',
        line=dict(color='#fa709a', width=2),
        stackgroup='one'
    ))
    
    fig_sentiment.update_layout(
        title="Daily Sentiment Distribution",
        xaxis_title="Date",
        yaxis_title="Number of Mentions",
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig_sentiment, use_container_width=True)
    
    # Platform Distribution & Topic Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌐 Platform Distribution")
        
        platform_counts = mentions_df['platform'].value_counts()
        
        fig_platform = px.pie(
            values=platform_counts.values,
            names=platform_counts.index,
            title="Mentions by Platform",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        
        fig_platform.update_traces(textposition='inside', textinfo='percent+label')
        fig_platform.update_layout(height=400)
        
        st.plotly_chart(fig_platform, use_container_width=True)
    
    with col2:
        st.markdown("### 🔥 Trending Topics")
        
        topic_counts = detect_trending_topics(mentions_df)
        
        fig_topics = go.Figure(go.Bar(
            x=topic_counts.values,
            y=topic_counts.index,
            orientation='h',
            marker=dict(
                color=topic_counts.values,
                colorscale='Viridis',
                showscale=True
            ),
            text=topic_counts.values,
            textposition='auto'
        ))
        
        fig_topics.update_layout(
            title="Top Discussion Topics",
            xaxis_title="Number of Mentions",
            yaxis_title="",
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_topics, use_container_width=True)
    
    # Sentiment by Platform
    st.markdown("### 🎭 Sentiment Analysis by Platform")
    
    platform_sentiment = mentions_df.groupby(['platform', 'sentiment']).size().reset_index(name='count')
    
    fig_platform_sent = px.bar(
        platform_sentiment,
        x='platform',
        y='count',
        color='sentiment',
        title="Sentiment Distribution Across Platforms",
        color_discrete_map={
            'Positive': '#43e97b',
            'Neutral': '#94a3b8',
            'Negative': '#fa709a'
        },
        barmode='group',
        height=400
    )
    
    fig_platform_sent.update_layout(template='plotly_white')
    st.plotly_chart(fig_platform_sent, use_container_width=True)
    
    # Recent Mentions Feed
    st.markdown("### 💬 Recent Mentions Feed")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_platform = st.multiselect("Filter by Platform", options=['All'] + list(mentions_df['platform'].unique()), default=['All'])
    
    with col2:
        filter_sentiment = st.multiselect("Filter by Sentiment", options=['All'] + list(mentions_df['sentiment'].unique()), default=['All'])
    
    with col3:
        filter_influencer = st.checkbox("Influencer Mentions Only", value=False)
    
    # Apply filters
    filtered_mentions = mentions_df.copy()
    
    if 'All' not in filter_platform and filter_platform:
        filtered_mentions = filtered_mentions[filtered_mentions['platform'].isin(filter_platform)]
    
    if 'All' not in filter_sentiment and filter_sentiment:
        filtered_mentions = filtered_mentions[filtered_mentions['sentiment'].isin(filter_sentiment)]
    
    if filter_influencer:
        filtered_mentions = filtered_mentions[filtered_mentions['is_influencer'] == True]
    
    # Sort by engagement
    filtered_mentions = filtered_mentions.sort_values('engagement', ascending=False).head(20)
    
    # Display mentions
    for idx, mention in filtered_mentions.iterrows():
        sentiment_emoji = '😊' if mention['sentiment'] == 'Positive' else '😐' if mention['sentiment'] == 'Neutral' else '😞'
        influencer_badge = '⭐ INFLUENCER' if mention['is_influencer'] else ''
        
        with st.container():
            st.markdown(f"""
            <div style="padding: 1rem; background-color: #f8fafc; border-left: 4px solid {'#43e97b' if mention['sentiment'] == 'Positive' else '#fa709a' if mention['sentiment'] == 'Negative' else '#94a3b8'}; border-radius: 8px; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div>
                        <span style="font-weight: bold; color: #1e293b;">{mention['platform']}</span>
                        <span style="color: #64748b; margin-left: 1rem;">{mention['date'].strftime('%Y-%m-%d %H:%M')}</span>
                        <span style="background: #fef3c7; padding: 2px 8px; border-radius: 4px; margin-left: 1rem; font-size: 0.8rem;">{influencer_badge}</span>
                    </div>
                    <div>
                        <span style="font-size: 1.5rem;">{sentiment_emoji}</span>
                    </div>
                </div>
                <div style="color: #334155; margin-bottom: 0.5rem;">
                    "{mention['text']}"
                </div>
                <div style="display: flex; gap: 1.5rem; font-size: 0.9rem; color: #64748b;">
                    <span>👥 {mention['author_followers']:,} followers</span>
                    <span>❤️ {mention['engagement']} engagements</span>
                    <span>👁️ {mention['reach']:,} reach</span>
                    <span>🏷️ {mention['topic']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Influencer Analysis
    st.markdown("### ⭐ Influencer Impact Analysis")
    
    influencer_mentions = mentions_df[mentions_df['is_influencer'] == True]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Influencer Mentions", len(influencer_mentions))
        st.metric("Avg Influencer Reach", f"{influencer_mentions['reach'].mean():,.0f}" if len(influencer_mentions) > 0 else "0")
    
    with col2:
        influencer_positive = len(influencer_mentions[influencer_mentions['sentiment'] == 'Positive'])
        influencer_sentiment_ratio = (influencer_positive / max(len(influencer_mentions), 1)) * 100
        st.metric("Positive Influencer %", f"{round(influencer_sentiment_ratio, 1)}%")
        st.metric("Total Influencer Reach", f"{influencer_mentions['reach'].sum():,}" if len(influencer_mentions) > 0 else "0")
    
    with col3:
        st.metric("Avg Influencer Followers", f"{influencer_mentions['author_followers'].mean():,.0f}" if len(influencer_mentions) > 0 else "0")
        st.metric("Influencer Engagement", f"{influencer_mentions['engagement'].sum():,}" if len(influencer_mentions) > 0 else "0")
    
    # Competitive Mentions
    st.markdown("### 🎯 Competitive Mentions")
    
    competitors = ['Competitor A', 'Competitor B', 'Competitor C']
    comp_data = []
    
    for comp in competitors:
        comp_mentions = random.randint(500, 2000)
        comp_sentiment = round(random.uniform(40, 75), 1)
        comp_data.append({
            'Brand': comp,
            'Mentions': comp_mentions,
            'Sentiment Score': comp_sentiment,
            'Share of Voice': round((comp_mentions / (comp_mentions + total_mentions)) * 100, 1)
        })
    
    # Add your brand
    comp_data.insert(0, {
        'Brand': brand_name,
        'Mentions': total_mentions,
        'Sentiment Score': sentiment_score,
        'Share of Voice': round((total_mentions / (total_mentions + sum(c['Mentions'] for c in comp_data))) * 100, 1)
    })
    
    comp_df = pd.DataFrame(comp_data)
    
    # Highlight your brand
    def highlight_brand(row):
        if row['Brand'] == brand_name:
            return ['background-color: #e0f2fe'] * len(row)
        return [''] * len(row)
    
    styled_comp = comp_df.style.apply(highlight_brand, axis=1)
    st.dataframe(styled_comp, use_container_width=True)
    
    # Export and Actions
    st.markdown("### 🛠️ Actions & Export")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Export Report", use_container_width=True):
            st.success("✅ Listening report exported!")
    
    with col2:
        if st.button("🔔 Set Alert", use_container_width=True):
            st.success("✅ Alert configured!")
    
    with col3:
        if st.button("📧 Email Digest", use_container_width=True):
            st.success("✅ Daily digest scheduled!")
    
    with col4:
        if st.button("🤖 AI Summary", use_container_width=True):
            st.info("📝 Generating AI-powered insights summary...")

if __name__ == "__main__":
    st.set_page_config(page_title="Social Listening", layout="wide")
    render_social_listening()
