import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import sqlite3
import pickle
import warnings
warnings.filterwarnings('ignore')
 
st.set_page_config(
    page_title="HealthLens India",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; background-color:#040d1a; color:#e8edf5; }
.stApp { background-color:#040d1a; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#071428 0%,#040d1a 100%); border-right:1px solid rgba(0,200,160,0.12); }
[data-testid="stSidebar"] .stSelectbox label,[data-testid="stSidebar"] p,[data-testid="stSidebar"] span { color:#8fa8c8 !important; }
.hero-wrap { background:linear-gradient(135deg,#071e3d 0%,#0a2a4a 50%,#071428 100%); border:1px solid rgba(0,200,160,0.18); border-radius:20px; padding:40px 48px; margin-bottom:32px; position:relative; overflow:hidden; }
.hero-logo { font-family:'Syne',sans-serif; font-size:13px; font-weight:700; letter-spacing:0.18em; text-transform:uppercase; color:#00c8a0; margin-bottom:12px; }
.hero-title { font-family:'Syne',sans-serif; font-size:42px; font-weight:800; line-height:1.1; color:#ffffff; margin-bottom:14px; letter-spacing:-0.02em; }
.hero-title span { color:#00c8a0; }
.hero-sub { font-size:15px; color:#7a9bbf; max-width:560px; line-height:1.7; font-weight:300; }
.hero-pills { display:flex; gap:10px; margin-top:24px; flex-wrap:wrap; }
.pill { background:rgba(0,200,160,0.1); border:1px solid rgba(0,200,160,0.25); color:#00c8a0; padding:5px 14px; border-radius:20px; font-size:12px; font-weight:500; }
.kpi-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:32px; }
.kpi-card { background:linear-gradient(135deg,#071e3d 0%,#0a1f3a 100%); border:1px solid rgba(255,255,255,0.07); border-radius:16px; padding:24px 22px; position:relative; overflow:hidden; }
.kpi-card:hover { border-color:rgba(0,200,160,0.3); }
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,#00c8a0,#0078ff); opacity:0.6; }
.kpi-label { font-size:11px; font-weight:500; letter-spacing:0.1em; text-transform:uppercase; color:#4a7090; margin-bottom:10px; }
.kpi-value { font-family:'Syne',sans-serif; font-size:36px; font-weight:800; color:#ffffff; line-height:1; margin-bottom:6px; }
.kpi-sub { font-size:12px; color:#4a7090; }
.kpi-accent { color:#00c8a0; }
.section-head { font-family:'Syne',sans-serif; font-size:20px; font-weight:700; color:#e8edf5; margin-bottom:16px; display:flex; align-items:center; gap:10px; }
.section-head::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.06); margin-left:8px; }
.content-card { background:#071428; border:1px solid rgba(255,255,255,0.07); border-radius:16px; padding:24px; margin-bottom:20px; }
.stTabs [data-baseweb="tab-list"] { background:transparent; border-bottom:1px solid rgba(255,255,255,0.07); gap:0; }
.stTabs [data-baseweb="tab"] { font-family:'DM Sans',sans-serif; font-size:13px; font-weight:500; color:#4a7090; padding:10px 22px; border-radius:0; border-bottom:2px solid transparent; }
.stTabs [aria-selected="true"] { color:#00c8a0 !important; border-bottom:2px solid #00c8a0 !important; background:transparent !important; }
.stButton > button { background:linear-gradient(135deg,#00c8a0,#0078ff); color:white; border:none; border-radius:10px; font-family:'DM Sans',sans-serif; font-weight:500; font-size:14px; padding:12px 28px; width:100%; }
.stTextInput input { background:#071e3d !important; border:1px solid rgba(0,200,160,0.25) !important; color:#e8edf5 !important; border-radius:10px !important; font-size:14px !important; }
.stTextArea textarea { background:#071e3d !important; border:1px solid rgba(0,200,160,0.2) !important; color:#e8edf5 !important; font-family:'Courier New',monospace !important; font-size:13px !important; border-radius:10px !important; }
.insight-box { background:rgba(0,200,160,0.06); border-left:3px solid #00c8a0; border-radius:0 10px 10px 0; padding:14px 18px; margin:10px 0; font-size:13px; color:#8fa8c8; line-height:1.6; }
.insight-box strong { color:#00c8a0; }
.warn-box { background:rgba(255,170,0,0.06); border-left:3px solid #ffaa00; border-radius:0 10px 10px 0; padding:14px 18px; margin:10px 0; font-size:13px; color:#c8a870; line-height:1.6; }
.warn-box strong { color:#ffaa00; }
.danger-box { background:rgba(255,60,60,0.06); border-left:3px solid #ff5c5c; border-radius:0 10px 10px 0; padding:14px 18px; margin:10px 0; font-size:13px; color:#c87070; line-height:1.6; }
.danger-box strong { color:#ff5c5c; }
.risk-high { background:linear-gradient(135deg,#3d0a0a,#5c1010); border:1px solid rgba(255,60,60,0.3); border-radius:16px; padding:28px 32px; text-align:center; }
.risk-low { background:linear-gradient(135deg,#0a2d1e,#0d3d28); border:1px solid rgba(0,200,160,0.3); border-radius:16px; padding:28px 32px; text-align:center; }
.risk-title { font-family:'Syne',sans-serif; font-size:28px; font-weight:800; margin-bottom:8px; }
.risk-conf { font-size:14px; color:#8fa8c8; margin-bottom:12px; }
.risk-note { font-size:13px; color:#6a8aaa; max-width:480px; margin:0 auto; line-height:1.6; }
.district-card { background:linear-gradient(135deg,#071e3d,#0a2a4a); border:1px solid rgba(0,200,160,0.2); border-radius:16px; padding:24px 28px; margin-top:16px; }
.indicator-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:16px; }
.ind-box { border-radius:10px; padding:14px; text-align:center; }
.ind-val { font-family:'Syne',sans-serif; font-size:22px; font-weight:800; margin-bottom:4px; }
.ind-lbl { font-size:10px; color:#4a7090; text-transform:uppercase; letter-spacing:0.06em; line-height:1.4; }
.tech-grid { display:flex; flex-wrap:wrap; gap:10px; margin-top:12px; }
.tech-pill { background:rgba(0,120,255,0.1); border:1px solid rgba(0,120,255,0.25); color:#5599ff; padding:6px 16px; border-radius:20px; font-size:13px; }
#MainMenu,footer,header { visibility:hidden; }
.block-container { padding-top:2rem; padding-bottom:2rem; }
</style>
""", unsafe_allow_html=True)
 
 
# ─── DATA ────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv('nfhs5_clean.csv')
 
@st.cache_resource
def load_model():
    with open('rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('feature_cols.pkl', 'rb') as f:
        features = pickle.load(f)
    return model, features
 
df          = load_data()
model, feature_cols = load_model()
 
FEATURE_LABELS = {
    feature_cols[0]: 'Anaemia in Women (%)',
    feature_cols[1]: 'Child Vaccination (%)',
    feature_cols[2]: 'Institutional Births (%)',
    feature_cols[3]: 'Child Stunting (%)'
}
NAT_AVG = {feat: df[feat].mean() for feat in feature_cols}
 
 
# ─── POLICY ENGINE ───────────────────────────────────────────────────────────
def get_policy_recommendations(row):
    recs = []
    a_col, v_col, b_col, s_col = feature_cols[0], feature_cols[1], feature_cols[2], feature_cols[3]
 
    anaemia_val = row[a_col]
    vacc_val    = row[v_col]
    birth_val   = row[b_col]
    stunt_val   = row[s_col]
 
    if anaemia_val > NAT_AVG[a_col] * 1.1:
        gap = anaemia_val - NAT_AVG[a_col]
        recs.append({
            'icon': '🩸',
            'issue': f"Anaemia in women at {anaemia_val:.1f}% — {gap:.1f}pp above national avg ({NAT_AVG[a_col]:.1f}%)",
            'action': "Deploy Iron-Folic Acid supplementation drives via ASHA workers. "
                      "Integrate anaemia screening into routine ANM visits under NHM.",
            'priority': 'high' if gap > 10 else 'medium'
        })
 
    vacc_gap = NAT_AVG[v_col] - vacc_val
    if vacc_gap > 5:
        recs.append({
            'icon': '💉',
            'issue': f"Child vaccination at {vacc_val:.1f}% — {vacc_gap:.1f}pp below national avg ({NAT_AVG[v_col]:.1f}%)",
            'action': "Deploy mobile vaccination units for remote areas. "
                      "Partner with Panchayati Raj institutions for community mobilisation. "
                      "Track unvaccinated children via HMIS portal.",
            'priority': 'high' if vacc_gap > 15 else 'medium'
        })
 
    birth_gap = NAT_AVG[b_col] - birth_val
    if birth_gap > 5:
        recs.append({
            'icon': '🏥',
            'issue': f"Institutional births at {birth_val:.1f}% — {birth_gap:.1f}pp below national avg ({NAT_AVG[b_col]:.1f}%)",
            'action': "Strengthen JSY (Janani Suraksha Yojana) incentives. "
                      "Improve road access to PHCs in remote areas. "
                      "Deploy skilled birth attendants to underserved blocks.",
            'priority': 'high' if birth_gap > 15 else 'medium'
        })
 
    if stunt_val > NAT_AVG[s_col] * 1.1:
        gap = stunt_val - NAT_AVG[s_col]
        recs.append({
            'icon': '🥗',
            'issue': f"Child stunting at {stunt_val:.1f}% — {gap:.1f}pp above national avg ({NAT_AVG[s_col]:.1f}%)",
            'action': "Scale up Poshan Abhiyaan nutrition programmes. "
                      "Increase ICDS Anganwadi coverage and improve supplementary nutrition quality.",
            'priority': 'high' if gap > 10 else 'medium'
        })
 
    if not recs:
        recs.append({
            'icon': '✅',
            'issue': "All indicators near or below national averages.",
            'action': "Focus on sustaining current performance. "
                      "Share district best practices with NHM state mission.",
            'priority': 'low'
        })
    return recs
 
 
# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:8px 0 24px;border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:24px;'>
        <div style='font-family:Syne,sans-serif;font-size:18px;font-weight:800;color:#fff;'>HealthLens</div>
        <div style='font-size:11px;color:#4a7090;letter-spacing:0.1em;text-transform:uppercase;margin-top:2px;'>India · NFHS-5</div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("<div style='font-size:11px;color:#4a7090;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;'>Filter by State</div>", unsafe_allow_html=True)
    state_list = ['All India'] + sorted(df['state'].unique().tolist())
    state      = st.selectbox("", state_list, label_visibility="collapsed")
    df_view    = df[df['state'] == state].copy() if state != 'All India' else df.copy()
 
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background:rgba(0,200,160,0.06);border:1px solid rgba(0,200,160,0.15);
                border-radius:12px;padding:16px;'>
        <div style='font-size:11px;color:#4a7090;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;'>Viewing</div>
        <div style='font-family:Syne,sans-serif;font-size:22px;font-weight:800;color:#fff;'>{len(df_view):,}</div>
        <div style='font-size:12px;color:#4a7090;'>districts in {state}</div>
        <div style='margin-top:12px;font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#ff5c5c;'>{df_view['high_risk'].sum()}</div>
        <div style='font-size:12px;color:#4a7090;'>high risk districts</div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("""<br><div style='font-size:11px;color:#2a4060;line-height:1.8;'>
        Data: NFHS-5 (2019–21)<br>Government of India<br>706 districts · 109 indicators
    </div>""", unsafe_allow_html=True)
 
 
# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-logo">🩺 HealthLens India</div>
    <div class="hero-title">District Health<br><span>Intelligence</span> Platform</div>
    <div class="hero-sub">
        End-to-end analytics identifying high-risk districts across India using NFHS-5
        government data — powered by machine learning, SQL analytics,
        and data-driven policy recommendations.
    </div>
    <div class="hero-pills">
        <span class="pill">706 Districts</span>
        <span class="pill">36 States & UTs</span>
        <span class="pill">95.77% ML Accuracy</span>
        <span class="pill">NFHS-5 · 2019–21</span>
        <span class="pill">Policy Recommendations</span>
        <span class="pill">District Search</span>
    </div>
</div>
""", unsafe_allow_html=True)
 
 
# ─── TABS ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  📊  Dashboard  ",
    "  🔍  District Search  ",
    "  📋  Policy Recommendations  ",
    "  🤖  Risk Predictor  ",
    "  🗄️  SQL Explorer  ",
])
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Districts Analysed</div>
            <div class="kpi-value">{len(df_view):,}</div>
            <div class="kpi-sub">across {df_view['state'].nunique()} states</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">High Risk Districts</div>
            <div class="kpi-value" style="color:#ff5c5c">{df_view['high_risk'].sum()}</div>
            <div class="kpi-sub">{df_view['high_risk'].mean()*100:.0f}% of total</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Avg Risk Score</div>
            <div class="kpi-value">{df_view['risk_score'].mean():.1f}</div>
            <div class="kpi-sub">national mean: 32.5</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">ML Accuracy</div>
            <div class="kpi-value kpi-accent">95.8%</div>
            <div class="kpi-sub">Random Forest · 5-fold CV</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    col_left, col_right = st.columns([1.4, 0.6])
    with col_left:
        st.markdown('<div class="section-head">🔴 Highest Risk Districts</div>', unsafe_allow_html=True)
        top15 = df_view.nlargest(15, 'risk_score')[['district','state','risk_score']].reset_index(drop=True)
        fig, ax = plt.subplots(figsize=(10, 7))
        fig.patch.set_facecolor('#071428'); ax.set_facecolor('#071428')
        cmap = plt.cm.get_cmap('RdYlGn_r')
        norm = mcolors.Normalize(vmin=top15['risk_score'].min(), vmax=top15['risk_score'].max())
        colors = [cmap(norm(v)) for v in top15['risk_score']]
        bars = ax.barh(top15['district'] + '  ·  ' + top15['state'],
                       top15['risk_score'], color=colors, height=0.65, edgecolor='none')
        ax.axvline(df['risk_score'].mean(), color='#00c8a0', linestyle='--',
                   linewidth=1.5, alpha=0.7, label=f'National avg: {df["risk_score"].mean():.1f}')
        for bar, val in zip(bars, top15['risk_score']):
            ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
                    f'{val:.1f}', va='center', fontsize=9, color='#8fa8c8')
        ax.invert_yaxis()
        ax.set_xlabel('Composite Health Risk Score', color='#4a7090', fontsize=11, labelpad=10)
        ax.tick_params(colors='#8fa8c8', labelsize=10)
        ax.spines[:].set_visible(False)
        ax.set_xlim(0, top15['risk_score'].max()*1.12)
        ax.legend(fontsize=10, facecolor='#071428', labelcolor='#8fa8c8', edgecolor='none')
        plt.tight_layout(); st.pyplot(fig); plt.close()
 
    with col_right:
        st.markdown('<div class="section-head">📈 Distribution</div>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(5, 7))
        fig2.patch.set_facecolor('#071428'); ax2.set_facecolor('#071428')
        n, bins, patches = ax2.hist(df_view['risk_score'], bins=30, edgecolor='none')
        bin_centers = 0.5*(bins[:-1]+bins[1:])
        norm2 = mcolors.Normalize(vmin=bin_centers.min(), vmax=bin_centers.max())
        cmap2 = plt.cm.get_cmap('cool')
        for patch, center in zip(patches, bin_centers):
            patch.set_facecolor(cmap2(norm2(center))); patch.set_alpha(0.85)
        ax2.axvline(df_view['risk_score'].median(), color='#00c8a0', linestyle='--',
                    linewidth=1.8, label=f"Median {df_view['risk_score'].median():.1f}")
        ax2.set_xlabel('Risk Score', color='#4a7090', fontsize=10)
        ax2.set_ylabel('Districts', color='#4a7090', fontsize=10)
        ax2.tick_params(colors='#6a8aaa', labelsize=9)
        ax2.spines[:].set_visible(False)
        ax2.legend(fontsize=9, facecolor='#071428', labelcolor='#8fa8c8', edgecolor='none')
        plt.tight_layout(); st.pyplot(fig2); plt.close()
 
    worst = df_view.nlargest(1,'risk_score').iloc[0]
    best  = df_view.nsmallest(1,'risk_score').iloc[0]
    st.markdown(f"""
    <div class="insight-box">
        <strong>Key Finding:</strong> {worst['district']}, {worst['state']} scores
        <strong>{worst['risk_score']:.1f}</strong> — driven by high anaemia and low vaccination.
        {best['district']}, {best['state']} leads at <strong>{best['risk_score']:.1f}</strong>,
        reflecting decades of primary healthcare investment.
    </div>""", unsafe_allow_html=True)
 
    st.markdown('<br><div class="section-head">🔗 Indicator Correlations</div>', unsafe_allow_html=True)
    key_cols_c = feature_cols + ['risk_score']
    disp_names = list(FEATURE_LABELS.values()) + ['Risk Score']
    corr_df = df_view[key_cols_c].copy(); corr_df.columns = disp_names
    fig3, ax3 = plt.subplots(figsize=(9, 4))
    fig3.patch.set_facecolor('#071428'); ax3.set_facecolor('#071428')
    mask = np.triu(np.ones(len(disp_names), dtype=bool))
    sns.heatmap(corr_df.corr(), annot=True, fmt='.2f', cmap='RdYlGn',
                mask=mask, ax=ax3, linewidths=1, linecolor='#040d1a',
                annot_kws={'size':11,'color':'white'}, cbar_kws={'shrink':0.6})
    ax3.tick_params(colors='#8fa8c8', labelsize=10)
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=25, ha='right')
    ax3.set_yticklabels(ax3.get_yticklabels(), rotation=0)
    ax3.collections[0].colorbar.ax.tick_params(colors='#6a8aaa', labelsize=9)
    plt.tight_layout(); st.pyplot(fig3); plt.close()
 
    st.markdown('<br><div class="section-head">🗺️ State-level Summary</div>', unsafe_allow_html=True)
    ss = df_view.groupby('state').agg(
        Districts=('district','count'), Avg_Risk=('risk_score','mean'),
        High_Risk=('high_risk','sum'), Max_Risk=('risk_score','max')
    ).round(2).reset_index().sort_values('Avg_Risk', ascending=False)
    ss.columns = ['State','Districts','Avg Risk Score','High Risk Count','Worst Score']
    st.dataframe(ss, use_container_width=True, hide_index=True)
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DISTRICT SEARCH
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div style='margin-bottom:24px;'>
        <div style='font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:#fff;margin-bottom:8px;'>District Health Profile</div>
        <div style='font-size:14px;color:#5a7a9a;line-height:1.6;max-width:580px;'>
            Search any of India's 706 districts to see its complete health profile —
            all 4 indicators, national rank, risk score, and tailored policy recommendations.
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    search = st.text_input("", placeholder="Type a district name — e.g. Pune, Bastar, Kozhikode, Araria...",
                           label_visibility="collapsed")
 
    def render_district(row):
        nat_rank = int(df['risk_score'].rank(ascending=False)[row.name])
        state_df = df[df['state'] == row['state']].copy()
        state_df['sr'] = state_df['risk_score'].rank(ascending=False).astype(int)
        state_rank = int(state_df.loc[state_df['district'] == row['district'], 'sr'].values[0])
        risk_color = '#ff5c5c' if row['high_risk'] == 1 else '#00c8a0'
        risk_label = 'HIGH RISK' if row['high_risk'] == 1 else 'LOW RISK'
 
        ind_html = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0;">'
        for feat, lbl, bg, color, higher_bad in [
            (feature_cols[0],'Anaemia\n(Women)','rgba(255,92,92,0.12)','#ff5c5c',True),
            (feature_cols[1],'Child\nVaccination','rgba(0,200,160,0.12)','#00c8a0',False),
            (feature_cols[2],'Institutional\nBirths','rgba(85,153,255,0.12)','#5599ff',False),
            (feature_cols[3],'Child\nStunting','rgba(255,170,0,0.12)','#ffaa00',True),
        ]:
            val  = row[feat]; avg = NAT_AVG[feat]; diff = val - avg
            arrow = '▲' if diff > 0 else '▼'
            dc = '#ff5c5c' if (diff > 0) == higher_bad else '#00c8a0'
            ind_html += f"""<div style="background:{bg};border-radius:10px;padding:14px;text-align:center;">
                <div style="font-family:Syne,sans-serif;font-size:22px;font-weight:800;color:{color};">{val:.1f}%</div>
                <div style="font-size:10px;color:#4a7090;text-transform:uppercase;letter-spacing:0.06em;margin-top:4px;">{lbl}</div>
                <div style="font-size:11px;color:{dc};margin-top:6px;">{arrow} {abs(diff):.1f}pp vs avg</div>
            </div>"""
        ind_html += '</div>'
 
        score_pct = (row['risk_score'] - df['risk_score'].min()) / \
                    (df['risk_score'].max() - df['risk_score'].min()) * 100
 
        st.markdown(f"""
        <div class="district-card">
            <div style='font-family:Syne,sans-serif;font-size:24px;font-weight:800;color:#fff;'>{row['district']}</div>
            <div style='font-size:13px;color:#4a7090;margin:4px 0 16px;'>
                {row['state']} &nbsp;·&nbsp;
                <span style='color:{risk_color};font-weight:600;'>{risk_label}</span> &nbsp;·&nbsp;
                National Rank #{nat_rank} of 706 &nbsp;·&nbsp;
                #{state_rank} in {row['state']}
            </div>
            {ind_html}
            <div>
                <div style='display:flex;justify-content:space-between;font-size:12px;color:#4a7090;margin-bottom:6px;'>
                    <span>Composite Risk Score</span>
                    <span style='color:{risk_color};font-weight:600;font-size:14px;'>{row['risk_score']:.1f}</span>
                </div>
                <div style='background:rgba(255,255,255,0.06);border-radius:6px;height:8px;'>
                    <div style='background:linear-gradient(90deg,#00c8a0,{risk_color});
                                width:{score_pct:.0f}%;height:8px;border-radius:6px;'></div>
                </div>
                <div style='display:flex;justify-content:space-between;font-size:10px;color:#2a4060;margin-top:4px;'>
                    <span>Lowest (15.9)</span><span>National Avg (32.5)</span><span>Highest (52.6)</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-head">📊 vs National Average</div>', unsafe_allow_html=True)
        fig_c, ax_c = plt.subplots(figsize=(9, 3.5))
        fig_c.patch.set_facecolor('#071428'); ax_c.set_facecolor('#071428')
        labels = list(FEATURE_LABELS.values())
        d_vals = [row[f] for f in feature_cols]
        n_vals = [NAT_AVG[f] for f in feature_cols]
        x = np.arange(len(labels)); w = 0.32
        ax_c.bar(x-w/2, d_vals, w, label=row['district'], color='#0078ff', alpha=0.9, edgecolor='none')
        ax_c.bar(x+w/2, n_vals, w, label='National Avg',  color='#00c8a0', alpha=0.6, edgecolor='none')
        ax_c.set_xticks(x); ax_c.set_xticklabels(labels, color='#8fa8c8', fontsize=10)
        ax_c.tick_params(colors='#6a8aaa'); ax_c.spines[:].set_visible(False)
        ax_c.legend(fontsize=10, facecolor='#071428', labelcolor='#8fa8c8', edgecolor='none')
        plt.tight_layout(); st.pyplot(fig_c); plt.close()
 
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-head">📋 Policy Recommendations</div>', unsafe_allow_html=True)
        for rec in get_policy_recommendations(row):
            box = 'danger-box' if rec['priority']=='high' else 'warn-box' if rec['priority']=='medium' else 'insight-box'
            st.markdown(f"""<div class="{box}">
                {rec['icon']} <strong>Issue:</strong> {rec['issue']}<br>
                → <strong>Action:</strong> {rec['action']}
            </div>""", unsafe_allow_html=True)
 
    if search and len(search) >= 2:
        matches = df[df['district'].str.contains(search, case=False, na=False)]
        if len(matches) == 0:
            st.markdown(f'<div class="warn-box"><strong>No district found</strong> matching "{search}".</div>', unsafe_allow_html=True)
        elif len(matches) > 1:
            st.markdown(f'<div class="insight-box"><strong>{len(matches)} matches found.</strong> Select one below.</div>', unsafe_allow_html=True)
            opts = (matches['district'] + ', ' + matches['state']).tolist()
            sel  = st.selectbox("Select:", opts, label_visibility="collapsed")
            sel_name = sel.split(', ')[0]
            row = matches[matches['district'] == sel_name].iloc[0]
            render_district(row)
        else:
            render_district(matches.iloc[0])
    elif not search:
        c_l, c_r = st.columns(2)
        with c_l:
            st.markdown('<div class="section-head">🔴 5 Highest Risk</div>', unsafe_allow_html=True)
            st.dataframe(df.nlargest(5,'risk_score')[['district','state','risk_score']], use_container_width=True, hide_index=True)
        with c_r:
            st.markdown('<div class="section-head">🟢 5 Lowest Risk</div>', unsafe_allow_html=True)
            st.dataframe(df.nsmallest(5,'risk_score')[['district','state','risk_score']], use_container_width=True, hide_index=True)
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — POLICY RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div style='margin-bottom:24px;'>
        <div style='font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:#fff;margin-bottom:8px;'>
            Data-driven Policy Recommendations
        </div>
        <div style='font-size:14px;color:#5a7a9a;line-height:1.6;max-width:640px;'>
            For each high-risk district, HealthLens analyses which indicators are driving
            the score and generates targeted intervention recommendations aligned with
            India's national health programmes — NHM, JSY, ABDM, and Poshan Abhiyaan.
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown(f"""
    <div class="insight-box" style='margin-bottom:24px;'>
        <strong>Methodology:</strong> Each district's 4 indicators are compared against national averages.
        Gaps exceeding 10% of the national mean trigger high-priority recommendations.
        Gaps of 5–10% trigger medium-priority. Recommendations reference specific
        Government of India schemes (JSY, POSHAN, NHM, HMIS).
    </div>
    """, unsafe_allow_html=True)
 
    top_risk = df_view[df_view['high_risk'] == 1].nlargest(20, 'risk_score')
 
    for _, row in top_risk.iterrows():
        recs = get_policy_recommendations(row)
        nat_rank = int(df['risk_score'].rank(ascending=False)[row.name])
        priority_icon = '🔴' if recs[0]['priority'] == 'high' else '🟡'
 
        with st.expander(
            f"{priority_icon}  {row['district']}, {row['state']}  ·  "
            f"Risk Score {row['risk_score']:.1f}  ·  National #{nat_rank}",
            expanded=False
        ):
            ind_h = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px;">'
            for feat, lbl, bg, color, hb in [
                (feature_cols[0],'Anaemia (Women)','rgba(255,92,92,0.1)','#ff5c5c',True),
                (feature_cols[1],'Child Vaccination','rgba(0,200,160,0.1)','#00c8a0',False),
                (feature_cols[2],'Inst. Births','rgba(85,153,255,0.1)','#5599ff',False),
                (feature_cols[3],'Child Stunting','rgba(255,170,0,0.1)','#ffaa00',True),
            ]:
                val = row[feat]; avg = NAT_AVG[feat]; diff = val - avg
                arrow = '▲' if diff > 0 else '▼'
                dc = '#ff5c5c' if (diff > 0) == hb else '#00c8a0'
                ind_h += f"""<div style="background:{bg};border-radius:10px;padding:12px;text-align:center;">
                    <div style="font-family:Syne,sans-serif;font-size:20px;font-weight:800;color:{color};">{val:.1f}%</div>
                    <div style="font-size:10px;color:#4a7090;text-transform:uppercase;margin-top:4px;">{lbl}</div>
                    <div style="font-size:11px;color:{dc};margin-top:5px;">{arrow} {abs(diff):.1f}pp vs avg</div>
                </div>"""
            ind_h += '</div>'
            st.markdown(ind_h, unsafe_allow_html=True)
 
            for rec in recs:
                box = 'danger-box' if rec['priority']=='high' else 'warn-box' if rec['priority']=='medium' else 'insight-box'
                st.markdown(f"""<div class="{box}">
                    {rec['icon']} <strong>Issue:</strong> {rec['issue']}<br>
                    → <strong>Recommended action:</strong> {rec['action']}
                </div>""", unsafe_allow_html=True)
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — RISK PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div style='margin-bottom:24px;'>
        <div style='font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:#fff;margin-bottom:8px;'>District Risk Predictor</div>
        <div style='font-size:14px;color:#5a7a9a;line-height:1.6;max-width:580px;'>
            Adjust health indicators to match any district's profile.
            The Random Forest model — 95.77% accuracy — instantly predicts
            risk classification and generates intervention recommendations.
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    c1, c2 = st.columns(2)
    user_inputs = {}
    slider_meta = {
        feature_cols[0]: ("Higher = higher risk", "#ff5c5c"),
        feature_cols[1]: ("Higher = lower risk",  "#00c8a0"),
        feature_cols[2]: ("Higher = lower risk",  "#5599ff"),
        feature_cols[3]: ("Higher = higher risk", "#ffaa00"),
    }
    for i, feat in enumerate(feature_cols):
        col = c1 if i % 2 == 0 else c2
        hint, color = slider_meta[feat]
        with col:
            st.markdown(f"""<div style='margin-bottom:4px;'>
                <span style='font-size:13px;font-weight:500;color:#c8ddf0;'>{FEATURE_LABELS[feat]}</span>
                <span style='font-size:11px;color:{color};margin-left:8px;'>· {hint}</span>
            </div>""", unsafe_allow_html=True)
            user_inputs[feat] = st.slider(
                FEATURE_LABELS[feat], label_visibility="collapsed",
                min_value=round(float(df[feat].min()),1),
                max_value=round(float(df[feat].max()),1),
                value=round(float(df[feat].mean()),1),
                step=0.1, key=f"pred_{feat}"
            )
 
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("  🔍  Predict Health Risk Classification  ", type="primary"):
        inp = pd.DataFrame([user_inputs])
        pred = model.predict(inp)[0]
        prob = model.predict_proba(inp)[0]
        st.markdown("<br>", unsafe_allow_html=True)
        if pred == 1:
            st.markdown(f"""<div class="risk-high">
                <div class="risk-title" style="color:#ff5c5c;">⚠️ HIGH RISK DISTRICT</div>
                <div class="risk-conf">Confidence: <strong style="color:#ff8080">{prob[1]*100:.1f}%</strong></div>
                <div class="risk-note">This profile indicates a high-risk district. See recommendations below.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="risk-low">
                <div class="risk-title" style="color:#00c8a0;">✅ LOW RISK DISTRICT</div>
                <div class="risk-conf">Confidence: <strong style="color:#00e8b8">{prob[0]*100:.1f}%</strong></div>
                <div class="risk-note">Relatively strong health indicators. Focus on sustaining performance.</div>
            </div>""", unsafe_allow_html=True)
 
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-head">Your Input vs National Average</div>', unsafe_allow_html=True)
        fig_c, ax_c = plt.subplots(figsize=(9, 3))
        fig_c.patch.set_facecolor('#071428'); ax_c.set_facecolor('#071428')
        x = np.arange(len(feature_cols)); w = 0.32
        ax_c.bar(x-w/2, [user_inputs[f] for f in feature_cols], w,
                 label='Your Input', color='#0078ff', alpha=0.9, edgecolor='none')
        ax_c.bar(x+w/2, [NAT_AVG[f] for f in feature_cols], w,
                 label='National Avg', color='#00c8a0', alpha=0.6, edgecolor='none')
        ax_c.set_xticks(x); ax_c.set_xticklabels(list(FEATURE_LABELS.values()), color='#8fa8c8', fontsize=10)
        ax_c.tick_params(colors='#6a8aaa'); ax_c.spines[:].set_visible(False)
        ax_c.legend(fontsize=10, facecolor='#071428', labelcolor='#8fa8c8', edgecolor='none')
        plt.tight_layout(); st.pyplot(fig_c); plt.close()
 
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-head">📋 Recommended Interventions</div>', unsafe_allow_html=True)
        for rec in get_policy_recommendations(pd.Series(user_inputs)):
            box = 'danger-box' if rec['priority']=='high' else 'warn-box' if rec['priority']=='medium' else 'insight-box'
            st.markdown(f"""<div class="{box}">
                {rec['icon']} <strong>{rec['issue']}</strong><br>→ {rec['action']}
            </div>""", unsafe_allow_html=True)
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — SQL EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("""
    <div style='margin-bottom:24px;'>
        <div style='font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:#fff;margin-bottom:8px;'>Live SQL Explorer</div>
        <div style='font-size:14px;color:#5a7a9a;line-height:1.6;max-width:580px;'>
            Query the NFHS-5 health database directly. Choose a sample or write your own SQL.
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    examples = {
        "🔴  Top 10 riskiest districts":
            "SELECT district, state,\n       ROUND(risk_score,2) AS risk_score\nFROM health_indicators\nORDER BY risk_score DESC\nLIMIT 10",
        "🗺️  State averages ranked":
            "SELECT state,\n       ROUND(AVG(risk_score),2) AS avg_risk,\n       COUNT(*) AS total_districts,\n       SUM(high_risk) AS high_risk_count\nFROM health_indicators\nGROUP BY state\nORDER BY avg_risk DESC",
        "📊  Districts worse than state average":
            "SELECT h.district, h.state,\n       ROUND(h.risk_score,2) AS risk_score,\n       ROUND(h.risk_score - s.avg_risk,2) AS above_state_avg\nFROM health_indicators h\nJOIN (\n    SELECT state, AVG(risk_score) AS avg_risk\n    FROM health_indicators GROUP BY state\n) s ON h.state = s.state\nWHERE h.risk_score > s.avg_risk\nORDER BY above_state_avg DESC LIMIT 15",
        "🏆  #1 riskiest per state (window fn)":
            "SELECT * FROM (\n    SELECT district, state,\n           ROUND(risk_score,2) AS risk_score,\n           RANK() OVER (PARTITION BY state ORDER BY risk_score DESC) AS rank_in_state\n    FROM health_indicators\n) WHERE rank_in_state = 1\nORDER BY risk_score DESC",
    }
 
    selected = st.selectbox("Sample queries:", list(examples.keys()))
    query    = st.text_area("SQL:", value=examples[selected], height=160)
 
    if st.button("  ▶  Run Query  ", type="primary"):
        try:
            conn = sqlite3.connect(':memory:')
            df.to_sql('health_indicators', conn, index=False, if_exists='replace')
            result = pd.read_sql_query(query, conn)
            conn.close()
            st.markdown(f"""<div style='font-size:12px;color:#00c8a0;margin:12px 0 8px;font-weight:500;'>✓ {len(result)} rows returned</div>""", unsafe_allow_html=True)
            st.dataframe(result, use_container_width=True, hide_index=True)
        except Exception as e:
            st.markdown(f"""<div style='background:rgba(255,60,60,0.08);border:1px solid rgba(255,60,60,0.2);border-radius:10px;padding:14px;color:#ff8080;font-size:13px;'>SQL Error: {str(e)}</div>""", unsafe_allow_html=True)