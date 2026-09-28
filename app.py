import streamlit as st
import numpy as np
import pickle

st.set_page_config(
    page_title="AI & Data Science ki Kitaab",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# STYLE
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;800&family=Playfair+Display:wght@700;900&display=swap');

#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background: linear-gradient(-45deg, #0f0c29, #1a0b3d, #2d0a52, #0f0c29);
    background-size: 400% 400%;
    animation: gradientShift 14s ease infinite;
    font-family: 'Poppins', sans-serif;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.block-container {
    max-width: 900px;
    margin: 0 auto;
    padding-top: 2rem;
    padding-bottom: 120px;
}

/* ---------- Landing hero ---------- */
.hero-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding-top: 20px;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 50px;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 8px #b026ff, 0 0 20px #b026ff, 0 0 40px #7b2ff7, 0 0 80px #00fff5;
    animation: flicker 4s ease-in-out infinite;
    margin-bottom: 6px;
    line-height: 1.15;
}
@keyframes flicker {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.88; }
}
.hero-subtitle {
    font-size: 16px;
    color: #cbb8ff;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 30px;
}

/* ---------- CSS Book ---------- */
.book-3d {
    position: relative;
    width: 160px; height: 220px;
    margin: 20px auto 40px auto;
    transform-style: preserve-3d;
    transform: rotateY(-25deg);
    animation: floatBook 5s ease-in-out infinite;
}
@keyframes floatBook {
    0%, 100% { transform: rotateY(-25deg) translateY(0px); }
    50% { transform: rotateY(-25deg) translateY(-14px); }
}
.book-cover {
    position: absolute; width: 160px; height: 220px;
    border-radius: 4px 8px 8px 4px;
    background: linear-gradient(135deg, #7b2ff7, #00c9ff);
    box-shadow: 0 0 25px rgba(176,38,255,0.65), 0 0 60px rgba(0,255,245,0.35), 10px 10px 30px rgba(0,0,0,0.5);
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 40px;
}
.book-spine {
    position: absolute; width: 18px; height: 220px; left: -16px;
    background: linear-gradient(180deg, #4b0f9c, #1a0b3d);
    transform: rotateY(90deg); transform-origin: right;
    border-radius: 4px 0 0 4px;
}
.book-pages {
    position: absolute; width: 150px; height: 210px; left: 4px; top: 5px;
    background: repeating-linear-gradient(180deg, #f5f3ff, #f5f3ff 2px, #e4defb 2px, #e4defb 3px);
    border-radius: 2px 6px 6px 2px;
    z-index: -1;
}

/* ---------- Feature chips ---------- */
.chip-row {
    display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;
    margin: 30px 0 10px 0;
}
.chip {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(176, 38, 255, 0.5);
    color: #e4defb; padding: 7px 16px; border-radius: 20px;
    font-size: 12.5px; letter-spacing: 1px;
}

/* ---------- Section divider ---------- */
.section-divider {
    width: 100%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(176,38,255,0.6), transparent);
    margin: 46px 0 34px 0;
}
.section-label {
    text-align: center; color: #8f7ac9; letter-spacing: 3px;
    font-size: 12px; text-transform: uppercase; margin-bottom: 18px;
}

/* ---------- Author card ---------- */
.author-card {
    display: flex; align-items: center; gap: 22px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(176, 38, 255, 0.35);
    border-radius: 18px; padding: 24px 26px;
    box-shadow: 0 0 30px rgba(123, 47, 247, 0.15);
}
.author-avatar {
    flex-shrink: 0; width: 72px; height: 72px; border-radius: 50%;
    background: linear-gradient(135deg, #7b2ff7, #00c9ff);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Playfair Display', serif; font-weight: 900; font-size: 26px;
    color: white; box-shadow: 0 0 20px rgba(0, 201, 255, 0.5);
}
.author-name { color: #fff; font-size: 19px; font-weight: 700; margin-bottom: 4px; }
.author-role { color: #00e5ff; font-size: 12.5px; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px; }
.author-bio { color: #cbb8ff; font-size: 14px; line-height: 1.6; }

/* ============================================================
   FLOATING CHAT WIDGET (portfolio-style)
   ============================================================ */
.st-key-fab_container {
    position: fixed !important;
    bottom: 26px; right: 26px;
    z-index: 9999;
}
.st-key-fab_container button {
    width: 60px; height: 60px;
    border-radius: 50% !important;
    font-size: 24px !important;
    background: linear-gradient(135deg, #7b2ff7, #00c9ff) !important;
    border: none !important;
    box-shadow: 0 0 20px rgba(123, 47, 247, 0.8), 0 4px 18px rgba(0,0,0,0.4) !important;
}

.st-key-chat_panel {
    position: fixed !important;
    bottom: 100px; right: 26px;
    width: 360px;
    z-index: 9998;
    background: linear-gradient(160deg, #1a0b3d, #120826);
    border: 1px solid rgba(176, 38, 255, 0.45);
    border-radius: 18px;
    padding: 14px 16px 12px 16px;
    box-shadow: 0 0 35px rgba(123, 47, 247, 0.35), 0 10px 40px rgba(0,0,0,0.5);
}

.widget-title {
    font-family: 'Playfair Display', serif;
    font-size: 17px; color: #fff; font-weight: 700;
    text-shadow: 0 0 8px #b026ff;
}
.widget-subtitle { color: #a996df; font-size: 11px; margin-top: -2px; }

.st-key-chat_panel .stButton button {
    background: transparent !important;
    border: none !important;
    color: #cbb8ff !important;
    box-shadow: none !important;
    font-size: 16px !important;
    padding: 0px 6px !important;
}

.st-key-msg_scroll {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 6px 4px;
}

.bubble {
    padding: 9px 13px;
    border-radius: 13px;
    font-size: 13.5px;
    line-height: 1.5;
    color: #f0eaff;
    margin: 4px 2px;
    max-width: 88%;
}
.bubble-user {
    background: linear-gradient(135deg, rgba(255, 93, 162, 0.25), rgba(123, 47, 247, 0.3));
    border: 1px solid rgba(255, 93, 162, 0.4);
    margin-left: auto;
    border-top-right-radius: 3px;
}
.bubble-assistant {
    background: rgba(0, 201, 255, 0.08);
    border: 1px solid rgba(0, 201, 255, 0.3);
    margin-right: auto;
    border-top-left-radius: 3px;
}

.st-key-chat_panel input[type="text"] {
    background: rgba(255,255,255,0.07) !important;
    color: #fff !important;
    border-radius: 10px !important;
    border: 1px solid rgba(176, 38, 255, 0.4) !important;
    font-size: 13.5px !important;
}
.st-key-chat_panel [data-testid="stFormSubmitButton"] button {
    background: linear-gradient(90deg, #7b2ff7, #00c9ff) !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    font-size: 13px !important;
    padding: 6px 14px !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA + RAG SETUP
# ============================================================
@st.cache_resource(show_spinner="Kitaab load ho rahi hai...")
def load_everything():
    import faiss
    from sentence_transformers import SentenceTransformer

    with open("chunks.pkl", "rb") as f:
        data = pickle.load(f)
    chunks = data["chunks"]
    chunk_pages = data["chunk_pages"]

    doc_vectors = np.load("embeddings.npy").astype("float32")
    dimension = doc_vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(doc_vectors)

    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    return chunks, chunk_pages, model, index


@st.cache_resource
def load_client():
    from groq import Groq
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


def rag_answer(question, chunks, model, index, client, k=6):
    q_vector = model.encode([question]).astype("float32")
    distances, ids = index.search(q_vector, k)
    contexts = [chunks[i] for i in ids[0]]
    combined_context = "\n\n---\n\n".join(contexts)

    prompt = f"""Neeche di gayi information ki base par sawal ka jawab Roman Urdu mein dein.
Agar jawab information mein nahi hai to kahein "Mujhe nahi pata".

Information:
{combined_context}

Sawal: {question}

Jawab:"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# ============================================================
# SESSION STATE
# ============================================================
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# HOMEPAGE (always visible, like a portfolio site)
# ============================================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">AI &amp; Data Science<br>ki Kitaab</div>
    <div class="hero-subtitle">Apni kitaab se, apne alfaz mein baat karein</div>
    <div class="book-3d">
        <div class="book-pages"></div>
        <div class="book-spine"></div>
        <div class="book-cover">📖</div>
    </div>
    <div class="chip-row">
        <div class="chip">🔎 RAG powered</div>
        <div class="chip">⚡ Groq LLM</div>
        <div class="chip">🧠 FAISS Vector Search</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Kitaab ke baare mein</div>', unsafe_allow_html=True)
st.markdown("""
<div class="author-card">
    <div class="author-avatar">JV</div>
    <div>
        <div class="author-name">Jake VanderPlas</div>
        <div class="author-role">Author &middot; Python Data Science Handbook</div>
        <div class="author-bio">
            Ye AI assistant "Python Data Science Handbook" par train kiya gaya hai —
            NumPy, Pandas, Matplotlib, Scikit-Learn aur data science ke buniyadi
            mafahim ki mashhoor, free-online kitaab. Neeche corner mein chat icon
            dabayein aur kitaab se koi bhi sawal Roman Urdu ya English mein pooch lein.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# FLOATING CHAT WIDGET
# ============================================================
with st.container(key="fab_container"):
    if st.button("💬" if not st.session_state.chat_open else "✕", key="fab_btn"):
        st.session_state.chat_open = not st.session_state.chat_open
        st.rerun()

if st.session_state.chat_open:
    with st.container(key="chat_panel"):
        st.markdown("""
        <div class="widget-title">📖 Kitaab Assistant</div>
        <div class="widget-subtitle">Python Data Science Handbook</div>
        """, unsafe_allow_html=True)

        chunks, chunk_pages, model, index = load_everything()
        client = load_client()

        with st.container(height=300, key="msg_scroll"):
            if not st.session_state.messages:
                st.markdown(
                    '<div class="bubble bubble-assistant">👋 Salam! Is kitaab se koi bhi sawal poochein.</div>',
                    unsafe_allow_html=True,
                )
            for msg in st.session_state.messages:
                cls = "bubble-user" if msg["role"] == "user" else "bubble-assistant"
                st.markdown(f'<div class="bubble {cls}">{msg["content"]}</div>', unsafe_allow_html=True)

        with st.form("widget_form", clear_on_submit=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                user_input = st.text_input(
                    "msg", label_visibility="collapsed", placeholder="Type your message..."
                )
            with c2:
                submitted = st.form_submit_button("Send")

        if submitted and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Soch raha hoon..."):
                answer = rag_answer(user_input, chunks, model, index, client)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
