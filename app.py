from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Math Jungle War",
    page_icon="🐒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Remove Streamlit's surrounding margins so the game can use the full viewport.
st.markdown(
    """
    <style>
      #MainMenu, footer, header { visibility: hidden; height: 0; }
      [data-testid="stSidebar"] { display: none; }
      [data-testid="stAppViewContainer"] .main { padding: 0 !important; }
      [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
        max-width: 100% !important;
      }
      [data-testid="stVerticalBlock"] { gap: 0 !important; }
      [data-testid="stElementContainer"] { margin: 0 !important; padding: 0 !important; }
      [data-testid="stIFrame"] {
        height: 100vh !important;
        min-height: 100vh !important;
        width: 100vw !important;
        margin: 0 !important;
      }
      [data-testid="stIFrame"] iframe {
        height: 100vh !important;
        min-height: 100vh !important;
        width: 100vw !important;
        display: block;
        border: 0 !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

HTML_FILE = Path(__file__).parent / "Math_Jungle_War_Game.html"

if not HTML_FILE.exists():
    st.error(
        "ไม่พบไฟล์เกม Math_Jungle_War_Game2_Scoreboard.html "
        "กรุณาวางไฟล์ HTML ไว้ในโฟลเดอร์เดียวกับ app.py"
    )
    st.stop()

html_content = HTML_FILE.read_text(encoding="utf-8")

# Give the iframe a viewport-sized height; CSS above keeps it full-screen.
components.html(html_content, height=1000, scrolling=False, width=None)
