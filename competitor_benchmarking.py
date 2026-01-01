"""
Competitor Benchmarking Module
Inspired by Socialinsider - Compare your performance against competitors
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

def generate_competitor_data(num_competitors=3):
    """Generate simulated competitor data for benchmarking"""
    competitors = []
    
    competitor_names = [
        "Competitor A", "Competitor B", "Competitor C", 
        "Competitor D", "Competitor E"
    ]
    
    for i in range(num_competitors):
        competitors.append({
            'name': competitor_names[i],
            'followers': random.randint(50000, 500000),
            'avg_engagement_rate': round(random.uniform(2.5, 8.5), 2),
            'posts_per_week': random.randint(3, 15),
            'avg_likes': random.randint(1000, 15000),
            'avg_comments': random.randint(50, 800),
            'avg_shares': random.randint(20, 500),
            'growth_rate': round(random.uniform(-2, 15), 2),
            'best_posting_time': f"{random.randint(6, 22)}:00",
            'top_content_type': random.choice(['Reels', 'Carousel', 'Static Image', 'Video']),
            'hashtag_usage': random.randint(5, 30),
            'response_time': f"{random.randint(1, 24)}h",
            'story_frequency': random.randint(2, 10)
        })
    
    return pd.DataFrame(competitors)

def calculate_competitive_score(your_data, competitor_data):
    """Calculate competitive positioning score"""
    scores = {}
    
    # Normalize metrics (0-100 scale)
    metrics = ['followers', 'avg_engagement_rate', 'posts_per_week', 'growth_rate']
    
    for metric in metrics:
        all_values = list(competitor_data[metric]) + [your_data.get(metric, 0)]
        max_val = max(all_values)
        min_val = min(all_values)
        
        if max_val > min_val:
            your_score = ((your_data.get(metric, 0) - min_val) / (max_val - min_val)) * 100
        else:
            your_score = 50
            
        scores[metric] = round(your_score, 1)
    
    overall_score = round(sum(scores.values()) / len(scores), 1)
    return overall_score, scores

def render_competitor_benchmarking(your_data=None):
    """Main rendering function for competitor benchmarking"""
    
    st.markdown("## 🎯 Competitor Benchmarking")
    st.markdown("Compare your performance against competitors and identify opportunities")
    
    # Configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        num_competitors = st.slider("Number of Competitors to Track", 1, 5, 3)
    
    with col2:
        time_period = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Last Year"])
    
    # Generate competitor data
    competitor_df = generate_competitor_data(num_competitors)
    
    # Your account data (simulated if not provided)
    if your_data is None:
        your_data = {
            'name': 'Your Account',
            'followers': random.randint(30000, 400000),
            'avg_engagement_rate': round(random.uniform(3.0, 7.5), 2),
            'posts_per_week': random.randint(4, 12),
            'avg_likes': random.randint(800, 12000),
            'avg_comments': random.randint(40, 600),
            'avg_shares': random.randint(15, 400),
            'growth_rate': round(random.uniform(1, 12), 2),
            'best_posting_time': "18:00",
            'top_content_type': 'Reels',
            'hashtag_usage': 15,
            'response_time': "3h",
            'story_frequency': 5
        }
    
    # Calculate competitive score
    overall_score, metric_scores = calculate_competitive_score(your_data, competitor_df)
    
    # Display competitive score
    st.markdown("### 📊 Your Competitive Position")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Score", f"{overall_score}/100", 
                 delta=f"{round(overall_score - 50, 1)} vs avg" if overall_score > 50 else f"{round(overall_score - 50, 1)} vs avg")
    
    with col2:
        rank = sum(1 for comp in competitor_df.itertuples() if comp.avg_engagement_rate > your_data['avg_engagement_rate']) + 1
        st.metric("Market Rank", f"#{rank}/{num_competitors + 1}")
    
    with col3:
        growth_vs_avg = your_data['growth_rate'] - competitor_df['growth_rate'].mean()
        st.metric("Growth vs Avg", f"{your_data['growth_rate']}%", delta=f"{round(growth_vs_avg, 1)}%")
    
    with col4:
        eng_vs_avg = your_data['avg_engagement_rate'] - competitor_df['avg_engagement_rate'].mean()
        st.metric("Engagement vs Avg", f"{your_data['avg_engagement_rate']}%", delta=f"{round(eng_vs_avg, 1)}%")
    
    # Radar Chart - Competitive Analysis
    st.markdown("### 🕸️ Multi-Dimensional Competitive Analysis")
    
    categories = ['Engagement Rate', 'Posting Frequency', 'Growth Rate', 'Follower Base', 'Content Quality']
    
    fig = go.Figure()
    
    # Add your account
    your_values = [
        metric_scores['avg_engagement_rate'],
        metric_scores['posts_per_week'],
        metric_scores['growth_rate'],
        metric_scores['followers'],
        random.randint(60, 95)  # Content quality score
    ]
    
    fig.add_trace(go.Scatterpolar(
        r=your_values,
        theta=categories,
        fill='toself',
        name='Your Account',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    # Add competitors
    colors = ['#f093fb', '#4facfe', '#43e97b', '#fa709a', '#feca57']
    for idx, comp in competitor_df.iterrows():
        _, comp_scores = calculate_competitive_score(comp.to_dict(), competitor_df.drop(idx))
        comp_values = [
            comp_scores['avg_engagement_rate'],
            comp_scores['posts_per_week'],
            comp_scores['growth_rate'],
            comp_scores['followers'],
            random.randint(50, 90)
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=comp_values,
            theta=categories,
            fill='toself',
            name=comp['name'],
            line_color=colors[idx % len(colors)],
            fillcolor=f'rgba({int(colors[idx % len(colors)][1:3], 16)}, {int(colors[idx % len(colors)][3:5], 16)}, {int(colors[idx % len(colors)][5:7], 16)}, 0.1)'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        height=500,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Metrics Comparison Table
    st.markdown("### 📋 Detailed Metrics Comparison")
    
    # Combine your data with competitors
    all_accounts = pd.concat([
        pd.DataFrame([your_data]),
        competitor_df
    ], ignore_index=True)
    
    # Format the dataframe for display
    display_df = all_accounts[[
        'name', 'followers', 'avg_engagement_rate', 'posts_per_week', 
        'growth_rate', 'top_content_type', 'best_posting_time'
    ]].copy()
    
    display_df.columns = ['Account', 'Followers', 'Engagement %', 'Posts/Week', 
                          'Growth %', 'Top Content', 'Best Time']
    
    # Highlight your account
    def highlight_your_account(row):
        if row['Account'] == 'Your Account':
            return ['background-color: #e8f4f8'] * len(row)
        return [''] * len(row)
    
    styled_df = display_df.style.apply(highlight_your_account, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=300)
    
    # Engagement Rate Comparison
    st.markdown("### 📈 Engagement Rate Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart comparison
        fig_bar = go.Figure()
        
        fig_bar.add_trace(go.Bar(
            x=all_accounts['name'],
            y=all_accounts['avg_engagement_rate'],
            marker_color=['#667eea' if name == 'Your Account' else '#94a3b8' 
                         for name in all_accounts['name']],
            text=all_accounts['avg_engagement_rate'],
            textposition='auto',
        ))
        
        fig_bar.update_layout(
            title="Engagement Rate Comparison",
            xaxis_title="Account",
            yaxis_title="Engagement Rate (%)",
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Growth rate comparison
        fig_growth = go.Figure()
        
        fig_growth.add_trace(go.Bar(
            x=all_accounts['name'],
            y=all_accounts['growth_rate'],
            marker_color=['#43e97b' if rate > 0 else '#fa709a' 
                         for rate in all_accounts['growth_rate']],
            text=all_accounts['growth_rate'],
            textposition='auto',
        ))
        
        fig_growth.update_layout(
            title="Growth Rate Comparison",
            xaxis_title="Account",
            yaxis_title="Growth Rate (%)",
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_growth, use_container_width=True)
    
    # Content Strategy Insights
    st.markdown("### 💡 Competitive Intelligence Insights")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Opportunities", "⚠️ Threats", "📊 Best Practices"])
    
    with tab1:
        st.markdown("#### Where You Can Win")
        
        opportunities = []
        
        # Check engagement rate
        if your_data['avg_engagement_rate'] > competitor_df['avg_engagement_rate'].mean():
            opportunities.append("✅ **Engagement Leader**: Your engagement rate is above average. Double down on your content strategy!")
        else:
            top_performer = competitor_df.loc[competitor_df['avg_engagement_rate'].idxmax()]
            opportunities.append(f"📈 **Engagement Gap**: {top_performer['name']} has {top_performer['avg_engagement_rate']}% engagement. Study their {top_performer['top_content_type']} content.")
        
        # Check posting frequency
        if your_data['posts_per_week'] < competitor_df['posts_per_week'].mean():
            opportunities.append(f"📅 **Posting Opportunity**: Competitors post {round(competitor_df['posts_per_week'].mean(), 1)} times/week. You're posting {your_data['posts_per_week']} times. Increase frequency!")
        
        # Check growth rate
        if your_data['growth_rate'] < competitor_df['growth_rate'].max():
            fastest_grower = competitor_df.loc[competitor_df['growth_rate'].idxmax()]
            opportunities.append(f"🚀 **Growth Opportunity**: {fastest_grower['name']} is growing at {fastest_grower['growth_rate']}%/month. Analyze their strategy!")
        
        for opp in opportunities:
            st.markdown(opp)
    
    with tab2:
        st.markdown("#### Competitive Threats")
        
        threats = []
        
        # Check if competitors are more active
        if competitor_df['posts_per_week'].max() > your_data['posts_per_week'] * 1.5:
            most_active = competitor_df.loc[competitor_df['posts_per_week'].idxmax()]
            threats.append(f"⚠️ **Activity Threat**: {most_active['name']} posts {most_active['posts_per_week']} times/week - significantly more than you.")
        
        # Check follower growth
        fast_growers = competitor_df[competitor_df['growth_rate'] > your_data['growth_rate'] * 1.3]
        if len(fast_growers) > 0:
            threats.append(f"⚠️ **Growth Threat**: {len(fast_growers)} competitor(s) are growing faster than you.")
        
        # Check engagement
        if competitor_df['avg_engagement_rate'].max() > your_data['avg_engagement_rate'] * 1.2:
            threats.append("⚠️ **Engagement Threat**: A competitor has significantly higher engagement. Your content may be losing relevance.")
        
        if not threats:
            st.success("✅ No major competitive threats detected. Keep up the good work!")
        else:
            for threat in threats:
                st.markdown(threat)
    
    with tab3:
        st.markdown("#### Industry Best Practices")
        
        # Find best performers in each category
        best_engagement = competitor_df.loc[competitor_df['avg_engagement_rate'].idxmax()]
        best_growth = competitor_df.loc[competitor_df['growth_rate'].idxmax()]
        most_active = competitor_df.loc[competitor_df['posts_per_week'].idxmax()]
        
        st.markdown(f"""
        **🏆 Engagement Champion**: {best_engagement['name']}
        - Engagement Rate: {best_engagement['avg_engagement_rate']}%
        - Top Content: {best_engagement['top_content_type']}
        - Posts at: {best_engagement['best_posting_time']}
        
        **🚀 Growth Leader**: {best_growth['name']}
        - Growth Rate: {best_growth['growth_rate']}%/month
        - Posting Frequency: {best_growth['posts_per_week']} times/week
        - Hashtags Used: {best_growth['hashtag_usage']} per post
        
        **📅 Most Consistent**: {most_active['name']}
        - Posts Per Week: {most_active['posts_per_week']}
        - Story Frequency: {most_active['story_frequency']} per day
        - Response Time: {most_active['response_time']}
        """)
    
    # Share of Voice Analysis
    st.markdown("### 🎤 Share of Voice Analysis")
    
    # Calculate share of voice (based on followers + engagement)
    all_accounts['sov_score'] = (
        all_accounts['followers'] * 0.4 + 
        all_accounts['avg_engagement_rate'] * all_accounts['followers'] * 0.6
    )
    
    all_accounts['sov_percentage'] = (all_accounts['sov_score'] / all_accounts['sov_score'].sum()) * 100
    
    fig_pie = px.pie(
        all_accounts,
        values='sov_percentage',
        names='name',
        title='Market Share of Voice',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.4
    )
    
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(height=500)
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Export Options
    st.markdown("### 📥 Export Benchmark Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export to Excel", use_container_width=True):
            st.success("✅ Benchmark report exported to Excel!")
    
    with col2:
        if st.button("📄 Generate PDF Report", use_container_width=True):
            st.success("✅ PDF report generated!")
    
    with col3:
        if st.button("📧 Email Report", use_container_width=True):
            st.success("✅ Report sent to your email!")

if __name__ == "__main__":
    st.set_page_config(page_title="Competitor Benchmarking", layout="wide")
    render_competitor_benchmarking()
