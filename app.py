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
# STYLE: animated gradient background + neon glow + CSS book
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&family=Playfair+Display:wght@700;900&display=swap');

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

/* ---------- Landing hero ---------- */
.hero-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding-top: 40px;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 56px;
    font-weight: 900;
    color: #fff;
    text-shadow:
        0 0 8px #b026ff,
        0 0 20px #b026ff,
        0 0 40px #7b2ff7,
        0 0 80px #00fff5;
    animation: flicker 4s ease-in-out infinite;
    margin-bottom: 6px;
}

@keyframes flicker {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.88; }
}

.hero-subtitle {
    font-size: 18px;
    color: #cbb8ff;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 40px;
}

/* ---------- CSS Book ---------- */
.book-3d {
    position: relative;
    width: 180px;
    height: 250px;
    margin: 20px auto 50px auto;
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
    width: 180px;
    height: 250px;
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
    font-size: 44px;
}

.book-spine {
    position: absolute;
    width: 20px;
    height: 250px;
    left: -18px;
    background: linear-gradient(180deg, #4b0f9c, #1a0b3d);
    transform: rotateY(90deg);
    transform-origin: right;
    border-radius: 4px 0 0 4px;
}

.book-pages {
    position: absolute;
    width: 170px;
    height: 240px;
    left: 4px;
    top: 5px;
    background: repeating-linear-gradient(
        180deg,
        #f5f3ff,
        #f5f3ff 2px,
        #e4defb 2px,
        #e4defb 3px
    );
    border-radius: 2px 6px 6px 2px;
    z-index: -1;
}

/* ---------- Start button ---------- */
div.stButton > button {
    background: linear-gradient(90deg, #7b2ff7, #00c9ff);
    color: white;
    font-weight: 600;
    font-size: 18px;
    padding: 14px 34px;
    border-radius: 40px;
    border: none;
    box-shadow: 0 0 18px rgba(123, 47, 247, 0.7);
    transition: all 0.25s ease-in-out;
}
div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 30px rgba(0, 201, 255, 0.9);
    color: white;
}

/* ---------- Feature chips ---------- */
.chip-row {
    display: flex;
    gap: 14px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 36px;
}
.chip {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(176, 38, 255, 0.5);
    color: #e4defb;
    padding: 8px 18px;
    border-radius: 20px;
    font-size: 13px;
    letter-spacing: 1px;
}

/* ---------- Chat header ---------- */
.chat-header {
    text-align: center;
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    color: #fff;
    text-shadow: 0 0 10px #b026ff, 0 0 25px #00fff5;
    margin-bottom: 4px;
}
.chat-subheader {
    text-align: center;
    color: #cbb8ff;
    font-size: 14px;
    margin-bottom: 24px;
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
        <div class="hero-title">AI &amp; Data Science ki Kitaab</div>
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
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📖  Kitaab Kholein", use_container_width=True):
            st.session_state.started = True
            st.rerun()


# ============================================================
# CHAT PAGE
# ============================================================
else:
    st.markdown('<div class="chat-header">📖 Kitaab se Poochein</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-subheader">Python Data Science Handbook par mabni AI assistant</div>', unsafe_allow_html=True)

    chunks, chunk_pages, model, index = load_everything()
    client = load_client()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Kitaab se koi sawal poochein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Kitaab parh raha hoon..."):
                answer = rag_answer(prompt, chunks, model, index, client)
                st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    st.write("")
    if st.button("⬅ Wapas Cover Page par"):
        st.session_state.started = False
        st.rerun()
