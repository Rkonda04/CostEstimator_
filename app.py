import streamlit as st
import pandas as pd
import re
import os
import base64

st.set_page_config(
    page_title="COH Pipe Cost Estimator · Civitas",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Logo loader ────────────────────────────────────────────────────────────────
def get_logo_b64():
    """Try to load civitas_logo.png from common locations and return as base64."""
    for path in [
        "civitas_logo.png",
        os.path.join(os.path.dirname(__file__), "civitas_logo.png"),
        "civitas_logo.png",
    ]:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

LOGO_B64 = get_logo_b64()

def logo_html(height="36px", style=""):
    """Return either the real logo img tag or a text fallback."""
    if LOGO_B64:
        return f'<img src="data:image/png;base64,{LOGO_B64}" style="height:{height};object-fit:contain;{style}" alt="Civitas">'
    # SVG arc fallback matching Civitas brand
    return f'''<svg style="height:{height};{style}" viewBox="0 0 140 44" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M4 36 Q22 4 40 36" stroke="white" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M10 40 Q22 14 34 40" stroke="rgba(255,255,255,0.4)" stroke-width="1.8" fill="none" stroke-linecap="round"/>
      <text x="46" y="30" font-family="sans-serif" font-weight="900" font-size="22" fill="white" letter-spacing="-0.5">civitas</text>
      <text x="47" y="41" font-family="sans-serif" font-weight="500" font-size="8" fill="rgba(255,255,255,0.45)" letter-spacing="3">ENGINEERING GROUP</text>
    </svg>'''

# ══════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM CSS
# Aesthetic: Refined luxury engineering tool. Dark purple navy header, cream/
# warm-white content area, generous whitespace, editorial typography.
# Distinctive: DM Serif Display for hero numbers, Outfit for UI, Mono for data.
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  /* Civitas Brand */
  --p0:  #1c0945;   /* deepest navy-purple */
  --p1:  #2e1470;   /* dark purple */
  --p2:  #5b2d8e;   /* brand purple */
  --p3:  #7c4ab8;   /* mid purple */
  --p4:  #a878e0;   /* light purple */
  --p5:  #d4b8f8;   /* pale purple */
  --p6:  #f0eaff;   /* ghost purple */
  --p7:  #f9f6ff;   /* near white purple */

  /* Warm neutrals */
  --bg:       #f5f4f7;
  --bg2:      #edeaf2;
  --surface:  #ffffff;
  --border:   #e4dff0;
  --border2:  #cfc8e8;

  /* Text */
  --t0:  #120630;
  --t1:  #2e1470;
  --t2:  #5a4880;
  --t3:  #8a7aaa;
  --t4:  #b8add0;

  /* Accent */
  --gold:    #c8880a;
  --gold-lt: #fdf3dc;
  --gold-bd: #f0d080;
  --teal:    #0e9070;
  --teal-lt: #d6f5ee;

  /* Type */
  --serif: 'DM Serif Display', Georgia, serif;
  --ui:    'Outfit', sans-serif;
  --mono:  'JetBrains Mono', monospace;

  /* Tokens */
  --radius:    16px;
  --radius-sm: 10px;
  --radius-xs: 6px;
  --shadow-xs: 0 1px 3px rgba(28,9,69,0.06);
  --shadow-sm: 0 2px 8px rgba(28,9,69,0.08), 0 6px 20px rgba(28,9,69,0.05);
  --shadow-md: 0 4px 16px rgba(28,9,69,0.10), 0 12px 36px rgba(28,9,69,0.08);
  --shadow-lg: 0 8px 32px rgba(28,9,69,0.14), 0 24px 64px rgba(28,9,69,0.10);
}

/* ── Reset ── */
html, body, [class*="css"], .stApp {
  font-family: var(--ui) !important;
  background: var(--bg) !important;
  color: var(--t0) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }
* { box-sizing: border-box; }

/* ══════════════════════════════════════════
   HEADER
══════════════════════════════════════════ */
.civ-header {
  background: var(--p0);
  height: 66px;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 40px;
  position: sticky; top: 0; z-index: 1000;
  box-shadow: 0 1px 0 rgba(255,255,255,0.06), 0 4px 24px rgba(0,0,0,0.35);
}
.civ-header-logo { display: flex; align-items: center; }
.civ-header-center { display: flex; flex-direction: column; align-items: center; }
.civ-header-app-name {
  font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.92);
  letter-spacing: 0.01em;
}
.civ-header-app-sub {
  font-size: 10px; color: rgba(255,255,255,0.38);
  letter-spacing: 0.12em; text-transform: uppercase; margin-top: 1px;
}
.civ-header-right { display: flex; align-items: center; gap: 8px; }
.hpill {
  padding: 4px 12px; border-radius: 20px;
  font-size: 10px; font-weight: 600; font-family: var(--mono);
  letter-spacing: 0.04em; border: 1px solid;
}
.hpill-dim { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.12); color: rgba(255,255,255,0.55); }
.hpill-gold { background: rgba(200,136,10,0.15); border-color: rgba(200,136,10,0.35); color: #f0c040; }
.civ-rule { height: 2px; background: linear-gradient(90deg, var(--p1) 0%, var(--p3) 40%, var(--p4) 60%, var(--p1) 100%); }

/* ══════════════════════════════════════════
   HOME — HERO
══════════════════════════════════════════ */
.hero {
  background: var(--p1);
  position: relative; overflow: hidden;
  padding: 72px 24px 64px;
  text-align: center;
}
/* geometric texture */
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background-image:
    radial-gradient(circle at 15% 50%, rgba(124,74,184,0.25) 0%, transparent 50%),
    radial-gradient(circle at 85% 20%, rgba(91,45,142,0.2) 0%, transparent 40%),
    radial-gradient(circle at 50% 100%, rgba(168,120,224,0.12) 0%, transparent 50%);
  pointer-events: none;
}
/* grid lines */
.hero::after {
  content: '';
  position: absolute; inset: 0;
  background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
}
.hero-inner { position: relative; z-index: 1; max-width: 680px; margin: 0 auto; }
.hero-eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
  border-radius: 20px; padding: 5px 16px; margin-bottom: 24px;
  font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.6);
  letter-spacing: 0.12em; text-transform: uppercase; font-family: var(--mono);
}
.hero-eyebrow-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--p4); }
.hero h1 {
  font-family: var(--serif);
  font-size: 52px; font-weight: 400; color: white;
  line-height: 1.1; letter-spacing: -0.02em;
  margin: 0 0 16px;
}
.hero h1 em { font-style: italic; color: var(--p5); }
.hero-sub {
  font-size: 16px; color: rgba(255,255,255,0.5);
  line-height: 1.7; margin: 0 auto 36px; max-width: 480px;
  font-weight: 400;
}
.hero-cta {
  display: inline-flex; align-items: center; gap: 10px;
  background: white; color: var(--p1);
  font-size: 14px; font-weight: 700;
  padding: 14px 32px; border-radius: 50px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2), 0 0 0 1px rgba(255,255,255,0.1);
  cursor: pointer; text-decoration: none;
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  font-family: var(--ui);
}
.hero-cta:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 8px 30px rgba(0,0,0,0.25); }
.hero-cta-arrow { font-size: 16px; transition: transform 0.2s; }
.hero-cta:hover .hero-cta-arrow { transform: translateX(4px); }

/* data ribbon under hero */
.hero-ribbon {
  background: rgba(255,255,255,0.05); border-top: 1px solid rgba(255,255,255,0.08);
  padding: 16px 24px; display: flex; justify-content: center; gap: 0;
  position: relative; z-index: 1;
}
.ribbon-stat {
  padding: 0 32px; text-align: center;
  border-right: 1px solid rgba(255,255,255,0.1);
}
.ribbon-stat:last-child { border-right: none; }
.ribbon-num {
  font-family: var(--mono); font-size: 20px; font-weight: 600;
  color: white; line-height: 1;
}
.ribbon-lbl { font-size: 10px; color: rgba(255,255,255,0.38); margin-top: 4px; letter-spacing: 0.08em; text-transform: uppercase; }

/* ══════════════════════════════════════════
   HOME CARDS
══════════════════════════════════════════ */
.home-wrap { max-width: 780px; margin: 0 auto; padding: 48px 24px 80px; }
.home-section { margin-bottom: 20px; animation: fadeUp 0.5s ease both; }
@keyframes fadeUp { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:translateY(0); } }
.home-section:nth-child(1) { animation-delay: 0.05s; }
.home-section:nth-child(2) { animation-delay: 0.12s; }
.home-section:nth-child(3) { animation-delay: 0.19s; }
.home-section:nth-child(4) { animation-delay: 0.26s; }

.home-card {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 30px 32px;
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  position: relative; overflow: hidden;
}
/* accent stripe */
.home-card::before {
  content: '';
  position: absolute; left: 0; top: 0; bottom: 0;
  width: 4px; background: linear-gradient(180deg, var(--p3), var(--p4));
  border-radius: 4px 0 0 4px;
}
.hc-title {
  font-family: var(--serif); font-size: 22px; font-weight: 400;
  color: var(--p2); margin: 0 0 16px; letter-spacing: -0.01em;
}
.hc-body { font-size: 14px; color: var(--t2); line-height: 1.7; margin: 0 0 14px; }
.hc-list { list-style: none; margin: 0; padding: 0; }
.hc-list li {
  font-size: 14px; color: var(--t2); padding: 6px 0;
  display: flex; align-items: flex-start; gap: 10px; line-height: 1.55;
  border-bottom: 1px solid var(--bg2);
}
.hc-list li:last-child { border-bottom: none; }
.hc-bullet {
  width: 18px; height: 18px; border-radius: 50%;
  background: var(--p6); display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; margin-top: 1px;
}
.hc-bullet::after { content: ''; width: 6px; height: 6px; border-radius: 50%; background: var(--p3); }

/* stat pills on home */
.stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 20px; }
.stat-pill {
  background: var(--p7); border: 1px solid var(--p6);
  border-radius: 10px; padding: 12px 20px; text-align: center; flex: 1; min-width: 100px;
}
.stat-pill-n { font-family: var(--mono); font-size: 22px; font-weight: 600; color: var(--p2); }
.stat-pill-l { font-size: 10px; color: var(--t3); margin-top: 3px; letter-spacing: 0.06em; text-transform: uppercase; }

/* step cards for quickstart */
.step-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 4px; }
.step-item {
  background: var(--p7); border-radius: 10px; padding: 14px 16px;
  display: flex; gap: 12px; align-items: flex-start;
  border: 1px solid var(--p6);
}
.step-num {
  width: 26px; height: 26px; border-radius: 50%;
  background: var(--p2); color: white;
  font-size: 12px; font-weight: 700; font-family: var(--mono);
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.step-text { font-size: 13px; color: var(--t1); line-height: 1.5; }
.step-text strong { color: var(--p2); }

/* ══════════════════════════════════════════
   ESTIMATOR — PIPE TYPE BUTTONS
══════════════════════════════════════════ */
.stButton > button {
  font-family: var(--ui) !important;
  font-weight: 600 !important; font-size: 13px !important;
  border-radius: 50px !important;
  padding: 9px 20px !important;
  transition: all 0.18s cubic-bezier(0.34, 1.4, 0.64, 1) !important;
  letter-spacing: 0.01em !important;
}
.stButton > button[kind="primary"] {
  background: var(--p2) !important; border: none !important;
  color: white !important;
  box-shadow: 0 4px 14px rgba(91,45,142,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
  background: var(--p1) !important;
  box-shadow: 0 6px 20px rgba(91,45,142,0.45) !important;
  transform: translateY(-2px) !important;
}
.stButton > button[kind="secondary"] {
  background: var(--surface) !important;
  border: 1.5px solid var(--border2) !important;
  color: var(--t2) !important; box-shadow: var(--shadow-xs) !important;
}
.stButton > button[kind="secondary"]:hover {
  border-color: var(--p3) !important; color: var(--p2) !important;
  background: var(--p7) !important;
  box-shadow: 0 4px 14px rgba(91,45,142,0.12) !important;
}

/* ══════════════════════════════════════════
   ESTIMATOR — CARDS & SURFACE
══════════════════════════════════════════ */
.e-card {
  background: var(--surface);
  border-radius: var(--radius); padding: 24px 28px;
  border: 1px solid var(--border); box-shadow: var(--shadow-sm);
  margin-bottom: 16px;
  animation: fadeUp 0.4s ease both;
}
.e-card-label {
  font-size: 10px; font-weight: 700; letter-spacing: 0.14em;
  text-transform: uppercase; color: var(--t3); margin-bottom: 16px;
  padding-bottom: 12px; border-bottom: 1px solid var(--bg2);
}

/* ══════════════════════════════════════════
   COST HERO CARD — Glassmorphism purple
══════════════════════════════════════════ */
.cost-card {
  background: linear-gradient(145deg, var(--p0) 0%, var(--p1) 40%, #3d1d80 100%);
  border-radius: var(--radius);
  padding: 28px 30px;
  color: white; position: relative; overflow: hidden;
  box-shadow: var(--shadow-lg);
  border: 1px solid rgba(255,255,255,0.08);
  margin-bottom: 16px;
  animation: fadeUp 0.4s ease both;
}
/* glass shimmer */
.cost-card::before {
  content: '';
  position: absolute; top: -80px; right: -80px;
  width: 260px; height: 260px; border-radius: 50%;
  background: radial-gradient(circle, rgba(168,120,224,0.18) 0%, transparent 65%);
  pointer-events: none;
}
.cost-card::after {
  content: '';
  position: absolute; bottom: -40px; left: 30px;
  width: 160px; height: 160px; border-radius: 50%;
  background: radial-gradient(circle, rgba(14,144,112,0.1) 0%, transparent 65%);
  pointer-events: none;
}
/* subtle dot grid */
.cost-card-grid {
  position: absolute; inset: 0;
  background-image: radial-gradient(rgba(255,255,255,0.06) 1px, transparent 1px);
  background-size: 24px 24px;
  pointer-events: none;
}
.cc-inner { position: relative; z-index: 1; }
.cc-context {
  font-family: var(--mono); font-size: 9px; font-weight: 500;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: rgba(255,255,255,0.32); margin-bottom: 12px;
}
.cc-label {
  font-size: 11px; font-weight: 500; color: rgba(255,255,255,0.45);
  margin-bottom: 6px; letter-spacing: 0.04em;
}
.cc-amount {
  font-family: var(--serif); font-size: 58px; font-weight: 400;
  color: white; line-height: 1; letter-spacing: -0.02em;
}
.cc-per { font-size: 18px; font-style: italic; color: rgba(255,255,255,0.4); margin-left: 6px; }
.cc-range {
  font-family: var(--mono); font-size: 11px; color: rgba(255,255,255,0.3);
  margin-top: 8px;
}
.cc-sep { border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 18px 0; }
.cc-total-lbl { font-size: 10px; color: rgba(255,255,255,0.38); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 5px; }
.cc-total-amt {
  font-family: var(--serif); font-size: 36px; font-weight: 400;
  color: #a0ffcc; letter-spacing: -0.01em;
}
.cc-infl-box {
  margin-top: 14px; padding: 10px 14px; border-radius: 10px;
  font-size: 11px; font-family: var(--mono); line-height: 1.55;
}
.cc-infl-future { background: rgba(200,136,10,0.14); border: 1px solid rgba(200,136,10,0.28); color: #f0c040; }
.cc-infl-hist   { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.09); color: rgba(255,255,255,0.32); }
.cc-chips { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 16px; }
.cc-chip {
  padding: 5px 12px; border-radius: 20px; font-size: 11px;
  background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12);
  color: rgba(255,255,255,0.5); font-family: var(--mono);
}
.cc-chip strong { color: rgba(255,255,255,0.9); }
.cc-empty {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; min-height: 260px; gap: 14px;
}
.cc-empty-icon { font-size: 48px; opacity: 0.18; }
.cc-empty-text { font-size: 14px; color: rgba(255,255,255,0.25); text-align: center; line-height: 1.7; font-style: italic; }

/* ══════════════════════════════════════════
   FUTURE BANNER
══════════════════════════════════════════ */
.fut-banner {
  background: var(--gold-lt); border: 1px solid var(--gold-bd);
  border-left: 4px solid var(--gold);
  border-radius: var(--radius-sm); padding: 12px 18px;
  font-size: 13px; color: #4a2e00; line-height: 1.65; margin-bottom: 14px;
}
.fut-banner strong { color: #2e1a00; }

/* ══════════════════════════════════════════
   SECTION DIVIDERS
══════════════════════════════════════════ */
.sec-div { display: flex; align-items: center; gap: 16px; margin: 32px 0 20px; }
.sec-div-line { flex: 1; height: 1px; background: var(--border); }
.sec-div-lbl {
  font-size: 10px; font-weight: 700; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--p3);
  padding: 5px 18px; background: var(--p7);
  border-radius: 20px; border: 1px solid var(--p6); white-space: nowrap;
}

/* ══════════════════════════════════════════
   TABLES
══════════════════════════════════════════ */
.tbl-wrap { overflow-x: auto; border-radius: var(--radius-sm); border: 1px solid var(--border); }
.civ-tbl { width: 100%; border-collapse: collapse; font-size: 13px; font-family: var(--ui); }
.civ-tbl thead th {
  background: var(--p0); padding: 12px 16px;
  color: rgba(255,255,255,0.75); font-size: 10px; font-weight: 600;
  letter-spacing: 0.12em; text-transform: uppercase; text-align: left; white-space: nowrap;
}
.civ-tbl thead th.r { text-align: right; }
.civ-tbl thead th.c { text-align: center; }
.civ-tbl tbody tr { border-bottom: 1px solid var(--bg2); transition: background 0.1s; }
.civ-tbl tbody tr:hover { background: var(--p7); }
.civ-tbl tbody tr:last-child { border-bottom: none; }
.civ-tbl td { padding: 11px 16px; color: var(--t0); vertical-align: middle; }
.civ-tbl td.r { text-align: right; font-family: var(--mono); }
.civ-tbl td.c { text-align: center; }
.civ-tbl tfoot tr { background: var(--p7); border-top: 2px solid var(--p6); }
.civ-tbl tfoot td { padding: 12px 16px; font-weight: 700; color: var(--p1); font-size: 13px; }
.civ-tbl tfoot td.r { text-align: right; font-family: var(--mono); }
.tag-low {
  display: inline-block; background: var(--teal-lt); color: var(--teal);
  font-size: 9px; font-weight: 700; padding: 1px 6px; border-radius: 4px;
  margin-left: 5px; font-family: var(--mono); letter-spacing: 0.04em;
}
.star-low { color: var(--teal); font-weight: 700; }
.dash-nil { color: var(--t4); }
.bh-col { border-left: 2px solid rgba(255,255,255,0.1) !important; }
.proj-name { font-weight: 600; color: var(--t1); }
.proj-desc { color: var(--t4); font-size: 11px; margin-top: 2px; }
.mat-sel-row td { background: #f0fdf8 !important; }
.bar-bg { background: var(--bg2); border-radius: 4px; height: 6px; overflow: hidden; min-width: 80px; }
.bar-fill { height: 100%; border-radius: 4px; }
.vs-low  { color: var(--teal); font-weight: 700; font-size: 12px; }
.vs-high { color: var(--gold); font-weight: 600; font-size: 12px; }

/* ══════════════════════════════════════════
   ESTIMATE SUMMARY
══════════════════════════════════════════ */
.grand-ttl { font-family: var(--serif); font-size: 28px; color: var(--teal); }
.yr-fut  { display:inline-block; background:var(--gold-lt); color:#6a3a00; border:1px solid var(--gold-bd); font-size:10px; font-weight:700; padding:2px 8px; border-radius:5px; font-family:var(--mono); }
.yr-hist { display:inline-block; background:var(--p7); color:var(--p2); border:1px solid var(--p6); font-size:10px; font-weight:600; padding:2px 8px; border-radius:5px; font-family:var(--mono); }
.proj-note { font-size:10px; color:var(--gold); font-family:var(--mono); font-weight:600; }
.base-note { font-size:10px; color:var(--t4); font-family:var(--mono); }

/* ══════════════════════════════════════════
   EMPTY STATE
══════════════════════════════════════════ */
.empty-box { text-align:center; padding:56px 24px; }
.empty-icon { font-size:48px; margin-bottom:14px; opacity:0.22; }
.empty-text { font-size:14px; color:var(--t3); line-height:1.8; font-style:italic; }

/* ══════════════════════════════════════════
   FOOTER
══════════════════════════════════════════ */
.civ-footer {
  background: var(--p0); padding: 22px 40px;
  text-align: center; font-family: var(--mono);
  font-size: 11px; color: rgba(255,255,255,0.28);
  letter-spacing: 0.05em;
}
.civ-footer strong { color: rgba(255,255,255,0.6); }

/* ══════════════════════════════════════════
   STREAMLIT OVERRIDES
══════════════════════════════════════════ */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
  font-family: var(--ui) !important; font-size: 10px !important;
  font-weight: 700 !important; letter-spacing: 0.1em !important;
  text-transform: uppercase !important; color: var(--t3) !important;
}
div[data-testid="stSelectbox"] > div > div {
  border: 1.5px solid var(--border) !important; border-radius: 10px !important;
  font-family: var(--ui) !important; font-size: 14px !important;
  background: var(--surface) !important; box-shadow: var(--shadow-xs) !important;
  transition: border-color 0.15s, box-shadow 0.15s !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within {
  border-color: var(--p3) !important;
  box-shadow: 0 0 0 3px rgba(91,45,142,0.12) !important;
}
div[data-testid="stNumberInput"] input {
  border: 1.5px solid var(--border) !important; border-radius: 10px !important;
  font-family: var(--mono) !important; font-size: 15px !important;
  color: var(--t1) !important; font-weight: 600 !important;
  padding: 10px 14px !important; background: var(--surface) !important;
  box-shadow: var(--shadow-xs) !important;
  transition: border-color 0.15s, box-shadow 0.15s !important;
}
div[data-testid="stNumberInput"] input:focus {
  border-color: var(--p3) !important;
  box-shadow: 0 0 0 3px rgba(91,45,142,0.12) !important;
}
div[data-testid="stAlert"] { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
CURRENT_YEAR        = 2026
PROJECTION_END_YEAR = 2050
INFLATION_RATES = {
    2021: 0.0470, 2022: 0.0800, 2023: 0.0410,
    2024: 0.0295, 2025: 0.0268,
    2026: 0.0270, 2027: 0.0240, 2028: 0.0230, 2029: 0.0200,
    **{yr: 0.0200 for yr in range(2030, PROJECTION_END_YEAR + 1)},
}
PIPE_TYPES = ["Waterline", "Gravity Main", "Force Main"]
PIPE_ICONS = {"Waterline": "🚰", "Gravity Main": "🏗️", "Force Main": "⚡"}
BID_COLORS = ["#1c0945","#2e1470","#1a3a6b","#0e6050","#5c3a1a","#4a0a5c"]

for k, v in [("page","home"),("line_items",[]),("pipe_type","Waterline")]:
    if k not in st.session_state: st.session_state[k] = v

# ── Math ───────────────────────────────────────────────────────────────────────
def cum_factor(from_year):
    if from_year >= CURRENT_YEAR: return 1.0
    f = 1.0
    for yr in range(int(from_year)+1, CURRENT_YEAR+1):
        f *= (1 + INFLATION_RATES.get(yr, 0.0))
    return round(f, 4)

def future_factor(target_year):
    if target_year <= CURRENT_YEAR: return 1.0
    f = 1.0
    for yr in range(CURRENT_YEAR+1, int(target_year)+1):
        f *= (1 + INFLATION_RATES.get(yr, 0.0200))
    return round(f, 4)

def sort_dia(vals):
    return sorted(vals, key=lambda d: int(re.search(r'\d+',str(d)).group())
                  if re.search(r'\d+',str(d)) else 9999)

# ── Data ───────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    csv_path = None
    for p in ["Data/pipe_items1.csv","pipe_items1.csv"]:
        if os.path.exists(p): csv_path=p; break
    try:
        alt = os.path.join(os.path.dirname(__file__),"Data","pipe_items1.csv")
        if not csv_path and os.path.exists(alt): csv_path=alt
    except: pass
    if not csv_path: return None,None,None,None

    df = pd.read_csv(csv_path, dtype=str)
    df["_cost_raw"] = pd.to_numeric(df["unit_cost"], errors="coerce") \
                      if "unit_cost" in df.columns else pd.Series(float("nan"), index=df.index)
    bidder_cols = sorted([c for c in df.columns if re.match(r'unit_cost_bidder\d+',c)],
                         key=lambda c: int(re.search(r'\d+',c).group()))
    for bc in bidder_cols: df[bc] = pd.to_numeric(df[bc], errors="coerce")
    if df["_cost_raw"].isna().all() and bidder_cols:
        df["_cost_raw"] = df[bidder_cols].mean(axis=1, skipna=True)
    if "unit" in df.columns:
        df = df[df["unit"].str.strip().str.upper()=="LF"]
    df = df.dropna(subset=["_cost_raw"])
    df = df[df["_cost_raw"]>0].copy()
    yc = next((c for c in ["YEAR","year"] if c in df.columns), None)
    df["YEAR"] = pd.to_numeric(df[yc], errors="coerce") if yc else float("nan")
    if "source" not in df.columns: df["source"]="Unknown"
    def ainf(row):
        yr=row["YEAR"]
        return row["_cost_raw"] if pd.isna(yr) else round(row["_cost_raw"]*cum_factor(int(yr)),2)
    df["_cost"] = df.apply(ainf, axis=1)
    hist = sorted([int(y) for y in df["YEAR"].dropna().unique() if 2010<=int(y)<=2030])
    # Full 2026→2050 range confirmed
    all_y = sorted(set(hist)|set(range(CURRENT_YEAR, PROJECTION_END_YEAR+1)))
    return df, bidder_cols, hist, all_y

def qrows(df,hist,pt,dia,mat=None,yr=None):
    m=(df["pipe_type"]==pt)&(df["diameter"]==dia)
    if mat and mat not in("-- All Materials --","-- Select Diameter First --"):
        m&=(df["material"]==mat)
    if yr is not None and hist and yr in hist:
        m2=m&(df["YEAR"]==yr)
        if not df[m2].empty: return df[m2]
    return df[m]

def qstats(rows):
    if rows.empty: return {}
    c=rows["_cost"].dropna()
    return {"avg":round(c.mean(),2),"lo":round(c.min(),2),"hi":round(c.max(),2),
            "n":len(c),"tabs":rows["source"].nunique()}

def qdiam(df,pt):
    return ["-- Select --"]+sort_dia(df[df["pipe_type"]==pt]["diameter"].dropna().unique())

def qmat(df,hist,pt,dia,yr=None):
    m=(df["pipe_type"]==pt)&(df["diameter"]==dia)
    if yr is not None and hist and yr in hist:
        m2=m&(df["YEAR"]==yr)
        if df[m2]["material"].dropna().any(): m=m2
    return ["-- All Materials --"]+sorted(df[m]["material"].dropna().unique())

def yrint(val):
    if val=="All Years": return None
    m=re.search(r'\d{4}',str(val))
    return int(m.group()) if m else None

df, bidder_cols, hist, all_y = load_data()

# ── Shared header ──────────────────────────────────────────────────────────────
def render_header(show_nav=True):
    nav = f'''
      <div class="civ-header-right">
        <span class="hpill hpill-dim">Base {CURRENT_YEAR}$</span>
        <span class="hpill hpill-gold">📈 → {PROJECTION_END_YEAR}</span>
      </div>''' if show_nav else '<div></div>'
    center = '''
      <div class="civ-header-center">
        <div class="civ-header-app-name">COH Pipe Cost Estimator</div>

      </div>''' if show_nav else '<div></div>'
    st.markdown(f"""
    <div class="civ-header">
      <div class="civ-header-logo">{logo_html(height="38px")}</div>
      {center}
      {nav}
    </div>
    <div class="civ-rule"></div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    render_header(show_nav=False)

    n_rows = len(df) if df is not None else 0
    n_proj = df["source"].nunique() if df is not None else 0
    hist_r = f"{min(hist)}–{max(hist)}" if hist else "—"

    st.markdown(f"""
    <div class="hero">
      <div class="hero-inner">
        <div class="hero-eyebrow">
          <div class="hero-eyebrow-dot"></div>
          Civitas Engineering Group &nbsp; 
        </div>
        <h1>Pipe Unit Cost<br><em>Estimator</em></h1>
       
      </div>
      <div class="hero-ribbon">
        <div class="ribbon-stat">
          <div class="ribbon-num">{n_rows:,}</div>
          <div class="ribbon-lbl">LF Bid Rows</div>
        </div>
        <div class="ribbon-stat">
          <div class="ribbon-num">{n_proj}</div>
          <div class="ribbon-lbl">Source Projects</div>
        </div>
        <div class="ribbon-stat">
          <div class="ribbon-num">{hist_r}</div>
          <div class="ribbon-lbl">Historical Range</div>
        </div>
        <div class="ribbon-stat">
          <div class="ribbon-num">{CURRENT_YEAR}–{PROJECTION_END_YEAR}</div>
          <div class="ribbon-lbl">Projection Window</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Launch button
    _, mid, _ = st.columns([2.5, 1, 2.5])
    with mid:
        st.markdown("<div style='margin-top:-1px'>", unsafe_allow_html=True)
        if st.button("Launch Estimator  →", type="primary", use_container_width=True):
            st.session_state.page = "estimator"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="home-wrap">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="home-section">
      <div class="home-card">
        <div class="hc-title">What this tool does</div>
        <ul class="hc-list">
          <li><div class="hc-bullet"></div>Look up average, min, and max unit costs ($/LF) for waterline, gravity main, and force main pipe</li>
          <li><div class="hc-bullet"></div>Filter by pipe <strong>diameter</strong>, <strong>material</strong>, and <strong>bid year</strong> from real Houston-area bid tab data</li>
          <li><div class="hc-bullet"></div>All historical costs automatically normalized to <strong>{CURRENT_YEAR} dollars</strong> using actual CPI rates</li>
          <li><div class="hc-bullet"></div>Project costs forward to any year through <strong>{PROJECTION_END_YEAR}</strong> using ENR escalation rates</li>
          <li><div class="hc-bullet"></div>Build a multi-line estimate and view your total with inflation notes</li>
        </ul>
        <div class="stat-row">
          <div class="stat-pill"><div class="stat-pill-n">{n_rows:,}</div><div class="stat-pill-l">LF bid rows</div></div>
          <div class="stat-pill"><div class="stat-pill-n">{n_proj}</div><div class="stat-pill-l">projects</div></div>
          <div class="stat-pill"><div class="stat-pill-n">{hist_r}</div><div class="stat-pill-l">data years</div></div>
          <div class="stat-pill"><div class="stat-pill-n">→ {PROJECTION_END_YEAR}</div><div class="stat-pill-l">project to</div></div>
        </div>
      </div>
    </div>

    <div class="home-section">
      <div class="home-card">
        <div class="hc-title">Who it's for</div>
        <ul class="hc-list">
          <li><div class="hc-bullet"></div>Civitas project engineers estimating waterline and pipe construction costs</li>
          <li><div class="hc-bullet"></div>City of Houston project managers reviewing CIP budget estimates</li>
          <li><div class="hc-bullet"></div>Planners needing a quick sanity check on pipe unit costs by material and diameter</li>
          <li><div class="hc-bullet"></div>Anyone forecasting what today's costs will look like in a future bid year</li>
        </ul>
      </div>
    </div>

    <div class="home-section">
      <div class="home-card">
        <div class="hc-title">Quick start</div>
        <div class="step-grid">
          <div class="step-item"><div class="step-num">1</div><div class="step-text">Choose a <strong>pipe type</strong> — Waterline, Gravity Main, or Force Main</div></div>
          <div class="step-item"><div class="step-num">2</div><div class="step-text">Select a <strong>diameter</strong> and <strong>material</strong> from the dropdowns</div></div>
          <div class="step-item"><div class="step-num">3</div><div class="step-text">Pick a <strong>bid year</strong> — historic to filter data, or future to project costs to {PROJECTION_END_YEAR}</div></div>
          <div class="step-item"><div class="step-num">4</div><div class="step-text">Enter a <strong>quantity</strong> and click <strong>＋ Add to Estimate</strong> to build your total</div></div>
        </div>
      </div>
    </div>

    <div class="home-section">
      <div class="home-card">
        <div class="hc-title">How costs are calculated</div>
        <ul class="hc-list">
          <li><div class="hc-bullet"></div><strong>Historic normalization:</strong> all historical bids inflated to {CURRENT_YEAR}$ using actual annual CPI rates</li>
          <li><div class="hc-bullet"></div><strong>Future projection:</strong> {CURRENT_YEAR}$ costs escalated forward using ENR-based rates (2.0%/yr after 2029)</li>
          <li><div class="hc-bullet"></div><strong>Unit cost shown:</strong> average across all matching LF rows; min/max range displayed for context</li>
          <li><div class="hc-bullet"></div>For budgetary planning only.</li>
        </ul>
      </div>
    </div>
    """, unsafe_allow_html=True)

    _, mid2, _ = st.columns([2.5, 1, 2.5])
    with mid2:
        if st.button("Launch Estimator  → ", type="primary", use_container_width=True):
            st.session_state.page = "estimator"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="civ-footer"><strong>Civitas Engineering Group, Inc.</strong> &nbsp;&nbsp; &nbsp;·&nbsp; Base Year {CURRENT_YEAR} &nbsp;·&nbsp; ENR Escalation → {PROJECTION_END_YEAR} &nbsp;·&nbsp; For Budgetary Planning Only</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ESTIMATOR PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "estimator":
    render_header(show_nav=True)

    if df is None:
        st.error("⚠️  `pipe_items1.csv` not found. Place it in `Data/pipe_items1.csv` next to `app.py`.")
        st.stop()

    st.markdown('<div style="max-width:1100px;margin:0 auto;padding:28px 24px 64px">', unsafe_allow_html=True)

    # Back + pipe type row
    back_col, *pt_cols = st.columns([0.42]+[1]*len(PIPE_TYPES))
    with back_col:
        if st.button("← Home", type="secondary", use_container_width=True):
            st.session_state.page="home"; st.rerun()
    for i, pt_opt in enumerate(PIPE_TYPES):
        with pt_cols[i]:
            active = st.session_state.pipe_type==pt_opt
            if st.button(f"{PIPE_ICONS[pt_opt]}  {pt_opt}", key=f"pt_{pt_opt}",
                         type="primary" if active else "secondary", use_container_width=True):
                st.session_state.pipe_type=pt_opt; st.rerun()

    st.markdown("<div style='margin-bottom:20px'></div>", unsafe_allow_html=True)
    pt = st.session_state.pipe_type

    col_l, col_r = st.columns([1.35, 1], gap="large")

    with col_l:
        st.markdown('<div class="e-card"><div class="e-card-label">Selection Filters</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: dia = st.selectbox("Diameter", qdiam(df,pt), key="dia")
        with c2: yr_raw = st.selectbox(f"Bid Year (up to {PROJECTION_END_YEAR})",
                                        ["All Years"]+[str(y) for y in all_y], key="yr")
        yr        = yrint(yr_raw)
        is_fut    = yr is not None and yr > CURRENT_YEAR
        is_hist   = yr is not None and hist and yr in hist
        c3, c4 = st.columns(2)
        with c3:
            mopts = ["-- Select Diameter First --"] if dia=="-- Select --" else qmat(df,hist,pt,dia,yr)
            mat = st.selectbox("Material", mopts, key="mat")
        with c4:
            qty = st.number_input("Quantity (LF)", min_value=0.0, max_value=9_999_999.0,
                                  value=1000.0, step=100.0, key="qty")
        st.markdown('</div>', unsafe_allow_html=True)

        if is_fut:
            ff_i=future_factor(yr); pct_i=(ff_i-1)*100; yrs_o=yr-CURRENT_YEAR
            st.markdown(f'<div class="fut-banner">📅 <strong>Future Year: {yr}</strong> — Projecting from {CURRENT_YEAR}$ using ENR escalation. Multiplier: <strong>&times;{ff_i:.4f}</strong> (+{pct_i:.1f}% over {yrs_o} yr{"s" if yrs_o!=1 else ""}). Historical bid table shows raw prices.</div>', unsafe_allow_html=True)

        ba, bb, _ = st.columns([1.5,1,1])
        with ba: add_click = st.button("＋ Add to Estimate", type="primary", use_container_width=True)
        with bb:
            if st.button("🗑 Clear All", type="secondary", use_container_width=True):
                st.session_state.line_items=[]; st.rerun()

    with col_r:
        rows    = qrows(df,hist,pt,dia,mat,yr) if dia!="-- Select --" else pd.DataFrame()
        s       = qstats(rows)
        mat_sel = mat not in("-- All Materials --","-- Select Diameter First --")
        ff      = future_factor(yr) if is_fut else 1.0
        du      = round(s["avg"]*ff,2) if s else 0
        dlo     = round(s["lo"]*ff,2)  if s else 0
        dhi     = round(s["hi"]*ff,2)  if s else 0
        tot     = round(du*qty,0) if s and mat_sel and qty>0 else None
        dy      = yr if yr else CURRENT_YEAR

        if dia=="-- Select --" or not s:
            icon = "📐" if dia=="-- Select --" else "🔍"
            msg  = "Select a diameter to view unit costs" if dia=="-- Select --" else "No data for this selection —<br>try adjusting the filters."
            st.markdown(f'<div class="cost-card"><div class="cost-card-grid"></div><div class="cc-inner"><div class="cc-empty"><div class="cc-empty-icon">{icon}</div><div class="cc-empty-text">{msg}</div></div></div></div>', unsafe_allow_html=True)
        else:
            ctx = f"{pt}  ·  {mat if mat_sel else 'All Materials'}  ·  {'All Years' if not yr else yr}"
            if is_fut:
                infl = f'<div class="cc-infl-box cc-infl-future">📈 Base {CURRENT_YEAR}$ avg: <strong>${s["avg"]:,.2f}/LF</strong> &times; {ff:.4f} (+{(ff-1)*100:.1f}% over {yr-CURRENT_YEAR} yrs) → <strong>${du:,.2f}/LF in {yr}$</strong></div>'
            elif is_hist:
                fv=cum_factor(yr)
                infl = f'<div class="cc-infl-box cc-infl-hist">Bids from {yr} normalized &times;{fv:.4f} (+{(fv-1)*100:.1f}%) → {CURRENT_YEAR}$</div>'
            else: infl=""
            tot_html = f'<hr class="cc-sep"><div class="cc-total-lbl">{qty:,.0f} LF &times; ${du:,.2f} &nbsp;→&nbsp; Estimated Total</div><div class="cc-total-amt">${tot:,.0f}</div>' if tot else ""

            st.markdown(f"""
            <div class="cost-card">
              <div class="cost-card-grid"></div>
              <div class="cc-inner">
                <div class="cc-context">{ctx.upper()}</div>
                <div class="cc-label">{'Projected' if is_fut else 'Average'} Unit Cost ({dy}$)</div>
                <div class="cc-amount">${du:,.2f}<span class="cc-per">/ LF</span></div>
                <div class="cc-range">Min ${dlo:,.2f} &nbsp;–&nbsp; Max ${dhi:,.2f} / LF</div>
                {tot_html}{infl}
                <div class="cc-chips">
                  <div class="cc-chip"><strong>{s["n"]}</strong> bid rows</div>
                  <div class="cc-chip"><strong>{s["tabs"]}</strong> project{'s' if s['tabs']!=1 else ''}</div>
                  <div class="cc-chip"><strong>{'All Yrs' if not yr else yr}</strong></div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

            if add_click:
                if mat_sel and qty>0:
                    st.session_state.line_items.append({
                        "pipe_type":pt,"diameter":dia,"material":mat,"qty":qty,
                        "bid_year":yr,"raw":round(rows["_cost_raw"].mean(),2),
                        "unit_cost":du,"n":s["n"],"tabs":s["tabs"],"total":tot,"is_future":is_fut,
                    }); st.rerun()
                else: st.warning("Select a specific material and quantity > 0 to add.")

    # ── Bid Data Table ──────────────────────────────────────────────────────────
    if dia!="-- Select --" and s:
        rows_tbl   = qrows(df,hist,pt,dia,mat,yr)
        present_bc = [bc for bc in bidder_cols if rows_tbl[bc].notna().any()] if bidder_cols else []

        if not rows_tbl.empty and present_bc:
            yr_lbl = str(yr) if yr else "All Years"
            st.markdown('<div class="sec-div"><div class="sec-div-line"></div><div class="sec-div-lbl">Historical Bid Data</div><div class="sec-div-line"></div></div>', unsafe_allow_html=True)
            grp_keys=["source","YEAR"] if "YEAR" in rows_tbl.columns else ["source"]
            pivots=[]
            for key,grp in rows_tbl.groupby(grp_keys,sort=True,dropna=False):
                kv=key if isinstance(key,tuple) else (key,)
                kd=dict(zip(grp_keys,kv))
                proj=str(kd.get("source","")).replace(".xlsx","").replace(".xls","")
                yr_v=kd.get("YEAR","")
                yr_v=int(yr_v) if pd.notna(yr_v) and yr_v!="" else "—"
                desc=""
                if "description" in grp.columns:
                    dv=grp["description"].dropna().unique(); desc=str(dv[0]) if len(dv) else ""
                rd={"proj":proj,"yr":yr_v,"desc":desc}
                for bc in present_bc:
                    vals=grp[bc].dropna(); rd[bc]=vals.iloc[0] if not vals.empty else None
                pivots.append(rd)

            hdr='<th>Project / File</th><th class="c">Year</th>'
            for i,bc in enumerate(present_bc):
                bnum=re.search(r'\d+',bc).group(); color=BID_COLORS[i%len(BID_COLORS)]
                hdr+=f'<th class="bh-col r" style="background:{color}">Bidder {bnum}</th>'

            body=""
            for pr in pivots:
                uvals=[pr[bc] for bc in present_bc if pr.get(bc) is not None]
                mn=min(uvals) if uvals else None
                pn=pr["proj"][:36]+("…" if len(pr["proj"])>36 else "")
                dn=pr["desc"][:62]+("…" if len(pr["desc"])>62 else "")
                pc=f'<div class="proj-name">{pn}</div>'
                if dn: pc+=f'<div class="proj-desc">{dn}</div>'
                body+=f'<tr><td>{pc}</td><td class="c" style="font-family:var(--mono);font-size:11px;color:var(--t4)">{pr["yr"]}</td>'
                for bc in present_bc:
                    uc=pr.get(bc); low=uc is not None and mn is not None and abs(uc-mn)<0.01 and len(uvals)>1
                    cs=(f'<span class="star-low">${uc:,.0f}<span class="tag-low">LOW</span></span>'
                        if low else f'${uc:,.0f}') if uc is not None else '<span class="dash-nil">—</span>'
                    body+=f'<td class="r" style="border-left:1px solid var(--bg2)">{cs}</td>'
                body+='</tr>'

            foot='<tr><td colspan="2" style="font-size:10px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--t1)">Avg across all projects (raw bids)</td>'
            for bc in present_bc:
                av=rows_tbl[bc].dropna().mean(); av=round(av,2) if pd.notna(av) else None
                foot+=f'<td class="r" style="border-left:1px solid var(--border)">{"$"+f"{av:,.2f}" if av else "—"}</td>'
            foot+='</tr>'
            yr_note=f'Cost card projected to {yr}$' if is_fut else f'Cost card normalized to {CURRENT_YEAR}$'
            st.markdown(f"""
            <div class="e-card">
              <div class="e-card-label">Raw Bid Prices by Project &amp; Bidder
                <span style="font-size:10px;color:var(--t4);font-weight:400;font-family:var(--mono);text-transform:none;letter-spacing:0;margin-left:10px">
                  {s["n"]} rows · {len(pivots)} project{'s' if len(pivots)!=1 else ''} · {len(present_bc)} bidder{'s' if len(present_bc)!=1 else ''} · {yr_lbl}
                </span>
              </div>
              <div class="tbl-wrap"><table class="civ-tbl"><thead><tr>{hdr}</tr></thead><tbody>{body}</tbody><tfoot>{foot}</tfoot></table></div>
              <div style="font-size:10px;color:var(--t4);margin-top:8px;font-family:var(--mono)">LOW = lowest bid per project &nbsp;·&nbsp; Raw prices shown &nbsp;·&nbsp; {yr_note}</div>
            </div>""", unsafe_allow_html=True)

        # Material Comparison
        all_mc=qrows(df,hist,pt,dia,yr=yr)
        mc=(all_mc.groupby("material",as_index=False)
            .agg(avg=("_cost","mean"),lo=("_cost","min"),hi=("_cost","max"),
                 n=("_cost","count"),tabs=("source","nunique"))
            .sort_values("avg"))
        mc[["avg","lo","hi"]]=mc[["avg","lo","hi"]].round(2)

        if len(mc)>1:
            cheapest=mc.iloc[0]["avg"]; max_avg=mc["avg"].max()
            mat_sel_c=mat not in("-- All Materials --","-- Select Diameter First --")
            yr_lbl=str(yr) if yr else "All Years"
            col_heads=(f'<th class="r">Base {CURRENT_YEAR}$ / LF</th><th class="r">Projected {yr}$ / LF</th>'
                       if is_fut else '<th class="r">Avg Unit Cost</th><th class="r">Min – Max</th>')
            mat_note=(f"{dia} · projected to {yr}$" if is_fut else f"{dia} · {yr_lbl} · {CURRENT_YEAR}$")
            st.markdown('<div class="sec-div"><div class="sec-div-line"></div><div class="sec-div-lbl">Material Comparison</div><div class="sec-div-line"></div></div>', unsafe_allow_html=True)

            mc_body=""
            for _,r in mc.iterrows():
                sel=mat_sel_c and (mat==r["material"])
                row_cls='class="mat-sel-row"' if sel else ""
                stag=' <span style="font-size:10px;color:var(--p2);font-weight:700">◀ selected</span>' if sel else ""
                pct_c=((r["avg"]-cheapest)/cheapest*100) if cheapest>0 else 0
                vs_cls="vs-low" if pct_c<0.5 else "vs-high"
                vs_txt="cheapest" if pct_c<0.5 else f"+{pct_c:.0f}%"
                bw=int((r["avg"]/max_avg)*100) if max_avg>0 else 0
                bc="#0e9070" if pct_c<0.5 else "#5b2d8e"
                pa=round(r["avg"]*ff,2)
                cc=(f'<td class="r" style="color:var(--t4);font-size:12px">${r["avg"]:,.2f}</td>'
                    f'<td class="r" style="font-weight:700;color:var(--t1)">${pa:,.2f}</td>'
                    if is_fut else
                    f'<td class="r" style="font-weight:700;color:var(--t1)">${r["avg"]:,.2f} / LF</td>'
                    f'<td class="r" style="font-size:12px;color:var(--t4)">${r["lo"]:,.2f} – ${r["hi"]:,.2f}</td>')
                mc_body+=f"""<tr {row_cls}>
                  <td style="font-weight:{'600' if sel else '400'}">{r['material']}{stag}</td>{cc}
                  <td class="r" style="font-size:12px;color:var(--t3)">{int(r['n'])} bids / {int(r['tabs'])} proj</td>
                  <td style="padding:10px 16px"><div class="bar-bg"><div class="bar-fill" style="background:{bc};width:{bw}%"></div></div></td>
                  <td class="c"><span class="{vs_cls}">{vs_txt}</span></td>
                </tr>"""

            st.markdown(f"""
            <div class="e-card">
              <div class="e-card-label">Material Comparison
                <span style="font-size:10px;color:var(--t4);font-weight:400;font-family:var(--mono);text-transform:none;letter-spacing:0;margin-left:10px">{mat_note} · sorted cheapest first</span>
              </div>
              <div class="tbl-wrap"><table class="civ-tbl"><thead><tr>
                <th>Material</th>{col_heads}<th class="r">Bid Data</th><th>Relative</th><th class="c">vs Cheapest</th>
              </tr></thead><tbody>{mc_body}</tbody></table></div>
              <div style="font-size:10px;color:var(--t4);margin-top:8px;font-family:var(--mono)">All costs CPI-adjusted to {CURRENT_YEAR}$. For budgetary planning only.</div>
            </div>""", unsafe_allow_html=True)

    # Estimate Summary
    st.markdown('<div class="sec-div"><div class="sec-div-line"></div><div class="sec-div-lbl">Estimate Summary</div><div class="sec-div-line"></div></div>', unsafe_allow_html=True)

    if not st.session_state.line_items:
        st.markdown('<div class="e-card"><div class="empty-box"><div class="empty-icon">📋</div><div class="empty-text">No line items yet.<br>Configure the filters above and click <strong>＋ Add to Estimate</strong>.</div></div></div>', unsafe_allow_html=True)
    else:
        rows_html=""
        for li in st.session_state.line_items:
            is_f=li.get("is_future",False)
            ff_li=future_factor(li["bid_year"]) if is_f and li["bid_year"] else 1.0
            pct_li=(ff_li-1)*100; yr_d=str(li["bid_year"]) if li["bid_year"] else "All"
            yt=(f'<span class="yr-fut">📅 {yr_d}</span>' if is_f else f'<span class="yr-hist">{yr_d}</span>')
            cn=(f'<span class="proj-note">&nbsp;+{pct_li:.1f}% proj</span>' if is_f
                else f'<span class="base-note">&nbsp;{CURRENT_YEAR}$</span>')
            rows_html+=f"""<tr>
              <td style="font-size:12px;color:var(--t3)">{li['pipe_type']}</td>
              <td style="font-weight:700;color:var(--t1)">{li['diameter']}</td>
              <td style="color:var(--t2)">{li['material']}</td>
              <td class="r">{li['qty']:,.0f} LF</td>
              <td class="c">{yt}</td>
              <td class="r">${li['unit_cost']:,.2f}{cn}</td>
              <td class="c" style="font-size:11px;color:var(--t3)">{li['n']} bids / {li['tabs']} proj</td>
              <td class="r" style="color:var(--teal);font-weight:700;font-size:15px">${li['total']:,.0f}</td>
            </tr>"""

        grand=sum(li["total"] for li in st.session_state.line_items)
        n_i=len(st.session_state.line_items)
        st.markdown(f"""
        <div class="e-card">
          <div class="e-card-label">{n_i} Line Item{'s' if n_i!=1 else ''}
            <span style="font-size:10px;color:var(--t4);font-weight:400;font-family:var(--mono);text-transform:none;letter-spacing:0;margin-left:10px">all costs in {CURRENT_YEAR}$ unless projected</span>
          </div>
          <div class="tbl-wrap"><table class="civ-tbl">
            <thead><tr>
              <th>Type</th><th>Diameter</th><th>Material</th>
              <th class="r">Quantity</th><th class="c">Bid Year</th>
              <th class="r">Unit Cost</th><th class="c">Bid Data</th><th class="r">Item Total</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
            <tfoot><tr>
              <td colspan="7" style="text-align:right;font-size:12px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--p2)">Total Project Estimate ({CURRENT_YEAR}$)</td>
              <td class="r"><span class="grand-ttl">${grand:,.0f}</span></td>
            </tr></tfoot>
          </table></div>
          <div style="font-size:10px;color:var(--t4);margin-top:8px;font-family:var(--mono)">🟡 Yellow bid year = projected future cost &nbsp;·&nbsp; For budgetary planning only — not for contract use.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="civ-footer"><strong>Civitas Engineering Group, Inc.</strong> &nbsp;·&nbsp; &nbsp;·&nbsp; COH Pipe Cost Estimator &nbsp;·&nbsp; Base Year {CURRENT_YEAR} &nbsp;·&nbsp; ENR Escalation → {PROJECTION_END_YEAR} &nbsp;·&nbsp; For Budgetary Planning Only</div>', unsafe_allow_html=True)