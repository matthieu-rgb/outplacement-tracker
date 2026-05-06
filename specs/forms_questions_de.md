# Formulare - Fragen auf Deutsch (DE)

Genaue Spezifikation der beiden Microsoft Forms in der deutschen Version.
Diese Fragen werden bei der Bereitstellung unverändert in Microsoft Forms übernommen.

Konventionen:
- Pflichtfeld durch (*) im Fragentitel gekennzeichnet
- Optionale Felder: kein Sternchen
- Sonderzeichen: ae = ae, oe = oe, ue = ue, ss = ss in Spaltennamen; Umlaute werden im für den Teilnehmer sichtbaren Text verwendet
- Reihenfolge der Fragen = Anzeigereihenfolge im Formular

---

## Formular 1: Onboarding - Karriereprofil (DE)

**Formularname**: Ihr Karriereprofil - Transfer Mappe

**Einleitungstext** (oben im Formular angezeigt):

> Dieser kurze Fragebogen hilft Ihrer Beraterin, Sie und Ihre Ziele besser zu verstehen.
> Die Angaben sind freiwillig - Sie entscheiden, was Sie teilen möchten. Sie können dieses Formular jederzeit erneut ausfüllen, um Ihre Angaben zu aktualisieren.
> Alle Informationen bleiben vertraulich und werden ausschliesslich im Rahmen Ihrer Begleitung verwendet.

---

### Frage 1 - Plan A: Berufliches Hauptziel

**Typ**: Mehrzeiliger Text (Multiple lines of text)
**Pflichtfeld**: nein
**Titel**: Ihr berufliches Hauptziel (Plan A)
**Beschreibung / Untertext**: Welche berufliche Richtung möchten Sie anstreben? Welche Art von Stelle suchen Sie? In welcher Branche oder Region?
**Platzhalter**: Beispiel: Projektmanager im Maschinenbau, Rhein-Saar-Region, Unternehmen ab 200 Mitarbeitern
**Zielspalte SharePoint**: `Profils.plan_a`

---

### Frage 2 - Plan B: Berufliches Alternativziel

**Typ**: Mehrzeiliger Text
**Pflichtfeld**: nein
**Titel**: Ihr berufliches Alternativziel (Plan B)
**Beschreibung / Untertext**: Falls Plan A nicht greift - welche alternative berufliche Richtung wäre für Sie ebenfalls interessant?
**Platzhalter**: Beispiel: Selbstständigkeit als Berater, oder Wechsel in den öffentlichen Dienst
**Zielspalte SharePoint**: `Profils.plan_b`

---

### Frage 3 - Marketingplan

**Typ**: Mehrzeiliger Text
**Pflichtfeld**: nein
**Titel**: Ihr berufliches Profil und Ihre Stärken
**Beschreibung / Untertext**: Was sind Ihre zentralen Kompetenzen? Was macht Sie für Arbeitgeber besonders interessant? Welche Erfahrungen oder Qualifikationen heben Sie hervor?
**Platzhalter**: Beispiel: 15 Jahre Erfahrung in der Fahrzeugelektronik, spezialisiert auf CAN-Bus und Diagnose, Führungserfahrung mit Teams bis 8 Personen, Deutsch und Französisch fließend
**Zielspalte SharePoint**: `Profils.marketingplan`

---

### Frage 4 - Zielmarkt

**Typ**: Mehrzeiliger Text
**Pflichtfeld**: nein
**Titel**: Ihr Zielmarkt
**Beschreibung / Untertext**: In welchem Umfeld möchten Sie arbeiten? Denken Sie an Region, Branche, Unternehmensgröße oder Unternehmenstyp.
**Platzhalter**: Beispiel: Saarland / Lothringen / Luxemburg, Automobilindustrie oder Maschinenbau, mittelständische Unternehmen (100-500 Mitarbeiter)
**Zielspalte SharePoint**: `Profils.zielmarkt`

---

**Bestätigungstext** (nach Absenden angezeigt):

> Vielen Dank für Ihre Angaben. Ihr Karriereprofil wurde gespeichert und steht Ihrer Beraterin zur Verfügung.
> Sie können dieses Formular jederzeit erneut ausfüllen, um Ihre Angaben zu aktualisieren.

---

## Formular 2: Monatlicher Bericht (DE)

**Formularname**: Ihr monatlicher Bericht - Transfer Mappe

**Einleitungstext** (oben im Formular angezeigt):

> Bitte nehmen Sie sich 5 Minuten Zeit, um diesen kurzen Bericht vor Ihrem nächsten Beratungstermin auszufüllen.
> Nur die erste Frage ist Pflichtangabe. Alle anderen Felder sind freiwillig - Sie entscheiden, was Sie teilen moechten.
> Diese Informationen helfen Ihrer Beraterin, den Termin gezielt vorzubereiten.

---

### Frage 1 - Monatsbericht (*)

**Typ**: Mehrzeiliger Text
**Pflichtfeld**: ja
**Titel**: Wie war Ihr Monat? (*)
**Beschreibung / Untertext**: Bitte beschreiben Sie kurz, wie der vergangene Monat verlaufen ist - beruflich und/oder persönlich, was auch immer Ihnen wichtig erscheint.
**Platzhalter**: Ihr Bericht hier...
**Zielspalte SharePoint**: `BilansMensuels.bilan_general`

---

### Frage 2 - Zielstatus

**Typ**: Auswahl (Choice) + Freitext-Ergänzung

**Teil 2a - Auswahl**
**Pflichtfeld**: nein
**Titel**: Wie stehen Sie bei den vereinbarten Zielen?
**Beschreibung / Untertext**: Denken Sie an die Ziele, die Sie beim letzten Termin mit Ihrer Beraterin vereinbart haben.
**Optionen** (Einzelauswahl):
- Vollständig erreicht
- Teilweise erreicht
- Nicht erreicht
- Noch nicht relevant
**Zielspalte SharePoint**: `BilansMensuels.statut_objectifs`
**Zuordnung der Werte**:
  - "Vollstaendig erreicht" -> `vollstaendig_erreicht`
  - "Teilweise erreicht" -> `teilweise_erreicht`
  - "Nicht erreicht" -> `nicht_erreicht`
  - "Noch nicht relevant" -> `noch_nicht_relevant`

**Teil 2b - Freitext**
**Pflichtfeld**: nein
**Titel**: Möchten Sie dazu etwas erläutern?
**Beschreibung / Untertext**: (optional) Kurze Erklärung oder Kontext zu Ihrer Antwort oben.
**Platzhalter**: Ihre Erlaeuterung hier...
**Zielspalte SharePoint**: `BilansMensuels.statut_objectifs_detail`

---

### Frage 3 - Was lief gut

**Typ**: Mehrzeiliger Text
**Pflichtfeld**: nein
**Titel**: Was lief in diesem Monat gut?
**Beschreibung / Untertext**: (optional) Welche positiven Entwicklungen, Erfolge oder Fortschritte haben Sie erlebt?
**Platzhalter**: Ihre Antwort hier...
**Zielspalte SharePoint**: `BilansMensuels.was_lief_gut`

---

### Frage 4 - Wo brauche ich Unterstützung

**Typ**: Mehrzeiliger Text
**Pflichtfeld**: nein
**Titel**: Wo brauchen Sie Unterstützung?
**Beschreibung / Untertext**: (optional) In welchen Bereichen würden Sie sich Hilfe oder Unterstützung wünschen - von Ihrer Beraterin oder anderweitig?
**Platzhalter**: Ihre Antwort hier...
**Zielspalte SharePoint**: `BilansMensuels.wo_brauche_ich_unterstuetzung`

---

### Frage 5 - Themen für den nächsten Termin

**Typ**: Mehrzeiliger Text
**Pflichtfeld**: nein
**Titel**: Welche Themen möchten Sie beim nächsten Termin besprechen?
**Beschreibung / Untertext**: (optional) Was liegt Ihnen besonders am Herzen für das nächste Gespräch?
**Platzhalter**: Ihre Antwort hier...
**Zielspalte SharePoint**: `BilansMensuels.themen_naechster_termin`

---

### Frage 6 - Sonstige Anmerkungen

**Typ**: Mehrzeiliger Text
**Pflichtfeld**: nein
**Titel**: Sonstige Anmerkungen
**Beschreibung / Untertext**: (optional) Haben Sie noch etwas, das Sie mitteilen moechten und das oben nicht abgedeckt ist?
**Platzhalter**: Ihre Antwort hier...
**Zielspalte SharePoint**: `BilansMensuels.sonstige_anmerkungen`

---

**Bestätigungstext** (nach Absenden angezeigt):

> Vielen Dank für Ihren Bericht. Ihre Beraterin wird diesen vor Ihrem Termin lesen.
> Wir freuen uns darauf, Sie bald zu sehen.

---

## Konfigurationshinweise für Forms

- **Freigabe**: "Jeder mit dem Link kann antworten" (Link vom Flow J-5 generiert, ein Link pro Teilnehmer pro Monat)
- **Anonymität**: "Antworten aufzeichnen" für den Microsoft-Kontonamen deaktivieren, wenn die Teilnehmer kein M365-Konto haben (Formular ohne Anmeldung zugänglich)
- **Einschränkung der Einreichungen**: 1 Antwort pro Link (Power Automate generiert einen eindeutigen Link pro Einladung)
- **Oberflächensprache**: Deutsch
- **Export**: Die Antworten werden über den Microsoft Forms-Connector in Power Automate abgerufen, nicht per manuellem Excel-Export
