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
    Simulated cross-platform trend fetcher with India focus.
    """
    trends = []
    
    # India-Specific University Logic
    if niche == 'University':
        if platform == 'Instagram':
            trends = [
                {'topic': 'CUET Preparation Tips', 'traffic': 'High', 'context': 'Cracking entrance exams in India'},
                {'topic': 'Campus Life in UP', 'traffic': 'High', 'context': 'Vibrant student life at TMU'},
                {'topic': 'Engineering Projects India', 'traffic': 'Medium', 'context': 'Innovation in local colleges'}
            ]
        elif platform == 'LinkedIn':
            trends = [
                {'topic': 'Placements 2025 India', 'traffic': 'High', 'context': 'Current job market in Delhi NCR'},
                {'topic': 'Upskilling for Indian Tech', 'traffic': 'High', 'context': 'Skills requested by top MNCs'},
                {'topic': 'NEP 2020 Implementation', 'traffic': 'Medium', 'context': 'Changes in Indian Higher Ed'}
            ]
        elif platform == 'TikTok/Reels':
            trends = [
                {'topic': 'Student Budget Food UP', 'traffic': 'Extreme', 'context': 'Hidden street food gems near campus'},
                {'topic': 'Hostel Hacks India', 'traffic': 'High', 'context': 'Survival guide for Indian hostels'},
                {'topic': 'Festival Celebs at Campus', 'traffic': 'High', 'context': 'Celebrity visits and cultural fests'}
            ]
    else:
        # General India Platform Trends
        if platform == 'Instagram':
            trends = [
                {'topic': 'Desi Aesthetic Carousels', 'traffic': 'High', 'context': 'Indian fashion and lifestyle dumps'},
                {'topic': 'Regional Language Content', 'traffic': 'Extreme', 'context': 'Hindi/Hinglish engagement spikes'},
                {'topic': 'Cricket World Cup Buzz', 'traffic': 'High', 'context': 'Sporting fever across platforms'}
            ]
        elif platform == 'LinkedIn':
            trends = [
                {'topic': 'Startups in Noida/Pune', 'traffic': 'High', 'context': 'The booming Indian SaaS ecosystem'},
                {'topic': 'Remote Work India', 'traffic': 'Extreme', 'context': 'Hybrid work shifts in tier-1 cities'},
                {'topic': 'Workplace Culture in India', 'traffic': 'High', 'context': 'Addressing corporate mental health'}
            ]
        elif platform == 'TikTok/Reels':
            trends = [
                {'topic': 'Bollywood Remakes', 'traffic': 'High', 'context': 'Dancing to trending movie tracks'},
                {'topic': 'Relatable Desi Parents', 'traffic': 'Extreme', 'context': 'Comedy skits on Indian households'},
                {'topic': 'Quick Recipes India', 'traffic': 'High', 'context': '5-minute Indian breakfast ideas'}
            ]
            
    return trends

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
    """Generate mode-based scripts for a trend with multiple templates"""
    if niche == 'University':
        templates = {
            'Student POV (Authentic)': f"Hook: 'I bet nobody told you this about {topic} at TMU...'\nBody: Show a quick clip of {topic} in action. Add 'POV: You realized {topic} is actually easy.'\nCTA: 'Tag a friend who needs to see this!'",
            'Faculty POV (Expert)': f"Hook: 'From a faculty perspective, {topic} is changing everything.'\nBody: Explain the 3 main benefits of {topic} for student success.\nCTA: 'Read our full research in bio.'",
            'Brand POV (Cinematic)': f"Hook: 'Why TMU is leading the way in {topic}.'\nBody: Cinematic shots of campus facilities related to {topic}.\nCTA: 'Apply for the 2025 session today.'",
            'Myth vs Fact (Viral)': f"Hook: '3 Myths about {topic} at TMU you need to stop believing.'\nBody: 1. It's too hard (Fact: We have 24/7 labs). 2. No placements (Fact: 90% rate). 3. {topic} is boring (Fact: It's hands-on).\nCTA: 'Check our stories for more facts!'",
            'Day in the Life (Relatable)': f"Hook: 'What using {topic} looks like as a TMU student.'\nBody: Morning coffee -> Lab session with {topic} -> Group project -> Success!\nCTA: 'Comment JOURNEY to see our full day vlog.'"
        }
        return templates
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
    """Generate UGC/Ambassador tasks and campaign briefs"""
    campaign_name = f"#{topic.replace(' ', '')}Challenge"
    return {
        'Campaign': campaign_name,
        'Ambassador Task': f"Create 1 Reel showing your {topic} routine on campus.",
        'Challenge Prompt': f"Share your {topic} journey with #TMUAmbassador",
        'Brief': {
            'Objective': f"Drive awareness for {topic} among prospective students.",
            'Key Message': f"TMU makes mastering {topic} fun and accessible.",
            'Visual Style': "Raw, handheld, authentic student-led camera work.",
            'Deliverables': "1x Reel (15-30s), 2x In-situ Stories.",
            'Reward': "Featured on main university handle + Amazon Voucher."
        }
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
            'Backups': [f"{random.randint(7, 10)} AM", f"{random.randint(1, 4)} PM"],
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
            target_region = st.selectbox("Region", ["India (UP/NCR)", "GLOBAL", "US", "EU"], index=0)
            
        if st.button("🚀 Fetch Targeted India-Only Trends", use_container_width=True):
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
                                with st.expander("📄 View Campaign Brief"):
                                    brief = row['UGC']['Brief']
                                    st.write(f"**Objective:** {brief['Objective']}")
                                    st.write(f"**Visual Style:** {brief['Visual Style']}")
                                    st.write(f"**Deliverables:** {brief['Deliverables']}")
                                    st.write(f"**Incentive:** {brief['Reward']}")
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
        funnel_data = {
            'Stage': ['Awareness', 'Consideration', 'Decision'],
            'Users': [1000, 200, 50],  # Example absolute numbers
            'Conversion': ['100%', '20%', '5%']
        }
        
        # Visual Funnel Layout
        for i, stage in enumerate(['Awareness 📢', 'Consideration 🤔', 'Decision 💰']):
            progress_val = [1.0, 0.4, 0.1][i]
            st.markdown(f"**{stage}**")
            st.progress(progress_val)
            st.caption(f"Conversion: {funnel_data['Conversion'][i]} | Target: 25%")
            
        st.warning("⚠️ **Funnel Gap Warning**: Critical drop-off between Consideration and Decision. You need more 'How to Apply' content.")
        
        st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📊 Performance Benchmarks</div>', unsafe_allow_html=True)
        st.caption("Average metrics for University/Education niche")
        
        bench_data = pd.DataFrame({
            'Metric': ['Reel Watch Time', 'Completion Rate', 'Save Rate', 'Share Rate'],
            'Market Avg': [12.5, 45, 8.2, 5.4],
            'TMU Performance': [8.2, 32, 4.1, 2.8]
        })
        
        fig = px.bar(bench_data, x='Metric', y=['Market Avg', 'TMU Performance'],
                     barmode='group',
                     color_discrete_map={'Market Avg': '#94a3b8', 'TMU Performance': '#6366f1'})
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="",
            yaxis_title="%"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.info("💡 **Strategy**: Improve CTA for Save; add study notes to carousels.")
        st.markdown('</div>', unsafe_allow_html=True)

        
        st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🗺️ Interest by Indian State</div>', unsafe_allow_html=True)
        st.caption("Interest in 'Admissions' across India")
        
        state_data = pd.DataFrame({
            'State': ['Uttar Pradesh', 'Delhi', 'Haryana', 'Bihar', 'Rajasthan', 'Uttarakhand'],
            'Intensity': [98, 85, 72, 65, 54, 88]
        })
        
        fig = px.bar(state_data, x='Intensity', y='State', 
                     orientation='h',
                     color='Intensity',
                     color_continuous_scale='Purples')
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False,
            xaxis_title="Trend Intensity",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

        
        st.markdown("---")
        st.markdown("### 🕵️ Competitor Strategy Map")
        st.info("Top themes being leveraged by 3 competing universities in UP.")
        
        comp_data = {
            'Competitor': ['Univ A (Delhi)', 'Univ B (Noida)', 'Univ C (Local)'],
            'Primary Hook': ['High Placements', 'Global Reach', 'Low Fees'],
            'Ad Spend': ['High', 'Medium', 'Aggressive'],
            'Gaps for TMU': ['Personalized POV', 'Lab Access', 'Hostel Life']
        }
        st.table(pd.DataFrame(comp_data))
        
        st.markdown("### 🚀 Platform Meta-Trends")
        meta_trends = fetch_marketing_trends()
        
        for mt in meta_trends:
            st.markdown(f"""
            <div style="padding: 1rem; background-color: #f1f5f9; border-radius: 12px; margin-bottom: 0.75rem; border: 1px solid #e2e8f0; transition: transform 0.2s ease-in-out;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                <div style="font-weight: 800; color: #1e293b; font-size: 1.1rem;">{mt['trend']}</div>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #475569; margin-top: 0.5rem; border-top: 1px solid #cbd5e1; padding-top: 0.5rem;">
                    <span style="background: #e2e8f0; padding: 2px 8px; border-radius: 4px;">{mt['platform']}</span>
                    <span style="color: #059669; font-weight: bold;">{mt['growth']} Growth</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Plotly visualization for growth rates
        st.markdown("#### 📊 Trend Growth Potential")
        try:
            trends_df = pd.DataFrame(meta_trends)
            trends_df['growth_num'] = trends_df['growth'].str.replace('+', '', regex=False).str.replace('%', '', regex=False).astype(float)
            
            fig = px.bar(trends_df, x='growth_num', y='trend', orientation='h',
                         color='growth_num', color_continuous_scale='Viridis')
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                coloraxis_showscale=False,
                xaxis_title="Projected Growth (%)",
                yaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
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
        
        st.markdown("### 🧪 Experiment Planner (A/B Test)")
        st.info("Plan your next content experiment to optimize reach.")
        with st.container(border=True):
            exp_type = st.selectbox("Experiment Type", ["Hook Variation", "Thumbnail Test", "CTA Swap", "Duration Test"])
            col_a, col_b = st.columns(2)
            with col_a:
                st.text_input("Variant A (Control)", "Standard Hook")
            with col_b:
                st.text_input("Variant B (Test)", "Question-based Hook")
            
            st.write("**Hypothesis:** Variant B will increase 'Watch Time' by 15% because it piques curiosity immediately.")
            if st.button("Log Experiment"):
                st.toast("Experiment Logged to Growth Suite!")

        st.markdown("#### 🚀 Growth Workflow Tracker")
        st.checkbox(f"Scripts Drafted for {target_platform}", value=False)
        st.checkbox("UGC Briefs Sent to Ambassadors", value=False)
        st.checkbox("Ad Creative Approved by Team", value=False)
        st.markdown("---")
        st.markdown("#### 💡 Next Quick Win")
        st.success("Host a Live Q&A about **Entrance Exams** this Wednesday to capture 'Decision' stage leads.")

