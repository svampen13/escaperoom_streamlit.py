import streamlit as st
import streamlit.components.v1 as components
import time
import base64
import os

# Page configuration - Clean without emojis in title or page_icon
st.set_page_config(
    page_title="Escape Room Hub",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Styling for Clean, Dark High-Contrast UI
st.markdown("""
    <style>
    /* Hide Streamlit chrome elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    
    .main {
        background-color: #0f172a;
        padding: 20px 40px !important;
    }
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    h1, h2, h3, h4 {
        color: #f8fafc !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .section-title {
        color: #38bdf8 !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        margin-bottom: 20px !important;
        line-height: 1.2 !important;
        text-transform: uppercase;
    }
    
    div[data-testid="stRadio"] > label p {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
        margin-bottom: 15px !important;
    }
    
    div[role="radiogroup"] label {
        background-color: #1e293b !important;
        padding: 18px 22px !important;
        border-radius: 12px !important;
        border: 2px solid #334155 !important;
        margin-bottom: 14px !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.2s ease-in-out;
    }
    
    div[role="radiogroup"] label p, div[role="radiogroup"] label span, div[role="radiogroup"] label div {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        line-height: 1.4 !important;
    }
    
    div[role="radiogroup"] label:hover {
        border-color: #38bdf8 !important;
        background-color: #0f172a !important;
        cursor: pointer;
    }
    
    div[data-testid="stSelectbox"] label p, label[data-testid="stWidgetLabel"] p {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        margin-bottom: 8px !important;
    }
    
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        font-size: 18px !important;
        background-color: #1e293b !important;
        border: 2px solid #334155 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
        font-size: 18px !important;
        color: #ffffff !important;
    }
    
    div[data-testid="stCheckbox"] label p, div[data-testid="stCheckbox"] label span {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        line-height: 1.4 !important;
    }
    
    div[data-testid="stCheckbox"] {
        margin-top: 15px !important;
    }
    
    .stTextInput > div > div > input {
        font-size: 32px !important;
        text-align: center;
        background-color: #1e293b;
        color: #ffffff;
        border: 2px solid #38bdf8;
        border-radius: 6px;
        padding: 10px;
    }
    .success-card {
        background-color: #064e3b;
        border-left: 6px solid #4ade80;
        padding: 20px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: bold;
        color: #4ade80;
        margin-top: 20px;
        white-space: pre-wrap;
    }
    .hint-card {
        background-color: #334155;
        border-left: 6px solid #facc15;
        padding: 15px;
        border-radius: 6px;
        font-size: 18px;
        color: #fde047;
        margin-top: 15px;
    }
    .timer-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 12px;
        border-radius: 6px;
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        color: #38bdf8;
        margin-bottom: 20px;
    }
    .log-card {
        background-color: #1e293b;
        border-left: 4px solid #38bdf8;
        padding: 16px 20px;
        border-radius: 6px;
        margin-top: 25px;
    }
    .log-title {
        font-size: 20px;
        font-weight: bold;
        color: #38bdf8;
        margin-bottom: 10px;
    }
    .log-item {
        font-size: 18px;
        color: #cbd5e1;
        margin-bottom: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Background music helper function
def play_background_music(file_path="bakgrundsmusik.mp3"):
    if st.session_state.get("enable_audio", True):
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                    b64 = base64.b64encode(data).decode()
                    audio_html = f"""
                    <audio autoplay loop style="display:none;">
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                    """
                    components.html(audio_html, height=0, width=0)
            except Exception:
                pass

# Audio synthesis via WebAudio API
def play_audio(sound_type):
    if st.session_state.get("enable_audio", True):
        if sound_type == "heartbeat":
            js = """<script>
            if (!window.heartbeatInterval) {
                var ctx = new (window.AudioContext || window.webkitAudioContext)();
                function playBeat() {
                    try {
                        var now = ctx.currentTime;
                        var osc1 = ctx.createOscillator();
                        var gain1 = ctx.createGain();
                        osc1.connect(gain1); gain1.connect(ctx.destination);
                        osc1.type = 'sine';
                        osc1.frequency.setValueAtTime(60, now);
                        osc1.frequency.exponentialRampToValueAtTime(30, now + 0.12);
                        gain1.gain.setValueAtTime(0.3, now);
                        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
                        osc1.start(now); osc1.stop(now + 0.12);

                        var osc2 = ctx.createOscillator();
                        var gain2 = ctx.createGain();
                        osc2.connect(gain2); gain2.connect(ctx.destination);
                        osc2.type = 'sine';
                        osc2.frequency.setValueAtTime(50, now + 0.18);
                        osc2.frequency.exponentialRampToValueAtTime(25, now + 0.32);
                        gain2.gain.setValueAtTime(0.25, now + 0.18);
                        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.32);
                        osc2.start(now + 0.18); osc2.stop(now + 0.32);
                    } catch(e) {}
                }
                playBeat();
                window.heartbeatInterval = setInterval(playBeat, 2200);
            }
            </script>"""
            components.html(js, height=0, width=0)
        elif sound_type == "stop_heartbeat":
            js = """<script>
            if (window.heartbeatInterval) {
                clearInterval(window.heartbeatInterval);
                window.heartbeatInterval = null;
            }
            </script>"""
            components.html(js, height=0, width=0)
        elif sound_type == "correct":
            js = """<script>
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            var osc = ctx.createOscillator();
            var gain = ctx.createGain();
            osc.connect(gain); gain.connect(ctx.destination);
            osc.type = 'sine'; osc.frequency.setValueAtTime(523.25, ctx.currentTime);
            osc.frequency.setValueAtTime(659.25, ctx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.25, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
            osc.start(); osc.stop(ctx.currentTime + 0.4);
            </script>"""
            components.html(js, height=0, width=0)
        elif sound_type == "wrong":
            js = """<script>
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            var osc = ctx.createOscillator();
            var gain = ctx.createGain();
            osc.connect(gain); gain.connect(ctx.destination);
            osc.type = 'sawtooth'; osc.frequency.setValueAtTime(180, ctx.currentTime);
            osc.frequency.setValueAtTime(130, ctx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.2, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);
            osc.start(); osc.stop(ctx.currentTime + 0.35);
            </script>"""
            components.html(js, height=0, width=0)
        elif sound_type == "victory":
            js = """<script>
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            [523.25, 659.25, 783.99, 1046.50].forEach(function(freq, idx) {
                var osc = ctx.createOscillator();
                var gain = ctx.createGain();
                osc.connect(gain); gain.connect(ctx.destination);
                osc.type = 'sine'; osc.frequency.setValueAtTime(freq, ctx.currentTime + idx*0.2);
                gain.gain.setValueAtTime(0.25, ctx.currentTime + idx*0.2);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx*0.2 + 0.5);
                osc.start(ctx.currentTime + idx*0.2);
                osc.stop(ctx.currentTime + idx*0.2 + 0.5);
            });
            </script>"""
            components.html(js, height=0, width=0)

# Embedded Base64 Image string for Elice
ELICE_IMAGE_B64 = "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"

# Function to render Elice arrest image cleanly with animated 3D Jail Bars overlay
def render_elice_arrest_card():
    img_src = ""
    if ELICE_IMAGE_B64:
        img_src = f"data:image/jpeg;base64,{ELICE_IMAGE_B64}"
    elif os.path.exists('.'):
        for fn in os.listdir('.'):
            if fn.lower().startswith('elice') and fn.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                try:
                    with open(fn, 'rb') as f:
                        img_src = f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
                    break
                except Exception:
                    pass

    if img_src:
        jail_html = f"""
        <div style="display:flex; justify-content:center; align-items:center; margin: 20px 0;">
            <div style="position:relative; width:100%; max-width:480px; border-radius:12px; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.8); border:3px solid #334155; background:#0f172a;">
                <img src="{img_src}" style="width:100%; display:block; filter: contrast(1.1) brightness(0.95);" alt="Elice">
                
                <!-- Falling 3D Steel Bars Overlay -->
                <div style="position:absolute; top:0; left:0; width:100%; height:100%; display:flex; justify-space-around; pointer-events:none; z-index:10; animation: dropBars 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;">
                    <div style="flex:1; margin:0 6px; background:linear-gradient(90deg, #334155 0%, #cbd5e1 50%, #1e293b 100%); box-shadow: 2px 0 8px rgba(0,0,0,0.7); border-radius:3px;"></div>
                    <div style="flex:1; margin:0 6px; background:linear-gradient(90deg, #334155 0%, #cbd5e1 50%, #1e293b 100%); box-shadow: 2px 0 8px rgba(0,0,0,0.7); border-radius:3px;"></div>
                    <div style="flex:1; margin:0 6px; background:linear-gradient(90deg, #334155 0%, #cbd5e1 50%, #1e293b 100%); box-shadow: 2px 0 8px rgba(0,0,0,0.7); border-radius:3px;"></div>
                    <div style="flex:1; margin:0 6px; background:linear-gradient(90deg, #334155 0%, #cbd5e1 50%, #1e293b 100%); box-shadow: 2px 0 8px rgba(0,0,0,0.7); border-radius:3px;"></div>
                    <div style="flex:1; margin:0 6px; background:linear-gradient(90deg, #334155 0%, #cbd5e1 50%, #1e293b 100%); box-shadow: 2px 0 8px rgba(0,0,0,0.7); border-radius:3px;"></div>
                    <div style="flex:1; margin:0 6px; background:linear-gradient(90deg, #334155 0%, #cbd5e1 50%, #1e293b 100%); box-shadow: 2px 0 8px rgba(0,0,0,0.7); border-radius:3px;"></div>
                </div>
                
                <!-- Horizontal Lock Bars -->
                <div style="position:absolute; top:25%; left:0; width:100%; height:14px; background:linear-gradient(180deg, #475569 0%, #94a3b8 50%, #1e293b 100%); box-shadow:0 3px 6px rgba(0,0,0,0.6); z-index:11;"></div>
                <div style="position:absolute; top:70%; left:0; width:100%; height:14px; background:linear-gradient(180deg, #475569 0%, #94a3b8 50%, #1e293b 100%); box-shadow:0 3px 6px rgba(0,0,0,0.6); z-index:11;"></div>

                <!-- Red Slam Stamp -->
                <div style="position:absolute; bottom:15px; left:50%; transform:translateX(-50%); width:90%; background:rgba(185, 28, 28, 0.92); border:3px solid #ef4444; border-radius:8px; padding:10px 5px; text-align:center; box-shadow:0 6px 20px rgba(0,0,0,0.9); z-index:12; animation: stampSlam 0.5s ease-out 0.6s both;">
                    <div style="color:#ffffff; font-weight:900; font-size:22px; letter-spacing:2px; text-transform:uppercase; font-family:sans-serif;">ARRESTERAD</div>
                    <div style="color:#fecaca; font-weight:700; font-size:13px; letter-spacing:1px; margin-top:2px; font-family:sans-serif;">ELICE 'SKUGGAN' — LÅST INOM LÅS OCH BOM</div>
                </div>
            </div>
        </div>

        <style>
        @keyframes dropBars {{
            0% {{ transform: translateY(-100%); }}
            100% {{ transform: translateY(0); }}
        }}
        @keyframes stampSlam {{
            0% {{ transform: translate(-50%, -100px) scale(2); opacity: 0; }}
            100% {{ transform: translate(-50%, 0) scale(1); opacity: 1; }}
        }}
        </style>
        
        <script>
        try {{
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            var now = ctx.currentTime;
            var osc = ctx.createOscillator();
            var gain = ctx.createGain();
            osc.connect(gain); gain.connect(ctx.destination);
            osc.type = 'square'; osc.frequency.setValueAtTime(120, now);
            osc.frequency.exponentialRampToValueAtTime(40, now + 0.25);
            gain.gain.setValueAtTime(0.4, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
            osc.start(now); osc.stop(now + 0.25);
        }} catch(e) {{}}
        </script>
        """
        components.html(jail_html, height=520)
    else:
        st.warning("Lägg bilden elice_animation_preview.png i ditt GitHub-arkiv för att visa fotot på Elice här!")

# Themes & Stages Definition
THEMES = {
    "sns": {
        "name": "Vem är den skyldige i SNS?",
        "description": "Använd verktygen och materialet i utredningsväskan för att hitta spår och lösa fallet.",
        "disabled": False,
        "stages": [
            {
                "title": "ETAPP 1: Brottsplatsen",
                "prompt": "Undersök brottsplatskartan i Kuvert 1 med hjälp av verktygen i utredningsväskan. Skriv in koden du får fram:",
                "code": "42",
                "summary": "Fotspår storlek 42 bekräftat på brottsplatsen.",
                "hint": "Använd UV-lampan ur utredningsväskan på fotspåret i Kuvert 1 för att avläsa den dolda skostorleken. Jämför med de 7 personalkorten.",
                "success_msg": "KOD GODKÄND!\n\nSpåret är bekräftat (skostorlek 42). Använd informationen för att granska de 7 personalkorten i er utredningsväska.\n\n📍 GÅ TILL BOKHYLLAN I KLASSRUMMET OCH HÄMTA KUVERT 2!",
                "next_btn": "FORTSÄTT TILL ETAPP 2 →"
            },
            {
                "title": "ETAPP 2: Vittnesförhören & Alibin",
                "prompt": "Studera förhören i Kuvert 2 och räkna antalet fel. Skriv in koden för klockslaget då brottet ägde rum (4 siffror):",
                "code": "1500",
                "summary": "Tidpunkt för brottet bekräftad till kl. 15:00.",
                "hint": "Räkna stavfelen i förhörsprotokollets fyra avsnitt (1 fel, 5 fel, 0 fel, 0 fel = 1500, dvs kl. 15:00). Jämför alibin på de kvarvarande personalkorten.",
                "success_msg": "KOD GODKÄND!\n\nTidpunkten för brottet är bekräftad till kl. 15:00. Jämför klockslaget med alibin på personalkorten.\n\n📍 HÄMTA KUVERT 3 UNDER LÄRARBORDET!",
                "next_btn": "FORTSÄTT TILL ETAPP 3 →"
            },
            {
                "title": "ETAPP 3: Bevisanalys",
                "prompt": "Granska dokumentet i Kuvert 3. När ni undersöker det på rätt sätt kommer koden att framträda. Mata in koden här:",
                "code": "HÖGER",
                "summary": "Förövaren bekräftad HÖGERHÄNT.",
                "hint": "Undersök dokumentet i Kuvert 3 mot ett fönster eller med en spegel för att avläsa den dolda slutsatsen.",
                "success_msg": "KOD GODKÄND!\n\nSlutsatsen i rapporten är bekräftad. Använd informationen för att granska personalkorten.\n\n📍 HÄMTA KUVERT 4 I SKÅPET LÄNGST BAK!",
                "next_btn": "FORTSÄTT TILL ETAPP 4 →"
            },
            {
                "title": "ETAPP 4: Slutgiltigt Chiffer & Utpekande",
                "prompt": "Använd chiffermallen ur utredningsväskan över loggboken i Kuvert 4. Skriv in namnet på den skyldige:",
                "code": "ELICE",
                "summary": "Den skyldige identifierad: ELICE.",
                "hint": "Lägg hålmallens stjärnmärkta hörn mot loggbokens övre högra hörn. Läs bokstäverna i fönstren i ordningsföljd.",
                "success_msg": "FALLET LÖST!\n\nDen skyldige i SNS är identifierad: ELICE! Utmärkt utredningsarbete!",
                "next_btn": "AVSLUTA UPPDRAGET"
            }
        ]
    },
    "kommande1": {
        "name": "Kommande uppdrag",
        "description": "Detta uppdrag är inte tillgängligt ännu.",
        "disabled": True,
        "stages": []
    },
    "kommande2": {
        "name": "Kommande uppdrag",
        "description": "Detta uppdrag är inte tillgängligt ännu.",
        "disabled": True,
        "stages": []
    }
}

# Session State Initialization
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "current_stage" not in st.session_state:
    st.session_state.current_stage = 0
if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "sns"
if "show_hint" not in st.session_state:
    st.session_state.show_hint = False
if "stage_cleared" not in st.session_state:
    st.session_state.stage_cleared = False
if "timer_minutes" not in st.session_state:
    st.session_state.timer_minutes = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "stage_start_time" not in st.session_state:
    st.session_state.stage_start_time = time.time()
if "hint_lock_minutes" not in st.session_state:
    st.session_state.hint_lock_minutes = 3
if "enable_audio" not in st.session_state:
    st.session_state.enable_audio = True
if "solved_log" not in st.session_state:
    st.session_state.solved_log = []

# Sidebar controls
st.sidebar.title("Inställningar")
if st.sidebar.button("Nollställ / Huvudmeny"):
    st.session_state.game_started = False
    st.session_state.current_stage = 0
    st.session_state.stage_cleared = False
    st.session_state.show_hint = False
    st.session_state.solved_log = []
    st.rerun()

# Main Menu View
if not st.session_state.game_started:
    play_audio("heartbeat")
    
    st.markdown("<h1 style='text-align: center; color: #38bdf8; font-size: 42px; margin-bottom: 5px; font-weight: 800;'>ESCAPE ROOM HUB</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 22px; margin-bottom: 25px;'>Välj uppdrag och inställningar nedan för att starta</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    col_left, col_right = st.columns([1.6, 1], gap="large")
    
    with col_left:
        theme_options = list(THEMES.keys())
        theme_choice = st.radio(
            "VÄLJ UPPDRAG:",
            options=theme_options,
            format_func=lambda x: f"{THEMES[x]['name']} — {THEMES[x]['description']}" if not THEMES[x]['disabled'] else f"{THEMES[x]['name']} (Ej tillgängligt)"
        )
        st.session_state.selected_theme = theme_choice

    with col_right:
        st.markdown("<div class='section-title'>INSTÄLLNINGAR:</div>", unsafe_allow_html=True)
        
        timer_choice = st.selectbox(
            "Tidsgräns för hela spelet:",
            options=["Fri tid (Ingen timer)", "30 minuter", "45 minuter", "60 minuter"]
        )
        if "30" in timer_choice:
            st.session_state.timer_minutes = 30
        elif "45" in timer_choice:
            st.session_state.timer_minutes = 45
        elif "60" in timer_choice:
            st.session_state.timer_minutes = 60
        else:
            st.session_state.timer_minutes = 0
            
        hint_lock_choice = st.selectbox(
            "Tidsspärr för ledtrådar:",
            options=["3 minuter (Standard)", "2 minuter", "4 minuter", "Ingen spärr (Öppen direkt)"]
        )
        if "2" in hint_lock_choice:
            st.session_state.hint_lock_minutes = 2
        elif "4" in hint_lock_choice:
            st.session_state.hint_lock_minutes = 4
        elif "Ingen" in hint_lock_choice:
            st.session_state.hint_lock_minutes = 0
        else:
            st.session_state.hint_lock_minutes = 3
            
        st.session_state.enable_audio = st.checkbox("Aktivera ljudeffekter & bakgrundsljud", value=True)
    
    st.write("---")
    
    is_disabled = THEMES[theme_choice]["disabled"]
    if is_disabled:
        st.warning("Det valda uppdraget är inte tillgängligt ännu.")
    else:
        if st.button("STARTA UPPDRAG", type="primary", use_container_width=True):
            play_audio("stop_heartbeat")
            st.session_state.game_started = True
            st.session_state.current_stage = 0
            st.session_state.stage_cleared = False
            st.session_state.show_hint = False
            st.session_state.solved_log = []
            st.session_state.start_time = time.time()
            st.session_state.stage_start_time = time.time()
            st.rerun()

# Active Game View
else:
    play_audio("stop_heartbeat")
    play_background_music("bakgrundsmusik.mp3")
    theme = THEMES[st.session_state.selected_theme]
    stages = theme["stages"]
    
    # Optional Timer display
    if st.session_state.timer_minutes > 0:
        elapsed = time.time() - st.session_state.start_time
        total_sec = st.session_state.timer_minutes * 60
        remaining = max(0, int(total_sec - elapsed))
        mins, secs = divmod(remaining, 60)
        
        timer_color = "#38bdf8" if remaining > 300 else "#ef4444"
        st.markdown(f"<div class='timer-card' style='color:{timer_color};'>ÅTERSTÅENDE TID: {mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)
    
    # Check if game completed
    if st.session_state.current_stage >= len(stages):
        play_audio("victory")
        st.balloons()
        st.markdown("<h1 style='text-align: center; color: #4ade80;'>FALLET LÖST!</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #f8fafc;'>Utmärkt utredningsarbete! Den skyldige har blivit identifierad och gripen.</h3>", unsafe_allow_html=True)
        
        # Render Elice arrest card with animated Jail Bars overlay
        render_elice_arrest_card()
        
        # Final summary log
        if st.session_state.solved_log:
            st.markdown("<div class='log-card'>", unsafe_allow_html=True)
            st.markdown("<div class='log-title'>SAMMANFATTNING AV BEVIS OCH KODER:</div>", unsafe_allow_html=True)
            for item in st.session_state.solved_log:
                st.markdown(f"<div class='log-item'>✓ {item}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.write("")
        if st.button("Tillbaka till huvudmenyn", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.current_stage = 0
            st.session_state.stage_cleared = False
            st.session_state.solved_log = []
            st.rerun()
    else:
        stage = stages[st.session_state.current_stage]
        
        st.markdown(f"## {stage['title']}")
        st.markdown(f"#### {stage['prompt']}")
        
        if not st.session_state.stage_cleared:
            code_input = st.text_input("Mata in koden här:", key=f"code_in_{st.session_state.current_stage}", placeholder="KOD").strip()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("LÅS UPP", type="primary", use_container_width=True):
                    # Flexible check for stage code
                    user_val = code_input.upper()
                    target_val = stage["code"].upper()
                    
                    is_correct = False
                    if target_val == "42" and user_val in ["42", "SKOSTORLEK 42", "STORLEK 42"]:
                        is_correct = True
                    elif target_val == "1500" and any(v in user_val for v in ["1500", "15:00", "15.00", "KL 15:00", "KL. 15:00", "15 00", "15"]):
                        is_correct = True
                    elif target_val == "HÖGER" and any(v in user_val for v in ["HÖGER", "HÖGERHÄNT", "HÖGER-HÄNT"]):
                        is_correct = True
                    elif target_val == "ELICE" and any(v in user_val for v in ["ELICE", "ELISE", "ELICE SVENSSON", "SVENSSON"]):
                        is_correct = True
                    elif user_val == target_val:
                        is_correct = True
                    
                    if is_correct:
                        st.session_state.stage_cleared = True
                        st.session_state.show_hint = False
                        
                        log_entry = f"Etapp {st.session_state.current_stage + 1}: Kod {stage['code']} ({stage['summary']})"
                        if log_entry not in st.session_state.solved_log:
                            st.session_state.solved_log.append(log_entry)
                            
                        play_audio("correct")
                        st.rerun()
                    else:
                        play_audio("wrong")
                        st.error("Felaktig kod. Försök igen eller använd ledtråden.")
            with col2:
                # Hint lock calculation
                lock_sec = st.session_state.hint_lock_minutes * 60
                time_since_stage_start = time.time() - st.session_state.get("stage_start_time", time.time())
                time_remaining = max(0, int(lock_sec - time_since_stage_start))
                
                if time_remaining > 0:
                    mins_rem, secs_rem = divmod(time_remaining, 60)
                    st.button(f"🔒 Ledtråd låst ({mins_rem:02d}:{secs_rem:02d})", disabled=True, use_container_width=True)
                else:
                    if st.button("💡 Visa ledtråd", use_container_width=True):
                        st.session_state.show_hint = True
            
            if st.session_state.show_hint:
                st.markdown(f"<div class='hint-card'>{stage['hint']}</div>", unsafe_allow_html=True)
        
        else:
            st.markdown(f"<div class='success-card'>{stage['success_msg']}</div>", unsafe_allow_html=True)
            
            # Show arrest card with animated Jail Bars if clearing stage 4
            if stage["code"] == "ELICE":
                render_elice_arrest_card()
                
            st.write("")
            if st.button(f"{stage['next_btn']}", type="primary", use_container_width=True):
                st.session_state.current_stage += 1
                st.session_state.stage_cleared = False
                st.session_state.show_hint = False
                st.session_state.stage_start_time = time.time()
                st.rerun()
