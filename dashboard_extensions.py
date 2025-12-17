"""
Dashboard Extensions Module
Additional charts and components for deep dive analysis
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def render_engagement_funnel(data):
    """Render an engagement funnel chart (Impressions -> Reach -> Engagement)"""
    st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-chart-title">🔻 Engagement Funnel</div>', unsafe_allow_html=True)
    
    if all(col in data.columns for col in ['impressions', 'reach', 'likes', 'comments', 'shares']):
        # Aggregate metrics
        total_impressions = data['impressions'].sum()
        total_reach = data['reach'].sum()
        
        # Calculate distinct engagement
        # Assuming simple sum for engagement actions
        total_engagement = data['likes'].sum() + data['comments'].sum() + data['shares'].sum()
        
        # Create funnel stages
        stages = ['Impressions', 'Reach', 'Engagement']
        values = [total_impressions, total_reach, total_engagement]
        
        fig = go.Figure(go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent previous",
            marker = {"color": ["#667eea", "#764ba2", "#10b981"]}
        ))
        
        fig.update_layout(
            template='plotly_white',
            height=350,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insight
        if total_reach > 0:
            conv_rate = (total_engagement / total_reach) * 100
            st.markdown(f"💡 **Conversion Rate:** {conv_rate:.1f}% of reached users engaged with content")
            
    else:
        st.info("Required metrics (impressions, reach, engagement) not available for funnel analysis")
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_metric_radar(data):
    """Render a radar chart comparing media types"""
    st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-chart-title">🕸️ Media Performance Radar</div>', unsafe_allow_html=True)
    
    if 'media_type' in data.columns and all(col in data.columns for col in ['likes', 'comments', 'shares', 'reach']):
        # Normalize metrics for fair comparison
        metrics = ['likes', 'comments', 'shares', 'reach']
        
        # Group by media type
        grouped = data.groupby('media_type')[metrics].mean()
        
        # Max scaling for radar chart (0-1 range)
        normalized = grouped.copy()
        for col in metrics:
            if normalized[col].max() > 0:
                normalized[col] = normalized[col] / normalized[col].max()
        
        fig = go.Figure()
        
        colors = ['#667eea', '#10b981', '#f59e0b', '#ef4444']
        
        for i, (media_type, row) in enumerate(normalized.iterrows()):
            color = colors[i % len(colors)]
            fig.add_trace(go.Scatterpolar(
                r=row.values,
                theta=[m.title() for m in metrics],
                fill='toself',
                name=str(media_type),
                line=dict(color=color)
            ))
            
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            template='plotly_white',
            height=400,
            margin=dict(l=40, r=40, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info("Missing media type or metric columns for radar analysis")
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_treemap_content(data):
    """Render a treemap of content performance"""
    st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-chart-title">📦 Content Distribution Treemap</div>', unsafe_allow_html=True)
    
    if 'media_type' in data.columns and 'likes' in data.columns:
        # Prepare hierarchy
        # If we have hashtags, we could use top hashtag per post, otherwise just use media type -> engagement
        
        df = data.copy()
        df['total_engagement'] = df['likes'] + df.get('comments', 0) + df.get('shares', 0)
        
        # Simplified grouping for visual clarity
        # Group by Media Type -> Top 5 Posts (by ID or Caption snippet)
        
        # Just purely Media Type distribution for now might be too simple. 
        # Let's try to simulate a sub-category if possible, or just individual posts if not too many.
        # If many posts, bin them.
        
        # Let's do Media Type -> Engagement bin
        df['engagement_level'] = pd.qcut(df['total_engagement'], q=3, labels=['Low', 'Medium', 'High'])
        
        grouped = df.groupby(['media_type', 'engagement_level']).size().reset_index(name='count')
        grouped['avg_engagement'] = df.groupby(['media_type', 'engagement_level'])['total_engagement'].mean().values
        
        fig = px.treemap(
            grouped,
            path=[px.Constant("All Content"), 'media_type', 'engagement_level'],
            values='count',
            color='avg_engagement',
            color_continuous_scale='Purples'
        )
        
        fig.update_layout(
            template='plotly_white',
            height=350,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_correlation_heatmap(data):
    """Render correlation matrix"""
    st.markdown('<div class="pro-chart-container fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-chart-title">🌡️ Metric Correlations</div>', unsafe_allow_html=True)
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    # Filter for relevant metrics
    relevant = [c for c in numeric_cols if c in ['likes', 'comments', 'shares', 'saves', 'impressions', 'reach', 'follower_count', 'sentiment_score', 'subjectivity']]
    
    if len(relevant) > 1:
        corr = data[relevant].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=[c.title().replace('_', ' ') for c in corr.columns],
            y=[c.title().replace('_', ' ') for c in corr.index],
            colorscale='RdBu',
            zmin=-1, zmax=1,
            text=np.round(corr.values, 2),
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            template='plotly_white',
            height=400,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough numeric metrics for correlation analysis")
        
    st.markdown('</div>', unsafe_allow_html=True)
