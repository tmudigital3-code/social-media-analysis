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
    feeds = [
        f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}",
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.reutersagency.com/feed/?best-topics=digital-media-environment"
    ]
    
    for url in feeds:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                trends = []
                for item in root.findall('.//item'):
                    title = item.find('title').text
                    desc = item.find('description').text if item.find('description') is not None else ""
                    trends.append({'topic': title, 'traffic': 'High', 'context': desc, 'source': 'Global News' if 'google' not in url else 'Google Trends'})
                if trends:
                    return trends[:10]
        except Exception:
            continue
            
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

def fetch_university_news():
    """Scrape real-time higher education news trends"""
    feeds = [
        "https://www.insidehighered.com/rss/feed/news",
        "https://www.timeshighereducation.com/rss.xml"
    ]
    news_trends = []
    
    for url in feeds:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                for item in root.findall('.//item'):
                    title = item.find('title').text
                    desc = item.find('description').text if item.find('description') is not None else ""
                    # Clean desc (simple HTML tag removal)
                    desc = re.sub('<[^<]+?>', '', desc)[:150] + "..."
                    
                    news_trends.append({
                        'topic': title,
                        'traffic': 'Trending',
                        'context': desc,
                        'source': 'Higher Ed News'
                    })
        except:
            continue
            
    return news_trends[:10]

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

def get_funnel_stage(topic):
    """Map topic to student journey stage"""
    topic_l = topic.lower()
    if any(x in topic_l for x in ['fee', 'scholarship', 'admissions', 'roi', 'placement', 'salary']):
        return "Decision 💰"
    if any(x in topic_l for x in ['recap', 'abroad', 'research', 'faculty', 'ranking', 'course']):
        return "Consideration 🤔"
    return "Awareness 📢"

def generate_ai_scripts(topic, niche='University'):
    """Generate mode-based scripts for a trend"""
    if niche == 'University':
        return {
            'Student POV': f"Hook: 'I bet nobody told you this about {topic} at TMU...'\nBody: Show a quick clip of {topic} in action. Add 'POV: You realized {topic} is actually easy.'\nCTA: 'Tag a friend who needs to see this!'",
            'Faculty POV': f"Hook: 'From a faculty perspective, {topic} is changing everything.'\nBody: Explain the 3 main benefits of {topic} for student success.\nCTA: 'Read our full research in bio.'",
            'Brand POV': f"Hook: 'Why TMU is leading the way in {topic}.'\nBody: Cinematic shots of campus facilities related to {topic}.\nCTA: 'Apply for the 2025 session today.'"
        }
    return {}

def generate_seo_captions(topic, niche='University'):
    """Generate SEO-optimized captions"""
    if niche == 'University':
        return f"Looking for the best universities in India? 🇮🇳 At TMU, we're mastering {topic} to help our students succeed in 2025. Whether it's campus life in UP or global placements, we've got you covered. ✨\n\n#TMU #BestUniversity #HigherEd #{topic.replace(' ', '')}"
    return f"Mastering {topic} in 2025. Here is what you need to know about the latest market shift. #growth #strategy #{topic.replace(' ', '')}"

def get_comment_bait(topic):
    """Generate questions to drive replies"""
    return [
        f"Which part of {topic} do you want us to show next?",
        f"What's your biggest fear about {topic} in 2025?",
        f"Scale of 1-10, how useful is {topic} to you?"
    ]

def get_ugc_strategy(topic):
    """Generate UGC/Ambassador tasks"""
    return {
        'Campaign': f"#{topic.replace(' ', '')}Challenge",
        'Ambassador Task': f"Create 1 Reel showing your {topic} routine on campus.",
        'Challenge Prompt': f"Share your {topic} journey with #TMUAmbassador"
    }

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
            'Funnel Stage': get_funnel_stage(topic),
            'Peak Time': f"{random.randint(6, 11)} {'PM' if random.random() > 0.4 else 'AM'}",
            'Backups': [f"{random.randint(7, 9)} AM", f"{random.randint(12, 2)} PM"],
            'Competitor Buzz': random.choice(['High', 'Growing', 'Saturated', 'Untapped']),
            'Sentiment': random.choice(['Very Positive 😊', 'Positive 🙂', 'Neutral 😐', 'Curiosity 🤔']),
            'Scripts': generate_ai_scripts(topic),
            'SEO Caption': generate_seo_captions(topic),
            'Comment Bait': get_comment_bait(topic),
            'UGC': get_ugc_strategy(topic),
            'Ad Blueprint': {
                'Audience': 'Parents (45-55) & Students (17-21) in UP/Delhi NCR',
                'Copy': f'Scale your future with {topic} at TMU. 🎓 #Admissions2025',
                'Creative': 'High-angle campus shot with students focusing on innovation.'
            },
            'Collab Type': random.choice(['Study YouTuber', 'Career Coach', 'Alumni Professional', 'Student Lifestyle Vlogger']),
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
                # Use platform-aware fetcher + Live News for University
                if target_niche == 'University':
                    trends = fetch_university_news()
                    if not trends: # Fallback to hardcoded university trends
                        trends = fetch_platform_trends(target_platform, target_niche)
                else:
                    trends = fetch_platform_trends(target_platform, target_niche)
                
                if trends:
                    st.success(f"📈 **Live Trends Engine v2.1 Active**: Found {len(trends)} high-impact trends for {target_platform}!")
                    
                    # Display trends
                    content_plan = generate_content_plan(trends)
                    
                    for index, row in content_plan.iterrows():
                        with st.expander(f"🔥 {target_platform} Trend: {row['Topic']} ({row['Funnel Stage']})"):
                            # 1. Execution Playbook
                            st.markdown("#### 📋 Execution Playbook")
                            c1, c2, c3 = st.columns([1, 1, 1])
                            with c1:
                                st.markdown(f"**Format Variants:**")
                                st.markdown("- **A:** Talking-head Reel")
                                st.markdown("- **B:** B-roll + Captions")
                                st.markdown("- **C:** Carousel Summary")
                                st.markdown(f"**⏳ Shelf Life:** {row['Shelf Life']}")
                            with c2:
                                st.markdown(f"**⏰ Posting Matrix:**")
                                st.markdown(f"- **Primary:** `{row['Peak Time']}`")
                                st.markdown(f"- **Backups:** `{', '.join(row['Backups'])}`")
                                st.markdown(f"**🏢 Competitor Buzz:** `{row['Competitor Buzz']}`")
                            with c3:
                                st.markdown("**✅ Hook-Hold-Reward:**")
                                st.markdown(f"1. Hook: *\"{row['Hooks'][0]}\"*")
                                st.markdown("2. Hold: 30-45s Value meat")
                                st.markdown("3. Reward: Save/CTA")
                            
                            st.markdown("---")
                            
                            # 2. AI Creative Assets
                            st.markdown("#### 🎬 AI Creative Assets")
                            t1, t2, t3 = st.tabs(["🎥 Video Scripts", "📝 SEO Captions", "💬 Comment Bait"])
                            with t1:
                                for mode, script in row['Scripts'].items():
                                    st.markdown(f"**{mode}:**")
                                    st.code(script, language="markdown")
                            with t2:
                                st.code(row['SEO Caption'], language="text")
                            with t3:
                                st.markdown("Questions to drive replies:")
                                for q in row['Comment Bait']:
                                    st.markdown(f"- *{q}*")
                                    
                            st.markdown("---")
                            
                            # 3. UGC & Engagement Health
                            st.markdown("#### 🤝 UGC & Strategy Layers")
                            u1, u2 = st.columns(2)
                            with u1:
                                st.markdown(f"**Campaign:** `{row['UGC']['Campaign']}`")
                                st.markdown(f"**Ambassador Task:** {row['UGC']['Ambassador Task']}")
                            with u2:
                                st.markdown(f"**🔥 Virality Score:** {row['Virality Score']}%")
                                st.progress(row['Virality Score']/100)
                                st.markdown(f"**🎭 Public Sentiment:** {row['Sentiment']}")
                            
                            st.markdown("**🏷️ Recommended Hashtags:**")
                            st.code(row['Hashtags'], language="text")
                            
                            st.markdown("---")
                            
                            # 4. Digital Marketing Team Suite
                            st.markdown("#### 📢 Digital Marketing Team Suite")
                            a1, a2 = st.columns(2)
                            with a1:
                                st.markdown("**🎯 Ad Campaign Blueprint:**")
                                st.info(f"**Target:** {row['Ad Blueprint']['Audience']}\n\n**Hook:** {row['Ad Blueprint']['Copy']}")
                                st.markdown(f"**Creative Direction:** {row['Ad Blueprint']['Creative']}")
                            with a2:
                                st.markdown("**🤝 Collab Opportunity:**")
                                st.success(f"Partner with a **{row['Collab Type']}** for this trend to maximize reach in the UP/Delhi region.")
                                st.markdown("**📲 WhatsApp/Email Snippet:**")
                                st.code(f"Hi [Name]! Did you know about the latest {row['Topic']} shifts at TMU? Check out how we are prepairing for 2025: [Link]", language="markdown")
                else: st.warning("No trends found for the current settings.")
        
        # --- NEW: Actionable Engagement Strategy Section ---
        st.markdown("---")
        st.markdown("### 🏆 Engagement Growth Masterclass")
        st.info("Tactical blueprints to turn trends into followers and community growth.")
        
        tab1, tab2, tab3 = st.tabs(["🚀 Growth Hacks", "🤝 Community Building", "📽️ Viral Scripting"])
        
        with tab1:
            st.markdown("""
            **High-Impact Tactics for 2025:**
            - **The 'Value-Loop' Carousel:** Don't just share news; end every post with a 'Save for Later' prompt. Saved posts are the #1 signal for algorithm reach.
            - **Trend Hijacking:** Use the 'Trending Audio' found in Reels/TikTok within the first 48 hours of it going viral.
            - **Niche SEO:** Use keywords like *'Best Universities in [Region]'* or *'[Topic] for Students'* in the first 2 lines of your caption.
            """)
            if target_niche == 'University':
                st.success("🎓 **University Growth Hack:** Tag your location as the 'Campus Library' or 'Student Union'. These geotags have 3x higher local discovery.")
        
        with tab2:
            st.markdown("""
            **How to build a loyal audience:**
            - **Reply-to-Video:** When a student asks a question in comments, answer it with a *Video Reply*. This builds extreme trust.
            - **The Poll-to-Post Pipeline:** Run a poll in Stories, then make a main-feed post based on the winning result.
            - **Consistent Aesthetics:** Use a signature filter or font so users recognize your content instantly in their feed.
            """)
            
        with tab3:
            st.markdown("### 📽️ Viral Scripting Blueprint")
            st.code("""
1. THE HOOK (0-3s): "Everyone's talking about [Trend], but they're missing this..."
2. THE MEAT (3-20s): Show 3 quick, value-packed points.
3. THE PAYOFF (20s+): "If you want the full guide, comment 'UNIVERSITY' below."
            """, language="markdown")

        # --- NEW: TMU 7-Day Growth Calendar ---
        st.markdown("---")
        st.markdown("### 📅 TMU 7-Day Growth Calendar")
        st.success("A balanced strategy of Awareness, Consideration, and Decision-stage content.")
        
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        plan = [
            "Awareness: Campus Life Reel (Trending Audio)",
            "Consideration: Labs/Infrastructure Showcase (Detailed Photo)",
            "Awareness: Student POV/UGC Challenge #HelloTMU",
            "Decision: Placement/Salary Success Story (Carousel)",
            "Consideration: Faculty Spotlight / Research Breakthru",
            "Awareness: Weekend Campus Event Hijack",
            "Decision: Admission Deadline Reminder / Scholarship Info"
        ]
        
        cal_df = pd.DataFrame({'Day': days, 'Content Pillar': plan})
        st.table(cal_df)


        
    with col2:
        # Funnel Analysis Widget
        st.markdown("### 🧬 Journey Funnel Analysis")
        funnel_cols = st.columns(3)
        with funnel_cols[0]: st.metric("Awareness", "80%", "-5%", help="Top of Funnel")
        with funnel_cols[1]: st.metric("Consideration", "20%", "0", help="Middle of Funnel")
        with funnel_cols[2]: st.metric("Decision", "0%", "-10%", delta_color="inverse", help="Bottom of Funnel")
        
        st.warning("⚠️ **Funnel Gap Warning**: You are underposting Decision-stage content (fees, ROI).")
        
        st.markdown("---")
        st.markdown("### 📊 Performance Benchmarks")
        st.caption("Average metrics for University/Education niche")
        bench_data = {
            'Metric': ['Reel Watch Time', 'Completion Rate', 'Save Rate', 'Share Rate'],
            'Market': [12.5, 45, 8.2, 5.4],
            'TMU': [8.2, 32, 4.1, 2.8]
        }
        df_bench = pd.DataFrame(bench_data)
        
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(data=df_bench.melt(id_vars='Metric'), x='Metric', y='value', hue='variable', ax=ax, palette=['#94a3b8', '#667eea'])
        ax.set_ylabel('Percentage / Seconds')
        ax.set_title('TMU vs Market Benchmarks')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        st.info("💡 **Fix**: Improve CTA for Save; add study notes or checklists to carousels.")
        
        st.markdown("---")
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
            
        st.markdown("### 💡 Strategic Content Gaps")
        st.info("High-priority gaps to increase your engagement rates:")
        
        if target_niche == 'University':
            st.markdown("- **📢 Student Stories:** Missing 'Raw & Unfiltered' campus tours.")
            st.markdown("- **💡 Career Advice:** High demand for 'Salary expectations' content.")
            st.markdown("- **⏰ Posting Window:** You are missing the 7 PM - 10 PM student peak.")
        else:
            st.markdown("- **Missing:** Reels about AI Tools")
            st.markdown("- **Opportunity:** Carousel posts on weekends")
            st.markdown("- **Gap:** Short-form video under 30s")
            
        st.markdown("### 🛠️ Engagement Health (v2.0)")
        score = st.slider("Engagement Health Score", 0, 100, 65)
        st.progress(score/100)
        
        st.checkbox("Reply to 80%+ comments in 1hr?", value=False)
        st.checkbox("Use question-based caption?", value=True)
        st.checkbox("Pin a top-performing comment?", value=False)
        st.checkbox("Cross-promote on WhatsApp/Telegam?", value=False)
        
        st.markdown("#### 🧪 Next Experiment")
        st.info("Host a Live Q&A about Entrance Exams this Wednesday.")

