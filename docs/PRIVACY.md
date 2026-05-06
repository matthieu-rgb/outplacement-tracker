# Datenschutzinformation - outplacement-tracker

outplacement-tracker v0.1 - Dokument für Organisationen, die diese Lösung einsetzen

---

## 1. Geltungsbereich und Zweck dieses Dokuments

Dieses Dokument richtet sich an Transfergesellschaften und Outplacement-Anbieter, die
die Lösung outplacement-tracker in ihrem Microsoft 365-Tenant einsetzen.

Es beschreibt:

- die durch die Lösung verarbeiteten personenbezogenen Daten und die jeweiligen Zwecke
- die Rechtsgrundlage jeder Verarbeitung
- die empfohlenen Speicherfristen
- die Rechte der betroffenen Personen und deren Ausübung
- die technischen und organisatorischen Maßnahmen (TOM)
- die Verantwortlichkeitskette gemäß DSGVO und BDSG

Dieses Dokument stellt keine Rechtsberatung dar. Jede Organisation, die die Lösung
einsetzt, muss es an ihre eigene Situation anpassen - in Abstimmung mit ihrem
Datenschutzbeauftragten (DSB) oder ihrer Rechtsabteilung.

---

## 2. Verantwortlichkeit und Auftragsverarbeitung

### 2.1 Verantwortlichkeitskette

```
[Teilnehmer]
   |
   Betroffene Person im Sinne von Art. 4 Nr. 1 DSGVO.
   Inhaber der Rechte nach Art. 15 bis 22 DSGVO.
   |
   v
[Transfergesellschaft]
   |
   VERANTWORTLICHER im Sinne von Art. 4 Nr. 7 DSGVO.
   Bestimmt die Zwecke und Mittel der Verarbeitung.
   Führt das Verzeichnis der Verarbeitungstätigkeiten (VVT) gemäß Art. 30 DSGVO.
   Informiert die Teilnehmer gemäß Art. 13 DSGVO.
   Gewährleistet die Ausübung der Betroffenenrechte (Art. 15-22 DSGVO).
   Schließt den AVV mit Microsoft ab (siehe Abschnitt 8).
   |
   v
[Matthieu Riegert - Urheber des Projekts]
   |
   WEDER VERANTWORTLICHER NOCH AUFTRAGSVERARBEITER.
   Stellt ein Open-Source-Kit unter freier Lizenz bereit.
   Verarbeitet, speichert, liest und greift auf keine personenbezogenen Daten zu.
   Hat keinen Zugriff auf den Microsoft 365-Tenant der einsetzenden Organisation.
   Es ist kein AVV mit dem Urheber abzuschließen.
   |
   v
[Microsoft Corporation]
   |
   AUFTRAGSVERARBEITER im Sinne von Art. 4 Nr. 8 und Art. 28 DSGVO.
   Der Microsoft Online Services Data Processing Agreement (DPA) stellt den AVV
   im Sinne von Art. 28 DSGVO dar. Dieser DPA wird von der Organisation bei
   der Buchung von Microsoft 365 akzeptiert.
   Microsoft speichert die Daten im Tenant der Organisation.
   Die EU Data Boundary von Microsoft gewährleistet den Datenverbleib in Europa
   (siehe Abschnitt 9).
```

### 2.2 Praktische Konsequenz

Die Organisation, die outplacement-tracker einsetzt, ist alleinige Verantwortliche.
Sie trägt die vollständige Verantwortung für:

- die Führung des Verzeichnisses der Verarbeitungstätigkeiten (Art. 30 DSGVO)
- die Information der Teilnehmer vor ihrer Aufnahme in die Lösung (Art. 13 DSGVO)
- die Bearbeitung von Anfragen zur Ausübung von Betroffenenrechten (Art. 15-22 DSGVO)
- die Umsetzung angemessener Sicherheitsmaßnahmen (Art. 32 DSGVO)
- die Meldung einer Datenpanne an die zuständige Aufsichtsbehörde (Art. 33 DSGVO),
  in Deutschland den Bundesbeauftragten für den Datenschutz und die Informationsfreiheit
  (BfDI) oder die zuständige Landesbehörde entsprechend dem Sitz der Organisation

Der Urheber des Projekts schließt keinen AVV ab, wird bei einer Datenpanne nicht
benachrichtigt und kann für einen Vorfall im Tenant des Kunden nicht haftbar gemacht werden.

---

## 3. Verarbeitete personenbezogene Daten

Die Lösung verarbeitet ausschließlich gewöhnliche personenbezogene Daten im Sinne von
Art. 4 Nr. 1 DSGVO. Es werden keine besonderen Kategorien personenbezogener Daten
im Sinne von Art. 9 DSGVO erfasst (keine Gesundheitsdaten, keine Daten zur ethnischen
Herkunft, keine politischen Meinungen usw.).

### 3.1 Liste "Participants" (Teilnehmerliste)

| Feld | Typ | Pflichtfeld | Zweck | Rechtsgrundlage |
|---|---|---|---|---|
| nom (Nachname) | Text | Ja | Identifikation des Teilnehmers, PDF-Erstellung | Art. 6 Abs. 1 lit. b DSGVO |
| prenom (Vorname) | Text | Ja | Identifikation des Teilnehmers, PDF-Erstellung | Art. 6 Abs. 1 lit. b DSGVO |
| email | Text | Ja | Versand der monatlichen automatischen Einladung | Art. 6 Abs. 1 lit. b DSGVO |
| langue (Sprache) | Auswahl (DE/EN) | Ja | Sprachliche Anpassung der Kommunikation | Art. 6 Abs. 1 lit. b DSGVO |
| id_conseillere (Beraterin) | M365-E-Mail | Ja | Weiterleitung des PDF an die zuständige Beraterin | Art. 6 Abs. 1 lit. b DSGVO |
| date_debut_parcours (Startdatum) | Datum | Ja | Berechnung der Maßnahmedauer, PDF-Deckblatt | Art. 6 Abs. 1 lit. b DSGVO |
| date_prochain_rdv (nächster Termin) | Datum | Ja | Automatischer Versand der Einladung J-5 | Art. 6 Abs. 1 lit. b DSGVO |
| statut (Status) | Auswahl | Ja | Filterung aktiver Teilnehmer in den Flows | Art. 6 Abs. 1 lit. b DSGVO |

Hinweis: Das Feld "Title" der Liste (Format "Vorname Nachname") wird automatisch durch
Power Automate generiert. Es enthält personenbezogene Daten und unterliegt denselben
Aufbewahrungsregeln wie die übrigen Felder.

### 3.2 Liste "Profils" (Profile)

| Feld | Typ | Pflichtfeld | Zweck | Rechtsgrundlage |
|---|---|---|---|---|
| id_participant (Teilnehmer-ID) | Ganzzahl | Ja | Fremdschlüssel zur Teilnehmerliste | Art. 6 Abs. 1 lit. b DSGVO |
| plan_a | Langer Text | Nein | Hauptberuflicher Plan - dokumentiert durch die Beraterin | Art. 6 Abs. 1 lit. b DSGVO |
| plan_b | Langer Text | Nein | Alternativer beruflicher Plan - dokumentiert durch die Beraterin | Art. 6 Abs. 1 lit. b DSGVO |
| marketingplan | Langer Text | Nein | Strategie zur Stellensuche - dokumentiert durch die Beraterin | Art. 6 Abs. 1 lit. b DSGVO |
| zielmarkt | Langer Text | Nein | Zielbranche(n) - dokumentiert durch die Beraterin | Art. 6 Abs. 1 lit. b DSGVO |
| date_creation (Erstellungsdatum) | Datum/Uhrzeit | Ja | Technische Nachverfolgbarkeit | Art. 6 Abs. 1 lit. b DSGVO |
| date_modification (Änderungsdatum) | Datum/Uhrzeit | Nein | Technische Nachverfolgbarkeit | Art. 6 Abs. 1 lit. b DSGVO |

Hinweis: Die vier Inhaltsfelder (plan_a, plan_b, marketingplan, zielmarkt) sind optional.
Ihre Befüllung liegt im Ermessen der Beraterin und des Teilnehmers. Sie können sensible
Informationen zu den beruflichen Vorhaben des Teilnehmers enthalten.

### 3.3 Liste "BilansMensuels" (Monatsberichte)

| Feld | Typ | Pflichtfeld | Zweck | Rechtsgrundlage |
|---|---|---|---|---|
| id_participant (Teilnehmer-ID) | Ganzzahl | Ja | Fremdschlüssel zur Teilnehmerliste | Art. 6 Abs. 1 lit. b DSGVO |
| date_rdv (Termindatum) | Datum | Ja | Datum des zugehörigen Monatstermins | Art. 6 Abs. 1 lit. b DSGVO |
| date_soumission (Einreichungsdatum) | Datum/Uhrzeit | Ja | Zeitstempel der Formulareinreichung | Art. 6 Abs. 1 lit. b DSGVO |
| bilan_general (allgemeiner Rückblick) | Langer Text | Ja | Freier Rückblick des Teilnehmers | Art. 6 Abs. 1 lit. b DSGVO |
| statut_objectifs (Zielstatus) | Auswahl | Nein | Selbsteinschätzung des Teilnehmers zu seinen Zielen | Art. 6 Abs. 1 lit. b DSGVO |
| statut_objectifs_detail (Zielstatus Detail) | Langer Text | Nein | Näheres zum Zielstatus | Art. 6 Abs. 1 lit. b DSGVO |
| was_lief_gut | Langer Text | Nein | Was gut lief (freie Angabe) | Art. 6 Abs. 1 lit. b DSGVO |
| wo_brauche_ich_unterstützung | Langer Text | Nein | Unterstützungsbedarf (freie Angabe) | Art. 6 Abs. 1 lit. b DSGVO |
| themen_nächster_termin | Langer Text | Nein | Vorgeschlagene Themen für den nächsten Termin | Art. 6 Abs. 1 lit. b DSGVO |
| sonstige_anmerkungen | Langer Text | Nein | Sonstige Hinweise | Art. 6 Abs. 1 lit. b DSGVO |

Hinweis: Von den 10 Feldern dieser Liste sind 7 optional. Der Teilnehmer entscheidet
selbst, was er mitteilen möchte. Die Lösung enthält keinerlei Mechanismus zur
Verfolgung einzelner Bewerbungen, keine Liste von Arbeitgeberkontakten und kein
Scoring oder Ranking der Teilnehmer.

### 3.4 Generierte PDF-Dokumente

Jede Ausführung von Flow 2 (PDF-Generierung) erzeugt eine PDF-Datei, die in der
SharePoint-Dokumentenbibliothek "TransferMappes" gespeichert wird. Diese Datei:

- enthält die personenbezogenen Daten aus den drei oben genannten Listen
- wird nach dem Format benannt: TransferMappe_{Vorname}_{Nachname}_{YYYY-MM-DD}.pdf
- wird per E-Mail an die zugewiesene Beraterin (Feld id_conseillere) übermittelt
- verbleibt im Tenant der Organisation und verlässt diesen nicht

Das PDF-Dokument ist ein personenbezogenes Dokument im Sinne der DSGVO. Es unterliegt
denselben Aufbewahrungsfristen wie die zugrunde liegenden Daten.

### 3.5 Power Automate-Ausführungsprotokolle

Die Power Automate-Flows erzeugen Ausführungsprotokolle (Run History), die im Portal
make.powerautomate.com einsehbar sind. Diese Protokolle können enthalten:

- Namen und E-Mail-Adressen von Teilnehmern (als Parameter von Aktionen verwendet)
- Fehlercodes und technische Meldungen

Diese Protokolle werden von Microsoft gemäß den Einstellungen der M365-Lizenz der
Organisation aufbewahrt (in der Regel 28 Tage bei E3). Sie werden von der Lösung
nicht exportiert und verlassen den Tenant nicht.

---

## 4. Rechtsgrundlage der Verarbeitung

### 4.1 Hauptrechtsgrundlage: Vertragsdurchführung (Art. 6 Abs. 1 lit. b DSGVO)

Die Verarbeitung ist erforderlich für die Durchführung des Transfervertrags zwischen
der Transfergesellschaft und dem Teilnehmer im Rahmen von § 111 SGB III
(Sozialgesetzbuch Drittes Buch - Arbeitförderung).

Die monatliche Begleitung (Monatsberichte, Berufsprofil, Termindaten) bildet den
eigentlichen Kern der Begleitungsleistung, der der Teilnehmer durch seinen Eintritt
in die Transfergesellschaft zugestimmt hat.

### 4.2 Ergänzendes berechtigtes Interesse (Art. 6 Abs. 1 lit. f DSGVO)

Die automatische Erstellung von Begleitdokumenten (kumulatives PDF, Zielvereinbarungen)
dient auch einem berechtigten Interesse der Organisation: das Vorhandensein
einer dokumentarischen Begleitung, die den Anforderungen der Agentur für Arbeit
bei einer Prüfung genügt. Dieses Interesse schränkt die Rechte des Teilnehmers
nicht unangemessen ein, da die erhobenen Daten streng beruflich und zweckgebunden sind.

### 4.3 Keine Einwilligung als Rechtsgrundlage

Die Lösung stützt sich nicht auf die Einwilligung (Art. 6 Abs. 1 lit. a DSGVO)
als Hauptrechtsgrundlage. Die Einwilligung wäre in diesem Kontext nicht geeignet, da
sie ein Machtungleichgewicht zwischen der Organisation und dem Teilnehmer schaffen
würde (Abhängigkeitsverhältnis). Die Organisation darf keine "Einwilligung"
im Sinne der DSGVO für die Nutzung dieser Lösung einholen: die Vertragsrechtsgrundlage
(Art. 6 Abs. 1 lit. b DSGVO) ist hinreichend und robuster.

---

## 5. Speicherung und Löschung personenbezogener Daten

### 5.1 Empfohlene Speicherfristen

| Datenkategorie | Empfohlene Frist | Fristbeginn | Begründung |
|---|---|---|---|
| Teilnehmerdaten (Liste) | 12 Monate nach Maßnahmeende | Datum Status "beendet" | Ende des vertraglichen SGB-III-Rahmens |
| Profile (Liste) | 12 Monate nach Maßnahmeende | Datum Status "beendet" | Wie oben |
| Monatsberichte (Liste) | 12 Monate nach Maßnahmeende | Datum Status "beendet" | Wie oben |
| Generierte PDFs (SharePoint) | 3 Jahre nach Maßnahmeende | Datum Status "beendet" | Dokumentationsnachweis Agentur für Arbeit |
| Power Automate-Protokolle | 28 Tage (Microsoft) | Ausführungsdatum | Automatisch gemäß M365 |

Hinweis: Die Frist von 3 Jahren für PDFs entspricht der allgemein anerkannten
Verjährungsfrist für Vertragsstreitigkeiten nach deutschem Recht (§ 195 BGB).
Die Organisation muss diese Fristen an ihre eigenen gesetzlichen Pflichten anpassen,
insbesondere etwaige Anforderungen der Agentur für Arbeit hinsichtlich des
Nachweises der Begleitung.

### 5.2 Löschverfahren (Löschkonzept)

Die Lösung verfügt über keine automatische Datenlöschung. Die Organisation ist
verantwortlich für die Einrichtung eines geeigneten Verfahrens.

**Option 1 - Manuelle Löschung:**

Wenn ein Teilnehmer seine Maßnahme abschließt (Status wechselt auf "beendet"),
führt der Administrator nach Ablauf der Speicherfrist folgende Schritte durch:

1. Löschung des Eintrags in der Liste "Participants"
2. Löschung des zugehörigen Eintrags in "Profils" (Filterung nach id_participant)
3. Löschung aller zugehörigen Einträge in "BilansMensuels" (Filterung nach id_participant)
4. Löschung oder Archivierung des PDF-Ordners in der Bibliothek "TransferMappes"

**Option 2 - Halbautomatische Löschung (empfohlen):**

Erstellung eines wöchentlich geplanten Power Automate-Flows, der:

1. Alle Teilnehmereinträge mit dem Status "beendet" abruft,
   deren Enddatum die konfigurierte Speicherfrist überschreitet
2. Die zugehörigen Einträge in allen drei Listen löscht
3. Einen Löschbericht an den Administrator sendet

Dieser ergänzende Flow ist im Kit v0.1 nicht enthalten. Seine Entwicklung ist
im BACKLOG.md für eine spätere Version vorgesehen.

**Option 3 - SharePoint-Aufbewahrungsrichtlinie:**

Microsoft 365 bietet konfigurierbare Aufbewahrungsrichtlinien über das
Microsoft Purview Compliance Center. Die Organisation kann eine Aufbewahrungsrichtlinie
für die SharePoint-Website TransferMappe mit automatischer Löschung nach der
gewählten Frist konfigurieren. Diese Option erfordert keine zusätzliche Entwicklung,
setzt jedoch eine Microsoft 365-Lizenz mit Microsoft Purview voraus (in E3 verfügbar).

### 5.3 Recht auf Löschung (Art. 17 DSGVO)

Bei einer Löschungsanfrage eines Teilnehmers wird das manuelle Verfahren (Option 1)
unverzüglich angewendet, ohne Ablauf der Speicherfrist. Siehe Abschnitt 6.

---

## 6. Rechte der betroffenen Personen

Teilnehmer haben gemäß Art. 15 bis 22 DSGVO folgende Rechte. Die Organisation
trägt die alleinige Verantwortung für deren Umsetzung.

### 6.1 Auskunftsrecht (Art. 15 DSGVO)

Der Teilnehmer kann eine Kopie aller seiner Daten anfordern. Der Administrator:

1. Exportiert den Eintrag aus der Liste "Participants" (CSV-Export über SharePoint)
2. Exportiert den Eintrag aus der Liste "Profils"
3. Exportiert alle Einträge aus "BilansMensuels" für die entsprechende id_participant
4. Stellt das oder die generierten PDFs aus der Bibliothek "TransferMappes" bereit

### 6.2 Recht auf Berichtigung (Art. 16 DSGVO)

Der Administrator oder die Beraterin kann Einträge direkt in den SharePoint-Listen
ändern. Die Versionierung ist für alle drei Listen aktiviert (Parameter
"versioning: true" im Schema), was eine Aufbewahrung des Änderungsverlaufs ermöglicht.

### 6.3 Recht auf Löschung (Art. 17 DSGVO)

Das unter Abschnitt 5.2 (Option 1) beschriebene manuelle Löschverfahren ist anzuwenden.
Die Anfrage und die durchgeführte Maßnahme sind zur Nachweisführung zu dokumentieren.

Hinweis: Das Recht auf Löschung kann eingeschränkt sein, wenn die Organisation
Begleitnachweise für die Agentur für Arbeit aufbewahren muss. In diesem Fall muss
die Organisation den Teilnehmer über den Grund der partiellen Ablehnung informieren
(Art. 17 Abs. 3 DSGVO).

### 6.4 Recht auf Einschränkung der Verarbeitung (Art. 18 DSGVO)

Der Administrator setzt den Status des Teilnehmers in der Liste "Participants"
auf "gesperrt". Der Einladungs-Flow und der PDF-Generierungs-Flow schließen automatisch
Teilnehmer aus, deren Status nicht "aktiv" ist. Es werden damit keine neuen Daten erzeugt.

### 6.5 Recht auf Datenübertragbarkeit (Art. 20 DSGVO)

Die SharePoint-Listen ermöglichen den Export im CSV-Format über die Standard-Oberfläche.
Die generierten PDFs sind unmittelbar portierbar. Die Organisation kann dem Teilnehmer
auf Anfrage sämtliche Daten in diesen Standardformaten bereitstellen.

### 6.6 Widerspruchsrecht (Art. 21 DSGVO)

Im Kontext des SGB III ist das Widerspruchsrecht angesichts der vertraglichen
Rechtsgrundlage (Art. 6 Abs. 1 lit. b DSGVO) eingeschränkt. Die Organisation muss
ihren DSB konsultieren, um zu bestimmen, in welchen Fällen ein Widerspruch zulässig ist.

### 6.7 Kommunikationskanal für Anfragen

Die Organisation muss einen Kommunikationskanal für Betroffenenanfragen festlegen
und den Teilnehmern mitteilen (E-Mail an den DSB, Online-Formular, postalischer Weg).
Dieser Kanal muss in der Datenschutzinformation an die Teilnehmer enthalten sein
(siehe Abschnitt 11).

---

## 7. Technische und organisatorische Maßnahmen (TOM)

### 7.1 In der Lösung integrierte Maßnahmen

Folgende Maßnahmen sind durch Konstruktion in outplacement-tracker umgesetzt:

| Maßnahme | Umsetzung | Ebene |
|---|---|---|
| Datenverbleib im Tenant | Keine Daten verlassen den M365-Tenant - keine externe API, kein Drittanbieter-Connector | Architekturimmanent |
| Datensparsamkeit | 7 von 10 Feldern in BilansMensuels sind optional - kein Bewerbungs-Tracking | Konstruktionsbedingt |
| Datentrennung nach Organisation | Ein Tenant = eine Organisation - keine Zusammenführung durch Konstruktion möglich | Architekturimmanent |
| SharePoint-Versionierung | Vollständiger Änderungsverlauf aller drei Listen | Im Schema aktiviert |
| Rollenbasierter SharePoint-Zugriff | Die Listen sind in einer SharePoint-Website mit konfigurierbaren Berechtigungen gehostet | Zu konfigurieren (siehe 7.2) |
| Keine PII in Einladungs-E-Mails | Die Teilnehmer-E-Mail enthält nur Vorname, Nachname, Termindatum und Forms-Link - kein Klartextverlauf | In den Templates umgesetzt |
| Power Automate-Ausführungsprotokolle | Jede Ausführung wird im Power Automate-Verlauf des Tenants protokolliert | Nativer M365-Standard |

### 7.2 Von der Organisation umzusetzende Maßnahmen

Diese Maßnahmen liegen in der Verantwortung der einsetzenden Organisation.

**Vor der Inbetriebnahme zwingend erforderlich:**

| Maßnahme | Erforderliche Aktion | Referenz |
|---|---|---|
| Multi-Faktor-Authentifizierung (MFA) | MFA für alle Konten aktivieren, die Zugriff auf die SharePoint-Website TransferMappe haben | Microsoft Entra ID - Richtlinie für bedingten Zugriff |
| Eingeschränkte SharePoint-Berechtigungen | Die Website TransferMappe muss privat sein - nur Beraterinnen und Administratoren als Mitglieder | SharePoint-Administration - Gruppenrechte |
| Freigegebenes Postfach als Absender | Freigegebenes Postfach anlegen (z.B. transfer@domain.de) - keine persönliche Mitarbeiteradresse verwenden | Exchange Online - Administration |
| DLP (Data Loss Prevention) | DLP-Richtlinie konfigurieren, die die externe Weitergabe der SharePoint-Listen mit PII verhindert | Microsoft Purview - DLP-Richtlinien |
| Zugriff auf das Power Automate-Portal | Zugriff auf das Power Automate-Portal auf benannte Administratoren beschränken | Microsoft Entra ID - Rollen |
| Information der Teilnehmer (Art. 13 DSGVO) | Datenschutzinformation an jeden Teilnehmer vor seiner Aufnahme in die Lösung aushändigen | DSGVO-Rechtspflicht |

**Dringend empfohlen:**

| Maßnahme | Erforderliche Aktion | Referenz |
|---|---|---|
| Regelmäßige Zugriffsüberprüfung | Vierteljährliche Prüfung der Mitglieder der SharePoint-Gruppe TransferMappe | M365-Administration - Zugriffsüberprüfungen |
| M365-Auditprotokoll | M365-Auditprotokolle aktivieren und aufbewahren (SharePoint, Exchange, Power Automate) | Microsoft Purview - Audit |
| SharePoint-Sicherung | Microsoft 365 Backup oder eine zertifizierte Drittlösung aktivieren | Microsoft 365 Backup |
| Schulung der Beraterinnen | Nutzer in den bewährten Praktiken der Datenverarbeitung in SharePoint schulen | Intern |
| Passwortrichtlinie | Eine Passwortrichtlinie gemäß BSI-Empfehlungen anwenden (mindestens 12 Zeichen) | Microsoft Entra ID |

---

## 8. Auftragsverarbeiter

### 8.1 Microsoft Corporation

Microsoft ist der einzige Auftragsverarbeiter im Rahmen dieser Lösung.

| Element | Detail |
|---|---|
| Bezeichnung | Microsoft Corporation |
| DSGVO-Rolle | Auftragsverarbeiter - Art. 4 Nr. 8 und Art. 28 DSGVO |
| Grundlage des AVV | Microsoft Online Services Data Processing Agreement (DPA), akzeptiert bei der M365-Buchung |
| Betroffene Dienste | SharePoint Online, Power Automate, Microsoft Forms, Exchange Online, Word Online |
| Datenzugriff | Microsoft greift nicht auf Inhalte zu, außer auf Weisung der Organisation oder aufgrund gesetzlicher Verpflichtung |
| Zertifizierungen | ISO 27001, ISO 27018, SOC 1/2/3, branchenspezifische Zertifizierungen verfügbar |

Die Organisation muss keinen zusätzlichen AVV mit Microsoft abschließen: Der Microsoft
Online Services DPA wird bei der M365-Buchung akzeptiert und deckt alle von dieser
Lösung genutzten Dienste ab.

Der Microsoft Online Services DPA ist verfügbar unter:
https://www.microsoft.com/en-us/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA

### 8.2 Keine weiteren Auftragsverarbeiter

outplacement-tracker nutzt:

- keine externen Dritt-APIs (Analytics, Monitoring, KI, Übersetzung usw.)
- keine Premium-Power-Automate-Connectoren, die Drittdienste einbinden
- keine von dem M365-Tenant der Organisation getrennte Hosting-Infrastruktur
- keine Dienste des Projektautors

Jede Weiterentwicklung der Lösung, die einen neuen Drittdienst einführt, muss
einer Datenschutz-Folgenabschätzung (DSFA, Art. 35 DSGVO) unterzogen werden, sofern
die betroffenen personenbezogenen Daten betroffen sind.

---

## 9. Datenübermittlungen außerhalb der Europäischen Union

### 9.1 Datenhaltung bei Microsoft 365

Standardmäßig speichern Microsoft 365-Tenants, deren Region auf Europa konfiguriert ist,
Daten im Ruhezustand (Data at Rest) in den europäischen Rechenzentren von Microsoft
(hauptsächlich Niederlande und Irland, mit Sekundärstandorten in Finnland und Österreich).

Microsoft hat die EU Data Boundary eingeführt, die gewährleistet, dass Daten der
meisten M365-Dienste (darunter SharePoint, Exchange, Power Automate) in Europa verbleiben -
einschließlich Betriebs- und Diagnosevorgängen. Dieser Perimeter gilt für M365-E3-Lizenzen
mit der Region Europäische Union bei der Tenant-Erstellung.

Zur Prüfung der Tenant-Region: M365-Verwaltungsportal > Einstellungen >
Organisationsprofil > Land oder Region der Daten.

### 9.2 Keine Datenübermittlung durch die Lösung

outplacement-tracker übermittelt keine Daten außerhalb des Microsoft 365-Tenants
der Organisation. Die Lösung kontaktiert keine externen Dienste.

### 9.3 Bei Unsicherheit über den Datenspeicherort

Wenn die Organisation nicht bestätigen kann, dass ihr Tenant auf die Region EU
konfiguriert ist, muss sie dies vor dem Deployment prüfen und korrigieren. Ohne
Gewähr für den Datenspeicherort könnte eine Übermittlung in ein Drittland ohne
angemessene Rechtsgrundlage stattfinden (Art. 44 bis 49 DSGVO), was einen Verstoß
darstellen würde.

---

## 10. Benennung eines Datenschutzbeauftragten (DSB)

### 10.1 Wahrscheinliche Pflicht für Transfergesellschaften

Art. 37 DSGVO verpflichtet zur Benennung eines DSB in mehreren Fällen, darunter:

- wenn die Verarbeitung von einer Behörde oder öffentlichen Stelle durchgeführt wird
  (Art. 37 Abs. 1 lit. a DSGVO)
- wenn die Kerntätigkeit in der umfangreichen regulären und systematischen
  Überwachung betroffener Personen besteht (Art. 37 Abs. 1 lit. b DSGVO)

Eine Transfergesellschaft, die gleichzeitig 1.500 bis 2.000 Teilnehmer betreut,
führt mit großer Wahrscheinlichkeit eine umfangreiche Verarbeitung mit regelmäßiger
Überwachung der betroffenen Personen durch. Die Pflicht zur Benennung eines DSB
ist damit aller Voraussicht nach gegeben.

Die nationale Ergänzung durch § 38 BDSG verpflichtet ebenfalls zur Benennung eines
DSB, wenn die Organisation mindestens 20 Personen beschäftigt, die ständig mit der
automatisierten Verarbeitung personenbezogener Daten befasst sind.

### 10.2 Rolle des DSB beim Deployment dieser Lösung

Der DSB der Organisation muss eingebunden werden:

- bei der Aktualisierung des Verzeichnisses der Verarbeitungstätigkeiten (VVT, Abschnitt 11)
- bei der Erstellung der Datenschutzinformation für die Teilnehmer (Art. 13 DSGVO)
- bei der Prüfung der Notwendigkeit einer DSFA (Art. 35 DSGVO)
- bei regelmäßigen Zugriffs- und Sicherheitsüberprüfungen

---

## 11. Compliance-Checkliste vor dem Deployment

Die Organisation muss folgende Maßnahmen vor der Inbetriebnahme der Lösung durchführen.

### 11.1 Zwingend erforderliche Maßnahmen

- [ ] Prüfen, dass die Region des M365-Tenants auf die Europäische Union konfiguriert ist
- [ ] SharePoint-Berechtigungen der Website TransferMappe auf privaten Zugriff konfigurieren
      (Mitgliedergruppe: nur Beraterinnen und Administratoren)
- [ ] MFA für alle Konten aktivieren, die Zugriff auf die SharePoint-Website TransferMappe haben
- [ ] Das freigegebene Absenderpostfach anlegen (z.B. transfer@domain.de) und
      jede persönliche Adresse aus den Flow-Variablen entfernen
- [ ] Das Verzeichnis der Verarbeitungstätigkeiten der Organisation (Art. 30 DSGVO)
      aktualisieren und diese Verarbeitungstätigkeit ergänzen
- [ ] Eine Datenschutzinformation für die Teilnehmer gemäß Art. 13 DSGVO erstellen
      und vor ihrer Aufnahme in die Lösung aushändigen; sie muss insbesondere enthalten:
      die erfassten Datenkategorien, die Zwecke, die Rechtsgrundlage,
      die Speicherfrist, die Betroffenenrechte und den DSB-Kontakt
- [ ] Das Löschverfahren für Daten am Ende der Maßnahme festlegen und dokumentieren
- [ ] Den DSB der Organisation in die Umsetzung einbeziehen
- [ ] Word-Template-Metadaten neutralisieren: die .docx-Datei vor dem Upload in SharePoint
      auf persönliche Autorenangaben prüfen und bereinigen (Datei > Informationen >
      Auf Probleme prüfen > Dokument prüfen in Word)

### 11.2 Empfohlene Maßnahmen

- [ ] Die Notwendigkeit einer DSFA (Datenschutz-Folgenabschätzung, Art. 35 DSGVO)
      angesichts des Teilnehmervolumens und der Art der Begleitung bewerten
- [ ] Eine DLP-Richtlinie in Microsoft Purview für die SharePoint-Website TransferMappe konfigurieren
- [ ] M365-Auditprotokolle aktivieren und gemäß interner Richtlinie aufbewahren
- [ ] Eine Zugriffsüberprüfung für SharePoint mindestens einmal jährlich planen
- [ ] Das Verfahren zur Bearbeitung von Betroffenenanfragen dokumentieren
      (Frist 1 Monat, Art. 12 Abs. 3 DSGVO)
- [ ] Beraterinnen in guten Praktiken schulen: keine Kopie von Teilnehmerdaten
      auf privaten Geräten, keine Weitergabe per ungesicherter E-Mail usw.

### 11.3 Anpassung der Konfiguration

- [ ] Konfigurationswerte der Flows (varSiteUrl, varSharedMailbox usw.)
      durch die tatsächlichen Werte der Organisation vor der Aktivierung ersetzen
- [ ] E-Mail-Templates anpassen (Logo, Organisationsname, Kontaktdaten)
- [ ] Word-PDF-Template anpassen (Logo, Corporate Design), falls abweichend von 10 k Beratung

---

## 12. Datensparsamkeit: Gestaltungsprinzipien

Die Lösung wurde im Einklang mit dem Grundsatz der Datensparsamkeit und Zweckbindung
(Art. 5 Abs. 1 lit. c und e DSGVO) entwickelt. Folgende Gestaltungsentscheidungen belegen dies:

**Monatliches Formular (Microsoft Forms):**

- 6 Felder insgesamt, davon 5 optional
- Der Teilnehmer entscheidet frei, was er mitteilen möchte
- Kein Feld zur Verfolgung einzelner Bewerbungen
- Kein Feld für Arbeitgeberkontakte
- Kein Scoring oder Bewertungsmechanismus für Teilnehmer

**SharePoint-Listen:**

- Keine Finanzdaten (Gehalt, Abfindung, Höhe der Leistungen)
- Keine Gesundheits- oder medizinischen Daten
- Keine Angaben zu den Gründen der Kündigung (Verhältnis zum früheren Arbeitgeber)
- Kein Foto, kein Ausweisdokument, keine biometrischen Daten

**Automatische E-Mails:**

- Die Einladungs-E-Mail enthält nur Vorname, Nachname, Termindatum und den Forms-Link
- Die E-Mail an die Beraterin enthält das PDF als Anlage, jedoch keinen Datenverlauf
  im Klartext im Nachrichtenkörper
- Keine persönliche E-Mail-Adresse des Projektautors erscheint in den Templates

**Generiertes PDF:**

- Das PDF enthält ausschließlich die in den Formularen eingegebenen Daten
- Es enthält keine versteckten persönlichen Metadaten (die Word-Metadaten der .docx-Vorlage
  sind vom Administrator vor dem Upload zu prüfen und zu bereinigen)
- Es wird nur an die zuständige Beraterin übermittelt, nicht an das gesamte Team

**Einsichtnahme durch den Teilnehmer:**

- Der Teilnehmer gibt seine Monatsberichte selbst über Microsoft Forms ein
- Er kann sich an seine Beraterin wenden, um eine Kopie seiner Daten zu erhalten
- Er kann sein Recht auf Berichtigung durch Information an seine Beraterin oder den Administrator ausüben

---

## 13. Revisionshistorie

| Version | Datum | Änderungen |
|---|---|---|
| 1.0 | 2026-05-05 | Erstfassung (französisch) |
| 1.1 | 2026-05-06 | Vollständige Neufassung auf Deutsch (ADR-007) |
