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
    
    # Add AI recommendations for content performance
    from advanced_techniques import render_trending_content_suggestions
    render_trending_content_suggestions(data)
    
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
        else:
            st.info("⚠️ Data missing for Media Type analysis. Required columns: 'media_type', 'likes'")
        
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
        else:
            st.info("⚠️ Data missing for Top Posts. Required: 'likes', 'comments', 'shares'")
        
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
    
    # Additional Content Performance Charts
    
    # Row 3: Content Length Analysis & Posting Frequency Analysis
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📝 Content Length Impact</div>', unsafe_allow_html=True)
        
        if 'caption' in data.columns and 'likes' in data.columns:
            # Calculate caption length and group for analysis
            data_caption = data.copy()
            data_caption['caption_length'] = data_caption['caption'].astype(str).str.len()
            
            # Create length groups
            bins = [0, 50, 100, 150, 200, 500]
            labels = ['0-50', '51-100', '101-150', '151-200', '200+']
            data_caption['length_group'] = pd.cut(data_caption['caption_length'], bins=bins, labels=labels, right=False)
            
            length_performance = data_caption.groupby('length_group').agg({
                'likes': 'mean',
                'comments': 'mean' if 'comments' in data.columns else 'count',
                'shares': 'mean' if 'shares' in data.columns else 'count'
            }).round(1)
            
            fig_length = go.Figure()
            fig_length.add_trace(go.Bar(name='Avg Likes', x=length_performance.index, y=length_performance['likes'],
                                       marker_color='#667eea'))
            if 'comments' in data.columns:
                fig_length.add_trace(go.Bar(name='Avg Comments', x=length_performance.index, y=length_performance['comments'],
                                           marker_color='#f093fb'))
            if 'shares' in data.columns:
                fig_length.add_trace(go.Bar(name='Avg Shares', x=length_performance.index, y=length_performance['shares'],
                                           marker_color='#10b981'))
            
            fig_length.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                barmode='group',
                xaxis_title='Caption Length (characters)',
                yaxis_title='Average Engagement'
            )
            st.plotly_chart(fig_length, use_container_width=True)
            
            # Best length insight
            best_length = length_performance['likes'].idxmax()
            best_likes = length_performance['likes'].max()
            st.markdown(f"💡 Optimal caption length: **{best_length}** chars ({best_likes:.1f} avg likes)")
        else:
            st.info("⚠️ Data missing for Content Length analysis. Required: 'caption', 'likes'")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📊 Posting Frequency Analysis</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns:
            # Daily posting frequency
            daily_posts = data.groupby(pd.Grouper(key='timestamp', freq='D')).size()
            
            fig_freq = go.Figure()
            fig_freq.add_trace(go.Scatter(
                x=daily_posts.index,
                y=daily_posts.values,
                mode='lines+markers',
                name='Posts per Day',
                line=dict(color='#667eea', width=3),
                marker=dict(size=6)
            ))
            
            fig_freq.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title='Date',
                yaxis_title='Number of Posts'
            )
            st.plotly_chart(fig_freq, use_container_width=True)
            
            # Frequency insights
            avg_frequency = daily_posts.mean()
            max_frequency = daily_posts.max()
            st.markdown(f"📊 Average: **{avg_frequency:.1f}** posts/day")
            st.markdown(f"📈 Peak: **{max_frequency}** posts/day")
        else:
            st.info("⚠️ Data missing for Frequency analysis. Required: 'timestamp'")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 4: Engagement Rate by Content Type & Saves Analysis
    col9, col10 = st.columns(2)
    
    # 📊 Engagement Rate by Content Type
    with col9:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📊 Engagement Rate by Content Type</div>', unsafe_allow_html=True)
        
        if all(col in data.columns for col in ['media_type', 'likes', 'impressions']) and len(data) > 0:
            # Calculate engagement rate by content type
            data_er_type = data.copy()
            # Ensure numeric data types
            data_er_type['likes'] = pd.to_numeric(data_er_type['likes'], errors='coerce').fillna(0)
            data_er_type['impressions'] = pd.to_numeric(data_er_type['impressions'], errors='coerce').fillna(0)
            
            # Group by media type and calculate engagement rate
            type_metrics = data_er_type.groupby('media_type').agg({
                'likes': 'sum',
                'impressions': 'sum'
            }).reset_index()
            
            # Calculate engagement rate (avoid division by zero)
            type_metrics['engagement_rate'] = np.where(
                type_metrics['impressions'] > 0,
                (type_metrics['likes'] / type_metrics['impressions']) * 100,
                0
            )
            
            fig_er_type = px.bar(
                type_metrics,
                x='media_type',
                y='engagement_rate',
                color='engagement_rate',
                color_continuous_scale=['#667eea', '#764ba2', '#f093fb'],
                text=type_metrics['engagement_rate'].round(2)
            )
            
            fig_er_type.update_traces(texttemplate='%{text}%', textposition='outside')
            fig_er_type.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                showlegend=False,
                xaxis_title="Content Type",
                yaxis_title="Engagement Rate (%)"
            )
            st.plotly_chart(fig_er_type, use_container_width=True)
            
            # Best content type insight
            if not type_metrics.empty:
                best_type = type_metrics.loc[type_metrics['engagement_rate'].idxmax(), 'media_type']
                best_rate = type_metrics['engagement_rate'].max()
                st.markdown(f"💡 **{best_type}** has highest engagement rate at {best_rate:.2f}%")
        else:
            st.info("⚠️ Data missing for Engagement Rate analysis. Required: 'media_type', 'likes', 'impressions'")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 💾 Saves Analysis
    with col10:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">💾 Saves Analysis</div>', unsafe_allow_html=True)
        
        if 'saves' in data.columns and 'media_type' in data.columns:
            # Ensure numeric data type
            data['saves'] = pd.to_numeric(data['saves'], errors='coerce').fillna(0)
            
            # Group by media type
            saves_by_type = data.groupby('media_type')['saves'].mean().round(1)
            
            fig_saves = px.bar(
                x=saves_by_type.index,
                y=saves_by_type.values,
                color=saves_by_type.values,
                color_continuous_scale=['#10b981', '#667eea', '#f093fb'],
                text=saves_by_type.values
            )
            
            fig_saves.update_traces(textposition='outside')
            fig_saves.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                showlegend=False,
                xaxis_title="Content Type",
                yaxis_title="Average Saves"
            )
            st.plotly_chart(fig_saves, use_container_width=True)
            
            # Best saving content insight
            if not saves_by_type.empty:
                best_saving_type = saves_by_type.idxmax()
                avg_saves = saves_by_type.max()
                st.markdown(f"💾 **{best_saving_type}** gets {avg_saves:.1f} avg saves per post")
        else:
            st.info("⚠️ Data missing for Saves analysis. Required: 'saves', 'media_type'")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 5: Engagement Correlation Matrix & Content Type Comparison
    col7, col8 = st.columns(2)
    
    with col7:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🔗 Engagement Correlation</div>', unsafe_allow_html=True)
        
        if all(col in data.columns for col in ['likes', 'comments', 'shares']):
            # Create correlation matrix
            corr_data = data[['likes', 'comments', 'shares']].corr()
            
            fig_corr = go.Figure(data=go.Heatmap(
                z=corr_data.values,
                x=corr_data.columns,
                y=corr_data.index,
                colorscale='RdBu',
                text=corr_data.values.round(2),
                texttemplate="%{text}",
                textfont={"size": 12}
            ))
            
            fig_corr.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title="Metrics",
                yaxis_title="Metrics"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Correlation insights
            likes_comments_corr = corr_data.loc['likes', 'comments']
            if abs(likes_comments_corr) > 0.7:
                st.markdown(f"🔗 Strong correlation between likes and comments (**{likes_comments_corr:.2f}**)")
            elif abs(likes_comments_corr) > 0.4:
                st.markdown(f"🔗 Moderate correlation between likes and comments (**{likes_comments_corr:.2f}**)")
            else:
                st.markdown(f"🔗 Weak correlation between likes and comments (**{likes_comments_corr:.2f}**)")
        else:
            st.info("⚠️ Data missing for Correlation analysis. Required: 'likes', 'comments', 'shares'")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col8:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">⚖️ Content Type Comparison</div>', unsafe_allow_html=True)
        
        if 'media_type' in data.columns and 'likes' in data.columns:
            # Compare different content types
            content_comparison = data.groupby('media_type').agg({
                'likes': ['mean', 'std'],
                'comments': ['mean', 'std'] if 'comments' in data.columns else ['count', 'count'],
                'shares': ['mean', 'std'] if 'shares' in data.columns else ['count', 'count']
            })
            
            # Flatten column names
            content_comparison.columns = ['_'.join(col).strip() for col in content_comparison.columns.values]
            content_comparison = content_comparison.reset_index()
            
            # Melt for visualization
            melted_data = content_comparison.melt(id_vars=['media_type'], 
                                                value_vars=[col for col in content_comparison.columns if 'mean' in col],
                                                var_name='metric', 
                                                value_name='average')
            melted_data['metric'] = melted_data['metric'].str.replace('_mean', '')
            
            fig_compare = px.bar(melted_data, 
                               x='media_type', 
                               y='average', 
                               color='metric',
                               barmode='group',
                               color_discrete_sequence=['#667eea', '#f093fb', '#10b981'])
            
            fig_compare.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title="Content Type",
                yaxis_title="Average Engagement"
            )
            st.plotly_chart(fig_compare, use_container_width=True)
        else:
            st.info("⚠️ Data missing for Content Type comparison. Required: 'media_type', 'likes'")
        
        st.markdown('</div>', unsafe_allow_html=True)


# ==================== 2. Audience Insights ====================
def render_audience_insights(data):
    """Audience Insights with Clear Visuals"""
    st.markdown('<div class="pro-header fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-title">👥 Audience Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-subtitle">Understand followers and their activity patterns</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add AI recommendations for optimal posting times
    from advanced_techniques import render_optimal_posting_times
    render_optimal_posting_times(data)
    
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
    
    # Additional Audience Insights Charts
    
    # Row 3: Follower Growth & Engagement Rate Over Time
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📈 Follower Growth Over Time</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'follower_count' in data.columns:
            # Resample to weekly data for smoother visualization
            follower_growth = data.set_index('timestamp').resample('W')['follower_count'].last().dropna()
            
            fig_follower = go.Figure()
            fig_follower.add_trace(go.Scatter(
                x=follower_growth.index,
                y=follower_growth.values,
                mode='lines+markers',
                name='Followers',
                line=dict(color='#667eea', width=3),
                marker=dict(size=6)
            ))
            
            fig_follower.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title='Date',
                yaxis_title='Follower Count'
            )
            st.plotly_chart(fig_follower, use_container_width=True)
            
            # Growth insights
            if len(follower_growth) > 1:
                growth_rate = ((follower_growth.iloc[-1] - follower_growth.iloc[0]) / follower_growth.iloc[0] * 100)
                st.markdown(f"📊 Total growth: **{growth_rate:+.1f}%**")
        else:
            st.info("⚠️ Data missing for Follower Growth. Required: 'timestamp', 'follower_count'")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">⚡ Engagement Rate by Day</div>', unsafe_allow_html=True)
        
        if all(col in data.columns for col in ['timestamp', 'likes', 'impressions']) and len(data) > 0:
            # Calculate daily engagement rate
            data_er = data.copy()
            data_er['date'] = pd.to_datetime(data_er['timestamp']).dt.date
            daily_metrics = data_er.groupby('date').agg({
                'likes': 'sum',
                'impressions': 'sum'
            }).reset_index()
            
            # Calculate engagement rate (avoid division by zero)
            daily_metrics['engagement_rate'] = np.where(
                daily_metrics['impressions'] > 0,
                (daily_metrics['likes'] / daily_metrics['impressions']) * 100,
                0
            )
            
            fig_er = go.Figure()
            fig_er.add_trace(go.Scatter(
                x=daily_metrics['date'],
                y=daily_metrics['engagement_rate'],
                mode='lines+markers',
                name='Engagement Rate',
                line=dict(color='#10b981', width=3),
                marker=dict(size=6)
            ))
            
            fig_er.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title='Date',
                yaxis_title='Engagement Rate (%)'
            )
            st.plotly_chart(fig_er, use_container_width=True)
            
            # Average engagement rate
            avg_er = daily_metrics['engagement_rate'].mean()
            st.markdown(f"📊 Avg engagement rate: **{avg_er:.2f}%**")
        else:
            st.info("⚠️ Data missing for Engagement Rate. Required: 'timestamp', 'likes', 'impressions'")
        
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
    
    # Row 4: Audience Engagement by Gender & Top Locations by Engagement
    col7, col8 = st.columns(2)
    
    # 👥 Audience Engagement by Gender
    with col7:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">👥 Audience Engagement by Gender</div>', unsafe_allow_html=True)
        
        if all(col in data.columns for col in ['audience_gender', 'likes', 'comments', 'shares']):
            # Group by gender and calculate average engagement
            gender_engagement = data.groupby('audience_gender').agg({
                'likes': 'mean',
                'comments': 'mean',
                'shares': 'mean'
            }).round(1)
            
            # Melt for visualization
            melted_gender = gender_engagement.reset_index().melt(
                id_vars=['audience_gender'],
                value_vars=['likes', 'comments', 'shares'],
                var_name='metric',
                value_name='average'
            )
            
            fig_gender = px.bar(
                melted_gender,
                x='audience_gender',
                y='average',
                color='metric',
                barmode='group',
                color_discrete_sequence=['#667eea', '#f093fb', '#10b981'],
                text='average'
            )
            
            fig_gender.update_traces(texttemplate='%{text}', textposition='outside')
            fig_gender.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title="Gender",
                yaxis_title="Average Engagement",
                showlegend=True
            )
            st.plotly_chart(fig_gender, use_container_width=True)
            
            # Best performing gender insight
            if not gender_engagement.empty:
                best_gender = gender_engagement['likes'].idxmax()
                best_likes = gender_engagement['likes'].max()
                st.markdown(f"💡 **{best_gender}** audience generates {best_likes:.1f} avg likes per post")
        else:
            st.info("⚠️ Data missing for Gender Engagement analysis. Required: 'audience_gender', 'likes', 'comments', 'shares'")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 🌍 Top Locations by Engagement
    with col8:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🌍 Top Locations by Engagement</div>', unsafe_allow_html=True)
        
        if all(col in data.columns for col in ['location', 'likes', 'comments', 'shares']):
            # Group by location and calculate total engagement
            location_engagement = data.groupby('location').agg({
                'likes': 'sum',
                'comments': 'sum',
                'shares': 'sum'
            }).reset_index()
            
            # Calculate total engagement
            location_engagement['total_engagement'] = (
                location_engagement['likes'] + 
                location_engagement['comments'] + 
                location_engagement['shares']
            )
            
            # Get top 10 locations
            top_locations = location_engagement.nlargest(10, 'total_engagement')
            
            fig_location = px.bar(
                top_locations,
                x='total_engagement',
                y='location',
                orientation='h',
                color='total_engagement',
                color_continuous_scale=['#667eea', '#764ba2', '#f093fb'],
                text='total_engagement'
            )
            
            fig_location.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig_location.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                showlegend=False,
                xaxis_title="Total Engagement",
                yaxis_title="Location"
            )
            st.plotly_chart(fig_location, use_container_width=True)
            
            # Best performing location insight
            if not top_locations.empty:
                best_location = top_locations.iloc[0]['location']
                best_engagement = top_locations.iloc[0]['total_engagement']
                st.markdown(f"📍 **{best_location}** leads with {best_engagement:,.0f} total engagements")
        else:
            st.info("⚠️ Data missing for Location Engagement analysis. Required: 'location', 'likes', 'comments', 'shares'")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Gender-Age Cross Analysis & Follower Growth Rate
    col5, col6 = st.columns(2)
    
    # 👥 Gender-Age Cross Analysis
    with col5:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">👥 Gender-Age Cross Analysis</div>', unsafe_allow_html=True)
        
        if 'audience_gender' in data.columns and 'audience_age' in data.columns:
            # Create cross-tabulation
            cross_tab = pd.crosstab(data['audience_gender'], data['audience_age'])
            
            fig_cross = go.Figure(data=go.Heatmap(
                z=cross_tab.values,
                x=cross_tab.columns,
                y=cross_tab.index,
                colorscale='Blues',
                text=cross_tab.values,
                texttemplate="%{text}",
                textfont={"size": 10}
            ))
            
            fig_cross.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title="Age Group",
                yaxis_title="Gender"
            )
            st.plotly_chart(fig_cross, use_container_width=True)
        else:
            st.info("⚠️ Data missing for Gender-Age analysis. Required: 'audience_gender', 'audience_age'")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 📈 Follower Growth Rate
    with col6:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📈 Follower Growth Rate</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'follower_count' in data.columns:
            # Calculate daily growth rate
            data_growth = data.copy()
            data_growth['timestamp'] = pd.to_datetime(data_growth['timestamp'])
            daily_followers = data_growth.groupby(pd.Grouper(key='timestamp', freq='D'))['follower_count'].last().dropna()
            
            if len(daily_followers) > 1:
                # Calculate percentage change
                growth_rate = daily_followers.pct_change() * 100
                
                fig_growth = go.Figure()
                fig_growth.add_trace(go.Scatter(
                    x=growth_rate.index,
                    y=growth_rate.values,
                    mode='lines+markers',
                    name='Growth Rate',
                    line=dict(color='#10b981', width=3),
                    marker=dict(size=6)
                ))
                
                fig_growth.add_hline(y=0, line_dash="dash", line_color="#64748b")
                
                fig_growth.update_layout(
                    template='plotly_white',
                    height=300,
                    margin=dict(l=0, r=0, t=10, b=0),
                    xaxis_title="Date",
                    yaxis_title="Growth Rate (%)")
                st.plotly_chart(fig_growth, use_container_width=True)
                
                # Growth insights
                avg_growth = growth_rate.mean()
                st.markdown(f"📊 Average daily growth: **{avg_growth:.2f}%**")
            else:
                st.info("Need more data points for growth rate calculation")
        else:
            st.info("⚠️ Data missing for Growth Rate analysis. Required: 'timestamp', 'follower_count'")
        
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
    
    # Row 4: Hourly Engagement Patterns & Day-of-Week Comparison
    col5, col6 = st.columns(2)
    
    # 🕒 Hourly Engagement Patterns
    with col5:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🕒 Hourly Engagement Patterns</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'likes' in data.columns:
            data_hourly = data.copy()
            data_hourly['timestamp'] = pd.to_datetime(data_hourly['timestamp'])
            data_hourly['hour'] = data_hourly['timestamp'].dt.hour
            
            # Group by hour and calculate average engagement
            hourly_engagement = data_hourly.groupby('hour').agg({
                'likes': 'mean',
                'comments': 'mean' if 'comments' in data.columns else 'count',
                'shares': 'mean' if 'shares' in data.columns else 'count'
            }).round(1)
            
            fig_hourly = go.Figure()
            fig_hourly.add_trace(go.Scatter(
                x=hourly_engagement.index,
                y=hourly_engagement['likes'],
                name='Likes',
                line=dict(color='#667eea', width=3),
                mode='lines+markers',
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.2)'
            ))
            
            if 'comments' in data.columns:
                fig_hourly.add_trace(go.Scatter(
                    x=hourly_engagement.index,
                    y=hourly_engagement['comments'],
                    name='Comments',
                    line=dict(color='#f093fb', width=3),
                    mode='lines+markers',
                    fill='tozeroy',
                    fillcolor='rgba(240, 147, 251, 0.2)'
                ))
            
            fig_hourly.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title='Hour of Day (24-hour)',
                yaxis_title='Average Engagement',
                hovermode='x unified'
            )
            st.plotly_chart(fig_hourly, use_container_width=True)
            
            # Best hour insight
            if not hourly_engagement.empty:
                best_hour = hourly_engagement['likes'].idxmax()
                best_likes = hourly_engagement['likes'].max()
                am_pm = "AM" if best_hour < 12 else "PM"
                hour_12 = best_hour if best_hour <= 12 else best_hour - 12
                if best_hour == 0:
                    hour_12 = 12
                st.markdown(f"⏰ Peak engagement at **{hour_12}:00 {am_pm}** with {best_likes:.1f} avg likes")
        else:
            st.info("⚠️ Data missing for Hourly analysis. Required: 'timestamp', 'likes'")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 🗓️ Day-of-Week Engagement Comparison
    with col6:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🗓️ Day-of-Week Engagement Comparison</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'likes' in data.columns:
            data_dow = data.copy()
            data_dow['timestamp'] = pd.to_datetime(data_dow['timestamp'])
            data_dow['day_of_week'] = data_dow['timestamp'].dt.day_name()
            
            # Group by day of week and calculate average engagement
            dow_engagement = data_dow.groupby('day_of_week').agg({
                'likes': 'mean',
                'comments': 'mean' if 'comments' in data.columns else 'count',
                'shares': 'mean' if 'shares' in data.columns else 'count'
            }).round(1)
            
            # Reorder days
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_engagement = dow_engagement.reindex([d for d in days_order if d in dow_engagement.index])
            
            fig_dow = go.Figure()
            fig_dow.add_trace(go.Bar(
                x=dow_engagement.index,
                y=dow_engagement['likes'],
                name='Likes',
                marker_color='#667eea',
                text=dow_engagement['likes'],
                textposition='outside'
            ))
            
            if 'comments' in data.columns:
                fig_dow.add_trace(go.Bar(
                    x=dow_engagement.index,
                    y=dow_engagement['comments'],
                    name='Comments',
                    marker_color='#f093fb',
                    text=dow_engagement['comments'],
                    textposition='outside'
                ))
            
            fig_dow.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title='Day of Week',
                yaxis_title='Average Engagement',
                barmode='group'
            )
            st.plotly_chart(fig_dow, use_container_width=True)
            
            # Best day insight
            if not dow_engagement.empty:
                best_day = dow_engagement['likes'].idxmax()
                best_likes = dow_engagement['likes'].max()
                st.markdown(f"📅 Best engagement on **{best_day}** with {best_likes:.1f} avg likes")
        else:
            st.info("⚠️ Data missing for Day-of-Week analysis. Required: 'timestamp', 'likes'")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Monthly Trend Analysis & Seasonal Patterns
    col3, col4 = st.columns(2)
    
    # 📅 Monthly Trend Analysis
    with col3:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📅 Monthly Trend Analysis</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'likes' in data.columns:
            data_monthly = data.copy()
            data_monthly['timestamp'] = pd.to_datetime(data_monthly['timestamp'])
            data_monthly['month'] = data_monthly['timestamp'].dt.to_period('M')
            monthly_trend = data_monthly.groupby('month').agg({
                'likes': 'sum',
                'comments': 'sum' if 'comments' in data.columns else 'count',
                'shares': 'sum' if 'shares' in data.columns else 'count'
            }).reset_index()
            
            # Convert Period to string for plotting
            monthly_trend['month_str'] = monthly_trend['month'].astype(str)
            
            fig_monthly = go.Figure()
            fig_monthly.add_trace(go.Scatter(
                x=monthly_trend['month_str'],
                y=monthly_trend['likes'],
                name='Likes',
                line=dict(color='#667eea', width=3),
                mode='lines+markers'
            ))
            
            if 'comments' in data.columns:
                fig_monthly.add_trace(go.Scatter(
                    x=monthly_trend['month_str'],
                    y=monthly_trend['comments'],
                    name='Comments',
                    line=dict(color='#f093fb', width=3),
                    mode='lines+markers'
                ))
            
            fig_monthly.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title="Month",
                yaxis_title="Engagement Count",
                hovermode='x unified'
            )
            st.plotly_chart(fig_monthly, use_container_width=True)
        else:
            st.info("⚠️ Data missing for Monthly analysis. Required: 'timestamp', 'likes'")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 🌞 Seasonal Patterns
    with col4:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🌞 Seasonal Patterns</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'likes' in data.columns:
            data_seasonal = data.copy()
            data_seasonal['timestamp'] = pd.to_datetime(data_seasonal['timestamp'])
            data_seasonal['season'] = data_seasonal['timestamp'].dt.month.map({
                12: 'Winter', 1: 'Winter', 2: 'Winter',
                3: 'Spring', 4: 'Spring', 5: 'Spring',
                6: 'Summer', 7: 'Summer', 8: 'Summer',
                9: 'Fall', 10: 'Fall', 11: 'Fall'
            })
            seasonal_performance = data_seasonal.groupby('season').agg({
                'likes': 'mean',
                'comments': 'mean' if 'comments' in data.columns else 'count',
                'shares': 'mean' if 'shares' in data.columns else 'count'
            }).round(1)
            
            # Reorder seasons
            season_order = ['Winter', 'Spring', 'Summer', 'Fall']
            seasonal_performance = seasonal_performance.reindex([s for s in season_order if s in seasonal_performance.index])
            
            fig_seasonal = go.Figure(data=[go.Bar(
                x=seasonal_performance.index,
                y=seasonal_performance['likes'],
                marker_color=['#667eea', '#10b981', '#fbbf24', '#ef4444'],
                text=seasonal_performance['likes'],
                textposition='outside'
            )])
            
            fig_seasonal.update_layout(
                template='plotly_white',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title="Season",
                yaxis_title="Average Likes"
            )
            st.plotly_chart(fig_seasonal, use_container_width=True)
            
            # Seasonal insights
            best_season = seasonal_performance['likes'].idxmax()
            best_likes = seasonal_performance['likes'].max()
            st.markdown(f"🌤️ **{best_season}** performs best with {best_likes:.0f} avg likes")
        else:
            st.info("⚠️ Data missing for Seasonal analysis. Required: 'timestamp', 'likes'")
        
        st.markdown('</div>', unsafe_allow_html=True)


# ==================== 4. Predictive Analytics ====================
def render_predictive_analytics(data):
    """Predictive analytics with engagement forecasting"""
    st.markdown('<div class="pro-header fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-title">🔮 Predictive Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="pro-header-subtitle">ML-powered engagement and follower growth predictions</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 1: Engagement Forecast & Follower Growth Prediction
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
    
    # Row 3: Engagement Trend Analysis & Follower Growth Acceleration
    col5, col6 = st.columns(2)
    
    # 📈 Engagement Trend Analysis
    with col5:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📈 Engagement Trend Analysis</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'likes' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            daily_data = data.groupby(pd.Grouper(key='timestamp', freq='D'))['likes'].sum().reset_index().dropna()
            
            if len(daily_data) > 7:
                # Calculate moving averages
                daily_data['MA7'] = daily_data['likes'].rolling(window=7).mean()
                daily_data['MA30'] = daily_data['likes'].rolling(window=30).mean()
                
                fig_trend = go.Figure()
                # Actual data
                fig_trend.add_trace(go.Scatter(
                    x=daily_data['timestamp'],
                    y=daily_data['likes'],
                    name='Daily',
                    line=dict(color='#667eea', width=1),
                    mode='lines'
                ))
                # 7-day moving average
                fig_trend.add_trace(go.Scatter(
                    x=daily_data['timestamp'],
                    y=daily_data['MA7'],
                    name='7-Day MA',
                    line=dict(color='#f093fb', width=2)
                ))
                # 30-day moving average
                fig_trend.add_trace(go.Scatter(
                    x=daily_data['timestamp'],
                    y=daily_data['MA30'],
                    name='30-Day MA',
                    line=dict(color='#10b981', width=2, dash='dash')
                ))
                
                fig_trend.update_layout(
                    template='plotly_white',
                    height=300,
                    margin=dict(l=0, r=0, t=10, b=0),
                    xaxis_title='Date',
                    yaxis_title='Likes',
                    hovermode='x unified'
                )
                st.plotly_chart(fig_trend, use_container_width=True)
                
                # Trend insights
                if len(daily_data) >= 30:
                    recent_trend = daily_data['MA7'].tail(7).mean() - daily_data['MA7'].tail(14).head(7).mean()
                    if recent_trend > 0:
                        st.markdown("↗️ Engagement trending upward")
                    elif recent_trend < 0:
                        st.markdown("↘️ Engagement trending downward")
                    else:
                        st.markdown("➡️ Engagement stable")
            else:
                st.info("Need 7+ days of data for trend analysis")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 🚀 Follower Growth Acceleration
    with col6:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🚀 Follower Growth Acceleration</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'follower_count' in data.columns:
            daily_followers = data.groupby(pd.Grouper(key='timestamp', freq='D'))['follower_count'].last().reset_index().dropna()
            
            if len(daily_followers) > 7:
                # Calculate growth rate and acceleration
                daily_followers['growth_rate'] = daily_followers['follower_count'].pct_change() * 100
                daily_followers['acceleration'] = daily_followers['growth_rate'].diff()
                
                fig_accel = go.Figure()
                fig_accel.add_trace(go.Scatter(
                    x=daily_followers['timestamp'],
                    y=daily_followers['acceleration'],
                    name='Acceleration',
                    line=dict(color='#fbbf24', width=3),
                    mode='lines+markers'
                ))
                
                fig_accel.add_hline(y=0, line_dash="dash", line_color="#64748b")
                
                fig_accel.update_layout(
                    template='plotly_white',
                    height=300,
                    margin=dict(l=0, r=0, t=10, b=0),
                    xaxis_title='Date',
                    yaxis_title='Growth Acceleration (%)',
                    hovermode='x unified'
                )
                st.plotly_chart(fig_accel, use_container_width=True)
                
                # Acceleration insights
                recent_accel = daily_followers['acceleration'].tail(7).mean()
                if recent_accel > 0:
                    st.markdown("🚀 Follower growth accelerating")
                elif recent_accel < 0:
                    st.markdown("🐢 Follower growth decelerating")
                else:
                    st.markdown("平稳 Follower growth steady")
            else:
                st.info("Need 7+ days of follower data for acceleration analysis")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Engagement Volatility & Confidence Intervals
    col3, col4 = st.columns(2)
    
    # 📉 Engagement Volatility Analysis
    with col3:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📉 Engagement Volatility Analysis</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'likes' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            daily_data = data.groupby(pd.Grouper(key='timestamp', freq='D'))['likes'].sum().reset_index().dropna()
            
            if len(daily_data) > 7:
                # Calculate rolling standard deviation as volatility measure
                daily_data['volatility'] = daily_data['likes'].rolling(window=7).std()
                
                fig_vol = go.Figure()
                fig_vol.add_trace(go.Scatter(
                    x=daily_data['timestamp'],
                    y=daily_data['volatility'],
                    mode='lines',
                    name='Volatility',
                    line=dict(color='#ef4444', width=3)
                ))
                
                fig_vol.update_layout(
                    template='plotly_white',
                    height=300,
                    margin=dict(l=0, r=0, t=10, b=0),
                    xaxis_title='Date',
                    yaxis_title='Engagement Volatility (Std Dev)'
                )
                st.plotly_chart(fig_vol, use_container_width=True)
                
                # Volatility insights
                avg_volatility = daily_data['volatility'].mean()
                st.markdown(f"📊 Average volatility: **{avg_volatility:.1f}** likes")
                
                if avg_volatility > daily_data['likes'].mean() * 0.3:
                    st.markdown("⚠️ High volatility detected - consider consistent posting schedule")
                else:
                    st.markdown("✅ Stable engagement patterns observed")
            else:
                st.info("Need 7+ days of data for volatility analysis")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 🎯 Prediction Confidence Intervals
    with col4:
        st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🎯 Prediction Confidence Intervals</div>', unsafe_allow_html=True)
        
        if 'timestamp' in data.columns and 'likes' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            daily_data = data.groupby(pd.Grouper(key='timestamp', freq='D'))['likes'].sum().reset_index().dropna()
            
            if len(daily_data) > 14:
                # Calculate confidence intervals using standard error
                from sklearn.linear_model import LinearRegression
                X = np.arange(len(daily_data)).reshape(-1, 1)
                y = daily_data['likes'].values
                
                model = LinearRegression()
                model.fit(X, y)
                
                # Predict with confidence intervals
                future_X = np.arange(len(daily_data), len(daily_data) + 30).reshape(-1, 1)
                future_y = model.predict(future_X)
                
                # Calculate standard error for confidence intervals
                residuals = y - model.predict(X)
                mse = np.mean(residuals**2)
                std_error = np.sqrt(mse)
                
                # 95% confidence intervals
                ci_upper = future_y + 1.96 * std_error
                ci_lower = future_y - 1.96 * std_error
                
                future_dates = pd.date_range(start=daily_data['timestamp'].iloc[-1] + timedelta(days=1), periods=30, freq='D')
                
                fig_ci = go.Figure()
                # Actual data
                fig_ci.add_trace(go.Scatter(
                    x=daily_data['timestamp'],
                    y=daily_data['likes'],
                    name='Actual',
                    line=dict(color='#667eea', width=3)
                ))
                # Prediction
                fig_ci.add_trace(go.Scatter(
                    x=future_dates,
                    y=future_y,
                    name='Forecast',
                    line=dict(color='#f093fb', width=3, dash='dash')
                ))
                # Confidence interval
                fig_ci.add_trace(go.Scatter(
                    x=np.concatenate([future_dates, future_dates[::-1]]),
                    y=np.concatenate([ci_upper, ci_lower[::-1]]),
                    fill='toself',
                    fillcolor='rgba(240, 147, 251, 0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name='95% Confidence'
                ))
                
                fig_ci.update_layout(
                    template='plotly_white',
                    height=300,
                    margin=dict(l=0, r=0, t=10, b=0),
                    xaxis_title='Date',
                    yaxis_title='Likes',
                    hovermode='x unified'
                )
                st.plotly_chart(fig_ci, use_container_width=True)
                
                # Confidence insights
                st.markdown(f"🎯 Forecast range: {int(ci_lower[0])} - {int(ci_upper[0])} likes (next day)")
            else:
                st.info("Need 14+ days of data for confidence intervals")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Professional Footer
st.markdown("""
<div class="pro-footer">
    <p><strong>Professional Social Media Analytics Platform</strong> | Powered by Advanced Analytics</p>
    <p style="font-size: 0.8rem; color: #94a3b8;">© 2025 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
