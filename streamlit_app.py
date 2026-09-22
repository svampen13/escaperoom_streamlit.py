import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Escape Room Hub",
    page_icon="🕵️‍♂️",
    layout="centered"
)

# Custom Styling for Accessibility & High Contrast
st.markdown("""
    <style>
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
    .stTextInput > div > div > input {
        font-size: 28px !important;
        text-align: center;
        background-color: #1e293b;
        color: #ffffff;
        border: 2px solid #38bdf8;
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
    </style>
""", unsafe_allow_html=True)

# Themes & Stages definition
THEMES = {
    "sns": {
        "name": "Vem är den skyldige i SNS?",
        "description": "Använd verktygen i utredningsväskan för att hitta spår och lösa fallet.",
        "stages": [
            {
                "title": "ETAPP 1: Brottsplatsen",
                "prompt": "Undersök brottsplatskartan i Kuvert 1 med hjälp av verktygen i utredningsväskan. Skriv in koden du får fram:",
                "code": "42",
                "hint": "Ledtråd: Vissa spår på kartan syns inte i vanligt ljus. Titta i utredningsväskan efter ett verktyg som avslöjar dolda tecken, mät spåret och jämför med tabellen i Bevishandboken.",
                "success_msg": "KOD GODKÄND!\n\nSpåret är bekräftat.\n\n📍 GÅ TILL BOKHYLLAN I KLASSRUMMET OCH HÄMTA KUVERT 2!",
                "next_btn": "JAG HAR HÄMTAT KUVERT 2 — FORTSÄTT →"
            },
            {
                "title": "ETAPP 2: Vittnesförhören & Alibin",
                "prompt": "Studera förhören i Kuvert 2 och jämför med Misstänkta-akten i väskan. Skriv in koden för att avgränsa de misstänkta:",
                "code": "4512",
                "hint": "Ledtråd: Sortera vittnesmålen i tidsordning och uteslut alla personer som har ett bekräftat alibi vid brottstillfället.",
                "success_msg": "KOD GODKÄND!\n\nAlibin analyserade och misstänkta avgränsade.\n\n📍 HÄMTA KUVERT 3 UNDER LÄRARBORDET!",
                "next_btn": "JAG HAR HÄMTAT KUVERT 3 — FORTSÄTT →"
            },
            {
                "title": "ETAPP 3: Slutgiltig analys",
                "prompt": "Granska bevisen i Kuvert 3 och jämför med Misstänkta-akten. Skriv koden som avslöjar vem som är den skyldige:",
                "code": "BERTIL",
                "hint": "Ledtråd: Använd chiffermallen ur utredningsväskan och lägg den över bokstavsbladet i Kuvert 3. Vilket namn träder fram?",
                "success_msg": "FALLET LÖST!\n\nDen skyldige i SNS är identifierad. Utmärkt utredningsarbete!",
                "next_btn": "AVSLUTA UPPDRAGET"
            }
        ]
    },
    "trafik": {
        "name": "Trafik & Körkort",
        "description": "Lös vägmärkesgåtor och trafiksäkerhetsscenarier.",
        "stages": [
            {
                "title": "ETAPP 1: UV-skylten",
                "prompt": "Granska materialet i Kuvert 1 med utredningsväskan för att hitta koden:",
                "code": "1234",
                "hint": "Ledtråd: Titta noga på vägmärket under UV-ljus.",
                "success_msg": "KOD GODKÄND!\n\n📍 HÄMTA KUVERT 2 VID TRAFIKSKYLTEN I KLASSRUMMET!",
                "next_btn": "JAG HAR HÄMTAT KUVERT 2 — FORTSÄTT →"
            },
            {
                "title": "ETAPP 2: Trafikreglerna",
                "prompt": "Analysera vägkorsningen i Kuvert 2. Vilken sifferkod bildar trafikreglerna?",
                "code": "5678",
                "hint": "Ledtråd: Tillämpa högerregeln för att få rätt ordning på siffrorna.",
                "success_msg": "KOD GODKÄND!\n\n📍 HÄMTA KUVERT 3 I SKÅPET LÄNGST BAK!",
                "next_btn": "JAG HAR HÄMTAT KUVERT 3 — FORTSÄTT →"
            },
            {
                "title": "ETAPP 3: Körkortsprovet",
                "prompt": "Avkoda det sista meddelandet i Kuvert 3:",
                "code": "9999",
                "hint": "Ledtråd: Räkna antalet röda vägmärken på kortet.",
                "success_msg": "GRATTIS!\n\nNi har klarat alla uppdrag i Trafiktemat!",
                "next_btn": "AVSLUTA UPPDRAGET"
            }
        ]
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

# Sidebar controls
st.sidebar.title("⚙️ Inställningar")
if st.sidebar.button("🔄 Nollställ / Huvudmeny"):
    st.session_state.game_started = False
    st.session_state.current_stage = 0
    st.session_state.stage_cleared = False
    st.session_state.show_hint = False

# Main Menu View
if not st.session_state.game_started:
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🕵️‍♂️ ESCAPE ROOM HUB</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #94a3b8;'>Välj ett uppdrag för att starta sessionen</h3>", unsafe_allow_html=True)
    
    st.write("---")
    
    theme_choice = st.radio(
        "Välj uppdrag:",
        options=list(THEMES.keys()),
        format_func=lambda x: f"{THEMES[x]['name']} — {THEMES[x]['description']}"
    )
    st.session_state.selected_theme = theme_choice
    
    st.write("")
    if st.button("🚀 STARTA UPPDRAG", type="primary", use_container_width=True):
        st.session_state.game_started = True
        st.session_state.current_stage = 0
        st.session_state.stage_cleared = False
        st.session_state.show_hint = False
        st.rerun()

# Active Game View
else:
    theme = THEMES[st.session_state.selected_theme]
    stages = theme["stages"]
    
    # Check if game completed
    if st.session_state.current_stage >= len(stages):
        st.balloons()
        st.markdown("<h1 style='text-align: center; color: #4ade80;'>🏆 FALLET LÖST!</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #f8fafc;'>Utmärkt utredningsarbete! Samtliga koder har knäckts.</h3>", unsafe_allow_html=True)
        if st.button("🔄 Tillbaka till huvudmenyn", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.current_stage = 0
            st.session_state.stage_cleared = False
            st.rerun()
    else:
        stage = stages[st.session_state.current_stage]
        
        st.caption(f"ETAPP {st.session_state.current_stage + 1} AV {len(stages)} — {theme['name']}")
        st.markdown(f"## {stage['title']}")
        st.markdown(f"#### {stage['prompt']}")
        
        if not st.session_state.stage_cleared:
            code_input = st.text_input("Mata in koden här:", key=f"code_in_{st.session_state.current_stage}", placeholder="KOD").strip()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔓 LÅS UPP", type="primary", use_container_width=True):
                    if code_input.lower() == stage["code"].lower():
                        st.session_state.stage_cleared = True
                        st.session_state.show_hint = False
                        st.rerun()
                    else:
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
