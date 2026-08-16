import streamlit as st
import markdown
from datetime import datetime
<<<<<<< Updated upstream
from pipeline import run_reseacrh_pipeline
=======
from pipeline import run_research_pipeline
>>>>>>> Stashed changes

# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(
<<<<<<< Updated upstream
    page_title="AI Research Agent", 
    page_icon="🔬", 
=======
    page_title="AI Research Agent",
    page_icon="🔬",
>>>>>>> Stashed changes
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    st.markdown("""
    <style>
<<<<<<< Updated upstream
        /* Import Inter Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Global Overrides */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        .stApp {
            background-color: #ffffff;
            color: #1a1a1a;
        }

        /* Hide Streamlit defaults */
=======
        /* Fonts: Space Grotesk for display, Inter for body/UI */
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

        :root {
            --bg-base: #F5F7FC;
            --surface-glass: rgba(255, 255, 255, 0.58);
            --surface-glass-strong: rgba(255, 255, 255, 0.80);
            --border-glass: rgba(255, 255, 255, 0.85);
            --text-primary: #1E2333;
            --text-secondary: #5B6478;
            --accent-1: #4F46E5;   /* indigo   */
            --accent-2: #7C3AED;   /* violet   */
            --accent-3: #06B6D4;   /* cyan     */
            --accent-warm: #FB7185; /* coral    */
            --success: #14B8A6;
            --shadow-glass: 0 8px 32px rgba(30, 35, 51, 0.08);
            --shadow-glass-lg: 0 16px 48px rgba(30, 35, 51, 0.12);
        }

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        /* Respect reduced-motion preference */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }

        .stApp {
            background-color: var(--bg-base);
            color: var(--text-primary);
        }

>>>>>>> Stashed changes
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

<<<<<<< Updated upstream
        /* Typography */
        h1, h2, h3, h4 {
            font-weight: 700 !important;
            letter-spacing: -0.5px;
            color: #1a1a1a !important;
        }

        /* Buttons */
        .stButton > button {
            background-color: #FF6B35;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(255, 107, 53, 0.2);
        }
        .stButton > button:hover {
            background-color: #FF5512;
            transform: translateY(-1px);
            box-shadow: 0 6px 12px rgba(255, 107, 53, 0.3);
        }
        .stButton > button:disabled {
            background-color: #e0e0e0;
            color: #a0a0a0;
            box-shadow: none;
        }

        /* Cards */
        .custom-card {
            background-color: #ffffff;
            border: 1px solid #f0f0f0;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            margin-bottom: 16px;
        }

        /* Stepper UI */
=======
        /* ---------- Aurora mesh backdrop (light, never dark) ---------- */
        .aurora-bg {
            position: fixed;
            inset: 0;
            z-index: -1;
            overflow: hidden;
            pointer-events: none;
        }
        .aurora-blob {
            position: absolute;
            border-radius: 50%;
            filter: blur(90px);
            opacity: 0.45;
            will-change: transform;
        }
        .blob-1 {
            width: 480px; height: 480px;
            top: -140px; left: -120px;
            background: radial-gradient(circle, var(--accent-1), transparent 70%);
            animation: drift1 24s ease-in-out infinite;
        }
        .blob-2 {
            width: 520px; height: 520px;
            bottom: -180px; right: -100px;
            background: radial-gradient(circle, var(--accent-3), transparent 70%);
            animation: drift2 28s ease-in-out infinite;
        }
        .blob-3 {
            width: 380px; height: 380px;
            top: 35%; right: 12%;
            background: radial-gradient(circle, var(--accent-warm), transparent 70%);
            opacity: 0.30;
            animation: drift3 26s ease-in-out infinite;
        }
        @keyframes drift1 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(60px, 40px) scale(1.12); }
        }
        @keyframes drift2 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(-50px, -30px) scale(1.08); }
        }
        @keyframes drift3 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(-30px, 50px) scale(0.92); }
        }

        /* ---------- Typography ---------- */
        h1, h2, h3, h4 {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700 !important;
            letter-spacing: -0.4px;
            color: var(--text-primary) !important;
        }
        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 2.6rem;
            text-align: center;
            background: linear-gradient(120deg, var(--accent-1), var(--accent-2) 45%, var(--accent-3));
            background-size: 200% auto;
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer 6s ease-in-out infinite;
            margin-bottom: 0;
        }
        @keyframes shimmer {
            0%, 100% { background-position: 0% center; }
            50% { background-position: 100% center; }
        }
        .hero-subtitle {
            text-align: center;
            color: var(--text-secondary);
            font-size: 1.02rem;
            margin-top: 4px;
            margin-bottom: 28px;
        }

        /* ---------- Buttons ---------- */
        .stButton > button, .stDownloadButton > button {
            background: linear-gradient(135deg, var(--accent-1) 0%, var(--accent-2) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 24px;
            font-weight: 600;
            letter-spacing: 0.2px;
            box-shadow: 0 4px 16px rgba(79, 70, 229, 0.30);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 24px rgba(79, 70, 229, 0.40);
        }
        .stButton > button:active, .stDownloadButton > button:active {
            transform: translateY(0);
        }
        .stButton > button:disabled {
            background: rgba(148, 163, 184, 0.35);
            color: rgba(100, 116, 139, 0.7);
            box-shadow: none;
        }
        /* Secondary-kind buttons (e.g. Reset) rendered as a quieter glass pill */
        button[kind="secondary"], button[data-testid="stBaseButton-secondary"] {
            background: var(--surface-glass) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-glass) !important;
            backdrop-filter: blur(12px);
            box-shadow: var(--shadow-glass) !important;
        }
        button[kind="secondary"]:hover, button[data-testid="stBaseButton-secondary"]:hover {
            box-shadow: var(--shadow-glass-lg) !important;
        }

        /* ---------- Glass cards ---------- */
        .custom-card {
            background: var(--surface-glass);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid var(--border-glass);
            border-radius: 20px;
            padding: 26px 28px;
            box-shadow: var(--shadow-glass);
            margin-bottom: 18px;
            animation: fadeInUp 0.5s ease both;
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(14px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* ---------- Agent pipeline stepper ---------- */
>>>>>>> Stashed changes
        .stepper-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
<<<<<<< Updated upstream
            margin: 40px 0 30px 0;
=======
            margin: 36px 0 30px 0;
>>>>>>> Stashed changes
            position: relative;
        }
        .step-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            z-index: 2;
            position: relative;
        }
<<<<<<< Updated upstream
        .step-circle {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: #ffffff;
            border: 2px solid #e6e6e6;
            color: #999;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            transition: all 0.4s ease;
=======
        .step-orb {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: var(--surface-glass);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-glass);
            box-shadow: var(--shadow-glass);
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
>>>>>>> Stashed changes
        }
        .step-label {
            margin-top: 8px;
            font-size: 13px;
<<<<<<< Updated upstream
            color: #999;
=======
            color: var(--text-secondary);
>>>>>>> Stashed changes
            font-weight: 500;
        }
        .step-line {
            flex: 1;
<<<<<<< Updated upstream
            height: 2px;
            background-color: #e6e6e6;
            margin: 0 -5px 22px -5px;
            z-index: 1;
            transition: background-color 0.4s ease;
        }
        
        /* Active & Completed States */
        .step-wrapper.active .step-circle {
            border-color: #FF6B35;
            color: #FF6B35;
            box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.15);
            animation: pulse 2s infinite;
        }
        .step-wrapper.active .step-label {
            color: #FF6B35;
            font-weight: 600;
        }
        .step-wrapper.completed .step-circle {
            background-color: #FF6B35;
            border-color: #FF6B35;
            color: white;
        }
        .step-wrapper.completed .step-label {
            color: #1a1a1a;
            font-weight: 500;
        }
        .step-line.active, .step-line.completed {
            background-color: #FF6B35;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(255, 107, 53, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(255, 107, 53, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 107, 53, 0); }
        }

        /* Markdown Content Polish */
        .report-content h1, .report-content h2, .report-content h3 {
            border-bottom: 1px solid #f0f0f0;
            padding-bottom: 8px;
            margin-top: 24px;
        }
        .report-content p {
            line-height: 1.7;
            color: #333;
        }
        .report-content code {
            background-color: #f4f4f4;
=======
            height: 3px;
            border-radius: 3px;
            background: rgba(148, 163, 184, 0.25);
            margin: 0 -4px 24px -4px;
            position: relative;
            overflow: hidden;
            z-index: 1;
        }
        .step-wrapper.active .step-orb {
            border-color: var(--accent-1);
            color: var(--accent-1);
            box-shadow: 0 0 0 6px rgba(79, 70, 229, 0.14), 0 0 18px rgba(79, 70, 229, 0.35);
            animation: pulseGlow 1.8s ease-in-out infinite;
        }
        .step-wrapper.active .step-label { color: var(--accent-1); font-weight: 600; }
        .step-wrapper.completed .step-orb {
            background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
            border-color: transparent;
            color: white;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
        }
        .step-wrapper.completed .step-label { color: var(--text-primary); font-weight: 500; }
        .step-line.completed { background: linear-gradient(90deg, var(--accent-1), var(--accent-2)); }
        .step-line.active { background: rgba(79, 70, 229, 0.20); }
        .step-line.active::after {
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 40%; height: 100%;
            background: linear-gradient(90deg, transparent, var(--accent-1), transparent);
            animation: flowAcross 1.6s ease-in-out infinite;
        }
        @keyframes flowAcross {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(350%); }
        }
        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 0 0 6px rgba(79, 70, 229, 0.14), 0 0 18px rgba(79, 70, 229, 0.35); }
            50% { box-shadow: 0 0 0 10px rgba(79, 70, 229, 0.08), 0 0 26px rgba(79, 70, 229, 0.45); }
        }

        /* ---------- Sidebar ---------- */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(255,255,255,0.75), rgba(245,247,252,0.60));
            backdrop-filter: blur(18px);
            border-right: 1px solid var(--border-glass);
        }
        [data-testid="stSidebar"] h3 { color: var(--text-primary); }

        /* ---------- Inputs ---------- */
        .stTextInput > div > div > input {
            background: var(--surface-glass-strong) !important;
            border: 1px solid var(--border-glass) !important;
            border-radius: 12px !important;
            color: var(--text-primary) !important;
            padding: 10px 14px !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: var(--accent-1) !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
        }

        /* ---------- Expander & text areas ---------- */
        [data-testid="stExpander"] {
            background: var(--surface-glass);
            backdrop-filter: blur(14px);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            box-shadow: var(--shadow-glass);
        }
        .stTextArea textarea {
            background: rgba(255, 255, 255, 0.65) !important;
            border-radius: 12px !important;
            border: 1px solid var(--border-glass) !important;
            font-family: 'Inter', monospace;
        }

        /* ---------- Alerts ---------- */
        [data-testid="stAlert"] {
            border-radius: 14px;
            backdrop-filter: blur(10px);
        }

        /* ---------- Markdown report content ---------- */
        .report-content h1, .report-content h2, .report-content h3 {
            border-bottom: 1px solid rgba(148, 163, 184, 0.25);
            padding-bottom: 8px;
            margin-top: 24px;
        }
        .report-content p { line-height: 1.7; color: var(--text-primary); }
        .report-content code {
            background-color: rgba(79, 70, 229, 0.08);
            color: var(--accent-1);
>>>>>>> Stashed changes
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }
    </style>
<<<<<<< Updated upstream
=======
    <div class="aurora-bg">
        <div class="aurora-blob blob-1"></div>
        <div class="aurora-blob blob-2"></div>
        <div class="aurora-blob blob-3"></div>
    </div>
>>>>>>> Stashed changes
    """, unsafe_allow_html=True)

load_css()

# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================
if 'pipeline_running' not in st.session_state:
    st.session_state.pipeline_running = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'research_data' not in st.session_state:
    st.session_state.research_data = {}
if 'pipeline_gen' not in st.session_state:
    st.session_state.pipeline_gen = None
if 'error' not in st.session_state:
    st.session_state.error = None
<<<<<<< Updated upstream
=======
if 'topic' not in st.session_state:
    st.session_state.topic = ""
>>>>>>> Stashed changes

# ==========================================
# 3. UI COMPONENTS & HELPER FUNCTIONS
# ==========================================
def render_stepper(current_step):
<<<<<<< Updated upstream
    """Renders a custom HTML/CSS horizontal stepper."""
=======
    """Renders a glass-orb horizontal stepper for the agent pipeline."""
>>>>>>> Stashed changes
    steps = [
        ("1", "Search"),
        ("2", "Reader"),
        ("3", "Writer"),
        ("4", "Critic")
    ]
<<<<<<< Updated upstream
    
=======

>>>>>>> Stashed changes
    html = '<div class="stepper-container">'
    for i, (num, label) in enumerate(steps):
        step_num = i + 1
        status_class = ""
        if current_step == 5 or current_step > step_num:
            status_class = "completed"
        elif current_step == step_num:
            status_class = "active"
<<<<<<< Updated upstream
            
        html += f'''
        <div class="step-wrapper {status_class}">
            <div class="step-circle">{num if status_class != "completed" else "✓"}</div>
=======

        html += f'''
        <div class="step-wrapper {status_class}">
            <div class="step-orb">{num if status_class != "completed" else "✓"}</div>
>>>>>>> Stashed changes
            <div class="step-label">{label}</div>
        </div>
        '''
        if i < len(steps) - 1:
            line_status = ""
            if current_step == 5 or current_step > step_num + 1:
                line_status = "completed"
            elif current_step == step_num + 1:
                line_status = "active"
            html += f'<div class="step-line {line_status}"></div>'
<<<<<<< Updated upstream
            
=======

>>>>>>> Stashed changes
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def create_html_download(topic, report, feedback):
<<<<<<< Updated upstream
    """Converts markdown report to a styled HTML string for download."""
=======
    """Converts markdown report to a styled, brand-matched HTML string for download."""
>>>>>>> Stashed changes
    report_html = markdown.markdown(report)
    feedback_html = markdown.markdown(feedback)
    return f"""
    <html>
    <head>
<<<<<<< Updated upstream
        <style>
            body {{ font-family: 'Inter', sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 40px auto; padding: 20px; }}
            h1, h2, h3 {{ color: #FF6B35; }}
            .feedback {{ background: #fff8f5; border-left: 4px solid #FF6B35; padding: 15px; margin-top: 40px; border-radius: 4px; }}
=======
        <meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Inter', sans-serif;
                line-height: 1.7;
                color: #1E2333;
                max-width: 800px;
                margin: 40px auto;
                padding: 24px;
                background: #F5F7FC;
            }}
            h1 {{
                font-family: 'Space Grotesk', sans-serif;
                background: linear-gradient(120deg, #4F46E5, #7C3AED);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            h2, h3 {{ font-family: 'Space Grotesk', sans-serif; color: #4F46E5; }}
            code {{ background: rgba(79,70,229,0.08); color: #4F46E5; padding: 2px 6px; border-radius: 4px; }}
            .feedback {{
                background: #F1F0FF;
                border-left: 4px solid #7C3AED;
                padding: 18px 20px;
                margin-top: 40px;
                border-radius: 10px;
            }}
>>>>>>> Stashed changes
        </style>
    </head>
    <body>
        <h1>Research Report: {topic}</h1>
        {report_html}
        <div class="feedback">
            <h3>🤖 AI Critic Feedback</h3>
            {feedback_html}
        </div>
    </body>
    </html>
    """

# ==========================================
# 4. SIDEBAR SETTINGS
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("Configure your research parameters below.")
<<<<<<< Updated upstream
    
=======

>>>>>>> Stashed changes
    detail_level = st.select_slider(
        "Report Detail",
        options=["Concise", "Balanced", "Deep Dive"],
        value="Balanced"
    )
<<<<<<< Updated upstream
    
    show_intermediate = st.toggle("Show Intermediate Outputs", value=True)
    
    st.markdown("---")
    st.markdown("### 📖 About")
    st.info("This multi-agent system uses LangChain/LangGraph to search, read, write, and critique research reports.")
    
=======

    show_intermediate = st.toggle("Show Intermediate Outputs", value=True)

    st.markdown("---")
    st.markdown("### 📖 About")
    st.info("This multi-agent system uses LangChain/LangGraph to search, read, write, and critique research reports.")

>>>>>>> Stashed changes
    if st.button("Clear Session", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ==========================================
# 5. MAIN APPLICATION LAYOUT
# ==========================================
<<<<<<< Updated upstream
st.markdown("<h1 style='text-align: center;'>🔬 Multi-Agent Research System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; margin-top: -10px;'>Enter a topic and let the AI agents collaborate to build your report.</p>", unsafe_allow_html=True)
=======
st.markdown("<div class='hero-title'>🔬 Multi-Agent Research System</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Enter a topic and let the AI agents collaborate to build your report.</div>", unsafe_allow_html=True)
>>>>>>> Stashed changes

# Input Area
col1, col2, col3 = st.columns([6, 1, 1])
with col1:
    topic = st.text_input("Research Topic", placeholder="e.g., The impact of AI on software development in 2024", label_visibility="collapsed")
with col2:
<<<<<<< Updated upstream
    if st.button("Run", use_container_width=True, disabled=st.session_state.pipeline_running or not topic):
=======
    if st.button("Run", type="primary", use_container_width=True, disabled=st.session_state.pipeline_running or not topic):
>>>>>>> Stashed changes
        st.session_state.pipeline_running = True
        st.session_state.current_step = 1
        st.session_state.research_data = {}
        st.session_state.error = None
<<<<<<< Updated upstream
        st.session_state.pipeline_gen = run_reseacrh_pipeline(topic)
=======
        st.session_state.topic = topic
        st.session_state.pipeline_gen = run_research_pipeline(topic)
>>>>>>> Stashed changes
        st.rerun()
with col3:
    if st.button("Reset", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ==========================================
# 6. PIPELINE EXECUTION LOGIC
# ==========================================
if st.session_state.pipeline_gen is not None:
    try:
        with st.spinner(f"Agent {st.session_state.current_step} is working..."):
            step_name, result = next(st.session_state.pipeline_gen)
<<<<<<< Updated upstream
            
            # Store the yielded data
            if step_name == 1:
                st.session_state.research_data['search_result'] = result.get('search_result', '')
            elif step_name == 2:
                st.session_state.research_data['scraped_result'] = result.get('scraped_result', '')
            elif step_name == 3:
                st.session_state.research_data['report'] = result.get('report', '')
            elif step_name == 4:
                st.session_state.research_data['feedback'] = result.get('feedback', '')
            
            st.session_state.current_step = step_name + 1
            st.rerun()
            
    except StopIteration:
        st.session_state.current_step = 5 # Mark as complete
        st.session_state.pipeline_gen = None
        st.session_state.pipeline_running = False
        st.rerun()
    except Exception as e:
        st.session_state.error = str(e)
        st.session_state.pipeline_gen = None
        st.session_state.pipeline_running = False
        st.rerun()

=======

            # Handle early error (e.g. empty topic)
            if step_name == 0:
                st.session_state.error = result.get('error', 'Unknown error.')
                st.session_state.pipeline_gen = None
                st.session_state.pipeline_running = False
                st.rerun()

            # Store the yielded data
            elif step_name == 1:
                st.session_state.research_data['search_result'] = result.get('search_result', '')
            elif step_name == 2:
                st.session_state.research_data['scraped_result'] = result.get('scraped_result', '')
            elif step_name == 3:
                st.session_state.research_data['report'] = result.get('report', '')
            elif step_name == 4:
                st.session_state.research_data['feedback'] = result.get('feedback', '')

            st.session_state.current_step = step_name + 1
            st.rerun()

    except StopIteration:
        st.session_state.current_step = 5  # Mark as complete
        st.session_state.pipeline_gen = None
        st.session_state.pipeline_running = False
        st.rerun()
    except Exception as e:
        st.session_state.error = str(e)
        st.session_state.pipeline_gen = None
        st.session_state.pipeline_running = False
        st.rerun()

>>>>>>> Stashed changes
# ==========================================
# 7. RENDERING RESULTS & PROGRESS
# ==========================================
if st.session_state.pipeline_running or st.session_state.current_step > 0:
    render_stepper(st.session_state.current_step)

# Error Handling
if st.session_state.error:
    st.error(f"**Pipeline Error Encountered:**\n\n``{st.session_state.error}``")
    st.warning("Please check your API keys, agent configurations, or try a different topic.")

# Display Outputs
data = st.session_state.research_data

if data:
    # Main Report Viewer
    if 'report' in data:
        st.markdown("### 📄 Final Research Report")
<<<<<<< Updated upstream
        
=======

>>>>>>> Stashed changes
        # Download Buttons
        dcol1, dcol2 = st.columns(2)
        with dcol1:
            st.download_button(
                label="⬇️ Download Markdown",
                data=data['report'].encode('utf-8'),
                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
<<<<<<< Updated upstream
                mime="text/markdown"
=======
                mime="text/markdown",
                use_container_width=True
            )
        with dcol2:
            html_content = create_html_download(st.session_state.get('topic', 'Research'), data['report'], data.get('feedback', ''))
            st.download_button(
                label="⬇️ Download HTML (Print to PDF)",
                data=html_content.encode('utf-8'),
                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
>>>>>>> Stashed changes
            )
        with dcol2:
            html_content = create_html_download(st.session_state.get('topic', 'Research'), data['report'], data.get('feedback', ''))
            st.download_button(
                label="⬇️ Download HTML (Print to PDF)",
                data=html_content.encode('utf-8'),
                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html"
            )
            
        st.markdown("---")
        
        # Styled Markdown Container
        with st.container():
            st.markdown('<div class="custom-card report-content">', unsafe_allow_html=True)
            st.markdown(data['report'])
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Critic Feedback
    if 'feedback' in data:
        st.markdown("### 🤖 AI Critic Feedback")
        with st.container():
            st.markdown('<div class="custom-card" style="border-left: 4px solid #FF6B35;">', unsafe_allow_html=True)
            st.markdown(data['feedback'])
            st.markdown('</div>', unsafe_allow_html=True)

<<<<<<< Updated upstream
=======
        st.markdown("---")

        # Styled Glass Markdown Container
        with st.container():
            st.markdown('<div class="custom-card report-content">', unsafe_allow_html=True)
            st.markdown(data['report'])
            st.markdown('</div>', unsafe_allow_html=True)

    # Critic Feedback
    if 'feedback' in data:
        st.markdown("### 🤖 AI Critic Feedback")
        with st.container():
            st.markdown('<div class="custom-card" style="border-left: 4px solid var(--accent-2);">', unsafe_allow_html=True)
            st.markdown(data['feedback'])
            st.markdown('</div>', unsafe_allow_html=True)

>>>>>>> Stashed changes
    # Expandable Intermediate Outputs
    if show_intermediate and ('search_result' in data or 'scraped_result' in data):
        st.markdown("### 🔍 Intermediate Agent Outputs")
        with st.expander("View Search & Scraping Results", expanded=False):
            if 'search_result' in data:
                st.markdown("#### Step 1: Search Agent Results")
                st.text_area("Search Output", data['search_result'], height=200, key="search_output")
<<<<<<< Updated upstream
            
            if 'scraped_result' in data:
                st.markdown("#### Step 2: Reader Agent Scraped Content")
                st.text_area("Scraped Output", data['scraped_result'], height=200, key="scraped_output")
=======

            if 'scraped_result' in data:
                st.markdown("#### Step 2: Reader Agent Scraped Content")
                st.text_area("Scraped Output", data['scraped_result'], height=200, key="scraped_output")
>>>>>>> Stashed changes
