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

    /* ═══════════════════════════════════════════
       MÓVIL  (≤ 768px)
    ═══════════════════════════════════════════ */
    @media (max-width: 768px) {

        /* ── Contenido principal más compacto ── */
        .block-container {
            padding: 1rem 0.75rem 2rem !important;
        }

        /* ── Títulos más pequeños ── */
        h1 { font-size: 1.6rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }

        /* ── Tabs: scroll horizontal en lugar de wrap ── */
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
            -webkit-overflow-scrolling: touch;
            border-radius: 12px !important;
            padding: 5px 6px !important;
            gap: 3px !important;
            scrollbar-width: none;
        }
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
        .stTabs [data-baseweb="tab"] {
            padding: 7px 11px !important;
            font-size: 11px !important;
            white-space: nowrap !important;
            flex-shrink: 0 !important;
        }

        /* ── Métricas: valor más pequeño ── */
        [data-testid="stMetric"] {
            padding: 12px 14px !important;
            border-radius: 12px !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 20px !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 10px !important;
        }

        /* ── Botones: ancho completo y más fáciles de tocar ── */
        .stButton > button {
            width: 100% !important;
            padding: 14px 20px !important;
            font-size: 15px !important;
            border-radius: 12px !important;
        }
        [data-testid="stFormSubmitButton"] > button {
            width: 100% !important;
            padding: 14px 20px !important;
            font-size: 15px !important;
        }

        /* ── Inputs más grandes para el dedo ── */
        input[type="text"],
        input[type="password"],
        input[type="number"],
        textarea {
            font-size: 16px !important;   /* evita zoom automático en iOS */
            padding: 10px 12px !important;
            min-height: 44px !important;
        }
        div[data-baseweb="select"] > div {
            min-height: 44px !important;
            font-size: 15px !important;
        }

        /* ── Login card ocupa todo el ancho ── */
        .login-card {
            padding: 36px 24px !important;
            border-radius: 18px !important;
            margin-top: 16px !important;
        }
        .login-card h2 { font-size: 28px !important; }

        /* ── Expanders con padding reducido ── */
        [data-testid="stExpander"] summary {
            padding: 12px 14px !important;
            font-size: 14px !important;
        }

        /* ── Dataframes scroll horizontal ── */
        .stDataFrame {
            overflow-x: auto !important;
        }

        /* ── Sidebar: oculta por defecto, se abre con el botón ─ */
        /* Streamlit ya lo hace solo en móvil, esto refina el tamaño */
        [data-testid="stSidebar"] {
            min-width: 260px !important;
            max-width: 85vw !important;
        }

        /* ── Número de columnas: forzar apilado ── */
        [data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }

        /* ── Slider más fácil de arrastrar ── */
        [data-testid="stSlider"] [role="slider"] {
            width: 22px !important;
            height: 22px !important;
        }

        /* ── Checkbox más grande ── */
        [data-testid="stCheckbox"] label {
            font-size: 15px !important;
            gap: 10px !important;
        }
        [data-testid="stCheckbox"] input {
            width: 20px !important;
            height: 20px !important;
        }
    }

    /* ═══════════════════════════════════════════
       MÓVIL PEQUEÑO  (≤ 400px)
    ═══════════════════════════════════════════ */
    @media (max-width: 400px) {
        .block-container { padding: 0.75rem 0.5rem 2rem !important; }
        h1 { font-size: 1.4rem !important; }
        .stTabs [data-baseweb="tab"] {
            padding: 6px 9px !important;
            font-size: 10px !important;
        }
        [data-testid="stMetricValue"] { font-size: 18px !important; }
    }

    </style>
    """, unsafe_allow_html=True)
