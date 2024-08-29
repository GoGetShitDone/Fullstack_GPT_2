import streamlit as st

st.set_page_config(
    page_title="FullstackGPT Home",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom right, #0E1121, #2E3649);
        color: #FAFAFA;
    }
    .app-block {
        background-color: rgba(25, 30, 30, 0.7);
        border: 1px solid #333333;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
        transition: transform 0.3s, box-shadow 0.3s;
        cursor: pointer;
    }
    .app-block:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .app-block h2 {
        font-size: 3em;
        margin-bottom: 10px;
    }
    .app-block h3 {
        color: #FAFAFA;
    }
</style>
""", unsafe_allow_html=True)

st.title("Welcome to FullstackGPT! 👋")

st.markdown("Click on any of them to explore! 🗺️")

apps = [
    ("Document GPT", "📄", "/DocumentGPT"),
    ("Private GPT", "🔒", "/PrivateGPT"),
    ("Quiz GPT", "🧐", "/QuizGPT"),
    ("Site GPT", "🌐", "/SiteGPT"),
    ("Meeting GPT", "🔗", "/MeetingGPT"),
    ("Investor GPT", "📈", "/InvestorGPT")
]

def create_app_block(title, emoji, url):
    return f"""
    <a href="{url}" style="text-decoration: none; color: inherit;">
        <div class="app-block">
            <h2>{emoji}</h2>
            <h3>{title}</h3>
        </div>
    </a>
    """

col1, col2 = st.columns(2)

for i, (title, emoji, url) in enumerate(apps):
    if i % 2 == 0:
        col1.markdown(create_app_block(title, emoji, url), unsafe_allow_html=True)
    else:
        col2.markdown(create_app_block(title, emoji, url), unsafe_allow_html=True)