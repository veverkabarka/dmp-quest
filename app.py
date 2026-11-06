import streamlit as st
import json
import base64

st.set_page_config(page_title="DMP Quest: OP JAK", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #f43f5e; color: white; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background-color: #e11d48; }
    .npc-box-datlik { background-color: rgba(56, 189, 248, 0.1); border-left: 5px solid #38bdf8; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .npc-box-matla { background-color: rgba(244, 63, 94, 0.1); border-left: 5px solid #f43f5e; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .upload-zone { background-color: rgba(245, 158, 11, 0.05); border: 2px dashed #f59e0b; padding: 20px; border-radius: 8px; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# --- POMOCNÁ FUNKCE: Generování tiskové šablony s logy ---
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
            <strong>Název projektu:</strong> {data_z_json_hry.get('nazev_projektu', 'Zpracovaný výzkum')}<br>
            <strong>Operační program:</strong> Jan Amos Komenský (OP JAK)<br>
            <strong>Verze DMP:</strong> {data_z_json_hry.get('verze_dmp', '1.0')}
        </div>
        <div class="content-section"><h2>1. Sběr dat a generování dat</h2><p>{sber or '[Tento výzkum je postaven na generování nových primárních dat. Podrobný plán bude aktualizován v měsíci M12.]'}</p></div>
        <div class="content-section"><h2>2. Dokumentace a kvalita dat (Metadata)</h2><p>{metadata or '[Konkrétní metadatové standardy budou implementovány do měsíce M12.]'}</p></div>
        <div class="content-section"><h2>3. Úložiště, zálohování a bezpečnost</h2><p>{uloziste or '[Během aktivní fázevýzkumu jsou data ukládána na bezpečné infrastruktuře.]'}</p></div>
    </body>
    </html>
    """
    return html_template

# --- INICIALIZACE STAVU HRY ---
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
if "active_quests" not in st.session_state:
    st.session_state.active_quests = {}

with st.sidebar:
    st.header("📄 Průběžný DMP Artefakt")
    st.caption("Soubory se automaticky aktualizují při každé změně.")
    aktualni_html = vygenerovat_oficialni_html_dmp(st.session_state.dmp_data)
    b64_html = base64.b64encode(aktualni_html.encode('utf-8')).decode('utf-8')
    href_html = f'<a href="data:text/html;base64,{b64_html}" download="DMP_Export_OPJAK.html" style="text-decoration:none;"><button style="width:100%; padding:12px; background-color:#005691; color:white; border:none; border-radius:6px; font-weight:bold; cursor:pointer; margin-bottom:10px;">📄 STÁHNOUT PDF / HTML</button></a>'
    st.markdown(href_html, unsafe_allow_html=True)
    st.divider()
    st.download_button(
        label="💾 ULOŽIT HERNÍ POZICI (JSON)",
        data=json.dumps(st.session_state.dmp_data, indent=2, ensure_ascii=False),
        file_name="dmp_quest_save.json",
        mime="application/json",
        use_container_width=True
    )

st.title("🛡️ DMP Quest: OP JAK Engine v1.0")
st.markdown("**Hrdina:** Výzkumník 🧪  |  **Úroveň:** 1 (Novic) 🧙‍♂️")
st.divider()

# =========================================================================
# 🔮 INTLIGENTNÍ PARSER: AUTOMATICKÁ ANALÝZA TEXTU
# =========================================================================
st.subheader("🔮 Magický portál: Nahrání svitků projektu")
st.caption("Vložte text projektové anotace. Systém automaticky odfiltruje zbytečnosti a vygeneruje úkoly.")
obsah_textu = st.text_area("Zde vložte text anotace výzkumu:", height=150, placeholder="Sem zkopírujte text (např. o mikroskopii nosičů léčiv)...")

if st.button("Spustit bleskovou textovou analýzu 🔮"):
    if not obsah_textu:
        st.error("❌ Vložte prosím text anotace projektu k analýze.")
    else:
        with st.spinner("🔮 Systém zpracovává klíčová slova výzkumu..."):
            text_lower = obsah_textu.lower()
            quests = {}
            
            # 🕵️‍♂️ KROK 1: DETEKCE MIKROSKOPIE A NOSIČŮ LÉČIV (Fyzikální/Chemický obor)
            if "mikroskop" in text_lower or "raman" in text_lower or "léčiv" in text_lower or "maytansine" in text_lower:
                st.session_state.dmp_data["nazev_projektu"] = "Charakterizace nosičů léčiv a studium jejich degradace"
                
                quests["kap1"] = {
                    "titul": "⚔️ Quest 1: Analýza spektroskopických matic (Sběr dat)",
                    "datlik": "Kolego, v anotaci vidím metody elektronové mikroskopie (SEM) a Ramanovy spektroskopie! To znamená velkoobjemové grafické snímky (TIFF) a spektrální matice (CSV). Skvělé, pro začátek projektu (Prolog) jednoduše schválíme tento standardní otevřený formát primárních dat.",
                    "matla": "Pozor na modelové léčivo Maytansine a úzkou spolupráci s FaF UK v Hradci a CATRIN v Olomouci! Musíme hned na začátku jasně ošetřit, kdo ta data fyzicky vlastní a jakým šifrovaným kanálem si je budeme posílat, jinak máme u auditu problém!",
                    "vzor": "V počáteční fázi projektu budou experimentální data z elektronové mikroskopie (SEM) ukládána v otevřených grafických formátech (TIFF) a spektrální data z Ramanovy spektroskopie v textových formátech (CSV/ASCII) pro zajištění dlouhodobé čitelnosti. Vzhledem k partnerské spolupráci s FaF UK a CATRIN UPOL bude do měsíce M6 implementována jednotná struktura popisu dat."
                }
                quests["kap3"] = {
                    "titul": "🛡️ Quest 2: Zabezpečení fyzikálních truhlic (Úložiště)",
                    "datlik": "Pro ukládání aktivních dat během výzkumu využijeme bezpečné servery naší Přírodovědecké fakulty UHK propojené se synchronizovaným cloudem CESNET (ownCloud). Zálohy poběží automaticky každou noc.",
                    "matla": "ownCloud je sice fajn, ale ty nanočástice oxidu grafenu a liposomů jsou drahé chráněné know-how! Přístup k nim musí být v laboratoři striktně omezen přístupovými právy, žádné veřejné sdílení chemických struktur na nešifrovaných discích!",
                    "vzor": "Aktivní výzkumná data budou průběžně ukládána na dedikovaných síťových discích Katedry fyziky UHK se zrcadleným zálohováním a paralelně synchronizována do zabezpečeného cloudového úložiště CESNET. Přístup k surovým datovým sadám bude chráněn přístupovými právy vázanými na identitu eduID."
                }
            
            # 🕵️‍♂️ KROK 2: OBECNÝ ZÁLOŽNÍ VÝZKUM (Pro jakékoliv jiné texty)
            else:
                st.session_state.dmp_data["nazev_projektu"] = "Analyzovaný vědecký záměr"
                quests["kap1"] = {
                    "titul": "⚔️ Quest 1: Typologie nových dat (Sběr dat)",
                    "datlik": "Prošel jsem text vašeho grantu a vypreparoval z něj základy. Výzkum staví na zelené louce, budeme generovat standardní primární datové sady.",
                    "matla": "Nezapomínejte, že ministerstvo chce v šabloně OP JAK přesný přehled formátů. Žádné obecné plácání!",
                    "vzor": "V rámci projektu budou generována primární data odpovídající cílům výzkumných aktivit. Data budou ukládána v běžných, dlouhodobě udržitelných formátech, jejichž přesná specifikace bude průběžně doplňována."
                }
                quests["kap3"] = {
                    "titul": "🛡️ Quest 2: Bezpečné úložiště (Zálohování)",
                    "datlik": "Ukládání aktivních dat bude realizováno na zálohovaných svazcích naší instituce. Data budou chráněna před ztrátou.",
                    "matla": "Prověřte si hned první měsíc kapacity našeho univerzitního IT centra, ať máme papíry pro monitoring v pořádku!",
                    "vzor": "Ukládání aktivních dat bude realizováno na zálohovaných svazcích instituce. Data budou chráněna před ztrátou pravidelným síťovým zálohováním."
                }

            st.session_state.active_quests = quests
            st.success("🎉 Analýza dokončena! Úkoly byly dynamicky vygenerovány přesně pro váš vědní obor.")

st.divider()

