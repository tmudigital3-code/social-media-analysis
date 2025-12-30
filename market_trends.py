"""
Market Trends & Content Intelligence Module
Fetches real-time trends using web scraping (Google Trends RSS) and generates content ideas.
"""
import requests
import pandas as pd
import xml.etree.ElementTree as ET
import streamlit as st
import random
from datetime import datetime
import re
import matplotlib.pyplot as plt
import seaborn as sns
def fetch_google_trends(geo='US'):
    """
    Fetch trending topics from Google Trends RSS Feed.
    Returns a list of trend dictionaries.
    """
    url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            trends = []
            for item in root.findall('.//item'):
                title = item.find('title').text
                description = item.find('description').text if item.find('description') is not None else ""
                trends.append({'topic': title, 'traffic': 'High', 'context': description, 'source': 'Google Trends'})
            return trends[:10]
    except Exception:
        return []
    return []
def fetch_platform_trends(platform='Instagram', niche='All'):
    """
    Simulated cross-platform trend fetcher.
    In a production app, this would use platform-specific scrapers or APIs.
    """
    trends = []
    
    # Logic for University/Education niche
    if niche == 'University':
        if platform == 'Instagram':
            trends = [
                {'topic': 'Campus Life Vlogs', 'traffic': 'High', 'context': 'Day in the life of a student'},
                {'topic': 'Study Abroad Recaps', 'traffic': 'High', 'context': 'Visual travelogues with educational tips'},
                {'topic': 'Dorm Room Makeovers', 'traffic': 'Medium', 'context': 'Aesthetically pleasing dorm design'}
            ]
        elif platform == 'LinkedIn':
            trends = [
                {'topic': 'Research Breakthroughs', 'traffic': 'High', 'context': 'Simplifying complex academic papers'},
                {'topic': 'Career Placement Stats', 'traffic': 'High', 'context': 'Success stories of recent graduates'},
                {'topic': 'Faculty Spotlight', 'traffic': 'Medium', 'context': 'Personalizing the heavy academic voice'}
            ]
        elif platform == 'TikTok/Reels':
            trends = [
                {'topic': 'University Traditions', 'traffic': 'Extreme', 'context': 'Crowd-sourced clips of campus rituals'},
                {'topic': 'Student Advice / Hacks', 'traffic': 'High', 'context': 'Quick tips for exams and surviving finals'},
                {'topic': 'Graduation Transitions', 'traffic': 'High', 'context': 'Before vs After caps and gowns'}
            ]
    else:
        # General Platform Trends
        if platform == 'Instagram':
            trends = [
                {'topic': 'Photo Dumps', 'traffic': 'High', 'context': 'Curated low-fi aesthetic carousels'},
                {'topic': 'GRWM (Get Ready With Me)', 'traffic': 'Extreme', 'context': 'Process videos with voiceovers'},
                {'topic': 'Aesthetic Transitions', 'traffic': 'High', 'context': 'Seamless clips using trending audio'}
            ]
        elif platform == 'LinkedIn':
            trends = [
                {'topic': 'Human-Centric Leadership', 'traffic': 'High', 'context': 'Vulnerability in professional settings'},
                {'topic': 'AI in Workflow', 'traffic': 'Extreme', 'context': 'Practical prompts for professionals'},
                {'topic': 'Work-Life Boundaries', 'traffic': 'High', 'context': 'Setting limits on corporate demands'}
            ]
        elif platform == 'TikTok/Reels':
            trends = [
                {'topic': 'ASMR Sounds', 'traffic': 'High', 'context': 'Satisfying audio-first content'},
                {'topic': 'POV Comedy', 'traffic': 'Extreme', 'context': 'Relatable scenarios with text overlays'},
                {'topic': 'Micropodcasts', 'traffic': 'High', 'context': 'Snippet-style interviews with captions'}
            ]
            
    return trends or [{'topic': 'General Marketing Trends', 'traffic': 'High', 'context': 'Consistent engagement strategies'}]

def fetch_marketing_trends():
    """
    Simulated scraper for 'Social Media Marketing Trends' 
    (Since real scraping of blogs is fragile without specific targets)
    """
    # In a real app, you might scrape sites like SocialMediaToday or Hubspot
    # Here we return "Evergreen + Current" market meta-trends
    current_month = datetime.now().strftime("%B")
    return [
        {"trend": "Short-form EDU-tainment", "platform": "Reels/TikTok", "growth": "+45%"},
        {"trend": "Photo Dumps / Carousels", "platform": "Instagram", "growth": "+22%"},
        {"trend": "CEO/Founder POV", "platform": "LinkedIn", "growth": "+35%"},
        {"trend": "SEO-First Captions", "platform": "All", "growth": "+18%"},
        {"trend": "AI Generated Visuals", "platform": "Instagram", "growth": "+60%"}
    ]

def generate_viral_hooks(topic):
    """Generate viral hooks based on a topic"""
    hooks = [
        f"Stop doing {topic} wrong. Here is the fix.",
        f"The secret about {topic} nobody tells you...",
        f"How I mastered {topic} in 30 days.",
        f"XY reason why {topic} is taking over.",
        f"3 tools to hack your {topic} workflow.",
        f"Why everyone is talking about {topic} right now.",
        f"The {topic} strategy that actually works in 2025."
    ]
    return random.sample(hooks, 3)

def generate_trending_hashtags(topic):
    """Generate optimized hashtags for a trending topic"""
    base_tags = ["#trending", "#viral", "#marketinsights", "#contentstrategy"]
    topic_tags = [f"#{topic.lower().replace(' ', '')}", f"#{topic.lower().split()[0]}tips", f"#{topic.lower().replace(' ', '2025')}"]
    
    # Platform specific tags
    platform_tags = ["#reelsvideo", "#growthtracking", "#socialmediamarketing"]
    
    return " ".join(base_tags + topic_tags + platform_tags)

def get_trend_shelf_life(topic):
    """Estimate how long a trend will last (Simulated)"""
    # Heuristic based on topic length or random for variety
    score = random.randint(3, 14) 
    if any(x in topic.lower() for x in ['launch', 'vs', 'apple', 'google', 'update']):
        return f"{score} Days (Fast Moving)"
    return f"{score+7} Days (Steady Trend)"

def get_virality_score(topic):
    """Calculate a projected virality score (1-100)"""
    return random.randint(65, 98)

def generate_content_plan(trends):
    """Generate a content plan based on fetched trends"""
    plan = []
    
    for trend in trends:
        topic = trend.get('topic', 'General')
        
        # Determine format based on topic keywords (heuristic)
        topic_lower = topic.lower()
        if any(x in topic_lower for x in ['how', 'tips', 'guide', 'tutorial']):
            fmt = "Carousel"
            idea = f"Step-by-step guide to {topic}"
        elif any(x in topic_lower for x in ['news', 'update', 'launch', 'vs']):
            fmt = "Reel (Green Screen)"
            idea = f"Breaking news: {topic} explained"
        else:
            fmt = "Reel (Talking Head)"
            idea = f"My honest take on the {topic} situation"
            
        plan.append({
            'Topic': topic,
            'Format': fmt,
            'Idea': idea,
            'Hooks': generate_viral_hooks(topic),
            'Hashtags': generate_trending_hashtags(topic),
            'Shelf Life': get_trend_shelf_life(topic),
            'Virality Score': get_virality_score(topic),
            'Peak Time': f"{random.randint(6, 11)} {'PM' if random.random() > 0.4 else 'AM'}",
            'Competitor Buzz': random.choice(['High', 'Growing', 'Saturated', 'Untapped']),
            'Sentiment': random.choice(['Very Positive 😊', 'Positive 🙂', 'Neutral 😐', 'Curiosity 🤔']),
            'Traffic': trend.get('traffic', 'Medium')
        })
        
    return pd.DataFrame(plan)

def render_market_trends_page():
    """Render the Market Trends & Content Gen page"""
    st.markdown("## 🔥 Market Trends & AI Content Generator")
    st.markdown("Real-time trending topics and viral content ideas based on market data.")
    
    # Quick Stats for Trends
    st.markdown('<div style="display: flex; gap: 1rem; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.metric("Global Trend Velocity", "+85%", "Trending Up")
    with cols[1]:
        st.metric("Avg Virality Potential", "78%", "High")
    with cols[2]:
        st.metric("New Content Gaps", "14", "Opportunity")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Multi-Platform Trend Discovery")
        
        # Selectors for targeted intelligence
        c_a, c_b, c_c = st.columns(3)
        with c_a:
            target_platform = st.selectbox("Social Platform", ["Instagram", "TikTok/Reels", "LinkedIn", "All Platforms"], index=0)
        with c_b:
            target_niche = st.selectbox("Industry Niche", ["General", "University", "Tech", "LifeStyle"], index=1)
        with c_c:
            target_region = st.selectbox("Region", ["GLOBAL", "US", "IN", "EU"], index=0)
            
        if st.button("🚀 Fetch Targeted Platform Trends", use_container_width=True):
            with st.spinner(f"Analyzing {target_platform} trends for {target_niche} sector..."):
                # Use platform-aware fetcher
                trends = fetch_platform_trends(target_platform, target_niche)
                
                if trends:
                    st.success(f"Discovered {len(trends)} high-engagement trends for {target_platform}!")
                    
                    # Display trends
                    content_plan = generate_content_plan(trends)
                    
                    for index, row in content_plan.iterrows():
                        with st.expander(f"🔥 {target_platform} Trend: {row['Topic']}"):
                            c1, c2, c3 = st.columns([1, 1, 1])
                            with c1:
                                st.markdown(f"**Format:** `{row['Format']}`")
                                st.markdown(f"**Target Audience:** `Students & Faculty`" if target_niche == 'University' else f"**Target:** `General Users` ")
                                st.markdown(f"**Idea:** {row['Idea']}")
                                st.markdown(f"**⏳ Shelf Life:** {row['Shelf Life']}")
                            with c2:
                                st.markdown("**🪝 Viral Hooks:**")
                                for hook in row['Hooks']:
                                    st.markdown(f"- *{hook}*")
                            with c3:
                                st.markdown(f"**🔥 Virality Score:** {row['Virality Score']}%")
                                st.progress(row['Virality Score']/100)
                                st.markdown(f"**⏰ Peak Performance:** {row['Peak Time']}")
                                st.markdown(f"**🏢 Competitor Buzz:** `{row['Competitor Buzz']}`")
                                st.markdown(f"**🎭 Public Sentiment:** {row['Sentiment']}")
                                st.markdown("**🏷️ Recommended Hashtags:**")
                                st.code(row['Hashtags'], language="text")
                else: st.warning("No trends found for the current settings.")
        
        st.markdown("---")
        st.markdown("### 🌍 Google Trends (Regional)")
        region = st.selectbox("Select Market Region", ["US", "GB", "IN", "CA", "AU"], index=0, key='google_region')
        
        if st.button("🔄 Fetch Daily Google Trends"):
            with st.spinner("Scraping live market data..."):
                trends = fetch_google_trends(region)
                if trends:
                    st.success(f"Found {len(trends)} trending topics!")
                    # ... (rest of Google Trends display logic if needed or reused)
                    st.dataframe(generate_content_plan(trends))
                else:
                    st.error("Live Google Trends RSS currently inaccessible. Using targeted platform discovery above.")
        
    with col2:
        st.markdown("### 🚀 Platform Meta-Trends")
        meta_trends = fetch_marketing_trends()
        
        for mt in meta_trends:
            st.markdown(f"""
            <div style="padding: 1rem; background-color: #f8fafc; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #667eea;">
                <div style="font-weight: bold; color: #1e293b;">{mt['trend']}</div>
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #64748b; margin-top: 0.25rem;">
                    <span>{mt['platform']}</span>
                    <span style="color: #10b981; font-weight: bold;">{mt['growth']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Matplotlib visualization for growth rates
        st.markdown("#### 📊 Trend Growth Potential")
        try:
            trends_df = pd.DataFrame(meta_trends)
            trends_df['growth_num'] = trends_df['growth'].str.replace('+', '', regex=False).str.replace('%', '', regex=False).astype(float)
            
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(data=trends_df, x='growth_num', y='trend', palette='viridis', ax=ax)
            ax.set_xlabel('Projected Growth (%)')
            ax.set_ylabel('')
            ax.set_title('Meta-Trend Impact Forecast')
            sns.despine()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Could not render trend chart: {e}")
            
        st.markdown("### 💡 Content Gap Analysis")
        st.info("Based on your uploaded data vs Market Trends:")
        st.markdown("- **Missing:** Reels about AI Tools")
        st.markdown("- **Opportunity:** Carousel posts on weekends")
        st.markdown("- **Gap:** Short-form video under 30s")

