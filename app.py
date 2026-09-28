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
# STYLE: animated gradient background + neon glow + real chat UI
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
    max-width: 820px;
    margin: 0 auto;
    padding-top: 2rem;
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
    text-shadow:
        0 0 8px #b026ff,
        0 0 20px #b026ff,
        0 0 40px #7b2ff7,
        0 0 80px #00fff5;
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
    width: 160px;
    height: 220px;
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
    position: absolute;
    width: 160px;
    height: 220px;
    border-radius: 4px 8px 8px 4px;
    background: linear-gradient(135deg, #7b2ff7, #00c9ff);
    box-shadow:
        0 0 25px rgba(176, 38, 255, 0.65),
        0 0 60px rgba(0, 255, 245, 0.35),
        10px 10px 30px rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 40px;
}

.book-spine {
    position: absolute;
    width: 18px;
    height: 220px;
    left: -16px;
    background: linear-gradient(180deg, #4b0f9c, #1a0b3d);
    transform: rotateY(90deg);
    transform-origin: right;
    border-radius: 4px 0 0 4px;
}

.book-pages {
    position: absolute;
    width: 150px;
    height: 210px;
    left: 4px;
    top: 5px;
    background: repeating-linear-gradient(
        180deg, #f5f3ff, #f5f3ff 2px, #e4defb 2px, #e4defb 3px
    );
    border-radius: 2px 6px 6px 2px;
    z-index: -1;
}

/* ---------- Buttons ---------- */
div.stButton > button {
    background: linear-gradient(90deg, #7b2ff7, #00c9ff);
    color: white;
    font-weight: 600;
    font-size: 17px;
    padding: 12px 30px;
    border-radius: 40px;
    border: none;
    box-shadow: 0 0 18px rgba(123, 47, 247, 0.7);
    transition: all 0.25s ease-in-out;
}
div.stButton > button:hover {
    transform: scale(1.04);
    box-shadow: 0 0 30px rgba(0, 201, 255, 0.9);
    color: white;
}

/* ---------- Feature chips ---------- */
.chip-row {
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 30px 0 10px 0;
}
.chip {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(176, 38, 255, 0.5);
    color: #e4defb;
    padding: 7px 16px;
    border-radius: 20px;
    font-size: 12.5px;
    letter-spacing: 1px;
}

/* ---------- Section divider ---------- */
.section-divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(176,38,255,0.6), transparent);
    margin: 46px 0 34px 0;
}

.section-label {
    text-align: center;
    color: #8f7ac9;
    letter-spacing: 3px;
    font-size: 12px;
    text-transform: uppercase;
    margin-bottom: 18px;
}

/* ---------- Author card ---------- */
.author-card {
    display: flex;
    align-items: center;
    gap: 22px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(176, 38, 255, 0.35);
    border-radius: 18px;
    padding: 24px 26px;
    box-shadow: 0 0 30px rgba(123, 47, 247, 0.15);
}
.author-avatar {
    flex-shrink: 0;
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7b2ff7, #00c9ff);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 26px;
    color: white;
    box-shadow: 0 0 20px rgba(0, 201, 255, 0.5);
}
.author-name {
    color: #fff;
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 4px;
}
.author-role {
    color: #00e5ff;
    font-size: 12.5px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.author-bio {
    color: #cbb8ff;
    font-size: 14px;
    line-height: 1.6;
}

/* ---------- Chat header ---------- */
.chat-header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 14px;
    margin-bottom: 18px;
    border-bottom: 1px solid rgba(176, 38, 255, 0.3);
}
.chat-header-title {
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    color: #fff;
    text-shadow: 0 0 10px #b026ff, 0 0 22px #00fff5;
}
.chat-header-sub {
    color: #a996df;
    font-size: 12.5px;
    margin-top: 2px;
}

/* ---------- Chat bubbles (override Streamlit chat_message) ---------- */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 4px 0 !important;
    max-width: 100%;
}

[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #ff5da2, #7b2ff7) !important;
    box-shadow: 0 0 12px rgba(255, 93, 162, 0.6);
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, #00c9ff, #7b2ff7) !important;
    box-shadow: 0 0 12px rgba(0, 201, 255, 0.6);
}

.bubble {
    padding: 14px 18px;
    border-radius: 16px;
    font-size: 15px;
    line-height: 1.6;
    color: #f0eaff;
}
.bubble-user {
    background: linear-gradient(135deg, rgba(255, 93, 162, 0.22), rgba(123, 47, 247, 0.28));
    border: 1px solid rgba(255, 93, 162, 0.4);
    border-top-left-radius: 4px;
}
.bubble-assistant {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(0, 201, 255, 0.3);
    border-top-left-radius: 4px;
}

/* ---------- Chat input ---------- */
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.06) !important;
    color: #fff !important;
    border-radius: 14px !important;
    border: 1px solid rgba(176, 38, 255, 0.4) !important;
}

.back-link {
    color: #a996df;
    font-size: 13px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA + RAG SETUP (cached so it loads once, not every rerun)
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
if "started" not in st.session_state:
    st.session_state.started = False
if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# LANDING PAGE
# ============================================================
if not st.session_state.started:
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

    st.write("")
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("📖  Kitaab Kholein", use_container_width=True):
            st.session_state.started = True
            st.rerun()

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
                mafahim ki mashhoor, free-online kitaab. Aap is kitaab se koi bhi sawal
                Roman Urdu ya English mein pooch sakte hain, jawab seedha kitaab ke
                content se banaya jata hai.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CHAT PAGE
# ============================================================
else:
    top_left, top_right = st.columns([5, 1])
    with top_left:
        st.markdown("""
        <div class="chat-header-bar">
            <div>
                <div class="chat-header-title">📖 Kitaab se Poochein</div>
                <div class="chat-header-sub">Python Data Science Handbook &middot; AI Assistant</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with top_right:
        if st.button("⬅ Wapas"):
            st.session_state.started = False
            st.rerun()

    chunks, chunk_pages, model, index = load_everything()
    client = load_client()

    for msg in st.session_state.messages:
        bubble_class = "bubble-user" if msg["role"] == "user" else "bubble-assistant"
        avatar = "🧑" if msg["role"] == "user" else "📖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(f'<div class="bubble {bubble_class}">{msg["content"]}</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("Kitaab se koi sawal poochein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(f'<div class="bubble bubble-user">{prompt}</div>', unsafe_allow_html=True)

        with st.chat_message("assistant", avatar="📖"):
            with st.spinner("Kitaab parh raha hoon..."):
                answer = rag_answer(prompt, chunks, model, index, client)
                st.markdown(f'<div class="bubble bubble-assistant">{answer}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": answer})
