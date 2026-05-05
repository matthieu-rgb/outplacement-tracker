"""
build_samples.py - Generation des samples PDF outplacement-tracker v0.1

Genere deux documents samples (DE et EN) avec des donnees fictives anonymisees,
puis les convertit en PDF via LibreOffice headless.

Donnees fictives :
- DE : Max Mustermann, 3 mois de bilans
- EN : John Doe, 3 mois de bilans (contenu traduit)
"""

import subprocess
import shutil
import tempfile
import os
from docx import Document
from docx.oxml import OxmlElement

# -------------------------------------------------------
# Constantes
# -------------------------------------------------------

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DE = os.path.join(REPO_ROOT, "templates", "word", "transfer_mappe_template_de.docx")
TEMPLATE_EN = os.path.join(REPO_ROOT, "templates", "word", "transfer_mappe_template_en.docx")
OUTPUT_DIR = os.path.join(REPO_ROOT, "samples")

NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# -------------------------------------------------------
# Donnees fictives - Max Mustermann (DE)
# -------------------------------------------------------

DATA_DE = {
    "doc_titre": "Transfer Mappe",
    "participant_prenom": "Max",
    "participant_nom": "Mustermann",
    "participant_date_debut": "01.01.2026",
    "conseillere_nom": "Maria Schmidt",
    "doc_date_generation": "05.05.2026",

    "profil_plan_a": (
        "Projektmanager im Bereich Automobilelektronik, bevorzugt Region Saarland / Lothringen / Luxemburg, "
        "Unternehmen ab 200 Mitarbeitern, Vollzeit."
    ),
    "profil_plan_b": (
        "Technischer Berater (Freelance) fuer Diagnose- und Steuergeraetesysteme, "
        "Schwerpunkt CAN-Bus und UDS-Protokoll."
    ),
    "profil_marketingplan": (
        "20 Jahre Erfahrung in der Fahrzeugproduktion und Elektronikdiagnose. "
        "Spezialisiert auf ECU-Programmierung, CAN-Bus-Analyse und OBD-II-Protokolle. "
        "Mehrsprachig: Deutsch (Muttersprache), Franzoesisch (fliessend), Englisch (gut). "
        "Teamleitung bis 8 Personen, strukturierte Arbeitsweise, hohe Fehlertoleranz."
    ),
    "profil_zielmarkt": (
        "Saarland, Lothringen, Luxemburg. Automobilindustrie, Maschinenbau, Zulieferer. "
        "Mittelstaendische und grosse Unternehmen (100 bis 2000 Mitarbeiter)."
    ),

    # Bilan 01 - Fevrier 2026
    "bilan_01_date_rdv": "01.02.2026",
    "bilan_01_date_soumission": "28.01.2026",
    "bilan_01_bilan_general": (
        "Der erste Monat war eine Phase der Orientierung. Ich habe die Unterstuetzungsangebote "
        "des Verbands kennengelernt und begonnen, meinen Lebenslauf zu aktualisieren. "
        "Erste Kontakte zu ehemaligen Kollegen aus der Branche wurden geknuepft."
    ),
    "bilan_01_statut_objectifs": "Teilweise erreicht",
    "bilan_01_statut_objectifs_detail": (
        "Den Lebenslauf habe ich fertiggestellt. Die Recherche nach Stellenausschreibungen "
        "hat laenger gedauert als geplant - starte damit intensiver im Februar."
    ),
    "bilan_01_was_lief_gut": (
        "Die Unterstuetzung durch die Beraterin war sehr hilfreich. "
        "Ich habe Klarheit ueber meine beruflichen Staerken gewonnen."
    ),
    "bilan_01_wo_brauche_ich": (
        "Hilfe beim Verfassen eines ueberzeugenden Anschreibens auf Deutsch und Franzoesisch."
    ),
    "bilan_01_themen_naechster_termin": (
        "Anschreiben-Muster besprechen. Netzwerkstrategie fuer die Grenzregion."
    ),
    "bilan_01_sonstige_anmerkungen": "",

    # Bilan 02 - Mars 2026
    "bilan_02_date_rdv": "01.03.2026",
    "bilan_02_date_soumission": "26.02.2026",
    "bilan_02_bilan_general": (
        "Sehr aktiver Monat. Ich habe zwei Vorstellungsgespraeche gefuehrt - "
        "eines bei einem Zulieferer in Saarbruecken, eines bei einem Unternehmen in Metz. "
        "Beide Gespraeche verliefen positiv, ich warte noch auf Rueckmeldungen."
    ),
    "bilan_02_statut_objectifs": "Vollstaendig erreicht",
    "bilan_02_statut_objectifs_detail": (
        "Ziel war 2 Bewerbungen abzuschicken - habe 5 abgeschickt und 2 Vorstellungsgespraeche erhalten."
    ),
    "bilan_02_was_lief_gut": (
        "Meine technischen Kenntnisse wurden in beiden Gespraechen sehr positiv bewertet. "
        "Das Netzwerkgespraech mit dem ehemaligen Kollegen hat zur Empfehlung fuer das Saarbrueckener Unternehmen gefuehrt."
    ),
    "bilan_02_wo_brauche_ich": (
        "Coaching zur Gehaltsverhandlung. Ich bin unsicher, wie ich meine Gehaltsvorstellungen "
        "in der Grenzregion (DE/FR/LU) positionieren soll."
    ),
    "bilan_02_themen_naechster_termin": (
        "Gehaltsverhandlung vorbereiten. Entscheidungskriterien bei mehreren Angeboten."
    ),
    "bilan_02_sonstige_anmerkungen": "Vorstellungsgespraech Saarbruecken: 15.02.2026. Metz: 22.02.2026.",

    # Bilan 03 - Avril 2026
    "bilan_03_date_rdv": "01.04.2026",
    "bilan_03_date_soumission": "28.03.2026",
    "bilan_03_bilan_general": (
        "Ich habe ein schriftliches Angebot vom Unternehmen in Saarbruecken erhalten. "
        "Das Angebot ist interessant, aber einige Vertragspunkte (Homeoffice-Regelung, Urlaubstage) "
        "entsprechen nicht ganz meinen Erwartungen. Ich bin noch in der Reflexionsphase."
    ),
    "bilan_03_statut_objectifs": "Vollstaendig erreicht",
    "bilan_03_statut_objectifs_detail": (
        "Alle Ziele des letzten Termins wurden erreicht. Angebot erhalten, Verhandlungsposition vorbereitet."
    ),
    "bilan_03_was_lief_gut": (
        "Das Gehaltscoaching hat sehr geholfen. Ich konnte die Erstofferte um 8% verbessern "
        "durch gezielte Argumentation."
    ),
    "bilan_03_wo_brauche_ich": (
        "Unterstuetzung bei der Bewertung der Vertragskonditionen. "
        "Vergleich mit dem Arbeitsrecht in der Grenzregion."
    ),
    "bilan_03_themen_naechster_termin": (
        "Vertragskonditionen analysieren: Homeoffice, Urlaubsanspruch, Kuendigungsfrist. "
        "Entscheidung bis 15. April erforderlich."
    ),
    "bilan_03_sonstige_anmerkungen": (
        "Angebot erhalten am 20.03.2026. Entscheidungsfrist: 15.04.2026."
    ),

    # Bilans 04 a 12 : vides (non encore soumis)
    **{f"bilan_{nn:02d}_{field}": "" for nn in range(4, 13)
       for field in [
           "date_rdv", "date_soumission", "bilan_general", "statut_objectifs",
           "statut_objectifs_detail", "was_lief_gut", "wo_brauche_ich",
           "themen_naechster_termin", "sonstige_anmerkungen"
       ]},
}

# -------------------------------------------------------
# Donnees fictives - John Doe (EN)
# -------------------------------------------------------

DATA_EN = {
    "doc_titre": "Transfer Portfolio",
    "participant_prenom": "John",
    "participant_nom": "Doe",
    "participant_date_debut": "01.01.2026",
    "conseillere_nom": "Maria Schmidt",
    "doc_date_generation": "05.05.2026",

    "profil_plan_a": (
        "Project Manager in automotive electronics, preferably in the Saarland / Lorraine / Luxembourg "
        "region, companies with 200+ employees, full-time position."
    ),
    "profil_plan_b": (
        "Independent technical consultant for diagnostics and ECU systems, "
        "focusing on CAN-Bus and UDS protocol."
    ),
    "profil_marketingplan": (
        "20 years of experience in vehicle production and electronics diagnostics. "
        "Specialised in ECU programming, CAN-Bus analysis and OBD-II protocols. "
        "Multilingual: German (fluent), French (fluent), English (native). "
        "Team leadership up to 8 people, structured approach, high attention to detail."
    ),
    "profil_zielmarkt": (
        "Saarland, Lorraine, Luxembourg. Automotive, mechanical engineering, suppliers. "
        "Mid-sized to large companies (100 to 2000 employees)."
    ),

    # Bilan 01 - February 2026
    "bilan_01_date_rdv": "01.02.2026",
    "bilan_01_date_soumission": "28.01.2026",
    "bilan_01_bilan_general": (
        "The first month was an orientation phase. I familiarised myself with the support "
        "services available and started updating my CV. Made first contact with former colleagues "
        "in the sector."
    ),
    "bilan_01_statut_objectifs": "Partially achieved",
    "bilan_01_statut_objectifs_detail": (
        "My CV is now complete. Job search took longer than planned - "
        "will focus more intensively on this in February."
    ),
    "bilan_01_was_lief_gut": (
        "The support from my advisor was very helpful. "
        "I gained clarity on my professional strengths."
    ),
    "bilan_01_wo_brauche_ich": (
        "Help writing a compelling cover letter in German and French."
    ),
    "bilan_01_themen_naechster_termin": (
        "Review cover letter templates. Networking strategy for the cross-border region."
    ),
    "bilan_01_sonstige_anmerkungen": "",

    # Bilan 02 - March 2026
    "bilan_02_date_rdv": "01.03.2026",
    "bilan_02_date_soumission": "26.02.2026",
    "bilan_02_bilan_general": (
        "Very active month. I attended two job interviews - one with a supplier in Saarbruecken, "
        "one with a company in Metz. Both interviews went positively, still awaiting feedback."
    ),
    "bilan_02_statut_objectifs": "Fully achieved",
    "bilan_02_statut_objectifs_detail": (
        "Target was 2 applications - sent 5 and obtained 2 interviews."
    ),
    "bilan_02_was_lief_gut": (
        "My technical expertise was very positively received in both interviews. "
        "A networking conversation with a former colleague led to a referral for the Saarbruecken role."
    ),
    "bilan_02_wo_brauche_ich": (
        "Coaching on salary negotiation. Unsure how to position my salary expectations "
        "in the cross-border region (DE/FR/LU)."
    ),
    "bilan_02_themen_naechster_termin": (
        "Prepare salary negotiation. Decision criteria when receiving multiple offers."
    ),
    "bilan_02_sonstige_anmerkungen": "Saarbruecken interview: 15.02.2026. Metz: 22.02.2026.",

    # Bilan 03 - April 2026
    "bilan_03_date_rdv": "01.04.2026",
    "bilan_03_date_soumission": "28.03.2026",
    "bilan_03_bilan_general": (
        "I received a written offer from the company in Saarbruecken. The offer is interesting, "
        "but some contract points (remote work policy, annual leave) do not fully meet my expectations. "
        "I am currently in the reflection phase."
    ),
    "bilan_03_statut_objectifs": "Fully achieved",
    "bilan_03_statut_objectifs_detail": (
        "All goals from the last session were achieved. Offer received, negotiation position prepared."
    ),
    "bilan_03_was_lief_gut": (
        "The salary coaching was very helpful. I managed to improve the initial offer by 8% "
        "through targeted argumentation."
    ),
    "bilan_03_wo_brauche_ich": (
        "Support evaluating contract terms. "
        "Comparison with employment law in the cross-border region."
    ),
    "bilan_03_themen_naechster_termin": (
        "Analyse contract terms: remote work, annual leave, notice period. "
        "Decision required by 15 April."
    ),
    "bilan_03_sonstige_anmerkungen": (
        "Offer received on 20.03.2026. Decision deadline: 15.04.2026."
    ),

    # Bilans 04 a 12 : empty (not yet submitted)
    **{f"bilan_{nn:02d}_{field}": "" for nn in range(4, 13)
       for field in [
           "date_rdv", "date_soumission", "bilan_general", "statut_objectifs",
           "statut_objectifs_detail", "was_lief_gut", "wo_brauche_ich",
           "themen_naechster_termin", "sonstige_anmerkungen"
       ]},
}

# -------------------------------------------------------
# Fonctions
# -------------------------------------------------------

def fill_sdt(body_element, tag_val, text):
    """Remplace le contenu d'un Content Control (SDT) par le texte fourni."""
    for sdt in body_element.iter(f"{{{NS}}}sdt"):
        tag_el = sdt.find(f".//{{{NS}}}tag")
        if tag_el is not None and tag_el.get(f"{{{NS}}}val") == tag_val:
            content = sdt.find(f"{{{NS}}}sdtContent")
            if content is not None:
                # Vider les runs existants dans les paragraphes
                for p in content.findall(f".//{{{NS}}}p"):
                    for r in p.findall(f".//{{{NS}}}r"):
                        for t in r.findall(f"{{{NS}}}t"):
                            t.text = text if text else ""
                            return
                # Si aucun run trouve, creer la structure minimale
                p = content.find(f"{{{NS}}}p")
                if p is None:
                    p = OxmlElement("w:p")
                    content.append(p)
                r = OxmlElement("w:r")
                t = OxmlElement("w:t")
                t.text = text if text else ""
                r.append(t)
                p.append(r)
            return


def fill_template(template_path, data, output_docx_path):
    """Ouvre le template, remplace tous les SDTs, sauvegarde en .docx."""
    doc = Document(template_path)
    body = doc.element.body
    for tag_val, text in data.items():
        fill_sdt(body, tag_val, str(text))
    doc.save(output_docx_path)
    print(f"  [OK] .docx genere : {output_docx_path}")


def convert_to_pdf_libreoffice(docx_path, output_dir):
    """Convertit un .docx en PDF via LibreOffice headless."""
    result = subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", output_dir, docx_path],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        print(f"  [ERREUR] LibreOffice : {result.stderr}")
        return False
    print(f"  [OK] PDF genere dans : {output_dir}")
    return True


# -------------------------------------------------------
# Execution principale
# -------------------------------------------------------

if __name__ == "__main__":
    print("=== build_samples.py - outplacement-tracker v0.1 ===")
    print()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- DE : Max Mustermann ---
    print("Participant DE : Max Mustermann")
    docx_de = os.path.join(OUTPUT_DIR, "sample_output_de.docx")
    fill_template(TEMPLATE_DE, DATA_DE, docx_de)

    pdf_de = os.path.join(OUTPUT_DIR, "sample_pdf_output_de.pdf")
    print("  Conversion en PDF (LibreOffice headless)...")
    success_de = convert_to_pdf_libreoffice(docx_de, OUTPUT_DIR)
    if success_de:
        # LibreOffice genere le PDF avec le meme nom que le docx
        generated_pdf = os.path.join(OUTPUT_DIR, "sample_output_de.pdf")
        if os.path.exists(generated_pdf) and generated_pdf != pdf_de:
            shutil.move(generated_pdf, pdf_de)
            print(f"  [OK] Renomme en : {pdf_de}")
    else:
        print("  [WARN] PDF DE non genere. Le .docx est disponible.")

    print()

    # --- EN : John Doe ---
    print("Participant EN : John Doe")
    docx_en = os.path.join(OUTPUT_DIR, "sample_output_en.docx")
    fill_template(TEMPLATE_EN, DATA_EN, docx_en)

    pdf_en = os.path.join(OUTPUT_DIR, "sample_pdf_output_en.pdf")
    print("  Conversion en PDF (LibreOffice headless)...")
    success_en = convert_to_pdf_libreoffice(docx_en, OUTPUT_DIR)
    if success_en:
        generated_pdf = os.path.join(OUTPUT_DIR, "sample_output_en.pdf")
        if os.path.exists(generated_pdf) and generated_pdf != pdf_en:
            shutil.move(generated_pdf, pdf_en)
            print(f"  [OK] Renomme en : {pdf_en}")
    else:
        print("  [WARN] PDF EN non genere. Le .docx est disponible.")

    print()
    print("=== Termine ===")
    print(f"Fichiers dans : {OUTPUT_DIR}/")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith((".docx", ".pdf")):
            fp = os.path.join(OUTPUT_DIR, f)
            size_kb = os.path.getsize(fp) // 1024
            print(f"  {f} ({size_kb} KB)")
