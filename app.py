from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Math Jungle War",
    page_icon="🐒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

HTML_FILE = Path(__file__).parent / "Math_Jungle_War_Game2_Scoreboard.html"

if not HTML_FILE.exists():
    st.error(
        "ไม่พบไฟล์เกม Math_Jungle_War_Game2_Scoreboard.html "
        "กรุณาวางไฟล์ HTML ไว้ในโฟลเดอร์เดียวกับ app.py"
    )
    st.stop()

html_content = HTML_FILE.read_text(encoding="utf-8")

# Render the HTML/CSS/JavaScript game inside Streamlit's HTML component.
components.html(html_content, height=850, scrolling=False)
