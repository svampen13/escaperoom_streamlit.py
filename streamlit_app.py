import streamlit as st
import time

# Page configuration
st.set_page_config(
    page_title="Escape Room Hub",
    page_icon="🕵️‍♂️",
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
    }
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    h1, h2, h3, h4 {
        color: #f8fafc !important;
    }
    .bag-reminder {
        background-color: #1e293b;
        border: 2px solid #38bdf8;
        border-radius: 10px;
        padding: 15px 20px;
        margin-bottom: 20px;
        color: #e2e8f0;
        font-size: 16px;
    }
    .bag-title {
        color: #38bdf8;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 5px;
    }
    .stTextInput > div > div > input {
        font-size: 28px !important;
        text-align: center;
        background-color: #1e293b;
        color: #ffffff;
        border: 2px solid #38bdf8;
        border-radius: 8px;
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
        font-style: italic;
        color: #fde047;
        margin-top: 15px;
    }
    .timer-box {
        background-color: #1e293b;
        border: 2px solid #f59e0b;
        padding: 10px 20px;
        border-radius: 8px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        color: #fbbf24;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Web Audio API Sound Generator Helper
def play_sound(sound_type):
    if not st.session_state.get("sound_enabled", True):
        return
    
    if sound_type == "correct":
        js_code = """
        <script>
        (function() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const now = ctx.currentTime;
                [523.25, 659.25, 783.99].forEach((freq, i) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.value = freq;
                    gain.gain.setValueAtTime(0.2, now + i*0.12);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + i*0.12 + 0.35);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now + i*0.12);
                    osc.stop(now + i*0.12 + 0.35);
                });
            } catch(e) {}
        })();
        </script>
        """
        st.components.v1.html(js_code, height=0)
    elif sound_type == "wrong":
        js_code = """
        <script>
        (function() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const now = ctx.currentTime;
                [220.0, 180.0].forEach((freq, i) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sawtooth';
                    osc.frequency.value = freq;
                    gain.gain.setValueAtTime(0.25, now + i*0.15);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + i*0.15 + 0.3);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now + i*0.15);
                    osc.stop(now + i*0.15 + 0.3);
                });
            } catch(e) {}
        })();
        </script>
        """
        st.components.v1.html(js_code, height=0)
    elif sound_type == "victory":
        js_code = """
        <script>
        (function() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const now = ctx.currentTime;
                const notes = [523.25, 659.25, 783.99, 1046.50];
                notes.forEach((freq, i) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'triangle';
                    osc.frequency.value = freq;
                    gain.gain.setValueAtTime(0.3, now + i*0.18);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + i*0.18 + 0.6);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now + i*0.18);
                    osc.stop(now + i*0.18 + 0.6);
                });
            } catch(e) {}
        })();
        </script>
        """
        st.components.v1.html(js_code, height=0)

# Themes & Stages Definition
THEMES = {
    "sns": {
        "name": "🕵️‍♂️ Vem är den skyldige i SNS?",
        "status": "active",
        "description": "Använd verktygen i utredningsväskan (UV-lampa, mätband, bevishandbok, chiffermall) samt de 5 misstänkta-korten i kuverten för att lösa fallet.",
        "bag_tools": "🧰 **I UTREDNINGSVÄSKAN FINNS:** UV-ficklampa, Måttband, Bevishandbok, Chiffermall och Misstänkta-akten.",
        "stages": [
            {
                "title": "DEL 1 AV 4 — Brottsplatsen",
                "prompt": "Undersök materialet i Kuvert 1. Skriv in koden du får fram:",
                "code": "42",
                "hint": "💡 Ledtråd: Lys med UV-lampan över brottsplatsen i Kuvert 1. Mät spåret och jämför med tabellen i Bevishandboken ur väskan.",
                "success_msg": "KOD GODKÄND! 🎉\n\nFotspåret visar storlek 42.\nAnvänd informationen för att granska de 5 misstänkta-korten i era kuvert och dra era egna slutsatser!\n\n📍 GÅ TILL BOKHYLLAN I KLASSRUMMET OCH HÄMTA KUVERT 2!",
                "next_btn": "JAG HAR HÄMTAT KUVERT 2 — FORTSÄTT →"
            },
            {
                "title": "DEL 2 AV 4 — Vittnesförhören",
                "prompt": "Studera förhören i Kuvert 2. Skriv in koden du får fram:",
                "code": "1500",
                "hint": "💡 Ledtråd: Sortera vittnesmålen kronologiskt. Vilket klockslag saknar helt bekräftade alibin?",
                "success_msg": "KOD GODKÄND! 🎉\n\nTidpunkten för brottet är bekräftad till kl. 15:00.\nJämför tidpunkten med alibin på de misstänkta-korten i ert kuvert!\n\n📍 HÄMTA KUVERT 3 UNDER LÄRARBORDET!",
                "next_btn": "JAG HAR HÄMTAT KUVERT 3 — FORTSÄTT →"
            },
            {
                "title": "DEL 3 AV 4 — Handstilsanalys",
                "prompt": "Granska brevet i Kuvert 3. Skriv in koden du får fram:",
                "code": "HÖGER",
                "hint": "💡 Ledtråd: Studera bläcklinjerna och vinkeln. Jämför med avsnittet om handstilsanalys i Bevishandboken ur väskan.",
                "success_msg": "KOD GODKÄND! 🎉\n\nFörövaren är bekräftad HÖGERHÄNT.\nGranska profilerna på de misstänkta-korten i ert kuvert!\n\n📍 HÄMTA KUVERT 4 I SKÅPET LÄNGST BAK!",
                "next_btn": "JAG HAR HÄMTAT KUVERT 4 — FORTSÄTT →"
            },
            {
                "title": "DEL 4 AV 4 — Slutgiltigt Chiffer",
                "prompt": "Använd materialet i Kuvert 4. Skriv in koden du får fram:",
                "code": "ELICE",
                "hint": "💡 Ledtråd: Passa in hålmallen exakt över hörnmarkeringarna på bokstavsarket. Läs bokstäverna som träder fram.",
                "success_msg": "🏆 FALLET LÖST!\n\nDen skyldige i SNS är identifierad: ELICE!\nUtmärkt utredningsarbete!",
                "next_btn": "AVSLUTA UPPDRAGET"
            }
        ]
    },
    "trafik": {
        "name": "🚗 Trafik & Körkort",
        "status": "active",
        "description": "Använd vägmärkeskartan och trafikreglerna i utredningsväskan för att lösa trafiksäkerhetsscenarier.",
        "bag_tools": "🧰 **I UTREDNINGSVÄSKAN FINNS:** Vägmärkesguide, UV-lampa, Korsningsmatris och Regelbok.",
        "stages": [
            {
                "title": "DEL 1 AV 3 — UV-skylten",
                "prompt": "Granska materialet i Kuvert 1 med UV-lampan ur utredningsväskan för att hitta koden:",
                "code": "1234",
                "hint": "💡 Ledtråd: Titta noga på vägmärket under UV-ljus.",
                "success_msg": "KOD GODKÄND! 🎉\n\n📍 HÄMTA KUVERT 2 VID TRAFIKSKYLTEN I KLASSRUMMET!",
                "next_btn": "JAG HAR HÄMTAT KUVERT 2 — FORTSÄTT →"
            },
            {
                "title": "DEL 2 AV 3 — Trafikreglerna",
                "prompt": "Analysera vägkorsningen i Kuvert 2. Vilken sifferkod bildar trafikreglerna?",
                "code": "5678",
                "hint": "💡 Ledtråd: Tillämpa högerregeln för att få rätt ordning på siffrorna.",
                "success_msg": "KOD GODKÄND! 🎉\n\n📍 HÄMTA KUVERT 3 I SKÅPET LÄNGST BAK!",
                "next_btn": "JAG HAR HÄMTAT KUVERT 3 — FORTSÄTT →"
            },
            {
                "title": "DEL 3 AV 3 — Körkortsprovet",
                "prompt": "Avkoda det sista meddelandet i Kuvert 3:",
                "code": "9999",
                "hint": "💡 Ledtråd: Räkna antalet röda vägmärken på kortet.",
                "success_msg": "🏆 GRATTIS!\n\nNi har klarat alla uppdrag i Trafiktemat!",
                "next_btn": "AVSLUTA UPPDRAGET"
            }
        ]
    },
    "kemi": {
        "name": "🧪 Mysteriet i Kemilabbet",
        "status": "coming_soon",
        "description": "🔒 Ej påbörjat ännu. Kommer i nästa uppdatering! (Experiment, kemiska reaktioner och dolda koder).",
        "bag_tools": "",
        "stages": []
    },
    "historia": {
        "name": "⏳ Tidsmaskinen & Antikens Koder",
        "status": "coming_soon",
        "description": "🔒 Ej påbörjat ännu. Kommer i nästa uppdatering! (Historiska gåtor, hieroglyfer och tidsresor).",
        "bag_tools": "",
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
    st.session_state.start_time = None
if "sound_enabled" not in st.session_state:
    st.session_state.sound_enabled = True
if "play_sound_trigger" not in st.session_state:
    st.session_state.play_sound_trigger = None

# Trigger Sound if set
if st.session_state.play_sound_trigger:
    play_sound(st.session_state.play_sound_trigger)
    st.session_state.play_sound_trigger = None

# Sidebar Controls
st.sidebar.title("⚙️ Meny & Inställningar")

if st.session_state.game_started:
    st.sidebar.subheader("🎮 Aktivt spel")
    theme_info = THEMES[st.session_state.selected_theme]
    st.sidebar.info(f"**Uppdrag:** {theme_info['name']}\n\n**Etapp:** {st.session_state.current_stage + 1} av {len(theme_info['stages'])}")
    
    # Sound toggle during game
    st.session_state.sound_enabled = st.sidebar.checkbox("🔊 Ljudeffekter", value=st.session_state.sound_enabled)
    
    st.sidebar.write("---")
    if st.sidebar.button("🔄 Nollställ / Tillbaka till start", use_container_width=True):
        st.session_state.game_started = False
        st.session_state.current_stage = 0
        st.session_state.stage_cleared = False
        st.session_state.show_hint = False
        st.session_state.start_time = None
        st.rerun()

else:
    st.sidebar.subheader("⚙️ Spelkonfiguration")
    
    # Timer Settings
    timer_option = st.sidebar.radio(
        "⏱️ Timer & Tidsgräns:",
        options=["Fri tid (Ingen timer)", "30 Minuter", "45 Minuter", "60 Minuter"],
        index=0
    )
    if "30" in timer_option:
        st.session_state.timer_minutes = 30
    elif "45" in timer_option:
        st.session_state.timer_minutes = 45
    elif "60" in timer_option:
        st.session_state.timer_minutes = 60
    else:
        st.session_state.timer_minutes = 0
        
    # Sound Effects Toggle
    st.session_state.sound_enabled = st.sidebar.checkbox("🔊 Aktivera Ljudeffekter", value=True)

# MAIN MENU VIEW
if not st.session_state.game_started:
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🕵️‍♂️ ESCAPE ROOM HUB</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #94a3b8;'>Välj ett uppdrag och ställ in inställningarna för att starta</h3>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### 📜 VÄLJ UPPDRAG:")
    
    # Theme selection options
    active_themes = {k: v for k, v in THEMES.items() if v["status"] == "active"}
    coming_soon_themes = {k: v for k, v in THEMES.items() if v["status"] == "coming_soon"}
    
    theme_choice = st.radio(
        "Tillgängliga uppdrag:",
        options=list(active_themes.keys()),
        format_func=lambda x: f"{THEMES[x]['name']}"
    )
    st.session_state.selected_theme = theme_choice
    
    # Display selected active theme details
    sel_theme = THEMES[theme_choice]
    st.info(f"**Om uppdraget:** {sel_theme['description']}\n\n{sel_theme['bag_tools']}")
    
    st.write("")
    st.markdown("#### 🔒 Kommande uppdrag (Ej ännu påbörjade):")
    for cs_key, cs_val in coming_soon_themes.items():
        st.caption(f"• **{cs_val['name']}** — {cs_val['description']}")
        
    st.write("---")
    
    if st.button("🚀 STARTA UPPDRAG", type="primary", use_container_width=True):
        st.session_state.game_started = True
        st.session_state.current_stage = 0
        st.session_state.stage_cleared = False
        st.session_state.show_hint = False
        st.session_state.start_time = time.time()
        st.rerun()

# ACTIVE GAME VIEW
else:
    theme = THEMES[st.session_state.selected_theme]
    stages = theme["stages"]
    
    # Header Banner
    st.markdown(f"<h2 style='text-align: center; color: #38bdf8;'>{theme['name']}</h2>", unsafe_allow_html=True)
    
    # Timer Display
    if st.session_state.timer_minutes > 0 and st.session_state.start_time:
        elapsed = int(time.time() - st.session_state.start_time)
        total_seconds = st.session_state.timer_minutes * 60
        remaining = max(0, total_seconds - elapsed)
        
        mins, secs = divmod(remaining, 60)
        timer_str = f"⏱️ ÅTERSTÅENDE TID: {mins:02d}:{secs:02d}"
        st.markdown(f"<div class='timer-box'>{timer_str}</div>", unsafe_allow_html=True)
    
    # Bag Tools Banner Box
    st.markdown(f"""
        <div class='bag-reminder'>
            <div class='bag-title'>🎒 PÅMINNELSE: ANVÄND UTREDNINGSVÄSKAN & KUVERTEN!</div>
            {theme['bag_tools']}<br>
            <em>Glöm inte att granska de 5 misstänkta-korten och bevisen i kuvertet noggrant tillsammans med gruppen!</em>
        </div>
    """, unsafe_allow_html=True)
    
    # Check if game completed
    if st.session_state.current_stage >= len(stages):
        st.balloons()
        
        st.session_state.play_sound_trigger = "victory"
        
        # Display Arrest Image for Elice if present, or st.image
        elice_found = False
        for fn in os.listdir('.'):
            if fn.lower().startswith('elice') and fn.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                st.image(fn, caption='ARRESTERAD: ELICE - DEN SKYLDIGE I SNS', use_column_width=True)
                elice_found = True
                break
        if not elice_found:
            st.warning('Lägg bilden elice.png i ditt GitHub-arkiv för att visa fotot på Elice här!')

        st.markdown("<h1 style='text-align: center; color: #4ade80;'>🏆 FALLET LÖST!</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #f8fafc;'>Utmärkt utredningsarbete! Samtliga koder har knäckts.</h3>", unsafe_allow_html=True)
        st.write("")
        if st.button("🔄 Tillbaka till huvudmenyn", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.current_stage = 0
            st.session_state.stage_cleared = False
            st.rerun()
            
    else:
        stage = stages[st.session_state.current_stage]
        
        st.caption(f"ETAPP {st.session_state.current_stage + 1} AV {len(stages)}")
        st.markdown(f"### {stage['title']}")
        st.markdown(f"#### {stage['prompt']}")
        
        if not st.session_state.stage_cleared:
            code_input = st.text_input("SKRIV IN KOD HÄR:", key=f"code_in_{st.session_state.current_stage}", placeholder="KOD").strip()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔓 LÅS UPP", type="primary", use_container_width=True):
                    if code_input.lower() == stage["code"].lower():
                        st.session_state.stage_cleared = True
                        st.session_state.show_hint = False
                        st.session_state.play_sound_trigger = "correct"
                        st.rerun()
                    else:
                        st.session_state.play_sound_trigger = "wrong"
                        st.error("❌ Felaktig kod. Försök igen eller använd ledtråden.")
            with col2:
                if st.button("💡 Visa ledtråd", use_container_width=True):
                    st.session_state.show_hint = True
            
            if st.session_state.show_hint:
                st.markdown(f"<div class='hint-card'>{stage['hint']}</div>", unsafe_allow_html=True)
        
        else:
            st.markdown(f"<div class='success-card'>{stage['success_msg']}</div>", unsafe_allow_html=True)
            st.write("")
            if st.button(f"➡️ {stage['next_btn']}", type="primary", use_container_width=True):
                st.session_state.current_stage += 1
                st.session_state.stage_cleared = False
                st.session_state.show_hint = False
                st.rerun()
