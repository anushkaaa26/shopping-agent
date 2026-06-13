import os
import tempfile
import streamlit as st
from shopping_agent import agent

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI Shopping Assistant", page_icon="🛒", layout="wide")

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Serif+Display:ital@0;1&display=swap');

/* ══════════════════════════════════════
   TOKENS
══════════════════════════════════════ */
:root {
  --bg:        #191b15;
  --surface:   #22261c;
  --surface2:  #2b3022;
  --surface3:  #343929;

  --border:    #3d4232;
  --border-hi: #5a6248;

  /* woodland accent scale */
  --moss:      #656D4A;
  --reseda:    #A4AC86;
  --khaki:     #B6AD90;
  --ash:       #C2C5AA;
  --lion:      #936639;
  --chamois:   #A68A64;
  --coffee:    #7F4F24;
  --seal:      #5B2C07;

  --text:      #EAE8E0;
  --text-dim:  #B6AD90;
  --muted:     #7a8260;

  /* bubble colours */
  --user-bg:     #1f2e28;
  --user-border: #2d4a38;
  --user-glow:   rgba(100,172,100,0.08);
  --bot-bg:      #231f18;
  --bot-border:  #3a3020;
  --bot-glow:    rgba(163,136,100,0.08);

  --radius: 16px;
  --font: 'DM Sans', sans-serif;
}

/* ══════════════════════════════════════
   GLOBAL
══════════════════════════════════════ */
html, body, [class*="css"] { font-family: var(--font) !important; }
.stApp { background: var(--bg) !important; color: var(--text) !important; }
.block-container {
  padding: 1.4rem 2.4rem 7rem !important;
  max-width: 1140px !important;
  margin: 0 auto !important;
}
h1:first-of-type { display: none !important; }
.stCaption        { display: none !important; }
footer            { display: none !important; }
#MainMenu         { display: none !important; }

/* ══════════════════════════════════════
   HEADER
══════════════════════════════════════ */
.shop-header {
  display: flex; align-items: center; gap: 16px;
  padding: 1.5rem 0 1.3rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1.6rem;
}
.header-icon-wrap {
  position: relative;
  width: 54px; height: 54px; flex-shrink: 0;
}
.header-icon-bg {
  width: 54px; height: 54px; border-radius: 16px;
  background: linear-gradient(145deg, #3d4a2a, #2b3020);
  border: 1.5px solid var(--moss);
  display: flex; align-items: center; justify-content: center;
  font-size: 26px;
  box-shadow: 0 4px 20px rgba(101,109,74,0.30), 0 0 0 4px rgba(101,109,74,0.08);
  animation: icon-breathe 3.5s ease-in-out infinite;
}
@keyframes icon-breathe {
  0%,100% { box-shadow: 0 4px 20px rgba(101,109,74,0.30), 0 0 0 4px rgba(101,109,74,0.08); }
  50%      { box-shadow: 0 4px 28px rgba(101,109,74,0.50), 0 0 0 8px rgba(101,109,74,0.12); }
}
.shop-header h1 {
  font-family: 'DM Serif Display', serif !important;
  font-size: 1.75rem !important;
  margin: 0 !important; padding: 0 !important;
  color: var(--text) !important;
  line-height: 1.15 !important;
  letter-spacing: -0.015em !important;
  background: linear-gradient(135deg, #E8E4D8, #B6AD90);
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
}
.header-meta { display: flex; flex-direction: column; gap: 5px; }
.tagline { display: flex; align-items: center; gap: 7px; flex-wrap: wrap; }
.header-sub {
  font-size: 0.68rem; color: var(--muted);
  letter-spacing: 0.09em; text-transform: uppercase; font-weight: 500;
}
.h-pill {
  font-size: 0.63rem; font-weight: 700;
  letter-spacing: 0.07em; padding: 2px 9px;
  border-radius: 999px; text-transform: uppercase;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: default;
}
.h-pill:hover { transform: translateY(-1px); box-shadow: 0 3px 10px rgba(0,0,0,0.3); }
.pill-g { background: #1e2e1c; color: #7fb574; border: 1px solid #3a5432; }
.pill-b { background: #1e2430; color: #7aafd4; border: 1px solid #2a4060; }
.pill-o { background: #2e2015; color: #c49a52; border: 1px solid #5a3a14; }
.status-badge {
  margin-left: auto; display: flex; align-items: center; gap: 6px;
  background: #182416; border: 1px solid #304828;
  border-radius: 999px; padding: 5px 14px;
  font-size: 0.7rem; color: #7fb574; font-weight: 600;
  white-space: nowrap;
  box-shadow: 0 0 12px rgba(127,181,116,0.12);
}
.s-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: #7fb574;
  box-shadow: 0 0 8px #7fb57488;
  animation: sblink 2.4s infinite;
}
@keyframes sblink { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.35;transform:scale(0.8)} }

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] section[data-testid="stSidebarContent"] {
  padding: 1.5rem 1.1rem !important;
}
.sb-head {
  display: flex; align-items: center; gap: 9px;
  margin-bottom: 4px;
}
.sb-icon {
  width: 30px; height: 30px; border-radius: 9px;
  background: linear-gradient(135deg, #3a4a28, #253020);
  border: 1px solid var(--moss);
  display: flex; align-items: center; justify-content: center;
  font-size: 15px;
  box-shadow: 0 2px 8px rgba(101,109,74,0.2);
}
.sb-title {
  font-size: 0.75rem; font-weight: 700;
  letter-spacing: 0.09em; text-transform: uppercase;
  color: var(--reseda);
}
.sb-caption {
  font-size: 0.76rem !important; color: var(--muted) !important;
  line-height: 1.6 !important; margin-bottom: 14px !important;
}
[data-testid="stFileUploader"] {
  background: var(--surface2) !important;
  border: 1.5px dashed var(--border-hi) !important;
  border-radius: 12px !important;
  transition: border-color 0.25s, background 0.25s, box-shadow 0.25s;
}
[data-testid="stFileUploader"]:hover {
  background: var(--surface3) !important;
  border-color: var(--reseda) !important;
  box-shadow: 0 0 16px rgba(164,172,134,0.12) !important;
}
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] small { color: var(--muted) !important; font-size: 0.79rem !important; }
[data-testid="stSidebar"] [data-testid="stImage"] img {
  border-radius: 10px !important;
  border: 1px solid var(--border-hi) !important;
  width: 100% !important;
  box-shadow: 0 6px 20px rgba(0,0,0,0.4) !important;
  margin-top: 8px !important;
  transition: transform 0.3s, box-shadow 0.3s;
}
[data-testid="stSidebar"] [data-testid="stImage"] img:hover {
  transform: scale(1.02) !important;
  box-shadow: 0 8px 28px rgba(0,0,0,0.5) !important;
}
[data-testid="stSidebar"] .stButton button {
  background: linear-gradient(135deg, #A4AC86 0%, #7a8060 60%, #5a6248 100%) !important;
  color: #15180e !important;
  border: none !important;
  border-radius: 11px !important;
  font-weight: 700 !important;
  font-size: 0.84rem !important;
  padding: 0.65rem 1.2rem !important;
  width: 100% !important;
  letter-spacing: 0.03em;
  transition: transform 0.18s, box-shadow 0.18s, filter 0.18s !important;
  box-shadow: 0 3px 14px rgba(100,109,74,0.32);
}
[data-testid="stSidebar"] .stButton button:hover {
  transform: translateY(-2px) !important;
  filter: brightness(1.08) !important;
  box-shadow: 0 6px 22px rgba(100,109,74,0.44) !important;
}
[data-testid="stSidebar"] .stButton button:active {
  transform: translateY(0px) !important;
  filter: brightness(0.95) !important;
}
.tips-card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-left: 3px solid var(--lion);
  border-radius: 11px;
  padding: 12px 14px;
  margin-top: 2px;
}
.tips-card .tips-title {
  font-size: 0.66rem; font-weight: 700;
  letter-spacing: 0.09em; text-transform: uppercase;
  color: var(--chamois); margin-bottom: 8px;
}
.tips-card ul { list-style: none; padding: 0; margin: 0; }
.tips-card ul li {
  font-size: 0.75rem; color: #7a8060;
  line-height: 1.7; padding-left: 14px; position: relative;
}
.tips-card ul li::before { content:"›"; position:absolute; left:0; color:var(--reseda); font-weight:700; }
.sb-divider { border: none; border-top: 1px solid var(--border); margin: 14px 0; }

/* ══════════════════════════════════════
   CUSTOM AVATAR OVERRIDE
   Replace Streamlit default avatar circles with
   distinct SVG icons via background-image trick
══════════════════════════════════════ */

/* --- USER avatar: teal-green person icon --- */
[data-testid="chatAvatarIcon-user"] {
  background: linear-gradient(145deg, #1a3830, #122820) !important;
  border: 2px solid #2d6650 !important;
  border-radius: 50% !important;
  box-shadow: 0 0 0 3px rgba(45,102,80,0.18), 0 3px 12px rgba(0,0,0,0.4) !important;
  overflow: hidden !important;
  transition: box-shadow 0.3s, transform 0.3s !important;
  position: relative;
}
[data-testid="chatAvatarIcon-user"]:hover {
  transform: scale(1.1) !important;
  box-shadow: 0 0 0 4px rgba(45,150,100,0.28), 0 4px 16px rgba(0,0,0,0.5) !important;
}
/* Hide the default letter/icon inside */
[data-testid="chatAvatarIcon-user"] > * { opacity: 0 !important; }
/* Inject SVG person via pseudo-element */
[data-testid="chatAvatarIcon-user"]::after {
  content: "";
  position: absolute; inset: 0;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Ccircle cx='18' cy='13' r='6' fill='%2364c896'/%3E%3Cellipse cx='18' cy='28' rx='10' ry='7' fill='%2364c896'/%3E%3C/svg%3E") center/70% no-repeat;
}

/* --- ASSISTANT avatar: orange-amber bot icon --- */
[data-testid="chatAvatarIcon-assistant"] {
  background: linear-gradient(145deg, #352210, #241508) !important;
  border: 2px solid #a0621a !important;
  border-radius: 50% !important;
  box-shadow: 0 0 0 3px rgba(160,98,26,0.20), 0 3px 12px rgba(0,0,0,0.4) !important;
  overflow: hidden !important;
  transition: box-shadow 0.3s, transform 0.3s !important;
  position: relative;
}
[data-testid="chatAvatarIcon-assistant"]:hover {
  transform: scale(1.1) !important;
  box-shadow: 0 0 0 4px rgba(200,130,40,0.30), 0 4px 16px rgba(0,0,0,0.5) !important;
}
[data-testid="chatAvatarIcon-assistant"] > * { opacity: 0 !important; }
/* Inject SVG robot via pseudo-element */
[data-testid="chatAvatarIcon-assistant"]::after {
  content: "";
  position: absolute; inset: 0;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect x='8' y='14' width='20' height='14' rx='4' fill='%23d4882a'/%3E%3Crect x='14' y='8' width='8' height='7' rx='3' fill='%23d4882a'/%3E%3Cline x1='18' y1='8' x2='18' y2='6' stroke='%23d4882a' stroke-width='2' stroke-linecap='round'/%3E%3Ccircle cx='18' cy='5' r='2' fill='%23f0b050'/%3E%3Ccircle cx='13' cy='20' r='2.5' fill='%23fff8ee'/%3E%3Ccircle cx='23' cy='20' r='2.5' fill='%23fff8ee'/%3E%3Crect x='13' y='24' width='10' height='2' rx='1' fill='%23fff8ee' opacity='0.6'/%3E%3Crect x='4' y='17' width='3' height='8' rx='1.5' fill='%23d4882a'/%3E%3Crect x='29' y='17' width='3' height='8' rx='1.5' fill='%23d4882a'/%3E%3C/svg%3E") center/75% no-repeat;
}

/* ══════════════════════════════════════
   CHAT MESSAGES
══════════════════════════════════════ */
[data-testid="stChatMessage"] {
  background: transparent !important;
  border: none !important;
  padding: 0.25rem 0 !important;
}

/* User bubble */
.stChatMessage:has([data-testid="chatAvatarIcon-user"]) [data-testid="stMarkdownContainer"] {
  background: var(--user-bg) !important;
  border: 1px solid var(--user-border) !important;
  border-radius: 20px 20px 5px 20px !important;
  padding: 0.85rem 1.2rem !important;
  color: var(--text) !important;
  font-size: 0.9rem !important; line-height: 1.7 !important;
  max-width: 72% !important; margin-left: auto !important;
  box-shadow: 0 2px 14px var(--user-glow), 0 1px 4px rgba(0,0,0,0.25);
  transition: transform 0.2s, box-shadow 0.2s;
  position: relative;
}
.stChatMessage:has([data-testid="chatAvatarIcon-user"]) [data-testid="stMarkdownContainer"]:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(100,172,100,0.14), 0 2px 8px rgba(0,0,0,0.3) !important;
}
/* left accent stripe on user bubble */
.stChatMessage:has([data-testid="chatAvatarIcon-user"]) [data-testid="stMarkdownContainer"]::before {
  content: "";
  position: absolute; right: -1px; top: 20%; bottom: 20%;
  width: 3px; border-radius: 999px;
  background: linear-gradient(180deg, #64c896, #2d7a54);
  opacity: 0.7;
}

/* Assistant bubble */
.stChatMessage:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stMarkdownContainer"] {
  background: var(--bot-bg) !important;
  border: 1px solid var(--bot-border) !important;
  border-radius: 20px 20px 20px 5px !important;
  padding: 0.85rem 1.2rem !important;
  color: var(--text) !important;
  font-size: 0.9rem !important; line-height: 1.75 !important;
  max-width: 84% !important;
  box-shadow: 0 2px 14px var(--bot-glow), 0 1px 4px rgba(0,0,0,0.25);
  transition: transform 0.2s, box-shadow 0.2s;
  position: relative;
}
.stChatMessage:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stMarkdownContainer"]:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(163,136,100,0.16), 0 2px 8px rgba(0,0,0,0.3) !important;
}
/* left accent stripe on bot bubble */
.stChatMessage:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stMarkdownContainer"]::before {
  content: "";
  position: absolute; left: -1px; top: 20%; bottom: 20%;
  width: 3px; border-radius: 999px;
  background: linear-gradient(180deg, #d4882a, #a0621a);
  opacity: 0.8;
}

/* ══════════════════════════════════════
   MARKDOWN
══════════════════════════════════════ */
.stMarkdown p  { margin-bottom: 0.5rem !important; }
.stMarkdown ul, .stMarkdown ol { padding-left: 1.4rem !important; }
.stMarkdown li { margin-bottom: 0.3rem !important; color: var(--text) !important; }
.stMarkdown strong { color: var(--chamois) !important; font-weight: 600 !important; }
.stMarkdown code {
  background: #252a1e !important;
  border: 1px solid var(--border-hi) !important;
  border-radius: 5px !important;
  padding: 0.15em 0.45em !important;
  font-size: 0.82em !important;
  color: var(--reseda) !important;
}
.stMarkdown a { color: var(--chamois) !important; text-decoration: none !important; transition: color 0.2s; }
.stMarkdown a:hover { color: var(--ash) !important; text-decoration: underline !important; }
.stMarkdown h2 { color: var(--ash) !important; font-size: 1rem !important; margin-top: 0.8rem !important; }
.stMarkdown h3 { color: var(--reseda) !important; font-size: 0.9rem !important; margin-top: 0.6rem !important; }
.stMarkdown blockquote {
  border-left: 3px solid var(--lion) !important;
  background: #242018 !important;
  padding: 0.5rem 0.9rem !important;
  border-radius: 0 8px 8px 0 !important;
  color: var(--text-dim) !important;
  margin: 0.5rem 0 !important;
}

/* ══════════════════════════════════════
   EMPTY STATE
══════════════════════════════════════ */
.empty-state { text-align: center; padding: 4.5rem 2rem 3rem; }
.empty-icon-ring {
  width: 88px; height: 88px; margin: 0 auto 1.4rem;
  border-radius: 50%;
  background: linear-gradient(145deg, #2b3820, #1c2416);
  border: 2px solid var(--moss);
  display: flex; align-items: center; justify-content: center;
  font-size: 2.4rem;
  box-shadow: 0 0 0 6px rgba(101,109,74,0.08), 0 8px 32px rgba(0,0,0,0.4);
  animation: ring-float 4s ease-in-out infinite;
}
@keyframes ring-float {
  0%,100% { transform: translateY(0); box-shadow: 0 0 0 6px rgba(101,109,74,0.08), 0 8px 32px rgba(0,0,0,0.4); }
  50%      { transform: translateY(-6px); box-shadow: 0 0 0 10px rgba(101,109,74,0.12), 0 16px 40px rgba(0,0,0,0.5); }
}
.empty-state h3 {
  font-family: 'DM Serif Display', serif;
  font-size: 1.55rem; color: var(--text); margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #E8E4D8, #B6AD90);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.empty-desc {
  font-size: 0.84rem; color: var(--text-dim);
  line-height: 1.75; max-width: 400px;
  margin: 0 auto 2rem;
}
.suggestion-row { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; }
.s-chip {
  border-radius: 999px; padding: 0.45rem 1.15rem;
  font-size: 0.77rem; font-weight: 500; cursor: default;
  transition: transform 0.22s, box-shadow 0.22s, filter 0.22s;
}
.s-chip:hover { transform: translateY(-2px); filter: brightness(1.18); box-shadow: 0 4px 14px rgba(0,0,0,0.35); }
.chip-a { background: #1e2c1c; color: #82b882; border: 1px solid #3a5432; }
.chip-b { background: #1c2530; color: #7aafd4; border: 1px solid #2a4060; }
.chip-c { background: #2a2416; color: #c49a52; border: 1px solid #5a3a14; }
.chip-d { background: #252220; color: #B6AD90; border: 1px solid #4a4030; }

/* ══════════════════════════════════════
   CHAT INPUT
══════════════════════════════════════ */
[data-testid="stChatInput"] {
  background: var(--surface) !important;
  border: 1.5px solid var(--border-hi) !important;
  border-radius: 16px !important;
  transition: border-color 0.22s, box-shadow 0.22s;
}
[data-testid="stChatInput"]:focus-within {
  border-color: var(--reseda) !important;
  box-shadow: 0 0 0 3px rgba(164,172,134,0.13), 0 4px 20px rgba(0,0,0,0.25) !important;
}
[data-testid="stChatInput"] textarea {
  background: transparent !important;
  color: var(--text) !important;
  font-family: var(--font) !important;
  font-size: 0.9rem !important;
  caret-color: var(--reseda) !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted) !important; }
[data-testid="stChatInputSubmitButton"] svg { fill: var(--reseda) !important; transition: fill 0.2s, transform 0.2s; }
[data-testid="stChatInputSubmitButton"]:hover svg { fill: var(--ash) !important; transform: scale(1.15) !important; }

/* spinner */
[data-testid="stSpinner"] { color: var(--reseda) !important; }

/* scrollbar */
::-webkit-scrollbar { width: 5px; background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* ── message slide-in animation ── */
[data-testid="stChatMessage"] {
  animation: msg-in 0.28s cubic-bezier(0.34,1.3,0.64,1) both;
}
@keyframes msg-in {
  from { opacity: 0; transform: translateY(10px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0)   scale(1);    }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("""
<div class="shop-header">
  <div class="header-icon-wrap">
    <div class="header-icon-bg">🛒</div>
  </div>
  <div class="header-meta">
    <h1>AI Shopping Assistant</h1>
    <div class="tagline">
      <span class="header-sub">Search · Compare · Order</span>
      <span class="h-pill pill-g">AI Search</span>
      <span class="h-pill pill-b">Auto Order</span>
      <span class="h-pill pill-o">Smart Rating</span>
    </div>
  </div>
  <div class="status-badge"><div class="s-dot"></div>Agent online</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar — shop by image
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sb-head">
      <div class="sb-icon">📷</div>
      <span class="sb-title">Shop by Image</span>
    </div>
    <p class="sb-caption">Upload a photo and I'll find similar products in the store.</p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload product image", type=["jpg", "jpeg", "png", "webp"]
    )
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

    if uploaded_file and st.button("Find similar products", use_container_width=True):
        suffix = os.path.splitext(uploaded_file.name)[1] or ".jpg"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            image_path = tmp.name
        prompt = f"I uploaded a product image. Please analyze it and find similar products in the store. Image path: {image_path}"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.pending_image = uploaded_file.name
        st.rerun()

    st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="tips-card">
      <div class="tips-title">💡 Tips for better results</div>
      <ul>
        <li>Be specific about brand, size, or colour</li>
        <li>Mention your budget for tighter matches</li>
        <li>Ask for alternatives if results don't fit</li>
        <li>Try "compare X vs Y" for side-by-side picks</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Chat state
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Empty state
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon-ring">🛍️</div>
      <h3>What are you looking for?</h3>
      <p class="empty-desc">
        Describe what you need and I'll search, compare, and order the best match —
        or upload a photo to find visually similar products.
      </p>
      <div class="suggestion-row">
        <div class="s-chip chip-a">🍯 Organic honey under $15</div>
        <div class="s-chip chip-b">🎧 Wireless earbuds with ANC</div>
        <div class="s-chip chip-c">👟 Running shoes size 10</div>
        <div class="s-chip chip-d">🖥️ 4K monitor under $400</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# Render history — show a friendlier label for image-search messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user" and msg["content"].startswith("I uploaded a product image"):
            filename = msg["content"].split("Image path:")[-1].strip()
            st.markdown(f"Searching by image: **{os.path.basename(filename)}**")
        else:
            st.markdown(msg["content"].replace("$", r"\$"))

# ---------------------------------------------------------------------------
# Run agent if there's an unprocessed message (image upload triggers this)
# ---------------------------------------------------------------------------
if (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
    and "pending_image" in st.session_state
):
    with st.chat_message("assistant"):
        with st.spinner("Analyzing image and searching…"):
            result = agent.invoke({"messages": st.session_state.messages})
            response = result["messages"][-1].content.replace("`", "")
        st.markdown(response.replace("$", r"\$"))
    st.session_state.messages.append({"role": "assistant", "content": response})
    del st.session_state.pending_image
    st.rerun()

# ---------------------------------------------------------------------------
# Text input
# ---------------------------------------------------------------------------
if prompt := st.chat_input("e.g. I want organic honey under $15 with 4+ rating"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            result = agent.invoke({"messages": st.session_state.messages})
            response = result["messages"][-1].content.replace("`", "")
        st.markdown(response.replace("$", r"\$"))
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()