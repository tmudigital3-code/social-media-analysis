"""
Influencer Discovery & Analysis Module
Find, analyze, and track influencers for collaboration opportunities
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

def generate_influencer_database(num_influencers=50):
    """Generate simulated influencer database"""
    influencers = []
    
    niches = ['Study Tips', 'Campus Life', 'Exam Prep', 'Career Counseling', 'Admission Consulting', 'Higher Education', 'Scholarships', 'Student Vlogs']
    platforms = ['Instagram', 'YouTube', 'LinkedIn', 'Twitter', 'TikTok']
    locations = ['Delhi', 'Mumbai', 'Bangalore', 'Pune', 'Hyderabad', 'Chennai', 'Ahmedabad', 'Kolkata']
    
    # Specific top private universities for recruitment focus
    target_universities = [
        'Parul University', 'Chandigarh University', 'LPU (Lovely Professional University)', 
        'Amity University', 'SRM Institute', 'VIT (Vellore Institute of Technology)', 
        'Manipal Academy', 'Shiv Nadar University', 'OP Jindal Global', 'Bennett University'
    ]
    
    # Names more likely to be associated with education/expert accounts
    first_names = ['Dr. Aarti', 'Prof. Raj', 'Student', 'Edu', 'Expert', 'Counselor', 'Aman', 'Priya', 'Rohan', 'Sneha', 'Official']
    last_names = ['Sharma', 'Verma', 'Kumar', 'Patel', 'Guides', 'Consultancy', 'Akademy', 'Hub', 'Joshi', 'Ambassador']
    
    for i in range(num_influencers):
        followers = random.randint(5000, 500000)
        engagement_rate = round(random.uniform(2.0, 15.0), 2)
        avg_views = followers * random.uniform(0.3, 0.8)
        university = random.choice(target_universities) if random.random() > 0.3 else "General Education"
        
        influencers.append({
            'id': i + 1,
            'name': f"{random.choice(first_names)} {random.choice(last_names)}",
            'handle': f"@{random.choice(first_names).lower()}{random.choice(last_names).lower()}{random.randint(10, 99)}",
            'platform': random.choice(platforms),
            'niche': random.choice(niches),
            'university_affinity': university,
            'followers': followers,
            'engagement_rate': engagement_rate,
            'avg_likes': int(followers * engagement_rate / 100 * 0.8),
            'avg_comments': int(followers * engagement_rate / 100 * 0.2),
            'avg_views': int(avg_views),
            'posts_per_week': random.randint(3, 14),
            'location': random.choice(locations),
            'verified': random.random() > 0.7,
            'collab_rate': random.randint(5000, 100000),
            'response_rate': round(random.uniform(40, 95), 1),
            'audience_age': random.choice(['18-24', '25-34', '18-34']),
            'audience_gender': random.choice(['60% F / 40% M', '55% M / 45% F', '50% F / 50% M']),
            'growth_rate': round(random.uniform(-2, 25), 2),
            'authenticity_score': round(random.uniform(65, 98), 1),
            'brand_affinity': round(random.uniform(50, 95), 1),
            'previous_collabs': random.randint(0, 50),
            'avg_reach': int(followers * random.uniform(1.2, 3.5)),
            'story_views': int(followers * random.uniform(0.15, 0.4))
        })
    
    return pd.DataFrame(influencers)

def calculate_influencer_score(influencer):
    """Calculate overall influencer score (0-100)"""
    # Weighted scoring
    engagement_score = min(influencer['engagement_rate'] * 5, 100)
    authenticity_score = influencer['authenticity_score']
    growth_score = min(max(influencer['growth_rate'] * 3, 0), 100)
    response_score = influencer['response_rate']
    
    overall_score = (
        engagement_score * 0.35 +
        authenticity_score * 0.25 +
        growth_score * 0.20 +
        response_score * 0.20
    )
    
    return round(overall_score, 1)

def render_influencer_discovery():
    """Main rendering function for influencer discovery"""
    
    from professional_dashboard import render_professional_header
    render_professional_header("🎓 Academic & Campus Influencer Discovery", "Identify and collaborate with educational influencers to boost college admissions and brand reach")
    
    # Generate influencer database
    influencers_df = generate_influencer_database(num_influencers=100)
    
    # Calculate scores
    influencers_df['overall_score'] = influencers_df.apply(calculate_influencer_score, axis=1)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Discovery", "📊 Analytics", "🤝 Campaigns", "📈 Tracking"
    ])
    
    with tab1:
        render_discovery_section(influencers_df)
    
    with tab2:
        render_influencer_analytics(influencers_df)
    
    with tab3:
        render_campaign_management()
    
    with tab4:
        render_influencer_tracking(influencers_df)

def render_discovery_section(influencers_df):
    """Render influencer discovery and search"""
    st.markdown("### 🎓 Find Education Influencers")
    
    # Search filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        platform_filter = st.multiselect(
            "Platform",
            options=['All'] + list(influencers_df['platform'].unique()),
            default=['All']
        )
    
    with col2:
        niche_filter = st.multiselect(
            "Niche",
            options=['All'] + list(influencers_df['niche'].unique()),
            default=['All']
        )
    
    with col3:
        location_filter = st.multiselect(
            "Location",
            options=['All'] + list(influencers_df['location'].unique()),
            default=['All']
        )
    
    with col4:
        verified_only = st.checkbox("Verified Only", value=False)
    
    # Advanced filters
    with st.expander("🎯 Advanced Filters"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            followers_range = st.slider(
                "Followers Range",
                min_value=0,
                max_value=500000,
                value=(10000, 200000),
                step=10000
            )
        
        with col2:
            engagement_range = st.slider(
                "Engagement Rate (%)",
                min_value=0.0,
                max_value=20.0,
                value=(3.0, 15.0),
                step=0.5
            )
        
        with col3:
            budget_range = st.slider(
                "Campaign Budget (₹)",
                min_value=0,
                max_value=200000,
                value=(20000, 100000),
                step=5000
            )
    
    # Apply filters
    filtered_df = influencers_df.copy()
    
    if 'All' not in platform_filter and platform_filter:
        filtered_df = filtered_df[filtered_df['platform'].isin(platform_filter)]
    
    if 'All' not in niche_filter and niche_filter:
        filtered_df = filtered_df[filtered_df['niche'].isin(niche_filter)]
    
    if 'All' not in location_filter and location_filter:
        filtered_df = filtered_df[filtered_df['location'].isin(location_filter)]
    
    if verified_only:
        filtered_df = filtered_df[filtered_df['verified'] == True]
    
    filtered_df = filtered_df[
        (filtered_df['followers'] >= followers_range[0]) &
        (filtered_df['followers'] <= followers_range[1]) &
        (filtered_df['engagement_rate'] >= engagement_range[0]) &
        (filtered_df['engagement_rate'] <= engagement_range[1]) &
        (filtered_df['collab_rate'] >= budget_range[0]) &
        (filtered_df['collab_rate'] <= budget_range[1])
    ]
    
    # Sort options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### 📋 Found {len(filtered_df)} Influencers")
    
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            ["Overall Score", "Followers", "Engagement Rate", "Authenticity", "Budget"]
        )
    
    # Sort
    sort_mapping = {
        "Overall Score": "overall_score",
        "Followers": "followers",
        "Engagement Rate": "engagement_rate",
        "Authenticity": "authenticity_score",
        "Budget": "collab_rate"
    }
    
    filtered_df = filtered_df.sort_values(sort_mapping[sort_by], ascending=False)
    
    # Display influencers
    for idx, influencer in filtered_df.head(20).iterrows():
        with st.container():
            col1, col2, col3 = st.columns([2, 3, 2])
            
            with col1:
                st.markdown(f"""
                <div class="pro-glass-card" style="padding: 1.2rem; background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); color: white;">
                    <h3 style="margin: 0; color: white; font-size: 1.2rem;">{influencer['name']}</h3>
                    <p style="margin: 0.3rem 0; opacity: 0.9; font-size: 0.85rem;">{influencer['handle']}</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.8rem;">
                        <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 6px; font-size: 0.7rem;">{influencer['platform']}</span>
                        <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 6px; font-size: 0.7rem;">{influencer['niche']}</span>
                        {f"<span style='background: rgba(255,255,255,0.3); padding: 2px 8px; border-radius: 6px; font-size: 0.7rem;'>✓ Verified</span>" if influencer['verified'] else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            
            with col2:
                st.markdown(f"""
                **📍 Location:** {influencer['location']}  
                **🏛️ University Affinity:** {influencer['university_affinity']}  
                **👥 Followers:** {influencer['followers']:,}  
                **📈 Engagement Rate:** {influencer['engagement_rate']}%  
                **🎯 Authenticity Score:** {influencer['authenticity_score']}/100  
                **💰 Collab Rate:** ₹{influencer['collab_rate']:,}  
                **📊 Overall Score:** {influencer['overall_score']}/100
                """)
                
                # Progress bar for overall score
                st.progress(influencer['overall_score'] / 100)
            
            with col3:
                st.markdown("**Audience Insights:**")
                st.markdown(f"Age: {influencer['audience_age']}")
                st.markdown(f"Gender: {influencer['audience_gender']}")
                st.markdown(f"Growth: {influencer['growth_rate']}%/month")
                st.markdown(f"Avg Reach: {influencer['avg_reach']:,}")
                
                if st.button("📧 Contact", key=f"contact_{influencer['id']}", use_container_width=True):
                    st.success(f"✅ Contact request sent to {influencer['name']}")
                
                if st.button("⭐ Add to List", key=f"add_{influencer['id']}", use_container_width=True):
                    st.success(f"✅ Added to campaign list")
        
        st.markdown("---")

def render_influencer_analytics(influencers_df):
    """Render influencer analytics and insights"""
    st.markdown("### 📊 Influencer Market Analytics")
    
    # Market overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Influencers", len(influencers_df))
    
    with col2:
        avg_engagement = influencers_df['engagement_rate'].mean()
        st.metric("Avg Engagement", f"{round(avg_engagement, 2)}%")
    
    with col3:
        avg_rate = influencers_df['collab_rate'].mean()
        st.metric("Avg Collab Rate", f"₹{round(avg_rate):,}")
    
    with col4:
        # Assuming 'your_data' and 'competitor_df' are defined elsewhere or are placeholders.
        # For syntactic correctness, these lines are commented out or replaced with dummy values if not defined.
        # If 'your_data' and 'competitor_df' are meant to be part of the change, they need to be defined.
        # As per instructions, I will only fix indentation and not introduce new undefined variables.
        # The user's provided snippet for col4 seems to be introducing new metrics.
        # I will keep the original content for col4 and ensure the indentation of the provided snippet's lines is correct if they were to be added.
        # Given the instruction "Fix indentation for st.markdown and st.metric inside with blocks",
        # and the provided snippet, it seems the user intended to replace the content of col4.
        # However, without 'your_data' and 'competitor_df', the code would be broken.
        # I will apply the indentation fix to the existing code and assume the new metrics were illustrative.
        # If the user intended to add these new metrics, they would need to provide definitions for 'your_data' and 'competitor_df'.
        # For now, I will only fix the indentation of the existing st.metric in col4.
        verified_pct = (len(influencers_df[influencers_df['verified'] == True]) / len(influencers_df)) * 100
        st.metric("Verified %", f"{round(verified_pct, 1)}%")
    
    # Platform distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🌐 Platform Distribution</div>', unsafe_allow_html=True)
        
        platform_counts = influencers_df['platform'].value_counts()
        
        fig = px.pie(
            values=platform_counts.values,
            names=platform_counts.index,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.6
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    
    with col2:
        st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🎯 Niche Distribution</div>', unsafe_allow_html=True)
        
        niche_counts = influencers_df['niche'].value_counts()
        
        fig = go.Figure(go.Bar(
            x=niche_counts.values,
            y=niche_counts.index,
            orientation='h',
            marker=dict(
                color=niche_counts.values,
                colorscale='GnBu'
            ),
            text=niche_counts.values,
            textposition='inside'
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    
    # Engagement vs Followers scatter
    st.markdown("#### 📈 Engagement Rate vs Followers")
    
    fig = px.scatter(
        influencers_df,
        x='followers',
        y='engagement_rate',
        size='overall_score',
        color='platform',
        hover_data=['name', 'niche', 'collab_rate'],
        title="Influencer Performance Matrix",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_layout(
        xaxis_title="Followers",
        yaxis_title="Engagement Rate (%)",
        height=500,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top performers
    st.markdown("#### 🏆 Top Performing Influencers")
    
    top_performers = influencers_df.nlargest(10, 'overall_score')
    
    display_df = top_performers[[
        'name', 'platform', 'niche', 'followers', 'engagement_rate', 
        'authenticity_score', 'overall_score', 'collab_rate'
    ]].copy()
    
    display_df.columns = ['Name', 'Platform', 'Niche', 'Followers', 'Engagement %', 
                          'Authenticity', 'Score', 'Rate (₹)']
    
    st.dataframe(display_df, use_container_width=True, height=400)

def render_campaign_management():
    """Render influencer campaign management"""
    st.markdown("### 🤝 Campaign Management")
    
    # Create new campaign
    with st.expander("➕ Create New Campaign", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            campaign_name = st.text_input("Campaign Name", placeholder="e.g., Undergraduate Admissions 2026")
            campaign_budget = st.number_input("Total Recruitment Budget (₹)", min_value=0, value=500000, step=50000)
            campaign_objective = st.selectbox(
                "Primary Objective",
                ["Admission Applications", "Campus Visit Requests", "Brand Awareness", "Direct Lead Generation", "Scholarship Awareness"]
            )
        
        with col2:
            start_date = st.date_input("Start Date", value=datetime.now())
            end_date = st.date_input("End Date", value=datetime.now() + timedelta(days=30))
            target_audience = st.multiselect(
                "Target Audience",
                ["Students (18-24)", "Parents (40-55)", "Young Professionals", "Educators"]
            )
        
        if st.button("🚀 Create Campaign", use_container_width=True):
            st.success(f"✅ Campaign '{campaign_name}' created successfully!")
    
    # Active campaigns
    st.markdown("#### 📋 Active Campaigns")
    
    campaigns = [
        {
            'name': 'Undergraduate Admissions 2026',
            'status': 'Active',
            'influencers': 12,
            'budget': 500000,
            'spent': 320000,
            'reach': 1250000,
            'engagement': 85000,
            'conversions': 4500 # Conversions here are Admission Leads
        },
        {
            'name': 'Campus Life & Infrastructure Showcase',
            'status': 'Active',
            'influencers': 7,
            'budget': 200000,
            'spent': 110000,
            'reach': 680000,
            'engagement': 42000,
            'conversions': 1200
        },
        {
            'name': 'Alumni Success & Placements',
            'status': 'Draft',
            'influencers': 5,
            'budget': 150000,
            'spent': 0,
            'reach': 0,
            'engagement': 0,
            'conversions': 0
        }
    ]
    
    for campaign in campaigns:
        status_color = '#10b981' if campaign['status'] == 'Active' else '#3b82f6'
        budget_pct = (campaign['spent'] / campaign['budget']) * 100
        
        with st.container():
            st.markdown(f"""
            <div style="padding: 1.5rem; background-color: #f8fafc; border-radius: 12px; margin-bottom: 1rem; border: 2px solid {status_color};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0; color: #1e293b;">{campaign['name']}</h3>
                    <span style="background: {status_color}; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold;">{campaign['status']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Influencers", campaign['influencers'])
            
            with col2:
                st.metric("Budget", f"₹{campaign['budget']:,}")
                st.progress(budget_pct / 100)
                st.caption(f"Spent: ₹{campaign['spent']:,} ({round(budget_pct, 1)}%)")
            
            with col3:
                st.metric("Reach", f"{campaign['reach']:,}")
            
            with col4:
                st.metric("Engagement", f"{campaign['engagement']:,}")
            
            with col5:
                st.metric("Conversions", f"{campaign['conversions']:,}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.button("📊 View Details", key=f"view_{campaign['name']}", use_container_width=True)
            
            with col2:
                st.button("✏️ Edit", key=f"edit_{campaign['name']}", use_container_width=True)
            
            with col3:
                st.button("📥 Export Report", key=f"export_{campaign['name']}", use_container_width=True)
        
        st.markdown("---")

def render_influencer_tracking(influencers_df):
    """Render influencer performance tracking"""
    st.markdown("### 📈 Influencer Performance Tracking")
    
    # Select influencers to track
    tracked_influencers = influencers_df.sample(5)
    st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
    st.markdown("#### 👥 Tracked Influencers")
    
    for idx, influencer in tracked_influencers.iterrows():
        with st.expander(f"⭐ {influencer['name']} ({influencer['platform']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Performance Metrics:**")
                
                # Generate trend data
                dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
                followers_trend = [influencer['followers'] + random.randint(-1000, 2000) for _ in range(30)]
                engagement_trend = [influencer['engagement_rate'] + random.uniform(-0.5, 0.5) for _ in range(30)]
                
                # Followers trend
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=followers_trend,
                    mode='lines+markers',
                    name='Followers',
                    line=dict(color='#667eea', width=2)
                ))
                
                fig.update_layout(
                    title="Follower Growth (30 Days)",
                    xaxis_title="Date",
                    yaxis_title="Followers",
                    height=300,
                    template='plotly_white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**Engagement Trend:**")
                
                # Engagement trend
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=engagement_trend,
                    mode='lines+markers',
                    name='Engagement Rate',
                    line=dict(color='#43e97b', width=2),
                    fill='tozeroy'
                ))
                
                fig.update_layout(
                    title="Engagement Rate (30 Days)",
                    xaxis_title="Date",
                    yaxis_title="Engagement %",
                    height=300,
                    template='plotly_white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent posts
            st.markdown("**Recent Posts Performance:**")
            
            recent_posts = []
            for i in range(5):
                recent_posts.append({
                    'Date': (datetime.now() - timedelta(days=i*2)).strftime('%Y-%m-%d'),
                    'Type': random.choice(['Reel', 'Post', 'Story', 'Video']),
                    'Likes': random.randint(1000, 20000),
                    'Comments': random.randint(50, 500),
                    'Shares': random.randint(20, 200),
                    'Engagement': round(random.uniform(3, 12), 2)
                })
            
            posts_df = pd.DataFrame(recent_posts)
            st.dataframe(posts_df, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Influencer Discovery", layout="wide")
    render_influencer_discovery()
