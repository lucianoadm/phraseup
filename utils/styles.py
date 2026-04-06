import streamlit as st

def load_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0 4px;
}
.logo-mark {
    width: 36px;
    height: 36px;
    background: #1a1a2e;
    color: #e8d5b7;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 14px;
    flex-shrink: 0;
}
.logo-title {
    font-size: 16px;
    font-weight: 600;
    color: #1a1a2e;
}
.logo-sub {
    font-size: 11px;
    color: #888;
}
.sidebar-footer {
    font-size: 12px;
    color: #aaa;
    line-height: 1.6;
}

/* Page header */
.page-header {
    margin-bottom: 1.5rem;
}
.page-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 28px;
    color: #1a1a2e;
    margin: 0;
}
.page-header p {
    font-size: 14px;
    color: #888;
    margin: 4px 0 0;
}

/* Chat bubbles */
.bubble-user {
    background: #1a1a2e;
    color: #f0e6d3;
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
    font-size: 15px;
    display: inline-block;
    max-width: 85%;
    line-height: 1.6;
    margin: 4px 0;
}
.bubble-wrap-user {
    text-align: right;
    margin: 8px 0;
}
.bubble-wrap-user small {
    font-size: 11px;
    color: #aaa;
    display: block;
    text-align: right;
    margin-bottom: 4px;
}

/* Response cards */
.response-card {
    background: white;
    border: 1px solid #eee;
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
}
.response-card-header {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 8px;
    padding: 3px 8px;
    border-radius: 4px;
    display: inline-block;
}
.tag-prof { background: #eeedfe; color: #3C3489; }
.tag-pos  { background: #e1f5ee; color: #085041; }

.response-phrase {
    font-size: 16px;
    color: #1a1a2e;
    font-weight: 500;
    line-height: 1.5;
    margin: 6px 0;
}
.response-why {
    font-size: 13px;
    color: #888;
    font-style: italic;
}

/* Library card */
.lib-card {
    background: white;
    border: 1px solid #eee;
    border-radius: 10px;
    padding: 14px 16px;
    margin: 8px 0;
}
.lib-original {
    font-size: 13px;
    color: #aaa;
    margin-bottom: 4px;
}
.lib-phrase {
    font-size: 15px;
    color: #1a1a2e;
    font-weight: 500;
    line-height: 1.5;
}
.lib-meta {
    font-size: 11px;
    color: #bbb;
    margin-top: 6px;
}

/* Stats */
.stat-card {
    background: white;
    border: 1px solid #eee;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.stat-number {
    font-size: 32px;
    font-weight: 600;
    color: #1a1a2e;
    font-family: 'DM Serif Display', serif;
}
.stat-label {
    font-size: 12px;
    color: #888;
    margin-top: 4px;
}

/* Training */
.training-phrase {
    background: #f8f7ff;
    border-left: 3px solid #7F77DD;
    border-radius: 0 8px 8px 0;
    padding: 14px 16px;
    font-size: 16px;
    color: #1a1a2e;
    font-weight: 500;
    line-height: 1.6;
    margin: 12px 0;
}

/* Score badge */
.score-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}
.score-high { background: #e1f5ee; color: #085041; }
.score-mid  { background: #faeeda; color: #633806; }
.score-low  { background: #fcebeb; color: #791F1F; }

/* Divider */
.section-divider {
    height: 1px;
    background: #f0f0f0;
    margin: 16px 0;
}

/* Chips / example pills */
.chip-row { display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0 16px; }

/* Hide Streamlit default elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)
