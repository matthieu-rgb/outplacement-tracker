# Transfer Mappe Template EN - Construction Specification

This file documents the exact content and layout of the English Word template
`transfer_mappe_template_en.docx` to be built manually in Microsoft Word.

For the exhaustive list of Content Controls and Tag values, see:
`specs/word_template_structure.md`

For Word construction instructions, see the section
"Instructions de construction du .docx" in `specs/word_template_structure.md`.

This is a 1:1 translation of `transfer_mappe_template_de_spec.md`.
All Tag values (Content Control tags) are IDENTICAL to the DE template.
Only the visible text (labels, headings, static content) is translated.

---

## File metadata

- **Filename** : `transfer_mappe_template_en.docx`
- **Format** : Office Open XML (.docx), Word 2016 or later
- **Document language** : English (en-GB)
- **Page setup** : A4 portrait, 2.5 cm margins
- **SharePoint storage path** : `/sites/TransferMappe/Templates/transfer_mappe_template_en.docx`

---

## Cover page

**Content (top to bottom) :**

```
[Company logo - image placed manually by the administrator]
[Vertical space]

TRANSFER PORTFOLIO
[Content Control : doc_titre - Plain Text]

[Horizontal rule, blue #003DA5, 2pt]

Participant :      [Content Control : participant_prenom] [Content Control : participant_nom]
Advisor :          [Content Control : conseillere_nom]
Start date :       [Content Control : participant_date_debut]
Generated on :     [Content Control : doc_date_generation]

[Vertical space]
[Cover page footer - confidentiality notice]
Confidential - For internal use only
```

**Styles applied :**
- "TRANSFER PORTFOLIO" : Heading 1, centred, 24pt, #003DA5, uppercase
- Labels ("Participant:", etc.) : Normal, bold
- Values (Content Controls) : Normal, not bold

---

## Section 1 : Career Profile

**Section heading :** `1. Career Profile` (Heading 1)

**Sub-heading :** `Professional Objectives` (Heading 2)

**Content :**

```
Plan A - Primary Career Goal
[Content Control : profil_plan_a]

Plan B - Alternative Career Goal
[Content Control : profil_plan_b]

Professional Profile and Strengths (Marketing Plan)
[Content Control : profil_marketingplan]

Target Market
[Content Control : profil_zielmarkt]
```

**Behaviour when profile not completed :**
The Flow injects "Not provided" into each empty Content Control.
The section remains visible in the PDF.

**Page break** after the Career Profile section.

---

## Sections 2 to 13 : Monthly Updates (bilans 01 to 12)

Each section is identical in structure. Replace `NN` with `01`, `02`, ..., `12`.

**Section heading :** `Monthly Update NN` (Heading 1)

**Content :**

```
Appointment date :   [Content Control : bilan_NN_date_rdv]
Submitted on :       [Content Control : bilan_NN_date_soumission]

Monthly Review *
[Content Control : bilan_NN_bilan_general]

Status of agreed objectives
[Content Control : bilan_NN_statut_objectifs]
[Content Control : bilan_NN_statut_objectifs_detail]

What went well?
[Content Control : bilan_NN_was_lief_gut]

Where do I need support?
[Content Control : bilan_NN_wo_brauche_ich]

Topics for the next session
[Content Control : bilan_NN_themen_naechster_termin]

Additional remarks
[Content Control : bilan_NN_sonstige_anmerkungen]
```

**Zielvereinbarung / Signature block (fixed zone, no Content Control) :**

```
[Horizontal rule, grey #cccccc]

Objective Agreement - Signatures

Date : .............................

Participant :                               Advisor :

_________________________________           _________________________________
[Content Control : participant_prenom]      [Content Control : conseillere_nom]
[Content Control : participant_nom]
```

Note : signature lines are paragraph borders (bottom border), not underscore characters.
Note : `participant_prenom`, `participant_nom`, `conseillere_nom` are the same Content Controls as on the cover page. Word allows multiple instances of the same Tag value - all will be populated with the same value by Power Automate.

**Page break** after each monthly section (except the last one).

---

## Global footer (all pages except cover page)

```
Transfer Portfolio | [Content Control : participant_prenom] [Content Control : participant_nom] | Confidential
                                                                                    Page X of Y
```

Note : page number (X of Y) is a native Word field (`{ PAGE }` and `{ NUMPAGES }`), not a Content Control.

---

## Formatting styles

| Element                        | Font        | Size | Colour   | Weight | Alignment  |
|--------------------------------|-------------|------|----------|--------|------------|
| Main title (cover page)        | Calibri     | 24pt | #003DA5  | Bold   | Centred    |
| Heading 1 (section titles)     | Calibri     | 16pt | #003DA5  | Bold   | Left       |
| Heading 2 (sub-headings)       | Calibri     | 13pt | #003DA5  | Bold   | Left       |
| Field labels                   | Calibri     | 11pt | #333333  | Bold   | Left       |
| Content (Content Controls)     | Calibri     | 11pt | #333333  | Normal | Left       |
| Signature text                 | Calibri     | 10pt | #666666  | Normal | Left       |
| Footer                         | Calibri     | 9pt  | #999999  | Normal | Justified  |

**Accent colour** : #003DA5 (corporate blue, consistent with DE template and 10k Beratung Transfer Mappe)
**Main text colour** : #333333 (dark grey, avoids pure black for readability)

---

## Validation checklist before uploading to SharePoint

- [ ] All 118 Content Controls are present (6 cover page + 4 profile + 108 monthly updates)
- [ ] Each Content Control is of type "Plain Text" (not Rich Text, not Date Picker)
- [ ] Each Tag value matches exactly the list in `specs/word_template_structure.md`
- [ ] The document opens without errors in Word Online (test via SharePoint)
- [ ] The "Populate a Microsoft Word template" action in Power Automate detects all fields
- [ ] A test generation with fictional data produces a readable PDF
- [ ] Signature blocks are visible and correctly placed at the bottom of each monthly section
