# Flow 2 : PDF-Generierung am Tag des Termins

outplacement-tracker v0.1 - Implementierungsanleitung (Blueprint ohne Tenant)

Dieses Dokument ermoeglicht einem Microsoft 365-Administrator, diesen Flow
von Grund auf neu zu erstellen, Aktion fuer Aktion, ohne JSON-Import.

---

## Uebersicht

| Parameter | Wert |
|---|---|
| Name des Flows | TransferMappe - Generation PDF |
| Ausloeseer | Geplant (taeglich um 06:00 Uhr) |
| Funktion | Fuer jeden aktiven Teilnehmer mit Termin heute : Profil und Berichte abrufen, Word-Vorlage befuellen, in PDF konvertieren, an die Beraterin senden, in SharePoint speichern |
| Haeufigkeit | Taeglich |
| Erforderliche Verbindungen | SharePoint, Word Online (Business), Office 365 Outlook |

Der Flow wird 1 Stunde vor dem J-5-Flow ausgeloest (06:00 Uhr vs. 07:00 Uhr), um Konflikte zu vermeiden.

---

## Schritt 1 : Flow erstellen

1. Auf make.powerautomate.com gehen
2. "Erstellen" > "Geplanter Cloud-Flow" anklicken
3. Folgendes eingeben :
   - Name : `TransferMappe - Generation PDF`
   - Startzeit : `06:00`
   - Wiederholen alle : `1 Tag`
4. "Erstellen" anklicken

---

## Schritt 2 : Konfigurationsvariablen

Am Anfang des Flows 4 Aktionen "Variable initialisieren" hinzufuegen.

| Variablenname | Typ | Anfangswert | Beschreibung |
|---|---|---|---|
| varSiteUrl | String | `https://{tenant}.sharepoint.com/sites/TransferMappe` | URL der SharePoint-Website |
| varSharedMailbox | String | `transfer@{domaine}.de` | Absenderadresse |
| varTemplatePathDE | String | `/sites/TransferMappe/TransferMappes/Templates/transfer_mappe_template_de.docx` | SharePoint-Pfad der Word-Vorlage DE |
| varTemplatePathEN | String | `/sites/TransferMappe/TransferMappes/Templates/transfer_mappe_template_en.docx` | SharePoint-Pfad der Word-Vorlage EN |

---

## Schritt 3 : Heutiges Datum berechnen

- Aktion : **Verfassen** (Datenvorgaenge > Verfassen)
- Name der Aktion : `Datum_heute`
- Eingaben (Ausdruck) :

```
formatDateTime(utcNow(), 'yyyy-MM-dd')
```

---

## Schritt 4 : Aktive Teilnehmer mit heutigem Termin abrufen

- Aktion : **Elemente abrufen** (SharePoint)
- Name der Aktion : `Get_participants_rdv_auj`
- Website : `variables('varSiteUrl')`
- Listenname : `Participants`
- Abfrage filtern :

```
statut eq 'actif' and date_prochain_rdv eq '@{outputs('Datum_heute')}'
```

- Maximale Anzahl von Elementen : `100`

---

## Schritt 5 : Fuer jeden Teilnehmer (Hauptschleife)

- Aktion : **Auf jedes anwenden**
- Name der Aktion : `Fuer_jeden_Teilnehmer_Termin`
- Eingabe : `value` von `Get_participants_rdv_auj`

### Aktion 5.1 : Profil des Teilnehmers abrufen

- Aktion : **Elemente abrufen** (SharePoint)
- Name der Aktion : `Get_profil`
- Website : `variables('varSiteUrl')`
- Listenname : `Profils`
- Abfrage filtern :

```
id_participant eq @{items('Fuer_jeden_Teilnehmer_Termin')?['ID']}
```

- Maximale Anzahl von Elementen : `1`

Hinweis : `ID` ist die von SharePoint automatisch generierte ID-Spalte (Ganzzahl). Nicht mit `id_participant` verwechseln.

### Aktion 5.2 : Alle Berichte des Teilnehmers abrufen (aufsteigend nach Datum sortiert)

- Aktion : **Elemente abrufen** (SharePoint)
- Name der Aktion : `Get_bilans`
- Website : `variables('varSiteUrl')`
- Listenname : `BilansMensuels`
- Abfrage filtern :

```
id_participant eq @{items('Fuer_jeden_Teilnehmer_Termin')?['ID']}
```

- Sortieren nach : `date_rdv` - Aufsteigend (ASC)
- Maximale Anzahl von Elementen : `12`

### Aktion 5.3 : Vorlagenpfad gemaess Sprache auswaehlen

- Aktion : **Bedingung**
- Name der Aktion : `Bedingung_Sprache_PDF`
- Bedingung : `items('Fuer_jeden_Teilnehmer_Termin')?['langue']` ist gleich `EN`
- Zweig "Wenn ja" : Variable `varTemplatePath` = `variables('varTemplatePathEN')` initialisieren
- Zweig "Wenn nein" : Variable `varTemplatePath` = `variables('varTemplatePathDE')` initialisieren

Hinweis : `varTemplatePath` als leeren String in Schritt 2 deklarieren, bevor sie hier zugewiesen wird.

### Aktion 5.4 : Word-Vorlage befuellen (Populate a Microsoft Word template)

- Aktion : **Microsoft Word-Vorlage auffuellen** (Word Online (Business))
- Name der Aktion : `Vorlage_befuellen`
- Speicherort : `SharePoint`
- Dokumentbibliothek : `Documents` (oder den Namen Ihrer Bibliothek verwenden)
- Datei : `variables('varTemplatePath')`

#### Zuordnung der Content Controls

Jede Zeile entspricht einem Feld in der Power Automate-Aktion.
Die Spalte "Ausdruck" enthaelt den dynamischen Ausdruck, der in das entsprechende Feld einzutragen ist.

**Deckblatt (6 Content Controls)**

| Content Control (Tag-Wert) | Power Automate-Ausdruck |
|---|---|
| `doc_titre` | `if(equals(items('Fuer_jeden_Teilnehmer_Termin')?['langue'], 'EN'), 'Transfer Portfolio', 'Transfer Mappe')` |
| `participant_prenom` | `items('Fuer_jeden_Teilnehmer_Termin')?['prenom']` |
| `participant_nom` | `items('Fuer_jeden_Teilnehmer_Termin')?['nom']` |
| `participant_date_debut` | `formatDateTime(items('Fuer_jeden_Teilnehmer_Termin')?['date_debut_parcours'], 'dd.MM.yyyy')` |
| `conseillere_nom` | `items('Fuer_jeden_Teilnehmer_Termin')?['id_conseillere']` |
| `doc_date_generation` | `formatDateTime(utcNow(), 'dd.MM.yyyy')` |

**Abschnitt Profil (4 Content Controls)**

Der Wert "Nicht angegeben" / "Not provided" wird eingefuegt, wenn das Feld leer ist.

| Content Control (Tag-Wert) | Power Automate-Ausdruck |
|---|---|
| `profil_plan_a` | `if(equals(length(body('Get_profil')?['value']), 0), if(equals(items('Fuer_jeden_Teilnehmer_Termin')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben'), coalesce(body('Get_profil')?['value'][0]?['plan_a'], if(equals(items('Fuer_jeden_Teilnehmer_Termin')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben')))` |
| `profil_plan_b` | `if(equals(length(body('Get_profil')?['value']), 0), if(equals(items('Fuer_jeden_Teilnehmer_Termin')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben'), coalesce(body('Get_profil')?['value'][0]?['plan_b'], if(equals(items('Fuer_jeden_Teilnehmer_Termin')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben')))` |
| `profil_marketingplan` | `if(equals(length(body('Get_profil')?['value']), 0), if(equals(items('Fuer_jeden_Teilnehmer_Termin')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben'), coalesce(body('Get_profil')?['value'][0]?['marketingplan'], if(equals(items('Fuer_jeden_Teilnehmer_Termin')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben')))` |
| `profil_zielmarkt` | `if(equals(length(body('Get_profil')?['value']), 0), if(equals(items('Fuer_jeden_Teilnehmer_Termin')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben'), coalesce(body('Get_profil')?['value'][0]?['zielmarkt'], if(equals(items('Fuer_jeden_Teilnehmer_Termin')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben')))` |

**Zuordnung statut_objectifs -> lesbarer Anzeigetext**

Der interne SharePoint-Code wird in einen lesbaren Text uebersetzt. Die Funktion `switch` in einer vorangehenden Verfassen-Aktion verwenden oder direkt als Ausdruck im Feld eintragen :

```
if(equals(items('Fuer_jeden_Teilnehmer_Termin')?['langue'], 'EN'),
  switch(body('Get_bilans')?['value'][0]?['statut_objectifs'],
    'vollstaendig_erreicht', 'Fully achieved',
    'teilweise_erreicht', 'Partially achieved',
    'nicht_erreicht', 'Not achieved',
    'noch_nicht_relevant', 'Not yet relevant',
    ''),
  switch(body('Get_bilans')?['value'][0]?['statut_objectifs'],
    'vollstaendig_erreicht', 'Vollständig erreicht',
    'teilweise_erreicht', 'Teilweise erreicht',
    'nicht_erreicht', 'Nicht erreicht',
    'noch_nicht_relevant', 'Noch nicht relevant',
    ''))
```

Hinweis : `[0]` durch `[1]`, `[2]` usw. ersetzen, je nach Nummer des betreffenden Berichts.

**Abschnitte Bericht 01 bis 12 (9 Content Controls x 12 = 108)**

Das Muster ist fuer jeden Bericht identisch. `NN` durch `01` bis `12` ersetzen und `[N-1]` durch den entsprechenden Array-Index (Bericht 01 = Index 0, Bericht 12 = Index 11).

Wenn Bericht N nicht existiert (Array kuerzer als N), einen leeren String `""` einfuegen.

Muster fuer `bilan_NN_*` (Beispiel mit Bericht 01, Index 0) :

| Content Control | Ausdruck |
|---|---|
| `bilan_01_date_rdv` | `if(greater(length(body('Get_bilans')?['value']), 0), formatDateTime(body('Get_bilans')?['value'][0]?['date_rdv'], 'dd.MM.yyyy'), '')` |
| `bilan_01_date_soumission` | `if(greater(length(body('Get_bilans')?['value']), 0), formatDateTime(body('Get_bilans')?['value'][0]?['date_soumission'], 'dd.MM.yyyy'), '')` |
| `bilan_01_bilan_general` | `if(greater(length(body('Get_bilans')?['value']), 0), coalesce(body('Get_bilans')?['value'][0]?['bilan_general'], ''), '')` |
| `bilan_01_statut_objectifs` | `if(greater(length(body('Get_bilans')?['value']), 0), [switch-Ausdruck Sprache/Code oben mit Index 0], '')` |
| `bilan_01_statut_objectifs_detail` | `if(greater(length(body('Get_bilans')?['value']), 0), coalesce(body('Get_bilans')?['value'][0]?['statut_objectifs_detail'], ''), '')` |
| `bilan_01_was_lief_gut` | `if(greater(length(body('Get_bilans')?['value']), 0), coalesce(body('Get_bilans')?['value'][0]?['was_lief_gut'], ''), '')` |
| `bilan_01_wo_brauche_ich` | `if(greater(length(body('Get_bilans')?['value']), 0), coalesce(body('Get_bilans')?['value'][0]?['wo_brauche_ich_unterstuetzung'], ''), '')` |
| `bilan_01_themen_naechster_termin` | `if(greater(length(body('Get_bilans')?['value']), 0), coalesce(body('Get_bilans')?['value'][0]?['themen_naechster_termin'], ''), '')` |
| `bilan_01_sonstige_anmerkungen` | `if(greater(length(body('Get_bilans')?['value']), 0), coalesce(body('Get_bilans')?['value'][0]?['sonstige_anmerkungen'], ''), '')` |

Fuer Bericht 02 (Index 1) : `[0]` durch `[1]` und `greater(..., 0)` durch `greater(..., 1)` in jedem Ausdruck ersetzen.

Fuer Bericht 12 (Index 11) : `greater(length(body('Get_bilans')?['value']), 11)` und `[11]`.

**Uebersichtstabelle der Schwellenwerte je Bericht**

| Bericht | Array-Index | Pruefbedingung |
|---|---|---|
| 01 | 0 | `greater(length(body('Get_bilans')?['value']), 0)` |
| 02 | 1 | `greater(length(body('Get_bilans')?['value']), 1)` |
| 03 | 2 | `greater(length(body('Get_bilans')?['value']), 2)` |
| 04 | 3 | `greater(length(body('Get_bilans')?['value']), 3)` |
| 05 | 4 | `greater(length(body('Get_bilans')?['value']), 4)` |
| 06 | 5 | `greater(length(body('Get_bilans')?['value']), 5)` |
| 07 | 6 | `greater(length(body('Get_bilans')?['value']), 6)` |
| 08 | 7 | `greater(length(body('Get_bilans')?['value']), 7)` |
| 09 | 8 | `greater(length(body('Get_bilans')?['value']), 8)` |
| 10 | 9 | `greater(length(body('Get_bilans')?['value']), 9)` |
| 11 | 10 | `greater(length(body('Get_bilans')?['value']), 10)` |
| 12 | 11 | `greater(length(body('Get_bilans')?['value']), 11)` |

### Aktion 5.5 : Word-Dokument in PDF konvertieren

- Aktion : **Word-Dokument in PDF konvertieren** (Word Online (Business))
- Name der Aktion : `In_PDF_konvertieren`
- Eingabe : Ausgabe der Aktion `Vorlage_befuellen` (Dateiinhalt)

Hinweis : Diese Aktion ist im Connector Word Online (Business) verfuegbar, der in E3 enthalten ist.
Sie erfordert keine Power Automate Premium-Lizenz.

### Aktion 5.6 : PDF in SharePoint speichern

- Aktion : **Datei erstellen** (SharePoint > Datei erstellen)
- Name der Aktion : `PDF_speichern`
- Website : `variables('varSiteUrl')`
- Ordnerpfad : `/TransferMappes/@{items('Fuer_jeden_Teilnehmer_Termin')?['nom']}_@{items('Fuer_jeden_Teilnehmer_Termin')?['prenom']}/`
- Dateiname :

```
TransferMappe_@{items('Fuer_jeden_Teilnehmer_Termin')?['prenom']}_@{items('Fuer_jeden_Teilnehmer_Termin')?['nom']}_@{outputs('Datum_heute')}.pdf
```

- Dateiinhalt : Ausgabe des Texts der Aktion `In_PDF_konvertieren`

Hinweis : Die Dokumentbibliothek `TransferMappes` in SharePoint manuell anlegen,
bevor der Flow zum ersten Mal ausgefuehrt wird. Der Unterordner je Teilnehmer wird automatisch erstellt.

### Aktion 5.7 : PDF an die Beraterin senden

- Aktion : **E-Mail senden (V2)** (Office 365 Outlook)
- Name der Aktion : `PDF_an_Beraterin_senden`
- Von : `variables('varSharedMailbox')`
- An : `items('Fuer_jeden_Teilnehmer_Termin')?['id_conseillere']`

**Betreff (Vorlage DE, Standardwert) :**

```
Transfer Mappe - @{items('Fuer_jeden_Teilnehmer_Termin')?['prenom']} @{items('Fuer_jeden_Teilnehmer_Termin')?['nom']} - Termin heute @{formatDateTime(items('Fuer_jeden_Teilnehmer_Termin')?['date_prochain_rdv'], 'dd.MM.yyyy')}
```

**HTML-Inhalt (DE) :**

```html
<!DOCTYPE html>
<html lang="de">
<body style="font-family: Arial, sans-serif; font-size: 14px; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px;">

  <p>Guten Morgen,</p>

  <p>im Anhang finden Sie die aktuelle Transfer Mappe von
  <strong>@{items('Fuer_jeden_Teilnehmer_Termin')?['prenom']} @{items('Fuer_jeden_Teilnehmer_Termin')?['nom']}</strong>
  für den Beratungstermin heute, <strong>@{formatDateTime(items('Fuer_jeden_Teilnehmer_Termin')?['date_prochain_rdv'], 'dd.MM.yyyy')}</strong>.</p>

  <p>Das Dokument enthält:</p>
  <ul>
    <li>Das Karriereprofil des Teilnehmers (falls ausgefüllt)</li>
    <li>Alle bisher eingereichten Monatsberichte in chronologischer Reihenfolge</li>
    <li>Freie Unterschriftenfelder für die Zielvereinbarung</li>
  </ul>

  <p>Eine Kopie wurde in SharePoint gespeichert:<br>
    <a href="@{body('PDF_speichern')?['Path']}" style="color: #003DA5;">Zum Dokument in SharePoint</a>
  </p>

  <p>Mit freundlichen Grüßen,<br>Transfer Mappe System</p>

  <hr style="border: none; border-top: 1px solid #dddddd; margin: 30px 0;">
  <p style="font-size: 11px; color: #999999;">Diese E-Mail wurde automatisch generiert.</p>

</body>
</html>
```

**Anhang :**

- In der Aktion "E-Mail senden (V2)" auf "Erweiterte Optionen anzeigen" klicken
- Anlagen aktivieren
- Name : `TransferMappe_@{items('Fuer_jeden_Teilnehmer_Termin')?['prenom']}_@{items('Fuer_jeden_Teilnehmer_Termin')?['nom']}_@{outputs('Datum_heute')}.pdf`
- Inhalt : Ausgabe des Texts von `In_PDF_konvertieren`

---

## Schritt 6 : Fehlerbehandlung

Ausserhalb der Hauptschleife hinzufuegen :

- Aktion : **E-Mail senden (V2)**
- Name der Aktion : `Fehler_benachrichtigen_PDF`
- Run after : **fehlgeschlagen**
- An : Administrator-Adresse
- Betreff : `FEHLER - Flow TransferMappe Generation PDF`
- Inhalt :

```
Im Flow "TransferMappe - Generation PDF" ist ein Fehler aufgetreten.

Datum : @{utcNow()}

Die Power Automate-Ausfuehrungsprotokolle pruefen.
Ein oder mehrere Teilnehmer haben heute Morgen kein PDF erhalten.

Link : https://make.powerautomate.com
```

---

## Zusammenfassung der Flow-Aktionen (in Reihenfolge)

```
[Geplanter Ausloeseer - 06:00 taeglich]
  |
  +-- [Variable initialisieren] varSiteUrl
  +-- [Variable initialisieren] varSharedMailbox
  +-- [Variable initialisieren] varTemplatePathDE
  +-- [Variable initialisieren] varTemplatePathEN
  +-- [Variable initialisieren] varTemplatePath  (String, leer)
  +-- [Verfassen] Datum_heute  (formatDateTime utcNow yyyy-MM-dd)
  +-- [Elemente abrufen] Get_participants_rdv_auj  (Filter statut=actif AND date=heute)
  +-- [Auf jedes anwenden] Fuer_jeden_Teilnehmer_Termin
        |
        +-- [Elemente abrufen] Get_profil  (Filter id_participant)
        +-- [Elemente abrufen] Get_bilans  (Filter id_participant, Sortierung date_rdv ASC)
        +-- [Bedingung] Bedingung_Sprache_PDF  (langue == EN ?)
              +-- [Wenn ja] varTemplatePath = varTemplatePathEN
              +-- [Wenn nein] varTemplatePath = varTemplatePathDE
        +-- [Word-Vorlage auffuellen] Vorlage_befuellen  (118 Content Controls)
        +-- [Word in PDF konvertieren] In_PDF_konvertieren
        +-- [Datei erstellen] PDF_speichern  (SharePoint /TransferMappes/...)
        +-- [E-Mail senden] PDF_an_Beraterin_senden  (mit PDF-Anhang)
  |
  +-- [E-Mail senden] Fehler_benachrichtigen_PDF  (Run after: fehlgeschlagen)
```

---

## Hinweise und zu beachtende Punkte

- Pruefen, dass die Word-Vorlagen (.docx) in SharePoint unter dem Pfad
  `/sites/TransferMappe/TransferMappes/Templates/` abgelegt sind, bevor der Flow zum ersten Mal ausgefuehrt wird
- Die Aktion "Populate a Microsoft Word template" erfordert, dass alle 118 Content Controls
  belegt sind. Kein Feld in der Aktion leer lassen : `""` einfuegen, wenn ein Bericht nicht existiert
- Die Bibliothek `TransferMappes` muss in SharePoint vor der ersten Ausfuehrung vorhanden sein
- Die Adresse `id_conseillere` in der Teilnehmerliste ist die M365-E-Mail der Beraterin.
  Power Automate kann sie direkt als Empfaengeradresse verwenden
- Empfohlene maximale PDF-Groesse : 10 MB. Ein PDF mit 12 Monatsberichten in Textform bleibt
  deutlich unterhalb dieser Grenze
- Der Flow verarbeitet Teilnehmer sequenziell. Fuer 100 Teilnehmer pro Tag ist mit einer
  Ausfuehrungszeit von etwa 20 bis 30 Minuten zu rechnen
- Die Word-Vorlage (.docx) waehrend der Produktion nie aendern, ohne zuvor mit einem
  Testteilnehmer zu testen : jede Aenderung eines Tag-Werts erfordert eine Aktualisierung des Flows
