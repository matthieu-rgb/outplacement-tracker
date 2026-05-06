# Bereitstellungsanleitung - outplacement-tracker v0.1

Diese Anleitung beschreibt den vollstaendigen Bereitstellungsablauf der Loesung auf einem
Microsoft 365-Tenant. Sie koordiniert die uebrigen Anleitungen des Kits in der richtigen Reihenfolge.

Geschaetzter Zeitaufwand : 1 bis 2 Stunden fuer einen erfahrenen M365-Administrator.

---

## 1. Voraussetzungen

### 1.1 Tenant und Lizenzen

- Microsoft 365-Tenant mit Plan **E3 oder hoeher** (erforderlich fuer Word Online Business und
  den enthaltenen Power Automate)
- Mindestens ein Konto mit SharePoint- und Power Automate-Administratorrechten
- Kein Premium-Connector erforderlich (die Loesung verwendet ausschliesslich Standard-E3-Connectoren)

### 1.2 SharePoint-Website

Vor Beginn eine dedizierte SharePoint-Website erstellen :

1. Auf `https://{tenant}.sharepoint.com` gehen
2. "Website erstellen" > "Teamwebsite" (Team Site) anklicken
3. Name der Website : `TransferMappe` (oder der interne Name Ihrer Organisation)
4. Zugriff : auf Beraterinnen und den Administrator beschraenkt (Teilnehmer haben KEINEN Zugriff)
5. Resultierende URL : `https://{tenant}.sharepoint.com/sites/TransferMappe`

### 1.3 Modul PnP.PowerShell

Auf dem Administratorrechner (Windows, PowerShell 7+) :

```powershell
Install-Module PnP.PowerShell -Force -Scope CurrentUser
```

### 1.4 Erforderliche Berechtigungen

| Wer | Erforderliche Berechtigungen |
|---|---|
| Administrator-Konto Bereitstellung | Site Collection Administrator auf der Website TransferMappe |
| Power Automate-Dienstkonto | Mitglied der Website (Lese-/Schreibzugriff auf die Listen) |
| Beraterinnen | Mitglieder der Website (Listenzugriff lesen, PDF-Empfang) |
| Teilnehmer | Kein Zugriff auf die SharePoint-Website |

---

## 2. Schritt 1 : SharePoint-Bereitstellung

### 2.1 PnP-Skript ausfuehren

```powershell
cd {Pfad_zum_Kit}
.\sharepoint\setup_lists.ps1 -SiteUrl "https://{tenant}.sharepoint.com/sites/TransferMappe"
```

Das Skript :
- Erstellt die 3 Listen (Participants, Profils, BilansMensuels)
- Fuegt alle Spalten jeder Liste hinzu
- Aktiviert die Versionierung (5 Versionen)
- Zeigt eine Zusammenfassung an

Das Skript ist idempotent : es kann ohne Fehler erneut ausgefuehrt werden, wenn die Listen bereits vorhanden sind.

### 2.2 Ergebnis pruefen

Im Browser :
- Auf `https://{tenant}.sharepoint.com/sites/TransferMappe` gehen
- "Websiteinhalt" (Site contents) anklicken
- Pruefen, dass die 3 Listen vorhanden sind : Participants, Profils, BilansMensuels

### 2.3 Dokumentbibliothek fuer PDFs erstellen

1. Auf der SharePoint-Website "Neu" > "Dokumentbibliothek" anklicken
2. Name : `TransferMappes`
3. In dieser Bibliothek einen Ordner `Templates` erstellen
4. Endpfad : `/sites/TransferMappe/TransferMappes/Templates/`

---

## 3. Schritt 2 : Microsoft Forms-Formulare erstellen

Die detaillierte Anleitung befolgen : `forms/forms_construction_guide.md`

In dieser Reihenfolge erstellen :
1. Onboarding-Formular DE : "Ihr Karriereprofil - Transfer Mappe"
2. Onboarding-Formular EN : "Your Career Profile - Transfer Mappe"
3. Monatlicher Bericht DE : "Ihr monatlicher Bericht - Transfer Mappe"
4. Monatlicher Bericht EN : "Your Monthly Update - Transfer Mappe"

Nach der Erstellung die URLs von Formular 3 und Formular 4 (monatlicher Bericht DE und EN) notieren.
Diese URLs werden in den Flows verwendet.

---

## 4. Schritt 3 : Word-Vorlagen hochladen

1. In die SharePoint-Dokumentbibliothek gehen : `/sites/TransferMappe/TransferMappes/Templates/`
2. Die beiden Dateien aus dem Kit hochladen :
   - `templates/word/transfer_mappe_template_de.docx`
   - `templates/word/transfer_mappe_template_en.docx`
3. Pruefen, dass die Dateien fuer das Power Automate-Dienstkonto zugaenglich sind
4. Den genauen Pfad jeder Datei kopieren (wird in Flow 2 verwendet)

Erwarteter Pfad :
- DE : `/sites/TransferMappe/TransferMappes/Templates/transfer_mappe_template_de.docx`
- EN : `/sites/TransferMappe/TransferMappes/Templates/transfer_mappe_template_en.docx`

---

## 5. Schritt 4 : J-5-Flow erstellen (Einladung)

Die detaillierte Anleitung befolgen : `power_automate/Flow_1_Invitation_J-5.md`

Kritische Punkte :
- Das Shared Mailbox konfigurieren, bevor der Flow erstellt wird
- Die URLs von Formular 3 und 4 in die Variablen `varFormUrlDE` und `varFormUrlEN` eintragen
- Mit einem fiktiven Teilnehmer testen, bevor die Loesung in Produktion geht

---

## 6. Schritt 5 : PDF-Flow erstellen (Generierung)

Die detaillierte Anleitung befolgen : `power_automate/Flow_2_Generation_PDF.md`

Kritische Punkte :
- Pruefen, dass die Word-Vorlagen in SharePoint vorhanden sind (Schritt 3), bevor der Flow erstellt wird
- Die Vorlagenpfade in `varTemplatePathDE` und `varTemplatePathEN` eintragen
- Alle 118 Content Controls muessen in der Aktion "Populate" belegt sein
- Mit einem fiktiven Teilnehmer testen, der mindestens 1 Bericht hat

---

## 7. Schritt 6 : Test mit einem fiktiven Teilnehmer

### 7.1 Testteilnehmer erstellen

In der Liste Participants manuell einen Eintrag erstellen :

| Spalte | Testwert |
|---|---|
| nom | Testperson |
| prenom | Test |
| email | ihre.testadresse@{domaine} |
| langue | DE |
| id_conseillere | beraterin.test@{domaine} |
| date_debut_parcours | heutiges Datum - 1 Monat |
| date_prochain_rdv | heutiges Datum + 5 Tage (zum Testen von Flow J-5) |
| statut | actif |
| Title | Test Testperson |

### 7.2 Flow J-5 testen

1. In Power Automate gehen > Meine Flows > TransferMappe - Invitation J-5
2. Manuell "Ausfuehren" (Run) anklicken
3. Pruefen, dass die Einladungs-E-Mail auf der Testadresse eingeht
4. Den Formularverweis in der E-Mail pruefen

### 7.3 PDF-Flow testen

1. Den Testteilnehmer aendern : `date_prochain_rdv` = heute
2. Manuell einen Bericht in BilansMensuels erstellen (alle relevanten Spalten)
3. Den PDF-Flow manuell ausfuehren
4. Pruefen, dass das PDF bei der Test-Beraterin eingeht und in SharePoint gespeichert wird

### 7.4 Nach dem Test bereinigen

Den fiktiven Teilnehmer und seine Testdaten nach der Validierung loeschen.

---

## 8. Schritt 7 : In Produktion gehen

1. Den Testmodus in beiden Flows deaktivieren
2. Die echten Teilnehmer in der Liste Participants anlegen
3. Den Teilnehmern die Links zu den Onboarding-Formularen mitteilen
4. Die Flows am ersten Produktionstag pruefen (Ausfuehrungsprotokolle einsehen)

---

## 9. Globale Konfigurationsvariablen

Alle Werte, die fuer Ihre Organisation anzupassen sind.

| Variable | Einzutragender Wert | Verwendungsort |
|---|---|---|
| `{tenant}` | Bezeichner Ihres M365-Tenants (z.B. contoso) | Ueberall in den URLs |
| `{domaine}` | E-Mail-Domaene der Organisation (z.B. contoso.de) | E-Mail-Adressen |
| `SiteUrl` | Vollstaendige URL der in Schritt 1 erstellten SharePoint-Website | setup_lists.ps1, Flow-Variablen |
| `varSharedMailbox` | Adresse des sendenden Shared Mailbox | Flow 1 und Flow 2 |
| `varFormUrlDE` | URL von Formular 3 (monatlicher Bericht DE) | Flow 1 |
| `varFormUrlEN` | URL von Formular 4 (monatlicher Bericht EN) | Flow 1 |
| `varTemplatePathDE` | SharePoint-Pfad der Word-Vorlage DE | Flow 2 |
| `varTemplatePathEN` | SharePoint-Pfad der Word-Vorlage EN | Flow 2 |
| Administrator-Fehleradresse | Empfaenger der Flow-Fehler-E-Mails | Flow 1 und Flow 2 |

---

## 10. Haeufige Probleme und Loesungshinweise

### Das PnP-Skript schlaegt mit "Access Denied" fehl

Pruefen, dass das PowerShell-Konto Site Collection Administrator auf der Website ist.
Im SharePoint Admin Center : Websites > Website TransferMappe > Berechtigungen.

### Der Flow J-5 findet keine Teilnehmer

Den OData-Filter auf `date_prochain_rdv` pruefen. Die Spalte muss vom Typ DateOnly sein.
Wenn die Spalte eine Uhrzeit enthaelt, den Filter anpassen (siehe Hinweis in Flow_1_Invitation_J-5.md).

### Der PDF-Flow schlaegt bei "Populate a Microsoft Word template" fehl

Pruefen, dass :
- Die .docx-Datei fuer das Power Automate-Dienstkonto zugaenglich ist
- Alle 118 Content Controls belegt sind (kein leeres Feld in der Aktion)
- Die Datei zum Zeitpunkt des Flow-Laufs nicht von einem anderen Benutzer geoeffnet ist

### Das PDF ist leer oder fehlerhaft

Pruefen, dass die Tag-Werte in der .docx-Datei genau den Feldnamen in der
Aktion "Populate" entsprechen. Die vollstaendige Liste in `specs/word_template_structure.md` nachschlagen.

### Das Shared Mailbox kann keine E-Mails senden

Das Shared Mailbox muss die Berechtigung "Senden als" fuer das Dienstkonto haben.
Im Exchange Admin Center : Empfaenger > Freigegebene Postfaecher > Berechtigungen.

### Der Flow ueberschreitet 30 Minuten fuer 100 Teilnehmer

Die Parallelitaetsgrenzen von Power Automate pruefen (standardmaessig verarbeitet die Schleife
"Apply to each" Elemente sequenziell). Bei Bedarf die Parallelitaet
(max. 50 gleichzeitig) auf der Schleife aktivieren.
Achtung : parallele Ausfuehrung kann Konflikte bei globalen Variablen verursachen --
Variablen im Schleifenbereich bevorzugen.
