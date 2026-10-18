import streamlit as st
import time
import base64
import os

st.set_page_config(
    page_title="Escape Room Hub",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
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
                        osc1.type = "sine";
                        osc1.frequency.setValueAtTime(60, now);
                        osc1.frequency.exponentialRampToValueAtTime(30, now + 0.12);
                        gain1.gain.setValueAtTime(0.3, now);
                        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
                        osc1.start(now); osc1.stop(now + 0.12);

                        var osc2 = ctx.createOscillator();
                        var gain2 = ctx.createGain();
                        osc2.connect(gain2); gain2.connect(ctx.destination);
                        osc2.type = "sine";
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
            st.components.v1.html(js, height=0, width=0)
        elif sound_type == "stop_heartbeat":
            js = """<script>
            if (window.heartbeatInterval) {
                clearInterval(window.heartbeatInterval);
                window.heartbeatInterval = null;
            }
            </script>"""
            st.components.v1.html(js, height=0, width=0)
        elif sound_type == "correct":
            js = """<script>
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            var osc = ctx.createOscillator();
            var gain = ctx.createGain();
            osc.connect(gain); gain.connect(ctx.destination);
            osc.type = "sine"; osc.frequency.setValueAtTime(523.25, ctx.currentTime);
            osc.frequency.setValueAtTime(659.25, ctx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.25, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
            osc.start(); osc.stop(ctx.currentTime + 0.4);
            </script>"""
            st.components.v1.html(js, height=0, width=0)
        elif sound_type == "wrong":
            js = """<script>
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            var osc = ctx.createOscillator();
            var gain = ctx.createGain();
            osc.connect(gain); gain.connect(ctx.destination);
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(180, ctx.currentTime);
            osc.frequency.setValueAtTime(130, ctx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.2, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);
            osc.start(); osc.stop(ctx.currentTime + 0.35);
            </script>"""
            st.components.v1.html(js, height=0, width=0)
        elif sound_type == "victory":
            js = """<script>
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            [523.25, 659.25, 783.99, 1046.50].forEach(function(freq, idx) {
                var osc = ctx.createOscillator();
                var gain = ctx.createGain();
                osc.connect(gain); gain.connect(ctx.destination);
                osc.type = "sine"; osc.frequency.setValueAtTime(freq, ctx.currentTime + idx*0.2);
                gain.gain.setValueAtTime(0.25, ctx.currentTime + idx*0.2);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx*0.2 + 0.5);
                osc.start(ctx.currentTime + idx*0.2);
                osc.stop(ctx.currentTime + idx*0.2 + 0.5);
            });
            </script>"""
            st.components.v1.html(js, height=0, width=0)

ELICE_IMAGE_B64 = "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"

def render_elice_arrest_card():
    img_src = ""
    for fn in ["elice_animation_preview.png", "elice.png", "Elice Escape.png", "elice escape.png"]:
        if os.path.exists(fn):
            try:
                with open(fn, "rb") as file_in:
                    data = file_in.read()
                    ext = "png" if fn.endswith(".png") else "jpeg"
                    img_src = f"data:image/{ext};base64,{base64.b64encode(data).decode()}"
                break
            except Exception:
                pass
    if not img_src and ELICE_IMAGE_B64:
        img_src = f"data:image/jpeg;base64,{ELICE_IMAGE_B64}"
    if img_src:
        jail_html = f"""
        <style>
        @keyframes dropBars {{
            0% {{ transform: translateY(-100%); opacity: 0; }}
            100% {{ transform: translateY(0); opacity: 1; }}
        }}
        @keyframes stampSlam {{
            0% {{ transform: translate(-50%, 0) scale(2); opacity: 0; }}
            80% {{ transform: translate(-50%, 0) scale(0.9); opacity: 1; }}
            100% {{ transform: translate(-50%, 0) scale(1); opacity: 1; }}
        }}
        </style>
        <div style="display:flex; justify-content:center; align-items:center; margin:20px 0;">
            <div style="position:relative; width:100%; max-width:420px; border-radius:12px; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.8); border:3px solid #334155; background:#0f172a;">
                <img src="{img_src}" style="width:100%; display:block; filter: contrast(1.05) brightness(0.95);" alt="Elice">
                <div style="position:absolute; top:20%; left:0; width:100%; height:8px; background:linear-gradient(180deg, #475569 0%, #cbd5e1 50%, #1e293b 100%); box-shadow:0 2px 5px rgba(0,0,0,0.7); z-index:9;"></div>
                <div style="position:absolute; top:78%; left:0; width:100%; height:8px; background:linear-gradient(180deg, #475569 0%, #cbd5e1 50%, #1e293b 100%); box-shadow:0 2px 5px rgba(0,0,0,0.7); z-index:9;"></div>
                <div style="position:absolute; top:0; left:0; width:100%; height:100%; display:flex; justify-content:space-evenly; align-items:stretch; pointer-events:none; z-index:10; animation: dropBars 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;">
                    <div style="width:10px; height:100%; background:linear-gradient(90deg, #334155 0%, #cbd5e1 40%, #ffffff 50%, #94a3b8 70%, #1e293b 100%); box-shadow: 2px 0 6px rgba(0,0,0,0.7); border-radius:3px;"></div>
                    <div style="width:10px; height:100%; background:linear-gradient(90deg, #334155 0%, #cbd5e1 40%, #ffffff 50%, #94a3b8 70%, #1e293b 100%); box-shadow: 2px 0 6px rgba(0,0,0,0.7); border-radius:3px;"></div>
                    <div style="width:10px; height:100%; background:linear-gradient(90deg, #334155 0%, #cbd5e1 40%, #ffffff 50%, #94a3b8 70%, #1e293b 100%); box-shadow: 2px 0 6px rgba(0,0,0,0.7); border-radius:3px;"></div>
                    <div style="width:10px; height:100%; background:linear-gradient(90deg, #334155 0%, #cbd5e1 40%, #ffffff 50%, #94a3b8 70%, #1e293b 100%); box-shadow: 2px 0 6px rgba(0,0,0,0.7); border-radius:3px;"></div>
                    <div style="width:10px; height:100%; background:linear-gradient(90deg, #334155 0%, #cbd5e1 40%, #ffffff 50%, #94a3b8 70%, #1e293b 100%); box-shadow: 2px 0 6px rgba(0,0,0,0.7); border-radius:3px;"></div>
                </div>
                <div style="position:absolute; bottom:15px; left:50%; transform:translateX(-50%); background:rgba(185, 28, 28, 0.95); color:#ffffff; padding:8px 16px; border:2px solid #f87171; border-radius:6px; font-weight:900; font-size:15px; text-transform:uppercase; letter-spacing:1.5px; text-align:center; box-shadow:0 4px 15px rgba(0,0,0,0.8); z-index:20; white-space:nowrap; animation: stampSlam 0.5s ease-out 0.6s both;">
                    ARRESTERAD — LÅST INOM LÅS OCH BOM
                </div>
            </div>
        </div>
        """
        st.markdown(jail_html, unsafe_allow_html=True)
    else:
        st.warning("Kunde inte läsa in bilden på Elice.")

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

def is_code_correct(user_input, target_code):
    u = user_input.strip().upper()
    t = target_code.strip().upper()
    if u == t:
        return True
    if t == "1500" and u in ["1500", "15:00", "15.00", "KL 15:00", "KL. 15:00", "15 00", "15"]:
        return True
    if t == "42" and u in ["42", "SKOSTORLEK 42", "STORLEK 42"]:
        return True
    if t == "HÖGER" and u in ["HÖGER", "HÖGERHÄNT", "HÖGER-HÄNT"]:
        return True
    if t == "ELICE" and u in ["ELICE", "ELISE", "ELICE SVENSSON", "ELICE SVENSON", "SVENSSON"]:
        return True
    return False

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

st.sidebar.title("Inställningar")
if st.sidebar.button("Nollställ / Huvudmeny"):
    st.session_state.game_started = False
    st.session_state.current_stage = 0
    st.session_state.stage_cleared = False
    st.session_state.show_hint = False
    st.session_state.solved_log = []
    st.rerun()

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
else:
    play_audio("stop_heartbeat")
    theme = THEMES[st.session_state.selected_theme]
    stages = theme["stages"]
    if st.session_state.timer_minutes > 0:
        elapsed = time.time() - st.session_state.start_time
        total_sec = st.session_state.timer_minutes * 60
        remaining = max(0, int(total_sec - elapsed))
        mins, secs = divmod(remaining, 60)
        timer_color = "#38bdf8" if remaining > 300 else "#ef4444"
        st.markdown(f"<div class='timer-card' style='color:{timer_color};'>ÅTERSTÅENDE TID: {mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)
    if st.session_state.current_stage >= len(stages):
        play_audio("victory")
        st.balloons()
        st.markdown("<h1 style='text-align: center; color: #4ade80;'>FALLET LÖST!</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #f8fafc;'>Utmärkt utredningsarbete! Den skyldige har blivit identifierad och gripen.</h3>", unsafe_allow_html=True)
        render_elice_arrest_card()
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
                    if is_code_correct(code_input, stage["code"]):
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
            if stage["code"] == "ELICE":
                render_elice_arrest_card()
            st.write("")
            if st.button(f"{stage['next_btn']}", type="primary", use_container_width=True):
                st.session_state.current_stage += 1
                st.session_state.stage_cleared = False
                st.session_state.show_hint = False
                st.session_state.stage_start_time = time.time()
                st.rerun()
