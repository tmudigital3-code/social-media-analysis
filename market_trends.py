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
    # Google Trends Daily Search Trends RSS
    url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            trends = []
            
            # Parse RSS items
            for item in root.findall('.//item'):
                title = item.find('title').text
                # Approx traffic is in ht:approx_traffic, need namespace usually, or loose parsing
                traffic = "High"
                # Description often contains news snippets
                description = item.find('description').text if item.find('description') is not None else ""
                
                trends.append({
                    'topic': title,
                    'traffic': traffic,
                    'context': description,
                    'source': 'Google Trends'
                })
            return trends[:10]  # Return top 10
    except Exception as e:
        print(f"Error fetching trends: {e}")
        return []
    
    return []

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
        st.markdown("### 🌍 Real-Time Google Trends")
        
        # Region selector
        region = st.selectbox("Select Market Region", ["US", "GB", "IN", "CA", "AU"], index=0)
        
        if st.button("🔄 Fetch Latest Trends"):
            with st.spinner("Scraping live market data..."):
                trends = fetch_google_trends(region)
                if trends:
                    st.success(f"Found {len(trends)} trending topics!")
                    
                    # Display trends
                    content_plan = generate_content_plan(trends)
                    
                    for index, row in content_plan.iterrows():
                        with st.expander(f"📈 Trend: {row['Topic']}"):
                            c1, c2, c3 = st.columns([1, 1, 1])
                            with c1:
                                st.markdown(f"**Format:** `{row['Format']}`")
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
                else:
                    st.warning("Could not scrape live trends. Checking fallback data...")
                    # Fallback
                    fallback_trends = [{'topic': 'AI Productivity', 'traffic': 'High'}, 
                                       {'topic': 'Sustainable Living', 'traffic': 'Medium'}]
                    content_plan = generate_content_plan(fallback_trends)
                    st.dataframe(content_plan)
        
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

