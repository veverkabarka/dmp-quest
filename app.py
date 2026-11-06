import streamlit as st
import json
import base64
import requests
import re

st.set_page_config(page_title="DMP Quest: OP JAK", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #f43f5e; color: white; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background-color: #e11d48; }
    .npc-box-datlik { background-color: rgba(56, 189, 248, 0.1); border-left: 5px solid #38bdf8; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .npc-box-matla { background-color: rgba(244, 63, 94, 0.1); border-left: 5px solid #f43f5e; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

def vygenerovat_oficialni_html_dmp(data_z_json_hry):
    sber = data_z_json_hry["kapitoly"].get("sber_a_generovani", {}).get("text_pro_sabonu", "")
    metadata = data_z_json_hry["kapitoly"].get("metadata_a_dokumentace", {}).get("text_pro_sabonu", "")
    uloziste = data_z_json_hry["kapitoly"].get("uloziste_a_bezpecnost", {}).get("text_pro_sabonu", "")

    html_template = f"""
    <!DOCTYPE html>
    <html lang="cs">
    <head>
        <meta charset="UTF-8">
        <title>DMP - {data_z_json_hry.get('nazev_projektu', 'Projekt OP JAK')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333333; line-height: 1.6; padding: 40px; max-width: 800px; margin: 0 auto; }}
            .header-logos {{ display: flex; justify-content: center; align-items: center; border-bottom: 2px solid #005691; padding-bottom: 20px; margin-bottom: 30px; }}
            .logo-opjak {{ height: 65px; width: auto; }}
            h1 {{ color: #005691; font-size: 24px; text-transform: uppercase; margin-top: 0; }}
            h2 {{ color: #005691; font-size: 18px; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 25px; }}
            .meta-info {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 30px; font-size: 14px; }}
            .content-section {{ margin-bottom: 20px; text-align: justify; }}
        </style>
    </head>
    <body>
        <div class="header-logos">
            <img class="logo-opjak" src="loga_spojena.png" alt="Publicita OP JAK">
        </div>
        <h1>Plán správy dat (Data Management Plan)</h1>
        <div class="meta-info">
            <strong>Název projektu:</strong> {data_z_json_hry.get('nazev_projektu', 'Projekt')}<br>
            <strong>Operační program:</strong> Jan Amos Komenský (OP JAK)<br>
            <strong>Verze DMP:</strong> {data_z_json_hry.get('verze_dmp', '1.0')}
        </div>
        <div class="content-section"><h2>1. Sběr dat a generování dat</h2><p>{sber or '[Tento výzkum je postaven na generování nových primárních dat.]'}</p></div>
        <div class="content-section"><h2>2. Dokumentace a kvalita dat (Metadata)</h2><p>{metadata or '[Konkrétní metadatové standardy budou implementovány do M12.]'}</p></div>
        <div class="content-section"><h2>3. Úložiště, zálohování a bezpečnost</h2><p>{uloziste or '[Během active fáze výzkumu jsou data ukládána na zabezpečených diskových polích.]'}</p></div>
    </body>
    </html>
    """
    return html_template

if "dmp_data" not in st.session_state:
    st.session_state.dmp_data = {
        "nazev_projektu": "Dosud neanalyzovaný projekt",
        "verze_dmp": "1.0",
        "aktualni_faze_hry": "Prolog (Začátek)",
        "kapitoly": {
            "sber_a_generovani": {"text_pro_sabonu": ""},
            "metadata_a_dokumentace": {"text_pro_sabonu": ""},
            "uloziste_a_bezpecnost": {"text_pro_sabonu": ""}
        }
    }
if "quest_data" not in st.session_state:
    st.session_state.quest_data = None

with st.sidebar:
    st.header("🔑 Zabezpečené AI zřídlo")
    user_api_key = st.text_input("Zadejte e-INFRA CZ Token:", type="password", placeholder="Pro simulaci nechte prázdné...")
    st.divider()
    st.header("📄 Průběžný DMP Artefakt")
    aktualni_html = vygenerovat_oficialni_html_dmp(st.session_state.dmp_data)
    b64_html = base64.b64encode(aktualni_html.encode('utf-8')).decode('utf-8')
    href_html = f'<a href="data:text/html;base64,{b64_html}" download="DMP_Export_OPJAK.html" style="text-decoration:none;"><button style="width:100%; padding:12px; background-color:#005691; color:white; border:none; border-radius:6px; font-weight:bold; cursor:pointer; margin-bottom:10px;">📄 STÁHNOUT PDF / HTML</button></a>'
    st.markdown(href_html, unsafe_allow_html=True)

st.title("🛡️ DMP Quest: OP JAK AI Engine")
st.markdown("**Hrdina:** Výzkumník 🧪  |  **Úroveň:** 1 (Novic) 🧙‍♂️")
st.divider()

st.subheader("🔮 Magický portál: Nahrání svitků projektu")
obsah_textu = st.text_area("Vložte text projektové žádosti nebo anotace:", height=150)

if st.button("Spustit bezpečnou AI analýzu 🔮"):
    if not obsah_textu:
        st.error("❌ Vložte prosím text anotace projektu k analýze.")
    else:
        # POKUS O REALNÉ VOLÁNÍ API
        api_success = False
        if user_api_key:
            with st.spinner("🔮 AI v MetaCentru provádí těžbu dat..."):
                system_instruction = "Jsi herní engine DMP Quest pro OP JAK. Analyzuj text a vrať výhradně JSON."
                try:
                    headers = {"Authorization": f"Bearer {user_api_key}", "Content-Type": "application/json"}
                    payload = {"model": "Thinker", "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": obsah_textu}], "temperature": 0.1}
                    response = requests.post("https://e-infra.cz", json=payload, headers=headers, timeout=5)
                    if response.status_code == 200 and response.text.strip():
                        match = re.search(r'\{.*\}', response.json()["choices"][0]["message"]["content"], re.DOTALL)
                        if match:
                            st.session_state.quest_data = json.loads(match.group(0))
                            st.session_state.dmp_data["nazev_projektu"] = st.session_state.quest_data.get("nazev_projektu", "Analyzovaný výzkum")
                            api_success = True
                            st.success("🎉 Analýza přes e-INFRA CZ proběhla úspěšně!")
                except Exception:
                    pass
        
        # 🛡️ ZÁLOŽNÍ INTELIGENTNÍ SIMULÁTOR (Pokud API selže nebo klíč chybí)
        if not api_success:
            st.warning("⚠️ Aktivován lokální simulační režim pro charakterizaci materiálů.")
            text_lower = obsah_textu.lower()
            
            # Detekce vašeho fyzikálního/chemického výzkumu nosičů léčiv
            if "mikroskop" in text_lower or "raman" in text_lower or "léčiv" in text_lower:
                st.session_state.quest_data = {
                    "nazev_projektu": "Charakterizace nosičů léčiv a studium jejich degradace",
                    "datlik_text": "Kolego, v textu vidím metody elektronové mikroskopie a Ramanovy spektroskopie! To znamená velkoobjemové grafické snímky (TIFF) a spektrální matice (CSV). Připravil jsem pro vás evoluční plán pro první fázi OP JAK, kde deklarujeme standardní otevřené formáty pro tato experimentální data.",
                    "matla_text": "Pozor na modelové léčivo Maytansine a úzkou institucionální spolupráci s FaF UK v Hradci a CATRIN v Olomouci! Musíme hned na začátku jasně smluvně ošetřit, kdo ta data vlastní a jakým šifrovaným kanálem si je budeme mezi univerzitami posílat, jinak máme u auditu problém!",
                    "navrzeny_text": "V počáteční fázi projektu budou experimentální data z elektronové mikroskopie (SEM) ukládána v otevřených grafických formátech (TIFF) a spektrální data z Ramanovy spektroskopie v textových formátech (CSV/ASCII) pro zajištění dlouhodobé čitelnosti. Vzhledem k partnerské spolupráci s FaF UK a CATRIN UPOL bude do měsíce M6 implementována jednotná struktura metadatového popisu a sdílený systém dokumentace výzkumu."
                }
            else:
                # Obecný záložní výzkum pro jiné texty
                st.session_state.quest_data = {
                    "nazev_projektu": "Analyzovaný výzkumný záměr",
                    "datlik_text": "Prošel jsem text vašeho grantu a vypreparoval z něj základy. Připravil jsem standardní roadmapu, která splňuje podmínky výzvy OP JAK.",
                    "matla_text": "Nezapomínejte, že ministerstvo chce přesný plán zálohování od prvního dne. Prověřte kapacity našeho IT centra!",
                    "navrzeny_text": "Data v rámci projektu budou dokumentována standardním způsobem. Ukládání aktivních dat bude realizováno na zálohovaných svazcích instituce. Sdílení dat bude odpovídat FAIR principům."
                }
            
            st.session_state.dmp_data["nazev_projektu"] = st.session_state.quest_data["nazev_projektu"]

st.divider()

if st.session_state.quest_data:
    st.subheader(f"⚔️ Dynamický Quest na míru: {st.session_state.dmp_data['nazev_projektu']}")
    st.markdown(f'<div class="npc-box-datlik"><strong>Prof. Datlík 🦆:</strong><br><em>„{st.session_state.quest_data.get("datlik_text", "")}“</em></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="npc-box-matla"><strong>Dr. Matla 🦫:</strong><br><em>„{st.session_state.quest_data.get("matla_text", "")}“</em></div>', unsafe_allow_html=True)
    st.divider()
    upraveny_text = st.text_area("Schvalte nebo upravte text vygenerovaný AI pro DMP šablonu:", value=st.session_state.quest_data.get("navrzeny_text", ""), height=130)
    if st.button("Schválit tento text a zapsat do DMP 🎯"):
        st.session_state.dmp_data["kapitoly"]["sber_a_generovani"]["text_pro_sabonu"] = upraveny_text
        st.balloons()
        st.success("🎉 Zapsáno do ministerské šablony! Zkontrolujte PDF v bočním panelu.")
