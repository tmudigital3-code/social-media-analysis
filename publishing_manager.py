"""
Multi-Account Publishing & Scheduling Module
Inspired by Hootsuite - Manage multiple social accounts and schedule posts
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import random

def get_connected_accounts():
    """Get list of connected social media accounts"""
    return [
        {'id': 1, 'platform': 'Instagram', 'handle': '@tmu_official', 'followers': 45000, 'status': 'Active'},
        {'id': 2, 'platform': 'Facebook', 'handle': 'TMU Official', 'followers': 78000, 'status': 'Active'},
        {'id': 3, 'platform': 'Twitter', 'handle': '@TMU_Edu', 'followers': 23000, 'status': 'Active'},
        {'id': 4, 'platform': 'LinkedIn', 'handle': 'TMU University', 'followers': 34000, 'status': 'Active'},
        {'id': 5, 'platform': 'YouTube', 'handle': 'TMU Official', 'followers': 12000, 'status': 'Active'},
        {'id': 6, 'platform': 'TikTok', 'handle': '@tmu_campus', 'followers': 56000, 'status': 'Limited'},
    ]

def get_scheduled_posts():
    """Get scheduled posts"""
    posts = []
    platforms = ['Instagram', 'Facebook', 'Twitter', 'LinkedIn', 'YouTube', 'TikTok']
    statuses = ['Scheduled', 'Draft', 'Published', 'Failed']
    content_types = ['Image', 'Video', 'Carousel', 'Story', 'Reel', 'Text']
    
    for i in range(30):
        scheduled_time = datetime.now() + timedelta(hours=random.randint(-48, 168))
        
        posts.append({
            'id': i + 1,
            'platform': random.choice(platforms),
            'content_type': random.choice(content_types),
            'caption': f"Sample post content {i+1}...",
            'scheduled_time': scheduled_time,
            'status': random.choice(statuses) if scheduled_time > datetime.now() else 'Published',
            'engagement_predicted': random.randint(500, 5000),
            'best_time_match': random.choice([True, False]),
            'hashtags': random.randint(5, 20),
            'media_count': random.randint(1, 10),
            'target_audience': random.choice(['Students', 'Parents', 'Alumni', 'General'])
        })
    
    return pd.DataFrame(posts)

def get_content_calendar(days=30):
    """Generate content calendar data"""
    calendar_data = []
    
    for day in range(days):
        date = datetime.now() + timedelta(days=day)
        num_posts = random.randint(1, 5)
        
        for _ in range(num_posts):
            calendar_data.append({
                'date': date.date(),
                'time': f"{random.randint(6, 22)}:00",
                'platform': random.choice(['Instagram', 'Facebook', 'Twitter', 'LinkedIn']),
                'content_type': random.choice(['Image', 'Video', 'Carousel', 'Story']),
                'campaign': random.choice(['Admissions 2025', 'Campus Life', 'Placements', 'Events', 'General']),
                'status': random.choice(['Scheduled', 'Draft', 'Needs Approval'])
            })
    
    return pd.DataFrame(calendar_data)

def get_best_posting_times():
    """Get optimal posting times for each platform"""
    return {
        'Instagram': [
            {'day': 'Monday', 'time': '18:00', 'engagement_score': 92},
            {'day': 'Wednesday', 'time': '19:00', 'engagement_score': 95},
            {'day': 'Friday', 'time': '17:00', 'engagement_score': 88},
        ],
        'Facebook': [
            {'day': 'Tuesday', 'time': '13:00', 'engagement_score': 85},
            {'day': 'Thursday', 'time': '15:00', 'engagement_score': 90},
            {'day': 'Saturday', 'time': '11:00', 'engagement_score': 82},
        ],
        'Twitter': [
            {'day': 'Monday', 'time': '09:00', 'engagement_score': 78},
            {'day': 'Wednesday', 'time': '12:00', 'engagement_score': 83},
            {'day': 'Friday', 'time': '16:00', 'engagement_score': 80},
        ],
        'LinkedIn': [
            {'day': 'Tuesday', 'time': '10:00', 'engagement_score': 88},
            {'day': 'Wednesday', 'time': '11:00', 'engagement_score': 92},
            {'day': 'Thursday', 'time': '14:00', 'engagement_score': 86},
        ]
    }

def render_publishing_dashboard():
    """Main rendering function for publishing dashboard"""
    
    st.markdown("## 📅 Multi-Account Publishing & Scheduling")
    st.markdown("Manage, schedule, and publish content across all your social media accounts")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Compose", "📅 Calendar", "⏰ Scheduled", "📊 Analytics", "⚙️ Accounts"
    ])
    
    with tab1:
        render_compose_section()
    
    with tab2:
        render_calendar_section()
    
    with tab3:
        render_scheduled_section()
    
    with tab4:
        render_publishing_analytics()
    
    with tab5:
        render_accounts_section()

def render_compose_section():
    """Render the compose post section"""
    st.markdown("### ✍️ Compose New Post")
    
    # Platform selection
    st.markdown("#### Select Platforms")
    
    accounts = get_connected_accounts()
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    selected_platforms = []
    
    with col1:
        if st.checkbox("📷 Instagram", value=True):
            selected_platforms.append('Instagram')
    
    with col2:
        if st.checkbox("📘 Facebook"):
            selected_platforms.append('Facebook')
    
    with col3:
        if st.checkbox("🐦 Twitter"):
            selected_platforms.append('Twitter')
    
    with col4:
        if st.checkbox("💼 LinkedIn"):
            selected_platforms.append('LinkedIn')
    
    with col5:
        if st.checkbox("📹 YouTube"):
            selected_platforms.append('YouTube')
    
    with col6:
        if st.checkbox("🎵 TikTok"):
            selected_platforms.append('TikTok')
    
    if not selected_platforms:
        st.warning("⚠️ Please select at least one platform")
        return
    
    st.success(f"✅ Posting to: {', '.join(selected_platforms)}")
    
    # Content input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Content")
        
        caption = st.text_area(
            "Caption",
            placeholder="Write your caption here...",
            height=150,
            help="Tip: Use emojis and hashtags to increase engagement"
        )
        
        # Character count
        char_count = len(caption)
        max_chars = {
            'Instagram': 2200,
            'Twitter': 280,
            'Facebook': 63206,
            'LinkedIn': 3000,
            'TikTok': 2200
        }
        
        # Show character limits for selected platforms
        for platform in selected_platforms:
            if platform in max_chars:
                limit = max_chars[platform]
                percentage = (char_count / limit) * 100
                color = 'green' if percentage < 80 else 'orange' if percentage < 100 else 'red'
                st.markdown(f"**{platform}**: {char_count}/{limit} characters ({round(percentage, 1)}%) <span style='color: {color}'>{'✓' if char_count <= limit else '⚠️'}</span>", unsafe_allow_html=True)
        
        # Hashtags
        hashtags = st.text_input(
            "Hashtags",
            placeholder="#university #education #TMU",
            help="Separate hashtags with spaces"
        )
        
        # Media upload
        st.markdown("#### Media")
        uploaded_files = st.file_uploader(
            "Upload Images/Videos",
            accept_multiple_files=True,
            type=['jpg', 'jpeg', 'png', 'mp4', 'mov']
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
    
    with col2:
        st.markdown("#### Scheduling")
        
        schedule_option = st.radio(
            "When to post?",
            ["Post Now", "Schedule for Later", "Add to Queue"]
        )
        
        if schedule_option == "Schedule for Later":
            schedule_date = st.date_input("Date", value=datetime.now())
            schedule_time = st.time_input("Time", value=datetime.now().time())
            
            scheduled_datetime = datetime.combine(schedule_date, schedule_time)
            st.info(f"📅 Scheduled for: {scheduled_datetime.strftime('%Y-%m-%d %H:%M')}")
        
        elif schedule_option == "Add to Queue":
            st.info("📋 Will be posted at the next optimal time")
        
        st.markdown("#### AI Optimization")
        
        if st.button("🤖 AI Caption Suggestions", use_container_width=True):
            st.success("✨ AI-generated caption suggestions:")
            st.code("🎓 Discover your future at TMU! Join thousands of students achieving their dreams. #TMU2025 #HigherEducation")
            st.code("📚 Excellence in education starts here. Explore our world-class programs and facilities. Apply now!")
        
        if st.button("🎯 Optimize Hashtags", use_container_width=True):
            st.success("📈 Recommended hashtags:")
            st.code("#TMU #University #HigherEd #StudentLife #Education2025 #CampusLife #IndiaEducation")
        
        if st.button("⏰ Best Time to Post", use_container_width=True):
            st.success("🕐 Optimal posting times:")
            st.info("Instagram: Today at 18:00 (92% engagement score)\nFacebook: Tomorrow at 13:00 (85% engagement score)")
        
        st.markdown("#### Target Audience")
        
        audience = st.multiselect(
            "Select audience",
            ["Students (17-21)", "Parents (40-55)", "Alumni", "Faculty", "General Public"],
            default=["Students (17-21)"]
        )
        
        st.markdown("#### Campaign")
        
        campaign = st.selectbox(
            "Add to campaign",
            ["None", "Admissions 2025", "Campus Life", "Placements", "Events", "Research"]
        )
    
    # Action buttons
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📤 Publish Now", use_container_width=True, type="primary"):
            st.success("✅ Post published successfully to " + ", ".join(selected_platforms))
    
    with col2:
        if st.button("⏰ Schedule Post", use_container_width=True):
            st.success("✅ Post scheduled successfully!")
    
    with col3:
        if st.button("💾 Save as Draft", use_container_width=True):
            st.info("📝 Draft saved")
    
    with col4:
        if st.button("👁️ Preview", use_container_width=True):
            st.info("👀 Opening preview...")

def render_calendar_section():
    """Render the content calendar"""
    st.markdown("### 📅 Content Calendar")
    
    # Calendar view options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        view_type = st.selectbox("View", ["Month", "Week", "Day"])
    
    with col2:
        filter_platform = st.multiselect("Filter Platform", ["All", "Instagram", "Facebook", "Twitter", "LinkedIn"])
    
    with col3:
        filter_campaign = st.multiselect("Filter Campaign", ["All", "Admissions 2025", "Campus Life", "Placements"])
    
    # Get calendar data
    calendar_df = get_content_calendar(days=30)
    
    # Apply filters
    if filter_platform and "All" not in filter_platform:
        calendar_df = calendar_df[calendar_df['platform'].isin(filter_platform)]
    
    if filter_campaign and "All" not in filter_campaign:
        calendar_df = calendar_df[calendar_df['campaign'].isin(filter_campaign)]
    
    # Calendar visualization
    st.markdown("#### Monthly Overview")
    
    # Group by date
    daily_posts = calendar_df.groupby('date').size().reset_index(name='count')
    
    # Create calendar heatmap
    fig = go.Figure(data=go.Scatter(
        x=daily_posts['date'],
        y=daily_posts['count'],
        mode='markers+lines',
        marker=dict(
            size=daily_posts['count'] * 5,
            color=daily_posts['count'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Posts")
        ),
        line=dict(color='#667eea', width=2)
    ))
    
    fig.update_layout(
        title="Posts Scheduled Per Day",
        xaxis_title="Date",
        yaxis_title="Number of Posts",
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed calendar table
    st.markdown("#### Scheduled Posts")
    
    # Format for display
    display_calendar = calendar_df.copy()
    display_calendar['date'] = pd.to_datetime(display_calendar['date']).dt.strftime('%Y-%m-%d')
    display_calendar = display_calendar.sort_values('date')
    
    # Color code by status
    def color_status(val):
        if val == 'Scheduled':
            return 'background-color: #d1fae5'
        elif val == 'Draft':
            return 'background-color: #fef3c7'
        elif val == 'Needs Approval':
            return 'background-color: #fee2e2'
        return ''
    
    styled_calendar = display_calendar.style.applymap(color_status, subset=['status'])
    st.dataframe(styled_calendar, use_container_width=True, height=400)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Scheduled", len(calendar_df[calendar_df['status'] == 'Scheduled']))
    
    with col2:
        st.metric("Drafts", len(calendar_df[calendar_df['status'] == 'Draft']))
    
    with col3:
        st.metric("Needs Approval", len(calendar_df[calendar_df['status'] == 'Needs Approval']))
    
    with col4:
        avg_per_day = len(calendar_df) / 30
        st.metric("Avg Posts/Day", round(avg_per_day, 1))

def render_scheduled_section():
    """Render scheduled posts section"""
    st.markdown("### ⏰ Scheduled Posts")
    
    scheduled_df = get_scheduled_posts()
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect("Status", ["All"] + list(scheduled_df['status'].unique()), default=["All"])
    
    with col2:
        platform_filter = st.multiselect("Platform", ["All"] + list(scheduled_df['platform'].unique()), default=["All"])
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Scheduled Time", "Platform", "Engagement Predicted"])
    
    # Apply filters
    filtered_df = scheduled_df.copy()
    
    if "All" not in status_filter and status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    
    if "All" not in platform_filter and platform_filter:
        filtered_df = filtered_df[filtered_df['platform'].isin(platform_filter)]
    
    # Sort
    if sort_by == "Scheduled Time":
        filtered_df = filtered_df.sort_values('scheduled_time')
    elif sort_by == "Engagement Predicted":
        filtered_df = filtered_df.sort_values('engagement_predicted', ascending=False)
    
    # Display posts
    for idx, post in filtered_df.head(20).iterrows():
        status_color = {
            'Scheduled': '#10b981',
            'Draft': '#f59e0b',
            'Published': '#3b82f6',
            'Failed': '#ef4444'
        }.get(post['status'], '#6b7280')
        
        time_diff = post['scheduled_time'] - datetime.now()
        time_str = f"in {time_diff.days} days" if time_diff.days > 0 else f"in {time_diff.seconds // 3600} hours"
        
        best_time_badge = "🎯 OPTIMAL TIME" if post['best_time_match'] else ""
        
        with st.container():
            st.markdown(f"""
            <div style="padding: 1rem; background-color: #f8fafc; border-left: 4px solid {status_color}; border-radius: 8px; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div>
                        <span style="font-weight: bold; color: #1e293b;">{post['platform']}</span>
                        <span style="background: {status_color}; color: white; padding: 2px 8px; border-radius: 4px; margin-left: 1rem; font-size: 0.8rem;">{post['status']}</span>
                        <span style="background: #fef3c7; padding: 2px 8px; border-radius: 4px; margin-left: 0.5rem; font-size: 0.8rem;">{best_time_badge}</span>
                    </div>
                    <div style="color: #64748b;">
                        {post['scheduled_time'].strftime('%Y-%m-%d %H:%M')} ({time_str})
                    </div>
                </div>
                <div style="color: #334155; margin-bottom: 0.5rem;">
                    {post['caption'][:100]}...
                </div>
                <div style="display: flex; gap: 1.5rem; font-size: 0.9rem; color: #64748b;">
                    <span>📊 {post['content_type']}</span>
                    <span>🏷️ {post['hashtags']} hashtags</span>
                    <span>📸 {post['media_count']} media</span>
                    <span>🎯 {post['target_audience']}</span>
                    <span>📈 ~{post['engagement_predicted']} predicted engagement</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.button("✏️ Edit", key=f"edit_{post['id']}")
            with col2:
                st.button("📋 Duplicate", key=f"dup_{post['id']}")
            with col3:
                st.button("🗑️ Delete", key=f"del_{post['id']}")
            with col4:
                st.button("📤 Post Now", key=f"post_{post['id']}")

def render_publishing_analytics():
    """Render publishing analytics"""
    st.markdown("### 📊 Publishing Analytics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Posts This Month", "127", delta="+23")
    
    with col2:
        st.metric("Avg Engagement", "3,456", delta="+12.5%")
    
    with col3:
        st.metric("Best Performing", "Instagram", delta="45% engagement")
    
    with col4:
        st.metric("Success Rate", "94.2%", delta="+2.1%")
    
    # Publishing frequency
    st.markdown("#### 📈 Publishing Frequency")
    
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    platforms = ['Instagram', 'Facebook', 'Twitter', 'LinkedIn']
    
    data = []
    for date in dates:
        for platform in platforms:
            data.append({
                'date': date,
                'platform': platform,
                'posts': random.randint(1, 8)
            })
    
    freq_df = pd.DataFrame(data)
    
    fig = px.line(
        freq_df,
        x='date',
        y='posts',
        color='platform',
        title="Daily Posts by Platform",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    # Best posting times heatmap
    st.markdown("#### ⏰ Optimal Posting Times")
    
    best_times = get_best_posting_times()
    
    col1, col2 = st.columns(2)
    
    with col1:
        platform_select = st.selectbox("Select Platform", list(best_times.keys()))
        
        times_df = pd.DataFrame(best_times[platform_select])
        
        fig = go.Figure(data=go.Bar(
            x=times_df['day'],
            y=times_df['engagement_score'],
            text=times_df['time'],
            textposition='auto',
            marker=dict(
                color=times_df['engagement_score'],
                colorscale='Viridis',
                showscale=True
            )
        ))
        
        fig.update_layout(
            title=f"Best Times for {platform_select}",
            xaxis_title="Day",
            yaxis_title="Engagement Score",
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Recommendations:**")
        for time_slot in best_times[platform_select]:
            st.info(f"📅 **{time_slot['day']}** at **{time_slot['time']}** - Engagement Score: {time_slot['engagement_score']}/100")

def render_accounts_section():
    """Render connected accounts section"""
    st.markdown("### ⚙️ Connected Accounts")
    
    accounts = get_connected_accounts()
    accounts_df = pd.DataFrame(accounts)
    
    # Display accounts
    for idx, account in accounts_df.iterrows():
        status_color = '#10b981' if account['status'] == 'Active' else '#f59e0b'
        
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            with col1:
                st.markdown(f"### {account['platform']}")
                st.markdown(f"**{account['handle']}**")
            
            with col2:
                st.metric("Followers", f"{account['followers']:,}")
            
            with col3:
                st.markdown(f"<span style='background: {status_color}; color: white; padding: 4px 12px; border-radius: 4px;'>{account['status']}</span>", unsafe_allow_html=True)
            
            with col4:
                if st.button("⚙️", key=f"settings_{account['id']}"):
                    st.info("Opening settings...")
        
        st.markdown("---")
    
    # Add new account
    if st.button("➕ Connect New Account", use_container_width=True):
        st.success("Opening account connection wizard...")

if __name__ == "__main__":
    st.set_page_config(page_title="Publishing Dashboard", layout="wide")
    render_publishing_dashboard()
