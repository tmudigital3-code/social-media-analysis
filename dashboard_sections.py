"""
Dashboard Sections Module
Contains individual dashboard components for the professional analytics platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


# ==================== 1. Content Performance ====================
def render_content_performance(data):
    """Analyze content performance with hashtag analysis and engagement metrics"""
    st.markdown('<div class="pro-header fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-title">🎬 Content Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-subtitle">Analyze what kind of content performs best</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 1: Media Type Performance & Top Posts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🎭 Media Type Performance</div>', unsafe_allow_html=True)
        
        if 'media_type' in data.columns and 'likes' in data.columns:
            media_performance = data.groupby('media_type').agg({
                'likes': 'mean',
                'comments': 'mean' if 'comments' in data.columns else 'count',
                'shares': 'mean' if 'shares' in data.columns else 'count'
            }).round(0)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Likes', x=media_performance.index, y=media_performance['likes'],
                                marker_color='#667eea'))
            if 'comments' in data.columns:
                fig.add_trace(go.Bar(name='Comments', x=media_performance.index, y=media_performance['comments'],
                                    marker_color='#f093fb'))
            if 'shares' in data.columns:
                fig.add_trace(go.Bar(name='Shares', x=media_performance.index, y=media_performance['shares'],
                                    marker_color='#10b981'))
            
            fig.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                barmode='group',
                yaxis_title='Average Count'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            best_type = media_performance['likes'].idxmax()
            best_likes = media_performance['likes'].max()
            st.markdown(f"💡 **{best_type}** performs best with {best_likes:.0f} avg likes")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🏆 Top Performing Posts</div>', unsafe_allow_html=True)
        
        if all(col in data.columns for col in ['likes', 'comments', 'shares']):
            data_copy = data.copy()
            data_copy['total_engagement'] = data_copy['likes'] + data_copy['comments'] + data_copy['shares']
            top_posts = data_copy.nlargest(5, 'total_engagement')[['timestamp', 'caption', 'likes', 'comments', 'shares']]
            
            # Truncate long captions
            top_posts['caption'] = top_posts['caption'].astype(str).str[:50] + '...'
            
            st.dataframe(top_posts, use_container_width=True, hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Hashtag Analysis
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🏷️ Top Hashtags by Engagement</div>', unsafe_allow_html=True)
        
        if 'hashtags' in data.columns and 'likes' in data.columns:
            # Process hashtags data
            all_hashtags = []
            for idx, row in data.iterrows():
                if pd.notna(row['hashtags']):
                    tags = str(row['hashtags']).split(',')
                    for tag in tags:
                        tag = tag.strip().lower()
                        if tag:
                            all_hashtags.append({'hashtag': tag, 'likes': row['likes'], 'reach': row.get('reach', 0)})
            
            if all_hashtags:  # Check if we have hashtag data
                hashtag_df = pd.DataFrame(all_hashtags)
                hashtag_summary = hashtag_df.groupby('hashtag').agg({
                    'likes': 'sum',
                    'reach': 'sum'
                }).reset_index()  # type: ignore
                hashtag_summary['count'] = hashtag_df.groupby('hashtag').size().values
                
                if len(hashtag_summary) > 0:  # Now check if we have summary data
                    top_10 = hashtag_summary.nlargest(10, 'likes')
                    
                    fig = px.scatter(
                        top_10,
                        x='count',
                        y='likes',
                        size='reach',
                        color='likes',
                        text='hashtag',
                        color_continuous_scale=['#667eea', '#764ba2', '#f093fb']
                    )
                    
                    fig.update_traces(textposition='top center')
                    fig.update_layout(
                        template='plotly_white',
                        height=300,
                        margin=dict(l=0, r=0, t=10, b=0),
                        xaxis_title="Hashtag Frequency",
                        yaxis_title="Total Likes"
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 🧮 Top 10 Hashtags by Reach
    with col4:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🧮 Top 10 Hashtags by Reach</div>', unsafe_allow_html=True)
        
        if 'hashtags' in data.columns and 'reach' in data.columns:
            # Process hashtags data
            all_hashtags = []
            for idx, row in data.iterrows():
                if pd.notna(row['hashtags']):
                    tags = str(row['hashtags']).split(',')
                    for tag in tags:
                        tag = tag.strip().lower()
                        if tag:
                            all_hashtags.append({'hashtag': tag, 'likes': row['likes'], 'reach': row.get('reach', 0)})
            
            if all_hashtags:  # Check if we have hashtag data
                hashtag_df = pd.DataFrame(all_hashtags)
                hashtag_summary = hashtag_df.groupby('hashtag').agg({
                    'likes': 'sum',
                    'reach': 'sum'
                }).reset_index()  # type: ignore
                hashtag_summary['count'] = hashtag_df.groupby('hashtag').size().values
                
                if len(hashtag_summary) > 0:  # Now check if we have summary data
                    top_10 = hashtag_summary.nlargest(10, 'reach')
                    
                    fig = px.bar(
                        top_10,
                        x='reach',
                        y='hashtag',
                        orientation='h',
                        color='reach',
                        color_continuous_scale=['#667eea', '#764ba2', '#f093fb'],
                        text='reach'
                    )
                    
                    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
                    fig.update_layout(
                        template='plotly_white',
                        height=350,
                        margin=dict(l=0, r=0, t=10, b=0),
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


# ==================== 2. Audience Insights ====================
def render_audience_insights(data):
    """Audience Insights with Clear Visuals"""
    st.markdown('<div class="pro-header fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-title">👥 Audience Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-subtitle">Understand followers and their activity patterns</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # 🧍‍♂️🧍‍♀️ Gender Distribution
    with col1:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🧍‍♂️🧍‍♀️ Gender Distribution</div>', unsafe_allow_html=True)
        
        if 'audience_gender' in data.columns:
            gender_dist = data['audience_gender'].value_counts()
            
            fig = go.Figure(data=[go.Pie(
                labels=gender_dist.index,
                values=gender_dist.values,
                marker_colors=['#667eea', '#f093fb', '#764ba2']
            )])
            
            fig.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 🕓 Active Users by Hour
    with col2:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🕓 Active Users by Hour</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns:
            data['hour'] = pd.to_datetime(data['timestamp']).dt.hour
            hourly_activity = data.groupby('hour').size()
            
            fig = go.Figure(data=[go.Heatmap(
                z=[hourly_activity.values],
                x=hourly_activity.index,
                y=['Activity'],
                colorscale='Purples',
                text=[hourly_activity.values],
                texttemplate="%{text}",
                textfont={"size": 10}
            )])
            
            fig.update_layout(
                template='plotly_white',
                height=150,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title="Hour of Day"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Best hour insight
            best_hour = hourly_activity.idxmax()
            am_pm = "AM" if best_hour < 12 else "PM"
            hour_12 = best_hour if best_hour <= 12 else best_hour - 12
            
            st.markdown('<div class="pro-insights">', unsafe_allow_html=True)
            st.markdown(f'💡 <strong>Most followers active at {hour_12}:00 {am_pm}</strong>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Age Distribution & Location
    col3, col4 = st.columns(2)
    
    # 📊 Age Distribution
    with col3:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📊 Audience Age Groups</div>', unsafe_allow_html=True)
        
        if 'audience_age' in data.columns:
            age_dist = data['audience_age'].value_counts().sort_index()
            
            fig = px.bar(
                x=age_dist.index,
                y=age_dist.values,
                color=age_dist.values,
                color_continuous_scale=['#667eea', '#764ba2', '#f093fb'],
                text=age_dist.values
            )
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                showlegend=False,
                xaxis_title="Age Group",
                yaxis_title="Count"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 🌍 Location Distribution
    with col4:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🌍 Top Locations</div>', unsafe_allow_html=True)
        
        if 'location' in data.columns:
            location_dist = data['location'].value_counts().head(10)
            
            fig = go.Figure(data=[go.Bar(
                x=location_dist.values,
                y=location_dist.index,
                orientation='h',
                marker_color='#667eea',
                text=location_dist.values,
                textposition='outside'
            )])
            
            fig.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title="Follower Count"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


# ==================== 3. Time-Based Trends ====================
def render_time_based_trends(data):
    """Analyze temporal patterns and trends in social media performance"""
    st.markdown('<div class="pro-header fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-title">⏰ Time-Based Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-subtitle">Temporal patterns and optimal posting times</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # 📈 Daily Engagement Trend
    with col1:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📈 Daily Engagement Trend</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'likes' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            daily_engagement = data.groupby(pd.Grouper(key='timestamp', freq='D')).agg({
                'likes': 'sum',
                'comments': 'sum' if 'comments' in data.columns else 'count',
                'shares': 'sum' if 'shares' in data.columns else 'count'
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_engagement.index,
                y=daily_engagement['likes'],
                name='Likes',
                line=dict(color='#667eea', width=3),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.2)'
            ))
            
            if 'comments' in data.columns:
                fig.add_trace(go.Scatter(
                    x=daily_engagement.index,
                    y=daily_engagement['comments'],
                    name='Comments',
                    line=dict(color='#f093fb', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(240, 147, 251, 0.2)'
                ))
            
            fig.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 📊 Weekly Pattern Analysis
    with col2:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📅 Weekly Pattern Analysis</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'likes' in data.columns:
            data_copy = data.copy()
            data_copy['timestamp'] = pd.to_datetime(data_copy['timestamp'])
            data_copy['day_of_week'] = data_copy['timestamp'].dt.day_name()
            data_copy['hour'] = data_copy['timestamp'].dt.hour
            
            # Create pivot table for heatmap
            heatmap_data = data_copy.pivot_table(values='likes', index='day_of_week', columns='hour', aggfunc='mean', fill_value=0)
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            heatmap_data = heatmap_data.reindex([d for d in days_order if d in heatmap_data.index])
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='Viridis',
                text=heatmap_data.values.round(0),
                texttemplate='%{text}',
                textfont={"size": 8}
            ))
            
            fig.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title="Hour of Day",
                yaxis_title="Day of Week"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Insight
            best_hour = data_copy.groupby('hour')['likes'].mean().idxmax()
            am_pm = "AM" if best_hour < 12 else "PM"
            hour_12 = best_hour if best_hour <= 12 else best_hour - 12
            
            st.markdown('<div class="pro-insights">', unsafe_allow_html=True)
            st.markdown(f'💡 <strong>Posts between {hour_12}:00 {am_pm} have 2× engagement</strong>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


# ==================== 4. Predictive Analytics ====================
def render_predictive_analytics(data):
    """Predictive analytics with engagement forecasting"""
    st.markdown('<div class="pro-header fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-title">🔮 Predictive Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-subtitle">ML-powered engagement and follower growth predictions</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # 📈 Engagement Forecast
    with col1:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📈 30-Day Engagement Forecast</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'likes' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            daily_data = data.groupby(pd.Grouper(key='timestamp', freq='D'))['likes'].sum().reset_index().dropna()
            
            if len(daily_data) > 14:
                # Simple forecasting using linear regression
                from sklearn.linear_model import LinearRegression
                X = np.arange(len(daily_data)).reshape(-1, 1)
                y = daily_data['likes'].values
                
                model = LinearRegression()
                model.fit(X, y)
                
                # Predict next 30 days
                future_X = np.arange(len(daily_data), len(daily_data) + 30).reshape(-1, 1)
                future_y = model.predict(future_X)
                future_dates = pd.date_range(start=daily_data['timestamp'].iloc[-1] + timedelta(days=1), periods=30, freq='D')
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=daily_data['timestamp'],
                    y=daily_data['likes'],
                    name='Actual',
                    line=dict(color='#667eea', width=3)
                ))
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=future_y,
                    name='Forecast',
                    line=dict(color='#f093fb', width=3, dash='dash')
                ))
                
                fig.update_layout(
                    template='plotly_white',
                    height=300,
                    margin=dict(l=0, r=0, t=10, b=0),
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Insights
                current_avg = daily_data['likes'].tail(7).mean()
                forecast_avg = future_y[:7].mean()
                growth = ((forecast_avg - current_avg) / current_avg * 100) if current_avg > 0 else 0
                
                st.markdown(f"📊 **Next 7 Days**: {forecast_avg:.0f} avg daily likes ({'+' if growth > 0 else ''}{growth:.1f}%)")
            else:
                st.info("Need 14+ days of data for forecasting")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 📊 Follower Growth Prediction
    with col2:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">👥 Follower Growth Prediction</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'follower_count' in data.columns:
            daily_followers = data.groupby(pd.Grouper(key='timestamp', freq='D'))['follower_count'].last().reset_index().dropna()
            
            if len(daily_followers) > 7:
                from sklearn.linear_model import LinearRegression
                X = np.arange(len(daily_followers)).reshape(-1, 1)
                y = daily_followers['follower_count'].values
                
                model = LinearRegression()
                model.fit(X, y)
                
                # Predict next 30 days
                future_X = np.arange(len(daily_followers), len(daily_followers) + 30).reshape(-1, 1)
                future_followers = model.predict(future_X)
                future_dates = pd.date_range(start=daily_followers['timestamp'].iloc[-1] + timedelta(days=1), periods=30, freq='D')
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=daily_followers['timestamp'],
                    y=daily_followers['follower_count'],
                    name='Actual',
                    line=dict(color='#10b981', width=3)
                ))
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=future_followers,
                    name='Prediction',
                    line=dict(color='#fbbf24', width=3, dash='dash')
                ))
                
                fig.update_layout(
                    template='plotly_white',
                    height=300,
                    margin=dict(l=0, r=0, t=10, b=0),
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Insights
                current_followers = int(daily_followers['follower_count'].iloc[-1])
                predicted_followers = int(future_followers[-1])
                growth = predicted_followers - current_followers
                
                st.markdown(f"👥 **30-Day Projection**: +{growth:,} new followers")
            else:
                st.info("Need 7+ days of follower data for predictions")
        
        st.markdown('</div>', unsafe_allow_html=True)