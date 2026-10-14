from pathlib import Path
import json
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Math Jungle War", page_icon="🐒", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
#MainMenu, footer, header { visibility:hidden; height:0; }
[data-testid="stSidebar"] { display:none; }
[data-testid="stAppViewContainer"] .main { padding:0 !important; }
[data-testid="stMainBlockContainer"] { padding:0 !important; max-width:100% !important; }
[data-testid="stVerticalBlock"] { gap:0 !important; }
[data-testid="stElementContainer"] { margin:0 !important; padding:0 !important; }
[data-testid="stIFrame"], [data-testid="stIFrame"] iframe { height:100vh !important; min-height:100vh !important; width:100vw !important; display:block; border:0 !important; margin:0 !important; }
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).parent
HTML_FILE = BASE_DIR / "Math_Jungle_War.html"
if not HTML_FILE.exists():
    st.error("ไม่พบไฟล์ Math_Jungle_War.html กรุณาวางไฟล์ไว้โฟลเดอร์เดียวกับ app.py")
    st.stop()
try:
    supabase_url = st.secrets.get("SUPABASE_URL", "")
    supabase_key = st.secrets.get("SUPABASE_ANON_KEY", "")
except Exception:
    supabase_url = os.getenv("SUPABASE_URL", "")
    supabase_key = os.getenv("SUPABASE_ANON_KEY", "")
if not supabase_url or not supabase_key:
    st.warning("ระบบออนไลน์ยังไม่พร้อม: ตั้งค่า SUPABASE_URL และ SUPABASE_ANON_KEY ใน Streamlit Secrets ก่อนเปิดให้ผู้เล่นเข้าใช้งาน")
html = HTML_FILE.read_text(encoding="utf-8")
# Streamlit serves files in ./static at /app/static when enableStaticServing=true.
# Keep MP3 files in ./static/ so the embedded HTML iframe can fetch them.
for song_name in ("song1.mp3", "song2.mp3", "song3.mp3", "song4.mp3"):
    song_path = BASE_DIR / "static" / song_name
    if not song_path.exists():
        st.warning(f"ไม่พบไฟล์เพลง {song_name} — กรุณาวางไฟล์ไว้ในโฟลเดอร์ static")
    html = html.replace(f"src:'{song_name}'", f"src:'/app/static/{song_name}'")
html = html.replace("__MJW_SUPABASE_URL_JSON__", json.dumps(supabase_url))
html = html.replace("__MJW_SUPABASE_ANON_KEY_JSON__", json.dumps(supabase_key))
components.html(html, height=1000, scrolling=False, width=None)
