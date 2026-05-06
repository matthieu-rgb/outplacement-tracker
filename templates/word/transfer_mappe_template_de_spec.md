# Transfer Mappe Template DE - Konstruktionsspezifikation

Diese Datei dokumentiert exakt den Inhalt und das Layout des deutschen Word-Templates
`transfer_mappe_template_de.docx`, das manuell in Microsoft Word erstellt werden muss.

Die vollstaendige Liste der Content Controls und Tag-Werte befindet sich in:
`specs/word_template_structure.md`

Die Konstruktionsanweisungen fuer Word befinden sich im Abschnitt
"Instructions de construction du .docx" in `specs/word_template_structure.md`.

---

## Metadaten der Datei

- **Dateiname** : `transfer_mappe_template_de.docx`
- **Format** : Office Open XML (.docx), Word 2016 oder hoeher
- **Dokumentsprache** : Deutsch (de-DE)
- **Seiteneinrichtung** : A4 Hochformat, Raender 2,5 cm
- **Ablageort in SharePoint** : `/sites/TransferMappe/Templates/transfer_mappe_template_de.docx`

---

## Deckblatt

**Inhalt (von oben nach unten) :**

```
[Firmenlogo - Bild wird manuell vom Administrator eingefuegt]
[Vertikaler Abstand]

TRANSFER MAPPE
[Content Control : doc_titre - Plain Text]

[Horizontale Linie blau #003DA5, Staerke 2pt]

Teilnehmer/in :    [Content Control : participant_prenom] [Content Control : participant_nom]
Beraterin :        [Content Control : conseillere_nom]
Beginn :           [Content Control : participant_date_debut]
Erstellt am :      [Content Control : doc_date_generation]

[Vertikaler Abstand]
[Fusszeile Deckblatt - Vertraulichkeitshinweis]
Vertraulich - Nur fuer den internen Gebrauch
```

**Verwendete Formatvorlagen :**
- "TRANSFER MAPPE" : Heading 1, zentriert, 24pt, #003DA5, Grossbuchstaben
- Bezeichner ("Teilnehmer/in :", usw.) : Normal, fett
- Werte (Content Controls) : Normal, nicht fett

---

## Abschnitt 1 : Karriereprofil

**Abschnittstitel :** `1. Karriereprofil` (Heading 1)

**Untertitel :** `Berufliche Zielsetzung` (Heading 2)

**Inhalt :**

```
Plan A - Berufliches Hauptziel
[Content Control : profil_plan_a]

Plan B - Berufliches Alternativziel
[Content Control : profil_plan_b]

Berufliches Profil und Stärken (Marketingplan)
[Content Control : profil_marketingplan]

Zielmarkt
[Content Control : profil_zielmarkt]
```

**Verhalten bei nicht ausgefuelltem Profil :**
Der Flow schreibt "Nicht angegeben" in jeden leeren Content Control.
Der Abschnitt bleibt im PDF sichtbar.

**Seitenumbruch** nach dem Abschnitt Karriereprofil.

---

## Abschnitte 2 bis 13 : Monatsberichte (Bilans mensuels 01 bis 12)

Jeder Abschnitt hat dieselbe Struktur. `NN` ist durch `01`, `02`, ..., `12` zu ersetzen.

**Abschnittstitel :** `Monatsbericht NN` (Heading 1)

**Inhalt :**

```
Termin :           [Content Control : bilan_NN_date_rdv]
Eingereicht am :   [Content Control : bilan_NN_date_soumission]

Monatlicher Rückblick *
[Content Control : bilan_NN_bilan_general]

Stand der vereinbarten Ziele
[Content Control : bilan_NN_statut_objectifs]
[Content Control : bilan_NN_statut_objectifs_detail]

Was lief gut?
[Content Control : bilan_NN_was_lief_gut]

Wo brauche ich Unterstützung?
[Content Control : bilan_NN_wo_brauche_ich]

Themen für den nächsten Termin
[Content Control : bilan_NN_themen_naechster_termin]

Sonstige Anmerkungen
[Content Control : bilan_NN_sonstige_anmerkungen]
```

**Block Zielvereinbarung / Unterschriften (fester Bereich, kein Content Control) :**

```
[Horizontale Linie grau #cccccc]

Zielvereinbarung - Unterschriften

Datum : .............................

Teilnehmer/in :                             Beraterin :

_________________________________           _________________________________
[Content Control : participant_prenom]      [Content Control : conseillere_nom]
[Content Control : participant_nom]
```

Hinweis: Die Unterschriftenlinien sind Absatzrahmen (unten), keine Unterstrich-Zeichen.
Hinweis: `participant_prenom`, `participant_nom`, `conseillere_nom` sind dieselben Content Controls wie auf dem Deckblatt. Word erlaubt mehrere Instanzen desselben Tag-Werts in einem Dokument - alle werden von Power Automate mit demselben Wert befuellt.

**Seitenumbruch** nach jedem Monatsbericht-Abschnitt (ausser dem letzten).

---

## Globale Fusszeile (alle Seiten ausser Deckblatt)

```
Transfer Mappe | [Content Control : participant_prenom] [Content Control : participant_nom] | Vertraulich
                                                                              Seite X von Y
```

Hinweis: Die Seitenzahl (X von Y) ist ein natives Word-Feld (`{ PAGE }` und `{ NUMPAGES }`), kein Content Control.

---

## Formatvorlagen

| Element                           | Schrift     | Groesse | Farbe    | Gewicht | Ausrichtung |
|-----------------------------------|-------------|---------|----------|---------|-------------|
| Haupttitel (Deckblatt)            | Calibri     | 24pt    | #003DA5  | Fett    | Zentriert   |
| Heading 1 (Abschnittstitel)       | Calibri     | 16pt    | #003DA5  | Fett    | Links       |
| Heading 2 (Untertitel)            | Calibri     | 13pt    | #003DA5  | Fett    | Links       |
| Feldbezeichner                    | Calibri     | 11pt    | #333333  | Fett    | Links       |
| Inhalt (Content Controls)         | Calibri     | 11pt    | #333333  | Normal  | Links       |
| Unterschriftentext                | Calibri     | 10pt    | #666666  | Normal  | Links       |
| Fusszeile                         | Calibri     | 9pt     | #999999  | Normal  | Blocksatz   |

**Akzentfarbe** : #003DA5 (Corporate-Blau, identisch mit der Transfer Mappe 10k Beratung)
**Haupttextfarbe** : #333333 (Dunkelgrau, vermeidet reines Schwarz fuer bessere Lesbarkeit)

---

## Pruefcheckliste vor dem Hochladen in SharePoint

- [ ] Alle 118 Content Controls sind vorhanden (6 Deckblatt + 4 Profil + 108 Monatsberichte)
- [ ] Jeder Content Control ist vom Typ "Plain Text" (nicht Rich Text, nicht Date Picker)
- [ ] Jeder Tag-Wert entspricht exakt der Liste in `specs/word_template_structure.md`
- [ ] Das Dokument oeffnet sich ohne Fehler in Word Online (Test ueber SharePoint)
- [ ] Die Aktion "Populate a Microsoft Word template" in Power Automate erkennt alle Felder
- [ ] Ein Testlauf mit fiktiven Daten erzeugt ein lesbares PDF
- [ ] Die Unterschriftenblocks sind sichtbar und korrekt am Ende jedes Monatsberichts platziert
