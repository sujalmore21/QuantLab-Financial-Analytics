"""
=========================================
Module  : theme.py
Project : QuantLab
Purpose : Shared design system — colors, type,
          CSS injection, and chart/component helpers.

Design direction
----------------
"Dealing-desk at close" — a dark trading-terminal
surface (graphite-navy, not pure black) with a single
warm gold accent used only for the number that matters
most (the optimal portfolio). Data is set in a mono
face like a real terminal; everything else is a quiet
grotesk. The signature element is the "ruler rule": a
tick-marked divider (like the gradations on a dial)
that replaces plain st.divider() calls throughout.
=========================================
"""

import streamlit as st

# -----------------------------------------------------
# Design tokens
# -----------------------------------------------------
COLORS = {
    "bg":          "#0B0E14",   # graphite-navy base
    "panel":       "#141A24",   # card surface
    "panel_alt":   "#0F141C",   # recessed surface (table, chart bg)
    "border":      "#232B38",   # hairline borders
    "text":        "#E7E4DC",   # warm off-white
    "muted":       "#8B93A1",   # secondary text
    "gold":        "#C9A227",   # single hero accent — "the desk's pen"
    "gold_dim":    "#8A7328",
    "blue":        "#5B7FA6",   # secondary series (low-risk portfolio)
    "red":         "#B5544B",   # risk / drawdown
    "green":       "#4F9D69",   # positive delta, used sparingly
}

FONT_DISPLAY = "'Space Grotesk', sans-serif"
FONT_BODY = "'Inter', sans-serif"
FONT_MONO = "'IBM Plex Mono', monospace"


# -----------------------------------------------------
# Icon system (inline SVG, outline style — no external
# icon font dependency, works in Streamlit markdown)
# -----------------------------------------------------
ICONS = {
    "trending-up": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline>',
    "trending-down": '<polyline points="22 17 13.5 8.5 8.5 13.5 2 7"></polyline><polyline points="16 17 22 17 22 11"></polyline>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>',
    "target": '<circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline>',
    "dollar-sign": '<line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>',
    "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>',
    "pie-chart": '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path>',
    "bar-chart": '<line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line>',
    "alert-triangle": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line>',
    "clock": '<circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>',
    "scale": '<path d="M16 3h5v5"></path><path d="M8 3H3v5"></path><path d="M12 3v18"></path><path d="M3 16l4.5-9L12 16"></path><path d="M14 16l3.5-9L21 16"></path><path d="M3 16a4.5 2.5 0 0 0 9 0"></path><path d="M14 16a3.5 2 0 0 0 7 0"></path>',
    "sliders": '<line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line><line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line>',
    "file-text": '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line>',
    "waves": '<path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.6 2 5.1 2 2.6 0 2.6-2 5.1-2 1.3 0 1.9.5 2.5 1"></path><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.6 2 5.1 2 2.6 0 2.6-2 5.1-2 1.3 0 1.9.5 2.5 1"></path><path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.6 2 5.1 2 2.6 0 2.6-2 5.1-2 1.3 0 1.9.5 2.5 1"></path>',
}


def icon_svg(name: str, size: int = 16, color: str = None, stroke_width: float = 2.0) -> str:
    """Inline SVG icon. Returns an <svg> string safe to drop into st.markdown(unsafe_allow_html=True)."""
    color = color or COLORS["gold"]
    body = ICONS.get(name, ICONS["activity"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="vertical-align:-3px; margin-right:7px; flex-shrink:0;">{body}</svg>'
    )


def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: {FONT_BODY};
        }}

        .stApp {{
            background: {COLORS["bg"]};
            color: {COLORS["text"]};
        }}

        /* Clean up chrome WITHOUT hiding the sidebar collapse/expand arrow.
           NOTE: we deliberately do NOT hide [data-testid="stToolbar"] wholesale
           anymore — on some Streamlit versions the sidebar toggle lives inside
           it, and hiding the toolbar was hiding the toggle along with it. We
           only hide the specific "Deploy" action button instead. */
        #MainMenu {{ visibility: hidden; }}
        [data-testid="stHeader"] {{
            background: transparent;
        }}
        [data-testid="stAppDeployButton"] {{ display: none !important; }}

        /* The ">" / "<" arrow that opens/closes the sidebar. Streamlit has
           renamed this element's testid across versions (collapsedControl ->
           stSidebarCollapsedControl -> stSidebarCollapseButton, and possibly
           others we haven't seen yet) — so we target every known name AND a
           substring match as a catch-all, and force it visible regardless of
           anything else on the page trying to hide it. */
        div[data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid*="ollaps"] {{
            visibility: visible !important;
            opacity: 1 !important;
            display: flex !important;
            color: {COLORS["gold"]} !important;
            z-index: 999999 !important;
        }}
        div[data-testid="collapsedControl"] button,
        [data-testid="stSidebarCollapsedControl"] button,
        [data-testid="stSidebarCollapseButton"] button,
        [data-testid*="ollaps"] button {{
            background: {COLORS["panel"]} !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 6px !important;
            visibility: visible !important;
            opacity: 1 !important;
        }}
        div[data-testid="collapsedControl"] svg,
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid*="ollaps"] svg {{
            fill: {COLORS["gold"]} !important;
            visibility: visible !important;
            opacity: 1 !important;
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }}

        /* ---------- Headings ---------- */
        h1, h2, h3 {{
            font-family: {FONT_DISPLAY};
            font-weight: 600;
            letter-spacing: -0.01em;
            color: {COLORS["text"]};
        }}

        /* ---------- Ticker header bar ---------- */
        .ql-tickerbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: {COLORS["panel"]};
            border: 1px solid {COLORS["border"]};
            border-left: 3px solid {COLORS["gold"]};
            border-radius: 4px;
            padding: 14px 22px;
            margin-bottom: 8px;
        }}
        .ql-tickerbar .ql-brand {{
            font-family: {FONT_DISPLAY};
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            color: {COLORS["text"]};
        }}
        .ql-tickerbar .ql-brand span {{ color: {COLORS["gold"]}; }}
        .ql-tickerbar .ql-tag-wrap {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .ql-tickerbar .ql-tag {{
            font-family: {FONT_MONO};
            font-size: 0.75rem;
            color: {COLORS["muted"]};
            text-transform: uppercase;
            letter-spacing: 0.12em;
        }}
        .ql-live-dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: {COLORS["green"]};
            box-shadow: 0 0 0 0 rgba(79, 157, 105, 0.6);
            animation: ql-pulse 2s infinite;
        }}
        @keyframes ql-pulse {{
            0%   {{ box-shadow: 0 0 0 0 rgba(79, 157, 105, 0.55); }}
            70%  {{ box-shadow: 0 0 0 6px rgba(79, 157, 105, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(79, 157, 105, 0); }}
        }}
        @media (prefers-reduced-motion: reduce) {{
            .ql-live-dot {{ animation: none; }}
        }}

        /* ---------- Sidebar ---------- */
        [data-testid="stSidebar"] {{
            background: {COLORS["panel_alt"]};
            border-right: 1px solid {COLORS["border"]};
        }}
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 0.5rem;
        }}
        .ql-sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 4px 16px 4px;
            border-bottom: 1px solid {COLORS["border"]};
            margin-bottom: 10px;
        }}
        .ql-sidebar-brand .ql-mark {{
            width: 8px; height: 8px;
            background: {COLORS["gold"]};
            border-radius: 2px;
            flex-shrink: 0;
        }}
        .ql-sidebar-brand .ql-name {{
            font-family: {FONT_DISPLAY};
            font-weight: 700;
            font-size: 1.05rem;
            color: {COLORS["text"]};
            letter-spacing: 0.01em;
        }}
        .ql-sidebar-brand .ql-name span {{ color: {COLORS["gold"]}; }}
        .ql-sidebar-foot {{
            font-family: {FONT_MONO};
            font-size: 0.65rem;
            color: {COLORS["muted"]};
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 14px 4px;
            border-top: 1px solid {COLORS["border"]};
            margin-top: 10px;
        }}

        /* Streamlit's auto-generated multipage nav — dark, mono, gold active state */
        [data-testid="stSidebarNav"] {{
            background: transparent;
            padding-top: 4px;
        }}
        [data-testid="stSidebarNav"] ul {{
            padding: 0 6px;
        }}
        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNavLink"] {{
            font-family: {FONT_MONO} !important;
            font-size: 0.8rem !important;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: {COLORS["muted"]} !important;
            border-radius: 4px;
            transition: background 0.15s ease, color 0.15s ease;
        }}
        [data-testid="stSidebarNav"] a:hover {{
            background: {COLORS["panel"]} !important;
            color: {COLORS["text"]} !important;
        }}
        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: {COLORS["panel"]} !important;
            color: {COLORS["gold"]} !important;
            border-left: 2px solid {COLORS["gold"]};
        }}

        /* The first nav item is the entry-point script (app.py), which Streamlit
           labels using the filename ("app"). Relabel it "Home" purely in CSS —
           no file rename needed, works no matter what the file is called.
           The visible label text lives in a NESTED span (not the <a> itself),
           and that span has its own font-size, so we have to collapse every
           descendant too, not just the anchor. */
        [data-testid="stSidebarNav"] li:first-child a,
        [data-testid="stSidebarNav"] li:first-child a * {{
            font-size: 0 !important;
            line-height: 0 !important;
        }}
        [data-testid="stSidebarNav"] li:first-child a {{
            position: relative;
        }}
        [data-testid="stSidebarNav"] li:first-child a::after {{
            content: "Home";
            font-family: {FONT_MONO};
            font-size: 0.8rem !important;
            line-height: normal !important;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}

        /* Generic sidebar widget text (selectbox, expander, etc.) */
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {{
            color: {COLORS["text"]};
        }}

        /* ================================================
           NATIVE WIDGET THEMING
           (config.toml sets base colors; this refines shape/
           hover/typography so widgets read as part of the
           product, not default Streamlit chrome)
           ================================================ */

        /* ---------- Buttons ---------- */
        .stButton > button,
        .stDownloadButton > button,
        .stFormSubmitButton > button {{
            background: {COLORS["panel"]};
            color: {COLORS["text"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 6px;
            font-family: {FONT_MONO};
            font-size: 0.8rem;
            font-weight: 500;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            padding: 0.55rem 1.1rem;
            transition: all 0.15s ease;
            box-shadow: 0 1px 2px rgba(0,0,0,0.25);
        }}
        .stButton > button:hover,
        .stDownloadButton > button:hover,
        .stFormSubmitButton > button:hover {{
            background: {COLORS["gold"]};
            color: {COLORS["bg"]};
            border-color: {COLORS["gold"]};
            box-shadow: 0 6px 16px rgba(201, 162, 39, 0.25);
            transform: translateY(-1px);
        }}
        .stButton > button:active,
        .stDownloadButton > button:active,
        .stFormSubmitButton > button:active {{
            transform: translateY(0px);
        }}

        /* ---------- Slider ---------- */
        [data-testid="stSlider"] label {{
            font-family: {FONT_MONO};
            font-size: 0.78rem;
            color: {COLORS["muted"]};
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}
        [data-testid="stTickBarMin"], [data-testid="stTickBarMax"] {{
            font-family: {FONT_MONO};
            color: {COLORS["muted"]};
        }}

        /* ---------- Radio (used as a pill/tab selector) ---------- */
        [data-testid="stRadio"] label {{
            font-family: {FONT_MONO};
            font-size: 0.82rem;
        }}
        [data-testid="stRadio"] > div {{
            gap: 6px;
        }}

        /* ---------- Selectbox ---------- */
        [data-testid="stSelectbox"] label {{
            font-family: {FONT_MONO};
            font-size: 0.78rem;
            color: {COLORS["muted"]};
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
            background: {COLORS["panel"]};
            border-color: {COLORS["border"]};
            border-radius: 6px;
        }}

        /* ---------- Alerts (info / success / warning / error) ---------- */
        [data-testid="stAlert"] {{
            background: {COLORS["panel"]};
            border: 1px solid {COLORS["border"]};
            border-left: 3px solid {COLORS["blue"]};
            border-radius: 6px;
            font-family: {FONT_BODY};
        }}
        [data-testid="stAlertContainer"] {{
            border-radius: 6px;
        }}
        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] strong,
        div[data-testid="stAlert"] span {{
            color: {COLORS["text"]} !important;
        }}
        div[data-testid="stAlert"] svg {{
            fill: {COLORS["blue"]} !important;
        }}

        /* ---------- Expander ---------- */
        [data-testid="stExpander"] {{
            background: {COLORS["panel"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 6px;
        }}
        [data-testid="stExpander"] summary {{
            font-family: {FONT_MONO};
            font-size: 0.82rem;
            color: {COLORS["text"]};
        }}

        /* ---------- Tabs ---------- */
        [data-testid="stTabs"] [data-baseweb="tab"] {{
            font-family: {FONT_MONO};
            font-size: 0.8rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: {COLORS["muted"]};
        }}
        [data-testid="stTabs"] [aria-selected="true"] {{
            color: {COLORS["gold"]} !important;
        }}

        /* ---------- Dataframe header row ---------- */
        [data-testid="stDataFrame"] thead tr th {{
            background: {COLORS["panel_alt"]} !important;
            color: {COLORS["gold"]} !important;
            font-family: {FONT_MONO} !important;
            font-size: 0.72rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* ---------- Ruler rule (signature divider) ---------- */
        .ql-rule {{
            position: relative;
            height: 18px;
            margin: 26px 0 22px 0;
            background-image: repeating-linear-gradient(
                to right,
                {COLORS["border"]} 0px, {COLORS["border"]} 1px,
                transparent 1px, transparent 24px
            );
            background-position: bottom;
            background-size: 100% 10px;
            background-repeat: repeat-x;
            border-bottom: 1px solid {COLORS["gold_dim"]};
        }}

        /* ---------- Section eyebrow ---------- */
        .ql-eyebrow {{
            font-family: {FONT_MONO};
            font-size: 0.72rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: {COLORS["gold"]};
            margin-bottom: 2px;
        }}
        .ql-section-title {{
            font-family: {FONT_DISPLAY};
            font-size: 1.35rem;
            font-weight: 600;
            color: {COLORS["text"]};
            margin-bottom: 14px;
            display: flex;
            align-items: center;
        }}

        /* ---------- KPI cards ---------- */
        .ql-kpi {{
            background: {COLORS["panel"]};
            border: 1px solid {COLORS["border"]};
            border-top: 2px solid {COLORS["gold"]};
            border-radius: 6px;
            padding: 16px 18px 14px 18px;
            height: 100%;
            box-shadow: 0 1px 2px rgba(0,0,0,0.25);
            transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
        }}
        .ql-kpi:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.35);
            border-color: {COLORS["gold_dim"]};
        }}
        .ql-kpi .ql-kpi-label {{
            font-family: {FONT_MONO};
            font-size: 0.7rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: {COLORS["muted"]};
            margin-bottom: 8px;
            display: flex;
            align-items: center;
        }}
        .ql-kpi .ql-kpi-value {{
            font-family: {FONT_MONO};
            font-size: 1.9rem;
            font-weight: 600;
            color: {COLORS["text"]};
            line-height: 1.1;
        }}
        .ql-kpi .ql-kpi-delta {{
            font-family: {FONT_MONO};
            font-size: 0.78rem;
            margin-top: 6px;
        }}
        .ql-kpi .ql-kpi-delta.pos {{ color: {COLORS["green"]}; }}
        .ql-kpi .ql-kpi-delta.neg {{ color: {COLORS["red"]}; }}
        .ql-kpi .ql-kpi-delta.neu {{ color: {COLORS["muted"]}; }}

        /* ---------- Module cards (wrap tables/charts) ---------- */
        .ql-card {{
            background: {COLORS["panel"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 6px;
            padding: 18px 20px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.25);
            transition: box-shadow 0.15s ease, border-color 0.15s ease;
        }}
        .ql-card:hover {{
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            border-color: {COLORS["gold_dim"]};
        }}
        .ql-card-label {{
            font-family: {FONT_MONO};
            font-size: 0.72rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: {COLORS["muted"]};
            margin-bottom: 12px;
            display: flex;
            align-items: center;
        }}

        /* ---------- Dataframe styling ---------- */
        [data-testid="stDataFrame"] {{
            border: 1px solid {COLORS["border"]};
            border-radius: 4px;
        }}

        /* ---------- Footer ---------- */
        .ql-footer {{
            font-family: {FONT_MONO};
            font-size: 0.7rem;
            color: {COLORS["muted"]};
            text-align: center;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding-top: 10px;
        }}

        /* ---------- Info/status pills (used on landing page) ---------- */
        .ql-pill {{
            background: {COLORS["panel"]};
            border: 1px solid {COLORS["border"]};
            border-left: 3px solid var(--pill-accent, {COLORS["gold"]});
            border-radius: 6px;
            padding: 16px 18px;
            height: 100%;
            box-shadow: 0 1px 2px rgba(0,0,0,0.25);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        .ql-pill:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }}
        .ql-pill .ql-pill-title {{
            font-family: {FONT_DISPLAY};
            font-weight: 600;
            font-size: 1rem;
            color: {COLORS["text"]};
            margin-bottom: 6px;
            display: flex;
            align-items: center;
        }}
        .ql-pill .ql-pill-body {{
            font-family: {FONT_BODY};
            font-size: 0.85rem;
            color: {COLORS["muted"]};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def ticker_header(brand: str, accent: str, tag: str, live: bool = True):
    dot = '<span class="ql-live-dot"></span>' if live else ""
    st.markdown(
        f"""
        <div class="ql-tickerbar">
            <div class="ql-brand">{brand}<span>{accent}</span></div>
            <div class="ql-tag-wrap">{dot}<div class="ql-tag">{tag}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand(name: str = "QUANT", accent: str = "LAB"):
    """Call once at the top of st.sidebar (or right after inject_css) on every
    page so the sidebar reads as part of the same product, not a default
    Streamlit nav list."""
    st.sidebar.markdown(
        f"""
        <div class="ql-sidebar-brand">
            <div class="ql-mark"></div>
            <div class="ql-name">{name}<span>{accent}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_foot(text: str = "System nominal"):
    st.sidebar.markdown(
        f"""
        <div class="ql-sidebar-foot">
            <span class="ql-live-dot" style="margin-right:6px;"></span>{text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def ruler_rule():
    st.markdown('<div class="ql-rule"></div>', unsafe_allow_html=True)


def section_title(eyebrow: str, title: str, icon: str = None):
    icon_html = icon_svg(icon, size=20) if icon else ""
    st.markdown(
        f"""
        <div class="ql-eyebrow">{eyebrow}</div>
        <div class="ql-section-title">{icon_html}{title}</div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str = None, delta_class: str = "neu", icon: str = None):
    icon_html = icon_svg(icon, size=14, color=COLORS["muted"]) if icon else ""
    delta_html = f'<div class="ql-kpi-delta {delta_class}">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="ql-kpi">
            <div class="ql-kpi-label">{icon_html}{label}</div>
            <div class="ql-kpi-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def pill(title: str, body: str, accent: str, icon: str = None):
    icon_html = icon_svg(icon, size=18, color=accent) if icon else ""
    st.markdown(
        f"""
        <div class="ql-pill" style="--pill-accent:{accent};">
            <div class="ql-pill-title">{icon_html}{title}</div>
            <div class="ql-pill-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer(text: str):
    ruler_rule()
    st.markdown(f'<div class="ql-footer">{text}</div>', unsafe_allow_html=True)


def render_table(df, label: str = "", format_dict: dict = None, hide_index: bool = True,
                  icon: str = None, highlight_col: str = None):
    """Wrap a dataframe in the same bordered card used everywhere else,
    so every page's tables look identical instead of each page hand-rolling
    the markdown wrapper. `highlight_col` picks out the top value in that
    column with a gold background."""
    icon_html = icon_svg(icon, size=13, color=COLORS["muted"]) if icon else ""
    label_html = f'<div class="ql-card-label">{icon_html}{label}</div>' if label else ""
    st.markdown(f'<div class="ql-card">{label_html}', unsafe_allow_html=True)

    styled = df.style
    if format_dict:
        styled = styled.format(format_dict)

    if highlight_col and highlight_col in df.columns:
        def _highlight_top(col):
            is_max = col == col.max()
            return [
                f'background-color:{COLORS["gold"]}; color:{COLORS["bg"]}; font-weight:600;'
                if v else '' for v in is_max
            ]
        styled = styled.apply(_highlight_top, subset=[highlight_col])

    st.dataframe(styled, use_container_width=True, hide_index=hide_index)
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------
# Plotly chart builders (kept here so both pages match)
# -----------------------------------------------------
def style_plotly(fig, height=380):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_family=FONT_MONO,
        font_color=COLORS["muted"],
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(
            orientation="h",
            yanchor="top", y=-0.12,
            xanchor="center", x=0.5,
            font=dict(color=COLORS["text"], size=11),
        ),
        hoverlabel=dict(
            bgcolor=COLORS["panel"],
            bordercolor=COLORS["border"],
            font=dict(family=FONT_MONO, color=COLORS["text"], size=12),
        ),
    )
    return fig


def allocation_donut(df, weight_col="Weight %", label_col="Stock"):
    import plotly.graph_objects as go

    palette = [COLORS["gold"], COLORS["blue"], COLORS["green"],
               COLORS["red"], "#7A6FA3", "#4A9C9E", "#B08A3E", "#6B7FB3"]
    colors = [palette[i % len(palette)] for i in range(len(df))]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=df[label_col],
                values=df[weight_col],
                hole=0.62,
                marker=dict(colors=colors, line=dict(color=COLORS["bg"], width=3)),
                textinfo="percent",
                textposition="inside",
                textfont=dict(color=COLORS["bg"], size=13, family=FONT_MONO),
                hovertemplate="<b>%{label}</b><br>%{value:.2f}%<extra></extra>",
                pull=[0.02] * len(df),
                sort=False,
            )
        ]
    )
    fig.update_layout(
        showlegend=True,
        annotations=[
            dict(
                text=f"{df[weight_col].sum():.0f}%<br><span style='font-size:10px;color:{COLORS['muted']}'>ALLOCATED</span>",
                x=0.5, y=0.5,
                font=dict(size=20, color=COLORS["text"], family=FONT_MONO),
                showarrow=False,
            )
        ],
    )
    return style_plotly(fig, height=400)


def comparison_bar(df_best, df_low, label_col="Stock", weight_col="Weight %"):
    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_best[label_col], y=df_best[weight_col],
            name="Optimal", marker_color=COLORS["gold"],
            hovertemplate="%{x}<br>Optimal: %{y:.2f}%<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=df_low[label_col], y=df_low[weight_col],
            name="Minimum risk", marker_color=COLORS["blue"],
            hovertemplate="%{x}<br>Min-risk: %{y:.2f}%<extra></extra>",
        )
    )
    fig.update_layout(
        barmode="group",
        xaxis=dict(color=COLORS["muted"], gridcolor=COLORS["border"]),
        yaxis=dict(color=COLORS["muted"], gridcolor=COLORS["border"], title="Weight %"),
    )
    return style_plotly(fig, height=360)


def efficient_frontier_chart(portfolios, max_sharpe_pt, min_risk_pt):
    """
    portfolios: list of dicts with 'risk', 'return', 'sharpe'
    max_sharpe_pt / min_risk_pt: single portfolio dicts to highlight
    """
    import plotly.graph_objects as go

    risks = [p["risk"] for p in portfolios]
    rets = [p["return"] for p in portfolios]
    sharpes = [p["sharpe"] for p in portfolios]

    fig = go.Figure()

    fig.add_trace(
        go.Scattergl(
            x=risks, y=rets,
            mode="markers",
            marker=dict(
                size=6,
                color=sharpes,
                colorscale=[[0, COLORS["blue"]], [1, COLORS["gold"]]],
                showscale=True,
                colorbar=dict(
                    title=dict(text="Sharpe", font=dict(color=COLORS["muted"], size=10)),
                    tickfont=dict(color=COLORS["muted"], size=10),
                    thickness=12,
                ),
                opacity=0.55,
                line=dict(width=0),
            ),
            name="Simulated portfolios",
            hovertemplate="Risk: %{x:.2%}<br>Return: %{y:.2%}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[max_sharpe_pt["risk"]], y=[max_sharpe_pt["return"]],
            mode="markers",
            marker=dict(size=16, color=COLORS["gold"], symbol="star",
                        line=dict(color=COLORS["bg"], width=1.5)),
            name="Max Sharpe",
            hovertemplate="Max Sharpe<br>Risk: %{x:.2%}<br>Return: %{y:.2%}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[min_risk_pt["risk"]], y=[min_risk_pt["return"]],
            mode="markers",
            marker=dict(size=14, color=COLORS["blue"], symbol="diamond",
                        line=dict(color=COLORS["bg"], width=1.5)),
            name="Minimum risk",
            hovertemplate="Min Risk<br>Risk: %{x:.2%}<br>Return: %{y:.2%}<extra></extra>",
        )
    )

    fig.update_layout(
        xaxis=dict(color=COLORS["muted"], gridcolor=COLORS["border"], title="Risk (volatility)", tickformat=".0%"),
        yaxis=dict(color=COLORS["muted"], gridcolor=COLORS["border"], title="Expected return", tickformat=".0%"),
        showlegend=True,
    )
    return style_plotly(fig, height=460)


def ranked_returns_bar(df, label_col="Stock", value_col="Annual Return %"):
    """Bar chart colored by sign, with the top performer picked out in gold."""
    import plotly.graph_objects as go

    df = df.sort_values(value_col, ascending=False).reset_index(drop=True)
    best_idx = df[value_col].idxmax()

    colors = []
    for i, v in enumerate(df[value_col]):
        if i == best_idx:
            colors.append(COLORS["gold"])
        elif v >= 0:
            colors.append(COLORS["green"])
        else:
            colors.append(COLORS["red"])

    fig = go.Figure(
        data=[
            go.Bar(
                x=df[label_col], y=df[value_col],
                marker_color=colors,
                hovertemplate="%{x}: %{y:.2f}%<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        xaxis=dict(color=COLORS["muted"], gridcolor=COLORS["border"]),
        yaxis=dict(color=COLORS["muted"], gridcolor=COLORS["border"], title=value_col,
                    zeroline=True, zerolinecolor=COLORS["border"]),
        showlegend=False,
    )
    return style_plotly(fig, height=380)


def price_line_chart(df, date_col="Date", price_col="Close", label="Price"):
    import plotly.graph_objects as go

    fig = go.Figure(
        data=[
            go.Scatter(
                x=df[date_col], y=df[price_col],
                mode="lines",
                line=dict(color=COLORS["gold"], width=2.25, shape="spline", smoothing=0.3),
                fill="tozeroy",
                fillcolor="rgba(201, 162, 39, 0.10)",
                name=label,
                hovertemplate="<b>%{x|%b %d, %Y}</b><br>$%{y:.2f}<extra></extra>",
            )
        ]
    )
    fig.update_layout(hovermode="x unified")
    fig.update_layout(
        xaxis=dict(color=COLORS["muted"], gridcolor=COLORS["border"]),
        yaxis=dict(color=COLORS["muted"], gridcolor=COLORS["border"], title="Price ($)"),
        showlegend=False,
    )
    return style_plotly(fig, height=340)


def risk_gradient_bar(df, label_col="Stock", value_col="Annual Volatility %"):
    """Bar chart colored on a blue (low risk) -> gold -> red (high risk) gradient."""
    import plotly.graph_objects as go

    df = df.sort_values(value_col, ascending=True).reset_index(drop=True)

    fig = go.Figure(
        data=[
            go.Bar(
                x=df[label_col], y=df[value_col],
                marker=dict(
                    color=df[value_col],
                    colorscale=[[0, COLORS["blue"]], [0.5, COLORS["gold"]], [1, COLORS["red"]]],
                    showscale=True,
                    colorbar=dict(
                        title=dict(text=value_col, font=dict(color=COLORS["muted"], size=10)),
                        tickfont=dict(color=COLORS["muted"], size=10),
                        thickness=12,
                    ),
                ),
                hovertemplate=f"%{{x}}: %{{y:.2f}}%<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        xaxis=dict(color=COLORS["muted"], gridcolor=COLORS["border"]),
        yaxis=dict(color=COLORS["muted"], gridcolor=COLORS["border"], title=value_col),
        showlegend=False,
    )
    return style_plotly(fig, height=380)


def drawdown_chart(dates, drawdown_pct, label="Drawdown"):
    """An 'underwater' equity curve — drawdown shaded below zero."""
    import plotly.graph_objects as go

    fig = go.Figure(
        data=[
            go.Scatter(
                x=dates, y=drawdown_pct,
                mode="lines",
                line=dict(color=COLORS["red"], width=1.75, shape="spline", smoothing=0.3),
                fill="tozeroy",
                fillcolor="rgba(181, 84, 75, 0.18)",
                name=label,
                hovertemplate="<b>%{x|%b %d, %Y}</b><br>%{y:.2f}%<extra></extra>",
            )
        ]
    )
    fig.update_layout(hovermode="x unified")
    fig.update_layout(
        xaxis=dict(color=COLORS["muted"], gridcolor=COLORS["border"]),
        yaxis=dict(color=COLORS["muted"], gridcolor=COLORS["border"], title="Drawdown %",
                    zeroline=True, zerolinecolor=COLORS["border"]),
        showlegend=False,
    )
    return style_plotly(fig, height=300)


def correlation_heatmap(returns_df):
    """returns_df: wide DataFrame of daily returns, one column per asset."""
    import plotly.graph_objects as go

    corr = returns_df.corr()
    labels = corr.columns.tolist()
    z = corr.values

    fig = go.Figure(
        data=go.Heatmap(
            z=z, x=labels, y=labels,
            colorscale=[[0, COLORS["blue"]], [0.5, COLORS["panel_alt"]], [1, COLORS["gold"]]],
            zmin=-1, zmax=1,
            text=[[f"{v:.2f}" for v in row] for row in z],
            texttemplate="%{text}",
            textfont=dict(size=10, family=FONT_MONO, color=COLORS["text"]),
            hovertemplate="%{x} vs %{y}<br>Correlation: %{z:.2f}<extra></extra>",
            colorbar=dict(
                tickfont=dict(color=COLORS["muted"], size=10),
                thickness=12,
            ),
            xgap=2, ygap=2,
        )
    )
    fig.update_layout(
        xaxis=dict(color=COLORS["muted"], side="bottom"),
        yaxis=dict(color=COLORS["muted"], autorange="reversed"),
    )
    height = max(320, 42 * len(labels) + 120)
    return style_plotly(fig, height=height)


def indexed_price_chart(prices_df, stocks, date_col="Date"):
    """prices_df: wide DataFrame with `date_col` + one price column per stock in `stocks`.
    Each series is indexed to 100 at the first row so relative growth is comparable
    across assets with very different price levels."""
    import plotly.graph_objects as go

    palette = [COLORS["gold"], COLORS["blue"], COLORS["green"], COLORS["red"],
               "#7A6FA3", "#4A9C9E", "#B08A3E", "#6B7FB3"]

    fig = go.Figure()
    for i, stock in enumerate(stocks):
        if stock not in prices_df.columns:
            continue
        series = prices_df[stock]
        if series.empty or series.iloc[0] == 0:
            continue
        indexed = series / series.iloc[0] * 100
        fig.add_trace(
            go.Scatter(
                x=prices_df[date_col], y=indexed,
                mode="lines", name=stock,
                line=dict(color=palette[i % len(palette)], width=1.75, shape="spline", smoothing=0.25),
                hovertemplate=f"<b>{stock}</b><br>%{{x|%b %d, %Y}}: %{{y:.1f}}<extra></extra>",
            )
        )

    fig.add_hline(y=100, line=dict(color=COLORS["border"], width=1, dash="dot"))

    fig.update_xaxes(
        color=COLORS["muted"], gridcolor=COLORS["border"],
        rangeslider=dict(visible=True, thickness=0.06, bgcolor=COLORS["panel_alt"],
                          bordercolor=COLORS["border"], borderwidth=1),
        rangeselector=dict(
            buttons=[
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(step="all", label="All"),
            ],
            bgcolor=COLORS["panel"], activecolor=COLORS["gold"],
            font=dict(color=COLORS["muted"], size=10),
        ),
    )
    fig.update_yaxes(color=COLORS["muted"], gridcolor=COLORS["border"], title="Indexed to 100")
    fig.update_layout(hovermode="x unified")

    return style_plotly(fig, height=460)