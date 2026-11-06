import streamlit as st
import json
import base64
import re
import html as html_mod

# =========================================================================
# NASTAVENÍ STRÁNKY
# =========================================================================
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


# =========================================================================
# 1. POMOCNÉ FUNKCE
# =========================================================================
def _logo_data_uri(cesta="loga_spojena.png"):
    """Bezpečně vloží logo jako base64 data URI. Při chybějícím souboru vrátí ''."""
    try:
        with open(cesta, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    except (FileNotFoundError, OSError):
        return ""


def _esc(text):
    """HTML-escape + zachování zalomení řádků (pro vkládání do <p>)."""
    return html_mod.escape(str(text or "")).replace("\n", "<br>")


def vygenerovat_oficialni_html_dmp(data_z_json_hry):
    k = data_z_json_hry.get("kapitoly", {})

    sber = _esc(k.get("sber_a_generovani", {}).get("text_pro_sabonu", ""))
    metadata = _esc(k.get("metadata_a_dokumentace", {}).get("text_pro_sabonu", ""))
    uloziste = _esc(k.get("uloziste_a_bezpecnost", {}).get("text_pro_sabonu", ""))

    nazev = html_mod.escape(str(data_z_json_hry.get("nazev_projektu", "Projekt OP JAK")))
    verze = html_mod.escape(str(data_z_json_hry.get("verze_dmp", "1.0")))
    logo = _logo_data_uri()

    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <title>DMP - {nazev}</title>
    <style>
        body {{ font-family: Arial, sans-serif; color: #333333; line-height: 1.6; padding: 40px; max-width: 800px; margin: 0 auto; }}
        .header-logos {{ display: flex; justify-content: center; align-items: center; border-bottom: 2px solid #005691; padding-bottom: 20px; margin-bottom: 30px; }}
        .logo-opjak {{ height: 65px; width: auto; }}
        h1 {{ color: #005691; font-size: 24px; text-transform: uppercase; margin-top: 0; }}
        h2 {{ color: #005691; font-size: 18px; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 25px; }}
        .meta-info {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 30px; font-size: 14px; }}
        .content-section {{ margin-bottom: 20px; text-align: justify; }}
        @media print {{ body {{ padding: 0; max-width: none; }} }}
    </style>
</head>
<body>
    <div class="header-logos">
        <img class="logo-opjak" src="{logo}" alt="Publicita OP JAK">
    </div>
    <h1>Plán správy dat (Data Management Plan)</h1>
    <div class="meta-info">
        <strong>Název projektu:</strong> {nazev}<br>
        <strong>Operační program:</strong> Jan Amos Komenský (OP JAK)<br>
        <strong>Verze DMP:</strong> {verze}
    </div>
    <div class="content-section"><h2>1. Sběr dat a generování dat</h2><p>{sber or '[Tento výzkum je postaven na generování nových primárních dat. Podrobný plán bude aktualizován v měsíci M12.]'}</p></div>
    <div class="content-section"><h2>2. Dokumentace a kvalita dat (Metadata)</h2><p>{metadata or '[Konkrétní metadatové standardy budou implementovány do měsíce M12.]'}</p></div>
    <div class="content-section"><h2>3. Úložiště, zálohování a bezpečnost</h2><p>{uloziste or '[Během aktivní fáze výzkumu jsou data ukládána na zabezpečených diskových polích.]'}</p></div>
</body>
</html>"""


def render_sidebar():
    """Vykreslí sidebar. Musí se volat až na konci skriptu, aby export obsahoval aktuální data."""
    with st.sidebar:
        st.header("📄 Průběžný DMP Artefakt")
        st.caption("Soubory se automaticky aktualizují při každé změně.")

        st.download_button(
            label="📄 STÁHNOUT DMP (HTML / TISK)",
            data=vygenerovat_oficialni_html_dmp(st.session_state.dmp_data),
            file_name="DMP_Export_OPJAK.html",
            mime="text/html",
            use_container_width=True,
        )
        st.caption("Uložte jako HTML, otevřete na disku a stiskněte Ctrl+P pro tisk do čistého PDF.")

        st.divider()

        st.download_button(
            label="💾 ULOŽIT HERNÍ POZICI (JSON)",
            data=json.dumps(st.session_state.dmp_data, indent=2, ensure_ascii=False),
            file_name="dmp_quest_save.json",
            mime="application/json",
            use_container_width=True,
        )

        st.divider()

        if st.button("🔄 Restartovat hru", help="Smaže všechny odpovědi a začne znovu."):
            for klic in list(st.session_state.keys()):
                if klic.startswith("ta_") or klic in ("dmp_data", "active_quests"):
                    del st.session_state[klic]
            st.rerun()


# =========================================================================
# 2. INICIALIZACE STAVU HRY
# =========================================================================
if "dmp_data" not in st.session_state:
    st.session_state.dmp_data = {
        "nazev_projektu": "Dosud neanalyzovaný projekt",
        "verze_dmp": "1.1",
        "aktualni_faze_hry": "Prolog (Začátek)",
        "kapitoly": {
            "sber_a_generovani": {"text_pro_sabonu": ""},
            "metadata_a_dokumentace": {"text_pro_sabonu": ""},
            "uloziste_a_bezpecnost": {"text_pro_sabonu": ""},
        },
    }

if "active_quests" not in st.session_state:
    st.session_state.active_quests = {}

MAPA_KAPITOL = {
    "kap1": "sber_a_generovani",
    "kap2": "metadata_a_dokumentace",
    "kap3": "uloziste_a_bezpecnost",
}


# =========================================================================
# 3. HLAVIČKA
# =========================================================================
st.title("🛡️ DMP Quest: OP JAK Engine v1.1")
st.markdown("**Hrdina:** Výzkumník 🧪  |  **Úroveň:** 1 (Novic) 🧙‍♂️")
st.divider()


# =========================================================================
# 4. INTELIGENTNÍ PARSER
# =========================================================================
st.subheader("🔮 Magický portál: Nahrání svitků projektu")
st.caption("Vložte text projektové anotace. Systém automaticky odfiltruje zbytečnosti a vygeneruje úkoly.")

obsah_textu = st.text_area(
    "Zde vložte text anotace výzkumu:",
    height=150,
    placeholder="Sem zkopírujte text o mikroskopii nosičů léčiv...",
)

if st.button("Spustit bleskovou textovou analýzu 🔮"):
    if not obsah_textu.strip():
        st.error("❌ Vložte prosím text anotace projektu k analýze.")
    else:
        with st.spinner("🔮 Systém zpracovává klíčová slova výzkumu..."):
            text_lower = obsah_textu.lower()
            quests = {}

            # Robustnější detekce – \b zabrání falešným zásahům uvnitř slov
            is_microscopy = bool(
                re.search(r"\bmikroskop\w*|\braman\w*|\bléčiv\w*|\bmaytansin\w*", text_lower)
            )

            if is_microscopy:
                st.session_state.dmp_data["nazev_projektu"] = (
                    "Charakterizace nosičů léčiv a studium jejich degradace"
                )

                quests["kap1"] = {
                    "titul": "⚔️ Quest 1: Analýza spektroskopických matic (Sběr dat)",
                    "datlik": "Kolego, v anotaci vidím metody elektronové mikroskopie (SEM) a Ramanovy spektroskopie! To znamená velkoobjemové grafické snímky (TIFF) a spektrální matice (CSV). Skvělé, pro začátek projektu (Prolog) jednoduše schválíme tento standardní otevřený formát primárních dat.",
                    "matla": "Pozor na modelové léčivo Maytansine a úzkou spolupráci s Farmaceutickou fakultou UK v Hradci a CATRIN v Olomouci! Musíme hned na začátku jasně ošetřit, kdo ta data fyzicky vlastní a jakým šifrovaným kanálem si je budeme posílat, jinak máme u auditu problém!",
                    "vzor": "V počáteční fázi projektu budou experimentální data z elektronové mikroskopie (SEM) ukládána v otevřených grafických formátech (TIFF) a spektrální data z Ramanovy spektroskopie v textových formátech (CSV/ASCII) pro zajištění dlouhodobé čitelnosti. Vzhledem k partnerské spolupráci s FaF UK a CATRIN UPOL bude do měsíce M6 implementována jednotná struktura popisu dat.",
                }
                quests["kap2"] = {
                    "titul": "📜 Quest 2: Kodex mikroskopických metadat (Metadata a standardy)",
                    "datlik": "Pro popis snímků a spekter využijeme standardizované hlavičky přímo z měřicích přístrojů. Data popíšeme základními informacemi o typu vzorku a verzi použitého softwaru.",
                    "matla": "Snímky z elektronového mikroskopu bez jasných metadat jsou za dva roky jen hromada křížovek! Musíme hned zavést sdílený elektronický laboratorní deník, jinak se v těch datech z Olomouce a Hradce nikdo nevyzná!",
                    "vzor": "Metadata budou generována automaticky softwarovým rozhraním analytických přístrojů (SEM, Raman) a ukládána společně se surovými daty. Popis metadat bude sledovat standardy doporučené pro materiálové vědy a bude sjednocen s externími partnery (FaF UK, CATRIN) do měsíce M12.",
                }
                quests["kap3"] = {
                    "titul": "🛡️ Quest 3: Zabezpečení fyzikálních truhlic (Úložiště)",
                    "datlik": "Pro ukládání aktivních dat během výzkumu využijeme bezpečné servery naší Přírodovědecké fakulty UHK propojené se synchronizovaným cloudem CESNET (ownCloud). Zálohy poběží automaticky každou noc.",
                    "matla": "ownCloud je sice fajn, ale ty nanočástice oxidu grafenu a liposomů jsou drahé chráněné know-how! Přístup k nim musí být v laboratoři striktně omezen přístupovými právy, žádné veřejné sdílení chemických struktur na nešifrovaných discích!",
                    "vzor": "Aktivní výzkumná data budou průběžně ukládána na dedikovaných síťových discích Katedry fyziky UHK se zrcadleným zálohováním a paralelně synchronizována do zabezpečeného cloudového úložiště CESNET. Přístup k surovým datovým sadám bude chráněn přístupovými právy vázanými na identitu eduID.",
                }

            else:
                st.session_state.dmp_data["nazev_projektu"] = "Analyzovaný výzkumný záměr"

                quests["kap1"] = {
                    "titul": "⚔️ Quest 1: Typologie nových dat (Sběr dat)",
                    "datlik": "Prošel jsem text vašeho grantu a vypreparoval z něj základy. Výzkum staví na zelené louce, budeme generovat standardní primární datové sady.",
                    "matla": "Nezapomínejte, že ministerstvo chce v šabloně OP JAK přesný přehled formátů. Žádné obecné plácání!",
                    "vzor": "V rámci projektu budou generována primární data odpovídající cílům výzkumných aktivit. Data budou ukládána v běžných, dlouhodobě udržitelných formátech, jejichž přesná specifikace bude průběžně doplňována.",
                }
                quests["kap2"] = {
                    "titul": "📜 Quest 2: Popis dat a metadata (Dokumentace)",
                    "datlik": "Ke každé datové sadě doporučuji vést čitelný README soubor s popisem proměnných, jednotek a způsobu sběru.",
                    "matla": "Bez metadat jsou data pro recenzenta nepoužitelná. Zaveďte jednotný popis hned od prvního měření!",
                    "vzor": "K vytvářeným datovým sadám bude vedena průvodní dokumentace v podobě souborů README s popisem struktury, jednotek a metodiky sběru dat. Dokumentace bude uložena společně s daty a bude aktualizována při každé změně datové sady.",
                }
                quests["kap3"] = {
                    "titul": "🛡️ Quest 3: Bezpečné úložiště (Zálohování)",
                    "datlik": "Ukládání aktivních dat bude realizováno na zálohovaných svazcích naší instituce. Data budou chráněna před ztrátou.",
                    "matla": "Prověřte si hned první měsíc kapacity našeho univerzitního IT centra, ať máme papíry pro monitoring v pořádku!",
                    "vzor": "Ukládání aktivních dat bude realizováno na zálohovaných svazcích instituce. Data budou chráněna před ztrátou pravidelným síťovým zálohováním.",
                }

            # Nová analýza = zahoď staré rozepsané texty, ať se načte nový vzor
            for klic in list(st.session_state.keys()):
                if klic.startswith("ta_"):
                    del st.session_state[klic]

            st.session_state.active_quests = quests

        st.success("🎉 Analýza dokončena! Úkoly byly dynamicky vygenerovány přesně pro váš vědní obor.")


# =========================================================================
# 5. RENDER ÚKOLŮ + PROPIS DO DMP
# =========================================================================
if st.session_state.active_quests:
    st.divider()
    st.subheader("🗺️ Vaše úkoly")

    for key, q in st.session_state.active_quests.items():
        st.markdown(f"### {q['titul']}")

        st.markdown(
            f'<div class="npc-box-datlik">🐿️ <strong>Datlík (datový kurátor):</strong><br>{_esc(q["datlik"])}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="npc-box-matla">🔥 <strong>Matla (bezpečnost):</strong><br>{_esc(q["matla"])}</div>',
            unsafe_allow_html=True,
        )

        kap = MAPA_KAPITOL.get(key)
        if not kap:
            st.warning(f"⚠️ Neznámý klíč úkolu: {key}")
            continue

        widget_key = f"ta_{key}"
        st.session_state.setdefault(
            widget_key,
            st.session_state.dmp_data["kapitoly"][kap]["text_pro_sabonu"] or q["vzor"],
        )

        text = st.text_area(
            "Text pro šablonu DMP (můžeš upravit):",
            key=widget_key,
            height=140,
        )

        # Zápis do NE-widget klíče – to je bezpečné i po instancování widgetu
        st.session_state.dmp_data["kapitoly"][kap]["text_pro_sabonu"] = text


# =========================================================================
# 6. SIDEBAR – až na konci, aby export obsahoval aktuální data
# =========================================================================
render_sidebar()
