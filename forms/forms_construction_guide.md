# Anleitung zur Erstellung der Microsoft Forms-Formulare

outplacement-tracker v0.1 - Sprint 2

Diese Anleitung ermöglicht einem Microsoft 365-Administrator die Neuerstellung der 4 Formulare
der Lösung von Grund auf. Geschätzter Zeitaufwand: 10 bis 15 Minuten pro Formular.

---

## 1. Übersicht

| # | Formularname | Sprache | Verwendungszweck |
|---|---|---|---|
| 1 | Ihr Karriereprofil - Transfer Mappe | DE | Onboarding des Teilnehmers, einmalig zu Beginn des Begleitungsprozesses ausgefüllt |
| 2 | Your Career Profile - Transfer Mappe | EN | Identisch, englische Version |
| 3 | Ihr monatlicher Bericht - Transfer Mappe | DE | Monatlicher Bericht, vom Flow J-5 verschickt |
| 4 | Your Monthly Update - Transfer Mappe | EN | Identisch, englische Version |

Die Formulare 1 und 2 (Onboarding) sind optional und werden vom Teilnehmer einmalig ausgefüllt.
Die Formulare 3 und 4 (monatlicher Bericht) werden automatisch vom Flow J-5 fünf Tage vor
jedem monatlichen Termin verschickt.

Jedes Formular ist in Microsoft Forms eigenständig. Es bestehen keine technischen Abhängigkeiten
zwischen den Formularen.

---

## 2. Voraussetzungen

- Microsoft 365-Konto mit Lizenz E3 oder höher
- Zugriff auf Microsoft Forms (forms.microsoft.com)
- Die 4 Formulare müssen unter dem Dienstkonto oder dem freigegebenen Postfach der Organisation
  erstellt werden (nicht unter einem persönlichen Konto)

---

## 3. Formular 1: Onboarding DE - "Ihr Karriereprofil - Transfer Mappe"

### 3.1 Formular erstellen

1. forms.microsoft.com aufrufen
2. Auf "Neues Formular" klicken
3. Formulartitel: `Ihr Karriereprofil - Transfer Mappe`
4. Beschreibung / Einleitungstext (folgenden Text unverändert einfügen):

```
Dieser kurze Fragebogen hilft Ihrer Beraterin, Sie und Ihre Ziele besser zu verstehen.
Die Angaben sind freiwillig - Sie entscheiden, was Sie teilen möchten. Sie können dieses Formular jederzeit erneut ausfüllen, um Ihre Angaben zu aktualisieren.
Alle Informationen bleiben vertraulich und werden ausschliesslich im Rahmen Ihrer Begleitung verwendet.
```

### 3.2 Frage 1 - Plan A

- Auf "Frage hinzufügen" klicken
- Fragetyp: **Mehrzeiliger Text**
- Titel: `Ihr berufliches Hauptziel (Plan A)`
- Untertitel / Beschreibung: `Welche berufliche Richtung möchten Sie anstreben? Welche Art von Stelle suchen Sie? In welcher Branche oder Region?`
- Platzhalter: `Beispiel: Projektmanager im Maschinenbau, Rhein-Saar-Region, Unternehmen ab 200 Mitarbeitern`
- Pflichtfeld: **Nein**
- Zielspalte SharePoint: `Profils.plan_a`

### 3.3 Frage 2 - Plan B

- Fragetyp: **Mehrzeiliger Text**
- Titel: `Ihr berufliches Alternativziel (Plan B)`
- Untertitel / Beschreibung: `Falls Plan A nicht greift - welche alternative berufliche Richtung wäre für Sie ebenfalls interessant?`
- Platzhalter: `Beispiel: Selbstständigkeit als Berater, oder Wechsel in den öffentlichen Dienst`
- Pflichtfeld: **Nein**
- Zielspalte SharePoint: `Profils.plan_b`

### 3.4 Frage 3 - Marketingplan

- Fragetyp: **Mehrzeiliger Text**
- Titel: `Ihr berufliches Profil und Ihre Stärken`
- Untertitel / Beschreibung: `Was sind Ihre zentralen Kompetenzen? Was macht Sie für Arbeitgeber besonders interessant? Welche Erfahrungen oder Qualifikationen heben Sie hervor?`
- Platzhalter: `Beispiel: 15 Jahre Erfahrung in der Fahrzeugelektronik, spezialisiert auf CAN-Bus und Diagnose, Führungserfahrung mit Teams bis 8 Personen, Deutsch und Französisch fließend`
- Pflichtfeld: **Nein**
- Zielspalte SharePoint: `Profils.marketingplan`

### 3.5 Frage 4 - Zielmarkt

- Fragetyp: **Mehrzeiliger Text**
- Titel: `Ihr Zielmarkt`
- Untertitel / Beschreibung: `In welchem Umfeld möchten Sie arbeiten? Denken Sie an Region, Branche, Unternehmensgröße oder Unternehmenstyp.`
- Platzhalter: `Beispiel: Saarland / Lothringen / Luxemburg, Automobilindustrie oder Maschinenbau, mittelständische Unternehmen (100-500 Mitarbeiter)`
- Pflichtfeld: **Nein**
- Zielspalte SharePoint: `Profils.zielmarkt`

### 3.6 Bestätigungstext (nach Absenden)

In den Formulareinstellungen (Zahnrad-Symbol > "Bestätigung"):

```
Vielen Dank für Ihre Angaben. Ihr Karriereprofil wurde gespeichert und steht Ihrer Beraterin zur Verfügung.
Sie können dieses Formular jederzeit erneut ausfüllen, um Ihre Angaben zu aktualisieren.
```

---

## 4. Formular 2: Onboarding EN - "Your Career Profile - Transfer Mappe"

Gleiche Vorgehensweise wie Formular 1, mit den folgenden englischen Texten.

### 4.1 Formular erstellen

- Titel: `Your Career Profile - Transfer Mappe`
- Einleitungstext:

```
This short questionnaire helps your advisor understand you and your goals better.
All fields are optional - you decide what you want to share. You can fill in this form again at any time to update your information.
All information remains confidential and will be used exclusively in the context of your career transition support.
```

### 4.2 Frage 1 - Plan A

- Typ: **Multiple lines of text**
- Titel: `Your primary career goal (Plan A)`
- Beschreibung: `What professional direction would you like to pursue? What kind of position are you looking for? In which sector or region?`
- Platzhalter: `Example: Project Manager in mechanical engineering, Rhine-Saar-Luxembourg region, companies with 200+ employees`
- Pflichtfeld: **No**
- Zielspalte SharePoint: `Profils.plan_a`

### 4.3 Frage 2 - Plan B

- Typ: **Multiple lines of text**
- Titel: `Your alternative career goal (Plan B)`
- Beschreibung: `If Plan A does not work out - what alternative professional direction would also be of interest to you?`
- Platzhalter: `Example: Self-employment as a consultant, or transition to the public sector`
- Pflichtfeld: **No**
- Zielspalte SharePoint: `Profils.plan_b`

### 4.4 Frage 3 - Marketing Plan

- Typ: **Multiple lines of text**
- Titel: `Your professional profile and strengths`
- Beschreibung: `What are your core competencies? What makes you particularly attractive to employers? Which experiences or qualifications do you want to highlight?`
- Platzhalter: `Example: 15 years of experience in automotive electronics, specialised in CAN-Bus and diagnostics, leadership experience with teams up to 8 people, fluent in German and French`
- Pflichtfeld: **No**
- Zielspalte SharePoint: `Profils.marketingplan`

### 4.5 Frage 4 - Target Market

- Typ: **Multiple lines of text**
- Titel: `Your target market`
- Beschreibung: `In what environment would you like to work? Think about region, sector, company size or type of organisation.`
- Platzhalter: `Example: Saarland / Lorraine / Luxembourg, automotive or mechanical engineering, mid-sized companies (100-500 employees)`
- Pflichtfeld: **No**
- Zielspalte SharePoint: `Profils.zielmarkt`

### 4.6 Bestätigungstext

```
Thank you for your input. Your career profile has been saved and is available to your advisor.
You can fill in this form again at any time to update your information.
```

---

## 5. Formular 3: Monatlicher Bericht DE - "Ihr monatlicher Bericht - Transfer Mappe"

### 5.1 Formular erstellen

- Titel: `Ihr monatlicher Bericht - Transfer Mappe`
- Einleitungstext:

```
Bitte nehmen Sie sich 5 Minuten Zeit, um diesen kurzen Bericht vor Ihrem nächsten Beratungstermin auszufüllen.
Nur die erste Frage ist Pflichtangabe. Alle anderen Felder sind freiwillig - Sie entscheiden, was Sie teilen möchten.
Diese Informationen helfen Ihrer Beraterin, den Termin gezielt vorzubereiten.
```

### 5.2 Frage 1 - Monatsbericht (*)

- Typ: **Mehrzeiliger Text**
- Titel: `Wie war Ihr Monat? (*)`
- Beschreibung: `Bitte beschreiben Sie kurz, wie der vergangene Monat verlaufen ist - beruflich und/oder persönlich, was auch immer Ihnen wichtig erscheint.`
- Platzhalter: `Ihr Bericht hier...`
- Pflichtfeld: **Ja**
- Zielspalte SharePoint: `BilansMensuels.bilan_general`

### 5.3 Frage 2a - Zielstatus (Auswahl)

- Typ: **Auswahl (Choice)**
- Titel: `Wie stehen Sie bei den vereinbarten Zielen?`
- Beschreibung: `Denken Sie an die Ziele, die Sie beim letzten Termin mit Ihrer Beraterin vereinbart haben.`
- Optionen (Einzelauswahl, nur eine Antwort möglich):
  - `Vollständig erreicht`
  - `Teilweise erreicht`
  - `Nicht erreicht`
  - `Noch nicht relevant`
- Pflichtfeld: **Nein**
- Zielspalte SharePoint: `BilansMensuels.statut_objectifs`
- Hinweis: Der Flow ordnet diese Bezeichnungen den internen Codes zu (vollstaendig_erreicht usw.)

### 5.4 Frage 2b - Erläuterung zum Zielstatus (Freitext)

- Typ: **Mehrzeiliger Text**
- Titel: `Möchten Sie dazu etwas erläutern?`
- Beschreibung: `(optional) Kurze Erklärung oder Kontext zu Ihrer Antwort oben.`
- Platzhalter: `Ihre Erläuterung hier...`
- Pflichtfeld: **Nein**
- Zielspalte SharePoint: `BilansMensuels.statut_objectifs_detail`

### 5.5 Frage 3 - Was lief gut

- Typ: **Mehrzeiliger Text**
- Titel: `Was lief in diesem Monat gut?`
- Beschreibung: `(optional) Welche positiven Entwicklungen, Erfolge oder Fortschritte haben Sie erlebt?`
- Platzhalter: `Ihre Antwort hier...`
- Pflichtfeld: **Nein**
- Zielspalte SharePoint: `BilansMensuels.was_lief_gut`

### 5.6 Frage 4 - Wo brauche ich Unterstützung

- Typ: **Mehrzeiliger Text**
- Titel: `Wo brauchen Sie Unterstützung?`
- Beschreibung: `(optional) In welchen Bereichen würden Sie sich Hilfe oder Unterstützung wünschen - von Ihrer Beraterin oder anderweitig?`
- Platzhalter: `Ihre Antwort hier...`
- Pflichtfeld: **Nein**
- Zielspalte SharePoint: `BilansMensuels.wo_brauche_ich_unterstuetzung`

### 5.7 Frage 5 - Themen für den nächsten Termin

- Typ: **Mehrzeiliger Text**
- Titel: `Welche Themen möchten Sie beim nächsten Termin besprechen?`
- Beschreibung: `(optional) Was liegt Ihnen besonders am Herzen für das nächste Gespräch?`
- Platzhalter: `Ihre Antwort hier...`
- Pflichtfeld: **Nein**
- Zielspalte SharePoint: `BilansMensuels.themen_naechster_termin`

### 5.8 Frage 6 - Sonstige Anmerkungen

- Typ: **Mehrzeiliger Text**
- Titel: `Sonstige Anmerkungen`
- Beschreibung: `(optional) Haben Sie noch etwas, das Sie mitteilen möchten und das oben nicht abgedeckt ist?`
- Platzhalter: `Ihre Antwort hier...`
- Pflichtfeld: **Nein**
- Zielspalte SharePoint: `BilansMensuels.sonstige_anmerkungen`

### 5.9 Bestätigungstext

```
Vielen Dank für Ihren Bericht. Ihre Beraterin wird diesen vor Ihrem Termin lesen.
Wir freuen uns darauf, Sie bald zu sehen.
```

---

## 6. Formular 4: Monatlicher Bericht EN - "Your Monthly Update - Transfer Mappe"

### 6.1 Formular erstellen

- Titel: `Your Monthly Update - Transfer Mappe`
- Einleitungstext:

```
Please take 5 minutes to complete this short update before your next appointment with your advisor.
Only the first question is mandatory. All other fields are optional - you decide what you want to share.
This information helps your advisor prepare for your session.
```

### 6.2 Frage 1 - General Review (*)

- Typ: **Multiple lines of text**
- Titel: `How was your month? (*)`
- Beschreibung: `Please briefly describe how the past month went - professionally and/or personally, whatever feels relevant to you.`
- Platzhalter: `Your update here...`
- Pflichtfeld: **Yes**
- Zielspalte SharePoint: `BilansMensuels.bilan_general`

### 6.3 Frage 2a - Objective status (choice)

- Typ: **Choice**
- Titel: `How are you progressing on the agreed objectives?`
- Beschreibung: `Think about the goals you agreed on with your advisor at your last session.`
- Optionen (Einzelauswahl):
  - `Fully achieved`
  - `Partially achieved`
  - `Not achieved`
  - `Not yet relevant`
- Pflichtfeld: **No**
- Zielspalte SharePoint: `BilansMensuels.statut_objectifs`
- Hinweis: Der Flow ordnet diese Bezeichnungen den internen Codes zu (vollstaendig_erreicht usw.)

### 6.4 Frage 2b - Details on objectives (free text)

- Typ: **Multiple lines of text**
- Titel: `Would you like to add any details?`
- Beschreibung: `(optional) A brief explanation or context for your answer above.`
- Platzhalter: `Your details here...`
- Pflichtfeld: **No**
- Zielspalte SharePoint: `BilansMensuels.statut_objectifs_detail`

### 6.5 Frage 3 - What went well

- Typ: **Multiple lines of text**
- Titel: `What went well this month?`
- Beschreibung: `(optional) What positive developments, successes or progress have you experienced?`
- Platzhalter: `Your answer here...`
- Pflichtfeld: **No**
- Zielspalte SharePoint: `BilansMensuels.was_lief_gut`

### 6.6 Frage 4 - Where I need support

- Typ: **Multiple lines of text**
- Titel: `Where do you need support?`
- Beschreibung: `(optional) In which areas would you welcome help or support - from your advisor or otherwise?`
- Platzhalter: `Your answer here...`
- Pflichtfeld: **No**
- Zielspalte SharePoint: `BilansMensuels.wo_brauche_ich_unterstuetzung`

### 6.7 Frage 5 - Topics for the next session

- Typ: **Multiple lines of text**
- Titel: `What topics would you like to discuss at the next session?`
- Beschreibung: `(optional) What is particularly important to you for your next conversation?`
- Platzhalter: `Your answer here...`
- Pflichtfeld: **No**
- Zielspalte SharePoint: `BilansMensuels.themen_naechster_termin`

### 6.8 Frage 6 - Additional remarks

- Typ: **Multiple lines of text**
- Titel: `Any other remarks?`
- Beschreibung: `(optional) Is there anything else you would like to share that is not covered above?`
- Platzhalter: `Your answer here...`
- Pflichtfeld: **No**
- Zielspalte SharePoint: `BilansMensuels.sonstige_anmerkungen`

### 6.9 Bestätigungstext

```
Thank you for your update. Your advisor will read it before your session.
We look forward to seeing you soon.
```

---

## 7. Konfiguration nach der Erstellung

Diese Einstellungen gelten für jedes der 4 Formulare.

### 7.1 Freigabe

In den Formulareinstellungen (Schaltfläche "Teilen" / "Share"):

- "Jeder mit dem Link kann antworten" / "Anyone with the link can respond" auswählen
- "Nur Personen in meiner Organisation" nicht aktivieren - die Teilnehmer verfügen nicht
  zwingend über ein M365-Konto

### 7.2 Anonymität

- Die Aufzeichnung des Microsoft 365-Kontonamens des Ausfüllenden deaktivieren
- In den Einstellungen: "Antworten aufzeichnen" / "Record name" deaktivieren
- Begründung: Die Teilnehmer haben kein M365-Konto, und die DSGVO schreibt
  Datensparsamkeit vor

### 7.3 Oberflächensprache

- Formular 1 und 3: Sprache = Deutsch
- Formular 2 und 4: Language = English
- Einstellung in den Formulareinstellungen > Sprache

### 7.4 Einschränkung der Einreichungen

- "Nur eine Antwort pro Person" / "One response per person" nicht aktivieren
- Der Flow erzeugt einen eindeutigen Link pro Einladung. Die Einschränkung der Antworten
  wird durch den Flow gesteuert, nicht durch Forms.

---

## 8. Integration mit Power Automate

Nach der Erstellung der 4 Formulare:

1. Die URL jedes Formulars über die Schaltfläche "Teilen" > "Link zum Teilen" abrufen
2. Diese URLs werden als Variablen in den beiden Flows konfiguriert:
   - `varFormUrlDE`: URL von Formular 3 (monatlicher Bericht DE)
   - `varFormUrlEN`: URL von Formular 4 (monatlicher Bericht EN)
3. Die Onboarding-Formulare (Formular 1 und 2) werden nicht automatisch verschickt.
   Ihr Link wird zu Beginn des Begleitungsprozesses manuell durch die Beraterin kommuniziert.
4. Die Antworten werden über den Connector "Microsoft Forms" in Power Automate abgerufen,
   nicht per manuellem Excel-Export.

Zur detaillierten Konfiguration der Flows siehe:
- `power_automate/Flow_1_Invitation_J-5.md`
- `power_automate/Flow_2_Generation_PDF.md`
