# Installationsanleitung - outplacement-tracker v0.1

Schritt-fur-Schritt-Anleitung zur Bereitstellung fur einen Microsoft 365-Administrator.
Geschatzte Dauer: 1 bis 2 Stunden.

---

## Voraussetzungen

### Tenant und Lizenzen

- Microsoft 365-Tenant mit **E3-Plan oder hoher**
  - Erforderlich fur: Word Online (Business), Power Automate (im Lieferumfang enthalten), Exchange Online
  - Es werden keine Premium-Connectoren fur Power Automate verwendet
- Mindestens ein Konto mit den folgenden Rollen:
  - SharePoint-Administrator (zum Erstellen der Website und der Listen)
  - Exchange-Administrator (zum Konfigurieren des freigegebenen Postfachs)
  - Dediziertes Dienstkonto fur Power Automate-Flows (empfohlen: nicht-nominatives Konto, z. B. `service-transfermappe@{domain}`)

### Erforderliche Tools auf dem Administratorrechner

- **PowerShell 7+**: [https://github.com/PowerShell/PowerShell/releases](https://github.com/PowerShell/PowerShell/releases)
- **Modul PnP.PowerShell** (einmalige Installation):

```powershell
Install-Module PnP.PowerShell -Force -Scope CurrentUser
```

- Moderner Browser mit Zugriff auf `https://admin.microsoft.com`, `https://make.powerautomate.com`, `https://forms.microsoft.com`

### Arbeitsverzeichnis

Kit auf dem Administratorrechner klonen oder herunterladen:

```
/pfad/zum/outplacement-tracker/
  sharepoint/
    setup_lists.ps1
    lists_schema.json
  templates/word/
    transfer_mappe_template_de.docx
    transfer_mappe_template_en.docx
  forms/
    forms_construction_guide.md
  power_automate/
    Flow_1_Invitation_J-5.md
    Flow_2_Generation_PDF.md
```

---

## Schritt 1 - SharePoint-Website erstellen

### 1.1 Website erstellen

1. `https://{tenant}-admin.sharepoint.com` aufrufen (SharePoint Admin Center)
2. Auf **Aktive Websites** > **Erstellen** > **Teamwebsite** klicken
3. Folgende Angaben ausfullen:
   - Websitename: `TransferMappe`
   - Websiteadresse: `transfermappe` (resultierende URL: `https://{tenant}.sharepoint.com/sites/transfermappe`)
   - Websitebesitzer: das Administratorkonto und das Power Automate-Dienstkonto
   - Sprache: nach Bedarf (hat keinen Einfluss auf die Daten)
   - Datenschutzeinstellungen: **Privat** (Teilnehmer haben keinen Zugriff)
4. Auf **Fertig stellen** klicken

Die URL der Website (im Folgenden `SiteUrl` genannt) lautet: `https://{tenant}.sharepoint.com/sites/transfermappe`

### 1.2 Berechtigungen konfigurieren

Auf der erstellten Website zu **Einstellungen** > **Websiteberechtigungen** navigieren:

| Konto | SharePoint-Rolle |
|---|---|
| Bereitstellungsadministrator | Besitzer (Site Collection Admin) |
| Power Automate-Dienstkonto | Mitglied (Lesen + Schreiben auf Listen und Bibliotheken) |
| Beraterinnen | Mitglied (Lesen der Listen, Empfang der PDFs) |
| Teilnehmer | Kein Zugriff auf die Website |

---

## Schritt 2 - Bereitstellung der SharePoint-Listen

### 2.1 PowerShell 7 offnen und verbinden

```powershell
Connect-PnPOnline -Url "https://{tenant}.sharepoint.com/sites/transfermappe" -Interactive
```

Ein Anmeldefenster offnet sich. Das M365-Administratorkonto verwenden. Die von PnP.PowerShell angeforderten Berechtigungen bestatigen (nur bei der ersten Verbindung).

### 2.2 Bereitstellungsskript ausfuhren

```powershell
# Aus dem Kit-Verzeichnis
.\sharepoint\setup_lists.ps1 -SiteUrl "https://{tenant}.sharepoint.com/sites/transfermappe"
```

Das Skript ist **idempotent**: Es kann ohne Fehler erneut ausgefuhrt werden, auch wenn die Listen bereits vorhanden sind. Die Konsole zeigt an, was erstellt und was ubersprungen wird.

### 2.3 Ergebnis pruefen

Nach Abschluss des Skripts muss die Konsole folgendes ausgeben:

```
[OK] Participants - N Spalten sichtbar
[OK] Profils - N Spalten sichtbar
[OK] BilansMensuels - N Spalten sichtbar
```

Im Browser `https://{tenant}.sharepoint.com/sites/transfermappe` aufrufen > **Websiteinhalt** und prufen, ob die 3 Listen vorhanden sind.

### 2.4 Struktur der erstellten Listen

**Liste Participants** (zentrale Tabelle, eine Zeile pro Teilnehmer):

| Spalte | Typ | Erforderlich | Hinweis |
|---|---|---|---|
| Title | Text | Ja | Format: `{Vorname} {Nachname}` |
| nom | Text | Ja | |
| prenom | Text | Ja | |
| email | Text | Ja | E-Mail des Teilnehmers |
| langue | Choice | Ja | DE oder EN, Standard: DE |
| id_conseillere | Text | Ja | M365-E-Mail der Beraterin |
| date_debut_parcours | DateTime (DateOnly) | Ja | |
| date_prochain_rdv | DateTime (DateOnly) | Ja | Nach jedem Termin aktualisiert |
| statut | Choice | Ja | actif / suspendu / termine |

**Liste Profils** (optionales Karriereprofil, null oder eine Zeile pro Teilnehmer):

| Spalte | Typ | Erforderlich |
|---|---|---|
| id_participant | Number | Ja |
| plan_a | Note (multiline) | Nein |
| plan_b | Note (multiline) | Nein |
| marketingplan | Note (multiline) | Nein |
| zielmarkt | Note (multiline) | Nein |
| date_creation | DateTime | Ja |
| date_modification | DateTime | Nein |

**Liste BilansMensuels** (null bis zwolf Monatsberichte pro Teilnehmer):

| Spalte | Typ | Erforderlich |
|---|---|---|
| id_participant | Number | Ja |
| date_rdv | DateTime (DateOnly) | Ja |
| date_soumission | DateTime | Ja |
| bilan_general | Note (multiline) | Ja |
| statut_objectifs | Choice | Nein |
| statut_objectifs_detail | Note (multiline) | Nein |
| was_lief_gut | Note (multiline) | Nein |
| wo_brauche_ich_unterstuetzung | Note (multiline) | Nein |
| themen_naechster_termin | Note (multiline) | Nein |
| sonstige_anmerkungen | Note (multiline) | Nein |

---

## Schritt 3 - Dokumentbibliothek erstellen

Die Bibliothek speichert die generierten PDFs und die Word-Vorlagen.

1. Auf der SharePoint-Website auf **Neu** > **Dokumentbibliothek** klicken
2. Name: `TransferMappes`
3. Auf **Erstellen** klicken
4. In der Bibliothek `TransferMappes` auf **Neu** > **Ordner** klicken
5. Ordnername: `Templates`

Erwartete Struktur in SharePoint:

```
/sites/transfermappe/TransferMappes/
  Templates/       <- Word-Vorlagen
  Nachname_Vorname/  <- wird automatisch vom Flow bei der ersten Generierung erstellt
```

---

## Schritt 4 - Word-Vorlagen hochladen

1. In der SharePoint-Bibliothek zu `TransferMappes/Templates/` navigieren
2. Auf **Hochladen** > **Dateien** klicken
3. Die beiden Dateien aus dem Kit auswahlen:
   - `templates/word/transfer_mappe_template_de.docx`
   - `templates/word/transfer_mappe_template_en.docx`
4. Prufen, ob beide Dateien im Ordner `Templates` sichtbar sind

Resultierende SharePoint-Pfade (werden in Flow 2 verwendet):

```
/sites/transfermappe/TransferMappes/Templates/transfer_mappe_template_de.docx
/sites/transfermappe/TransferMappes/Templates/transfer_mappe_template_en.docx
```

Prufen, ob das Power Automate-Dienstkonto diese Dateien offnen kann (Mitgliedszugriff auf die Bibliothek).

---

## Schritt 5 - Microsoft Forms-Formulare erstellen

Die detaillierte Anleitung befolgen: `forms/forms_construction_guide.md`

Die 4 Formulare werden auf dem Dienstkonto (oder dem freigegebenen Postfach) erstellt, nicht auf einem nominativen Konto.

### 5.1 Bei Microsoft Forms anmelden

`https://forms.microsoft.com` mit dem Dienstkonto aufrufen.

### 5.2 Die 4 Formulare in der angegebenen Reihenfolge erstellen

| # | Titel | Sprache | Verwendung |
|---|---|---|---|
| 1 | Ihr Karriereprofil - Transfer Mappe | DE | Onboarding (einmalig) |
| 2 | Your Career Profile - Transfer Mappe | EN | Onboarding (einmalig) |
| 3 | Ihr monatlicher Bericht - Transfer Mappe | DE | Monatsbericht |
| 4 | Your Monthly Update - Transfer Mappe | EN | Monatsbericht |

Fur jedes Formular die detaillierte Vorgehensweise in `forms/forms_construction_guide.md` befolgen (Fragenstruktur, genaue Texte, Bestatitigungsmeldungen).

### 5.3 Konfiguration nach der Erstellung (gilt fur alle 4 Formulare)

In den **Einstellungen** jedes Formulars:

- **Teilen**: "Jeder mit dem Link kann antworten" auswahlen. Nicht auf M365-Konten einschranken (Teilnehmer haben kein M365-Konto).
- **Namensaufzeichnung**: "Record name" deaktivieren (Datensparsamkeit gemass DSGVO).
- **Mehrfachantworten**: "Eine Antwort pro Person" nicht aktivieren (der Flow sendet bei jedem Termin einen Link).

### 5.4 URLs der Formulare 3 und 4 abrufen

Nur fur Formulare 3 und 4 (Monatsberichte):

1. Das Formular offnen
2. Auf **Teilen** > **Link kopieren** klicken
3. Diese beiden URLs aufbewahren: Sie werden in den Flow-Variablen verwendet

Beispiel fur das URL-Format von Forms:
```
https://forms.office.com/r/XXXXXXXXXX
```

Die Formulare 1 und 2 (Onboarding) werden nicht von den Flows verwendet. Ihr Link wird zu Beginn des Beratungsprozesses manuell von der Beraterin mitgeteilt.

---

## Schritt 6 - Einladungsflow J-5 erstellen

Die detaillierte Anleitung befolgen: `power_automate/Flow_1_Invitation_J-5.md`

### 6.1 Voraussetzungen vor der Erstellung des Flows

- Das sendende freigegebene Postfach muss konfiguriert sein (siehe Schritt 8)
- Die URLs der Formulare 3 und 4 mussen verfugbar sein (siehe Schritt 5.4)

### 6.2 Flow erstellen

1. `https://make.powerautomate.com` mit dem Dienstkonto aufrufen
2. Auf **Erstellen** > **Geplanter Flow** klicken
3. Name: `TransferMappe - Invitation J-5`
4. Startzeit: `07:00`, Wiederholen alle: `1 Tag`
5. Die Aktionen in der in `Flow_1_Invitation_J-5.md` definierten Reihenfolge erstellen

### 6.3 Pflichtangaben fur Variablen

In den Aktionen "Variable initialisieren" am Anfang des Flows:

| Variable | Einzutragender Wert |
|---|---|
| `varSiteUrl` | `https://{tenant}.sharepoint.com/sites/transfermappe` |
| `varSharedMailbox` | Adresse des freigegebenen Postfachs (z. B. `transfer@{domain}.de`) |
| `varFormUrlDE` | URL von Formular 3 (Monatsbericht DE) |
| `varFormUrlEN` | URL von Formular 4 (Monatsbericht EN) |

### 6.4 Fehlerbehandlung konfigurieren

Die Aktion `Notifier_erreur` ausserhalb der Schleife hinzufugen, mit **Ausfuhren nach: Fehler**.
Die E-Mail-Adresse des Administrators als Empfanger eintragen.

### 6.5 Flow speichern und aktivieren

Auf **Speichern** klicken und prufen, ob der Flow den Status **Aktiv** hat.

---

## Schritt 7 - PDF-Generierungsflow erstellen

Die detaillierte Anleitung befolgen: `power_automate/Flow_2_Generation_PDF.md`

### 7.1 Voraussetzungen vor der Erstellung des Flows

- Die Word-Vorlagen mussen in SharePoint hochgeladen worden sein (siehe Schritt 4)
- Die Bibliothek `TransferMappes` muss vorhanden sein (siehe Schritt 3)

### 7.2 Flow erstellen

1. `https://make.powerautomate.com` aufrufen
2. Auf **Erstellen** > **Geplanter Flow** klicken
3. Name: `TransferMappe - Generation PDF`
4. Startzeit: `06:00`, Wiederholen alle: `1 Tag`
5. Die Aktionen in der in `Flow_2_Generation_PDF.md` definierten Reihenfolge erstellen

Der PDF-Generierungsflow wird um 06:00 Uhr ausgefuhrt, eine Stunde vor dem Einladungsflow (07:00 Uhr), um Kollisionen zu vermeiden.

### 7.3 Pflichtangaben fur Variablen

| Variable | Einzutragender Wert |
|---|---|
| `varSiteUrl` | `https://{tenant}.sharepoint.com/sites/transfermappe` |
| `varSharedMailbox` | Adresse des freigegebenen Postfachs |
| `varTemplatePathDE` | `/sites/transfermappe/TransferMappes/Templates/transfer_mappe_template_de.docx` |
| `varTemplatePathEN` | `/sites/transfermappe/TransferMappes/Templates/transfer_mappe_template_en.docx` |

### 7.4 Die 118 Content Controls befulllen

Die Aktion "Vorlage in Microsoft Word auffulllen" erfordert die vollstandige Zuordnung aller 118 Content Controls. Die vollstandige Tabelle befindet sich in `power_automate/Flow_2_Generation_PDF.md`, Abschnitt "Mapping des Content Controls".

Kein Feld in dieser Aktion leer lassen: fur nicht vorhandene Monatsberichte `""` einsetzen.

### 7.5 Flow speichern und aktivieren

Auf **Speichern** klicken und prufen, ob der Flow den Status **Aktiv** hat.

---

## Schritt 8 - Freigegebenes Postfach konfigurieren

### 8.1 Freigegebenes Postfach erstellen (sofern noch nicht vorhanden)

1. `https://admin.microsoft.com` aufrufen > **Exchange** > **Empfanger** > **Freigegebene Postfacher**
2. Auf **Freigegebenes Postfach hinzufugen** klicken
3. Anzeigename: `Transfer Mappe`
4. E-Mail-Adresse: `transfer@{domain}.de` (oder gemas interner Konvention)
5. Auf **Speichern** klicken

### 8.2 Dem Dienstkonto die Berechtigung "Senden als" erteilen

1. Im Exchange Admin Center das freigegebene Postfach `transfer@{domain}.de` offnen
2. Auf die Registerkarte **Delegierung** klicken
3. Unter **Senden als (Send As)** auf **Bearbeiten** klicken
4. Das Power Automate-Dienstkonto hinzufugen
5. Speichern

5 bis 15 Minuten warten, bis die Berechtigung ubernommen wurde, bevor der Test durchgefuhrt wird.

### 8.3 Prufen

Auf `https://outlook.office.com` mit dem Dienstkonto prufen, ob das freigegebene Postfach in der Postfachliste erscheint. Andernfalls manuell hinzufugen: **Einstellungen** > **Weiteres Postfach offnen**.

---

## Schritt 9 - Test mit einem fiktiven Teilnehmer

Dieser Schritt validiert das vollstandige Funktionieren von Anfang bis Ende vor der Inbetriebnahme.

### 9.1 Testteilnehmer erstellen

In der SharePoint-Liste `Participants` auf **Neues Element** klicken und folgendes ausfulllen:

| Spalte | Wert |
|---|---|
| Title | `Test Testperson` |
| nom | `Testperson` |
| prenom | `Test` |
| email | Ihre personliche E-Mail-Adresse (um die Test-E-Mail zu empfangen) |
| langue | `DE` |
| id_conseillere | Ihre E-Mail-Adresse (um das PDF zu empfangen) |
| date_debut_parcours | Heutiges Datum minus 1 Monat |
| date_prochain_rdv | Heutiges Datum plus 5 Tage |
| statut | `actif` |

### 9.2 Einladungsflow J-5 testen

1. In Power Automate `TransferMappe - Invitation J-5` offnen
2. Auf **Ausfuhren** (manuelle Ausfuhrung) klicken
3. Im Posteingang prufen, ob die Einladungs-E-Mail empfangen wurde
4. Auf den Link in der E-Mail klicken, um zu bestatigen, dass das richtige Forms-Formular geoffnet wird

### 9.3 Testmonatsbericht erstellen

In der SharePoint-Liste `BilansMensuels` auf **Neues Element** klicken und folgendes ausfulllen:

| Spalte | Wert |
|---|---|
| Title | `2026-05-01 - Test Testperson` |
| id_participant | `{SharePoint-ID des Testteilnehmers}` |
| date_rdv | Heutiges Datum |
| date_soumission | Heutiges Datum |
| bilan_general | `Testbericht - zu loschen` |

Die SharePoint-ID des Teilnehmers ist in der URL beim Bearbeiten des Elements sichtbar (Parameter `ID=...`).

### 9.4 Termindatum anpassen und PDF-Generierungsflow testen

1. In der Liste Participants den Testteilnehmer bearbeiten: `date_prochain_rdv` = heute
2. In Power Automate `TransferMappe - Generation PDF` offnen
3. Auf **Ausfuhren** (manuelle Ausfuhrung) klicken
4. Folgendes prufen:
   - Die E-Mail mit dem PDF als Anhang wird von der Testberaterin empfangen
   - Das PDF wird in `TransferMappes/Testperson_Test/` gespeichert
   - Das PDF ist lesbar und enthalt die Daten des Testberichts

### 9.5 Ausfuhrungsprotokolle prufen

In Power Automate jeden Flow offnen und den **Ausfuhrungsverlauf** aufrufen (letzte 28 Tage). Eine erfolgreiche Ausfuhrung zeigt den Status "Erfolgreich" in Grun. Bei einem Fehler auf die Ausfuhrung klicken, um die Details der fehlerhaften Aktion anzuzeigen.

### 9.6 Nach dem Test bereinigen

In SharePoint folgendes loschen:
- Den Eintrag aus der Liste `Participants` (Testteilnehmer)
- Den Eintrag aus der Liste `BilansMensuels` (Testbericht)
- Den Ordner `TransferMappes/Testperson_Test/` und seinen Inhalt

---

## Schritt 10 - Bereinigung und Inbetriebnahme

### 10.1 Abschlusspruefungen vor der Freigabe

- [ ] Beide Flows haben den Status "Aktiv"
- [ ] Das freigegebene Postfach sendet korrekt (Test in Schritt 9 erfolgreich)
- [ ] Die Word-Vorlagen sind fur das Dienstkonto zuganglich
- [ ] Die 4 Forms-Formulare sind offentlich zuganglich (Link ohne erforderliches Konto)
- [ ] Die Testdaten wurden aus den 3 SharePoint-Listen geloscht

### 10.2 Echte Teilnehmer anlegen

In der SharePoint-Liste `Participants` einen Datensatz pro Teilnehmer erstellen.
Das Feld `date_prochain_rdv` muss ausgefullt sein, damit die Flows ausgefuhrt werden.

### 10.3 Links der Onboarding-Formulare verteilen

Die Beraterinnen teilen den Teilnehmern zu Beginn des Beratungsprozesses manuell den Link zu Formular 1 (DE) oder Formular 2 (EN) mit. Diese Formulare werden nicht automatisch von den Flows versendet.

### 10.4 Die ersten Produktionstage uberwachen

Den **Ausfuhrungsverlauf** beider Flows in Power Automate an den ersten 3 Werktagen prufen. Bei einem Fehler wird automatisch eine Benachrichtigungs-E-Mail an den Administrator gesendet (Aktion `Notifier_erreur`, konfiguriert in Schritt 6.4 und 7.5).

---

## Konfigurationsvariablen

Zusammenfassung aller anzupassenden Werte. In einem internen, sicheren Dokument aufbewahren.

| Variable | Einzutragender Wert | Verwendung |
|---|---|---|
| `{tenant}` | Bezeichner des M365-Tenants (z. B. `contoso`) | Alle SharePoint- und Admin-URLs |
| `{domain}` | E-Mail-Domain der Organisation (z. B. `contoso.de`) | E-Mail-Adressen, freigegebenes Postfach |
| `SiteUrl` | Vollstandige URL der Website (z. B. `https://contoso.sharepoint.com/sites/transfermappe`) | PowerShell-Skript, Flow-Variablen |
| `varSharedMailbox` | Absenderadresse (z. B. `transfer@contoso.de`) | Flow 1 und Flow 2 |
| `varFormUrlDE` | URL von Formular 3 - Monatsbericht DE | Flow 1 |
| `varFormUrlEN` | URL von Formular 4 - Monatsbericht EN | Flow 1 |
| `varTemplatePathDE` | `/sites/transfermappe/TransferMappes/Templates/transfer_mappe_template_de.docx` | Flow 2 |
| `varTemplatePathEN` | `/sites/transfermappe/TransferMappes/Templates/transfer_mappe_template_en.docx` | Flow 2 |
| Fehlerbenachrichtigungsadresse | E-Mail des Administrators (Empfanger der Warnmeldungen) | Flow 1 und Flow 2 |
| Dienstkonto | E-Mail des Power Automate-Dienstkontos | Power Automate-Verbindungen, Senden als |

---

## Fehlerbehebung

### Das PnP-Skript schlagt mit "Access Denied" fehl

**Ursache**: Das PowerShell-Konto ist kein Site Collection Administrator auf der Website.

**Losung**: Im SharePoint Admin Center zu **Aktive Websites** navigieren > die TransferMappe-Website auswahlen > **Mitgliedschaft** > das Konto als Besitzer hinzufugen.

---

### Das PnP-Skript schlagt mit "The remote server returned an error: (403)" fehl

**Ursache**: Das Modul PnP.PowerShell verwendet eine mit den Tenant-Einstellungen inkompatible Authentifizierungsversion (MFA, Conditional Access).

**Losung**: Sicherstellen, dass `-Interactive` als Verbindungsmethode verwendet wird. Prufen, ob die Conditional Access-Richtlinien des Tenants Drittanbieteranwendungen auf dem Administratorrechner erlauben.

---

### Der Einladungsflow J-5 findet keinen Teilnehmer, obwohl das Datum ubereinstimmt

**Ursache**: Der OData-Filter auf `date_prochain_rdv` kann fehlschlagen, wenn die Spalte einen DateTime-Wert mit Uhrzeit speichert (auch `T00:00:00Z`).

**Losung**: In der Aktion `Get_participants_J5` den OData-Filter ersetzen durch:

```
statut eq 'actif' and date_prochain_rdv ge '@{outputs('Calculer_date_cible')}T00:00:00Z' and date_prochain_rdv lt '@{outputs('Calculer_date_cible')}T23:59:59Z'
```

---

### Der PDF-Generierungsflow schlagt bei der Aktion "Vorlage in Microsoft Word auffulllen" fehl

**Mogliche Ursachen und Losungen**:

1. **Vorlagendatei nicht gefunden**: Den genauen Pfad in `varTemplatePathDE` / `varTemplatePathEN` prufen. Der Pfad ist Gross-/Kleinschreibung-sensitiv und darf nicht die Website-URL als Prafix enthalten.

2. **Datei von einem anderen Benutzer geoffnet**: Die Aktion schlagt fehl, wenn die .docx-Datei gerade in Word Online bearbeitet wird. Sicherstellen, dass niemand die Datei wahrend der Flow-Ausfuhrung bearbeitet.

3. **Content Control fehlt**: Wenn ein Tag-Wert in der .docx-Datei nicht genau dem in der Power Automate-Aktion eingetragenen Feld entspricht, schlagt der Flow fehl. Die genaue Ubereinstimmung der Tag-Werte prufen (vollstandige Liste in `specs/word_template_structure.md`).

4. **Leeres Feld in der Aktion**: Alle 118 Felder mussen ausgefullt sein. Fur nicht vorhandene Monatsberichte `""` einsetzen, anstatt das Feld leer zu lassen.

---

### Das freigegebene Postfach kann nicht senden (Fehler "Senden als" verweigert)

**Ursache**: Die Berechtigung "Senden als" wurde noch nicht ubernommen, oder das Dienstkonto befindet sich nicht in der Liste.

**Losung**:
1. Im Exchange Admin Center prufen, ob das Dienstkonto korrekt in der Delegierung "Senden als" des freigegebenen Postfachs eingetragen ist
2. 15 Minuten fur die Ubernahme warten
3. Falls das Problem weiterhin besteht, die Berechtigung loschen und erneut hinzufugen

---

### Das PDF wird generiert, ist aber leer oder enthalt nicht ausgefullte Felder

**Ursache**: Content Controls in der .docx-Vorlage haben Tag-Werte, die nicht genau mit den Power Automate-Ausdrucken ubereinstimmen.

**Losung**: Die .docx-Datei in Word offnen, die Anzeige der Content Controls aktivieren (Entwickler > Entwurfsmodus) und die Tag-Werte jedes Content Controls prufen. Mit der Liste in `specs/word_template_structure.md` vergleichen.

---

### Der Flow uberschreitet die Ausfuhrungszeitgrenze bei einer grossen Anzahl von Teilnehmern

**Kontext**: Power Automate verarbeitet Elemente in einer "Apply to each"-Schleife standardmasig sequenziell. Bei 100 Teilnehmern kann der PDF-Generierungsflow 20 bis 30 Minuten dauern.

**Losung**: Parallelverarbeitung fur die Hauptschleife aktivieren:
1. In der Schleife "Pour_chaque_participant_rdv" auf die drei Punkte > **Einstellungen** klicken
2. **Parallelitatssteuerung** aktivieren, auf 10 bis 20 einstellen (50 nicht uberschreiten)
3. Achtung: Bei aktivierter Parallelitat schleifenlokale Variablen verwenden, keine globalen Variablen

---

### Ein Teilnehmer erhalt die Einladung in der falschen Sprache

**Ursache**: Die Spalte `langue` dieses Datensatzes in der Liste Participants ist nicht korrekt ausgefullt.

**Losung**: In der SharePoint-Liste `Participants` den Wert der Spalte `langue` fur diesen Teilnehmer prufen. Der Wert muss genau `DE` oder `EN` lauten (Grossbuchstaben, kein Leerzeichen).
