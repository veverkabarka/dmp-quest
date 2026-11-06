import streamlit as st
import json
import base64
import requests

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

# --- POMOCNÁ FUNKCE: Generování tiskové šablony ---
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
            <strong>Název projektu:</strong> {data_z_json_hry.get('nazev_projektu', 'Projekt z analýzy grantu')}<br>
            <strong>Operační program:</strong> Jan Amos Komenský (OP JAK)<br>
            <strong>Verze DMP:</strong> {data_z_json_hry.get('verze_dmp', '1.0')}
        </div>
        <div class="content-section"><h2>1. Sběr dat a generování dat</h2><p>{sber or '[Tento výzkum je postaven na generování nových primárních dat.]'}</p></div>
        <div class="content-section"><h2>2. Dokumentace a kvalita dat (Metadata)</h2><p>{metadata or '[Konkrétní metadatové standardy budou implementovány do M12.]'}</p></div>
        <div class="content-section"><h2>3. Úložiště, zálohování a bezpečnost</h2><p>{uloziste or '[Během aktivní fáze výzkumu jsou data ukládána na zabezpečených diskových polích.]'}</p></div>
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
if "quest_data" not in st.session_state:
    st.session_state.quest_data = None

# =========================================================================
# 📊 BOČNÍ PANEL (SIDEBAR) – BEZPEČNOSTNÍ KLÍČ A EXPORTY
# =========================================================================
with st.sidebar:
    st.header("🔑 Zabezpečené AI zřídlo")
    # Uživatelské zadání API klíče z e-INFRA CZ
    user_api_key = st.text_input("Zadejte e-INFRA CZ Token:", type="password", placeholder="Bearer token z chat.ai.e-infra.cz...")
    st.caption("Klíč se nikam neukládá, po zavření prohlížeče bezpečně mizí.")
    
    st.divider()
    st.header("📄 Průběžný DMP Artefakt")
    aktualni_html = vygenerovat_oficialni_html_dmp(st.session_state.dmp_data)
    b64_html = base64.b64encode(aktualni_html.encode('utf-8')).decode('utf-8')
    href_html = f'<a href="data:text/html;base64,{b64_html}" download="DMP_Export_OPJAK.html" style="text-decoration:none;"><button style="width:100%; padding:12px; background-color:#005691; color:white; border:none; border-radius:6px; font-weight:bold; cursor:pointer; margin-bottom:10px;">📄 STÁHNOUT PDF / HTML</button></a>'
    st.markdown(href_html, unsafe_allow_html=True)
    
    st.download_button(
        label="💾 ULOŽIT HERNÍ POZICI (JSON)",
        data=json.dumps(st.session_state.dmp_data, indent=2, ensure_ascii=False),
        file_name="dmp_quest_save.json",
        mime="application/json",
        use_container_width=True
    )

# =========================================================================
# ⚔️ HLAVNÍ PLOCHA HRY
# =========================================================================
st.title("🛡️ DMP Quest: OP JAK AI Engine")
st.markdown("**Hrdina:** Výzkumník 🧪  |  **Úroveň:** 1 (Novic) 🧙‍♂️")
st.divider()

# 🔮 PORTÁL NAHRÁVÁNÍ TEXTU GRANTU
st.subheader("🔮 Magický portál: Nahrání svitků projektu")
st.caption("AI v e-INFRA CZ přečte text a vytvoří úkoly na míru vědnímu oboru.")
obsah_textu = st.text_area("Vložte text projektové žádosti nebo anotace:", height=150, placeholder="Sem zkopírujte anotaci projektu (např. nosiče léčiv, mikroskopie)...")

if st.button("Spustit bezpečnou AI analýzu 🔮"):
    if not user_api_key:
        st.error("❌ Nejprve zadejte svůj e-INFRA CZ Token v bočním panelu!")
    elif not obsah_textu:
        st.error("❌ Vložte prosím text anotace projektu k analýze.")
    else:
        with st.spinner("🔮 AI v MetaCentru provádí těžbu dat..."):
            # Master Prompt instruující model od e-infra
            system_instruction = (
                "Jsi Game Master hry DMP Quest. Analyzuj text projektu a vytáhni z něj informace pro DMP. "
                "Vrať VÝHRADNĚ validní JSON objekt bez markdown značek se strukturou: "
                '{"nazev_projektu": "...", "datlik_text": "...", "matla_text": "...", "navrzeny_text": "..."}'
            )
            
            try:
                # Volání oficiálního rozhraní e-INFRA CZ
                headers = {"Authorization": f"Bearer {user_api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": "thinker",
                    "messages": [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": obsah_textu}
                    ],
                    "temperature": 0.2
                }
                response = requests.post("https://e-infra.cz", json=payload, headers=headers)
                
                if response.status_code == 200:
                    odpoved_text = response.json()["choices"][0]["message"]["content"].strip()
                    # Očištění od případných ```json wrapperů
                    if odpoved_text.startswith("```"):
                        odpoved_text = odpoved_text.replace("```json", "").replace("```", "").strip()
                    
                    st.session_state.quest_data = json.loads(odpoved_text)
                    st.session_state.dmp_data["nazev_projektu"] = st.session_state.quest_data["nazev_projektu"]
                    st.success("🎉 Analýza dokončena! Nový quest byl dynamicky vygenerován na míru vašeho projektu.")
                else:
                    st.error(f"Chyba API e-INFRA: Kód {response.status_code}. Zkontrolujte platnost tokenu.")
            except Exception as e:
                st.error(f"Chyba při komunikaci: {str(e)}")

st.divider()

# =========================================================================
# ⚔️ DYNAMICKÝ QUEST (Zobrazí se pouze po úspěšné AI analýze)
# =========================================================================
if st.session_state.quest_data:
    st.subheader(f"⚔️ Dynamický Quest: Kapitola 1 & 3")
    
    # AI vložila text do úst Datlíkovi
    st.markdown(f"""
    <div class="npc-box-datlik">
        <strong>Prof. Datlík 🦆:</strong><br>
        <em>„{st.session_state.quest_data['datlik_text']}“</em>
    </div>
    """, unsafe_allow_html=True)
    
    # AI vložila text do úst Matlovi
    st.markdown(f"""
    <div class="npc-box-matla">
        <strong>Dr. Matla 🦫:</strong><br>
        <em>„{st.session_state.quest_data['matla_text']}“</em>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Textová zóna s popisem navrženým na míru přímo od e-INFRA AI
    upraveny_text = st.text_area("Schvalte nebo upravte text vygenerovaný AI na míru projektu:", 
                                 value=st.session_state.quest_data['navrzeny_text'], height=130)
    
    if st.button("Schválit tento AI text a zapsat do DMP 🎯"):
        st.session_state.dmp_data["kapitoly"]["sber_a_generovani"]["text_pro_sabonu"] = upraveny_text
        st.balloons()
        st.success("🎉 Zapsáno do ministerské šablony! Zkontrolujte PDF v bočním panelu.")
