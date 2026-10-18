import streamlit as st
import streamlit.components.v1 as components
import time
import base64
import os

# Page configuration - Clean without emojis in title
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
    
    @keyframes dropBars {
        0% { transform: translateY(-100%); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    @keyframes stampSlam {
        0% { transform: scale(3) rotate(-10deg); opacity: 0; }
        70% { transform: scale(0.9) rotate(-3deg); opacity: 1; }
        100% { transform: scale(1) rotate(-5deg); opacity: 0.95; }
    }
    </style>
""", unsafe_allow_html=True)

# Background music helper function
def play_background_music(file_path="bakgrundsmusik.mp3"):
    if st.session_state.get("enable_audio", True) and os.path.exists(file_path):
        try:
            st.sidebar.audio(file_path, loop=True, autoplay=True)
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

# Function to render Elice arrest image with thin, realistic 3D jail bars overlay
def render_elice_arrest_card():
    img_src = ""
    for fn in ["elice_animation_preview.png", "elice.png", "Elice Escape.png"]:
        if os.path.exists(fn):
            try:
                with open(fn, 'rb') as f:
                    img_src = "data:image/png;base64," + base64.b64encode(f.read()).decode()
                break
            except Exception:
                pass
                
    if not img_src:
        if os.path.exists('.'):
            for fn in os.listdir('.'):
                if fn.lower().startswith('elice') and fn.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    try:
                        with open(fn, 'rb') as f:
                            img_src = "data:image/png;base64," + base64.b64encode(f.read()).decode()
                        break
                    except Exception:
                        pass

    if img_src:
        jail_html = f"""
        <div style="display:flex; justify-content:center; align-items:center; margin: 20px 0;">
            <div style="position:relative; width:100%; max-width:480px; border-radius:12px; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.8); border:3px solid #334155; background:#0f172a;">
                <img src="{img_src}" style="width:100%; display:block; filter: contrast(1.1) brightness(0.95);" alt="Elice">
                
                <!-- Thin 3D Steel Jail Bars Overlay -->
                <div style="position:absolute; top:0; left:0; width:100%; height:100%; display:flex; justify-content:space-around; pointer-events:none; z-index:10; animation: dropBars 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;">
                    <div style="width:10px; background:linear-gradient(90deg, #1e293b 0%, #cbd5e1 40%, #0f172a 100%); box-shadow: 2px 0 6px rgba(0,0,0,0.8);"></div>
                    <div style="width:10px; background:linear-gradient(90deg, #1e293b 0%, #cbd5e1 40%, #0f172a 100%); box-shadow: 2px 0 6px rgba(0,0,0,0.8);"></div>
                    <div style="width:10px; background:linear-gradient(90deg, #1e293b 0%, #cbd5e1 40%, #0f172a 100%); box-shadow: 2px 0 6px rgba(0,0,0,0.8);"></div>
                    <div style="width:10px; background:linear-gradient(90deg, #1e293b 0%, #cbd5e1 40%, #0f172a 100%); box-shadow: 2px 0 6px rgba(0,0,0,0.8);"></div>
                    <div style="width:10px; background:linear-gradient(90deg, #1e293b 0%, #cbd5e1 40%, #0f172a 100%); box-shadow: 2px 0 6px rgba(0,0,0,0.8);"></div>
                    <!-- Horizontal Steel Beam -->
                    <div style="position:absolute; top:35%; left:0; width:100%; height:12px; background:linear-gradient(180deg, #1e293b 0%, #cbd5e1 50%, #0f172a 100%); box-shadow: 0 3px 6px rgba(0,0,0,0.8);"></div>
                    <div style="position:absolute; top:68%; left:0; width:100%; height:12px; background:linear-gradient(180deg, #1e293b 0%, #cbd5e1 50%, #0f172a 100%); box-shadow: 0 3px 6px rgba(0,0,0,0.8);"></div>
                </div>

                <!-- ARRESTERAD Red Stamp Overlay -->
                <div style="position:absolute; top:42%; left:5%; width:90%; padding: 10px 5px; background: rgba(185, 28, 28, 0.9); border: 4px solid #ef4444; border-radius: 8px; color: #ffffff; font-weight: 900; font-size: 22px; text-align: center; text-transform: uppercase; letter-spacing: 2px; text-shadow: 2px 2px 4px rgba(0,0,0,0.9); z-index:20; animation: stampSlam 0.5s ease-out 0.6s both; box-shadow: 0 0 20px rgba(239, 68, 68, 0.6);">
                    ARRESTERAD — ELICE
                </div>
            </div>
        </div>
        """
        components.html(jail_html, height=480)
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
            
