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

# Themes & Stages definition
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
                "hint": "Ledtråd: Vissa spår på kartan syns inte i vanligt ljus. Titta i utredningsväskan efter ett verktyg som avslöjar dolda tecken, mät spåret och jämför med tabellen i Bevishandboken.",
                "success_msg": "KOD GODKÄND!\n\nSpåret är bekräftat. Använd informationen för att granska de 6 personalakterna i er utredningsväska.\n\n📍 GÅ TILL BOKHYLLAN I KLASSRUMMET OCH HÄMTA KUVERT 2!",
                "next_btn": "FORTSÄTT TILL ETAPP 2 →"
            },
            {
                "title": "ETAPP 2: Vittnesförhören & Alibin",
                "prompt": "Studera förhören i Kuvert 2 och jämför med tiderna. Skriv in koden för klockslaget då brottet ägde rum (4 siffror):",
                "code": "1500",
                "summary": "Tidpunkt för brottet bekräftad till kl. 15:00.",
                "hint": "Ledtråd: Sortera vittnesmålen i tidsordning och identifiera vilket klockslag som har en lucka utan bekräftade observationer.",
                "success_msg": "KOD GODKÄND!\n\nTidpunkten för brottet är bekräftad till kl. 15:00. Jämför klockslaget med alibin på korten i kuvertet.\n\n📍 HÄMTA KUVERT 3 UNDER LÄRARBORDET!",
                "next_btn": "FORTSÄTT TILL ETAPP 3 →"
            },
            {
                "title": "ETAPP 3: Bevisanalys",
                "prompt": "Granska brevet i Kuvert 3. Skriv in koden du får fram:",
                "code": "HÖGER",
                "summary": "Förövaren bekräftad HÖGERHÄNT.",
                "hint": "Ledtråd: Granska bläckdraget och lutningen i handstilen. Jämför med guiden i Bevishandboken.",
                "success_msg": "KOD GODKÄND!\n\nFörövaren är bekräftad HÖGERHÄNT. Granska profilerna på era misstänkta-kort i kuvertet.\n\n📍 HÄMTA KUVERT 4 I SKÅPET LÄNGST BAK!",
                "next_btn": "FORTSÄTT TILL ETAPP 4 →"
            },
            {
                "title": "ETAPP 4: Slutgiltigt Chiffer",
                "prompt": "Använd chiffermallen ur Kuvert 4 över bokstavsarket. Skriv in namnet på den skyldige:",
                "code": "ELICE",
                "summary": "Den skyldige identifierad: ELICE.",
                "hint": "Ledtråd: Lägg hålmallen exakt över hörnmarkeringarna på bokstavsarket. Läs bokstäverna från vänster till höger.",
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
        st.markdown("<h1 style='text-align: center; color: #4ade80;'>FALLET LÖST!</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #f8fafc;'>Utmärkt utredningsarbete! Samtliga koder har knäckts.</h3>", unsafe_allow_html=True)
        
        # Check for Elice image file
        elice_b64 = None
        for img_name in ['elice.png', 'elice.jpg', 'elice.jpeg', 'Elice.png', 'Elice.jpg', 'elice_skuggan.png']:
            if os.path.exists(img_name):
                try:
                    with open(img_name, 'rb') as f:
                        elice_b64 = base64.b64encode(f.read()).decode()
                    break
                except Exception:
                    pass
        
        if elice_b64:
            img_content = f'<img src="data:image/png;base64,{elice_b64}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;">'
        else:
            img_content = """<div style="width:100%; height:100%; background: #1e293b; display:flex; flex-direction:column; align-items:center; justify-content:center; border-radius:8px;">
                <div style="font-size: 70px;">👤</div>
                <div style="color: #94a3b8; font-weight: bold; font-size: 18px; margin-top: 10px;">ELICE "SKUGGAN"</div>
                <div style="color: #ef4444; font-size: 13px; margin-top: 6px; padding: 0 12px; text-align: center;">Ladda upp <b>elice.png</b> till din GitHub-mapp så visas hennes bild här!</div>
            </div>"""

        jail_animation_html = f"""
        <style>
        @keyframes dropBars {{
            0% {{ transform: translateY(-100%); }}
            100% {{ transform: translateY(0); }}
        }}
        @keyframes stampIn {{
            0% {{ transform: scale(3) rotate(-15deg); opacity: 0; }}
            80% {{ transform: scale(0.9) rotate(-15deg); opacity: 1; }}
            100% {{ transform: scale(1) rotate(-15deg); opacity: 1; }}
        }}
        .jail-card {{
            background-color: #1e293b;
            border: 3px solid #ef4444;
            box-shadow: 0 0 30px rgba(239, 68, 68, 0.4);
            border-radius: 12px;
            padding: 20px;
            max-width: 380px;
            margin: 25px auto;
            text-align: center;
        }}
        .jail-frame {{
            position: relative;
            width: 280px;
            height: 350px;
            margin: 0 auto;
            border-radius: 8px;
            overflow: hidden;
            border: 4px solid #334155;
            background-color: #0f172a;
        }}
        .jail-bars {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                90deg,
                #0f172a 0px,
                #0f172a 14px,
                #475569 14px,
                #94a3b8 18px,
                #1e293b 22px,
                transparent 22px,
                transparent 48px
            );
            box-shadow: inset 0 0 15px rgba(0,0,0,0.8);
            animation: dropBars 1.2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
            z-index: 2;
        }}
        .jail-stamp {{
            position: absolute;
            top: 40%;
            left: 5%;
            width: 90%;
            border: 4px solid #ef4444;
            color: #ef4444;
            font-size: 26px;
            font-weight: 900;
            text-transform: uppercase;
            padding: 8px 0;
            letter-spacing: 2px;
            background: rgba(15, 23, 42, 0.9);
            transform: rotate(-15deg);
            animation: stampIn 0.6s ease-out 0.9s forwards;
            opacity: 0;
            z-index: 3;
            text-shadow: 0 0 10px rgba(239, 68, 68, 0.7);
        }}
        </style>
        <div class="jail-card">
            <div style="font-size: 22px; font-weight: 800; color: #f8fafc; margin-bottom: 12px; letter-spacing: 1px;">🔒 ARRESTERAD: ELICE "SKUGGAN"</div>
            <div class="jail-frame">
                {img_content}
                <div class="jail-bars"></div>
                <div class="jail-stamp">LÅS OCH BOM</div>
            </div>
            <div style="color: #cbd5e1; font-size: 15px; margin-top: 14px; font-weight: 600;">PEKADES UT AV HÅLMALLEN I LOGGBOKEN</div>
        </div>
        """
        st.markdown(jail_animation_html, unsafe_allow_html=True)
        
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
