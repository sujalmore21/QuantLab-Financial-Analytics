"""
=========================================
Module  : reports.py
Project : QuantLab
Purpose : Exportable Portfolio Reports
=========================================
"""

import io
import base64
from datetime import datetime

import pandas as pd
import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image, KeepTogether, PageBreak,
)
from reportlab.pdfgen import canvas as pdfcanvas

from services.report_service import ReportService
from config import STOCKS
from theme import (
    inject_css, ticker_header, ruler_rule, section_title,
    kpi_card, footer, sidebar_brand, sidebar_foot, COLORS,
)


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="QuantLab · Reports",
    page_icon="📈",
    layout="wide",
)

inject_css()
sidebar_brand()

ticker_header(
    brand="QUANT",
    accent="LAB",
    tag="Report Center",
)


# ==========================================================
# Load Data
# ==========================================================

@st.cache_resource(show_spinner=False)
def get_service():
    return ReportService()


service = get_service()

try:
    with st.spinner("Preparing report data..."):
        summary = service.get_summary()
        best = summary["best_portfolio"]
        low_risk = summary["low_risk_portfolio"]
except Exception as exc:
    st.error(f"Could not load portfolio data: {exc}")
    st.stop()

sidebar_foot("Report data ready")


def alloc_df(portfolio):
    df = pd.DataFrame({"Stock": STOCKS, "Weight %": portfolio["weights"]})
    df["Weight %"] = df["Weight %"] * 100
    return df.sort_values("Weight %", ascending=False).reset_index(drop=True)


generated_at = datetime.now().strftime("%B %d, %Y %H:%M")


# ==========================================================
# Report Metadata
# ==========================================================

st.write("")
section_title("Metadata", "Report Details", icon="clock")

m1, m2, m3, m4 = st.columns(4)
with m1:
    kpi_card("Generated", datetime.now().strftime("%b %d, %Y"), datetime.now().strftime("%H:%M"), "neu", icon="clock")
with m2:
    kpi_card("Assets Covered", str(len(STOCKS)), "in optimization universe", "neu", icon="layers")
with m3:
    kpi_card("Optimal Sharpe", f"{best['sharpe']:.2f}", "max-Sharpe candidate", "neu", icon="target")
with m4:
    kpi_card("Min Risk", f"{low_risk['risk']:.2%}", "minimum-risk candidate", "neu", icon="shield")

ruler_rule()


# ==========================================================
# Preview (on-page quick look)
# ==========================================================

section_title("Preview", "What Will Be Included", icon="file-text")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="ql-card"><div class="ql-card-label">Optimal portfolio — top holdings</div>', unsafe_allow_html=True)
    st.dataframe(
        alloc_df(best).head(5).style.format({"Weight %": "{:.2f}%"}),
        use_container_width=True, hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="ql-card"><div class="ql-card-label">Minimum-risk portfolio — top holdings</div>', unsafe_allow_html=True)
    st.dataframe(
        alloc_df(low_risk).head(5).style.format({"Weight %": "{:.2f}%"}),
        use_container_width=True, hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

ruler_rule()


# ==========================================================
# PDF Generation
# ==========================================================

def _asset_colors(n):
    palette = [COLORS["gold"], COLORS["blue"], COLORS["green"], COLORS["red"],
               "#7A6FA3", "#4A9C9E", "#B08A3E", "#6B7FB3", "#9B7EDE", "#5FA8D3"]
    return [palette[i % len(palette)] for i in range(n)]


def _make_donut_png(df) -> io.BytesIO:
    fig, ax = plt.subplots(figsize=(4.6, 3.6), dpi=170)
    fig.patch.set_alpha(0)
    colors_list = _asset_colors(len(df))

    # Only show a % label on wedges big enough for it to fit without overlapping;
    # small slices (which is what caused the earlier label pile-up) rely on the
    # legend instead of an on-wedge label.
    def _autopct(pct):
        return f"{pct:.1f}%" if pct >= 4 else ""

    wedges, texts, autotexts = ax.pie(
        df["Weight %"], labels=None, autopct=_autopct, startangle=90, pctdistance=0.78,
        colors=colors_list,
        wedgeprops=dict(width=0.42, edgecolor="#FFFFFF", linewidth=1.5),
        textprops={"fontsize": 8, "color": "#1A1F29"},
    )
    for at in autotexts:
        at.set_fontsize(7.5)
        at.set_color("#1A1F29")
        at.set_fontweight("bold")
    ax.set_aspect("equal")

    legend_labels = [f"{s}  {w:.1f}%" for s, w in zip(df["Stock"], df["Weight %"])]
    ax.legend(
        wedges, legend_labels, loc="center left", bbox_to_anchor=(1.02, 0.5),
        fontsize=7.5, frameon=False, labelspacing=0.6, handlelength=1.2, handleheight=1.2,
    )

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf


def _make_comparison_png(best_df, low_df) -> io.BytesIO:
    fig, ax = plt.subplots(figsize=(6.6, 2.9), dpi=170)
    fig.patch.set_alpha(0)
    x = range(len(best_df))
    width = 0.36
    ax.bar([i - width / 2 for i in x], best_df["Weight %"], width,
           label="Optimal", color=COLORS["gold"])
    ax.bar([i + width / 2 for i in x], low_df["Weight %"], width,
           label="Minimum Risk", color=COLORS["blue"])
    ax.set_xticks(list(x))
    ax.set_xticklabels(best_df["Stock"], fontsize=8, color="#1A1F29")
    ax.set_ylabel("Weight %", fontsize=8, color="#5A6270")
    ax.tick_params(axis="y", labelsize=7.5, colors="#5A6270")
    ax.legend(fontsize=8, frameon=False, loc="upper right")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#D9D9D9")
    ax.spines["bottom"].set_color("#D9D9D9")
    ax.set_facecolor("none")
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=170, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf


def build_pdf_report(best, low_risk) -> bytes:
    buffer = io.BytesIO()

    gold = colors.HexColor(COLORS["gold"])
    navy = colors.HexColor("#0B0E14")
    ink = colors.HexColor("#1A1F29")
    muted = colors.HexColor("#5A6270")
    faint = colors.HexColor("#8B93A1")
    hairline = colors.HexColor("#D9D9D9")
    zebra = colors.HexColor("#F5F5F3")

    def _draw_page_frame(canvas_obj, doc_obj):
        canvas_obj.saveState()
        page_w, page_h = letter
        banner_h = 0.72 * inch

        # Header banner
        canvas_obj.setFillColor(navy)
        canvas_obj.rect(0, page_h - banner_h, page_w, banner_h, fill=1, stroke=0)
        canvas_obj.setFillColor(gold)
        canvas_obj.rect(0, page_h - banner_h - 3, page_w, 3, fill=1, stroke=0)

        canvas_obj.setFont("Helvetica-Bold", 16)
        canvas_obj.setFillColor(colors.white)
        canvas_obj.drawString(0.7 * inch, page_h - 0.44 * inch, "QUANT")
        w = canvas_obj.stringWidth("QUANT", "Helvetica-Bold", 16)
        canvas_obj.setFillColor(gold)
        canvas_obj.drawString(0.7 * inch + w, page_h - 0.44 * inch, "LAB")

        canvas_obj.setFont("Helvetica", 7.5)
        canvas_obj.setFillColor(colors.HexColor("#A8ADB8"))
        canvas_obj.drawString(0.7 * inch, page_h - 0.6 * inch, "Quantitative Investment Analytics Platform")

        canvas_obj.setFont("Helvetica", 7.5)
        canvas_obj.setFillColor(colors.HexColor("#A8ADB8"))
        canvas_obj.drawRightString(page_w - 0.7 * inch, page_h - 0.44 * inch, "Portfolio Optimization Report")
        canvas_obj.drawRightString(page_w - 0.7 * inch, page_h - 0.6 * inch, f"Generated {generated_at}")

        # Footer
        canvas_obj.setStrokeColor(gold)
        canvas_obj.setLineWidth(0.75)
        canvas_obj.line(0.7 * inch, 0.55 * inch, page_w - 0.7 * inch, 0.55 * inch)
        canvas_obj.setFont("Helvetica", 7.5)
        canvas_obj.setFillColor(faint)
        canvas_obj.drawString(0.7 * inch, 0.38 * inch,
                               "QuantLab · Quantitative Investment Analytics Platform · For internal use only")
        canvas_obj.drawRightString(page_w - 0.7 * inch, 0.38 * inch, f"Page {canvas_obj.getPageNumber()}")
        canvas_obj.restoreState()

    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        topMargin=0.85 * inch, bottomMargin=0.55 * inch,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
    )

    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        "QLBody", parent=styles["Normal"], fontName="Helvetica",
        fontSize=9.5, textColor=ink, leading=15, spaceAfter=10,
    )
    heading_style = ParagraphStyle(
        "QLHeading", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=13, textColor=ink, spaceBefore=10, spaceAfter=5,
    )
    caption_style = ParagraphStyle(
        "QLCaption", parent=styles["Normal"], fontName="Helvetica-Oblique",
        fontSize=8, textColor=muted, spaceAfter=12, alignment=1,
    )
    meta_style = ParagraphStyle(
        "QLMeta", parent=styles["Normal"], fontName="Helvetica",
        fontSize=9, textColor=muted,
    )
    bullet_style = ParagraphStyle(
        "QLBullet", parent=styles["Normal"], fontName="Helvetica",
        fontSize=9.5, textColor=ink, leading=14.5, spaceAfter=8,
        leftIndent=14, bulletIndent=0,
    )

    best_df = alloc_df(best)
    low_df = alloc_df(low_risk).set_index("Stock").loc[best_df["Stock"]].reset_index()
    top3 = ", ".join(best_df["Stock"].head(3).tolist())
    return_gap = best["return"] - low_risk["return"]
    risk_gap = best["risk"] - low_risk["risk"]

    story = []

    # ---- Executive summary ----
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(
        f"The optimal (max-Sharpe) portfolio targets an expected annual return of "
        f"<b>{best['return']:.2%}</b> at <b>{best['risk']:.2%}</b> volatility "
        f"(Sharpe ratio {best['sharpe']:.2f}), concentrated primarily in {top3}. "
        f"The minimum-risk alternative trades {return_gap:+.2%} in expected return for a "
        f"{-risk_gap:+.2%} change in volatility, spreading exposure more evenly across the "
        f"{len(best_df)}-asset universe. Both candidates are drawn from the same Monte Carlo "
        f"efficient-frontier simulation.",
        body_style,
    ))

    # ---- KPI table ----
    story.append(Paragraph("Portfolio Summary", heading_style))
    kpi_data = [
        ["Metric", "Optimal (Max Sharpe)", "Minimum Risk"],
        ["Expected Return", f"{best['return']:.2%}", f"{low_risk['return']:.2%}"],
        ["Portfolio Risk", f"{best['risk']:.2%}", f"{low_risk['risk']:.2%}"],
        ["Sharpe Ratio", f"{best['sharpe']:.2f}", f"{low_risk['sharpe']:.2f}"],
    ]
    kpi_table = Table(kpi_data, colWidths=[2.2 * inch, 2.15 * inch, 2.15 * inch])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), navy),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, zebra]),
        ("GRID", (0, 0), (-1, -1), 0.5, hairline),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 4))

    # ---- Key Insights (computed, not generic filler) ----
    low_sorted = alloc_df(low_risk)  # independently sorted, before we reindex low_df to match best_df's order below
    top1_stock, top1_weight = best_df.iloc[0]["Stock"], best_df.iloc[0]["Weight %"]
    top3_weight = best_df["Weight %"].head(3).sum()
    lr_top1_stock, lr_top1_weight = low_sorted.iloc[0]["Stock"], low_sorted.iloc[0]["Weight %"]
    lr_top3_weight = low_sorted["Weight %"].head(3).sum()
    sharpe_gap = best["sharpe"] - low_risk["sharpe"]

    story.append(Paragraph("Key Insights", heading_style))

    insights = [
        f"<b>Why the optimal portfolio wins on Sharpe:</b> it scores {best['sharpe']:.2f} vs. "
        f"{low_risk['sharpe']:.2f} for the minimum-risk portfolio ({sharpe_gap:+.2f}) by concentrating "
        f"{top3_weight:.1f}% of capital in its top 3 holdings ({top3}) — assets whose return/volatility "
        f"profile in this sample data offers the best reward per unit of risk. Its single largest position "
        f"is <b>{top1_stock}</b> at {top1_weight:.1f}%.",

        f"<b>Why the minimum-risk portfolio is lower-risk:</b> it spreads capital far more evenly — its "
        f"largest position ({lr_top1_stock}) is only {lr_top1_weight:.1f}% (vs. {top1_weight:.1f}% for the "
        f"optimal portfolio), and its top 3 holdings hold {lr_top3_weight:.1f}% combined (vs. {top3_weight:.1f}%). "
        f"That diversification is what pulls annualized volatility down to {low_risk['risk']:.2%}, at the cost "
        f"of {-return_gap:.2%} lower expected return.",

        (
            f"<b>The risk/return trade-off:</b> moving from the minimum-risk to the optimal portfolio adds "
            f"{return_gap:.2%} expected return for {risk_gap:.2%} additional volatility — roughly "
            f"{(return_gap / risk_gap):.2f}% of extra return per 1% of extra risk taken on."
            if risk_gap > 0 else
            f"<b>The risk/return trade-off:</b> the optimal portfolio delivers both a higher expected return "
            f"({best['return']:.2%} vs. {low_risk['return']:.2%}) and no higher volatility than the "
            f"minimum-risk portfolio in this sample — it dominates on both axes."
        ),

        f"<b>Who each fits:</b> the optimal (max-Sharpe) allocation suits an investor prioritizing "
        f"risk-adjusted growth and comfortable with concentration in a handful of names. The minimum-risk "
        f"allocation suits an investor prioritizing capital preservation and broader diversification over "
        f"squeezing out the last percentage point of return.",
    ]

    for point in insights:
        story.append(Paragraph(f"•  {point}", bullet_style))

    story.append(Paragraph(
        "This report is generated automatically from historical simulation data for informational purposes "
        "only and does not constitute financial advice.",
        caption_style,
    ))
    story.append(Spacer(1, 10))

    # ---- Report contents box (fills remaining page-1 space with something useful
    #      instead of leaving a large dead gap above the footer) ----
    contents_header = Table(
        [["What's in this report"]],
        colWidths=[6.6 * inch],
    )
    contents_header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), navy),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ]))

    contents_style = ParagraphStyle(
        "QLContents", parent=styles["Normal"], fontName="Helvetica",
        fontSize=9.5, textColor=ink, leading=14,
    )
    contents_num_style = ParagraphStyle(
        "QLContentsNum", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=9.5, textColor=gold, leading=14,
    )
    contents_rows = [
        ["01", "Portfolio Summary", "Headline return, risk, and Sharpe ratio for both candidates"],
        ["02", "Key Insights", "Computed analysis of why each portfolio wins on its own metric"],
        ["03", "Optimal (Max Sharpe) Allocation", "Full holding-by-holding breakdown with donut chart"],
        ["04", "Minimum Risk Allocation", "Full holding-by-holding breakdown for the low-risk candidate"],
        ["05", "Weight Comparison", "Side-by-side chart of both portfolios across every holding"],
    ]
    contents_data = [
        [Paragraph(n, contents_num_style), Paragraph(f"<b>{t}</b>", contents_style), Paragraph(d, contents_style)]
        for n, t, d in contents_rows
    ]
    contents_table = Table(contents_data, colWidths=[0.4 * inch, 2.1 * inch, 4.1 * inch])
    contents_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, zebra]),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, hairline),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ]))

    wrapped_contents = Table(
        [[contents_header], [contents_table]],
        colWidths=[6.6 * inch],
    )
    wrapped_contents.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, hairline),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(wrapped_contents)

    # Page 2 always starts fresh with the allocation sections — explicit break
    # avoids the automatic-flow problem where a whole KeepTogether block gets
    # bumped to the next page and leaves a large dead gap behind on this one.
    story.append(PageBreak())

    # ---- Optimal allocation: donut chart + table side note ----
    # NOTE: each section below is wrapped in KeepTogether so a heading can never
    # get stranded alone at the bottom of a page while its chart/table jumps to
    # the next one — that orphaning was the main cause of the awkward layout.
    donut_buf = _make_donut_png(best_df)
    donut_img = Image(donut_buf, width=3.1 * inch, height=2.43 * inch)

    rows = [["Stock", "Weight %"]] + [
        [row["Stock"], f"{row['Weight %']:.2f}%"] for _, row in best_df.iterrows()
    ]
    alloc_table = Table(rows, colWidths=[1.55 * inch, 1.35 * inch])
    top_idx = best_df["Weight %"].idxmax()
    table_style = [
        ("BACKGROUND", (0, 0), (-1, 0), gold),
        ("TEXTCOLOR", (0, 0), (-1, 0), ink),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, zebra]),
        ("GRID", (0, 0), (-1, -1), 0.5, hairline),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4),
    ]
    table_style.append(("BACKGROUND", (0, top_idx + 1), (-1, top_idx + 1), colors.HexColor("#FBF0D6")))
    table_style.append(("FONTNAME", (0, top_idx + 1), (-1, top_idx + 1), "Helvetica-Bold"))
    alloc_table.setStyle(TableStyle(table_style))

    layout_table = Table(
        [[donut_img, alloc_table]],
        colWidths=[3.2 * inch, 2.9 * inch],
    )
    layout_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
    ]))
    story.append(KeepTogether([
        Paragraph("Optimal (Max Sharpe) — Allocation", heading_style),
        layout_table,
    ]))

    # ---- Minimum risk table ----
    rows_lr = [["Stock", "Weight %"]] + [
        [row["Stock"], f"{row['Weight %']:.2f}%"] for _, row in low_df.iterrows()
    ]
    lr_table = Table(rows_lr, colWidths=[3.05 * inch, 3.05 * inch])
    lr_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(COLORS["blue"])),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, zebra]),
        ("GRID", (0, 0), (-1, -1), 0.5, hairline),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4),
    ]))
    story.append(KeepTogether([
        Paragraph("Minimum Risk — Allocation", heading_style),
        lr_table,
    ]))

    # ---- Comparison chart ----
    comp_buf = _make_comparison_png(best_df, low_df)
    comp_img = Image(comp_buf, width=6.3 * inch, height=2.15 * inch)
    methodology_para = Paragraph(
        "Methodology: Monte Carlo simulation over randomly weighted portfolios across the tracked "
        f"asset universe ({len(best_df)} assets), optimizing for maximum Sharpe ratio and minimum "
        "annualized volatility respectively under Modern Portfolio Theory.",
        caption_style,
    )
    story.append(KeepTogether([
        Paragraph("Optimal vs. Minimum Risk — Weight Comparison", heading_style),
        comp_img,
        Spacer(1, 4),
        methodology_para,
    ]))

    doc.build(story, onFirstPage=_draw_page_frame, onLaterPages=_draw_page_frame)
    return buffer.getvalue()


# ==========================================================
# Export Actions — Preview first, download only after review
# ==========================================================

section_title("Export", "Review & Download the Full Report", icon="download")

# session state so the generated PDF survives reruns (e.g. clicking Download)
# without being rebuilt from scratch every time.
if "ql_pdf_bytes" not in st.session_state:
    st.session_state.ql_pdf_bytes = None
if "ql_pdf_generated_at" not in st.session_state:
    st.session_state.ql_pdf_generated_at = None

st.markdown(
    """
    <div class="ql-card" style="padding:18px 20px; margin-bottom:14px;">
        <div class="ql-card-label" style="margin-bottom:4px;">Step 1 · Generate & review</div>
        <div style="font-size:13px; color:#5A6270;">
            Build the full PDF and preview it below before downloading — nothing is
            saved to your device until you're happy with it.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

gen_col, status_col = st.columns([1, 3])
with gen_col:
    generate_clicked = st.button(
        "🔍  Generate & Preview Report",
        use_container_width=True,
        type="primary",
    )

if generate_clicked:
    with st.spinner("Building your report..."):
        st.session_state.ql_pdf_bytes = build_pdf_report(best, low_risk)
        st.session_state.ql_pdf_generated_at = datetime.now()

with status_col:
    if st.session_state.ql_pdf_bytes:
        stamp = st.session_state.ql_pdf_generated_at.strftime("%b %d, %Y · %H:%M")
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; height:100%; padding-top:6px;
                        font-size:13px; color:#2E7D32;">
                ✅&nbsp; Report ready — generated {stamp}. Scroll down to review it.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---- Preview panel (only shown once a report has been generated) ----
if st.session_state.ql_pdf_bytes:
    ruler_rule()
    section_title("Preview", "Report Preview — Review Before Downloading", icon="eye")

    b64_pdf = base64.b64encode(st.session_state.ql_pdf_bytes).decode("utf-8")
    st.markdown(
        f"""
        <div style="border:1px solid #D9D9D9; border-radius:14px; overflow:hidden;
                    box-shadow:0 2px 14px rgba(0,0,0,0.06); margin-bottom:16px;">
            <iframe
                src="data:application/pdf;base64,{b64_pdf}"
                width="100%"
                height="820"
                style="border:none; display:block;"
                type="application/pdf">
            </iframe>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="ql-card" style="padding:16px 20px; margin-bottom:8px;">
            <div class="ql-card-label" style="margin-bottom:4px;">Step 2 · Happy with it?</div>
            <div style="font-size:13px; color:#5A6270;">
                Download the PDF below, or click <b>Generate &amp; Preview Report</b>
                again after making changes upstream to refresh it.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    dl_col1, dl_col2, dl_col3 = st.columns(3)

    with dl_col1:
        st.download_button(
            "📄  Download PDF report",
            data=st.session_state.ql_pdf_bytes,
            file_name=f"quantlab_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )

    with dl_col2:
        combined = pd.concat(
            [alloc_df(best).assign(Portfolio="Optimal"),
             alloc_df(low_risk).assign(Portfolio="Minimum Risk")],
            ignore_index=True,
        )
        st.download_button(
            "📊  Download CSV (both portfolios)",
            data=combined.to_csv(index=False),
            file_name=f"quantlab_allocations_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with dl_col3:
        st.download_button(
            "🥇  Download optimal only (CSV)",
            data=alloc_df(best).to_csv(index=False),
            file_name=f"quantlab_optimal_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
        )
else:
    st.info(
        "Click **Generate & Preview Report** above to build the PDF and review it "
        "here before downloading.",
        icon="ℹ️",
    )


footer("QuantLab · Quantitative Investment Analytics Platform")