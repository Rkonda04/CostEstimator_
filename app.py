import streamlit as st
import pandas as pd
import re
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="COH Pipe Cost Estimator",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global style ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background: #f4f6f9;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Top header bar ── */
.top-bar {
    background: linear-gradient(135deg, #1a2744 0%, #243560 100%);
    padding: 18px 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 20px rgba(26,39,68,0.25);
    position: sticky;
    top: 0;
    z-index: 999;
}
.top-bar-left { display: flex; align-items: center; gap: 14px; }
.top-bar-logo {
    background: #3b7dd8;
    color: white;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 5px 10px;
    border-radius: 5px;
}
.top-bar-title {
    color: white;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: -0.02em;
}
.top-bar-sub {
    color: rgba(255,255,255,0.5);
    font-size: 12px;
    font-weight: 400;
    margin-left: 4px;
}
.top-bar-badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: rgba(255,255,255,0.8);
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    padding: 4px 12px;
    border-radius: 20px;
}

/* ── Main content wrapper ── */
.main-wrapper {
    padding: 28px 36px;
    max-width: 1400px;
    margin: 0 auto;
}

/* ── Section headers ── */
.section-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 10px;
}

/* ── Cards ── */
.card {
    background: white;
    border-radius: 12px;
    padding: 22px 26px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    margin-bottom: 16px;
    border: 1px solid #e8ecf3;
}

/* ── Pipe type pills ── */
.pill-group { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 4px; }
.pill {
    padding: 8px 18px;
    border-radius: 24px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    border: 2px solid #e2e8f0;
    background: white;
    color: #64748b;
    transition: all 0.15s;
}
.pill-active {
    border-color: #1a2744;
    background: #1a2744;
    color: white;
}

/* ── Cost card ── */
.cost-card {
    background: linear-gradient(135deg, #1a2744 0%, #243560 100%);
    border-radius: 12px;
    padding: 24px 28px;
    color: white;
    position: relative;
    overflow: hidden;
}
.cost-card::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 140px; height: 140px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.cost-card-label { font-size: 11px; color: rgba(255,255,255,0.5); font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px; }
.cost-card-value { font-size: 42px; font-weight: 700; letter-spacing: -0.03em; line-height: 1; }
.cost-card-unit { font-size: 14px; font-weight: 400; color: rgba(255,255,255,0.5); margin-left: 4px; }
.cost-card-range { font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 8px; }
.cost-card-total { margin-top: 16px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.12); }
.cost-card-total-val { font-size: 26px; font-weight: 700; color: #4ade80; }
.cost-card-infl { font-size: 10px; color: rgba(255,255,255,0.35); margin-top: 5px; font-family: 'DM Mono', monospace; }

/* ── Stat chips ── */
.stat-chip-row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 14px; }
.stat-chip {
    background: #f1f5f9;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 12px;
    color: #475569;
}
.stat-chip strong { color: #1a2744; font-weight: 700; }

/* ── Table styles ── */
.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    font-family: 'DM Sans', sans-serif;
}
.data-table th {
    background: #1a2744;
    color: white;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.data-table th.right { text-align: right; }
.data-table th.center { text-align: center; }
.data-table td { padding: 9px 14px; border-bottom: 1px solid #f1f5f9; color: #374151; }
.data-table td.right { text-align: right; }
.data-table td.center { text-align: center; }
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: #f8fafc; }
.data-table tfoot td {
    background: #f1f5f9;
    font-weight: 700;
    border-top: 2px solid #e2e8f0;
    color: #1a2744;
}
.lowest-cost { color: #16a34a !important; font-weight: 700 !important; }
.cheapest-badge {
    display: inline-block;
    background: #dcfce7;
    color: #16a34a;
    font-size: 10px;
    font-weight: 700;
    padding: 1px 6px;
    border-radius: 4px;
    margin-left: 4px;
}
.more-pct { color: #f59e0b; font-size: 11px; }
.selected-row td { background: #f0fdf4 !important; font-weight: 600; }

/* ── Summary estimate table ── */
.est-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}
.est-table th {
    background: #0f172a;
    color: white;
    padding: 10px 14px;
    font-size: 11px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.est-table th.right { text-align: right; }
.est-table td { padding: 10px 14px; border-bottom: 1px solid #f1f5f9; }
.est-table td.right { text-align: right; }
.est-table tfoot td {
    background: #f8fafc;
    border-top: 2px solid #1a2744;
    font-weight: 700;
    font-size: 15px;
}
.grand-total { color: #16a34a; font-size: 20px; font-weight: 800; }
.infl-note { font-size: 10px; color: #94a3b8; font-family: 'DM Mono', monospace; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 40px 20px;
    color: #94a3b8;
}
.empty-state-icon { font-size: 36px; margin-bottom: 12px; }
.empty-state-text { font-size: 14px; }

/* ── Alert / info ── */
.info-banner {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 12px;
    color: #1d4ed8;
    margin-bottom: 14px;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #64748b !important;
}
div[data-testid="stSelectbox"] > div > div {
    border: 2px solid #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #1a2744 !important;
    box-shadow: 0 0 0 3px rgba(26,39,68,0.08) !important;
}
div[data-testid="stNumberInput"] input {
    border: 2px solid #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 14px !important;
}
.stButton > button {
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.15s !important;
}

/* ── Divider ── */
.section-divider {
    border: none;
    border-top: 1px solid #e8ecf3;
    margin: 20px 0;
}

/* ── Scroll hint ── */
.scroll-hint { font-size: 10px; color: #cbd5e1; text-align: right; margin-top: 4px; }

/* ── Bidder header colors ── */
.bh-0 { background: #1a2744 !important; }
.bh-1 { background: #1a4a6b !important; }
.bh-2 { background: #1a5c3a !important; }
.bh-3 { background: #5c3a1a !important; }
.bh-4 { background: #4a1a5c !important; }
.bh-5 { background: #1a4a4a !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
CURRENT_YEAR = 2026
INFLATION_RATES = {
    2021: 0.0470, 2022: 0.0800, 2023: 0.0410,
    2024: 0.0295, 2025: 0.0268, 2026: 0.0240,
}
PIPE_TYPES = ["Waterline", "Gravity Main", "Force Main", "Wastewater"]
PIPE_ICONS = {"Waterline": "🚰", "Gravity Main": "🏗️", "Force Main": "⚡", "Wastewater": "🔧"}
BID_COLORS = ["#1a2744","#1a4a6b","#1a5c3a","#5c3a1a","#4a1a5c","#1a4a4a"]

# ── Session state ──────────────────────────────────────────────────────────────
if "line_items" not in st.session_state:
    st.session_state.line_items = []
if "pipe_type" not in st.session_state:
    st.session_state.pipe_type = "Waterline"

# ── Helpers ────────────────────────────────────────────────────────────────────
def cum_factor(from_year):
    if from_year is None or from_year >= CURRENT_YEAR:
        return 1.0
    f = 1.0
    for yr in range(int(from_year) + 1, CURRENT_YEAR + 1):
        f *= (1 + INFLATION_RATES.get(yr, 0.0))
    return round(f, 4)

def sort_dia(vals):
    def key(d):
        m = re.search(r'\d+', str(d))
        return int(m.group()) if m else 9999
    return sorted(vals, key=key)

@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), "Data", "pipe_items1.csv")
    if not os.path.exists(csv_path):
        # Try current dir
        csv_path = "Data/pipe_items1.csv"
    if not os.path.exists(csv_path):
        csv_path = "pipe_items1.csv"
    if not os.path.exists(csv_path):
        return None, None

    df = pd.read_csv(csv_path, dtype=str)

    # Detect bidder columns
    bidder_cols = sorted(
        [c for c in df.columns if re.match(r'unit_cost_bidder\d+', c)],
        key=lambda c: int(re.search(r'\d+', c).group())
    )
    if not bidder_cols:
        return None, None

    for bc in bidder_cols:
        df[bc] = pd.to_numeric(df[bc], errors="coerce")

    df["_cost_raw"] = df[bidder_cols].mean(axis=1, skipna=True)

    if "unit" in df.columns:
        df = df[df["unit"].str.strip().str.upper() == "LF"]
    df = df.dropna(subset=["_cost_raw"])
    df = df[df["_cost_raw"] > 0].copy()

    yc = next((c for c in ["YEAR", "year"] if c in df.columns), None)
    df["YEAR"] = pd.to_numeric(df[yc], errors="coerce") if yc else float("nan")
    if "source" not in df.columns:
        df["source"] = "Unknown"

    def apply_inflation(row):
        yr = row["YEAR"]
        if pd.isna(yr):
            return row["_cost_raw"]
        return round(row["_cost_raw"] * cum_factor(int(yr)), 2)

    df["_cost"] = df.apply(apply_inflation, axis=1)
    return df, bidder_cols

def get_rows(df, pt, dia, mat=None, yr=None):
    m = (df["pipe_type"] == pt) & (df["diameter"] == dia)
    if mat and mat not in ("-- All Materials --", "-- Select Diameter First --"):
        m &= (df["material"] == mat)
    if yr is not None:
        m_yr = m & (df["YEAR"] == yr)
        if not df[m_yr].empty:
            return df[m_yr]
    return df[m]

def get_stats(rows):
    if rows.empty:
        return {}
    c = rows["_cost"].dropna()
    return {
        "avg": round(c.mean(), 2),
        "lo": round(c.min(), 2),
        "hi": round(c.max(), 2),
        "n": len(c),
        "tabs": rows["source"].nunique(),
    }

def get_diameters(df, pt):
    vals = df[df["pipe_type"] == pt]["diameter"].dropna().unique()
    return ["-- Select --"] + sort_dia(vals)

def get_materials(df, pt, dia, yr=None):
    m = (df["pipe_type"] == pt) & (df["diameter"] == dia)
    if yr is not None:
        m2 = m & (df["YEAR"] == yr)
        if df[m2]["material"].dropna().any():
            m = m2
    return ["-- All Materials --"] + sorted(df[m]["material"].dropna().unique())

def yr_int(val):
    if val == "All Years":
        return None
    m = re.search(r'\d{4}', str(val))
    return int(m.group()) if m else None

# ── Load data ──────────────────────────────────────────────────────────────────
df, bidder_cols = load_data()

# ── Top bar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-bar">
  <div class="top-bar-left">
    <div class="top-bar-logo">CIVITAS</div>
    <div>
      <span class="top-bar-title">COH Pipe Cost Estimator</span>
      <span class="top-bar-sub">· City of Houston</span>
    </div>
  </div>
  <div class="top-bar-badge">FY 2026 $ · CPI Adjusted</div>
</div>
""", unsafe_allow_html=True)

# ── No data state ──────────────────────────────────────────────────────────────
if df is None:
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
    st.error("⚠️ `pipe_items1.csv` not found. Place it in `Data/pipe_items1.csv` next to `app.py`.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

data_years = sorted([int(y) for y in df["YEAR"].dropna().unique() if 2010 <= int(y) <= 2030])

# ── Main layout ────────────────────────────────────────────────────────────────
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# ── Row 1: Pipe type selector ──────────────────────────────────────────────────
st.markdown('<div class="section-label">Pipe Type</div>', unsafe_allow_html=True)

col_types = st.columns(len(PIPE_TYPES))
for i, pt in enumerate(PIPE_TYPES):
    with col_types[i]:
        active = st.session_state.pipe_type == pt
        icon = PIPE_ICONS[pt]
        style = "background:#1a2744;color:white;border-color:#1a2744;" if active else "background:white;color:#374151;"
        if st.button(f"{icon}  {pt}", key=f"pill_{pt}", use_container_width=True):
            st.session_state.pipe_type = pt
            st.rerun()

st.markdown("<div style='margin-bottom:20px'></div>", unsafe_allow_html=True)

# ── Row 2: Filters + Cost Card ─────────────────────────────────────────────────
left_col, right_col = st.columns([1.5, 1], gap="large")

with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Filters</div>', unsafe_allow_html=True)

    pt = st.session_state.pipe_type
    diameters = get_diameters(df, pt)

    f1, f2 = st.columns(2)
    with f1:
        dia = st.selectbox("Diameter", diameters, key="dia_select")
    with f2:
        year_opts = ["All Years"] + [str(y) for y in data_years]
        yr_val = st.selectbox("Bid Year", year_opts, key="year_select")

    yr = yr_int(yr_val)

    if dia == "-- Select --":
        mat_opts = ["-- Select Diameter First --"]
    else:
        mat_opts = get_materials(df, pt, dia, yr)

    f3, f4 = st.columns(2)
    with f3:
        mat = st.selectbox("Material", mat_opts, key="mat_select")
    with f4:
        qty = st.number_input("Quantity (LF)", min_value=0.0, max_value=9_999_999.0,
                              value=1000.0, step=100.0, key="qty_input")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Add to estimate buttons ──
    b1, b2, _ = st.columns([1.4, 1, 2])
    with b1:
        add_clicked = st.button("＋ Add to Estimate", type="primary", use_container_width=True)
    with b2:
        clear_clicked = st.button("🗑 Clear All", use_container_width=True)

    if clear_clicked:
        st.session_state.line_items = []
        st.rerun()

with right_col:
    # ── Cost card ──
    if dia == "-- Select --":
        st.markdown("""
        <div class="cost-card" style="min-height:200px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:8px">
          <div style="font-size:36px">📐</div>
          <div style="color:rgba(255,255,255,0.5);font-size:13px;text-align:center">Select a pipe type<br>and diameter to view costs</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        rows = get_rows(df, pt, dia, mat, yr)
        s = get_stats(rows)

        if not s:
            st.markdown("""
            <div class="cost-card" style="min-height:200px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:8px">
              <div style="font-size:28px">🔍</div>
              <div style="color:rgba(255,255,255,0.5);font-size:13px;text-align:center">No data for this selection.<br>Try a different filter combination.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            mat_selected = mat not in ("-- All Materials --", "-- Select Diameter First --")
            total = round(s["avg"] * qty, 0) if mat_selected and qty > 0 else None

            infl_note = ""
            if yr and yr < CURRENT_YEAR:
                f_val = cum_factor(yr)
                pct = (f_val - 1) * 100
                infl_note = f'<div class="cost-card-infl">Bids from {yr} inflated ×{f_val:.4f} (+{pct:.1f}%) → {CURRENT_YEAR}$</div>'

            yr_label = str(yr) if yr else "All Years"
            context_line = f"{pt} · {dia}" + (f" · {mat}" if mat_selected else "") + f" · {yr_label}"

            total_html = ""
            if total is not None:
                total_html = f"""
                <div class="cost-card-total">
                  <div style="font-size:11px;color:rgba(255,255,255,0.45);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px">{qty:,.0f} LF · Estimated Total</div>
                  <div class="cost-card-total-val">${total:,.0f}</div>
                </div>
                """

            st.markdown(f"""
            <div class="cost-card">
              <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-bottom:12px">{context_line}</div>
              <div class="cost-card-label">Avg Unit Cost ({CURRENT_YEAR}$)</div>
              <div class="cost-card-value">${s["avg"]:,.2f}<span class="cost-card-unit">/ LF</span></div>
              <div class="cost-card-range">Min ${s["lo"]:,.2f} &nbsp;–&nbsp; Max ${s["hi"]:,.2f} / LF</div>
              {total_html}
              {infl_note}
            </div>
            <div class="stat-chip-row">
              <div class="stat-chip"><strong>{s["n"]}</strong> bid rows</div>
              <div class="stat-chip"><strong>{s["tabs"]}</strong> project{'' if s['tabs']==1 else 's'}</div>
              <div class="stat-chip"><strong>{yr_label}</strong></div>
            </div>
            """, unsafe_allow_html=True)

            # ── Add to estimate logic ──
            if add_clicked:
                if mat_selected and qty > 0 and s:
                    raw_avg = round(rows["_cost_raw"].mean(), 2)
                    st.session_state.line_items.append({
                        "pipe_type": pt, "diameter": dia, "material": mat,
                        "qty": qty, "bid_year": yr, "raw": raw_avg,
                        "unit_cost": s["avg"], "n": s["n"], "tabs": s["tabs"],
                        "total": round(s["avg"] * qty, 0),
                    })
                    st.rerun()
                else:
                    st.warning("Select a specific material and quantity > 0 to add to estimate.")

st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

# ── Bid Data Table ─────────────────────────────────────────────────────────────
if dia != "-- Select --" and s:
    rows_for_table = get_rows(df, pt, dia, mat, yr)
    present_bidder_cols = [bc for bc in bidder_cols if rows_for_table[bc].notna().any()]

    if present_bidder_cols and not rows_for_table.empty:
        mat_selected_tbl = mat not in ("-- All Materials --", "-- Select Diameter First --")
        yr_label = str(yr) if yr else "All Years"
        n_bidders = len(present_bidder_cols)
        grp_keys = ["source", "YEAR"] if "YEAR" in rows_for_table.columns else ["source"]

        pivot_rows = []
        for key, grp in rows_for_table.groupby(grp_keys, sort=True, dropna=False):
            key_vals = key if isinstance(key, tuple) else (key,)
            key_dict = dict(zip(grp_keys, key_vals))
            proj = str(key_dict.get("source", "")).replace(".xlsx", "").replace(".xls", "")
            yr_v = key_dict.get("YEAR", "")
            yr_v = int(yr_v) if pd.notna(yr_v) and yr_v != "" else "—"
            desc = ""
            if "description" in grp.columns:
                dv = grp["description"].dropna().unique()
                desc = str(dv[0]) if len(dv) else ""
            row_data = {"proj": proj, "yr": yr_v, "desc": desc}
            for bc in present_bidder_cols:
                vals = grp[bc].dropna()
                row_data[bc] = round(vals.mean(), 2) if not vals.empty else None
            pivot_rows.append(row_data)

        n_projects = len(pivot_rows)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
          <div>
            <div class="section-label">Bid Data — Unit Costs by Project & Bidder</div>
            <div style="font-size:12px;color:#64748b">{s['n']} rows &nbsp;·&nbsp; {n_projects} project{'s' if n_projects!=1 else ''} &nbsp;·&nbsp; {n_bidders} bidder{'s' if n_bidders!=1 else ''} &nbsp;·&nbsp; {yr_label} &nbsp;·&nbsp; all costs in {CURRENT_YEAR}$</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Build HTML table
        header_html = """
        <th class="data-table-th">Project / File</th>
        <th class="data-table-th center">Year</th>
        """
        for i, bc in enumerate(present_bidder_cols):
            bnum = re.search(r'\d+', bc).group()
            color = BID_COLORS[i % len(BID_COLORS)]
            header_html += f'<th style="padding:10px 14px;text-align:right;background:{color};color:white;border-left:3px solid rgba(255,255,255,0.15);white-space:nowrap;font-size:11px;letter-spacing:0.05em;text-transform:uppercase">Bidder {bnum}</th>'

        tbody_html = ""
        for i, pr in enumerate(pivot_rows):
            bg = "background:#fafbfd;" if i % 2 else ""
            uc_vals = [pr[bc] for bc in present_bidder_cols if pr.get(bc) is not None]
            min_uc = min(uc_vals) if uc_vals else None

            proj_label = pr["proj"]
            if len(proj_label) > 32: proj_label = proj_label[:30] + "…"
            desc_label = pr["desc"]
            if len(desc_label) > 55: desc_label = desc_label[:53] + "…"
            proj_cell = f'<span style="font-weight:600;font-size:12px;color:#1a2744">{proj_label}</span>'
            if desc_label:
                proj_cell += f'<br><span style="color:#94a3b8;font-size:10px">{desc_label}</span>'

            tbody_html += f'<tr style="border-bottom:1px solid #f1f5f9;{bg}">'
            tbody_html += f'<td style="padding:9px 14px;font-size:12px">{proj_cell}</td>'
            tbody_html += f'<td style="padding:9px 14px;text-align:center;font-size:12px;color:#94a3b8;font-family:DM Mono,monospace">{pr["yr"]}</td>'

            for bc in present_bidder_cols:
                uc = pr.get(bc)
                is_low = (uc is not None and min_uc is not None
                          and abs(uc - min_uc) < 0.01 and len(uc_vals) > 1)
                if uc is not None:
                    if is_low:
                        uc_s = f'<span style="color:#16a34a;font-weight:700">${uc:,.0f} ★</span>'
                    else:
                        uc_s = f'${uc:,.0f}'
                else:
                    uc_s = '<span style="color:#e2e8f0">—</span>'
                tbody_html += f'<td style="padding:9px 12px;text-align:right;font-size:12px;font-family:DM Mono,monospace;border-left:2px solid #f1f5f9">{uc_s}</td>'
            tbody_html += '</tr>'

        # Footer avg row
        tfoot_html = f'<tr style="background:#f1f5f9;border-top:2px solid #e2e8f0"><td colspan="2" style="padding:9px 14px;font-size:12px;font-weight:700;color:#1a2744">Avg across all projects ({CURRENT_YEAR}$)</td>'
        for bc in present_bidder_cols:
            avg_uc = rows_for_table[bc].dropna().mean()
            avg_uc = round(avg_uc, 2) if pd.notna(avg_uc) else None
            tfoot_html += f'<td style="padding:9px 12px;text-align:right;font-weight:700;font-size:12px;color:#1a2744;border-left:2px solid #e2e8f0;font-family:DM Mono,monospace">{"$"+f"{avg_uc:,.2f}" if avg_uc else "—"}</td>'
        tfoot_html += '</tr>'

        table_html = f"""
        <div style="overflow-x:auto">
          <table class="data-table">
            <thead><tr>{header_html}</tr></thead>
            <tbody>{tbody_html}</tbody>
            <tfoot>{tfoot_html}</tfoot>
          </table>
        </div>
        <div style="font-size:10px;color:#cbd5e1;margin-top:6px">★ = lowest unit cost per project &nbsp;·&nbsp; Raw bid prices shown &nbsp;·&nbsp; Avg unit cost card above is inflation-adjusted to {CURRENT_YEAR}$</div>
        """
        st.markdown(table_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Material Comparison ────────────────────────────────────────────────────
    all_rows = get_rows(df, pt, dia, yr=yr)
    mc = (all_rows.groupby("material", as_index=False)
          .agg(avg=("_cost", "mean"), lo=("_cost", "min"),
               hi=("_cost", "max"), n=("_cost", "count"),
               tabs=("source", "nunique"))
          .sort_values("avg"))
    mc["avg"] = mc["avg"].round(2)
    mc["lo"] = mc["lo"].round(2)
    mc["hi"] = mc["hi"].round(2)

    if len(mc) > 1:
        mat_selected_comp = mat not in ("-- All Materials --", "-- Select Diameter First --")
        cheapest = mc.iloc[0]["avg"]
        yr_label = str(yr) if yr else "All Years"

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="section-label">Material Comparison</div>
        <div style="font-size:12px;color:#64748b;margin-bottom:14px">{dia} &nbsp;·&nbsp; {yr_label} &nbsp;·&nbsp; sorted cheapest first &nbsp;·&nbsp; all costs {CURRENT_YEAR}$</div>
        """, unsafe_allow_html=True)

        mc_html = ""
        for _, r in mc.iterrows():
            sel = mat_selected_comp and (mat == r["material"])
            hl = "background:#f0fdf4;" if sel else ""
            tag = ' <span style="color:#16a34a;font-size:10px;font-weight:700">◀ selected</span>' if sel else ""
            pct = ((r["avg"] - cheapest) / cheapest * 100) if cheapest > 0 else 0
            vs = "cheapest" if pct < 0.5 else f"+{pct:.0f}%"
            vs_color = "#16a34a" if pct < 0.5 else "#f59e0b"
            vs_bold = "font-weight:700;" if pct < 0.5 else ""

            # Bar chart viz
            max_avg = mc["avg"].max()
            bar_pct = int((r["avg"] / max_avg) * 100) if max_avg > 0 else 0
            bar_color = "#16a34a" if pct < 0.5 else "#3b82f6"

            mc_html += f"""
            <tr style="border-bottom:1px solid #f1f5f9;{hl}">
              <td style="padding:10px 14px;font-size:13px;font-weight:{'600' if sel else '400'}">
                {r['material']}{tag}
              </td>
              <td style="padding:10px 14px;text-align:right;font-weight:700;font-family:DM Mono,monospace;color:#1a2744">${r['avg']:,.2f} / LF</td>
              <td style="padding:10px 14px;text-align:right;font-size:11px;color:#94a3b8;font-family:DM Mono,monospace">${r['lo']:,.2f} – ${r['hi']:,.2f}</td>
              <td style="padding:10px 14px;text-align:right;font-size:11px;color:#64748b">{int(r['n'])} bids / {int(r['tabs'])} proj</td>
              <td style="padding:10px 14px;min-width:120px">
                <div style="background:#f1f5f9;border-radius:4px;height:6px;overflow:hidden">
                  <div style="background:{bar_color};width:{bar_pct}%;height:100%;border-radius:4px"></div>
                </div>
              </td>
              <td style="padding:10px 14px;font-size:12px;font-weight:600;color:{vs_color};{vs_bold};text-align:center">{vs}</td>
            </tr>
            """

        st.markdown(f"""
        <div style="overflow-x:auto">
          <table class="data-table" style="width:100%">
            <thead>
              <tr>
                <th>Material</th>
                <th class="right">Avg Unit Cost</th>
                <th class="right">Min – Max</th>
                <th class="right">Bid Data</th>
                <th>Cost Relative</th>
                <th class="center">vs Cheapest</th>
              </tr>
            </thead>
            <tbody>{mc_html}</tbody>
          </table>
        </div>
        <div style="font-size:10px;color:#cbd5e1;margin-top:6px">All costs inflation-adjusted to {CURRENT_YEAR}$. For budgetary planning only.</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── Estimate Summary ───────────────────────────────────────────────────────────
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(f'<div class="section-label">Estimate Summary</div>', unsafe_allow_html=True)

if not st.session_state.line_items:
    st.markdown("""
    <div class="card">
      <div class="empty-state">
        <div class="empty-state-icon">📋</div>
        <div class="empty-state-text">No items added yet.<br>Select a pipe type, diameter, and material, then click <strong>＋ Add to Estimate</strong>.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    rows_html = ""
    for i, li in enumerate(st.session_state.line_items):
        yr_tag = str(li["bid_year"]) if li["bid_year"] else "All"
        f_val = cum_factor(li["bid_year"]) if li["bid_year"] else 1.0
        infl = ""
        if abs(f_val - 1.0) > 0.001:
            infl = f'<br><span class="infl-note">raw ${li["raw"]:,.2f} · {yr_tag}$ ×{f_val:.3f}</span>'

        rows_html += f"""
        <tr>
          <td style="padding:11px 14px;font-size:12px;color:#64748b">{li['pipe_type']}</td>
          <td style="padding:11px 14px;font-weight:700;color:#1a2744">{li['diameter']}</td>
          <td style="padding:11px 14px;font-size:13px">{li['material']}</td>
          <td style="padding:11px 14px;text-align:right;font-family:DM Mono,monospace">{li['qty']:,.0f} LF</td>
          <td style="padding:11px 14px;text-align:right;font-family:DM Mono,monospace">${li['unit_cost']:,.2f}{infl}</td>
          <td style="padding:11px 14px;text-align:center;font-size:11px;color:#64748b">{li['n']} bids / {li['tabs']} proj</td>
          <td style="padding:11px 14px;text-align:right;font-weight:700;color:#16a34a;font-size:15px;font-family:DM Mono,monospace">${li['total']:,.0f}</td>
        </tr>
        """

    grand = sum(li["total"] for li in st.session_state.line_items)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="overflow-x:auto">
      <table class="est-table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Diameter</th>
            <th>Material</th>
            <th class="right">Quantity</th>
            <th class="right">Unit Cost ({CURRENT_YEAR}$)</th>
            <th style="text-align:center">Bid Data</th>
            <th class="right">Item Total</th>
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
        <tfoot>
          <tr>
            <td colspan="6" style="padding:14px;text-align:right;font-size:13px;color:#475569">Total Estimate ({CURRENT_YEAR}$)</td>
            <td style="padding:14px;text-align:right"><span class="grand-total">${grand:,.0f}</span></td>
          </tr>
        </tfoot>
      </table>
    </div>
    <div style="font-size:10px;color:#cbd5e1;margin-top:8px">All costs in {CURRENT_YEAR} dollars. For budgetary planning only. Not for contract use.</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # main-wrapper