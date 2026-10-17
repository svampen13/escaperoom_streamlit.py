import streamlit as st
import time
import base64
import os

# Page configuration - Clean without emojis
st.set_page_config(
    page_title="Escape Room Hub",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Styling for Clean, Dark High-Contrast UI & Jail Bars Overlay Animation
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
    
    /* JAIL OVERLAY CSS ANIMATION */
    .jail-container {
        position: relative;
        display: inline-block;
        width: 100%;
        max-width: 480px;
        margin: 0 auto;
        border-radius: 12px;
        overflow: hidden;
        border: 3px solid #ef4444;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.5);
        background-color: #090d16;
    }
    .jail-img {
        width: 100%;
        height: auto;
        display: block;
    }
    .jail-bars-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: space-around;
        pointer-events: none;
        animation: dropBars 1.2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }
    .bar {
        width: 12px;
        height: 100%;
        background: linear-gradient(90deg, #334155, #94a3b8, #1e293b);
        border-left: 1px solid #475569;
        border-right: 1px solid #0f172a;
        box-shadow: 2px 0 5px rgba(0,0,0,0.7);
    }
    .stamp-badge {
        position: absolute;
        top: 45%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-10deg) scale(0);
        background-color: rgba(220, 38, 38, 0.92);
        color: #ffffff;
        font-weight: 900;
        font-size: 24px;
        letter-spacing: 2px;
        padding: 12px 24px;
        border: 4px solid #ffffff;
        border-radius: 8px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        box-shadow: 0 0 20px rgba(0,0,0,0.8);
        animation: stampSlam 0.5s ease-out 1.2s forwards;
        white-space: nowrap;
    }
    
    @keyframes dropBars {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(0); }
    }
    @keyframes stampSlam {
        0% { transform: translate(-50%, -50%) rotate(-10deg) scale(3); opacity: 0; }
        100% { transform: translate(-50%, -50%) rotate(-10deg) scale(1); opacity: 1; }
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

# Function to render Elice arrest image with animated jail bars
def render_elice_arrest_card():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        img_src = None
        # Look for local file in repository
        for fn in os.listdir('.'):
            if fn.lower().startswith('elice') and fn.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                try:
                    with open(fn, 'rb') as f:
                        b64_data = base64.b64encode(f.read()).decode()
                        ext = fn.split('.')[-1].lower()
                        mime = 'image/png' if ext == 'png' else 'image/jpeg'
                        img_src = f"data:{mime};base64,{b64_data}"
                        break
                except Exception:
                    pass
        
        if img_src:
            jail_html = f"""
            <div style="text-align: center; margin-top: 15px; margin-bottom: 25px;">
                <div class="jail-container">
                    <img src="{img_src}" class="jail-img" alt="Elice Skuggan" />
                    <div class="jail-bars-overlay">
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                    </div>
                    <div class="stamp-badge">ARRESTERAD</div>
                </div>
                <div style="color: #f8fafc; font-weight: 800; font-size: 22px; margin-top: 12px; font-family: sans-serif;">
                    ELICE "SKUGGAN"
                </div>
                <div style="color: #ef4444; font-size: 16px; font-weight: 800; margin-top: 4px; font-family: sans-serif; letter-spacing: 1px;">
                    LÅST INOM LÅS OCH BOM
                </div>
            </div>
            """
            st.markdown(jail_html, unsafe_allow_html=True)
        else:
            st.warning("Lägg bilden elice_animation_preview.png i ditt GitHub-arkiv för att visa fotot på Elice här!")

# Themes & Stages Definition - Clean SNS Focus
THEMES = {
    "sns": {
        "name": "Vem är den skyldige i SNS?",
        "status": "active",
        "description": "Använd verktygen i utredningsväskan (UV-lampa, mätband, bevishandbok, chiffermall) samt de 7 personalkorten i kuverten för att lösa fallet.",
        "bag_tools": "I UTREDNINGSVÄSKAN FINNS: UV-ficklampa, Måttband, Bevishandbok, Chiffermall och Personalkorten.",
        "stages": [
            {
                "title": "ETAPP 1: Brottsplatsen & Skostorlek",
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
        "name": "Kommande uppdrag 1",
        "status": "coming_soon",
        "description": "Ej påbörjat ännu. Kommer i nästa uppdatering!",
        "bag_tools": "",
        "stages": []
    },
    "kommande2": {
        "name": "Kommande uppdrag 2",
        "status": "coming_soon",
        "description": "Ej påbörjat ännu. Kommer i nästa uppdatering!",
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
if "hint_lock_minutes" not in st.session_state:
    st.session_state.hint_lock_minutes = 3

# Sidebar Controls - Clean
st.sidebar.title("Meny & Inställningar")

if st.session_state.game_started:
    st.sidebar.subheader("Aktivt spel")
    theme_info = THEMES[st.session_state.selected_theme]
    st.sidebar.info(f"**Uppdrag:** {theme_info['name']}\n\n**Etapp:** {st.session_state.current_stage + 1} av {len(theme_info['stages'])}")
    
    st.session_state.sound_enabled = st.sidebar.checkbox("Ljudeffekter", value=st.session_state.sound_enabled)
    
    st.sidebar.write("---")
    if st.sidebar.button("Nollställ / Tillbaka till start", use_container_width=True):
        st.session_state.game_started = False
        st.session_state.current_stage = 0
        st.session_state.stage_cleared = False
        st.session_state.show_hint = False
        st.session_state.start_time = None
        st.rerun()

else:
    st.sidebar.subheader("Spelkonfiguration")
    
    # 4 Clean Settings
    timer_option = st.sidebar.radio(
        "Timer & Tidsgräns:",
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
        
    hint_option = st.sidebar.radio(
        "Tidsspärr för ledtrådar:",
        options=["3 Minuter (Standard)", "2 Minuter", "4 Minuter", "Ingen spärr"],
        index=0
    )
    if "2" in hint_option:
        st.session_state.hint_lock_minutes = 2
    elif "4" in hint_option:
        st.session_state.hint_lock_minutes = 4
    elif "Ingen" in hint_option:
        st.session_state.hint_lock_minutes = 0
    else:
        st.session_state.hint_lock_minutes = 3

    st.session_state.sound_enabled = st.sidebar.checkbox("Aktivera Ljudeffekter", value=True)

# Helper function for flexible code matching
def is_code_correct(user_input, stage):
    u = user_input.strip().upper()
    target = stage["code"].upper()
    
    if target == "42":
        return u == "42" or "42" in u
    elif target == "1500":
        clean = u.replace(":", "").replace(".", "").replace(" ", "").replace("KL", "")
        return clean == "1500" or clean == "15" or "1500" in u or "15:00" in u
    elif target == "HÖGER":
        return "HÖGER" in u or "HOGER" in u
    elif target == "ELICE":
        return any(name in u for name in ["ELICE", "ELISE", "SVENSSON", "SVENSON", "SKUGGAN"])
    return u == target

# MAIN MENU VIEW
if not st.session_state.game_started:
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>ESCAPE ROOM HUB</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #94a3b8;'>Välj ett uppdrag och ställ in inställningarna för att starta</h4>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### VÄLJ UPPDRAG:")
    
    active_themes = {k: v for k, v in THEMES.items() if v["status"] == "active"}
    coming_soon_themes = {k: v for k, v in THEMES.items() if v["status"] == "coming_soon"}
    
    theme_choice = st.radio(
        "Tillgängliga uppdrag:",
        options=list(active_themes.keys()),
        format_func=lambda x: f"{THEMES[x]['name']}"
    )
    st.session_state.selected_theme = theme_choice
    
    sel_theme = THEMES[theme_choice]
    st.info(f"**Om uppdraget:** {sel_theme['description']}\n\n{sel_theme['bag_tools']}")
    
    st.write("")
    st.markdown("#### Kommande uppdrag (Ej ännu påbörjade):")
    for cs_key, cs_val in coming_soon_themes.items():
        st.caption(f"• **{cs_val['name']}** — {cs_val['description']}")
        
    st.write("---")
    
    if st.button("STARTA UPPDRAG", type="primary", use_container_width=True):
        st.session_state.game_started = True
        st.session_state.current_stage = 0
        st.session_state.stage_cleared = False
        st.session_state.show_hint = False
        st.session_state.start_time = time.time()
        st.session_state.stage_start_time = time.time()
        st.rerun()

# ACTIVE GAME VIEW
else:
    theme = THEMES[st.session_state.selected_theme]
    stages = theme["stages"]
    
    st.markdown(f"<h2 style='text-align: center; color: #38bdf8;'>{theme['name']}</h2>", unsafe_allow_html=True)
    
    if st.session_state.timer_minutes > 0 and st.session_state.start_time:
        elapsed = int(time.time() - st.session_state.start_time)
        total_seconds = st.session_state.timer_minutes * 60
        remaining = max(0, total_seconds - elapsed)
        
        mins, secs = divmod(remaining, 60)
        timer_str = f"ÅTERSTÅENDE TID: {mins:02d}:{secs:02d}"
        st.markdown(f"<div class='timer-box'>{timer_str}</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='bag-reminder'>
            <div class='bag-title'>PÅMINNELSE: ANVÄND UTREDNINGSVÄSKAN & KUVERTEN!</div>
            {theme['bag_tools']}<br>
            <em>Glöm inte att granska personalkorten och bevisen i kuvertet noggrant tillsammans med gruppen!</em>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.current_stage >= len(stages):
        play_sound("victory")
        st.balloons()
        
        st.markdown("<h1 style='text-align: center; color: #4ade80;'>FALLET LÖST!</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #f8fafc;'>Utmärkt utredningsarbete! Samtliga koder har knäckts.</h3>", unsafe_allow_html=True)
        
        render_elice_arrest_card()
        
