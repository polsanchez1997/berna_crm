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

    /* ═══════════════════════════════════════════════════════
       MÓVIL  (≤ 768px)  —  diseño tipo app nativa
    ═══════════════════════════════════════════════════════ */
    @media (max-width: 768px) {

        /* ── Layout base ── */
        .block-container {
            padding: 0.6rem 0.8rem 5rem !important;
            max-width: 100% !important;
        }

        /* ── FORZAR COLOR DE TEXTO (fix Android Chrome) ── */
        html, body, [class*="css"],
        p, span, div, label, li,
        .stMarkdown, .stMarkdown p,
        .stText, .stCaption,
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="caption"],
        .stTextInput label,
        .stNumberInput label,
        .stSelectbox label,
        .stDateInput label,
        .stSlider label,
        .stCheckbox label,
        .stRadio label,
        [data-baseweb="form-control-label"] {
            color: #2f2f2f !important;
        }
        /* Placeholders */
        input::placeholder, textarea::placeholder {
            color: #9c8c8c !important;
            opacity: 1 !important;
        }
        /* Texto dentro de inputs */
        input, textarea, select {
            color: #2f2f2f !important;
        }

        /* ── Tipografía ── */
        h1 {
            font-size: 1.55rem !important;
            margin-bottom: 0.4rem !important;
            color: #2f2f2f !important;
        }
        h2 { font-size: 1.2rem !important; color: #2f2f2f !important; }
        h3 { font-size: 1rem !important;  color: #2f2f2f !important; }
        p, label, .stMarkdown { font-size: 14px !important; }

        /* ── Tabs: barra deslizable tipo app ── */
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none !important;
            border-radius: 10px !important;
            padding: 3px 4px !important;
            gap: 2px !important;
            position: sticky !important;
            top: 3.2rem !important;
            z-index: 100 !important;
        }
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none !important; }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px !important;
            font-size: 12px !important;
            white-space: nowrap !important;
            flex-shrink: 0 !important;
            border-radius: 10px !important;
            min-height: 36px !important;
        }

        /* ── Métricas: grid 2 columnas ── */
        [data-testid="stMetric"] {
            padding: 14px 12px !important;
            border-radius: 14px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.3rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 9px !important;
            letter-spacing: 0.4px !important;
        }
        [data-testid="stMetricDelta"] { font-size: 11px !important; }

        /* ── Columnas: apilar verticalmente ── */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 0 !important;
        }

        /* ── Botones: grandes, táctiles, ancho completo ── */
        .stButton > button {
            width: 100% !important;
            min-height: 50px !important;
            padding: 13px 20px !important;
            font-size: 15px !important;
            border-radius: 14px !important;
            letter-spacing: 0.2px !important;
        }
        [data-testid="stFormSubmitButton"] > button {
            width: 100% !important;
            min-height: 50px !important;
            padding: 13px 20px !important;
            font-size: 15px !important;
            border-radius: 14px !important;
        }
        [data-testid="stDownloadButton"] > button {
            width: 100% !important;
            min-height: 44px !important;
            font-size: 14px !important;
            text-align: center !important;
        }

        /* ── Inputs: 16px evita zoom en iOS, área táctil grande ── */
        input[type="text"],
        input[type="password"],
        input[type="number"],
        textarea {
            font-size: 16px !important;
            min-height: 48px !important;
            padding: 12px 14px !important;
            border-radius: 12px !important;
        }
        div[data-baseweb="select"] > div {
            min-height: 48px !important;
            font-size: 16px !important;
            border-radius: 12px !important;
        }
        [data-testid="stDateInput"] input {
            min-height: 48px !important;
            font-size: 16px !important;
        }

        /* ── Slider: thumb más grande ── */
        [data-testid="stSlider"] [role="slider"] {
            width: 26px !important;
            height: 26px !important;
            box-shadow: 0 2px 8px rgba(140,94,88,0.35) !important;
        }
        [data-testid="stSlider"] {
            padding: 8px 0 !important;
        }

        /* ── Checkbox: área táctil cómoda ── */
        [data-testid="stCheckbox"] label {
            font-size: 15px !important;
            min-height: 44px !important;
            display: flex !important;
            align-items: center !important;
            gap: 10px !important;
            cursor: pointer !important;
        }

        /* ── Expanders: cabecera más grande ── */
        [data-testid="stExpander"] {
            border-radius: 16px !important;
            margin-bottom: 8px !important;
        }
        [data-testid="stExpander"] summary {
            padding: 16px 16px !important;
            font-size: 14px !important;
            min-height: 52px !important;
            display: flex !important;
            align-items: center !important;
        }

        /* ── Dataframes: scroll horizontal suave ── */
        .stDataFrame {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            border-radius: 14px !important;
        }
        .stDataFrame thead tr th {
            font-size: 10px !important;
            padding: 8px 10px !important;
        }
        .stDataFrame tbody tr td {
            font-size: 12px !important;
            padding: 8px 10px !important;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            min-width: 280px !important;
            max-width: 88vw !important;
        }
        [data-testid="stSidebar"] .block-container {
            padding: 1.5rem 1rem 2rem !important;
        }

        /* ── Login card ── */
        .login-card {
            padding: 40px 24px !important;
            border-radius: 22px !important;
            margin-top: 10px !important;
            box-shadow: 0 12px 40px rgba(140,94,88,0.12) !important;
        }
        .login-card h2 { font-size: 2rem !important; }

        /* ── Alerts ── */
        [data-testid="stAlert"] {
            border-radius: 14px !important;
            font-size: 13px !important;
            padding: 12px 14px !important;
        }

        /* ── Separadores ── */
        hr { margin: 0.8rem 0 !important; }

        /* ── Número input: sin flechas (más limpio en móvil) ── */
        input[type="number"]::-webkit-inner-spin-button,
        input[type="number"]::-webkit-outer-spin-button {
            opacity: 1;
            height: 32px;
        }

        /* ── Quitar hover effects (no aplican en touch) ── */
        [data-testid="stMetric"]:hover {
            transform: none !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
        }
        .stButton > button:hover {
            transform: none !important;
        }
        [data-testid="stFormSubmitButton"] > button:hover {
            transform: none !important;
        }
    }

    /* ═══════════════════════════════════════════════════════
       MÓVIL PEQUEÑO  (≤ 390px)  —  iPhone SE / mini
    ═══════════════════════════════════════════════════════ */
    @media (max-width: 390px) {
        .block-container { padding: 0.5rem 0.6rem 5rem !important; }
        h1 { font-size: 1.35rem !important; }
        .stTabs [data-baseweb="tab"] {
            padding: 7px 10px !important;
            font-size: 11px !important;
        }
        [data-testid="stMetricValue"] { font-size: 1.15rem !important; }
        .login-card { padding: 32px 18px !important; }
        .login-card h2 { font-size: 1.7rem !important; }
    }

    </style>
    """, unsafe_allow_html=True)
