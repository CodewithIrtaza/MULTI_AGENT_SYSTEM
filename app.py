import streamlit as st
import markdown
from datetime import datetime
from pipeline import run_reseacrh_pipeline

# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="AI Research Agent", 
    page_icon="🔬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    st.markdown("""
    <style>
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
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

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
        .stepper-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 40px 0 30px 0;
            position: relative;
        }
        .step-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            z-index: 2;
            position: relative;
        }
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
        }
        .step-label {
            margin-top: 8px;
            font-size: 13px;
            color: #999;
            font-weight: 500;
        }
        .step-line {
            flex: 1;
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
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }
    </style>
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

# ==========================================
# 3. UI COMPONENTS & HELPER FUNCTIONS
# ==========================================
def render_stepper(current_step):
    """Renders a custom HTML/CSS horizontal stepper."""
    steps = [
        ("1", "Search"),
        ("2", "Reader"),
        ("3", "Writer"),
        ("4", "Critic")
    ]
    
    html = '<div class="stepper-container">'
    for i, (num, label) in enumerate(steps):
        step_num = i + 1
        status_class = ""
        if current_step == 5 or current_step > step_num:
            status_class = "completed"
        elif current_step == step_num:
            status_class = "active"
            
        html += f'''
        <div class="step-wrapper {status_class}">
            <div class="step-circle">{num if status_class != "completed" else "✓"}</div>
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
            
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def create_html_download(topic, report, feedback):
    """Converts markdown report to a styled HTML string for download."""
    report_html = markdown.markdown(report)
    feedback_html = markdown.markdown(feedback)
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Inter', sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 40px auto; padding: 20px; }}
            h1, h2, h3 {{ color: #FF6B35; }}
            .feedback {{ background: #fff8f5; border-left: 4px solid #FF6B35; padding: 15px; margin-top: 40px; border-radius: 4px; }}
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
    
    detail_level = st.select_slider(
        "Report Detail",
        options=["Concise", "Balanced", "Deep Dive"],
        value="Balanced"
    )
    
    show_intermediate = st.toggle("Show Intermediate Outputs", value=True)
    
    st.markdown("---")
    st.markdown("### 📖 About")
    st.info("This multi-agent system uses LangChain/LangGraph to search, read, write, and critique research reports.")
    
    if st.button("Clear Session", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ==========================================
# 5. MAIN APPLICATION LAYOUT
# ==========================================
st.markdown("<h1 style='text-align: center;'>🔬 Multi-Agent Research System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; margin-top: -10px;'>Enter a topic and let the AI agents collaborate to build your report.</p>", unsafe_allow_html=True)

# Input Area
col1, col2, col3 = st.columns([6, 1, 1])
with col1:
    topic = st.text_input("Research Topic", placeholder="e.g., The impact of AI on software development in 2024", label_visibility="collapsed")
with col2:
    if st.button("Run", use_container_width=True, disabled=st.session_state.pipeline_running or not topic):
        st.session_state.pipeline_running = True
        st.session_state.current_step = 1
        st.session_state.research_data = {}
        st.session_state.error = None
        st.session_state.pipeline_gen = run_reseacrh_pipeline(topic)
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
        
        # Download Buttons
        dcol1, dcol2 = st.columns(2)
        with dcol1:
            st.download_button(
                label="⬇️ Download Markdown",
                data=data['report'].encode('utf-8'),
                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
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

    # Expandable Intermediate Outputs
    if show_intermediate and ('search_result' in data or 'scraped_result' in data):
        st.markdown("### 🔍 Intermediate Agent Outputs")
        with st.expander("View Search & Scraping Results", expanded=False):
            if 'search_result' in data:
                st.markdown("#### Step 1: Search Agent Results")
                st.text_area("Search Output", data['search_result'], height=200, key="search_output")
            
            if 'scraped_result' in data:
                st.markdown("#### Step 2: Reader Agent Scraped Content")
                st.text_area("Scraped Output", data['scraped_result'], height=200, key="scraped_output")
