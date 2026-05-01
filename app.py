import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroWave, Sleep & Consciousness",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── ROOT VARIABLES ── */
:root {
    --bg:         #080b14;
    --bg2:        #0d1221;
    --bg3:        #111827;
    --border:     rgba(99,102,241,0.18);
    --indigo:     #6366f1;
    --cyan:       #06b6d4;
    --emerald:    #10b981;
    --amber:      #f59e0b;
    --violet:     #8b5cf6;
    --text:       #e2e8f0;
    --muted:      #64748b;
    --card:       rgba(13,18,33,0.85);
}

/* ── BASE ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(99,102,241,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(6,182,212,0.08) 0%, transparent 60%),
        var(--bg);
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    font-family: 'DM Mono', monospace !important;
}

/* ── HIDE DEFAULT STREAMLIT CHROME ── */
footer { visibility: hidden; }
[data-testid="stStatusWidget"] { visibility: hidden; }
.block-container { padding-top: 2rem !important; }

/* ── RADIO BUTTONS (NAV) ── */
div[role="radiogroup"] label {
    display: flex !important;
    align-items: center !important;
    padding: 10px 14px !important;
    margin: 4px 0 !important;
    border-radius: 8px !important;
    border: 1px solid transparent !important;
    transition: all 0.2s ease !important;
    font-size: 13px !important;
    letter-spacing: 0.03em !important;
    color: var(--muted) !important;
    cursor: pointer !important;
}

div[role="radiogroup"] label:hover {
    background: rgba(99,102,241,0.08) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

div[role="radiogroup"] label[data-checked="true"],
div[role="radiogroup"] label:has(input:checked) {
    background: rgba(99,102,241,0.15) !important;
    border-color: rgba(99,102,241,0.4) !important;
    color: #a5b4fc !important;
}

/* ── CARDS ── */
.nw-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 32px;
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
}

.nw-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(99,102,241,0.04) 0%, transparent 60%);
    pointer-events: none;
}

/* ── METRIC CARDS ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 24px 0;
}

.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease;
}

.metric-card:hover { border-color: rgba(99,102,241,0.4); }

.metric-card .accent-line {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}

.metric-card .metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 6px;
}

.metric-card .metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
}

/* ── HERO ── */
.hero-section {
    padding: 48px 0 32px;
    position: relative;
}

.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--indigo);
    margin-bottom: 16px;
    opacity: 0.9;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.02em;
    margin-bottom: 8px;
}

.hero-title .gradient-text {
    background: linear-gradient(135deg, #6366f1 0%, #06b6d4 50%, #10b981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 17px;
    line-height: 1.7;
    color: var(--muted);
    max-width: 640px;
    margin-bottom: 32px;
    font-weight: 300;
}

/* ── STAGE BADGES ── */
.stage-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.05em;
    margin: 3px;
}

/* ── PHILOSOPHICAL QUOTE ── */
.phil-quote {
    border-left: 2px solid var(--indigo);
    padding: 16px 24px;
    margin: 24px 0;
    font-style: italic;
    font-size: 15px;
    line-height: 1.8;
    color: #94a3b8;
    background: rgba(99,102,241,0.04);
    border-radius: 0 12px 12px 0;
}

/* ── SECTION HEADERS ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 4px;
    letter-spacing: -0.01em;
}

.section-sub {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 20px;
}

/* ── DATA TABLE ── */
.dataframe {
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
}

/* ── DIVIDER ── */
.nw-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 32px 0;
}

/* ── PLOTLY CHART CONTAINERS ── */
.js-plotly-plot {
    border-radius: 12px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)


# ── DATA LOADER ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("sleep_eeg_features.csv")
    return df


# ── SIDEBAR NAVIGATION ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 28px;'>
        <div style='font-family: Syne, sans-serif; font-size: 18px; font-weight: 800;
                    letter-spacing: -0.01em; color: #e2e8f0; margin-bottom: 4px;'>
            🧠 NeuroWave
        </div>
        <div style='font-family: DM Mono, monospace; font-size: 10px;
                    letter-spacing: 0.15em; text-transform: uppercase;
                    color: #6366f1; opacity: 0.9;'>
            Sleep & Consciousness
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family: DM Mono, monospace; font-size: 10px;
                letter-spacing: 0.12em; text-transform: uppercase;
                color: #64748b; margin-bottom: 8px; padding-left: 2px;'>
        Navigation
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        label="nav",
        options=[
            "🏠  Overview",
            "📊  Statistical Analysis",
            "🎲  Probability & Distributions",
            "🔮  Prediction Model",
        ],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: rgba(99,102,241,0.15); margin: 24px 0;'>",
                unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family: DM Mono, monospace; font-size: 10px;
                color: #334155; line-height: 1.8; padding: 0 2px;'>
        <div style='color: #475569; margin-bottom: 8px; letter-spacing: 0.08em;
                    text-transform: uppercase;'>Dataset</div>
        <a href="https://physionet.org/content/sleep-edfx/1.0.0/">View the Sleep-EDF Database</a><br>
        Sleep-EDF · PhysioNet<br>
        82 Subjects · Clinical EEG<br>
        5 Sleep Stages · EEG Band Powers<br><br>
        <div style='color: #475569; margin-bottom: 8px; letter-spacing: 0.08em;
                    text-transform: uppercase;'>Course</div>
        Probability & Statistics<br>
        Spring 2026 · FAST-NUCES
    </div>
    """, unsafe_allow_html=True)


# ── PAGE ROUTER ─────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
#  PAGE 1, OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠  Overview":

    df = load_data()

    # ── HERO ──
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-eyebrow'>⬡ Probability & Statistics · Spring 2026</div>
        <div class='hero-title'>
            Neuro<span class='gradient-text'>Wave</span>
        </div>
        <div style='font-family: DM Mono, monospace; font-size: 13px;
                    letter-spacing: 0.1em; color: #6366f1; margin-bottom: 20px;'>
            SLEEP & CONSCIOUSNESS ANALYSIS
        </div>
        <div class='hero-subtitle'>
            Every night, your brain dissolves consciousness and reconstructs it
            following a structured, measurable architecture. We analyzed
            clinical EEG recordings from 82 subjects to map that journey
            and expose one of neuroscience's most striking paradoxes.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PHILOSOPHICAL QUOTE ──
    st.markdown("""
    <div class='phil-quote'>
        "Is consciousness a binary switch or a spectrum the brain traverses every night?
        Our data reveals the boundary between waking and dreaming is thinner than we ever imagined."
    </div>
    """, unsafe_allow_html=True)

    # ── DATASET METRICS ──
    total_epochs   = len(df)
    total_minutes  = round(total_epochs * 0.5)
    total_hours    = round(total_minutes / 60, 1)
    n_subjects     = df["subject_id"].nunique()
    n_features     = len(df.columns)
    rem_pct        = round((df["sleep_stage"] == "REM").mean() * 100, 1)

    st.markdown(f"""
    <div class='metric-grid'>
        <div class='metric-card'>
            <div class='accent-line' style='background: linear-gradient(90deg, #6366f1, #8b5cf6);'></div>
            <div class='metric-value' style='color: #a5b4fc;'>{n_subjects}</div>
            <div class='metric-label'>Clinical Subjects</div>
        </div>
        <div class='metric-card'>
            <div class='accent-line' style='background: linear-gradient(90deg, #06b6d4, #10b981);'></div>
            <div class='metric-value' style='color: #67e8f9;'>{total_epochs:,}</div>
            <div class='metric-label'>EEG Epochs (30s each)</div>
        </div>
        <div class='metric-card'>
            <div class='accent-line' style='background: linear-gradient(90deg, #10b981, #06b6d4);'></div>
            <div class='metric-value' style='color: #6ee7b7;'>{total_hours:,}</div>
            <div class='metric-label'>Total Hours Recorded</div>
        </div>
        <div class='metric-card'>
            <div class='accent-line' style='background: linear-gradient(90deg, #f59e0b, #ef4444);'></div>
            <div class='metric-value' style='color: #fcd34d;'>{rem_pct}%</div>
            <div class='metric-label'>Time in REM State</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)

    # ── TWO COLUMN LAYOUT ──
    # ── HYPNOGRAM FULL WIDTH ──
    st.markdown("""
    <div class='section-header'>Sleep Architecture</div>
    <div class='section-sub'>The Hypnogram, Consciousness Through A Single Night</div>
    """, unsafe_allow_html=True)

    subjects = sorted(df["subject_id"].unique())
    selected = st.selectbox(
        "Select Subject",
        subjects,
        format_func=lambda x: f"Subject {x:02d}",
        label_visibility="collapsed"
    )

    sub_df = df[df["subject_id"] == selected].sort_values("epoch_start").copy()
    stage_order = {"Wake": 4, "REM": 3, "N1": 2, "N2": 1, "N3": 0}
    stage_colors = {
        "Wake": "#f59e0b",
        "REM":  "#6366f1",
        "N1":   "#06b6d4",
        "N2":   "#10b981",
        "N3":   "#1e40af"
    }

    sub_df["stage_num"]   = sub_df["sleep_stage"].map(stage_order)
    sub_df["epoch_hours"] = sub_df["epoch_start"] / 3600

    fig_hyp = go.Figure()

    for stage, color in stage_colors.items():
        mask = sub_df["sleep_stage"] == stage
        fig_hyp.add_trace(go.Scatter(
            x=sub_df.loc[mask, "epoch_hours"],
            y=sub_df.loc[mask, "stage_num"],
            mode="markers",
            marker=dict(color=color, size=3, symbol="square"),
            name=stage,
            hovertemplate=f"<b>{stage}</b><br>Time: %{{x:.2f}}h<extra></extra>"
        ))

    fig_hyp.add_trace(go.Scatter(
        x=sub_df["epoch_hours"],
        y=sub_df["stage_num"],
        mode="lines",
        line=dict(color="rgba(148,163,184,0.25)", width=1),
        showlegend=False,
        hoverinfo="skip"
    ))

    fig_hyp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,18,33,0.6)",
        font=dict(family="DM Mono", color="#94a3b8", size=11),
        xaxis=dict(
            title="Hours into Night",
            gridcolor="rgba(99,102,241,0.08)",
            showgrid=True,
            zeroline=False,
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            tickvals=list(stage_order.values()),
            ticktext=list(stage_order.keys()),
            gridcolor="rgba(99,102,241,0.08)",
            showgrid=True,
            zeroline=False,
            tickfont=dict(size=11)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left",   x=0,
            font=dict(size=10),
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        height=380,
    )

    st.plotly_chart(fig_hyp, use_container_width=True, config={"displayModeBar": False})

    # Subject mini stats
    if "age" in df.columns and "gender" in df.columns:
        sub_age    = int(sub_df["age"].iloc[0]) if "age" in sub_df.columns else "N/A"
        sub_gender = "Female" if sub_df["gender"].iloc[0] == 1 else "Male"
        sub_rem    = round((sub_df["sleep_stage"] == "REM").mean() * 100, 1)
        sub_n3     = round((sub_df["sleep_stage"] == "N3").mean()  * 100, 1)
        sub_eff    = round((sub_df["sleep_stage"] != "Wake").mean() * 100, 1)

        st.markdown(f"""
        <div style='display:flex; gap:12px; flex-wrap:wrap; margin-top:8px; margin-bottom:32px;'>
            <div style='font-family: DM Mono, monospace; font-size:11px;
                        color:#64748b; background:rgba(13,18,33,0.8);
                        border:1px solid rgba(99,102,241,0.15);
                        border-radius:8px; padding:8px 14px;'>
                Age: <span style='color:#a5b4fc'>{sub_age}</span>
            </div>
            <div style='font-family: DM Mono, monospace; font-size:11px;
                        color:#64748b; background:rgba(13,18,33,0.8);
                        border:1px solid rgba(99,102,241,0.15);
                        border-radius:8px; padding:8px 14px;'>
                Gender: <span style='color:#a5b4fc'>{sub_gender}</span>
            </div>
            <div style='font-family: DM Mono, monospace; font-size:11px;
                        color:#64748b; background:rgba(13,18,33,0.8);
                        border:1px solid rgba(99,102,241,0.15);
                        border-radius:8px; padding:8px 14px;'>
                REM: <span style='color:#6366f1'>{sub_rem}%</span>
            </div>
            <div style='font-family: DM Mono, monospace; font-size:11px;
                        color:#64748b; background:rgba(13,18,33,0.8);
                        border:1px solid rgba(99,102,241,0.15);
                        border-radius:8px; padding:8px 14px;'>
                N3: <span style='color:#1e40af'>{sub_n3}%</span>
            </div>
            <div style='font-family: DM Mono, monospace; font-size:11px;
                        color:#64748b; background:rgba(13,18,33,0.8);
                        border:1px solid rgba(99,102,241,0.15);
                        border-radius:8px; padding:8px 14px;'>
                Efficiency: <span style='color:#10b981'>{sub_eff}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)

    # ── PIE CHART + LEGEND SIDE BY SIDE BELOW ──
    st.markdown("""
    <div class='section-header'>Consciousness Distribution</div>
    <div class='section-sub'>How Awareness Splits Across The Night, All 82 Subjects</div>
    """, unsafe_allow_html=True)

    col_pie, col_legend = st.columns([1, 1], gap="large")

    with col_pie:
        stage_counts = df["sleep_stage"].value_counts().reset_index()
        stage_counts.columns = ["stage", "epochs"]
        stage_counts["minutes"] = stage_counts["epochs"] * 0.5

        color_map = {
            "Wake": "#f59e0b",
            "N1":   "#06b6d4",
            "N2":   "#10b981",
            "N3":   "#1e40af",
            "REM":  "#6366f1"
        }

        fig_pie = go.Figure(data=go.Pie(
            labels=stage_counts["stage"],
            values=stage_counts["minutes"],
            hole=0.55,
            marker=dict(
                colors=[color_map.get(s, "#64748b") for s in stage_counts["stage"]],
                line=dict(color="#080b14", width=2)
            ),
            textinfo="label+percent",
            textfont=dict(family="DM Mono", size=11, color="#e2e8f0"),
            hovertemplate="<b>%{label}</b><br>%{value:.0f} minutes<br>%{percent}<extra></extra>"
        ))

        fig_pie.add_annotation(
            text="All<br>Subjects",
            x=0.5, y=0.5,
            font=dict(family="DM Mono", size=11, color="#64748b"),
            showarrow=False
        )

        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
        )

        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    with col_legend:
        st.markdown("<div style='padding-top: 24px;'>", unsafe_allow_html=True)
        stage_info = {
            "Wake": ("#f59e0b", "Fully conscious, externally aware"),
            "N1":   ("#06b6d4", "Dissolution threshold, consciousness fading"),
            "N2":   ("#10b981", "Light sleep, brain actively blocks sensation"),
            "N3":   ("#1e40af", "Deep slow-wave, most unconscious state"),
            "REM":  ("#6366f1", "Paradox, brain awake, body paralyzed, dreaming"),
        }
        for stage, (color, desc) in stage_info.items():
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:12px;
                        padding: 12px 0; border-bottom:1px solid rgba(99,102,241,0.08);'>
                <div style='width:10px; height:10px; border-radius:3px;
                            background:{color}; flex-shrink:0;'></div>
                <div style='font-family:Syne,sans-serif; font-size:13px;
                            font-weight:600; color:#e2e8f0; min-width:40px;'>{stage}</div>
                <div style='font-family:DM Sans,sans-serif; font-size:12px;
                            color:#64748b; line-height:1.4;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        

    # ── DATASET OVERVIEW TABLE ──
    st.markdown("""
    <div class='section-header'>Dataset Overview</div>
    <div class='section-sub'>Per-Subject Summary, Sleep Architecture Breakdown</div>
    """, unsafe_allow_html=True)

    agg_dict = {
        "total_epochs": ("sleep_stage", "count"),
        "wake_pct":     ("sleep_stage", lambda x: round((x=="Wake").mean()*100, 1)),
        "n1_pct":       ("sleep_stage", lambda x: round((x=="N1").mean()*100, 1)),
        "n2_pct":       ("sleep_stage", lambda x: round((x=="N2").mean()*100, 1)),
        "n3_pct":       ("sleep_stage", lambda x: round((x=="N3").mean()*100, 1)),
        "rem_pct":      ("sleep_stage", lambda x: round((x=="REM").mean()*100, 1)),
    }

    if "age" in df.columns:
        agg_dict["age"]    = ("age", "first")
    if "gender" in df.columns:
        agg_dict["gender"] = ("gender", lambda x: "F" if x.iloc[0]==1 else "M")

    summary = df.groupby("subject_id").agg(**agg_dict).reset_index()

    summary = summary.rename(columns={
        "subject_id":   "Subject",
        "total_epochs": "Epochs",
        "wake_pct":     "Wake %",
        "n1_pct":       "N1 %",
        "n2_pct":       "N2 %",
        "n3_pct":       "N3 %",
        "rem_pct":      "REM %",
        "age":          "Age",
        "gender":       "Sex"
    })

    col_order = ["Subject"]
    if "Age" in summary.columns:    col_order.append("Age")
    if "Sex" in summary.columns:    col_order.append("Sex")
    col_order += ["Epochs", "Wake %", "N1 %", "N2 %", "N3 %", "REM %"]
    summary = summary[[c for c in col_order if c in summary.columns]]

    st.dataframe(
        summary,
        use_container_width=True,
        height=340,
        hide_index=True,
        column_config={
            "REM %": st.column_config.ProgressColumn(
                "REM %", min_value=0, max_value=17.2, format="%.1f%%"
            ),
            "N3 %": st.column_config.ProgressColumn(
                "N3 %", min_value=0, max_value=51.2, format="%.1f%%"
            ),
        }
    )

    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)

    # ── ABOUT SECTION ──
    st.markdown("""
    <div class='section-header'>About This Project</div>
    <div class='section-sub'>Research Context & Philosophical Framing</div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="large")

    with c1:
        st.markdown("""
        <div class='nw-card'>
            <div style='font-size:24px; margin-bottom:12px;'>🔬</div>
            <div style='font-family:Syne,sans-serif; font-size:15px;
                        font-weight:700; margin-bottom:10px; color:#e2e8f0;'>
                The Data
            </div>
            <div style='font-size:13px; color:#64748b; line-height:1.7;'>
                Sleep-EDF dataset from PhysioNet, 82 subjects with clinical
                overnight EEG recordings. Each 30-second epoch is annotated
                with expert-scored sleep stages and EEG band power features
                extracted across 5 frequency domains.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='nw-card'>
            <div style='font-size:24px; margin-bottom:12px;'>🧠</div>
            <div style='font-family:Syne,sans-serif; font-size:15px;
                        font-weight:700; margin-bottom:10px; color:#e2e8f0;'>
                The Paradox
            </div>
            <div style='font-size:13px; color:#64748b; line-height:1.7;'>
                REM sleep brain activity is electrically indistinguishable
                from waking consciousness, yet you are unaware of the external
                world and generating a complete internal reality. Our statistical
                analysis makes this paradox quantitatively visible.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class='nw-card'>
            <div style='font-size:24px; margin-bottom:12px;'>📐</div>
            <div style='font-family:Syne,sans-serif; font-size:15px;
                        font-weight:700; margin-bottom:10px; color:#e2e8f0;'>
                The Question
            </div>
            <div style='font-size:13px; color:#64748b; line-height:1.7;'>
                How does the architecture of consciousness change with age?
                We use regression modeling to show that REM sleep, the
                brain's nightly construction of inner reality, measurably
                diminishes as we grow older.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  PAGE 2, STATISTICAL ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📊  Statistical Analysis":
 
    df = load_data()
 
    bands        = ["delta_relative","theta_relative","alpha_relative",
                    "beta_relative","gamma_relative"]
    band_labels  = ["Delta","Theta","Alpha","Beta","Gamma"]
    stage_order  = ["Wake","N1","N2","N3","REM"]
    stage_colors = {
        "Wake":"#f59e0b","N1":"#06b6d4",
        "N2":"#10b981","N3":"#1e40af","REM":"#6366f1"
    }
 
    # ── HERO ──
    st.markdown("""
    <div class='hero-section' style='padding: 32px 0 24px;'>
        <div class='hero-eyebrow'>⬡ Page 2 of 4</div>
        <div class='hero-title' style='font-size: 42px;'>
            Statistical <span class='gradient-text'>Analysis</span>
        </div>
        <div class='hero-subtitle'>
            Descriptive measures, confidence intervals, and band power
            distributions across all five consciousness states.
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    # ── SECTION 1, HEATMAP ─────────────────────────────────────────────────
    st.markdown("""
    <div class='section-header'>Brainwave Power Heatmap</div>
    <div class='section-sub'>Mean Relative Band Power Per Sleep Stage</div>
    """, unsafe_allow_html=True)
 
    matrix = []
    for stage in stage_order:
        row = df[df["sleep_stage"]==stage][bands].mean().values
        matrix.append(row)
    matrix = np.array(matrix).round(4)
 
    fig_heat = go.Figure(data=go.Heatmap(
        z=matrix,
        x=band_labels,
        y=stage_order,
        colorscale=[
            [0.0,  "#0d1221"],
            [0.3,  "#1e3a5f"],
            [0.6,  "#2563eb"],
            [0.85, "#6366f1"],
            [1.0,  "#a5b4fc"]
        ],
        text=[[f"{v:.4f}" for v in row] for row in matrix],
        texttemplate="%{text}",
        textfont=dict(family="DM Mono", size=12, color="#e2e8f0"),
        showscale=True,
        colorbar=dict(
            tickfont=dict(family="DM Mono", size=10, color="#64748b"),
            outlinewidth=0,
            thickness=12,
        ),
        hovertemplate="<b>%{y}, %{x}</b><br>Relative Power: %{z:.4f}<extra></extra>"
    ))
 
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,18,33,0.6)",
        font=dict(family="DM Mono", color="#94a3b8", size=12),
        xaxis=dict(side="top", tickfont=dict(size=12, color="#e2e8f0")),
        yaxis=dict(tickfont=dict(size=12, color="#e2e8f0"), autorange="reversed"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=320,
    )
 
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})
 
    # Heatmap insights
    st.markdown("""
    <div class='nw-card' style='margin: 4px 0 32px;'>
        <div style='font-family: DM Mono, monospace; font-size: 10px; letter-spacing: 0.15em;
                    text-transform: uppercase; color: #6366f1; margin-bottom: 12px;'>
            🔍 Key Insight, The REM Paradox
        </div>
        <div style='font-size: 13px; color: #94a3b8; line-height: 1.8;'>
            The Delta Dominance (0.9011 in N3): This is the biggest "tell." N3 is Deep Sleep, also known as Slow Wave Sleep (SWS). It is defined by high-amplitude, low-frequency Delta waves. Seeing nearly 90% of the power in the Delta band for N3 is exactly what you'd expect.<br>
            Theta Peak in REM (0.1672): REM sleep is often characterized by "sawtooth" waves and high Theta activity. Your heatmap shows Theta at its highest relative power during REM compared to any other stage, which is spot on.<br>
            Beta/Gamma in Wake: Notice that the higher frequencies (Beta and Gamma) are at their absolute peak while the subject is Wake. This reflects active processing and consciousness.<br>
            The Gradient of Deepening Sleep: Look at the Delta column. It climbs steadily from Wake (0.60) -> N1 -> N2 -> N3 (0.90), showing the brain slowing down as it descends into deep sleep.<br>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)
 
    # ── SECTION 2, BOX PLOTS ───────────────────────────────────────────────
    st.markdown("""
    <div class='section-header'>Band Power Distribution by Stage</div>
    <div class='section-sub'>Select a Frequency Band to Explore Its Behaviour Across Consciousness States</div>
    """, unsafe_allow_html=True)
 
    selected_band = st.radio(
        "Band",
        options=bands,
        format_func=lambda x: x.replace("_relative","").title(),
        horizontal=True,
        label_visibility="collapsed"
    )
 
    band_display = selected_band.replace("_relative","").title()
 
    fig_box = go.Figure()
    for stage in stage_order:
        stage_data = df[df["sleep_stage"]==stage][selected_band].dropna()
        fig_box.add_trace(go.Box(
            y=stage_data,
            name=stage,
            marker_color=stage_colors[stage],
            line=dict(color=stage_colors[stage], width=1.5),
            fillcolor=stage_colors[stage].replace("#","rgba(").replace(
                "f59e0b","245,158,11,0.15)").replace(
                "06b6d4","6,182,212,0.15)").replace(
                "10b981","16,185,129,0.15)").replace(
                "1e40af","30,64,175,0.15)").replace(
                "6366f1","99,102,241,0.15)"),
            boxmean=True,
            hovertemplate=f"<b>%{{x}}</b><br>{band_display}: %{{y:.4f}}<extra></extra>"
        ))
 
    fig_box.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,18,33,0.6)",
        font=dict(family="DM Mono", color="#94a3b8", size=11),
        yaxis=dict(
            title=f"{band_display} Relative Power",
            gridcolor="rgba(99,102,241,0.08)",
            zeroline=False
        ),
        xaxis=dict(gridcolor="rgba(99,102,241,0.08)"),
        showlegend=False,
        margin=dict(l=10, r=10, t=20, b=10),
        height=360,
    )
 
    st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})
 
    # Dynamic insight per band
    band_insights = {
        "delta_relative": (
            "Delta dominates N3 at <strong style='color:#a5b4fc;'>0.901</strong>, "
            "nine-tenths of all brain electrical activity is slow synchronized waves. "
            "This is the brain in its most unconscious configuration. "
            "Crucially, N3 also has the <strong style='color:#a5b4fc;'>lowest standard deviation (0.062)</strong> "
            "of any stage, deep sleep is the brain's most consistent, predictable state. "
            "REM delta (0.676) sits higher than Wake (0.604), suggesting the dreaming brain "
            "carries more slow-wave activity than commonly assumed."
        ),
        "theta_relative": (
            "Theta is highest in REM at <strong style='color:#a5b4fc;'>0.167</strong>, "
            "the dreaming brain's dominant rhythm. The hippocampus, which consolidates memory, "
            "runs on theta frequencies. This explains why REM sleep is so critical for "
            "memory integration: the same rhythm active during memory retrieval while awake "
            "dominates the brain's nightly replay. "
            "N1's elevated theta (0.134) marks the exact moment consciousness begins dissolving, "
            "the threshold crossing is measurable."
        ),
        "alpha_relative": (
            "Alpha is the <strong style='color:#a5b4fc;'>wakefulness marker</strong>, "
            "highest in Wake (0.085) and nearly absent in N3 (0.022). "
            "The key finding: REM alpha (0.063) is significantly lower than Wake alpha (0.085). "
            "This single difference is what statistically separates the two most similar brain states. "
            "Alpha represents the idling conscious brain. Its suppression in REM means "
            "the dreaming brain is not 'idling', it is fully occupied generating internal experience, "
            "with no bandwidth left for external monitoring."
        ),
        "beta_relative": (
            "Beta power confirms active cognition, highest in Wake (0.116) and "
            "dramatically lowest in N3 (0.011). "
            "The REM beta value (0.061) sits at roughly <strong style='color:#a5b4fc;'>half of waking beta</strong>, "
            "suggesting the dreaming brain is cognitively active but not at full waking capacity. "
            "This partial beta suppression during REM may explain the characteristic dream quality, "
            "vivid and emotionally intense, but with reduced logical coherence and critical thinking."
        ),
        "gamma_relative": (
            "Gamma is the most philosophically loaded band. "
            "Associated with sensory binding, the brain integrating separate inputs into unified conscious experience. "
            "Wake gamma (0.101) is <strong style='color:#a5b4fc;'>three times higher than REM gamma (0.032)</strong>. "
            "This is the clearest measurable difference between waking and dreaming consciousness. "
            "The external world requires active binding. Internal dream reality apparently does not, "
            "or uses a different mechanism. N3 gamma (0.008) is near zero: "
            "in deep sleep, the binding process that creates unified experience essentially stops."
        ),
    }
 
    st.markdown(f"""
    <div class='nw-card' style='margin: 4px 0 32px;'>
        <div style='font-family: DM Mono, monospace; font-size: 10px; letter-spacing: 0.15em;
                    text-transform: uppercase; color: #06b6d4; margin-bottom: 12px;'>
            🔍 {band_display} Band, Insight
        </div>
        <div style='font-size: 13px; color: #94a3b8; line-height: 1.8;'>
            {band_insights[selected_band]}
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)
 
    # ── SECTION 3, DESCRIPTIVE STATS TABLE ─────────────────────────────────
    st.markdown("""
    <div class='section-header'>Descriptive Statistics</div>
    <div class='section-sub'>Mean · Median · Std Dev · Skewness · Kurtosis, Per Stage Per Band</div>
    """, unsafe_allow_html=True)
 
    stage_filter = st.selectbox(
        "Filter by Stage",
        ["All Stages"] + stage_order,
        label_visibility="collapsed"
    )
 
    desc_rows = []
    for stage in stage_order:
        stage_df = df[df["sleep_stage"]==stage]
        for band, label in zip(bands, band_labels):
            data = stage_df[band].dropna()
            desc_rows.append({
                "Stage":    stage,
                "Band":     label,
                "Mean":     round(data.mean(),   4),
                "Median":   round(data.median(), 4),
                "Std Dev":  round(data.std(),    4),
                "Min":      round(data.min(),    4),
                "Max":      round(data.max(),    4),
                "Skewness": round(data.skew(),   4),
                "Kurtosis": round(data.kurtosis(), 4),
                "N Epochs": len(data),
            })
 
    desc_df = pd.DataFrame(desc_rows)
    if stage_filter != "All Stages":
        desc_df = desc_df[desc_df["Stage"] == stage_filter]
 
    st.dataframe(
        desc_df,
        use_container_width=True,
        hide_index=True,
        height=300,
    )
 
    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)
 
    # ── SECTION 4, CONFIDENCE INTERVALS ────────────────────────────────────
    st.markdown("""
    <div class='section-header'>Confidence Intervals</div>
    <div class='section-sub'>95% CI on Mean Band Power, How Reliable Are Our Stage Estimates?</div>
    """, unsafe_allow_html=True)
 
    from scipy import stats as scipy_stats
 
    ci_rows = []
    for stage in stage_order:
        stage_df = df[df["sleep_stage"]==stage]
        for band, label in zip(bands, band_labels):
            data = stage_df[band].dropna()
            n    = len(data)
            mean = data.mean()
            se   = scipy_stats.sem(data)
            ci   = scipy_stats.t.interval(0.95, df=n-1, loc=mean, scale=se)
            ci_rows.append({
                "Stage":    stage,
                "Band":     label,
                "Mean":     round(mean,   4),
                "CI Lower": round(ci[0],  4),
                "CI Upper": round(ci[1],  4),
                "Margin":   round(ci[1]-mean, 5),
                "N Epochs": n,
            })
 
    ci_df = pd.DataFrame(ci_rows)
 
    # CI bar chart, select band
    ci_band = st.selectbox(
        "Select band for CI chart",
        options=list(zip(bands, band_labels)),
        format_func=lambda x: x[1],
        label_visibility="collapsed"
    )
 
    ci_plot = ci_df[ci_df["Band"] == ci_band[1]].copy()
 
    fig_ci = go.Figure()
    for _, row in ci_plot.iterrows():
        color = stage_colors[row["Stage"]]
        fig_ci.add_trace(go.Bar(
            x=[row["Stage"]],
            y=[row["Mean"]],
            error_y=dict(
                type="data",
                array=[row["CI Upper"] - row["Mean"]],
                arrayminus=[row["Mean"] - row["CI Lower"]],
                visible=True,
                color="rgba(255,255,255,0.4)",
                thickness=2,
                width=8
            ),
            marker=dict(
                color=color,
                opacity=0.85,
                line=dict(color=color, width=1)
            ),
            name=row["Stage"],
            hovertemplate=(
                f"<b>{row['Stage']}</b><br>"
                f"Mean: {row['Mean']:.4f}<br>"
                f"95% CI: [{row['CI Lower']:.4f}, {row['CI Upper']:.4f}]"
                "<extra></extra>"
            )
        ))
 
    fig_ci.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,18,33,0.6)",
        font=dict(family="DM Mono", color="#94a3b8", size=11),
        yaxis=dict(
            title=f"{ci_band[1]} Relative Power",
            gridcolor="rgba(99,102,241,0.08)",
            zeroline=False
        ),
        xaxis=dict(gridcolor="rgba(99,102,241,0.08)"),
        showlegend=False,
        bargap=0.35,
        margin=dict(l=10, r=10, t=20, b=10),
        height=340,
    )
 
    st.plotly_chart(fig_ci, use_container_width=True, config={"displayModeBar": False})
 
    # CI table
    st.dataframe(
        ci_df,
        use_container_width=True,
        hide_index=True,
        height=280,
    )
 
    st.markdown("""
    <div class='nw-card' style='margin: 16px 0 32px;'>
        <div style='font-family: DM Mono, monospace; font-size: 10px; letter-spacing: 0.15em;
                    text-transform: uppercase; color: #10b981; margin-bottom: 12px;'>
            🔍 Insight, Confidence & Consistency
        </div>
        <div style='font-size: 13px; color: #94a3b8; line-height: 1.8;'>
            N3 consistently produces the <strong style='color:#e2e8f0;'>narrowest confidence intervals</strong>
            across all bands, meaning deep sleep is the most statistically reliable brain state.
            When the brain enters deep unconsciousness, it does so with remarkable uniformity across subjects.
            Wake and REM produce the widest intervals, conscious and dreaming states vary
            significantly between individuals, reflecting personal differences in alertness, stress,
            and dream intensity. This variability itself is a finding:
            <strong style='color:#a5b4fc;'>unconsciousness is uniform, consciousness is individual.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)
 
    # ── SECTION 5, REM % BY AGE GROUP CI ───────────────────────────────────
    st.markdown("""
    <div class='section-header'>REM Sleep Across Age Groups</div>
    <div class='section-sub'>95% Confidence Intervals on Mean REM %, Does Consciousness Diminish With Age?</div>
    """, unsafe_allow_html=True)
 
    subject_data = df.groupby("subject_id").apply(lambda x: pd.Series({
        "age":     x["age"].iloc[0]     if "age"    in x.columns else np.nan,
        "rem_pct": (x["sleep_stage"]=="REM").mean() * 100,
    })).reset_index().dropna()
 
    bins   = [20, 35, 50, 65, 120]
    labels = ["20–35", "36–50", "51–65", "65+"]
    subject_data["age_group"] = pd.cut(
        subject_data["age"], bins=bins, labels=labels
    )
 
    age_ci_rows = []
    for g in labels:
        d = subject_data[subject_data["age_group"]==g]["rem_pct"].dropna()
        if len(d) < 2:
            continue
        mean = d.mean()
        ci   = scipy_stats.t.interval(
            0.95, df=len(d)-1, loc=mean, scale=scipy_stats.sem(d)
        )
        age_ci_rows.append({
            "Age Group":   g,
            "N Subjects":  len(d),
            "Mean REM %":  round(mean,   2),
            "CI Lower":    round(ci[0],  2),
            "CI Upper":    round(ci[1],  2),
            "CI Width":    round(ci[1]-ci[0], 2),
        })
 
    age_ci_df = pd.DataFrame(age_ci_rows)
 
    fig_age_ci = go.Figure()
 
    colors_age = ["#06b6d4","#6366f1","#8b5cf6","#f59e0b"]
    for i, row in age_ci_df.iterrows():
        c = colors_age[i % len(colors_age)]
        fig_age_ci.add_trace(go.Scatter(
            x=[row["Age Group"]],
            y=[row["Mean REM %"]],
            error_y=dict(
                type="data",
                array=[row["CI Upper"] - row["Mean REM %"]],
                arrayminus=[row["Mean REM %"] - row["CI Lower"]],
                visible=True,
                color=c,
                thickness=2.5,
                width=14
            ),
            mode="markers",
            marker=dict(color=c, size=12, symbol="circle"),
            name=row["Age Group"],
            hovertemplate=(
                f"<b>{row['Age Group']} years</b><br>"
                f"Mean REM: {row['Mean REM %']:.2f}%<br>"
                f"95% CI: [{row['CI Lower']:.2f}%, {row['CI Upper']:.2f}%]<br>"
                f"n = {row['N Subjects']} subjects"
                "<extra></extra>"
            )
        ))
 
    fig_age_ci.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,18,33,0.6)",
        font=dict(family="DM Mono", color="#94a3b8", size=11),
        yaxis=dict(
            title="Mean REM %",
            gridcolor="rgba(99,102,241,0.08)",
            zeroline=False,
            range=[0, 16]
        ),
        xaxis=dict(
            title="Age Group",
            gridcolor="rgba(99,102,241,0.08)"
        ),
        showlegend=False,
        margin=dict(l=10, r=10, t=20, b=10),
        height=320,
    )
 
    st.plotly_chart(fig_age_ci, use_container_width=True, config={"displayModeBar": False})
 
    col_t, col_i = st.columns([1, 1], gap="large")
 
    with col_t:
        st.dataframe(age_ci_df, use_container_width=True, hide_index=True)
 
    with col_i:
        st.markdown("""
        <div class='nw-card' style='height: 100%;'>
            <div style='font-family: DM Mono, monospace; font-size: 10px; letter-spacing: 0.15em;
                        text-transform: uppercase; color: #f59e0b; margin-bottom: 12px;'>
                🔍 Insight, Age & The Dreaming Mind
            </div>
            <div style='font-size: 13px; color: #94a3b8; line-height: 1.8;'>
                The data shows a clear downward trend,
                <strong style='color:#e2e8f0;'>subjects aged 20–35 average 7.47% REM</strong>
                while those aged 65+ average only 5.32%.
                That is a <strong style='color:#a5b4fc;'>29% relative reduction</strong>
                in consciousness-rich sleep across a lifetime.
                The brain's nightly capacity to generate internal reality,
                vivid, emotional, narratively coherent, measurably contracts with age.
                The confidence intervals confirm this is a real effect,
                not statistical noise.
            </div>
        </div>
        """, unsafe_allow_html=True)
 
 
# ════════════════════════════════════════════════════════════════════════════
#  PAGE 3, PROBABILITY & DISTRIBUTIONS
# ════════════════════════════════════════════════════════════════════════════
elif page == "🎲  Probability & Distributions":
 
    df = load_data()
    from scipy import stats as scipy_stats
 
    stage_order  = ["Wake","N1","N2","N3","REM"]
    stage_colors = {
        "Wake":"#f59e0b","N1":"#06b6d4",
        "N2":"#10b981","N3":"#1e40af","REM":"#6366f1"
    }
    bands       = ["delta_relative","theta_relative","alpha_relative",
                   "beta_relative","gamma_relative"]
    band_labels = ["Delta","Theta","Alpha","Beta","Gamma"]
 
    # ── HERO ──
    st.markdown("""
    <div class='hero-section' style='padding: 32px 0 24px;'>
        <div class='hero-eyebrow'>⬡ Page 3 of 4</div>
        <div class='hero-title' style='font-size: 42px;'>
            Probability <span class='gradient-text'>&amp; Distributions</span>
        </div>
        <div class='hero-subtitle'>
            How does the sleeping brain transition between states?
            What distributions govern its behaviour? And what does
            probability theory reveal about consciousness and age?
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    # ── SECTION 1, TRANSITION MATRIX ───────────────────────────────────────
    st.markdown("""
    <div class='section-header'>Sleep Stage Transition Matrix</div>
    <div class='section-sub'>Probability of Moving From One Consciousness State to Another</div>
    """, unsafe_allow_html=True)
 
    # Build transition matrix from data
    transitions = pd.DataFrame(0, index=stage_order, columns=stage_order)
    for subject in df["subject_id"].unique():
        sub    = df[df["subject_id"]==subject].sort_values("epoch_start")
        stages = sub["sleep_stage"].values
        for i in range(len(stages)-1):
            f, t = stages[i], stages[i+1]
            if f in stage_order and t in stage_order:
                transitions.loc[f, t] += 1
 
    probs = transitions.div(transitions.sum(axis=1), axis=0).round(3)
 
    fig_trans = go.Figure(data=go.Heatmap(
        z=probs.values,
        x=[f"→ {s}" for s in stage_order],
        y=stage_order,
        colorscale=[
            [0.0,  "#0d1221"],
            [0.2,  "#0f2d4a"],
            [0.5,  "#1d4ed8"],
            [0.8,  "#6366f1"],
            [1.0,  "#a5b4fc"],
        ],
        text=[[f"{v:.3f}" for v in row] for row in probs.values],
        texttemplate="%{text}",
        textfont=dict(family="DM Mono", size=12, color="#e2e8f0"),
        showscale=True,
        colorbar=dict(
            tickfont=dict(family="DM Mono", size=10, color="#64748b"),
            outlinewidth=0, thickness=12,
            title=dict(text="P", font=dict(color="#64748b", size=11))
        ),
        hovertemplate="<b>%{y} → %{x}</b><br>Probability: %{z:.3f}<extra></extra>"
    ))
 
    fig_trans.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,18,33,0.6)",
        font=dict(family="DM Mono", color="#94a3b8", size=12),
        xaxis=dict(side="top", tickfont=dict(size=12, color="#e2e8f0")),
        yaxis=dict(tickfont=dict(size=12, color="#e2e8f0"),
                   title="From Stage", autorange="reversed"),
        margin=dict(l=10, r=10, t=50, b=10),
        height=340,
    )
 
    st.plotly_chart(fig_trans, use_container_width=True,
                    config={"displayModeBar": False})
 
    # Transition table
    probs_display = probs.copy()
    probs_display.index.name = "From \\ To"
    st.dataframe(probs_display, use_container_width=True)
 
    # Key transitions highlighted
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        st.markdown("""
        <div class='nw-card'>
            <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.15em;
                        text-transform:uppercase; color:#06b6d4; margin-bottom:10px;'>
                Wake → N1
            </div>
            <div style='font-family:Syne,sans-serif; font-size:36px; font-weight:800;
                        color:#a5b4fc; margin-bottom:8px;'>83.7%</div>
            <div style='font-size:12px; color:#64748b; line-height:1.7;'>
                When consciousness begins dissolving, the brain almost always
                passes through N1 first. The threshold is rarely skipped.
                Falling asleep is a structured process, not a sudden drop.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='nw-card'>
            <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.15em;
                        text-transform:uppercase; color:#1e40af; margin-bottom:10px;'>
                N3 → Wake
            </div>
            <div style='font-family:Syne,sans-serif; font-size:36px; font-weight:800;
                        color:#a5b4fc; margin-bottom:8px;'>4.2%</div>
            <div style='font-size:12px; color:#64748b; line-height:1.7;'>
                Deep unconsciousness almost never exits directly to full awareness.
                The brain climbs back gradually through N2 (47.6%) first,
                consciousness reassembles in stages, not all at once.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='nw-card'>
            <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.15em;
                        text-transform:uppercase; color:#6366f1; margin-bottom:10px;'>
                REM → Wake
            </div>
            <div style='font-family:Syne,sans-serif; font-size:36px; font-weight:800;
                        color:#a5b4fc; margin-bottom:8px;'>33.5%</div>
            <div style='font-size:12px; color:#64748b; line-height:1.7;'>
                REM is the most volatile state, one in three REM epochs
                transitions directly to wakefulness. The dreaming brain
                sits closest to the surface of consciousness.
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown("""
    <div class='nw-card' style='margin: 20px 0 32px;'>
        <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.15em;
                    text-transform:uppercase; color:#6366f1; margin-bottom:12px;'>
            🔍 Insight, Consciousness Is Probabilistic, Not Binary
        </div>
        <div style='font-size:13px; color:#94a3b8; line-height:1.8;'>
            The transition matrix reveals that <strong style='color:#e2e8f0;'>no stage
            exits to another with 100% certainty.</strong> Every transition is probabilistic.
            The brain doesn't decide to sleep, it drifts according to likelihoods shaped
            by biological rhythms. The near-zero N3→REM probability (0.008) confirms
            that deep unconsciousness and dreaming are the most separated states,
            the brain never jumps directly from its deepest unconscious configuration
            into its most vivid internal reality. It always climbs back through intermediate
            states first. <strong style='color:#a5b4fc;'>Consciousness is not a switch.
            It is a Markov chain.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)
 
    # ── SECTION 2, BAND POWER DISTRIBUTIONS ────────────────────────────────
    st.markdown("""
    <div class='section-header'>Empirical Band Power Distributions</div>
    <div class='section-sub'>Histogram + KDE, How Each Brainwave Band Distributes Across Epochs</div>
    """, unsafe_allow_html=True)
 
    col_sel1, col_sel2 = st.columns([1, 1], gap="large")
    with col_sel1:
        dist_band = st.selectbox(
            "Select Band",
            options=list(zip(bands, band_labels)),
            format_func=lambda x: x[1],
            label_visibility="collapsed",
            key="dist_band"
        )
    with col_sel2:
        dist_stage = st.selectbox(
            "Select Stage",
            options=["All Stages"] + stage_order,
            label_visibility="collapsed",
            key="dist_stage"
        )
 
    plot_df = df.copy()
    if dist_stage != "All Stages":
        plot_df = df[df["sleep_stage"] == dist_stage]
 
    fig_dist = go.Figure()
 
    if dist_stage == "All Stages":
        for stage in stage_order:
            data = df[df["sleep_stage"]==stage][dist_band[0]].dropna()
            fig_dist.add_trace(go.Histogram(
                x=data,
                name=stage,
                opacity=0.6,
                nbinsx=60,
                marker_color=stage_colors[stage],
                histnorm="probability density",
                hovertemplate=f"<b>{stage}</b><br>{dist_band[1]}: %{{x:.3f}}<extra></extra>"
            ))
        fig_dist.update_layout(barmode="overlay")
    else:
        data  = plot_df[dist_band[0]].dropna()
        color = stage_colors.get(dist_stage, "#6366f1")
        fig_dist.add_trace(go.Histogram(
            x=data,
            name=dist_stage,
            opacity=0.7,
            nbinsx=60,
            marker_color=color,
            histnorm="probability density",
            hovertemplate=f"<b>{dist_stage}</b><br>{dist_band[1]}: %{{x:.3f}}<extra></extra>"
        ))
        # KDE overlay
        from scipy.stats import gaussian_kde
        kde    = gaussian_kde(data)
        x_range = np.linspace(data.min(), data.max(), 300)
        fig_dist.add_trace(go.Scatter(
            x=x_range, y=kde(x_range),
            mode="lines",
            line=dict(color="white", width=2, dash="dot"),
            name="KDE",
            hoverinfo="skip"
        ))
 
    fig_dist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,18,33,0.6)",
        font=dict(family="DM Mono", color="#94a3b8", size=11),
        xaxis=dict(
            title=f"{dist_band[1]} Relative Power",
            gridcolor="rgba(99,102,241,0.08)", zeroline=False
        ),
        yaxis=dict(
            title="Probability Density",
            gridcolor="rgba(99,102,241,0.08)", zeroline=False
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="left", x=0, bgcolor="rgba(0,0,0,0)",
            font=dict(size=10)
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        height=360,
    )
 
    st.plotly_chart(fig_dist, use_container_width=True,
                    config={"displayModeBar": False})
 
    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)
 
    # ── SECTION 3, NORMALITY TESTS ──────────────────────────────────────────
    st.markdown("""
    <div class='section-header'>Normality Testing</div>
    <div class='section-sub'>Shapiro-Wilk Test, Are EEG Band Powers Normally Distributed?</div>
    """, unsafe_allow_html=True)
 
    norm_rows = []
    for stage in stage_order:
        stage_df = df[df["sleep_stage"]==stage]
        for band, label in zip(bands, band_labels):
            data   = stage_df[band].dropna()
            sample = data[:5000]
            w, p   = scipy_stats.shapiro(sample)
            norm_rows.append({
                "Stage":     stage,
                "Band":      label,
                "W Stat":    round(w, 4),
                "P-Value":   round(p, 6),
                "Normal?":  "✅ Yes" if p > 0.05 else "❌ No",
                "N Epochs":  len(data),
            })
 
    norm_df = pd.DataFrame(norm_rows)
 
    # Summary metric
    n_normal    = (norm_df["Normal?"] == "✅ Yes").sum()
    n_total     = len(norm_df)
    n_not_normal = n_total - n_normal
 
    m1, m2, m3 = st.columns(3, gap="large")
    with m1:
        st.markdown(f"""
        <div class='metric-card' style='text-align:center; padding:20px;'>
            <div class='accent-line' style='background:linear-gradient(90deg,#ef4444,#f59e0b);'></div>
            <div class='metric-value' style='color:#fca5a5; font-size:40px;'>{n_not_normal}</div>
            <div class='metric-label'>Non-Normal Distributions</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class='metric-card' style='text-align:center; padding:20px;'>
            <div class='accent-line' style='background:linear-gradient(90deg,#10b981,#06b6d4);'></div>
            <div class='metric-value' style='color:#6ee7b7; font-size:40px;'>{n_normal}</div>
            <div class='metric-label'>Normal Distributions</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class='metric-card' style='text-align:center; padding:20px;'>
            <div class='accent-line' style='background:linear-gradient(90deg,#6366f1,#8b5cf6);'></div>
            <div class='metric-value' style='color:#a5b4fc; font-size:40px;'>{n_total}</div>
            <div class='metric-label'>Total Tests Run</div>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    norm_stage_filter = st.selectbox(
        "Filter by stage",
        ["All Stages"] + stage_order,
        label_visibility="collapsed",
        key="norm_filter"
    )
    norm_display = norm_df if norm_stage_filter == "All Stages" \
                   else norm_df[norm_df["Stage"] == norm_stage_filter]
 
    st.dataframe(norm_display, use_container_width=True,
                 hide_index=True, height=280)
 
    st.markdown("""
    <div class='nw-card' style='margin: 16px 0 32px;'>
        <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.15em;
                    text-transform:uppercase; color:#ef4444; margin-bottom:12px;'>
            🔍 Insight, The Brain Does Not Follow a Bell Curve
        </div>
        <div style='font-size:13px; color:#94a3b8; line-height:1.8;'>
            <strong style='color:#e2e8f0;'>Every single distribution, all 25 stage-band
            combinations, failed the Shapiro-Wilk normality test.</strong>
            This is not a data quality issue. It is a fundamental finding about
            the nature of brain activity. EEG power distributions are heavy-tailed,
            skewed, and multimodal, reflecting the complex, nonlinear dynamics
            of neural systems. The brain does not produce normally distributed signals
            because it is not a simple random process.
            This has a direct statistical implication:
            <strong style='color:#a5b4fc;'>any analysis of this data must use
            non-parametric methods or robust statistics</strong>, not assumptions
            of normality. Our confidence intervals used the t-distribution with
            sufficient sample sizes, which remains valid via the Central Limit Theorem
            regardless of the underlying distribution shape.
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)
 
    # ── SECTION 4, DEEP SLEEP PROBABILITY BY AGE ───────────────────────────
    st.markdown("""
    <div class='section-header'>Probability of Healthy Deep Sleep by Age</div>
    <div class='section-sub'>P(N3 &gt; 15%) Across Age Groups, How Age Rewrites the Odds</div>
    """, unsafe_allow_html=True)
 
    subject_data = df.groupby("subject_id").apply(lambda x: pd.Series({
        "age":    x["age"].iloc[0] if "age" in x.columns else np.nan,
        "n3_pct": (x["sleep_stage"]=="N3").mean()*100,
        "rem_pct":(x["sleep_stage"]=="REM").mean()*100,
    })).reset_index().dropna()
 
    age_groups = {
        "Young\n(≤ 40)": subject_data[subject_data["age"] <= 40],
        "Middle\n(41–60)": subject_data[(subject_data["age"]>40) & (subject_data["age"]<=60)],
        "Older\n(> 60)": subject_data[subject_data["age"] > 60],
    }
 
    prob_rows = []
    for label, group in age_groups.items():
        n3   = group["n3_pct"]
        rem  = group["rem_pct"]
        prob_rows.append({
            "Age Group":          label.replace("\n"," "),
            "N Subjects":         len(group),
            "Mean N3 %":          round(n3.mean(), 2),
            "P(N3 > 15%)":        round((n3 > 15).mean() * 100, 1),
            "Mean REM %":         round(rem.mean(), 2),
            "P(REM > 8%)":        round((rem > 8).mean() * 100, 1),
        })
 
    prob_df = pd.DataFrame(prob_rows)
 
    # Two bar charts side by side
    col_p1, col_p2 = st.columns(2, gap="large")
 
    with col_p1:
        st.markdown("""
        <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.12em;
                    text-transform:uppercase; color:#64748b; margin-bottom:8px;'>
            P(N3 &gt; 15%), Healthy Deep Sleep
        </div>
        """, unsafe_allow_html=True)
 
        fig_p1 = go.Figure()
        colors_p = ["#06b6d4","#6366f1","#f59e0b"]
        for i, row in prob_df.iterrows():
            fig_p1.add_trace(go.Bar(
                x=[row["Age Group"]],
                y=[row["P(N3 > 15%)"]],
                marker=dict(
                    color=colors_p[i],
                    opacity=0.85,
                    line=dict(color=colors_p[i], width=1)
                ),
                text=f"{row['P(N3 > 15%)']}%",
                textposition="outside",
                textfont=dict(family="DM Mono", size=13, color="#e2e8f0"),
                name=row["Age Group"],
                hovertemplate=(
                    f"<b>{row['Age Group']}</b><br>"
                    f"P(N3>15%): {row['P(N3 > 15%)']}%<br>"
                    f"n = {row['N Subjects']} subjects"
                    "<extra></extra>"
                )
            ))
        fig_p1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(13,18,33,0.6)",
            font=dict(family="DM Mono", color="#94a3b8", size=11),
            yaxis=dict(
                title="Probability (%)",
                gridcolor="rgba(99,102,241,0.08)",
                zeroline=False, range=[0, 105]
            ),
            xaxis=dict(gridcolor="rgba(99,102,241,0.08)"),
            showlegend=False, bargap=0.4,
            margin=dict(l=10, r=10, t=20, b=10),
            height=320,
        )
        st.plotly_chart(fig_p1, use_container_width=True,
                        config={"displayModeBar": False})
 
    with col_p2:
        st.markdown("""
        <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.12em;
                    text-transform:uppercase; color:#64748b; margin-bottom:8px;'>
            P(REM &gt; 8%), Rich Dreaming Sleep
        </div>
        """, unsafe_allow_html=True)
 
        fig_p2 = go.Figure()
        for i, row in prob_df.iterrows():
            fig_p2.add_trace(go.Bar(
                x=[row["Age Group"]],
                y=[row["P(REM > 8%)"]],
                marker=dict(
                    color=colors_p[i],
                    opacity=0.85,
                    line=dict(color=colors_p[i], width=1)
                ),
                text=f"{row['P(REM > 8%)']}%",
                textposition="outside",
                textfont=dict(family="DM Mono", size=13, color="#e2e8f0"),
                name=row["Age Group"],
                hovertemplate=(
                    f"<b>{row['Age Group']}</b><br>"
                    f"P(REM>8%): {row['P(REM > 8%)']}%<br>"
                    f"n = {row['N Subjects']} subjects"
                    "<extra></extra>"
                )
            ))
        fig_p2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(13,18,33,0.6)",
            font=dict(family="DM Mono", color="#94a3b8", size=11),
            yaxis=dict(
                title="Probability (%)",
                gridcolor="rgba(99,102,241,0.08)",
                zeroline=False, range=[0, 105]
            ),
            xaxis=dict(gridcolor="rgba(99,102,241,0.08)"),
            showlegend=False, bargap=0.4,
            margin=dict(l=10, r=10, t=20, b=10),
            height=320,
        )
        st.plotly_chart(fig_p2, use_container_width=True,
                        config={"displayModeBar": False})
 
    st.dataframe(prob_df, use_container_width=True, hide_index=True)
 
    st.markdown("""
    <div class='nw-card' style='margin: 16px 0 0;'>
        <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.15em;
                    text-transform:uppercase; color:#f59e0b; margin-bottom:12px;'>
            🔍 Insight, The Probability of Restorative Sleep Collapses With Age
        </div>
        <div style='font-size:13px; color:#94a3b8; line-height:1.8;'>
            The most striking finding in this entire project is here.
            <strong style='color:#e2e8f0;'>A young subject (≤40) has an 88.2% chance
            of achieving healthy deep sleep (N3 &gt; 15%) on any given night.</strong>
            By the time a person is over 60, that probability collapses to
            <strong style='color:#fcd34d;'>36.4%</strong>, less than one in three nights.
            Deep sleep is where physical restoration happens, where growth hormone releases,
            where the brain clears metabolic waste through the glymphatic system.
            This is not just a sleep statistic.
            <strong style='color:#a5b4fc;'>It is a probabilistic statement about
            how ageing rewrites the brain's nightly relationship with unconsciousness,
            and by extension, with restoration, memory, and health.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
 


# ════════════════════════════════════════════════════════════════════════════
#  PAGE 4, PREDICTION MODEL
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔮  Prediction Model":
 
    df = load_data()
    import statsmodels.api as sm
    from scipy import stats as scipy_stats
 
    # ── BUILD SUBJECT-LEVEL DATA ─────────────────────────────────────────────
    subject_data = df.groupby("subject_id").apply(lambda x: pd.Series({
        "age":      x["age"].iloc[0]    if "age"    in x.columns else np.nan,
        "gender":   x["gender"].iloc[0] if "gender" in x.columns else np.nan,
        "rem_pct":  (x["sleep_stage"]=="REM").mean()  * 100,
        "n3_pct":   (x["sleep_stage"]=="N3").mean()   * 100,
        "n2_pct":   (x["sleep_stage"]=="N2").mean()   * 100,
        "wake_pct": (x["sleep_stage"]=="Wake").mean() * 100,
        "sleep_eff":(x["sleep_stage"]!="Wake").mean() * 100,
    })).reset_index().dropna()
 
    # Fix gender encoding 1/2 → 0/1
    subject_data["gender_bin"] = subject_data["gender"].map({1.0: 0, 2.0: 1})
 
    # ── FIT MODELS ───────────────────────────────────────────────────────────
    # Model 1, Simple: Age → REM
    X1      = sm.add_constant(subject_data[["age"]])
    m1      = sm.OLS(subject_data["rem_pct"], X1).fit()
 
    # Model 2, Multiple: Age + Gender + N3 → REM
    X2      = sm.add_constant(subject_data[["age","gender_bin","n3_pct"]])
    m2      = sm.OLS(subject_data["rem_pct"], X2).fit()
 
    # Model 3, Age → Sleep Efficiency (strongest model)
    X3      = sm.add_constant(subject_data[["age"]])
    m3      = sm.OLS(subject_data["sleep_eff"], X3).fit()
 
    # ── HERO ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class='hero-section' style='padding: 32px 0 24px;'>
        <div class='hero-eyebrow'>⬡ Page 4 of 4</div>
        <div class='hero-title' style='font-size: 42px;'>
            Prediction <span class='gradient-text'>Model</span>
        </div>
        <div class='hero-subtitle'>
            Can we predict how age reshapes the sleeping brain?
            Three regression models, from simple to multiple,
            quantify how a lifetime of ageing rewrites the nightly
            architecture of consciousness.
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    # ── SECTION 1, CORRELATION MATRIX ───────────────────────────────────────
    st.markdown("""
    <div class='section-header'>Correlation Matrix</div>
    <div class='section-sub'>Relationships Between Age, Sleep Stages & Efficiency, Before We Model</div>
    """, unsafe_allow_html=True)
 
    corr_vars = ["age","rem_pct","n3_pct","sleep_eff","wake_pct"]
    corr_labels = ["Age","REM %","N3 %","Sleep Eff.","Wake %"]
    corr_matrix = subject_data[corr_vars].corr().round(3)
 
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_labels,
        y=corr_labels,
        colorscale=[
            [0.0,  "#ef4444"],
            [0.25, "#7f1d1d"],
            [0.5,  "#0d1221"],
            [0.75, "#1e3a5f"],
            [1.0,  "#a5b4fc"],
        ],
        zmid=0,
        text=[[f"{v:.3f}" for v in row] for row in corr_matrix.values],
        texttemplate="%{text}",
        textfont=dict(family="DM Mono", size=13, color="#e2e8f0"),
        showscale=True,
        zmin=-1, zmax=1,
        colorbar=dict(
            tickfont=dict(family="DM Mono", size=10, color="#64748b"),
            outlinewidth=0, thickness=12,
        ),
        hovertemplate="<b>%{y} × %{x}</b><br>r = %{z:.3f}<extra></extra>"
    ))
 
    fig_corr.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,18,33,0.6)",
        font=dict(family="DM Mono", color="#94a3b8", size=12),
        xaxis=dict(tickfont=dict(size=12, color="#e2e8f0")),
        yaxis=dict(tickfont=dict(size=12, color="#e2e8f0"), autorange="reversed"),
        margin=dict(l=10, r=10, t=20, b=10),
        height=340,
    )
 
    st.plotly_chart(fig_corr, use_container_width=True,
                    config={"displayModeBar": False})
 
    # Correlation highlights
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        st.markdown("""
        <div class='nw-card'>
            <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.15em;
                        text-transform:uppercase; color:#ef4444; margin-bottom:10px;'>
                Age × Sleep Efficiency
            </div>
            <div style='font-family:Syne,sans-serif; font-size:36px; font-weight:800;
                        color:#fca5a5; margin-bottom:8px;'>−0.685</div>
            <div style='font-size:12px; color:#64748b; line-height:1.7;'>
                The strongest correlation in the dataset. As age increases,
                sleep efficiency falls sharply. Nearly 47% of efficiency
                variance is explained by age alone.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='nw-card'>
            <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.15em;
                        text-transform:uppercase; color:#10b981; margin-bottom:10px;'>
                N3 × Sleep Efficiency
            </div>
            <div style='font-family:Syne,sans-serif; font-size:36px; font-weight:800;
                        color:#6ee7b7; margin-bottom:8px;'>+0.810</div>
            <div style='font-size:12px; color:#64748b; line-height:1.7;'>
                Deep sleep and overall sleep quality are nearly the same thing.
                More N3 means better efficiency, the highest correlation
                in the entire matrix.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='nw-card'>
            <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.15em;
                        text-transform:uppercase; color:#6366f1; margin-bottom:10px;'>
                Age × N3
            </div>
            <div style='font-family:Syne,sans-serif; font-size:36px; font-weight:800;
                        color:#a5b4fc; margin-bottom:8px;'>−0.447</div>
            <div style='font-size:12px; color:#64748b; line-height:1.7;'>
                Age erodes deep sleep directly. The brain's capacity for
                its deepest unconscious state declines measurably and
                consistently across a lifetime.
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)
 
    # ── SECTION 2, MODEL SELECTOR ────────────────────────────────────────────
    st.markdown("""
    <div class='section-header'>Regression Models</div>
    <div class='section-sub'>Three Models, Simple to Multiple, Each Telling a Different Part of the Story</div>
    """, unsafe_allow_html=True)
 
    model_choice = st.radio(
        "model",
        options=[
            "Model 1, Age → REM %",
            "Model 2, Age + N3 + Gender → REM %",
            "Model 3, Age → Sleep Efficiency",
        ],
        horizontal=True,
        label_visibility="collapsed"
    )
 
    # ── MODEL STATS CARDS ────────────────────────────────────────────────────
    if model_choice == "Model 1, Age → REM %":
        model   = m1
        x_col   = "age"
        y_col   = "rem_pct"
        x_label = "Age (years)"
        y_label = "REM %"
        scatter_color = "#6366f1"
        model_insight = """
            Age alone is a <strong style='color:#e2e8f0;'>weak predictor of REM sleep</strong>
            (R²=0.047, p=0.155). The relationship exists, the negative coefficient confirms
            REM declines with age, but age alone explains less than 5% of REM variability.
            This is not a failure of the model. It is a finding: REM sleep is influenced by
            many factors beyond age, stress, medication, sleep disorders, individual biology.
            <strong style='color:#a5b4fc;'>The simple model correctly tells us that age
            matters, but does not act alone.</strong> This motivates the multiple regression.
        """
        sig_color = "#f59e0b"
        sig_text  = "Not Significant (p = 0.155)"
 
    elif model_choice == "Model 2, Age + N3 + Gender → REM %":
        model   = m2
        x_col   = "age"
        y_col   = "rem_pct"
        x_label = "Age (years)"
        y_label = "REM %"
        scatter_color = "#6366f1"
        model_insight = """
            Adding N3 percentage and gender transforms the model.
            <strong style='color:#e2e8f0;'>R² jumps from 0.047 to 0.330</strong>,
            the model now explains 33% of REM variance (adjusted R²=0.281).
            The overall model is highly significant (F=6.74, p=0.0008).
            Age becomes significant (p=0.002, coef=−0.070):
            every additional year of age reduces REM by 0.07 percentage points.
            N3 is also highly significant (p=0.000, coef=−0.124):
            deep sleep and REM compete, more N3 means less REM.
            Gender is not significant (p=0.517), partly due to encoding issues
            in the original dataset.
            <strong style='color:#a5b4fc;'>This is the project's primary model.</strong>
        """
        sig_color = "#10b981"
        sig_text  = "Significant (p = 0.0008)"
 
    else:
        model   = m3
        x_col   = "age"
        y_col   = "sleep_eff"
        x_label = "Age (years)"
        y_label = "Sleep Efficiency %"
        scatter_color = "#06b6d4"
        model_insight = """
            This is the strongest and cleanest model in the project.
            <strong style='color:#e2e8f0;'>Age alone explains 46.9% of sleep
            efficiency variance</strong> (R²=0.469, p&lt;0.0001).
            The intercept of 97.4 means a theoretical zero-year-old would have
            near-perfect sleep efficiency. Every year of age reduces sleep
            efficiency by <strong style='color:#67e8f9;'>0.29 percentage points</strong>.
            By age 70, predicted efficiency drops ~17 points from the young baseline.
            The brain's ability to sustain consolidated, uninterrupted sleep
            deteriorates with age in a measurable, linear fashion.
            <strong style='color:#a5b4fc;'>This is the most presentable
            finding for a public audience.</strong>
        """
        sig_color = "#10b981"
        sig_text  = "Highly Significant (p < 0.0001)"
 
    # Model stat cards
    r2      = round(model.rsquared, 3)
    adj_r2  = round(model.rsquared_adj, 3)
    f_stat  = round(model.fvalue, 3)
    f_p     = model.f_pvalue
    n_obs   = int(model.nobs)
 
    s1, s2, s3, s4 = st.columns(4, gap="large")
    for col, val, label, color in [
        (s1, f"{r2:.3f}",     "R-Squared",     "#6366f1"),
        (s2, f"{adj_r2:.3f}", "Adj. R-Squared","#06b6d4"),
        (s3, f"{f_stat:.2f}", "F-Statistic",   "#10b981"),
        (s4, f"{n_obs}",      "Observations",  "#f59e0b"),
    ]:
        col.markdown(f"""
        <div class='metric-card' style='text-align:center; padding:20px; margin-top:16px;'>
            <div class='accent-line'
                 style='background:linear-gradient(90deg,{color},{color}88);'></div>
            <div class='metric-value' style='color:{color}; font-size:30px;'>{val}</div>
            <div class='metric-label'>{label}</div>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown(f"""
    <div style='font-family:DM Mono,monospace; font-size:11px; letter-spacing:0.1em;
                color:{sig_color}; margin: 12px 0 20px; padding-left:4px;'>
        ● {sig_text}
    </div>
    """, unsafe_allow_html=True)
 
    # ── SCATTER + REGRESSION LINE ────────────────────────────────────────────
    x_data  = subject_data[x_col]
    y_data  = subject_data[y_col]
    x_range = np.linspace(x_data.min(), x_data.max(), 200)
 
    if model_choice == "Model 2, Age + N3 + Gender → REM %":
        mean_n3  = subject_data["n3_pct"].mean()
        mode_gen = subject_data["gender_bin"].mode()[0]
        X_line_df = pd.DataFrame({
            "const":      1.0,
            "age":        x_range,
            "gender_bin": mode_gen,
            "n3_pct":     mean_n3
        })
        y_pred_line = model.predict(X_line_df)
    else:
        X_line_df   = pd.DataFrame({"const": 1.0, "age": x_range})
        y_pred_line = model.predict(X_line_df)
 
    # Residuals for color coding
    if model_choice == "Model 2, Age + N3 + Gender → REM %":
        X_full   = sm.add_constant(
            subject_data[["age","gender_bin","n3_pct"]]
        )
    else:
        X_full   = sm.add_constant(subject_data[[x_col]])
    y_fitted     = model.predict(X_full)
    residuals    = y_data - y_fitted
    res_abs      = residuals.abs()
    res_norm     = (res_abs - res_abs.min()) / (res_abs.max() - res_abs.min())
 
    fig_reg = go.Figure()
 
    # Confidence band
    pred_summary  = model.get_prediction(X_line_df)
    pred_frame    = pred_summary.summary_frame(alpha=0.05)
 
    fig_reg.add_trace(go.Scatter(
        x=np.concatenate([x_range, x_range[::-1]]),
        y=np.concatenate([pred_frame["mean_ci_upper"],
                          pred_frame["mean_ci_lower"][::-1]]),
        fill="toself",
        fillcolor=f"rgba(99,102,241,0.08)",
        line=dict(color="rgba(0,0,0,0)"),
        name="95% CI Band",
        hoverinfo="skip"
    ))
 
    # Scatter points
    fig_reg.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode="markers",
        marker=dict(
            color=scatter_color,
            size=9,
            opacity=0.8,
            line=dict(color="white", width=0.5)
        ),
        name="Subjects",
        hovertemplate=(
            f"<b>Subject</b><br>"
            f"{x_label}: %{{x:.0f}}<br>"
            f"{y_label}: %{{y:.2f}}"
            "<extra></extra>"
        )
    ))
 
    # Regression line
    fig_reg.add_trace(go.Scatter(
        x=x_range,
        y=y_pred_line,
        mode="lines",
        line=dict(color="white", width=2.5),
        name="Regression Line",
        hoverinfo="skip"
    ))
 
    fig_reg.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,18,33,0.6)",
        font=dict(family="DM Mono", color="#94a3b8", size=11),
        xaxis=dict(
            title=x_label,
            gridcolor="rgba(99,102,241,0.08)",
            zeroline=False
        ),
        yaxis=dict(
            title=y_label,
            gridcolor="rgba(99,102,241,0.08)",
            zeroline=False
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="left",  x=0,
            bgcolor="rgba(0,0,0,0)", font=dict(size=10)
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        height=380,
    )
 
    st.plotly_chart(fig_reg, use_container_width=True,
                    config={"displayModeBar": False})
 
    # Coefficient table
    coef_rows = []
    for name, coef, pval, ci_lo, ci_hi, se in zip(
        model.params.index,
        model.params.values,
        model.pvalues.values,
        model.conf_int()[0].values,
        model.conf_int()[1].values,
        model.bse.values,
    ):
        coef_rows.append({
            "Variable":  name,
            "Coeff":     round(coef,  4),
            "Std Error": round(se,    4),
            "P-Value":   round(pval,  4),
            "CI Lower":  round(ci_lo, 4),
            "CI Upper":  round(ci_hi, 4),
            "Significant": "✅ Yes" if pval < 0.05 else "❌ No",
        })
 
    coef_df = pd.DataFrame(coef_rows)
    st.dataframe(coef_df, use_container_width=True, hide_index=True)
 
    st.markdown(f"""
    <div class='nw-card' style='margin: 16px 0 32px;'>
        <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.15em;
                    text-transform:uppercase; color:#6366f1; margin-bottom:12px;'>
            🔍 Model Insight
        </div>
        <div style='font-size:13px; color:#94a3b8; line-height:1.8;'>
            {model_insight.strip()}
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)
 
    # ── SECTION 3, RESIDUAL PLOT ─────────────────────────────────────────────
    st.markdown("""
    <div class='section-header'>Residual Analysis</div>
    <div class='section-sub'>Are the Model Errors Random?, Checking Regression Assumptions</div>
    """, unsafe_allow_html=True)
 
    col_r1, col_r2 = st.columns(2, gap="large")
 
    with col_r1:
        # Residuals vs Fitted
        fig_res = go.Figure()
        fig_res.add_hline(y=0, line=dict(color="rgba(255,255,255,0.2)",
                                          width=1, dash="dot"))
        fig_res.add_trace(go.Scatter(
            x=y_fitted, y=residuals,
            mode="markers",
            marker=dict(color="#6366f1", size=8, opacity=0.7,
                        line=dict(color="white", width=0.5)),
            hovertemplate="Fitted: %{x:.2f}<br>Residual: %{y:.2f}<extra></extra>",
            name="Residuals"
        ))
        fig_res.update_layout(
            title=dict(text="Residuals vs Fitted Values",
                       font=dict(family="DM Mono", size=12, color="#94a3b8")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(13,18,33,0.6)",
            font=dict(family="DM Mono", color="#94a3b8", size=11),
            xaxis=dict(title="Fitted Values",
                       gridcolor="rgba(99,102,241,0.08)", zeroline=False),
            yaxis=dict(title="Residuals",
                       gridcolor="rgba(99,102,241,0.08)", zeroline=False),
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10),
            height=300,
        )
        st.plotly_chart(fig_res, use_container_width=True,
                        config={"displayModeBar": False})
 
    with col_r2:
        # Residual histogram
        fig_rh = go.Figure()
        fig_rh.add_trace(go.Histogram(
            x=residuals,
            nbinsx=20,
            marker=dict(color="#06b6d4", opacity=0.75,
                        line=dict(color="#080b14", width=1)),
            histnorm="probability density",
            name="Residuals",
            hovertemplate="Residual: %{x:.2f}<br>Density: %{y:.3f}<extra></extra>"
        ))
        # Normal curve overlay
        from scipy.stats import gaussian_kde
        if len(residuals) > 3:
            kde_r   = gaussian_kde(residuals)
            xr      = np.linspace(residuals.min(), residuals.max(), 200)
            fig_rh.add_trace(go.Scatter(
                x=xr, y=kde_r(xr),
                mode="lines",
                line=dict(color="white", width=2, dash="dot"),
                name="KDE", hoverinfo="skip"
            ))
        fig_rh.update_layout(
            title=dict(text="Residual Distribution",
                       font=dict(family="DM Mono", size=12, color="#94a3b8")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(13,18,33,0.6)",
            font=dict(family="DM Mono", color="#94a3b8", size=11),
            xaxis=dict(title="Residual Value",
                       gridcolor="rgba(99,102,241,0.08)", zeroline=False),
            yaxis=dict(title="Density",
                       gridcolor="rgba(99,102,241,0.08)", zeroline=False),
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10),
            height=300,
        )
        st.plotly_chart(fig_rh, use_container_width=True,
                        config={"displayModeBar": False})
 
    st.markdown("""
    <div class='nw-card' style='margin: 4px 0 32px;'>
        <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.15em;
                    text-transform:uppercase; color:#06b6d4; margin-bottom:12px;'>
            🔍 Insight, Checking Model Honesty
        </div>
        <div style='font-size:13px; color:#94a3b8; line-height:1.8;'>
            A good regression model has <strong style='color:#e2e8f0;'>randomly scattered
            residuals</strong>, no systematic pattern. If residuals fan out or curve,
            the model is missing something. The residual histogram should approximate
            a normal distribution centered at zero, confirming errors are random noise,
            not structure the model failed to capture.
            These plots are your model's integrity check.
            <strong style='color:#a5b4fc;'>Presenting residual analysis shows statistical
            maturity, most undergraduate projects skip this entirely.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)
 
    # ── SECTION 4, INTERACTIVE PREDICTOR ────────────────────────────────────
    st.markdown("""
    <div class='section-header'>Sleep Quality Predictor</div>
    <div class='section-sub'>Enter Your Age, Get Your Predicted Sleep Efficiency</div>
    """, unsafe_allow_html=True)
 
    st.markdown("""
    <div style='font-size:13px; color:#64748b; margin-bottom:24px; line-height:1.7;'>
        Based on Model 3 (Age → Sleep Efficiency, R²=0.469).
        This is our strongest and most interpretable model.
        Prediction uses the formula:
        <span style='font-family:DM Mono,monospace; color:#a5b4fc;'>
        Sleep Efficiency = 97.41 − (0.290 × Age)
        </span>
    </div>
    """, unsafe_allow_html=True)
 
    col_in, col_out = st.columns([1, 1], gap="large")
 
    with col_in:
        pred_age = st.slider(
            "Your Age",
            min_value=20, max_value=90,
            value=25, step=1,
            label_visibility="visible"
        )
 
        predicted_eff = round(97.4077 - (0.2902 * pred_age), 1)
        predicted_eff = max(0, min(100, predicted_eff))
 
        # Confidence interval for prediction
        X_pred = pd.DataFrame({"const": 1.0, "age": [pred_age]})
        pred_pi = m3.get_prediction(X_pred).summary_frame(alpha=0.05)
        pi_lo   = round(pred_pi["obs_ci_lower"].iloc[0], 1)
        pi_hi   = round(pred_pi["obs_ci_upper"].iloc[0], 1)
 
        if predicted_eff >= 88:
            eff_color = "#10b981"
            eff_label = "Excellent"
            eff_desc  = "Your age group shows consistently high sleep consolidation."
        elif predicted_eff >= 80:
            eff_color = "#06b6d4"
            eff_label = "Good"
            eff_desc  = "Mild age-related decline beginning. Sleep remains well consolidated."
        elif predicted_eff >= 70:
            eff_color = "#f59e0b"
            eff_label = "Fair"
            eff_desc  = "Noticeable fragmentation. More time spent awake during the night."
        else:
            eff_color = "#ef4444"
            eff_label = "Low"
            eff_desc  = "Significant age-related sleep disruption predicted."
 
        st.markdown(f"""
        <div class='nw-card' style='text-align:center; padding:32px; margin-top:16px;'>
            <div class='accent-line'
                 style='background:linear-gradient(90deg,{eff_color},{eff_color}55);'></div>
            <div style='font-family:DM Mono,monospace; font-size:11px;
                        letter-spacing:0.15em; text-transform:uppercase;
                        color:{eff_color}; margin-bottom:12px;'>
                Predicted Sleep Efficiency
            </div>
            <div style='font-family:Syne,sans-serif; font-size:56px; font-weight:800;
                        color:{eff_color}; line-height:1; margin-bottom:8px;'>
                {predicted_eff}%
            </div>
            <div style='font-family:DM Mono,monospace; font-size:12px;
                        color:#475569; margin-bottom:16px;'>
                95% PI: [{pi_lo}%, {pi_hi}%]
            </div>
            <div style='display:inline-block; padding:4px 14px; border-radius:20px;
                        background:rgba(99,102,241,0.12);
                        border:1px solid rgba(99,102,241,0.25);
                        font-family:DM Mono,monospace; font-size:11px;
                        color:{eff_color}; margin-bottom:16px;'>
                {eff_label}
            </div>
            <div style='font-size:12px; color:#64748b; line-height:1.6;'>
                {eff_desc}
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    with col_out:
        # Gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=predicted_eff,
            number=dict(
                suffix="%",
                font=dict(family="Syne", size=36, color="#e2e8f0")
            ),
            gauge=dict(
                axis=dict(
                    range=[50, 100],
                    tickfont=dict(family="DM Mono", size=10, color="#64748b"),
                    tickwidth=1,
                    tickcolor="#334155"
                ),
                bar=dict(color=eff_color, thickness=0.25),
                bgcolor="rgba(13,18,33,0.6)",
                borderwidth=0,
                steps=[
                    dict(range=[50, 70],  color="rgba(239,68,68,0.12)"),
                    dict(range=[70, 80],  color="rgba(245,158,11,0.12)"),
                    dict(range=[80, 88],  color="rgba(6,182,212,0.12)"),
                    dict(range=[88, 100], color="rgba(16,185,129,0.12)"),
                ],
                threshold=dict(
                    line=dict(color="white", width=2),
                    thickness=0.75,
                    value=predicted_eff
                )
            ),
            domain=dict(x=[0,1], y=[0,1])
        ))
 
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Mono", color="#94a3b8"),
            margin=dict(l=20, r=20, t=40, b=20),
            height=300,
        )
 
        st.plotly_chart(fig_gauge, use_container_width=True,
                        config={"displayModeBar": False})
 
        # Context vs dataset
        young_eff = round(97.4077 - (0.2902 * 25), 1)
        old_eff   = round(97.4077 - (0.2902 * 75), 1)
        st.markdown(f"""
        <div style='display:flex; gap:12px; margin-top:8px;'>
            <div style='flex:1; background:rgba(13,18,33,0.8);
                        border:1px solid rgba(99,102,241,0.15);
                        border-radius:10px; padding:14px; text-align:center;'>
                <div style='font-family:DM Mono,monospace; font-size:10px;
                            color:#64748b; text-transform:uppercase;
                            letter-spacing:0.1em; margin-bottom:6px;'>Age 25</div>
                <div style='font-family:Syne,sans-serif; font-size:22px;
                            font-weight:800; color:#10b981;'>{young_eff}%</div>
            </div>
            <div style='flex:1; background:rgba(13,18,33,0.8);
                        border:1px solid rgba(99,102,241,0.15);
                        border-radius:10px; padding:14px; text-align:center;'>
                <div style='font-family:DM Mono,monospace; font-size:10px;
                            color:#64748b; text-transform:uppercase;
                            letter-spacing:0.1em; margin-bottom:6px;'>Age 75</div>
                <div style='font-family:Syne,sans-serif; font-size:22px;
                            font-weight:800; color:#ef4444;'>{old_eff}%</div>
            </div>
            <div style='flex:1; background:rgba(13,18,33,0.8);
                        border:1px solid rgba(99,102,241,0.15);
                        border-radius:10px; padding:14px; text-align:center;'>
                <div style='font-family:DM Mono,monospace; font-size:10px;
                            color:#64748b; text-transform:uppercase;
                            letter-spacing:0.1em; margin-bottom:6px;'>Drop</div>
                <div style='font-family:Syne,sans-serif; font-size:22px;
                            font-weight:800; color:#f59e0b;'>
                    {round(young_eff - old_eff, 1)}pp
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown("<hr class='nw-divider'>", unsafe_allow_html=True)
 
    # ── SECTION 5, FINAL CONCLUSION ─────────────────────────────────────────
    st.markdown("""
    <div class='section-header'>Conclusion</div>
    <div class='section-sub'>What This Project Found, And What It Means</div>
    """, unsafe_allow_html=True)
 
    st.markdown("""
    <div class='nw-card'>
        <div style='font-family:DM Mono,monospace; font-size:10px; letter-spacing:0.15em;
                    text-transform:uppercase; color:#6366f1; margin-bottom:20px;'>
            ⬡ NeuroWave, Final Findings
        </div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:20px;'>
            <div>
                <div style='font-family:Syne,sans-serif; font-size:14px; font-weight:700;
                            color:#e2e8f0; margin-bottom:8px;'>What we found</div>
                <div style='font-size:13px; color:#64748b; line-height:1.9;'>
                    ● Sleep is not unconsciousness, it is a structured journey
                    through five measurably distinct brain states<br>
                    ● REM sleep is electrically near-identical to waking state,
                    separated only by suppressed alpha and gamma power<br>
                    ● No EEG band power distribution across any sleep stage is normal,
                    the brain is a nonlinear system<br>
                    ● Deep sleep probability collapses from 88% to 36% between
                    young and older subjects<br>
                    ● Age explains 47% of sleep efficiency variance, the strongest
                    predictive relationship in the dataset
                </div>
            </div>
            <div>
                <div style='font-family:Syne,sans-serif; font-size:14px; font-weight:700;
                            color:#e2e8f0; margin-bottom:8px;'>What it means</div>
                <div style='font-size:13px; color:#64748b; line-height:1.9;'>
                    ● Consciousness is not a binary switch, it is a probabilistic
                    spectrum the brain traverses every single night<br>
                    ● The boundary between waking and dreaming is thinner than
                    intuition suggests, one suppressed frequency band apart<br>
                    ● Ageing does not just change how we sleep, it statistically
                    rewrites the brain's nightly relationship with awareness<br>
                    ● The transition matrix confirms consciousness reassembles
                    gradually, it cannot be rushed or skipped<br>
                    ● Statistical analysis of sleep is not just data science,
                    it is empirical philosophy of mind
                </div>
            </div>
        </div>
        <div style='margin-top:24px; padding-top:20px;
                    border-top:1px solid rgba(99,102,241,0.15);
                    font-style:italic; font-size:14px; color:#6366f1;
                    line-height:1.8; text-align:center;'>
            "We set out to statistically characterize sleep stages.
            What we found is that the brain state we call unconscious REM sleep
            is electrically indistinguishable from waking consciousness,
            raising the question of what consciousness actually is."
        </div>
    </div>
    """, unsafe_allow_html=True)