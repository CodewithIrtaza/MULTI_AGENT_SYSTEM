"""
Research Agent Studio — Premium Streamlit Interface (v2)
=========================================================
Sidebar-free, animation-rich UI for the multi-agent research pipeline.

Run:
    streamlit run app.py
"""

from __future__ import annotations

import io
import time
import contextlib
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Callable

import streamlit as st

# ---------------------------------------------------------------------------
# Backend import
# ---------------------------------------------------------------------------
_import_error: Optional[Exception] = None
run_reseacrh_pipeline: Optional[Callable] = None

try:
    from pipeline import run_reseacrh_pipeline  # noqa: F401
except ImportError as e1:
    try:
        from pipeline import run_reseacrh_pipeline  # noqa: F401
    except ImportError as e2:
        _import_error = e2 or e1


# ===========================================================================
# PAGE CONFIG — no sidebar
# ===========================================================================
st.set_page_config(
    page_title="Research Agent Studio",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_VERSION = "v2.0.0"
ACTIVE_MODEL = "llama-3.3-70b + 8b"


# ===========================================================================
# DESIGN SYSTEM — CSS (complete rewrite, no sidebar styles)
# ===========================================================================
def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        :root{
            --bg:#0B0F19;
            --bg-secondary:#111827;
            --surface:#1F2937;
            --surface-hover:#283548;
            --surface-alt:#1a2332;
            --accent:#6366F1;
            --accent-light:#818CF8;
            --accent-glow:rgba(99,102,241,0.25);
            --accent-soft:rgba(99,102,241,0.12);
            --accent-soft-strong:rgba(99,102,241,0.22);
            --orange:#F97316;
            --orange-glow:rgba(249,115,22,0.25);
            --teal:#14B8A6;
            --teal-glow:rgba(20,184,166,0.25);
            --pink:#EC4899;
            --text:#F9FAFB;
            --text-secondary:#9CA3AF;
            --text-soft:#6B7280;
            --border:rgba(255,255,255,0.08);
            --border-light:rgba(255,255,255,0.12);
            --success:#22C55E;
            --warning:#F59E0B;
            --error:#EF4444;
            --radius-xl:24px;
            --radius-lg:18px;
            --radius-md:14px;
            --radius-sm:10px;
            --shadow-glow:0 0 40px rgba(99,102,241,0.15), 0 0 80px rgba(99,102,241,0.05);
            --shadow-card:0 4px 24px rgba(0,0,0,0.3), 0 1px 4px rgba(0,0,0,0.2);
            --shadow-card-hover:0 8px 40px rgba(0,0,0,0.4), 0 0 30px rgba(99,102,241,0.1);
        }

        html, body, [class*="css"]{
            font-family:'Plus Jakarta Sans', -apple-system, sans-serif;
            color:var(--text);
        }

        /* ---- Hide Streamlit chrome + sidebar ---- */
        #MainMenu, footer, header {visibility:hidden;}
        section[data-testid="stSidebar"]{ display:none !important; }
        button[kind="header"]{ display:none !important; }

        .stApp{
            background:
                radial-gradient(ellipse at 15% 5%, rgba(99,102,241,0.12) 0%, transparent 50%),
                radial-gradient(ellipse at 85% 90%, rgba(249,115,22,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(20,184,166,0.04) 0%, transparent 60%),
                var(--bg);
        }
        .block-container{
            padding-top:1.8rem;
            padding-bottom:4rem;
            max-width:960px;
        }

        ::-webkit-scrollbar{ width:8px; height:8px; }
        ::-webkit-scrollbar-track{ background:transparent; }
        ::-webkit-scrollbar-thumb{ background:rgba(255,255,255,0.1); border-radius:10px; }
        ::-webkit-scrollbar-thumb:hover{ background:var(--accent); }

        /* ---- Typography ---- */
        h1,h2,h3,.serif{
            font-family:'Fraunces', serif;
            letter-spacing:-0.02em;
            color:var(--text);
        }
        .mono{ font-family:'JetBrains Mono', monospace; }

        /* ---- Hero Header ---- */
        .hero-header{
            text-align:center;
            padding:2rem 0 2.5rem 0;
            position:relative;
        }
        .hero-header .logo-ring{
            width:72px; height:72px; border-radius:20px;
            background:linear-gradient(135deg, var(--accent), var(--orange));
            display:inline-flex; align-items:center; justify-content:center;
            font-size:2rem;
            box-shadow:0 8px 32px rgba(99,102,241,0.3), 0 0 60px rgba(99,102,241,0.1);
            margin-bottom:1rem;
            animation:float-logo 4s ease-in-out infinite;
        }
        @keyframes float-logo{
            0%,100%{transform:translateY(0px);}
            50%{transform:translateY(-6px);}
        }
        .hero-header h1{
            font-size:2.2rem; font-weight:700; margin:0;
            background:linear-gradient(135deg, var(--text) 0%, var(--accent-light) 100%);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            background-clip:text;
        }
        .hero-header .tagline{
            color:var(--text-secondary); font-size:0.95rem; margin-top:0.4rem;
        }
        .hero-pills{
            display:flex; gap:0.6rem; justify-content:center; margin-top:1rem; flex-wrap:wrap;
        }
        .pill{
            display:inline-flex; align-items:center; gap:0.45rem;
            padding:0.4rem 0.9rem; border-radius:999px;
            font-size:0.76rem; font-weight:600;
            border:1px solid var(--border-light);
            background:var(--surface);
            color:var(--text-secondary);
            backdrop-filter:blur(8px);
        }
        .pill-dot{ width:7px; height:7px; border-radius:50%; background:var(--success); }
        .pill-dot.off{ background:var(--error); }

        /* ---- Search Card ---- */
        .search-card{
            background:var(--surface);
            border:1px solid var(--border-light);
            border-radius:var(--radius-xl);
            padding:1.8rem 2rem;
            box-shadow:var(--shadow-card);
            margin-bottom:2rem;
            position:relative;
            overflow:hidden;
        }
        .search-card::before{
            content:'';
            position:absolute; top:0; left:0; right:0; height:3px;
            background:linear-gradient(90deg, var(--accent), var(--orange), var(--teal));
        }
        .search-card .label{
            font-size:0.72rem; font-weight:700; letter-spacing:0.1em;
            text-transform:uppercase; color:var(--accent-light); margin-bottom:0.8rem;
        }

        /* ---- Inputs ---- */
        .stTextInput input, .stTextArea textarea{
            border-radius:var(--radius-md) !important;
            border:1.5px solid var(--border-light) !important;
            padding:0.85rem 1.1rem !important;
            font-size:1rem !important;
            background:var(--bg-secondary) !important;
            color:var(--text) !important;
            transition:border-color .2s ease, box-shadow .2s ease;
        }
        .stTextInput input:focus, .stTextArea textarea:focus{
            border-color:var(--accent) !important;
            box-shadow:0 0 0 4px var(--accent-soft) !important;
        }
        .stTextInput input::placeholder{ color:var(--text-soft) !important; }

        /* ---- Buttons ---- */
        .stButton>button, .stFormSubmitButton>button{
            background:linear-gradient(135deg, var(--accent), #7C3AED) !important;
            color:white !important; border:none !important; border-radius:var(--radius-sm) !important;
            padding:0.7rem 1.4rem !important; font-weight:700 !important; font-size:0.94rem !important;
            box-shadow:0 6px 20px rgba(99,102,241,0.35) !important;
            transition:transform .15s ease, box-shadow .15s ease, filter .15s ease !important;
        }
        .stButton>button:hover, .stFormSubmitButton>button:hover{
            transform:translateY(-2px) !important;
            box-shadow:0 10px 28px rgba(99,102,241,0.45) !important;
            filter:brightness(1.06) !important;
        }
        .stButton>button:active{ transform:translateY(0px) scale(0.98) !important; }
        .stButton>button:disabled{
            background:var(--surface) !important; color:var(--text-soft) !important;
            box-shadow:none !important; transform:none !important;
        }
        button[kind="secondary"]{
            background:var(--surface) !important; color:var(--text) !important;
            border:1px solid var(--border-light) !important; box-shadow:none !important;
        }

        /* ============================================================ */
        /* LOADING ANIMATION                                             */
        /* ============================================================ */
        .loading-overlay{
            position:relative;
            padding:3rem 1.5rem;
            text-align:center;
        }

        /* Orbiting dots ring */
        .orbit-container{
            width:160px; height:160px; margin:0 auto 2rem auto; position:relative;
        }
        .orbit-ring{
            width:160px; height:160px; border-radius:50%;
            border:2px dashed rgba(99,102,241,0.2);
            animation:spin 12s linear infinite;
            position:absolute; top:0; left:0;
        }
        .orbit-ring-2{
            width:120px; height:120px; border-radius:50%;
            border:2px dashed rgba(249,115,22,0.15);
            animation:spin-reverse 8s linear infinite;
            position:absolute; top:20px; left:20px;
        }
        @keyframes spin{ from{transform:rotate(0deg);} to{transform:rotate(360deg);} }
        @keyframes spin-reverse{ from{transform:rotate(360deg);} to{transform:rotate(0deg);} }

        .orbit-dot{
            position:absolute; width:14px; height:14px; border-radius:50%;
            animation:orbit-pulse 2s ease-in-out infinite;
        }
        .orbit-dot-1{ background:var(--accent); top:-7px; left:50%; margin-left:-7px;
            box-shadow:0 0 20px var(--accent-glow); animation-delay:0s; }
        .orbit-dot-2{ background:var(--orange); bottom:-7px; left:50%; margin-left:-7px;
            box-shadow:0 0 20px var(--orange-glow); animation-delay:0.5s; }
        .orbit-dot-3{ background:var(--teal); top:50%; margin-top:-7px; right:-7px;
            box-shadow:0 0 20px var(--teal-glow); animation-delay:1s; }
        .orbit-dot-4{ background:var(--pink); top:50%; margin-top:-7px; left:-7px;
            box-shadow:0 0 18px rgba(236,72,153,0.3); animation-delay:1.5s; }

        @keyframes orbit-pulse{
            0%,100%{transform:scale(1);opacity:1;}
            50%{transform:scale(1.5);opacity:0.5;}
        }

        .orbit-center{
            position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
            width:60px; height:60px; border-radius:16px;
            background:linear-gradient(135deg, var(--accent), var(--orange));
            display:flex; align-items:center; justify-content:center;
            font-size:1.6rem;
            box-shadow:0 0 40px var(--accent-glow);
            animation:center-pulse 2.5s ease-in-out infinite;
        }
        @keyframes center-pulse{
            0%,100%{box-shadow:0 0 40px var(--accent-glow);}
            50%{box-shadow:0 0 60px var(--accent-glow), 0 0 80px rgba(249,115,22,0.15);}
        }

        .loading-title{
            font-family:'Fraunces',serif;
            font-size:1.6rem; font-weight:700;
            background:linear-gradient(135deg, var(--text) 0%, var(--accent-light) 100%);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            background-clip:text;
            margin-bottom:0.3rem;
        }
        .loading-subtitle{
            color:var(--text-secondary); font-size:0.92rem; margin-bottom:2rem;
        }




        /* ============================================================ */
        /* RESULTS                                                       */
        /* ============================================================ */

        /* Metrics row */
        .metrics-row{
            display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:2rem;
        }
        .metric-card{
            background:var(--surface);
            border:1px solid var(--border);
            border-radius:var(--radius-lg);
            padding:1.2rem 1.3rem;
            box-shadow:var(--shadow-card);
            transition:all .25s ease;
        }
        .metric-card:hover{
            border-color:var(--accent);
            box-shadow:var(--shadow-card-hover);
            transform:translateY(-2px);
        }
        .metric-label{ font-size:0.76rem; font-weight:600; color:var(--text-secondary); margin-bottom:0.3rem; }
        .metric-value{ font-family:'Fraunces',serif; font-size:1.5rem; font-weight:700; color:var(--text); }
        .metric-icon{ font-size:1.2rem; float:right; opacity:0.6; }

        /* Result section heading */
        .result-heading{
            font-family:'Fraunces',serif; font-size:1.4rem; font-weight:700;
            color:var(--text); margin-bottom:0.3rem;
        }
        .result-topic{
            color:var(--accent-light); font-size:0.9rem; margin-bottom:1.5rem;
        }

        /* Tabs override */
        .stTabs [data-baseweb="tab-list"]{
            gap:0.35rem; border-bottom:1px solid var(--border);
        }
        .stTabs [data-baseweb="tab"]{
            height:auto; padding:0.65rem 1.2rem; border-radius:10px 10px 0 0;
            font-weight:600; color:var(--text-secondary); background:transparent;
        }
        .stTabs [aria-selected="true"]{
            color:var(--accent-light) !important;
            background:var(--accent-soft) !important;
            border-bottom:2px solid var(--accent) !important;
        }

        /* Report surface */
        .report-surface{
            background:var(--surface);
            border:1px solid var(--border-light);
            border-radius:var(--radius-xl);
            padding:2.2rem 2.5rem;
            box-shadow:var(--shadow-card);
            line-height:1.8; color:var(--text);
            position:relative; overflow:hidden;
        }
        .report-surface::before{
            content:'';
            position:absolute; top:0; left:0; right:0; height:3px;
            background:linear-gradient(90deg, var(--accent), var(--teal), var(--orange));
        }
        .report-surface h1, .report-surface h2, .report-surface h3{
            font-family:'Fraunces',serif; color:var(--text);
        }
        .report-surface p{ color:var(--text-secondary); }
        .report-surface strong{ color:var(--text); }
        .report-surface a{ color:var(--accent-light); }
        .report-surface ul, .report-surface ol{ color:var(--text-secondary); }

        /* Content card (feedback, search, etc.) */
        .content-card{
            background:var(--surface);
            border:1px solid var(--border);
            border-radius:var(--radius-lg);
            padding:1.8rem 2rem;
            box-shadow:var(--shadow-card);
            line-height:1.7;
            color:var(--text-secondary);
        }
        .content-card h1,.content-card h2,.content-card h3{ color:var(--text); }
        .content-card strong{ color:var(--text); }

        /* Expander */
        div[data-testid="stExpander"]{
            border:1px solid var(--border) !important;
            border-radius:var(--radius-md) !important;
            background:var(--surface) !important;
            overflow:hidden;
        }
        div[data-testid="stExpander"] summary{ font-weight:600; color:var(--text); }

        /* Download button */
        .stDownloadButton > button {
            background:linear-gradient(135deg, var(--teal), #0D9488) !important;
            box-shadow:0 6px 20px rgba(20,184,166,0.3) !important;
        }
        .stDownloadButton > button:hover{
            box-shadow:0 10px 28px rgba(20,184,166,0.4) !important;
        }

        /* Empty state */
        .empty-state{
            text-align:center; padding:4rem 2rem;
            border:1.5px dashed var(--border-light); border-radius:var(--radius-xl);
            background:var(--surface);
        }
        .empty-state .emoji{ font-size:3rem; margin-bottom:0.8rem; }
        .empty-state .title{ font-weight:700; font-size:1.15rem; color:var(--text); }
        .empty-state .desc{ color:var(--text-secondary); font-size:0.92rem; margin-top:0.4rem; }

        /* History chips in main area */
        .history-section{ margin-top:2rem; }
        .history-chips{
            display:flex; flex-wrap:wrap; gap:0.5rem; margin-top:0.6rem;
        }
        .history-chip{
            display:inline-flex; align-items:center; gap:0.4rem;
            padding:0.45rem 0.9rem; border-radius:999px;
            font-size:0.8rem; font-weight:600;
            border:1px solid var(--border-light);
            background:var(--surface);
            color:var(--text-secondary);
            cursor:pointer; transition:all .2s ease;
        }
        .history-chip:hover{
            border-color:var(--accent);
            background:var(--accent-soft);
            color:var(--accent-light);
        }

        /* Misc overrides */
        hr{ border-color:var(--border) !important; }
        div[data-testid="stToggle"] label{ font-size:0.85rem; color:var(--text-secondary); }
        .section-label{
            font-size:0.72rem; font-weight:700; letter-spacing:0.1em;
            text-transform:uppercase; color:var(--accent-light); margin-bottom:0.5rem;
        }

        /* Progress bar */
        div[data-testid="stProgress"] > div > div{
            background:linear-gradient(90deg, var(--accent), var(--orange)) !important;
        }

        /* Metrics streamlit override */
        div[data-testid="stMetric"]{
            background:var(--surface); border:1px solid var(--border);
            border-radius:var(--radius-md); padding:1rem 1.1rem;
            box-shadow:var(--shadow-card);
        }
        div[data-testid="stMetricLabel"]{ color:var(--text-secondary); font-weight:600; }
        div[data-testid="stMetricValue"]{ color:var(--text); font-family:'Fraunces',serif; }

        /* Toast */
        div[data-testid="stToast"]{ border-radius:var(--radius-md); }

        /* responsive */
        @media (max-width:768px){
            .metrics-row{ grid-template-columns:repeat(2,1fr); }
            .hero-header h1{ font-size:1.6rem; }
            .report-surface{ padding:1.4rem 1.2rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ===========================================================================
# STATE
# ===========================================================================
@dataclass
class RunRecord:
    topic: str
    timestamp: str
    state: dict
    duration_s: float = 0.0


def init_state() -> None:
    defaults = {
        "history": [],
        "is_running": False,
        "current_state": None,
        "current_topic": None,
        "logs": "",
        "last_duration": 0.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


PIPELINE_STAGES = [
    {"key": "search_result", "name": "Search Agent", "icon": "🔍", "desc": "Scanning the web for reliable sources"},
    {"key": "scraped_result", "name": "Reader Agent", "icon": "📄", "desc": "Deep-reading the most relevant page"},
    {"key": "report", "name": "Writer Chain", "icon": "✍️", "desc": "Synthesizing a structured report"},
    {"key": "feedback", "name": "Critic Chain", "icon": "🧐", "desc": "Reviewing for accuracy & quality"},
]


# ===========================================================================
# COMPONENTS
# ===========================================================================
def render_header(backend_ok: bool) -> None:
    dot_class = "" if backend_ok else "off"
    dot_label = "Online" if backend_ok else "Offline"
    st.markdown(
        f"""
        <div class="hero-header">
            <div class="logo-ring">🧭</div>
            <h1>Research Agent Studio</h1>
            <p class="tagline">Multi-agent pipeline &mdash; Search → Read → Write → Critique</p>
            <div class="hero-pills">
                <span class="pill"><span class="pill-dot {dot_class}"></span>{dot_label}</span>
                <span class="pill">🧠 {ACTIVE_MODEL}</span>
                <span class="pill">⚡ {APP_VERSION}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_search_panel(disabled: bool):
    st.markdown(
        '<div class="search-card">'
        '<div class="label">🚀 Start a new research task</div>',
        unsafe_allow_html=True,
    )
    with st.form("research_form", clear_on_submit=False):
        topic = st.text_input(
            "Research topic",
            placeholder="🔎  e.g. Latest advances in retrieval-augmented generation (RAG)",
            label_visibility="collapsed",
        )
        c1, c2, c3 = st.columns([4, 1, 1.2])
        with c1:
            st.caption("Agents will search, read, write, and critique automatically.")
        with c2:
            clear = st.form_submit_button("Clear", use_container_width=True, type="secondary")
        with c3:
            submitted = st.form_submit_button(
                "▶  Run Research", use_container_width=True, disabled=disabled
            )
    st.markdown("</div>", unsafe_allow_html=True)
    return topic, submitted, clear


def render_loading_animation() -> str:
    """Return HTML for the beautiful loading animation."""
    return """
    <div class="loading-overlay">
        <div class="orbit-container">
            <div class="orbit-ring">
                <div class="orbit-dot orbit-dot-1"></div>
                <div class="orbit-dot orbit-dot-2"></div>
            </div>
            <div class="orbit-ring-2">
                <div class="orbit-dot orbit-dot-3"></div>
                <div class="orbit-dot orbit-dot-4"></div>
            </div>
            <div class="orbit-center">🧭</div>
        </div>
        <div class="loading-title">Agents are researching…</div>
        <div class="loading-subtitle">Sit back — the multi-agent pipeline is working on your topic</div>
    </div>
    """


def render_results_metrics() -> None:
    """Render the metrics row using custom HTML for consistent dark-theme styling."""
    n_runs = len(st.session_state.history)
    report_len = len(str(st.session_state.current_state.get("report", "")))
    st.markdown(
        f"""
        <div class="metrics-row">
            <div class="metric-card">
                <span class="metric-icon">⏱️</span>
                <div class="metric-label">Last Run Time</div>
                <div class="metric-value">{st.session_state.last_duration:.1f}s</div>
            </div>
            <div class="metric-card">
                <span class="metric-icon">📚</span>
                <div class="metric-label">Total Queries</div>
                <div class="metric-value">{n_runs}</div>
            </div>
            <div class="metric-card">
                <span class="metric-icon">🤖</span>
                <div class="metric-label">Pipeline</div>
                <div class="metric-value">4 Agents</div>
            </div>
            <div class="metric-card">
                <span class="metric-icon">📝</span>
                <div class="metric-label">Report Length</div>
                <div class="metric-value">{report_len:,}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state():
    st.markdown(
        """
        <div class="empty-state">
            <div class="emoji">🧭</div>
            <div class="title">No research yet</div>
            <div class="desc">Enter a topic above and run the pipeline to see results here.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_history_chips() -> None:
    """Render recent searches as inline chip buttons (replaces sidebar history)."""
    if not st.session_state.history:
        return
    st.markdown('<div class="section-label">🕐 Recent Searches</div>', unsafe_allow_html=True)
    cols = st.columns(min(len(st.session_state.history[-6:]), 6))
    for i, run in enumerate(reversed(st.session_state.history[-6:])):
        label = run.topic[:28] + ("…" if len(run.topic) > 28 else "")
        with cols[i % len(cols)]:
            if st.button(f"📄 {label}", key=f"hist_{i}", use_container_width=True):
                st.session_state.current_state = run.state
                st.session_state.current_topic = run.topic
                st.session_state.last_duration = run.duration_s
                st.rerun()


# ===========================================================================
# MAIN
# ===========================================================================
def main() -> None:
    init_state()
    inject_css()

    backend_ok = run_reseacrh_pipeline is not None
    render_header(backend_ok)

    if not backend_ok:
        st.error(
            f"Could not import `run_reseacrh_pipeline` from `pipeline.py`.\n\n"
            f"**Error:** `{_import_error}`\n\n"
            f"Make sure `pipeline.py`, `agents.py`, and `tools.py` are in the same folder, "
            f"and that `.env` contains the required API keys."
        )

    topic, submitted, clear = render_search_panel(disabled=st.session_state.is_running)

    if clear:
        st.session_state.current_state = None
        st.session_state.current_topic = None
        st.rerun()

    # -----------------------------------------------------------------
    # Execute pipeline with loading animation
    # -----------------------------------------------------------------
    if submitted:
        if not backend_ok:
            st.error("Pipeline unavailable — resolve the import error above first.")
        elif not topic or not topic.strip():
            st.warning("Please enter a research topic before running the pipeline.")
        else:
            st.session_state.is_running = True
            clean_topic = topic.strip()
            st.session_state.current_topic = clean_topic

            # Show loading animation with live elapsed timer
            loading_placeholder = st.empty()
            timer_placeholder = st.empty()

            captured_output = io.StringIO()
            error_occurred: Optional[Exception] = None
            final_state = None
            start_time = time.time()

            # Run pipeline in a background thread so UI can show live timer
            result_container = {"state": None, "error": None}

            def _run_pipeline():
                try:
                    with contextlib.redirect_stdout(captured_output):
                        result_container["state"] = run_reseacrh_pipeline(clean_topic)
                except Exception as e:
                    result_container["error"] = e

            thread = threading.Thread(target=_run_pipeline, daemon=True)
            thread.start()

            TIMEOUT_SECONDS = 180  # 3 minute hard timeout

            # Live timer loop — updates every 2s while pipeline runs
            while thread.is_alive():
                elapsed = time.time() - start_time
                if elapsed > TIMEOUT_SECONDS:
                    result_container["error"] = TimeoutError(
                        f"Pipeline exceeded {TIMEOUT_SECONDS}s timeout. "
                        f"Groq API may be rate-limiting you — try again in a minute."
                    )
                    break
                loading_placeholder.markdown(
                    render_loading_animation(), unsafe_allow_html=True
                )
                mins, secs = divmod(int(elapsed), 60)
                timer_placeholder.markdown(
                    f'<div style="text-align:center;color:#9CA3AF;font-size:0.85rem;">'
                    f'⏱️ Elapsed: {mins}m {secs:02d}s</div>',
                    unsafe_allow_html=True,
                )
                time.sleep(2)

            # Wait for thread to finish (if it hasn't timed out)
            thread.join(timeout=5)

            elapsed = time.time() - start_time
            final_state = result_container["state"]
            error_occurred = result_container["error"]

            st.session_state.is_running = False
            st.session_state.logs = captured_output.getvalue()
            st.session_state.last_duration = elapsed

            if error_occurred:
                loading_placeholder.empty()
                timer_placeholder.empty()
                st.error(f"Pipeline failed after {elapsed:.1f}s: `{error_occurred}`")
                if st.session_state.logs:
                    with st.expander("🪵 Raw execution logs", expanded=True):
                        st.code(st.session_state.logs, language="text")
            else:
                loading_placeholder.empty()
                timer_placeholder.empty()
                st.session_state.current_state = final_state
                st.session_state.history.append(
                    RunRecord(
                        topic=clean_topic,
                        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
                        state=final_state,
                        duration_s=elapsed,
                    )
                )
                st.toast("Research complete!", icon="✅")
                st.rerun()

    # -----------------------------------------------------------------
    # Results — well structured content
    # -----------------------------------------------------------------
    state = st.session_state.current_state
    if state:
        st.markdown(
            f'<div class="result-heading">📁 Research Results</div>'
            f'<div class="result-topic">Topic: {st.session_state.current_topic}</div>',
            unsafe_allow_html=True,
        )

        render_results_metrics()

        tab_report, tab_feedback, tab_search, tab_scraped, tab_logs = st.tabs(
            ["📝 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📄 Scraped Content", "🪵 Logs"]
        )

        with tab_report:
            st.markdown('<div class="report-surface">', unsafe_allow_html=True)
            st.markdown(str(state.get("report", "_No report generated._")))
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                "⬇ Download report (.md)",
                data=str(state.get("report", "")),
                file_name=f"report_{st.session_state.current_topic[:30].replace(' ', '_')}.md",
                mime="text/markdown",
            )

        with tab_feedback:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown(str(state.get("feedback", "_No feedback generated._")))
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_search:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown(str(state.get("search_result", "_No search results._")))
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_scraped:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown(str(state.get("scraped_result", "_No scraped content._")))
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_logs:
            if st.session_state.logs:
                st.code(st.session_state.logs, language="text")
            else:
                st.caption("No logs captured for this run.")

        st.markdown("<br>", unsafe_allow_html=True)
        render_history_chips()

        # Clear / New Search button
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 2])
        with c2:
            if st.button("🔄 New Search", use_container_width=True):
                st.session_state.current_state = None
                st.session_state.current_topic = None
                st.rerun()
    else:
        render_empty_state()
        if st.session_state.history:
            st.markdown("<br>", unsafe_allow_html=True)
            render_history_chips()


if __name__ == "__main__":
    main()