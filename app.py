from pathlib import Path
import json
import os
import re
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Math Jungle War",
    page_icon="🐒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    #MainMenu, footer, header { visibility:hidden; height:0; }
    [data-testid="stSidebar"] { display:none; }
    [data-testid="stAppViewContainer"] .main { padding:0 !important; }
    [data-testid="stMainBlockContainer"] { padding:0 !important; max-width:100% !important; }
    [data-testid="stVerticalBlock"] { gap:0 !important; }
    [data-testid="stElementContainer"] { margin:0 !important; padding:0 !important; }
    [data-testid="stIFrame"], [data-testid="stIFrame"] iframe {
        height:100vh !important; min-height:100vh !important; width:100vw !important;
        display:block; border:0 !important; margin:0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = Path(__file__).resolve().parent

# Accept either common HTML filename used by the project's different ZIP versions.
html_candidates = [
    BASE_DIR / "Math_Jungle_War.html",
    BASE_DIR / "Math_Jungle_War_Shared_Leaderboard.html",
]
HTML_FILE = next((path for path in html_candidates if path.is_file()), None)
if HTML_FILE is None:
    expected = " หรือ ".join(path.name for path in html_candidates)
    st.error(f"ไม่พบไฟล์ HTML กรุณาวาง {expected} ไว้โฟลเดอร์เดียวกับ app.py")
    st.stop()

# Read the MP3 files from the static folder at the same level as app.py.
static_dir = BASE_DIR / "static"
song_names = ("song1.mp3", "song2.mp3", "song3.mp3", "song4.mp3")
missing_songs = [name for name in song_names if not (static_dir / name).is_file()]
if missing_songs:
    st.error(
        "ไม่พบไฟล์เพลง: " + ", ".join(missing_songs)
        + ". ต้องวางไฟล์ไว้ที่ static/ชื่อไฟล์.mp3 โดย static อยู่ระดับเดียวกับ app.py"
    )

# Streamlit static serving URL is /app/static/<filename> when enabled.
html = HTML_FILE.read_text(encoding="utf-8")
for song_name in song_names:
    url = f"/app/static/{song_name}"
    html = re.sub(
        rf"(src\s*:\s*['\"]){re.escape(song_name)}(['\"])",
        lambda match, url=url: match.group(1) + url + match.group(2),
        html,
    )

try:
    supabase_url = st.secrets.get("SUPABASE_URL", "")
    supabase_key = st.secrets.get("SUPABASE_ANON_KEY", "")
except Exception:
    supabase_url = os.getenv("SUPABASE_URL", "")
    supabase_key = os.getenv("SUPABASE_ANON_KEY", "")

if not supabase_url or not supabase_key:
    st.warning(
        "ระบบออนไลน์ยังไม่พร้อม: ตั้งค่า SUPABASE_URL และ SUPABASE_ANON_KEY ใน Streamlit Secrets "
        "หากต้องการใช้ leaderboard ออนไลน์"
    )

html = html.replace("__MJW_SUPABASE_URL_JSON__", json.dumps(supabase_url))
html = html.replace("__MJW_SUPABASE_ANON_KEY_JSON__", json.dumps(supabase_key))
components.html(html, height=1000, scrolling=False, width=None)
