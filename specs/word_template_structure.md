# Word Template Structure - Transfer Mappe v0.1

Vollständige Spezifikation des Word-Templates für die Generierung des kumulativen PDFs.
Dieses Dokument ist die Referenz für:
- Den manuellen Aufbau der .docx-Datei in Microsoft Word
- Die Erstellung der Content Controls mit ihren Tag-Werten
- Die Konfiguration der Aktion "Populate a Microsoft Word template" in Power Automate

---

## Technischer Kontext

Power Automate (Plan E3, ohne Premium) verwendet die native Aktion **"Populate a Microsoft Word template"** des Connectors Word Online (Business). Diese Aktion ersetzt die Content Controls des Templates durch die einzufügenden Werte.

**Kompatibilitätseinschränkungen**:
- Nur Content Controls vom Typ **Plain Text** (`<w:sdt>` mit `<w:tag w:val="..."/>`) werden von dieser Aktion unterstützt
- Content Controls vom Typ Rich Text, Image, Date Picker oder Dropdown werden von Power Automate NICHT befüllt
- Der Tag-Wert (`w:val`) ist der Bezeichner, den Power Automate für die Zuordnung verwendet: er muss im Dokument eindeutig und exakt identisch mit dem im Flow konfigurierten Feldnamen sein
- Die Monatsbericht-Abschnitte (1- bis 12-mal wiederholt) verwenden den Schleifenmechanismus: Jede Berichtsinstanz wird in einen eigenen Content Control eingefügt (bilan_01_, bilan_02_ usw.)

---

## Allgemeine Dokumentstruktur

```
[Deckblatt]
  - Dokumenttitel
  - Vor- und Nachname des Teilnehmers
  - Beginn des Begleitungsprozesses
  - Zuständige Beraterin
  - Datum der PDF-Generierung

[Abschnitt 1: Karriereprofil]
  - Plan A
  - Plan B
  - Marketingplan
  - Zielmarkt
  - (Abschnitt wird auch bei leerem Inhalt angezeigt, mit Hinweis "Nicht angegeben")

[Abschnitt 2: Zielvereinbarung - Bericht 01]
  - Datum des Termins
  - Allgemeiner Monatsbericht
  - Zielstatus
  - Zielstatus - Erläuterung
  - Was lief gut
  - Wo brauche ich Unterstützung
  - Themen nächster Termin
  - Sonstige Anmerkungen
  - [Unterschriftenblock - leerer handschriftlicher Bereich]

[Abschnitt 3: Zielvereinbarung - Bericht 02]
  ... (gleiche Struktur)

[...]

[Abschnitt 13: Zielvereinbarung - Bericht 12]
  ... (gleiche Struktur)

[Globale Fußzeile]
  - Vertraulichkeitshinweis
  - Seitenzahl / Gesamtzahl
```

---

## Vollständiges Inventar der Content Controls

### Deckblatt

| Tag-Wert (w:val)          | Typ        | SharePoint-Quelle                        | Wert wenn leer            |
|---------------------------|------------|------------------------------------------|---------------------------|
| `doc_titre`               | Plain Text | Fest (DE: "Transfer Mappe", EN: "Transfer Portfolio") | - |
| `participant_prenom`      | Plain Text | `Participants.prenom`                    | -                         |
| `participant_nom`         | Plain Text | `Participants.nom`                       | -                         |
| `participant_date_debut`  | Plain Text | `Participants.date_debut_parcours` (TT.MM.JJJJ) | -                  |
| `conseillere_nom`         | Plain Text | Abgeleitet von `Participants.id_conseillere` (M365-Anzeigename) | - |
| `doc_date_generation`     | Plain Text | Aktuelles Datum zum Zeitpunkt des Flow-Auslösers (TT.MM.JJJJ) | - |

---

### Abschnitt Karriereprofil

| Tag-Wert (w:val)          | Typ        | SharePoint-Quelle                        | Wert wenn leer               |
|---------------------------|------------|------------------------------------------|------------------------------|
| `profil_plan_a`           | Plain Text | `Profils.plan_a`                         | DE: "Nicht angegeben" / EN: "Not provided" |
| `profil_plan_b`           | Plain Text | `Profils.plan_b`                         | DE: "Nicht angegeben" / EN: "Not provided" |
| `profil_marketingplan`    | Plain Text | `Profils.marketingplan`                  | DE: "Nicht angegeben" / EN: "Not provided" |
| `profil_zielmarkt`        | Plain Text | `Profils.zielmarkt`                      | DE: "Nicht angegeben" / EN: "Not provided" |

---

### Abschnitte Monatsbericht (12-mal wiederholt)

Das Präfix `bilan_NN_`, wobei `NN` von `01` bis `12` geht, identifiziert jeden Bericht im Dokument.
Power Automate fügt die Berichte in aufsteigend chronologischer Reihenfolge ein (`date_rdv` ASC).
Abschnitte für noch nicht eingereichte Berichte werden leer gelassen oder ausgeblendet (siehe Hinweis unten).

**Beispiel für Bericht 01:**

| Tag-Wert (w:val)                    | Typ        | SharePoint-Quelle                              | Wert wenn leer / nicht eingereicht |
|-------------------------------------|------------|------------------------------------------------|------------------------------------|
| `bilan_01_date_rdv`                 | Plain Text | `BilansMensuels.date_rdv` (TT.MM.JJJJ)        | Leer lassen                        |
| `bilan_01_date_soumission`          | Plain Text | `BilansMensuels.date_soumission` (TT.MM.JJJJ) | Leer lassen                        |
| `bilan_01_bilan_general`            | Plain Text | `BilansMensuels.bilan_general`                | Leer lassen                        |
| `bilan_01_statut_objectifs`         | Plain Text | `BilansMensuels.statut_objectifs` (übersetztes Label) | Leer lassen              |
| `bilan_01_statut_objectifs_detail`  | Plain Text | `BilansMensuels.statut_objectifs_detail`      | Leer lassen                        |
| `bilan_01_was_lief_gut`             | Plain Text | `BilansMensuels.was_lief_gut`                 | Leer lassen                        |
| `bilan_01_wo_brauche_ich`           | Plain Text | `BilansMensuels.wo_brauche_ich_unterstuetzung`| Leer lassen                        | Hinweis: Tag-Wert bewusst abgekürzt (max. 64 Zeichen empfohlen für Power Automate); der Flow stellt die Zuordnung sicher |
| `bilan_01_themen_naechster_termin`  | Plain Text | `BilansMensuels.themen_naechster_termin`      | Leer lassen                        |
| `bilan_01_sonstige_anmerkungen`     | Plain Text | `BilansMensuels.sonstige_anmerkungen`         | Leer lassen                        |

**Gleiche Struktur für Berichte 02 bis 12** (`01` durch `02`, `03`, ..., `12` ersetzen).

**Vollständige Liste aller Tag-Werte der Berichte:**

```
bilan_01_date_rdv               bilan_07_date_rdv
bilan_01_date_soumission        bilan_07_date_soumission
bilan_01_bilan_general          bilan_07_bilan_general
bilan_01_statut_objectifs       bilan_07_statut_objectifs
bilan_01_statut_objectifs_detail bilan_07_statut_objectifs_detail
bilan_01_was_lief_gut           bilan_07_was_lief_gut
bilan_01_wo_brauche_ich         bilan_07_wo_brauche_ich
bilan_01_themen_naechster_termin bilan_07_themen_naechster_termin
bilan_01_sonstige_anmerkungen   bilan_07_sonstige_anmerkungen

bilan_02_date_rdv               bilan_08_date_rdv
bilan_02_date_soumission        bilan_08_date_soumission
bilan_02_bilan_general          bilan_08_bilan_general
bilan_02_statut_objectifs       bilan_08_statut_objectifs
bilan_02_statut_objectifs_detail bilan_08_statut_objectifs_detail
bilan_02_was_lief_gut           bilan_08_was_lief_gut
bilan_02_wo_brauche_ich         bilan_08_wo_brauche_ich
bilan_02_themen_naechster_termin bilan_08_themen_naechster_termin
bilan_02_sonstige_anmerkungen   bilan_08_sonstige_anmerkungen

bilan_03_date_rdv               bilan_09_date_rdv
bilan_03_date_soumission        bilan_09_date_soumission
bilan_03_bilan_general          bilan_09_bilan_general
bilan_03_statut_objectifs       bilan_09_statut_objectifs
bilan_03_statut_objectifs_detail bilan_09_statut_objectifs_detail
bilan_03_was_lief_gut           bilan_09_was_lief_gut
bilan_03_wo_brauche_ich         bilan_09_wo_brauche_ich
bilan_03_themen_naechster_termin bilan_09_themen_naechster_termin
bilan_03_sonstige_anmerkungen   bilan_09_sonstige_anmerkungen

bilan_04_date_rdv               bilan_10_date_rdv
bilan_04_date_soumission        bilan_10_date_soumission
bilan_04_bilan_general          bilan_10_bilan_general
bilan_04_statut_objectifs       bilan_10_statut_objectifs
bilan_04_statut_objectifs_detail bilan_10_statut_objectifs_detail
bilan_04_was_lief_gut           bilan_10_was_lief_gut
bilan_04_wo_brauche_ich         bilan_10_wo_brauche_ich
bilan_04_themen_naechster_termin bilan_10_themen_naechster_termin
bilan_04_sonstige_anmerkungen   bilan_10_sonstige_anmerkungen

bilan_05_date_rdv               bilan_11_date_rdv
bilan_05_date_soumission        bilan_11_date_soumission
bilan_05_bilan_general          bilan_11_bilan_general
bilan_05_statut_objectifs       bilan_11_statut_objectifs
bilan_05_statut_objectifs_detail bilan_11_statut_objectifs_detail
bilan_05_was_lief_gut           bilan_11_was_lief_gut
bilan_05_wo_brauche_ich         bilan_11_wo_brauche_ich
bilan_05_themen_naechster_termin bilan_11_themen_naechster_termin
bilan_05_sonstige_anmerkungen   bilan_11_sonstige_anmerkungen

bilan_06_date_rdv               bilan_12_date_rdv
bilan_06_date_soumission        bilan_12_date_soumission
bilan_06_bilan_general          bilan_12_bilan_general
bilan_06_statut_objectifs       bilan_12_statut_objectifs
bilan_06_statut_objectifs_detail bilan_12_statut_objectifs_detail
bilan_06_was_lief_gut           bilan_12_was_lief_gut
bilan_06_wo_brauche_ich         bilan_12_wo_brauche_ich
bilan_06_themen_naechster_termin bilan_12_themen_naechster_termin
bilan_06_sonstige_anmerkungen   bilan_12_sonstige_anmerkungen
```

**Gesamt Content Controls**: 6 (Deckblatt) + 4 (Profil) + 108 (12 x 9 Berichte) = **118 Content Controls**

---

### Unterschriftenblock (in jedem Berichtsabschnitt)

Der Unterschriftenblock ist KEIN von Power Automate befüllter Content Control. Es handelt sich um einen festen Bereich des Word-Templates, der auf jeder Berichtsseite vorhanden ist.

**Blockstruktur (am Ende jedes Berichtsabschnitts, im Template):**

```
Zielvereinbarung - Unterschriften

Datum: .......................

Teilnehmer/in:                          Beraterin:

_________________________________       _________________________________
{{participant_prenom}} {{participant_nom}}   {{conseillere_nom}}
```

Hinweis: Die Unterschriftenlinien werden mit einer Absatzunterkante (Word-Rahmen) gezeichnet, nicht mit Unterstrichen als Klartext. Die Namen werden über Content Controls eingefügt (`participant_prenom`, `participant_nom`, `conseillere_nom` - dieselben wie auf dem Deckblatt, im Dokument mehrfach referenzierbar).

---

## Zuordnung statut_objectifs -> angezeigtes Label im PDF

Der Flow übersetzt den internen SharePoint-Code in ein lesbares Label, bevor er ihn in den Content Control einfügt.

| SharePoint-Code              | Label DE                  | Label EN                  |
|------------------------------|---------------------------|---------------------------|
| `vollstaendig_erreicht`      | Vollständig erreicht      | Fully achieved            |
| `teilweise_erreicht`         | Teilweise erreicht        | Partially achieved        |
| `nicht_erreicht`             | Nicht erreicht            | Not achieved              |
| `noch_nicht_relevant`        | Noch nicht relevant       | Not yet relevant          |
| (leer, nicht eingereicht)    | -                         | -                         |

---

## Anleitung zur Erstellung der .docx-Datei in Microsoft Word

### Schritt 1: Datei erstellen

1. Word öffnen, neues leeres Dokument
2. Seiteneinrichtung: A4, Seitenränder 2,5 cm an allen Seiten
3. Formatvorlagen definieren:
   - "Heading 1": Calibri 18pt, fett, Farbe #003DA5 (Corporate-Blau)
   - "Heading 2": Calibri 14pt, fett, Farbe #003DA5
   - "Normal": Calibri 11pt, Farbe #333333, Zeilenabstand 1,15
   - "SignatureLine": benutzerdefinierte Formatvorlage, keine Aufzählungszeichen, Unterkante 0,5pt #666666

### Schritt 2: Content Controls einfügen

Für jeden Content Control:
1. Menüband > Entwickler > Steuerelemente > "Nur-Text-Inhaltssteuerelement" (Aa) auswählen
2. Auf "Eigenschaften" (Schlüsselsymbol) klicken
3. Folgendes eingeben:
   - **Titel**: lesbares Label (z.B. "Monatsbericht - Monat 01")
   - **Tag**: exakter Tag-Wert (z.B. `bilan_01_bilan_general`)
4. "Inhaltssteuerelement entfernen, wenn Inhalt bearbeitet wird" aktivieren: NEIN
5. Formatvorlage: standardmäßig "Normal"

### Schritt 3: Registerkarte Entwickler aktivieren (falls nicht sichtbar)

Datei > Optionen > Menüband anpassen > "Entwickler" aktivieren

### Schritt 4: Im Format .docx speichern

Datei > Speichern unter > Format: "Word-Dokument (.docx)"
NICHT als .doc (altes Format) oder .dotx (Word-Vorlage) speichern - Power Automate erfordert eine Standard-.docx-Datei.

### Schritt 5: Datei in SharePoint ablegen

Das Template muss in einer SharePoint-Dokumentbibliothek gespeichert werden, die für das Power Automate-Dienstkonto zugänglich ist (z.B. /sites/TransferMappe/Templates/transfer_mappe_template_de.docx).

---

## XML-Referenzstruktur eines Content Controls (Auszug)

Dieser XML-Auszug zeigt die erwartete Struktur im .docx-Dokument. Er dient als Referenz für die Validierung oder die programmatische Erstellung.

```xml
<w:sdt>
  <w:sdtPr>
    <w:tag w:val="bilan_01_bilan_general"/>
    <w:alias w:val="Bilan general - Mois 01"/>
    <w:showingPlcHdr/>
    <w:text/>
  </w:sdtPr>
  <w:sdtContent>
    <w:p>
      <w:r>
        <w:rPr>
          <w:rStyle w:val="PlaceholderText"/>
        </w:rPr>
        <w:t>Bilan general du mois</w:t>
      </w:r>
    </w:p>
  </w:sdtContent>
</w:sdt>
```

---

## Wichtige Hinweise für Power Automate

1. **Zu verwendende Aktion**: "Populate a Microsoft Word template" des Connectors "Word Online (Business)"
2. **Template-Pfad**: auf die .docx-Datei in SharePoint zeigen (nicht OneDrive)
3. **Dynamische Felder**: Power Automate erkennt automatisch alle Content Controls des Templates und schlägt ihre Tag-Werte als auszufüllende Felder in der Aktion vor
4. **Leere Felder**: Ist ein Feld nicht ausgefüllt (Bericht nicht eingereicht, leeres Profil), eine leere Zeichenkette `""` einfügen - das Feld darf in der Power Automate-Aktion niemals fehlen
5. **PDF-Konvertierung**: nach der Aktion "Populate" die Aktion "Convert Word Document to PDF" desselben Connectors Word Online (Business) verwenden - in E3 ohne Premium verfügbar
6. **Reihenfolge der Berichte**: Berichte vor der Einspielschleife in Power Automate nach `date_rdv` ASC sortieren
