"""
build_templates.py
------------------
Generates transfer_mappe_template_de.docx and transfer_mappe_template_en.docx.

Each file contains 118 Plain Text Content Controls (w:sdt elements) with the
exact Tag values required by the Power Automate "Populate a Microsoft Word template"
action (Word Online Business connector).

Dependencies:
    pip install python-docx

Usage:
    python3 build_templates.py

Output:
    templates/word/transfer_mappe_template_de.docx
    templates/word/transfer_mappe_template_en.docx

Verification:
    python3 -c "
    from docx import Document
    import zipfile, re
    d = Document('templates/word/transfer_mappe_template_de.docx')
    with zipfile.ZipFile('templates/word/transfer_mappe_template_de.docx') as z:
        xml = z.read('word/document.xml').decode()
    tags = re.findall(r'w:val=\"([^\"]+)\"', xml)
    print(len(tags), 'tag values found')
    "
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_sdt_block(tag_val, placeholder=""):
    """
    Build a block-level Plain Text Content Control (w:sdt) element.
    This is the structure required by Power Automate "Populate a Microsoft Word
    template" action. Tag value is the key used for field matching in the Flow.
    """
    sdt = OxmlElement('w:sdt')

    sdtPr = OxmlElement('w:sdtPr')

    tag = OxmlElement('w:tag')
    tag.set(qn('w:val'), tag_val)
    sdtPr.append(tag)

    alias = OxmlElement('w:alias')
    alias.set(qn('w:val'), tag_val)
    sdtPr.append(alias)

    text_el = OxmlElement('w:text')
    sdtPr.append(text_el)

    sdt.append(sdtPr)

    sdtContent = OxmlElement('w:sdtContent')
    p = OxmlElement('w:p')
    r = OxmlElement('w:r')
    t = OxmlElement('w:t')
    t.text = placeholder
    r.append(t)
    p.append(r)
    sdtContent.append(p)
    sdt.append(sdtContent)

    return sdt


def append_sdt(doc, tag_val, placeholder=""):
    """Append a block-level SDT directly to the document body."""
    doc.element.body.append(make_sdt_block(tag_val, placeholder))


def add_heading(doc, text, level=1):
    """Add a heading paragraph with blue corporate color (#003DA5)."""
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        run.font.color.rgb = RGBColor(0x00, 0x3D, 0xA5)
    return p


def add_label_paragraph(doc, label):
    """Add a bold label paragraph (for field captions)."""
    p = doc.add_paragraph()
    run = p.add_run(label)
    run.bold = True
    return p


def add_signature_block(doc, labels):
    """
    Add the fixed signature block for a Zielvereinbarung section.
    This is plain text - NOT a Content Control. Power Automate ignores it.
    labels = {
        'title': str,
        'datum': str,
        'left_label': str,
        'right_label': str,
        'left_line': str,
        'right_line': str,
    }
    """
    doc.add_paragraph()
    p = doc.add_paragraph(labels['title'])
    p.runs[0].bold = True

    doc.add_paragraph(labels['datum'])

    sig_p = doc.add_paragraph()
    sig_p.add_run(labels['left_label'])
    sig_p.add_run("                    ")
    sig_p.add_run(labels['right_label'])

    line_p = doc.add_paragraph()
    line_p.add_run(labels['left_line'])
    line_p.add_run("       ")
    line_p.add_run(labels['right_line'])

    doc.add_paragraph()


# ---------------------------------------------------------------------------
# Content Control tag lists
# ---------------------------------------------------------------------------

COVER_TAGS = [
    "doc_titre",
    "participant_prenom",
    "participant_nom",
    "participant_date_debut",
    "conseillere_nom",
    "doc_date_generation",
]

PROFIL_TAGS = [
    "profil_plan_a",
    "profil_plan_b",
    "profil_marketingplan",
    "profil_zielmarkt",
]

BILAN_FIELDS = [
    "date_rdv",
    "date_soumission",
    "bilan_general",
    "statut_objectifs",
    "statut_objectifs_detail",
    "was_lief_gut",
    "wo_brauche_ich",
    "themen_naechster_termin",
    "sonstige_anmerkungen",
]

# Expected total: 6 + 4 + (12 * 9) = 118


# ---------------------------------------------------------------------------
# DE template content
# ---------------------------------------------------------------------------

DE_STRINGS = {
    "doc_title_fixed":  "TRANSFER MAPPE",
    "doc_titre_placeholder": "Transfer Mappe",
    "confidential": "Vertraulich - Nur fuer den internen Gebrauch",
    "cover_labels": {
        "doc_titre":              "Dokumenttitel",
        "participant_prenom":     "Teilnehmer/in - Vorname",
        "participant_nom":        "Teilnehmer/in - Nachname",
        "participant_date_debut": "Beginn des Parcours",
        "conseillere_nom":        "Beraterin",
        "doc_date_generation":    "Erstellt am",
    },
    "section_profil_heading":  "1. Karriereprofil",
    "section_profil_sub":      "Berufliche Zielsetzung",
    "profil_labels": {
        "profil_plan_a":         "Plan A - Berufliches Hauptziel",
        "profil_plan_b":         "Plan B - Berufliches Alternativziel",
        "profil_marketingplan":  "Berufliches Profil und Staerken (Marketingplan)",
        "profil_zielmarkt":      "Zielmarkt",
    },
    "bilan_heading":  "Zielvereinbarung - Bilan {nn:02d}",
    "bilan_labels": {
        "date_rdv":                "Datum des Termins",
        "date_soumission":         "Eingangsdatum",
        "bilan_general":           "Allgemeine Einschaetzung des Monats",
        "statut_objectifs":        "Status der vorherigen Ziele",
        "statut_objectifs_detail": "Details zum Zielstatus",
        "was_lief_gut":            "Was lief gut?",
        "wo_brauche_ich":          "Wo brauche ich Unterstuetzung?",
        "themen_naechster_termin": "Themen fuer den naechsten Termin",
        "sonstige_anmerkungen":    "Sonstige Anmerkungen",
    },
    "signature": {
        "title":       "Zielvereinbarung - Unterschriften",
        "datum":       "Datum: .............................",
        "left_label":  "Teilnehmer/in:",
        "right_label": "                              Beraterin:",
        "left_line":   "_________________________________",
        "right_line":  "       _________________________________",
    },
}


# ---------------------------------------------------------------------------
# EN template content
# ---------------------------------------------------------------------------

EN_STRINGS = {
    "doc_title_fixed":  "TRANSFER PORTFOLIO",
    "doc_titre_placeholder": "Transfer Portfolio",
    "confidential": "Confidential - For internal use only",
    "cover_labels": {
        "doc_titre":              "Document title",
        "participant_prenom":     "Participant - First name",
        "participant_nom":        "Participant - Last name",
        "participant_date_debut": "Start date",
        "conseillere_nom":        "Advisor",
        "doc_date_generation":    "Generated on",
    },
    "section_profil_heading":  "1. Career Profile",
    "section_profil_sub":      "Professional objectives",
    "profil_labels": {
        "profil_plan_a":         "Plan A - Primary professional objective",
        "profil_plan_b":         "Plan B - Alternative professional objective",
        "profil_marketingplan":  "Professional profile and strengths (Marketing plan)",
        "profil_zielmarkt":      "Target market",
    },
    "bilan_heading":  "Monthly Review - Session {nn:02d}",
    "bilan_labels": {
        "date_rdv":                "Appointment date",
        "date_soumission":         "Submission date",
        "bilan_general":           "General monthly review",
        "statut_objectifs":        "Previous objectives status",
        "statut_objectifs_detail": "Objectives status detail",
        "was_lief_gut":            "What went well?",
        "wo_brauche_ich":          "Where do I need support?",
        "themen_naechster_termin": "Topics for next appointment",
        "sonstige_anmerkungen":    "Additional remarks",
    },
    "signature": {
        "title":       "Monthly Review - Signatures",
        "datum":       "Date: .............................",
        "left_label":  "Participant:",
        "right_label": "                              Advisor:",
        "left_line":   "_________________________________",
        "right_line":  "       _________________________________",
    },
}


# ---------------------------------------------------------------------------
# Core build function
# ---------------------------------------------------------------------------

def build_template(output_path, strings):
    """
    Build a single .docx template with all 118 Content Controls.

    Structure:
    - Cover page  : 6 SDTs  (COVER_TAGS)
    - Profil      : 4 SDTs  (PROFIL_TAGS)
    - Bilans 01-12: 9 SDTs each = 108 SDTs
    Total         : 118 SDTs
    """
    doc = Document()

    # Page setup: A4, 2.5 cm margins
    section = doc.sections[0]
    section.page_width  = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(2.5)
    section.right_margin  = Cm(2.5)

    # Default paragraph font
    doc.styles['Normal'].font.name = 'Calibri'
    doc.styles['Normal'].font.size = Pt(11)

    # ---- Cover page ----
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run(strings["doc_title_fixed"])
    title_run.bold = True
    title_run.font.size = Pt(24)
    title_run.font.color.rgb = RGBColor(0x00, 0x3D, 0xA5)

    doc.add_paragraph()  # spacer

    # Cover Content Controls - each preceded by a label paragraph
    cover_labels = strings["cover_labels"]
    for tag in COVER_TAGS:
        add_label_paragraph(doc, cover_labels[tag] + ":")
        if tag == "doc_titre":
            placeholder = strings["doc_titre_placeholder"]
        else:
            placeholder = ""
        append_sdt(doc, tag, placeholder)
        doc.add_paragraph()  # spacer

    conf_p = doc.add_paragraph(strings["confidential"])
    conf_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # ---- Section 1 : Profil ----
    add_heading(doc, strings["section_profil_heading"], level=1)
    add_heading(doc, strings["section_profil_sub"], level=2)
    doc.add_paragraph()

    profil_labels = strings["profil_labels"]
    for tag in PROFIL_TAGS:
        add_label_paragraph(doc, profil_labels[tag] + ":")
        append_sdt(doc, tag, "")
        doc.add_paragraph()

    doc.add_page_break()

    # ---- Sections Bilans 01 to 12 ----
    bilan_labels = strings["bilan_labels"]
    sig = strings["signature"]

    for nn in range(1, 13):
        prefix = f"bilan_{nn:02d}_"

        add_heading(doc, strings["bilan_heading"].format(nn=nn), level=1)
        doc.add_paragraph()

        for field in BILAN_FIELDS:
            tag = prefix + field
            add_label_paragraph(doc, bilan_labels[field] + ":")
            append_sdt(doc, tag, "")
            doc.add_paragraph()

        # Fixed signature block (not a Content Control)
        add_signature_block(doc, sig)

        if nn < 12:
            doc.add_page_break()

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Saved: {output_path}")


# ---------------------------------------------------------------------------
# Verification helper
# ---------------------------------------------------------------------------

def verify_template(path, expected_count=118):
    """
    Count <w:tag w:val="..."> occurrences in the document XML and report.
    Each unique tag value should appear exactly once.
    """
    import zipfile
    import re

    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml').decode('utf-8')

    # Match w:val attributes on w:tag elements specifically
    # Pattern: <w:tag w:val="something"/>
    tags = re.findall(r'<w:tag\s+w:val="([^"]+)"', xml)

    duplicates = [t for t in set(tags) if tags.count(t) > 1]
    missing_cover = [t for t in COVER_TAGS if t not in tags]
    missing_profil = [t for t in PROFIL_TAGS if t not in tags]

    missing_bilans = []
    for nn in range(1, 13):
        for field in BILAN_FIELDS:
            tag = f"bilan_{nn:02d}_{field}"
            if tag not in tags:
                missing_bilans.append(tag)

    print(f"\nVerification: {path}")
    print(f"  Content Controls found : {len(tags)}")
    print(f"  Expected               : {expected_count}")
    print(f"  OK                     : {len(tags) == expected_count}")
    if duplicates:
        print(f"  WARN duplicates        : {duplicates}")
    if missing_cover:
        print(f"  MISSING cover tags     : {missing_cover}")
    if missing_profil:
        print(f"  MISSING profil tags    : {missing_profil}")
    if missing_bilans:
        print(f"  MISSING bilan tags     : {missing_bilans}")
    if not duplicates and not missing_cover and not missing_profil and not missing_bilans:
        print("  All 118 tag values present and unique.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))

    de_path = os.path.join(base, "transfer_mappe_template_de.docx")
    en_path = os.path.join(base, "transfer_mappe_template_en.docx")

    print("Building DE template...")
    build_template(de_path, DE_STRINGS)

    print("Building EN template...")
    build_template(en_path, EN_STRINGS)

    print("\nRunning verification...")
    verify_template(de_path)
    verify_template(en_path)

    print("\nDone. Open the .docx files in Word to inspect Content Controls.")
    print("In Word: Developer tab > Design Mode to see all SDTs highlighted.")
