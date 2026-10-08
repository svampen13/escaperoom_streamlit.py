import streamlit as st
import streamlit.components.v1 as components
import time
import base64
import os

# Page configuration
st.set_page_config(
    page_title="Escape Room Hub",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling for clean UI, dark background, high contrast, clean typography
st.markdown("""
    <style>
    /* Hide Streamlit Chrome */
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
    
    /* Heading Level Alignment */
    .section-title {
        color: #38bdf8 !important;
        font-size: 32px !important;
        font-weight: 800 !important;
        margin-bottom: 20px !important;
        line-height: 1.2 !important;
        text-transform: uppercase;
    }
    
    /* VERY LARGE Radio Selection Styling for Välja Uppdrag */
    div[data-testid="stRadio"] > label p {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
        margin-bottom: 15px !important;
    }
    
    div[role="radiogroup"] label {
        background-color: #1e293b !important;
        padding: 22px 28px !important;
        border-radius: 12px !important;
        border: 2px solid #334155 !important;
        margin-bottom: 18px !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.2s ease-in-out;
    }
    
    div[role="radiogroup"] label p, div[role="radiogroup"] label span, div[role="radiogroup"] label div {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        line-height: 1.4 !important;
    }
    
    div[role="radiogroup"] label:hover {
        border-color: #38bdf8 !important;
        background-color: #0f172a !important;
        cursor: pointer;
    }
    
    /* Selectbox Label & Option Text Styling */
    div[data-testid="stSelectbox"] label p, label[data-testid="stWidgetLabel"] p {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        margin-bottom: 8px !important;
    }
    
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        font-size: 22px !important;
        background-color: #1e293b !important;
        border: 2px solid #334155 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
        font-size: 22px !important;
        color: #ffffff !important;
    }

    /* Checkbox Label Text Styling */
    div[data-testid="stCheckbox"] label p, div[data-testid="stCheckbox"] label span {
        font-size: 24px !important;
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

# Audio synthesis via WebAudio API (heartbeat for menu, sound effects for gameplay)
def play_audio(sound_type):
    if st.session_state.get("enable_audio", True):
        if sound_type == "heartbeat":
            js = """<script>
            if (!window.heartbeatInterval) {
                var ctx = new (window.AudioContext || window.webkitAudioContext)();
                function playBeat() {
                    try {
                        var now = ctx.currentTime;
                        // First thump (lub)
                        var osc1 = ctx.createOscillator();
                        var gain1 = ctx.createGain();
                        osc1.connect(gain1); gain1.connect(ctx.destination);
                        osc1.type = 'sine';
                        osc1.frequency.setValueAtTime(60, now);
                        osc1.frequency.exponentialRampToValueAtTime(30, now + 0.12);
                        gain1.gain.setValueAtTime(0.3, now);
                        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
                        osc1.start(now); osc1.stop(now + 0.12);

                        // Second thump (dub)
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
            // Metallic jail door clang
            var oscClang = ctx.createOscillator();
            var gainClang = ctx.createGain();
            oscClang.type = 'square';
            oscClang.frequency.setValueAtTime(140, ctx.currentTime);
            oscClang.frequency.exponentialRampToValueAtTime(30, ctx.currentTime + 0.45);
            gainClang.gain.setValueAtTime(0.4, ctx.currentTime);
            gainClang.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.45);
            oscClang.connect(gainClang); gainClang.connect(ctx.destination);
            oscClang.start(ctx.currentTime); oscClang.stop(ctx.currentTime + 0.45);

            // Victory fanfare
            [523.25, 659.25, 783.99, 1046.50].forEach(function(freq, idx) {
                var osc = ctx.createOscillator();
                var gain = ctx.createGain();
                osc.connect(gain); gain.connect(ctx.destination);
                osc.type = 'sine'; osc.frequency.setValueAtTime(freq, ctx.currentTime + 0.3 + idx*0.18);
                gain.gain.setValueAtTime(0.25, ctx.currentTime + 0.3 + idx*0.18);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3 + idx*0.18 + 0.5);
                osc.start(ctx.currentTime + 0.3 + idx*0.18);
                osc.stop(ctx.currentTime + 0.3 + idx*0.18 + 0.5);
            });
            </script>"""
            components.html(js, height=0, width=0)

# Themes & Stages definition

def get_elice_img_tag():
    img_b64 = None
    for fname in ['elice.png', 'elice.jpg', 'Elice.png', 'Elice.jpg', 'elice.jpeg', 'Elice.jpeg']:
        if os.path.exists(fname):
            try:
                with open(fname, 'rb') as f:
                    img_b64 = base64.b64encode(f.read()).decode()
                    break
            except Exception:
                pass
    if img_b64:
        return f'<img src="data:image/png;base64,{img_b64}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;" />'
    else:
        return """<div style="width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #1e293b; color: #94a3b8;">
            <svg width="90" height="90" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            <span style="margin-top: 10px; font-size: 14px; color: #cbd5e1; font-weight: bold;">ELICE "SKUGGAN"</span>
        </div>"""

def render_jail_animation():
    img_tag = get_elice_img_tag()
    return f"""
    <style>
    @keyframes slideJailBars {{
        0% {{ transform: translateY(-100%); }}
        100% {{ transform: translateY(0); }}
    }}
    @keyframes stampAnim {{
        0% {{ transform: scale(2.5) rotate(-12deg); opacity: 0; }}
        80% {{ transform: scale(0.9) rotate(-12deg); opacity: 1; }}
        100% {{ transform: scale(1) rotate(-12deg); opacity: 1; }}
    }}
    @keyframes redPulse {{
        0% {{ box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); }}
        50% {{ box-shadow: 0 0 35px rgba(239, 68, 68, 0.9); }}
        100% {{ box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); }}
    }}
    .jail-frame {{
        position: relative;
        width: 260px;
        height: 330px;
        margin: 15px auto;
        border: 4px solid #ef4444;
        border-radius: 12px;
        overflow: hidden;
        background-color: #0f172a;
        animation: redPulse 2s infinite ease-in-out;
    }}
    .jail-bars-overlay {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        display: flex;
        justify-content: space-around;
        background: rgba(0, 0, 0, 0.25);
        animation: slideJailBars 1.2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        z-index: 10;
    }}
    .jail-bar {{
        width: 10px;
        height: 100%;
        background: linear-gradient(90deg, #1e293b, #94a3b8, #0f172a);
        box-shadow: 2px 0 6px rgba(0,0,0,0.8);
    }}
    .arrest-stamp {{
        position: absolute;
        top: 42%;
        left: 5%;
        right: 5%;
        text-align: center;
        color: #ef4444;
        border: 4px solid #ef4444;
        font-size: 24px;
        font-weight: 900;
        padding: 6px 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: rgba(15, 23, 42, 0.88);
        animation: stampAnim 0.5s ease-out 1.2s forwards;
        opacity: 0;
        z-index: 20;
        transform-origin: center;
        border-radius: 6px;
    }}
    </style>
    <div style="text-align: center; margin-top: 10px;">
        <div class="jail-frame">
            {img_tag}
            <div class="jail-bars-overlay">
                <div class="jail-bar"></div>
                <div class="jail-bar"></div>
                <div class="jail-bar"></div>
                <div class="jail-bar"></div>
                <div class="jail-bar"></div>
                <div class="jail-bar"></div>
            </div>
            <div class="arrest-stamp">ARRESTERAD</div>
        </div>
        <div style="font-size: 24px; font-weight: 800; color: #38bdf8; margin-top: 10px;">
            ELICE "SKUGGAN"
        </div>
        <div style="font-size: 16px; color: #94a3b8; margin-bottom: 15px;">
            Gärningspersonen är identifierad och omhändertagen!
        </div>
    </div>
    """

THEMES = {
    "sns": {
        "name": "Vem är den skyldige i SNS?",
        "description": "Använd verktygen och materialet i utredningsväskan för att hitta spår och lösa fallet.",
        "disabled": False,
        "stages": [
            {
                "title": "ETAPP 1: Brottsplatsanalys",
                "prompt": "Undersök materialet i Kuvert 1. Skriv in koden du får fram:",
                "code": "42",
                "summary": "Skostorlek 42 bekräftad på brottsplatsen.",
                "hint": "Ledtråd: Använd verktyget ur utredningsväskan på kartan i Kuvert 1 för att avslöja det dolda spåret. Jämför sedan med de 6 personalakterna.",
                "success_msg": "KOD GODKÄND!\n\nSpåret är bekräftat. Granska informationen mot de 6 personalakterna i utredningsväskan.\n\n📍 GÅ TILL BOKHYLLAN I KLASSRUMMET OCH HÄMTA KUVERT 2!",
                "next_btn": "FORTSÄTT TILL ETAPP 2 →"
            },
            {
                "title": "ETAPP 2: Vittnesförhör & Alibin",
                "prompt": "Studera förhören i Kuvert 2. Skriv in koden du får fram:",
                "code": "1500",
                "summary": "Tidpunkt för brottet bekräftad till kl. 15:00.",
                "hint": "Ledtråd: Granska förhörsprotokollen noggrant. Sortera iakttagelserna i tidsordning och identifiera vilket klockslag som saknar bekräftade alibin. Jämför med de 6 personalakterna.",
                "success_msg": "KOD GODKÄND!\n\nTidpunkten för brottet är bekräftad till kl. 15:00. Jämför klockslaget med alibin på de 6 personalakterna.\n\n📍 HÄMTA KUVERT 3 UNDER LÄRARBORDET!",
                "next_btn": "FORTSÄTT TILL ETAPP 3 →"
            },
            {
                "title": "ETAPP 3: Bevisanalys",
                "prompt": "Granska brevet i Kuvert 3. Skriv in koden du får fram:",
                "code": "HÖGER",
                "summary": "Profilbeviset bekräftat: HÖGER.",
                "hint": "Ledtråd: Spegla rapporten i Kuvert 3 i en spegel eller mot fönstret. Läs den tekniska slutsatsen i texten och jämför med profilerna på de 6 personalakterna.",
                "success_msg": "KOD GODKÄND!\n\nProfilbeviset är bekräftat. Jämför med de 6 personalakterna för att avskriva oskyldiga.\n\n📍 HÄMTA KUVERT 4 I SKÅPET LÄNGST BAK!",
                "next_btn": "FORTSÄTT TILL ETAPP 4 →"
            },
            {
                "title": "ETAPP 4: Slutgiltig Identifiering",
                "prompt": "Använd materialet i Kuvert 4 över loggboken. Skriv in koden du får fram:",
                "code": "ELICE",
                "summary": "Den skyldige identifierad: ELICE.",
                "hint": "Ledtråd: Passa in mönstermallen ur utredningsväskan exakt över markeringarna på loggboken i Kuvert 4. Läs av bokstäverna som framträder i fönstren.",
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
            "Tidsgräns:",
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
        st.markdown("<h1 style='text-align: center; color: #4ade80; margin-bottom: 5px;'>🏆 FALLET LÖST!</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #f8fafc; margin-bottom: 20px;'>Utmärkt utredningsarbete! Samtliga koder har knäckts.</h3>", unsafe_allow_html=True)
        
        # Jail Bars Animation & Suspect Card
        st.markdown(render_jail_animation(), unsafe_allow_html=True)
        
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
                    if code_input.lower() == stage["code"].lower():
                        st.session_state.stage_cleared = True
                        st.session_state.show_hint = False
                        
                        # Add to solved log
                        log_entry = f"Etapp {st.session_state.current_stage + 1}: Kod {stage['code']} ({stage['summary']})"
                        if log_entry not in st.session_state.solved_log:
                            st.session_state.solved_log.append(log_entry)
                            
                        play_audio("correct")
                        st.rerun()
                    else:
                        play_audio("wrong")
                        st.error("Felaktig kod. Försök igen eller använd ledtråden.")
            with col2:
                if st.button("Visa ledtråd", use_container_width=True):
                    st.session_state.show_hint = True
            
            if st.session_state.show_hint:
                st.markdown(f"<div class='hint-card'>{stage['hint']}</div>", unsafe_allow_html=True)
        
        else:
            st.markdown(f"<div class='success-card'>{stage['success_msg']}</div>", unsafe_allow_html=True)
            st.write("")
            if st.button(f"{stage['next_btn']}", type="primary", use_container_width=True):
                st.session_state.current_stage += 1
                st.session_state.stage_cleared = False
                st.session_state.show_hint = False
                st.rerun()
                
        # Display persistent evidence log at bottom
        if st.session_state.solved_log:
            st.markdown("<div class='log-card'>", unsafe_allow_html=True)
            st.markdown("<div class='log-title'>BEVISSAMLING / LÖSTA ETAPPER:</div>", unsafe_allow_html=True)
            for item in st.session_state.solved_log:
                st.markdown(f"<div class='log-item'>✓ {item}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
