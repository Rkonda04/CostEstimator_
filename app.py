import streamlit as st
import pandas as pd
import re
import os

st.set_page_config(
    page_title="COH Pipe Cost Estimator · Civitas",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Civitas purple theme, PFAS-style layout
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --purple:        #5b2d8e;
  --purple-dark:   #3a1870;
  --purple-mid:    #7040b0;
  --purple-light:  #9b6fda;
  --purple-pale:   #f3efff;
  --purple-border: #ddd0f5;
  --bg:            #eeedf4;
  --white:         #ffffff;
  --border:        #e8e3f0;
  --text:          #1a0f2e;
  --text-mid:      #3a1870;
  --text-muted:    #6b5e8a;
  --text-light:    #a090c0;
  --amber:         #c97700;
  --amber-bg:      #fff8ec;
  --amber-border:  #f5d080;
  --green:         #1a7a42;
  --green-bg:      #eafaf2;
  --mono:          'JetBrains Mono', monospace;
  --sans:          'Inter', sans-serif;
  --r:             14px;
  --r-sm:          10px;
  --shadow:        0 2px 8px rgba(91,45,142,0.08), 0 8px 28px rgba(91,45,142,0.06);
  --shadow-sm:     0 1px 4px rgba(91,45,142,0.07);
}

html, body, [class*="css"], .stApp {
  font-family: var(--sans) !important;
  background: var(--bg) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── SHARED HEADER ── */
.civ-header {
  background: linear-gradient(135deg, var(--purple-dark) 0%, var(--purple) 100%);
  padding: 0 36px;
  display: flex; align-items: center; justify-content: space-between;
  height: 64px;
  position: sticky; top: 0; z-index: 1000;
  box-shadow: 0 2px 20px rgba(58,24,112,0.4);
}
.civ-logo { display: flex; align-items: center; gap: 10px; cursor: pointer; }
.civ-logo svg { width: 44px; height: 44px; }
.civ-logo-text { font-size: 26px; font-weight: 900; color: white; letter-spacing: -0.02em; line-height:1; }
.civ-logo-sub  { font-size: 9px;  font-weight: 500; color: rgba(255,255,255,0.45); letter-spacing: 0.2em; text-transform: uppercase; }
.civ-nav { display: flex; align-items: center; gap: 8px; }
.civ-nav-badge {
  padding: 5px 14px; border-radius: 20px; font-size: 11px;
  font-weight: 600; font-family: var(--mono);
}
.badge-wh  { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: rgba(255,255,255,0.85); }
.badge-amb { background: rgba(255,200,60,0.2); border: 1px solid rgba(255,200,60,0.35); color: #ffd060; }
.civ-subbar {
  height: 3px;
  background: linear-gradient(90deg, var(--purple-mid), var(--purple-light), var(--purple-mid));
}

/* ══════════════════════════════════════
   HOME PAGE — PFAS style
══════════════════════════════════════ */
.hero-banner {
  background: linear-gradient(135deg, var(--purple-dark) 0%, var(--purple) 100%);
  padding: 56px 24px 52px;
  text-align: center;
}
.hero-banner h1 {
  font-size: 42px; font-weight: 900; color: white;
  letter-spacing: -0.03em; margin: 0 0 12px;
  line-height: 1.1;
}
.hero-banner p {
  font-size: 16px; color: rgba(255,255,255,0.65);
  margin: 0 auto 28px; max-width: 520px; line-height: 1.6;
}
.hero-btn {
  display: inline-block;
  background: white; color: var(--purple);
  font-size: 15px; font-weight: 700;
  padding: 13px 32px; border-radius: 50px;
  cursor: pointer; border: none;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  transition: all 0.18s;
  text-decoration: none;
}
.hero-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(0,0,0,0.2); }

.home-wrap {
  max-width: 760px; margin: 0 auto; padding: 40px 24px 80px;
}
.info-card {
  background: white; border-radius: var(--r);
  border-left: 4px solid var(--purple);
  padding: 28px 32px;
  box-shadow: var(--shadow);
  margin-bottom: 20px;
}
.info-card h2 {
  font-size: 20px; font-weight: 800; color: var(--purple);
  margin: 0 0 16px; letter-spacing: -0.01em;
}
.info-card ul { margin: 0; padding: 0; list-style: none; }
.info-card ul li {
  font-size: 14px; color: var(--text-muted);
  padding: 5px 0; display: flex; align-items: flex-start; gap: 10px;
  line-height: 1.5;
}
.info-card ul li::before {
  content: '—'; color: var(--purple); font-weight: 700;
  flex-shrink: 0; margin-top: 1px;
}
.info-card p { font-size: 14px; color: var(--text-muted); margin: 0 0 12px; line-height: 1.6; }

.data-stats {
  display: flex; gap: 16px; flex-wrap: wrap; margin-top: 14px;
}
.stat-pill {
  background: var(--purple-pale); border: 1px solid var(--purple-border);
  border-radius: 8px; padding: 10px 18px; text-align: center;
}
.stat-pill-num { font-size: 22px; font-weight: 800; color: var(--purple); font-family: var(--mono); }
.stat-pill-lbl { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

/* ══════════════════════════════════════
   ESTIMATOR PAGE
══════════════════════════════════════ */
.page-wrap { max-width: 1100px; margin: 0 auto; padding: 28px 24px 64px; }

/* pipe-type pill buttons */
.stButton > button {
  border-radius: 50px !important;
  font-family: var(--sans) !important;
  font-weight: 600 !important; font-size: 14px !important;
  padding: 10px 22px !important;
  transition: all 0.18s ease !important;
}
.stButton > button[kind="primary"] {
  background: var(--purple) !important; border: none !important;
  color: white !important; box-shadow: 0 4px 16px rgba(91,45,142,0.32) !important;
}
.stButton > button[kind="primary"]:hover {
  background: var(--purple-dark) !important;
  box-shadow: 0 6px 20px rgba(91,45,142,0.42) !important;
  transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
  background: white !important; border: 2px solid var(--border) !important;
  color: var(--text-muted) !important; box-shadow: var(--shadow-sm) !important;
}
.stButton > button[kind="secondary"]:hover {
  border-color: var(--purple-light) !important; color: var(--purple) !important;
  background: var(--purple-pale) !important;
}

/* cards */
.card {
  background: var(--white); border-radius: var(--r);
  padding: 22px 26px; border: 1px solid var(--border);
  box-shadow: var(--shadow); margin-bottom: 16px;
}
.card-label {
  font-size: 11px; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--purple); margin-bottom: 18px;
}

/* cost hero */
.cost-hero {
  background: linear-gradient(140deg, var(--purple-dark) 0%, var(--purple) 60%, var(--purple-mid) 100%);
  border-radius: var(--r); padding: 26px 28px; color: white;
  position: relative; overflow: hidden;
  box-shadow: 0 8px 32px rgba(91,45,142,0.38);
  border: 1px solid rgba(255,255,255,0.07); margin-bottom: 16px;
}
.cost-hero::before {
  content: ''; position: absolute; top: -55px; right: -55px;
  width: 190px; height: 190px; border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.07) 0%, transparent 65%);
  pointer-events: none;
}
.ch-eye  { font-size: 10px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; color: rgba(255,255,255,0.38); margin-bottom: 10px; font-family: var(--mono); }
.ch-lbl  { font-size: 12px; font-weight: 500; color: rgba(255,255,255,0.48); margin-bottom: 6px; }
.ch-val  { font-size: 52px; font-weight: 900; letter-spacing: -0.03em; line-height: 1; color: white; }
.ch-unit { font-size: 18px; font-weight: 400; color: rgba(255,255,255,0.38); margin-left: 4px; }
.ch-rng  { font-size: 12px; color: rgba(255,255,255,0.32); margin-top: 6px; font-family: var(--mono); }
.ch-div  { border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 16px 0; }
.ch-tot-lbl { font-size: 11px; color: rgba(255,255,255,0.42); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px; }
.ch-tot-val { font-size: 32px; font-weight: 900; color: #7dffc2; letter-spacing: -0.02em; }
.ch-infl { margin-top: 14px; padding: 10px 14px; border-radius: 10px; font-size: 11px; font-family: var(--mono); line-height: 1.55; }
.ch-fut  { background: rgba(255,200,60,0.14); border: 1px solid rgba(255,200,60,0.28); color: #ffd060; }
.ch-hist { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: rgba(255,255,255,0.36); }
.ch-chips { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 16px; }
.ch-chip { padding: 5px 13px; border-radius: 20px; font-size: 11px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.14); color: rgba(255,255,255,0.58); font-family: var(--mono); }
.ch-chip strong { color: white; }
.ch-empty { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 240px; gap: 12px; }
.ch-empty-icon { font-size: 44px; opacity: 0.22; }
.ch-empty-text { font-size: 13px; color: rgba(255,255,255,0.28); text-align: center; line-height: 1.7; }

/* future banner */
.fut-banner { background: var(--amber-bg); border: 1px solid var(--amber-border); border-left: 4px solid var(--amber); border-radius: var(--r-sm); padding: 12px 16px; font-size: 13px; color: #5a3800; line-height: 1.6; margin-bottom: 14px; }
.fut-banner strong { color: #3a2200; }

/* section dividers */
.sec-div { display: flex; align-items: center; gap: 16px; margin: 30px 0 18px; }
.sec-div-line { flex: 1; height: 1px; background: var(--border); }
.sec-div-lbl { font-size: 11px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: var(--purple); white-space: nowrap; padding: 5px 16px; background: var(--purple-pale); border-radius: 20px; border: 1px solid var(--purple-border); }

/* tables */
.tbl-wrap { overflow-x: auto; border-radius: var(--r-sm); border: 1px solid var(--border); margin-bottom: 8px; }
.civ-tbl { width: 100%; border-collapse: collapse; font-size: 13px; font-family: var(--sans); }
.civ-tbl thead th { background: var(--purple); padding: 11px 14px; color: rgba(255,255,255,0.88); font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; text-align: left; white-space: nowrap; }
.civ-tbl thead th.r { text-align: right; }
.civ-tbl thead th.c { text-align: center; }
.civ-tbl tbody tr { border-bottom: 1px solid #f0eaf9; }
.civ-tbl tbody tr:nth-child(even) { background: #faf8ff; }
.civ-tbl tbody tr:hover { background: var(--purple-pale); }
.civ-tbl tbody tr:last-child { border-bottom: none; }
.civ-tbl td { padding: 10px 14px; color: var(--text); vertical-align: middle; }
.civ-tbl td.r { text-align: right; font-family: var(--mono); }
.civ-tbl td.c { text-align: center; }
.civ-tbl tfoot tr { background: #f5f0ff; border-top: 2px solid var(--purple-border); }
.civ-tbl tfoot td { padding: 11px 14px; font-weight: 700; color: var(--purple-dark); }
.civ-tbl tfoot td.r { text-align: right; font-family: var(--mono); }
.star-low { color: var(--green); font-weight: 700; }
.tag-low { display: inline-block; background: var(--green-bg); color: var(--green); font-size: 9px; font-weight: 800; padding: 1px 5px; border-radius: 4px; margin-left: 4px; font-family: var(--mono); }
.dash-nil { color: #ccc; }
.bh-col { border-left: 2px solid rgba(255,255,255,0.15) !important; }
.proj-name { font-weight: 600; color: var(--text-mid); font-size: 13px; }
.proj-desc { color: var(--text-light); font-size: 10px; margin-top: 2px; }
.mat-sel-row td { background: #f0fdf7 !important; }
.mat-bar-bg { background: var(--border); border-radius: 4px; height: 7px; overflow: hidden; min-width: 80px; }
.mat-bar-fill { height: 100%; border-radius: 4px; }
.vs-low  { color: var(--green); font-weight: 700; font-size: 12px; }
.vs-high { color: var(--amber); font-weight: 600; font-size: 12px; }

/* estimate summary */
.grand-total { font-size: 26px; font-weight: 900; color: var(--green); font-family: var(--mono); }
.yr-fut  { display: inline-block; background: var(--amber-bg); color: #7a4a00; border: 1px solid var(--amber-border); font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 5px; font-family: var(--mono); }
.yr-hist { display: inline-block; background: var(--purple-pale); color: var(--purple); border: 1px solid var(--purple-border); font-size: 10px; font-weight: 600; padding: 2px 7px; border-radius: 5px; font-family: var(--mono); }
.proj-pct { font-size: 10px; color: var(--amber); font-family: var(--mono); font-weight: 600; }
.base-yr  { font-size: 10px; color: var(--text-light); font-family: var(--mono); }

/* empty state */
.empty-box { text-align: center; padding: 52px 24px; }
.empty-icon { font-size: 44px; margin-bottom: 14px; opacity: 0.28; }
.empty-text { font-size: 14px; color: var(--text-muted); line-height: 1.8; }

/* footer */
.civ-footer { background: var(--purple-dark); color: rgba(255,255,255,0.38); font-size: 11px; padding: 18px 36px; text-align: center; font-family: var(--mono); letter-spacing: 0.04em; }
.civ-footer strong { color: rgba(255,255,255,0.72); }

/* widget overrides */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
  font-size: 11px !important; font-weight: 700 !important;
  letter-spacing: 0.1em !important; text-transform: uppercase !important;
  color: var(--text-muted) !important; margin-bottom: 4px !important;
}
div[data-testid="stSelectbox"] > div > div {
  border: 1.5px solid var(--border) !important; border-radius: 10px !important;
  font-family: var(--sans) !important; font-size: 14px !important;
  background: white !important; box-shadow: var(--shadow-sm) !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within {
  border-color: var(--purple) !important; box-shadow: 0 0 0 3px rgba(91,45,142,0.12) !important;
}
div[data-testid="stNumberInput"] input {
  border: 1.5px solid var(--border) !important; border-radius: 10px !important;
  font-family: var(--mono) !important; font-size: 15px !important;
  color: var(--text-mid) !important; font-weight: 600 !important;
  padding: 10px 14px !important; background: white !important;
  box-shadow: var(--shadow-sm) !important;
}
div[data-testid="stNumberInput"] input:focus {
  border-color: var(--purple) !important; box-shadow: 0 0 0 3px rgba(91,45,142,0.12) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
CURRENT_YEAR        = 2026
PROJECTION_END_YEAR = 2050   # ← years 2026–2050 in dropdown ✓
INFLATION_RATES = {
    2021: 0.0470, 2022: 0.0800, 2023: 0.0410,
    2024: 0.0295, 2025: 0.0268,
    2026: 0.0270, 2027: 0.0240, 2028: 0.0230, 2029: 0.0200,
    **{yr: 0.0200 for yr in range(2030, PROJECTION_END_YEAR + 1)},
}
PIPE_TYPES = ["Waterline", "Gravity Main", "Force Main", "Wastewater"]
PIPE_ICONS = {"Waterline": "🚰", "Gravity Main": "🏗️", "Force Main": "⚡", "Wastewater": "🔧"}
BID_COLORS = ["#3a1870","#5b2d8e","#1a4a6b","#1a5c3a","#5c3a1a","#4a1a5c"]

# ── Session state ──────────────────────────────────────────────────────────────
for key, val in [("page","home"), ("line_items",[]), ("pipe_type","Waterline")]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Math helpers ───────────────────────────────────────────────────────────────
def cum_factor(from_year):
    if from_year >= CURRENT_YEAR: return 1.0
    f = 1.0
    for yr in range(int(from_year) + 1, CURRENT_YEAR + 1):
        f *= (1 + INFLATION_RATES.get(yr, 0.0))
    return round(f, 4)

def future_factor(target_year):
    if target_year <= CURRENT_YEAR: return 1.0
    f = 1.0
    for yr in range(CURRENT_YEAR + 1, int(target_year) + 1):
        f *= (1 + INFLATION_RATES.get(yr, 0.0200))
    return round(f, 4)

def sort_dia(vals):
    return sorted(vals, key=lambda d: int(re.search(r'\d+', str(d)).group())
                  if re.search(r'\d+', str(d)) else 9999)

# ── Data loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    csv_path = None
    for p in ["Data/pipe_items1.csv", "pipe_items1.csv"]:
        if os.path.exists(p): csv_path = p; break
    try:
        alt = os.path.join(os.path.dirname(__file__), "Data", "pipe_items1.csv")
        if not csv_path and os.path.exists(alt): csv_path = alt
    except Exception: pass
    if not csv_path: return None, None, None, None

    df = pd.read_csv(csv_path, dtype=str)
    df["_cost_raw"] = pd.to_numeric(df.get("unit_cost", pd.Series(dtype=str)), errors="coerce") \
                      if "unit_cost" in df.columns else pd.Series(float("nan"), index=df.index)

    bidder_cols = sorted(
        [c for c in df.columns if re.match(r'unit_cost_bidder\d+', c)],
        key=lambda c: int(re.search(r'\d+', c).group())
    )
    for bc in bidder_cols:
        df[bc] = pd.to_numeric(df[bc], errors="coerce")
    if df["_cost_raw"].isna().all() and bidder_cols:
        df["_cost_raw"] = df[bidder_cols].mean(axis=1, skipna=True)

    if "unit" in df.columns:
        df = df[df["unit"].str.strip().str.upper() == "LF"]
    df = df.dropna(subset=["_cost_raw"])
    df = df[df["_cost_raw"] > 0].copy()

    yc = next((c for c in ["YEAR","year"] if c in df.columns), None)
    df["YEAR"] = pd.to_numeric(df[yc], errors="coerce") if yc else float("nan")
    if "source" not in df.columns: df["source"] = "Unknown"

    def apply_inf(row):
        yr = row["YEAR"]
        return row["_cost_raw"] if pd.isna(yr) else round(row["_cost_raw"] * cum_factor(int(yr)), 2)
    df["_cost"] = df.apply(apply_inf, axis=1)

    historic = sorted([int(y) for y in df["YEAR"].dropna().unique() if 2010 <= int(y) <= 2030])
    # All years: historic data years UNION 2026→2050 projection years
    all_yrs  = sorted(set(historic) | set(range(CURRENT_YEAR, PROJECTION_END_YEAR + 1)))
    return df, bidder_cols, historic, all_yrs

def get_rows(df, historic, pt, dia, mat=None, yr=None):
    m = (df["pipe_type"] == pt) & (df["diameter"] == dia)
    if mat and mat not in ("-- All Materials --", "-- Select Diameter First --"):
        m &= (df["material"] == mat)
    if yr is not None and historic and yr in historic:
        m_yr = m & (df["YEAR"] == yr)
        if not df[m_yr].empty: return df[m_yr]
    return df[m]

def get_stats(rows):
    if rows.empty: return {}
    c = rows["_cost"].dropna()
    return {"avg": round(c.mean(),2), "lo": round(c.min(),2),
            "hi": round(c.max(),2), "n": len(c), "tabs": rows["source"].nunique()}

def get_diameters(df, pt):
    return ["-- Select --"] + sort_dia(df[df["pipe_type"]==pt]["diameter"].dropna().unique())

def get_materials(df, historic, pt, dia, yr=None):
    m = (df["pipe_type"]==pt) & (df["diameter"]==dia)
    if yr is not None and historic and yr in historic:
        m2 = m & (df["YEAR"]==yr)
        if df[m2]["material"].dropna().any(): m = m2
    return ["-- All Materials --"] + sorted(df[m]["material"].dropna().unique())

def yr_int(val):
    if val == "All Years": return None
    m = re.search(r'\d{4}', str(val))
    return int(m.group()) if m else None

# ── Load ───────────────────────────────────────────────────────────────────────
df, bidder_cols, historic, all_yrs = load_data()

# ══════════════════════════════════════════════════════════════════════════════
# SHARED HEADER
# ══════════════════════════════════════════════════════════════════════════════
def render_header(show_nav=True):
    nav_html = f"""
      <div class="civ-nav">
        <span class="civ-nav-badge badge-wh">Base {CURRENT_YEAR}$</span>
        <span class="civ-nav-badge badge-amb">📈 → {PROJECTION_END_YEAR}</span>
      </div>""" if show_nav else ""

    st.markdown(f"""
    <div class="civ-header">
      <div class="civ-logo">
        <svg viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M5 34 Q22 4 39 34" stroke="rgba(255,255,255,0.9)" stroke-width="3.5" fill="none" stroke-linecap="round"/>
          <path d="M11 38 Q22 12 33 38" stroke="rgba(255,255,255,0.42)" stroke-width="2" fill="none" stroke-linecap="round"/>
        </svg>
        <div>
          <div class="civ-logo-text">civitas</div>
          <div class="civ-logo-sub">Engineering Group</div>
        </div>
      </div>
      {nav_html}
    </div>
    <div class="civ-subbar"></div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    render_header(show_nav=False)

    n_rows = len(df) if df is not None else 0
    n_proj = df["source"].nunique() if df is not None else 0
    hist_range = f"{min(historic)}–{max(historic)}" if historic else "—"

    # Hero banner
    st.markdown(f"""
    <div class="hero-banner">
      <div style="display:flex;align-items:center;justify-content:center;gap:16px;margin-bottom:28px">
        <div style="text-align:center">
          <div style="font-size:11px;color:rgba(255,255,255,0.45);letter-spacing:0.2em;text-transform:uppercase;margin-bottom:2px">Civitas Engineering Group</div>
          <div style="width:48px;height:2px;background:rgba(255,255,255,0.3);border-radius:2px"></div>
        </div>
        
        
      </div>
      <h1>COH Pipe Cost Estimator</h1>
      <p>Estimate unit costs for water and wastewater pipe installation based on historical bid data from Houston-area projects, with inflation adjustment and future cost projection.</p>
    </div>
    """, unsafe_allow_html=True)

    # Launch button
    st.markdown("<div style='text-align:center;margin-top:-22px;margin-bottom:40px'>", unsafe_allow_html=True)
    _, mid, _ = st.columns([2, 1, 2])
    with mid:
        if st.button("Launch Estimator →", type="primary", use_container_width=True):
            st.session_state.page = "estimator"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Info cards — centered
    st.markdown('<div class="home-wrap">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-card">
      <h2>What This Tool Does</h2>
      <ul>
        <li>Look up average, minimum, and maximum unit costs ($/LF) for waterline, gravity main, force main, and wastewater pipe</li>
        <li>Filter by pipe diameter, material, and bid year using real historical bid tab data</li>
        <li>Automatically adjusts historical costs to <strong>{CURRENT_YEAR} dollars</strong> using CPI inflation rates</li>
        <li>Projects costs forward to any year through <strong>{PROJECTION_END_YEAR}</strong> using ENR escalation rates</li>
        <li>Build a multi-line estimate and view the total project cost</li>
      </ul>
      <div class="data-stats">
        <div class="stat-pill">
          <div class="stat-pill-num">{n_rows:,}</div>
          <div class="stat-pill-lbl">LF bid rows</div>
        </div>
        <div class="stat-pill">
          <div class="stat-pill-num">{n_proj}</div>
          <div class="stat-pill-lbl">source projects</div>
        </div>
        <div class="stat-pill">
          <div class="stat-pill-num">{hist_range}</div>
          <div class="stat-pill-lbl">historical years</div>
        </div>
        <div class="stat-pill">
          <div class="stat-pill-num">{CURRENT_YEAR}–{PROJECTION_END_YEAR}</div>
          <div class="stat-pill-lbl">projection range</div>
        </div>
      </div>
    </div>

    <div class="info-card">
      <h2>Who It's For</h2>
      <ul>
        <li>Civitas project engineers estimating waterline or wastewater construction costs</li>
        <li>Planners needing a quick sanity check on pipe unit costs by material and diameter</li>
        <li>Anyone forecasting what today's costs will look like in a future bid year</li>
      </ul>
    </div>

    <div class="info-card">
      <h2>Quick Start</h2>
      <p>Get a cost estimate in 4 steps:</p>
      <ul>
        <li>Select your <strong>pipe type</strong> (Waterline, Gravity Main, Force Main, or Wastewater)</li>
        <li>Choose a <strong>diameter</strong> and <strong>material</strong> from the dropdowns</li>
        <li>Set a <strong>bid year</strong> — pick a historic year to filter data, or a future year (up to {PROJECTION_END_YEAR}) to project costs forward</li>
        <li>Enter a <strong>quantity</strong> and click <strong>＋ Add to Estimate</strong> to build your line-item total</li>
      </ul>
    </div>

    <div class="info-card">
      <h2>How Costs Are Calculated</h2>
      <ul>
        <li><strong>Historic normalization:</strong> All historical bids are inflated to {CURRENT_YEAR}$ using actual CPI rates</li>
        <li><strong>Future projection:</strong> {CURRENT_YEAR}$ costs are escalated forward using ENR projected rates (2.0%/yr after 2029)</li>
        <li><strong>Unit cost shown:</strong> Average across all matching LF bid rows; min/max range also displayed</li>
        <li>For budgetary planning only — not for contract use. AACE Class 5 accuracy.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;margin-top:32px'>", unsafe_allow_html=True)
    _, mid2, _ = st.columns([2, 1, 2])
    with mid2:
        if st.button("Launch Estimator →  ", type="primary", use_container_width=True):
            st.session_state.page = "estimator"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="civ-footer">
      <strong>Civitas Engineering Group, Inc.</strong> &nbsp;·&nbsp;
      Base Year {CURRENT_YEAR} &nbsp;·&nbsp;
      ENR Escalation → {PROJECTION_END_YEAR} &nbsp;·&nbsp;
      For Budgetary Planning Only
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ESTIMATOR PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "estimator":
    render_header(show_nav=True)

    if df is None:
        st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
        st.error("⚠️  `pipe_items1.csv` not found. Place it in `Data/pipe_items1.csv` next to `app.py`.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    # Back link + pipe type buttons
    back_col, *pt_cols = st.columns([0.5] + [1]*len(PIPE_TYPES))
    with back_col:
        if st.button("← Home", type="secondary", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    for i, pt_opt in enumerate(PIPE_TYPES):
        with pt_cols[i]:
            active = st.session_state.pipe_type == pt_opt
            if st.button(f"{PIPE_ICONS[pt_opt]}  {pt_opt}", key=f"btn_{pt_opt}",
                         type="primary" if active else "secondary", use_container_width=True):
                st.session_state.pipe_type = pt_opt
                st.rerun()

    st.markdown("<div style='margin-bottom:18px'></div>", unsafe_allow_html=True)
    pt = st.session_state.pipe_type

    # Two columns
    col_l, col_r = st.columns([1.35, 1], gap="large")

    with col_l:
        st.markdown('<div class="card"><div class="card-label">Selection Filters</div>', unsafe_allow_html=True)
        fc1, fc2 = st.columns(2)
        with fc1:
            dia = st.selectbox("Diameter", get_diameters(df, pt), key="sel_dia")
        with fc2:
            # All years: historic + 2026→2050 — verify all 25 future years appear
            year_opts = ["All Years"] + [str(y) for y in all_yrs]
            yr_raw = st.selectbox(f"Bid Year (historic or up to {PROJECTION_END_YEAR})", year_opts, key="sel_yr")

        yr         = yr_int(yr_raw)
        is_future  = yr is not None and yr > CURRENT_YEAR
        is_hist    = yr is not None and historic and yr in historic

        fc3, fc4 = st.columns(2)
        with fc3:
            mat_opts = (["-- Select Diameter First --"] if dia == "-- Select --"
                        else get_materials(df, historic, pt, dia, yr))
            mat = st.selectbox("Material", mat_opts, key="sel_mat")
        with fc4:
            qty = st.number_input("Quantity (LF)", min_value=0.0, max_value=9_999_999.0,
                                  value=1000.0, step=100.0, key="num_qty")
        st.markdown('</div>', unsafe_allow_html=True)

        if is_future:
            ff_i = future_factor(yr)
            pct_i = (ff_i - 1) * 100
            yrs_out = yr - CURRENT_YEAR
            st.markdown(f"""
            <div class="fut-banner">
              📅 <strong>Future Year: {yr}</strong> — Projecting from {CURRENT_YEAR}$ using ENR escalation.
              Multiplier: <strong>&times;{ff_i:.4f}</strong> (+{pct_i:.1f}% over {yrs_out} yr{'s' if yrs_out!=1 else ''}).
              Historical bid table shows raw prices unchanged.
            </div>""", unsafe_allow_html=True)

        ba, bb, _ = st.columns([1.5, 1, 1])
        with ba:
            add_clicked = st.button("＋ Add to Estimate", type="primary", use_container_width=True)
        with bb:
            if st.button("🗑 Clear All", type="secondary", use_container_width=True):
                st.session_state.line_items = []
                st.rerun()

    with col_r:
        rows    = get_rows(df, historic, pt, dia, mat, yr) if dia != "-- Select --" else pd.DataFrame()
        s       = get_stats(rows)
        mat_sel = mat not in ("-- All Materials --","-- Select Diameter First --")
        ff      = future_factor(yr) if is_future else 1.0
        du      = round(s["avg"]*ff,2) if s else 0
        dlo     = round(s["lo"]*ff,2)  if s else 0
        dhi     = round(s["hi"]*ff,2)  if s else 0
        tot     = round(du*qty,0) if s and mat_sel and qty>0 else None
        dy      = yr if yr else CURRENT_YEAR

        if dia == "-- Select --" or not s:
            icon = "📐" if dia == "-- Select --" else "🔍"
            msg  = ("Select a diameter to view costs" if dia == "-- Select --"
                    else "No data for this selection —<br>try adjusting the filters.")
            st.markdown(f'<div class="cost-hero"><div class="ch-empty"><div class="ch-empty-icon">{icon}</div><div class="ch-empty-text">{msg}</div></div></div>', unsafe_allow_html=True)
        else:
            ctx = f"{pt} · {mat if mat_sel else 'All Materials'} · {'All Years' if not yr else yr}"
            infl_html = (
                f'<div class="ch-infl ch-fut">📈 Base {CURRENT_YEAR}$ avg: <strong>${s["avg"]:,.2f}/LF</strong> &times; {ff:.4f} (+{(ff-1)*100:.1f}% over {yr-CURRENT_YEAR} yrs) → <strong>${du:,.2f}/LF in {yr}$</strong></div>'
                if is_future else
                (f'<div class="ch-infl ch-hist">Bids from {yr} normalized &times;{cum_factor(yr):.4f} (+{(cum_factor(yr)-1)*100:.1f}%) → {CURRENT_YEAR}$</div>'
                 if is_hist else "")
            )
            tot_html = (f'<hr class="ch-div"><div class="ch-tot-lbl">{qty:,.0f} LF &times; ${du:,.2f} &nbsp;→&nbsp; Estimated Total</div><div class="ch-tot-val">${tot:,.0f}</div>'
                        if tot is not None else "")

            st.markdown(f"""
            <div class="cost-hero">
              <div class="ch-eye">{ctx.upper()}</div>
              <div class="ch-lbl">{'Projected' if is_future else 'Avg'} Unit Cost ({dy}$)</div>
              <div class="ch-val">${du:,.2f}<span class="ch-unit">/ LF</span></div>
              <div class="ch-rng">Min ${dlo:,.2f} &nbsp;–&nbsp; Max ${dhi:,.2f} / LF</div>
              {tot_html}{infl_html}
              <div class="ch-chips">
                <div class="ch-chip"><strong>{s["n"]}</strong> bid rows</div>
                <div class="ch-chip"><strong>{s["tabs"]}</strong> project{'s' if s['tabs']!=1 else ''}</div>
                <div class="ch-chip"><strong>{'All Yrs' if not yr else yr}</strong></div>
              </div>
            </div>""", unsafe_allow_html=True)

            if add_clicked:
                if mat_sel and qty > 0:
                    st.session_state.line_items.append({
                        "pipe_type": pt, "diameter": dia, "material": mat,
                        "qty": qty, "bid_year": yr, "raw": round(rows["_cost_raw"].mean(),2),
                        "unit_cost": du, "n": s["n"], "tabs": s["tabs"],
                        "total": tot, "is_future": is_future,
                    })
                    st.rerun()
                else:
                    st.warning("Select a specific material and quantity > 0 to add.")

    # ── Bid Data Table ──────────────────────────────────────────────────────────
    if dia != "-- Select --" and s:
        rows_tbl   = get_rows(df, historic, pt, dia, mat, yr)
        present_bc = [bc for bc in bidder_cols if rows_tbl[bc].notna().any()] if bidder_cols else []

        if not rows_tbl.empty and present_bc:
            yr_lbl = str(yr) if yr else "All Years"
            st.markdown('<div class="sec-div"><div class="sec-div-line"></div><div class="sec-div-lbl">Historical Bid Data</div><div class="sec-div-line"></div></div>', unsafe_allow_html=True)

            grp_keys = ["source","YEAR"] if "YEAR" in rows_tbl.columns else ["source"]
            pivot_rows = []
            for key, grp in rows_tbl.groupby(grp_keys, sort=True, dropna=False):
                kv = key if isinstance(key, tuple) else (key,)
                kd = dict(zip(grp_keys, kv))
                proj = str(kd.get("source","")).replace(".xlsx","").replace(".xls","")
                yr_v = kd.get("YEAR","")
                yr_v = int(yr_v) if pd.notna(yr_v) and yr_v != "" else "—"
                desc = ""
                if "description" in grp.columns:
                    dv = grp["description"].dropna().unique()
                    desc = str(dv[0]) if len(dv) else ""
                rd = {"proj": proj, "yr": yr_v, "desc": desc}
                for bc in present_bc:
                    vals = grp[bc].dropna()
                    rd[bc] = vals.iloc[0] if not vals.empty else None
                pivot_rows.append(rd)

            hdr = '<th>Project / File</th><th class="c">Year</th>'
            for i, bc in enumerate(present_bc):
                bnum  = re.search(r'\d+', bc).group()
                color = BID_COLORS[i % len(BID_COLORS)]
                hdr  += f'<th class="bh-col r" style="background:{color}">Bidder {bnum}</th>'

            body = ""
            for pr in pivot_rows:
                uvals = [pr[bc] for bc in present_bc if pr.get(bc) is not None]
                mn    = min(uvals) if uvals else None
                pn = pr["proj"][:36] + ("…" if len(pr["proj"])>36 else "")
                dn = pr["desc"][:62] + ("…" if len(pr["desc"])>62 else "")
                pc = f'<div class="proj-name">{pn}</div>'
                if dn: pc += f'<div class="proj-desc">{dn}</div>'
                body += f'<tr><td>{pc}</td><td class="c" style="font-family:var(--mono);font-size:12px;color:var(--text-light)">{pr["yr"]}</td>'
                for bc in present_bc:
                    uc  = pr.get(bc)
                    low = uc is not None and mn is not None and abs(uc-mn)<0.01 and len(uvals)>1
                    cs  = (f'<span class="star-low">${uc:,.0f}<span class="tag-low">LOW</span></span>'
                           if low else f'${uc:,.0f}') if uc is not None else '<span class="dash-nil">—</span>'
                    body += f'<td class="r" style="border-left:1px solid #f0eaf9">{cs}</td>'
                body += '</tr>'

            foot = '<tr><td colspan="2" style="font-size:11px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--purple-dark)">Avg across all projects (raw bids)</td>'
            for bc in present_bc:
                av = rows_tbl[bc].dropna().mean()
                av = round(av,2) if pd.notna(av) else None
                foot += f'<td class="r" style="border-left:1px solid var(--purple-border)">{"$"+f"{av:,.2f}" if av else "—"}</td>'
            foot += '</tr>'

            yr_note = f'Cost card projected to {yr}$' if is_future else f'Cost card normalized to {CURRENT_YEAR}$'
            st.markdown(f"""
            <div class="card">
              <div class="card-label">Raw Bid Prices by Project &amp; Bidder
                <span style="font-size:10px;color:var(--text-light);font-weight:400;font-family:var(--mono);text-transform:none;letter-spacing:0;margin-left:10px">
                  {s["n"]} rows · {len(pivot_rows)} project{'s' if len(pivot_rows)!=1 else ''} · {len(present_bc)} bidder{'s' if len(present_bc)!=1 else ''} · {yr_lbl}
                </span>
              </div>
              <div class="tbl-wrap">
                <table class="civ-tbl"><thead><tr>{hdr}</tr></thead><tbody>{body}</tbody><tfoot>{foot}</tfoot></table>
              </div>
              <div style="font-size:10px;color:var(--text-light);margin-top:8px;font-family:var(--mono)">
                LOW = lowest bid per project &nbsp;·&nbsp; Raw prices shown &nbsp;·&nbsp; {yr_note}
              </div>
            </div>""", unsafe_allow_html=True)

        # ── Material Comparison ────────────────────────────────────────────────
        all_mc = get_rows(df, historic, pt, dia, yr=yr)
        mc = (all_mc.groupby("material", as_index=False)
              .agg(avg=("_cost","mean"), lo=("_cost","min"), hi=("_cost","max"),
                   n=("_cost","count"), tabs=("source","nunique"))
              .sort_values("avg"))
        mc[["avg","lo","hi"]] = mc[["avg","lo","hi"]].round(2)

        if len(mc) > 1:
            cheapest  = mc.iloc[0]["avg"]
            max_avg   = mc["avg"].max()
            mat_sel_c = mat not in ("-- All Materials --","-- Select Diameter First --")
            yr_lbl    = str(yr) if yr else "All Years"
            col_heads = (f'<th class="r">Base {CURRENT_YEAR}$ / LF</th><th class="r">Projected {yr}$ / LF</th>'
                         if is_future else '<th class="r">Avg Unit Cost</th><th class="r">Min – Max</th>')
            mat_note  = (f"{dia} · projected to {yr}$" if is_future else f"{dia} · {yr_lbl} · {CURRENT_YEAR}$")

            st.markdown('<div class="sec-div"><div class="sec-div-line"></div><div class="sec-div-lbl">Material Comparison</div><div class="sec-div-line"></div></div>', unsafe_allow_html=True)

            mc_body = ""
            for _, r in mc.iterrows():
                sel     = mat_sel_c and (mat == r["material"])
                row_cls = 'class="mat-sel-row"' if sel else ""
                stag    = ' <span style="font-size:10px;color:var(--purple);font-weight:700">◀</span>' if sel else ""
                pct_c   = ((r["avg"]-cheapest)/cheapest*100) if cheapest>0 else 0
                vs_cls  = "vs-low" if pct_c<0.5 else "vs-high"
                vs_txt  = "cheapest" if pct_c<0.5 else f"+{pct_c:.0f}%"
                bar_w   = int((r["avg"]/max_avg)*100) if max_avg>0 else 0
                bar_c   = "#1a7a42" if pct_c<0.5 else "#6230b0"
                proj_a  = round(r["avg"]*ff,2)
                cost_cells = (
                    f'<td class="r" style="color:var(--text-light);font-size:12px">${r["avg"]:,.2f}</td>'
                    f'<td class="r" style="font-weight:700;color:var(--text-mid)">${proj_a:,.2f}</td>'
                    if is_future else
                    f'<td class="r" style="font-weight:700;color:var(--text-mid)">${r["avg"]:,.2f} / LF</td>'
                    f'<td class="r" style="font-size:12px;color:var(--text-light)">${r["lo"]:,.2f} – ${r["hi"]:,.2f}</td>'
                )
                mc_body += f"""<tr {row_cls}>
                  <td style="font-weight:{'600' if sel else '400'}">{r['material']}{stag}</td>
                  {cost_cells}
                  <td class="r" style="font-size:12px;color:var(--text-muted)">{int(r['n'])} bids / {int(r['tabs'])} proj</td>
                  <td style="padding:10px 14px"><div class="mat-bar-bg"><div class="mat-bar-fill" style="background:{bar_c};width:{bar_w}%"></div></div></td>
                  <td class="c"><span class="{vs_cls}">{vs_txt}</span></td>
                </tr>"""

            st.markdown(f"""
            <div class="card">
              <div class="card-label">Material Comparison
                <span style="font-size:10px;color:var(--text-light);font-weight:400;font-family:var(--mono);text-transform:none;letter-spacing:0;margin-left:10px">{mat_note} · sorted cheapest first</span>
              </div>
              <div class="tbl-wrap">
                <table class="civ-tbl"><thead><tr>
                  <th>Material</th>{col_heads}<th class="r">Bid Data</th><th>Relative</th><th class="c">vs Cheapest</th>
                </tr></thead><tbody>{mc_body}</tbody></table>
              </div>
              <div style="font-size:10px;color:var(--text-light);margin-top:8px;font-family:var(--mono)">All costs CPI-adjusted to {CURRENT_YEAR}$. For budgetary planning only.</div>
            </div>""", unsafe_allow_html=True)

    # ── Estimate Summary ────────────────────────────────────────────────────────
    st.markdown('<div class="sec-div"><div class="sec-div-line"></div><div class="sec-div-lbl">Estimate Summary</div><div class="sec-div-line"></div></div>', unsafe_allow_html=True)

    if not st.session_state.line_items:
        st.markdown("""<div class="card"><div class="empty-box"><div class="empty-icon">📋</div>
          <div class="empty-text">No line items yet.<br>Configure the filters above and click <strong>＋ Add to Estimate</strong>.</div>
          </div></div>""", unsafe_allow_html=True)
    else:
        rows_html = ""
        for li in st.session_state.line_items:
            is_fut   = li.get("is_future", False)
            ff_li    = future_factor(li["bid_year"]) if is_fut and li["bid_year"] else 1.0
            pct_li   = (ff_li-1)*100
            yr_disp  = str(li["bid_year"]) if li["bid_year"] else "All"
            yr_tag   = (f'<span class="yr-fut">📅 {yr_disp}</span>'
                        if is_fut else f'<span class="yr-hist">{yr_disp}</span>')
            cost_note = (f'<span class="proj-pct">&nbsp;+{pct_li:.1f}% proj</span>'
                         if is_fut else f'<span class="base-yr">&nbsp;{CURRENT_YEAR}$</span>')
            rows_html += f"""<tr>
              <td style="font-size:12px;color:var(--text-muted)">{li['pipe_type']}</td>
              <td style="font-weight:700;color:var(--text-mid)">{li['diameter']}</td>
              <td>{li['material']}</td>
              <td class="r">{li['qty']:,.0f} LF</td>
              <td class="c">{yr_tag}</td>
              <td class="r">${li['unit_cost']:,.2f}{cost_note}</td>
              <td class="c" style="font-size:11px;color:var(--text-muted)">{li['n']} bids / {li['tabs']} proj</td>
              <td class="r" style="color:var(--green);font-weight:700;font-size:15px">${li['total']:,.0f}</td>
            </tr>"""

        grand   = sum(li["total"] for li in st.session_state.line_items)
        n_items = len(st.session_state.line_items)

        st.markdown(f"""
        <div class="card">
          <div class="card-label">{n_items} Line Item{'s' if n_items!=1 else ''}
            <span style="font-size:10px;color:var(--text-light);font-weight:400;font-family:var(--mono);text-transform:none;letter-spacing:0;margin-left:10px">all costs in {CURRENT_YEAR}$ unless projected</span>
          </div>
          <div class="tbl-wrap">
            <table class="civ-tbl">
              <thead><tr>
                <th>Type</th><th>Diameter</th><th>Material</th>
                <th class="r">Quantity</th><th class="c">Bid Year</th>
                <th class="r">Unit Cost</th><th class="c">Bid Data</th><th class="r">Item Total</th>
              </tr></thead>
              <tbody>{rows_html}</tbody>
              <tfoot><tr>
                <td colspan="7" style="text-align:right;font-size:12px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--purple)">
                  Total Project Estimate ({CURRENT_YEAR}$)
                </td>
                <td class="r"><span class="grand-total">${grand:,.0f}</span></td>
              </tr></tfoot>
            </table>
          </div>
          <div style="font-size:10px;color:var(--text-light);margin-top:8px;font-family:var(--mono)">
            🟡 Yellow bid year = projected future cost &nbsp;·&nbsp; For budgetary planning only 
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="civ-footer">
      <strong>Civitas Engineering Group, Inc.</strong> &nbsp;·&nbsp;  &nbsp;·&nbsp;
      COH Pipe Cost Estimator &nbsp;·&nbsp; Base Year {CURRENT_YEAR} &nbsp;·&nbsp;
      ENR Escalation → {PROJECTION_END_YEAR} &nbsp;·&nbsp; For Budgetary Planning Only
    </div>""", unsafe_allow_html=True)