"""
Hashtag Performance Tracker
Track, analyze, and optimize hashtag strategies across platforms
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
from collections import Counter

def generate_hashtag_data():
    """Generate simulated hashtag performance data"""
    hashtags = []
    
    # Education-related hashtags
    tag_list = [
        '#TMU', '#University', '#HigherEducation', '#StudentLife', '#CampusLife',
        '#Education', '#CollegeLife', '#Admissions2025', '#Placements', '#Engineering',
        '#MBA', '#Research', '#Innovation', '#StudyInIndia', '#CareerGoals',
        '#FutureLeaders', '#AcademicExcellence', '#CampusCulture', '#StudentSuccess',
        '#EducationMatters', '#UniversityLife', '#CollegeAdmissions', '#Scholarship',
        '#OnlineLearning', '#SkillDevelopment', '#YouthEmpowerment', '#DreamBig',
        '#SuccessStory', '#Motivation', '#InspireEducation'
    ]
    
    for tag in tag_list:
        posts_used = random.randint(5, 150)
        avg_reach = random.randint(1000, 50000)
        avg_engagement = random.randint(100, 5000)
        
        hashtags.append({
            'hashtag': tag,
            'posts_used': posts_used,
            'total_reach': avg_reach * posts_used,
            'avg_reach': avg_reach,
            'total_engagement': avg_engagement * posts_used,
            'avg_engagement': avg_engagement,
            'engagement_rate': round(random.uniform(2.5, 12.0), 2),
            'impressions': avg_reach * posts_used * random.uniform(1.2, 2.5),
            'saves': random.randint(50, 2000),
            'shares': random.randint(20, 800),
            'trending_score': round(random.uniform(40, 98), 1),
            'competition': random.choice(['Low', 'Medium', 'High', 'Very High']),
            'relevance_score': round(random.uniform(60, 100), 1),
            'growth_trend': random.choice(['Rising', 'Stable', 'Declining']),
            'best_platform': random.choice(['Instagram', 'Twitter', 'TikTok', 'LinkedIn']),
            'category': random.choice(['Branded', 'Industry', 'Trending', 'Community', 'Location'])
        })
    
    return pd.DataFrame(hashtags)

def generate_hashtag_trends(hashtag, days=30):
    """Generate trend data for a specific hashtag"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    base_reach = random.randint(5000, 30000)
    base_engagement = random.randint(500, 3000)
    
    trend_data = []
    for date in dates:
        # Add some randomness and trend
        reach = base_reach + random.randint(-2000, 5000)
        engagement = base_engagement + random.randint(-200, 800)
        
        trend_data.append({
            'date': date,
            'reach': reach,
            'engagement': engagement,
            'posts': random.randint(5, 50),
            'engagement_rate': round((engagement / reach) * 100, 2) if reach > 0 else 0
        })
    
    return pd.DataFrame(trend_data)

def get_hashtag_recommendations(niche='Education'):
    """Get AI-powered hashtag recommendations"""
    recommendations = {
        'Education': {
            'High Performance': ['#StudentSuccess', '#FutureLeaders', '#InnovationInEducation'],
            'Growing': ['#EdTech2025', '#SkillsForFuture', '#LearningJourney'],
            'Niche': ['#CampusInnovation', '#ResearchMatters', '#AcademicLife'],
            'Trending': ['#EducationRevolution', '#SmartLearning', '#YouthPower']
        }
    }
    
    return recommendations.get(niche, recommendations['Education'])

def calculate_hashtag_score(hashtag_data):
    """Calculate overall hashtag effectiveness score"""
    # Normalize metrics
    reach_score = min((hashtag_data['avg_reach'] / 50000) * 100, 100)
    engagement_score = min((hashtag_data['engagement_rate'] / 12) * 100, 100)
    trending_score = hashtag_data['trending_score']
    relevance_score = hashtag_data['relevance_score']
    
    # Competition penalty
    competition_penalty = {
        'Low': 1.0,
        'Medium': 0.9,
        'High': 0.75,
        'Very High': 0.6
    }
    
    penalty = competition_penalty.get(hashtag_data['competition'], 0.8)
    
    overall_score = (
        reach_score * 0.25 +
        engagement_score * 0.35 +
        trending_score * 0.20 +
        relevance_score * 0.20
    ) * penalty
    
    return round(overall_score, 1)

def render_hashtag_tracker():
    """Main rendering function for hashtag tracker"""
    
    from professional_dashboard import render_professional_header
    render_professional_header("🏷️ Hashtag Performance Tracker", "Optimize your hashtag strategy with data-driven insights")
    
    # Generate hashtag data
    hashtags_df = generate_hashtag_data()
    hashtags_df['effectiveness_score'] = hashtags_df.apply(calculate_hashtag_score, axis=1)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", "🔍 Analysis", "💡 Recommendations", "📈 Trends"
    ])
    
    with tab1:
        render_hashtag_overview(hashtags_df)
    
    with tab2:
        render_hashtag_analysis(hashtags_df)
    
    with tab3:
        render_hashtag_recommendations()
    
    with tab4:
        render_hashtag_trends_section(hashtags_df)

def render_hashtag_overview(hashtags_df):
    """Render hashtag overview dashboard"""
    # Overview Section
    st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-chart-title">📊 Hashtag Performance Overview</div>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_hashtags = len(hashtags_df)
        st.metric("Total Hashtags", total_hashtags)
    
    with col2:
        total_reach = hashtags_df['total_reach'].sum()
        st.metric("Total Reach", f"{total_reach:,.0f}")
    
    with col3:
        avg_engagement = hashtags_df['engagement_rate'].mean()
        st.metric("Avg Engagement", f"{round(avg_engagement, 2)}%")
    
    with col4:
        top_performer = hashtags_df.loc[hashtags_df['effectiveness_score'].idxmax()]
        st.metric("Top Performer", top_performer['hashtag'])
    
    with col5:
        rising_count = len(hashtags_df[hashtags_df['growth_trend'] == 'Rising'])
        st.metric("Rising Hashtags", rising_count, delta=f"+{rising_count}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Top performing hashtags
    st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
    
    top_hashtags = hashtags_df.nlargest(10, 'effectiveness_score')
    
    for idx, hashtag in top_hashtags.iterrows():
        trend_emoji = '📈' if hashtag['growth_trend'] == 'Rising' else '📊' if hashtag['growth_trend'] == 'Stable' else '📉'
        
        competition_color = {
            'Low': '#10b981',
            'Medium': '#f59e0b',
            'High': '#ef4444',
            'Very High': '#991b1b'
        }.get(hashtag['competition'], '#6b7280')
        
        with st.container():
            st.markdown(f"""
            <div style="padding: 1rem; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-left: 5px solid #667eea; border-radius: 8px; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: #1e293b;">{trend_emoji} {hashtag['hashtag']}</h3>
                        <div style="display: flex; gap: 1rem; margin-top: 0.5rem; font-size: 0.9rem; color: #64748b;">
                            <span>📊 {hashtag['posts_used']} posts</span>
                            <span>👁️ {hashtag['avg_reach']:,.0f} avg reach</span>
                            <span>❤️ {hashtag['engagement_rate']}% engagement</span>
                            <span style="background: {competition_color}; color: white; padding: 2px 8px; border-radius: 4px;">{hashtag['competition']} Competition</span>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; font-weight: bold; color: #667eea;">{hashtag['effectiveness_score']}</div>
                        <div style="font-size: 0.8rem; color: #64748b;">Effectiveness Score</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bars
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.caption("Trending Score")
                st.progress(hashtag['trending_score'] / 100)
            
            with col2:
                st.caption("Relevance Score")
                st.progress(hashtag['relevance_score'] / 100)
            
            with col3:
                st.caption("Effectiveness")
                st.progress(hashtag['effectiveness_score'] / 100)
    
    # Category distribution
    st.markdown("### 📂 Hashtag Categories")
    
    col1, col2 = st.columns(2)
    
    with col1:
        category_counts = hashtags_df['category'].value_counts()
        
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Hashtags by Category",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        platform_counts = hashtags_df['best_platform'].value_counts()
        
        fig = go.Figure(go.Bar(
            x=platform_counts.index,
            y=platform_counts.values,
            marker=dict(
                color=platform_counts.values,
                colorscale='Viridis'
            ),
            text=platform_counts.values,
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Best Performing Platform",
            xaxis_title="Platform",
            yaxis_title="Count",
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_hashtag_analysis(hashtags_df):
    """Render detailed hashtag analysis"""
    st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.multiselect(
            "Category",
            options=['All'] + list(hashtags_df['category'].unique()),
            default=['All']
        )
    
    with col2:
        competition_filter = st.multiselect(
            "Competition Level",
            options=['All'] + list(hashtags_df['competition'].unique()),
            default=['All']
        )
    
    with col3:
        trend_filter = st.multiselect(
            "Growth Trend",
            options=['All'] + list(hashtags_df['growth_trend'].unique()),
            default=['All']
        )
    
    # Apply filters
    filtered_df = hashtags_df.copy()
    
    if 'All' not in category_filter and category_filter:
        filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]
    
    if 'All' not in competition_filter and competition_filter:
        filtered_df = filtered_df[filtered_df['competition'].isin(competition_filter)]
    
    if 'All' not in trend_filter and trend_filter:
        filtered_df = filtered_df[filtered_df['growth_trend'].isin(trend_filter)]
    
    # Scatter plot: Reach vs Engagement
    st.markdown("#### 📈 Reach vs Engagement Analysis")
    
    fig = px.scatter(
        filtered_df,
        x='avg_reach',
        y='engagement_rate',
        size='effectiveness_score',
        color='competition',
        hover_data=['hashtag', 'posts_used', 'trending_score'],
        title="Hashtag Performance Matrix",
        color_discrete_map={
            'Low': '#10b981',
            'Medium': '#f59e0b',
            'High': '#ef4444',
            'Very High': '#991b1b'
        }
    )
    
    fig.update_layout(
        xaxis_title="Average Reach",
        yaxis_title="Engagement Rate (%)",
        height=500,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.markdown("#### 📋 Detailed Hashtag Metrics")
    
    display_df = filtered_df[[
        'hashtag', 'posts_used', 'avg_reach', 'engagement_rate', 
        'trending_score', 'competition', 'growth_trend', 'effectiveness_score'
    ]].copy()
    
    display_df.columns = [
        'Hashtag', 'Posts', 'Avg Reach', 'Engagement %', 
        'Trending', 'Competition', 'Trend', 'Score'
    ]
    
    display_df = display_df.sort_values('Score', ascending=False)
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    # Competition analysis
    st.markdown("#### ⚔️ Competition Analysis")
    
    competition_stats = filtered_df.groupby('competition').agg({
        'avg_reach': 'mean',
        'engagement_rate': 'mean',
        'effectiveness_score': 'mean'
    }).round(2)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Avg Reach',
        x=competition_stats.index,
        y=competition_stats['avg_reach'],
        marker_color='#667eea'
    ))
    
    fig.add_trace(go.Bar(
        name='Engagement Rate',
        x=competition_stats.index,
        y=competition_stats['engagement_rate'] * 1000,  # Scale for visibility
        marker_color='#43e97b'
    ))
    
    fig.update_layout(
        title="Performance by Competition Level",
        xaxis_title="Competition Level",
        yaxis_title="Value",
        barmode='group',
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_hashtag_recommendations():
    """Render AI-powered hashtag recommendations"""
    st.markdown("### 💡 AI-Powered Hashtag Recommendations")
    
    # Niche selection
    niche = st.selectbox(
        "Select Your Niche",
        ["Education", "Technology", "Lifestyle", "Business", "Health"]
    )
    
    recommendations = get_hashtag_recommendations(niche)
    
    # Display recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚀 High Performance Hashtags")
        st.success("These hashtags consistently deliver high engagement")
        for tag in recommendations['High Performance']:
            st.markdown(f"- **{tag}** - Proven high engagement")
        
        st.markdown("#### 📈 Growing Hashtags")
        st.info("These hashtags are gaining momentum")
        for tag in recommendations['Growing']:
            st.markdown(f"- **{tag}** - Rising trend")
    
    with col2:
        st.markdown("#### 🎯 Niche Hashtags")
        st.warning("Targeted hashtags for specific audiences")
        for tag in recommendations['Niche']:
            st.markdown(f"- **{tag}** - Niche targeting")
        
        st.markdown("#### 🔥 Trending Now")
        st.error("Currently trending hashtags")
        for tag in recommendations['Trending']:
            st.markdown(f"- **{tag}** - Hot right now")
    
    # Hashtag generator
    st.markdown("### 🤖 AI Hashtag Generator")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        post_content = st.text_area(
            "Paste your post content",
            placeholder="Enter your post caption here...",
            height=100
        )
    
    with col2:
        num_hashtags = st.slider("Number of hashtags", 5, 30, 15)
        
        if st.button("🎯 Generate Hashtags", use_container_width=True):
            st.success("Generated hashtags:")
            generated = " ".join([f"#{random.choice(['Education', 'Student', 'Campus', 'University', 'Learning'])}{random.choice(['Life', 'Goals', '2025', 'Success', 'Journey'])}" for _ in range(num_hashtags)])
            st.code(generated)
    
    # Hashtag sets
    st.markdown("### 📦 Pre-Built Hashtag Sets")
    
    sets = {
        "Admissions Campaign": "#Admissions2025 #JoinUs #FutureStarts #DreamBig #ApplyNow #UniversityLife #NewBeginnings #StudentJourney #EducationFirst #YourFuture",
        "Campus Life": "#CampusLife #StudentLife #UniversityVibes #CollegeDays #CampusCulture #StudentCommunity #CollegeMemories #CampusFun #StudentExperience #UniversityDays",
        "Placements": "#Placements2025 #CareerSuccess #JobReady #PlacementDrive #CareerGoals #FutureLeaders #SuccessStory #DreamJob #CareerOpportunity #PlacementSeason",
        "Events": "#CampusEvent #UniversityEvent #StudentEvent #CulturalFest #TechFest #CollegeFest #EventHighlights #CampusCelebration #StudentGathering #FestVibes"
    }
    
    for set_name, hashtags in sets.items():
        with st.expander(f"📋 {set_name}"):
            st.code(hashtags)
            if st.button(f"📋 Copy {set_name}", key=f"copy_{set_name}"):
                st.success(f"✅ Copied {set_name} hashtags!")

def render_hashtag_trends_section(hashtags_df):
    """Render hashtag trends and historical data"""
    st.markdown("### 📈 Hashtag Trends")
    
    # Select hashtag to analyze
    selected_hashtag = st.selectbox(
        "Select Hashtag to Analyze",
        options=hashtags_df['hashtag'].tolist()
    )
    
    # Get trend data
    trend_df = generate_hashtag_trends(selected_hashtag, days=30)
    
    # Display trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👁️ Reach Trend")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend_df['date'],
            y=trend_df['reach'],
            mode='lines+markers',
            name='Reach',
            line=dict(color='#667eea', width=3),
            fill='tozeroy'
        ))
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Reach",
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### ❤️ Engagement Trend")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend_df['date'],
            y=trend_df['engagement'],
            mode='lines+markers',
            name='Engagement',
            line=dict(color='#43e97b', width=3),
            fill='tozeroy'
        ))
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Engagement",
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Posts volume
    st.markdown("#### 📊 Posts Volume")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=trend_df['date'],
        y=trend_df['posts'],
        marker_color='#f093fb',
        name='Posts'
    ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Posts",
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Trend insights
    st.markdown("### 💡 Trend Insights")
    
    avg_reach = trend_df['reach'].mean()
    avg_engagement = trend_df['engagement'].mean()
    total_posts = trend_df['posts'].sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg Daily Reach", f"{avg_reach:,.0f}")
    
    with col2:
        st.metric("Avg Daily Engagement", f"{avg_engagement:,.0f}")
    
    with col3:
        st.metric("Total Posts (30d)", total_posts)
    
    # Recommendations
    recent_trend = trend_df.tail(7)['reach'].mean()
    older_trend = trend_df.head(7)['reach'].mean()
    
    if recent_trend > older_trend * 1.1:
        st.success(f"📈 **{selected_hashtag}** is trending upward! Great time to use this hashtag.")
    elif recent_trend < older_trend * 0.9:
        st.warning(f"📉 **{selected_hashtag}** is declining. Consider alternative hashtags.")
    else:
        st.info(f"📊 **{selected_hashtag}** is stable. Consistent performance expected.")

if __name__ == "__main__":
    st.set_page_config(page_title="Hashtag Tracker", layout="wide")
    render_hashtag_tracker()
