import streamlit as st
import streamlit.components.v1 as components
import time
import base64
import os

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
    
    /* Prison Bars Animation Styles */
    @keyframes slideJailBars {
        0% {
            transform: translateY(-100%);
            opacity: 0;
        }
        60% {
            transform: translateY(0%);
            opacity: 1;
        }
        75% {
            transform: translateY(-12px);
        }
        100% {
            transform: translateY(0%);
            opacity: 1;
        }
    }

    @keyframes pulseSiren {
        0% { box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); border-color: #ef4444; }
        50% { box-shadow: 0 0 35px rgba(239, 68, 68, 0.95); border-color: #f87171; }
        100% { box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); border-color: #ef4444; }
    }

    @keyframes stampArrested {
        0% { transform: scale(3) rotate(-15deg); opacity: 0; }
        80% { transform: scale(0.9) rotate(-15deg); opacity: 1; }
        100% { transform: scale(1) rotate(-15deg); opacity: 1; }
    }

    .jail-card-container {
        position: relative;
        width: 320px;
        height: 420px;
        margin: 25px auto;
        background: #1e293b;
        border: 4px solid #ef4444;
        border-radius: 14px;
        overflow: hidden;
        animation: pulseSiren 2s infinite;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }

    .jail-mugshot {
        width: 100%;
        height: 280px;
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-bottom: 2px solid #334155;
        position: relative;
    }

    .jail-silhouette {
        font-size: 110px;
        line-height: 1;
        margin-top: 10px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5));
    }

    .jail-bars-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: space-evenly;
        z-index: 10;
        pointer-events: none;
        animation: slideJailBars 1.2s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        animation-delay: 0.4s;
        transform: translateY(-100%);
    }

    .jail-bar {
        width: 14px;
        height: 100%;
        background: linear-gradient(90deg, #475569 0%, #cbd5e1 40%, #94a3b8 70%, #334155 100%);
        box-shadow: 3px 0 6px rgba(0,0,0,0.6);
        border-radius: 3px;
    }

    .jail-bar-cross {
        position: absolute;
        width: 100%;
        height: 12px;
        background: linear-gradient(180deg, #475569 0%, #cbd5e1 50%, #334155 100%);
        z-index: 11;
        box-shadow: 0 2px 5px rgba(0,0,0,0.5);
    }

    .jail-bar-cross.top { top: 22%; }
    .jail-bar-cross.bottom { bottom: 22%; }

    .arrested-stamp {
        position: absolute;
        top: 35%;
        left: 5%;
        right: 5%;
        border: 6px solid #ef4444;
        color: #ef4444;
        font-size: 30px;
        font-weight: 900;
        text-transform: uppercase;
        padding: 8px 10px;
        border-radius: 8px;
        letter-spacing: 2px;
        background: rgba(15, 23, 42, 0.90);
        z-index: 20;
        animation: stampArrested 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        animation-delay: 1.5s;
        opacity: 0;
        transform: rotate(-15deg);
        box-shadow: 0 4px 15px rgba(0,0,0,0.7);
    }

    .suspect-details {
        padding: 14px;
        background-color: #1e293b;
    }

    .suspect-name {
        font-size: 26px;
        font-weight: 800;
        color: #f8fafc;
        margin: 0;
        letter-spacing: 1px;
    }

    .suspect-title {
        font-size: 15px;
        color: #ef4444;
        font-weight: bold;
        text-transform: uppercase;
        margin-top: 4px;
        letter-spacing: 1.5px;
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
        components.html(js_code, height=0)
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
        components.html(js_code, height=0)
    elif sound_type == "victory":
        js_code = """
        <script>
        (function() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const now = ctx.currentTime;
                
                // Fanfare melody
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

                // Metallic prison door slam impact sound at 0.5s
                setTimeout(() => {
                    try {
                        const slamCtx = new (window.AudioContext || window.webkitAudioContext)();
                        const slamTime = slamCtx.currentTime;
                        
                        // Low thud
                        const osc = slamCtx.createOscillator();
                        const gain = slamCtx.createGain();
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(120, slamTime);
                        osc.frequency.exponentialRampToValueAtTime(30, slamTime + 0.4);
                        gain.gain.setValueAtTime(0.5, slamTime);
                        gain.gain.exponentialRampToValueAtTime(0.001, slamTime + 0.4);
                        osc.connect(gain);
                        gain.connect(slamCtx.destination);
                        osc.start(slamTime);
                        osc.stop(slamTime + 0.4);

                        // Metallic clang noise
                        const noiseBuffer = slamCtx.createBuffer(1, slamCtx.sampleRate * 0.3, slamCtx.sampleRate);
                        const output = noiseBuffer.getChannelData(0);
                        for (let i = 0; i < noiseBuffer.length; i++) {
                            output[i] = Math.random() * 2 - 1;
                        }
                        const whiteNoise = slamCtx.createBufferSource();
                        whiteNoise.buffer = noiseBuffer;

                        const filter = slamCtx.createBiquadFilter();
                        filter.type = 'bandpass';
                        filter.frequency.value = 1000;

                        const noiseGain = slamCtx.createGain();
                        noiseGain.gain.setValueAtTime(0.4, slamTime);
                        noiseGain.gain.exponentialRampToValueAtTime(0.01, slamTime + 0.3);

                        whiteNoise.connect(filter);
                        filter.connect(noiseGain);
                        noiseGain.connect(slamCtx.destination);
                        whiteNoise.start(slamTime);
                    } catch(e) {}
                }, 500);

            } catch(e) {}
        })();
        </script>
        """
        components.html(js_code, height=0)

# Themes & Stages Definition
THEMES = {
    "sns": {
        "name": "🕵️‍♂️ Vem är den skyldige i SNS?",
        "status": "active",
        "description": "Använd verktygen i utredningsväskan (UV-lampa, mätband, bevishandbok, chiffermall) samt de 6 misstänkta-korten för att lösa fallet.",
        "bag_tools": "🧰 **I UTREDNINGSVÄSKAN FINNS:** UV-ficklampa, Måttband, Bevishandbok, Hålmall (Dekoderkort) och Misstänkta-akten.",
        "culprit_name": "ELICE \"SKUGGAN\"",
        "culprit_title": "ARRESTERAD — PEKADES UT AV HÅLMALLEN",
        "stages": [
            {
                "title": "DEL 1 AV 4 — Brottsplatsen & Skostorlek",
                "prompt": "Undersök brottsplatskartan i Kuvert 1 med hjälp av UV-lampan och mätbandet ur utredningsväskan. Skriv in koden för fotspårets storlek:",
                "code": "42",
                "hint": "💡 Ledtråd: Lys med UV-lampan över brottsplatsen i Kuvert 1. Mät spåret och jämför med tabellen i Bevishandboken ur väskan.",
                "success_msg": "KOD GODKÄND! 🎉\n\nFotspåret visar storlek 42.\nAnvänd informationen för att granska de 6 misstänkta-korten i er utredningsväska och avskriv felaktiga spår!\n\n📍 GÅ TILL BOKHYLLAN I KLASSRUMMET OCH HÄMTA KUVERT 2!",
                "next_btn": "JAG HAR HÄMTAT KUVERT 2 — FORTSÄTT →"
            },
            {
                "title": "DEL 2 AV 4 — Vittnesförhör & Alibi",
                "prompt": "Studera förhören i Kuvert 2 och jämför med tiderna. Skriv in koden för klockslaget då brottet skedde (4 siffror):",
                "code": "1500",
                "hint": "💡 Ledtråd: Sortera vittnesmålen kronologiskt. Vilket klockslag saknar helt bekräftade alibin?",
                "success_msg": "KOD GODKÄND! 🎉\n\nTidpunkten för brottet är bekräftad till kl. 15:00.\nJämför tidpunkten med eftermiddagsloggen på personalkorten i utredningsväskan!\n\n📍 HÄMTA KUVERT 3 UNDER LÄRARBORDET!",
                "next_btn": "JAG HAR HÄMTAT KUVERT 3 — FORTSÄTT →"
            },
            {
                "title": "DEL 3 AV 4 — Handstil & Dominans",
                "prompt": "Granska det handskrivna brevet i Kuvert 3. Skriv om förövaren är HÖGER eller VÄNSTERhänt:",
                "code": "HÖGER",
                "hint": "💡 Ledtråd: Studera bläcklinjerna och vinkeln. Jämför med avsnittet om handstilsanalys i Bevishandboken ur väskan.",
                "success_msg": "KOD GODKÄND! 🎉\n\nFörövaren är bekräftad HÖGERHÄNT.\nGranska fotona på de misstänkta-korten för att avgöra handdominans!\n\n📍 HÄMTA KUVERT 4 I SKÅPET LÄNGST BAK!",
                "next_btn": "JAG HAR HÄMTAT KUVERT 4 — FORTSÄTT →"
            },
            {
                "title": "DEL 4 AV 4 — Slutgiltigt Chiffer",
                "prompt": "Ta fram Hålmallen ur utredningsväskan och lägg den över Loggboken i Kuvert 4. Skriv in namnet på den skyldige:",
                "code": "ELICE",
                "hint": "💡 Ledtråd: Passa in Hålmallens HÖGER-hörn exakt över hörnmarkeringen på Loggboken. Läs bokstäverna som träder fram i fönstren.",
                "success_msg": "🏆 FALLET LÖST!\n\nDen skyldige i SNS är identifierad: ELICE!\nUtmärkt utredningsarbete!",
                "next_btn": "AVSLUTA UPPDRAGET & SE GRIPANDET"
            }
        ]
    },
    "trafik": {
        "name": "🚗 Trafik & Körkort",
        "status": "active",
        "description": "Använd vägmärkeskartan och trafikreglerna i utredningsväskan för att lösa trafiksäkerhetsscenarier.",
        "bag_tools": "🧰 **I UTREDNINGSVÄSKAN FINNS:** Vägmärkesguide, UV-lampa, Korsningsmatris och Regelbok.",
        "culprit_name": "TRAFIKSYNDAREN",
        "culprit_title": "KÖRKORTET INDRAGET",
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
        "culprit_name": "",
        "culprit_title": "",
        "stages": []
    },
    "historia": {
        "name": "⏳ Tidsmaskinen & Antikens Koder",
        "status": "coming_soon",
        "description": "🔒 Ej påbörjat ännu. Kommer i nästa uppdatering! (Historiska gåtor, hieroglyfer och tidsresor).",
        "bag_tools": "",
        "culprit_name": "",
        "culprit_title": "",
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
    st.sidebar.info(f"**Uppdrag:** {theme_info['name']}\n\n**Etapp:** {min(st.session_state.current_stage + 1, len(theme_info['stages']))} av {len(theme_info['stages'])}")
    
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
    
    # Check if game completed
    if st.session_state.current_stage >= len(stages):
        st.balloons()
        st.session_state.play_sound_trigger = "victory"
        
        st.markdown("<h1 style='text-align: center; color: #4ade80;'>🏆 FALLET LÖST!</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #f8fafc;'>Utmärkt utredningsarbete! Den skyldige är fasttagen!</h3>", unsafe_allow_html=True)
        
        # Animated Jail Card Component
        culprit = theme.get("culprit_name", "ELICE \"SKUGGAN\"")
        culprit_title = theme.get("culprit_title", "ARRESTERAD — PEKADES UT AV HÅLMALLEN")
        
        jail_html = f"""
        <div class="jail-card-container">
            <div class="jail-mugshot">
                <div class="jail-silhouette">👩‍🔬</div>
                <div class="jail-bars-overlay">
                    <div class="jail-bar-cross top"></div>
                    <div class="jail-bar"></div>
                    <div class="jail-bar"></div>
                    <div class="jail-bar"></div>
                    <div class="jail-bar"></div>
                    <div class="jail-bar"></div>
                    <div class="jail-bar-cross bottom"></div>
                </div>
                <div class="arrested-stamp">LÅS OCH BOM</div>
            </div>
            <div class="suspect-details">
                <div class="suspect-name">{culprit}</div>
                <div class="suspect-title">{culprit_title}</div>
            </div>
        </div>
        """
        st.markdown(jail_html, unsafe_allow_html=True)
        
        st.write("")
        if st.button("🔄 Tillbaka till huvudmenyn", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.current_stage = 0
            st.session_state.stage_cleared = False
            st.rerun()
            
    else:
        stage = stages[st.session_state.current_stage]
        
        # Bag Tools Banner Box
        st.markdown(f"""
            <div class='bag-reminder'>
                <div class='bag-title'>🎒 PÅMINNELSE: ANVÄND UTREDNINGSVÄSKAN & KUVERTEN!</div>
                {theme['bag_tools']}<br>
                <em>Glöm inte att granska de 6 misstänkta-korten och bevisen i kuvertet noggrant tillsammans med gruppen!</em>
            </div>
        """, unsafe_allow_html=True)
        
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
