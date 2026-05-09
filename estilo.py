import streamlit as st


def aplicar_estilo():
    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;1,500&family=Inter:wght@300;400;500;600&display=swap');

    :root {
        --bg:            #F7F3F0;
        --card:          #FFFFFF;
        --primary:       #8C5E58;
        --primary-dark:  #6f4b46;
        --primary-light: #EDE0DC;
        --primary-faint: #F9F1EF;
        --text:          #2f2f2f;
        --muted:         #9c8c8c;
        --border:        #E9E2DD;
        --success:       #5a8a6a;
        --warning:       #b5833a;
        --danger:        #a04040;
    }

    /* ─── BASE ─── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text);
        background-color: var(--bg);
    }
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        letter-spacing: 0.2px;
        color: var(--text);
    }
    .stApp { background-color: var(--bg); }
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    /* ─── SIDEBAR ─── */
    [data-testid="stSidebar"] {
        background-color: #EFE7E2;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] h2 {
        font-family: 'Playfair Display', serif;
        color: var(--primary);
    }

    /* ─── TABS ─── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: var(--primary-light);
        padding: 6px 8px;
        border-radius: 16px;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 16px;
        font-weight: 500;
        font-size: 13px;
        color: var(--muted);
        background: transparent;
        border: none;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: var(--card) !important;
        color: var(--primary) !important;
        box-shadow: 0 2px 8px rgba(140,94,88,0.14);
    }
    .stTabs [data-baseweb="tab-border"],
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    /* ─── METRICS ─── */
    [data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px 22px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s, transform 0.2s;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 6px 20px rgba(140,94,88,0.12);
        transform: translateY(-1px);
    }
    [data-testid="stMetricValue"] {
        color: var(--primary);
        font-family: 'Playfair Display', serif;
        font-size: 26px !important;
        font-weight: 600;
    }
    [data-testid="stMetricLabel"] {
        color: var(--muted);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        font-weight: 500;
    }
    [data-testid="stMetricDelta"] { font-size: 13px; }

    /* ─── BUTTONS ─── */
    .stButton > button {
        background-color: var(--primary);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(140,94,88,0.22);
    }
    .stButton > button:hover {
        background-color: var(--primary-dark);
        box-shadow: 0 4px 14px rgba(140,94,88,0.32);
        transform: translateY(-1px);
    }
    .stButton > button:active { transform: translateY(0); }
    .stButton > button[kind="secondary"] {
        background-color: transparent;
        color: var(--primary);
        border: 1.5px solid var(--primary);
        box-shadow: none;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: var(--primary-faint);
        box-shadow: none;
    }
    .stButton > button:disabled {
        background-color: #d4c8c5 !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* ─── FORM SUBMIT ─── */
    [data-testid="stFormSubmitButton"] > button {
        background-color: var(--primary);
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(140,94,88,0.22);
        transition: all 0.2s;
    }
    [data-testid="stFormSubmitButton"] > button:hover {
        background-color: var(--primary-dark);
        box-shadow: 0 4px 14px rgba(140,94,88,0.32);
        transform: translateY(-1px);
    }

    /* ─── DOWNLOAD BUTTON ─── */
    [data-testid="stDownloadButton"] > button {
        background-color: transparent;
        color: var(--primary);
        border: 1.5px solid var(--border);
        border-radius: 10px;
        font-size: 13px;
        font-weight: 500;
        padding: 6px 14px;
        box-shadow: none;
        transition: all 0.2s;
    }
    [data-testid="stDownloadButton"] > button:hover {
        border-color: var(--primary);
        background-color: var(--primary-faint);
        box-shadow: none;
        transform: none;
    }

    /* ─── INPUTS ─── */
    input[type="text"],
    input[type="password"],
    input[type="number"],
    textarea {
        border-radius: 10px !important;
        border-color: var(--border) !important;
        background-color: var(--card) !important;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    input:focus, textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(140,94,88,0.1) !important;
    }
    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        background-color: var(--card) !important;
        border-color: var(--border) !important;
    }
    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(140,94,88,0.1) !important;
    }

    /* ─── SLIDER ─── */
    [data-testid="stSlider"] [role="slider"] {
        background-color: var(--primary) !important;
    }

    /* ─── EXPANDERS ─── */
    [data-testid="stExpander"] {
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        background: var(--card);
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        margin-bottom: 10px;
        overflow: hidden;
    }
    [data-testid="stExpander"] summary {
        font-weight: 500;
        color: var(--primary);
        padding: 14px 18px;
        transition: background 0.15s;
    }
    [data-testid="stExpander"] summary:hover {
        background: var(--primary-faint);
        color: var(--primary-dark);
    }

    /* ─── DATAFRAMES ─── */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border) !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .stDataFrame thead tr th {
        background-color: var(--primary-faint) !important;
        color: var(--primary) !important;
        font-weight: 600;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    /* ─── ALERTS ─── */
    [data-testid="stAlert"] { border-radius: 12px; }
    [data-testid="stAlert"][kind="error"]   { border-left: 4px solid var(--danger);  }
    [data-testid="stAlert"][kind="warning"] { border-left: 4px solid var(--warning); }
    [data-testid="stAlert"][kind="success"] { border-left: 4px solid var(--success); }
    [data-testid="stAlert"][kind="info"]    { border-left: 4px solid var(--primary); }

    /* ─── DIVIDER ─── */
    hr { border-color: var(--border); opacity: 0.5; }

    /* ─── DATE INPUT ─── */
    [data-testid="stDateInput"] input {
        border-radius: 10px !important;
    }

    /* ─── CHECKBOX ─── */
    [data-testid="stCheckbox"] label { font-size: 14px; }

    /* ─── LOGIN CARD ─── */
    .login-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 52px 44px;
        box-shadow: 0 16px 48px rgba(140,94,88,0.1);
        text-align: center;
        margin-top: 40px;
    }
    .login-card h2 {
        font-size: 38px;
        color: var(--primary);
        margin-bottom: 4px;
    }

    /* ─── SCROLLBAR ─── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--muted); }

    /* ─── ALTAIR CHART ─── */
    .vega-embed { border-radius: 12px; }

    </style>
    """, unsafe_allow_html=True)
