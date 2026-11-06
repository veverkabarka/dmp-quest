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
    </style>
""", unsafe_allow_html=True)

def vygenerovat_oficialni_html_dmp(data_z_json_hry):
    sber = data_z_json_hry["kapitoly"].get("sber_a_generovani", {}).get("text_pro_sabonu", "")
    metadata = data_z_json_hry["kapitoly"].get("metadata_a_dokumentace", {}).get("text_pro_sabonu", "")
    uloziste = data_z_json_hry["kapitoly"].get("uloziste_a_bezpecnost", {}).get("text_pro_sabonu", "")
    pravni = data_z_json_hry["kapitoly"].get("pravni_požadavky", {}).get("text_pro_sabonu", "")
    sdileni = data_z_json_hry["kapitoly"].get("sdileni_a_udrzitelnost", {}).get("text_pro_sabonu", "")
    naklady = data_z_json_hry["kapitoly"].get("odpovednost_a_naklady", {}).get("text_pro_sabonu", "")

    # Oficiální a přímý link na spojené logo spolufinancování EU z portálu DotaceEU
    url_kombinovane_logo = "https://dotaceeu.cz"

    html_template = f"""
    <!DOCTYPE html>
    <html lang="cs">
    <head>
        <meta charset="UTF-8">
        <title>DMP - {data_z_json_hry.get('nazev_projektu', 'Projekt OP JAK')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333333; line-height: 1.6; padding: 40px; max-width: 800px; margin: 0 auto; }}
            .header-logos {{ display: flex; justify-content: center; align-items: center; border-bottom: 2px solid #005691; padding-bottom: 20px; margin-bottom: 30px; }}
            .logo-opjak {{ height: 75px; width: auto; }}
            h1 {{ color: #005691; font-size: 24px; text-transform: uppercase; margin-top: 0; }}
            h2 {{ color: #005691; font-size: 18px; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 25px; }}
            .meta-info {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 30px; font-size: 14px; }}
            .content-section {{ margin-bottom: 20px; text-align: justify; }}
            @media print {{
                body {{ padding: 0; margin: 0; font-size: 12pt; }}
                .no-print {{ display: none; }}
                @page {{ size: A4; margin: 2cm; }}
                h2 {{ page-break-after: avoid; }}
                .content-section {{ page-break-inside: avoid; }}
            }}
        </style>
    </head>
    <body>
        <div class="header-logos">
            <!-- Jediné spojené oficiální logo spolufinancování -->
            <img class="logo-opjak" src="{url_kombinovane_logo}" alt="Spolufinancováno Evropskou unií">
        </div>
        <h1>Plán správy dat (Data Management Plan)</h1>
        <div class="meta-info">
            <strong>Název projektu:</strong> {data_z_json_hry.get('nazev_projektu', 'Analýza kvantových struktur polymerů')}<br>
            <strong>Operační program:</strong> Jan Amos Komenský (OP JAK)<br>
            <strong>Verze DMP:</strong> {data_z_json_hry.get('verze_dmp', '1.0')}
        </div>
        <div class="content-section"><h2>1. Sběr dat a generování dat</h2><p>{sber or '[Tento výzkum je postaven na generování nových primárních dat.]'}</p></div>
        <div class="content-section"><h2>2. Dokumentace a kvalita dat (Metadata)</h2><p>{metadata or '[Konkrétní metadatové standardy budou implementovány do M12.]'}</p></div>
        <div class="content-section"><h2>3. Úložiště, zálohování a bezpečnost</h2><p>{uloziste or '[Během aktivní fáze výzkumu jsou data ukládána na zabezpečených diskových polích.]'}</p></div>
        <div class="content-section"><h2>4. Právní požadavky, autorská práva a licence</h2><p>{pravni or '[Otázky duševního vlastnictví budou dohodnuty do M12.]'}</p></div>
        <div class="content-section"><h2>5. Sdílení dat a dlouhodobé uchování</h2><p>{sdileni or '[Dlouhodobé uložení dat po skončení projektu bude zajištěno v repozitáři.]'}</p></div>
        <div class="content-section"><h2>6. Odpovědnost a zdroje (Náklady)</h2><p>{naklady or '[Odpovědnost za správu dat nese hlavní řešitel projektu.]'}</p></div>
        <div class="no-print" style="margin-top: 40px; text-align: center; border-top: 1px dashed #ccc; padding-top: 20px;">
            <button onclick="window.print()" style="padding: 10px 20px; background: #005691; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">Tisk / Uložit do PDF (Ctrl+P)</button>
        </div>
    </body>
    </html>
    """
    return html_template

if "dmp_data" not in st.session_state:
    st.session_state.dmp_data = {
        "nazev_projektu": "Analýza kvantových struktur polymerů",
        "verze_dmp": "1.0",
        "aktualni_faze_hry": "Prolog (Začátek)",
        "kapitoly": {
            "sber_a_generovani": {"text_pro_sabonu": ""},
            "metadata_a_dokumentace": {"text_pro_sabonu": ""},
            "uloziste_a_bezpecnost": {"text_pro_sabonu": ""},
            "pravni_požadavky": {"text_pro_sabonu": ""},
            "sdileni_a_udrzitelnost": {"text_pro_sabonu": ""},
            "odpovednost_a_naklady": {"text_pro_sabonu": ""}
        }
    }

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

st.title("🛡️ DMP Quest: OP JAK")
st.markdown("**Hrdina:** Výzkumník 🧪  |  **Úroveň:** 1 (Novic) 🧙‍♂️")
st.divider()
st.subheader("⚔️ Quest: Recyklace starých svitků (Sekce DSW 2.2.b.1)")

st.markdown('<div class="npc-box-datlik"><strong>Prof. Datlík 🦆:</strong><br><em>„Kolego, podle textu žádosti stavíte čistě na zelené louce! Připravil jsem pro vás standardní evoluční plán pro první fázi OP JAK. Upravte text níže a klikněte na tlačítko!“</em></div>', unsafe_allow_html=True)
st.markdown('<div class="npc-box-matla"><strong>Dr. Matla 🦫:</strong><br><em>„Schvalte klidně Datlíkův plán, ale v M12 vás tu zkontroluji, jestli jste do projektu nějaká cizí data tajně nepropašovali!“</em></div>', unsafe_allow_html=True)
st.divider()

vzorovy_text = "V počáteční fázi projektu se nepředpokládá opětovné využití stávajících externích datových sad. Výzkum je postaven na generování nových primárních dat. Tento stav bude revidován v rámci pravidelné aktualizace DMP v měsíci M12."
upraveny_text = st.text_area("Aktuální text plánu pro OP JAK šablonu:", value=vzorovy_text, height=120)

if st.button("Schválit tento text, zapsat do DMP a získat +30 XP 🎯"):
    st.session_state.dmp_data["kapitoly"]["sber_a_generovani"]["text_pro_sabonu"] = upraveny_text
    st.balloons()
    st.success("🎉 Úkol splněn! Data byla uložena do paměti.")
