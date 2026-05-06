# Datenschutzinformation - outplacement-tracker

outplacement-tracker v0.1 - Dokument fuer Organisationen, die diese Loesung einsetzen

---

## 1. Geltungsbereich und Zweck dieses Dokuments

Dieses Dokument richtet sich an Transfergesellschaften und Outplacement-Anbieter, die
die Loesung outplacement-tracker in ihrem Microsoft 365-Tenant einsetzen.

Es beschreibt:

- die durch die Loesung verarbeiteten personenbezogenen Daten und die jeweiligen Zwecke
- die Rechtsgrundlage jeder Verarbeitung
- die empfohlenen Speicherfristen
- die Rechte der betroffenen Personen und deren Ausuebung
- die technischen und organisatorischen Massnahmen (TOM)
- die Verantwortlichkeitskette gemaess DSGVO und BDSG

Dieses Dokument stellt keine Rechtsberatung dar. Jede Organisation, die die Loesung
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
   Fuehrt das Verzeichnis der Verarbeitungstaetigkeiten (VVT) gemaess Art. 30 DSGVO.
   Informiert die Teilnehmer gemaess Art. 13 DSGVO.
   Gewaehrleistet die Ausuebung der Betroffenenrechte (Art. 15-22 DSGVO).
   Schliesst den AVV mit Microsoft ab (siehe Abschnitt 8).
   |
   v
[Matthieu Riegert - Urheber des Projekts]
   |
   WEDER VERANTWORTLICHER NOCH AUFTRAGSVERARBEITER.
   Stellt ein Open-Source-Kit unter freier Lizenz bereit.
   Verarbeitet, speichert, liest und greift auf keine personenbezogenen Daten zu.
   Hat keinen Zugriff auf den Microsoft 365-Tenant der einsetzenden Organisation.
   Es ist kein AVV mit dem Urheber abzuschliessen.
   |
   v
[Microsoft Corporation]
   |
   AUFTRAGSVERARBEITER im Sinne von Art. 4 Nr. 8 und Art. 28 DSGVO.
   Der Microsoft Online Services Data Processing Agreement (DPA) stellt den AVV
   im Sinne von Art. 28 DSGVO dar. Dieser DPA wird von der Organisation bei
   der Buchung von Microsoft 365 akzeptiert.
   Microsoft speichert die Daten im Tenant der Organisation.
   Die EU Data Boundary von Microsoft gewaehrleistet den Datenverbleib in Europa
   (siehe Abschnitt 9).
```

### 2.2 Praktische Konsequenz

Die Organisation, die outplacement-tracker einsetzt, ist alleinige Verantwortliche.
Sie tragt die vollstaendige Verantwortung fuer:

- die Fuehrung des Verzeichnisses der Verarbeitungstaetigkeiten (Art. 30 DSGVO)
- die Information der Teilnehmer vor ihrer Aufnahme in die Loesung (Art. 13 DSGVO)
- die Bearbeitung von Anfragen zur Ausuebung von Betroffenenrechten (Art. 15-22 DSGVO)
- die Umsetzung angemessener Sicherheitsmassnahmen (Art. 32 DSGVO)
- die Meldung einer Datenpanne an die zustaendige Aufsichtsbehoerde (Art. 33 DSGVO),
  in Deutschland den Bundesbeauftragten fuer den Datenschutz und die Informationsfreiheit
  (BfDI) oder die zustaendige Landesbehoerde entsprechend dem Sitz der Organisation

Der Urheber des Projekts schliesst keinen AVV ab, wird bei einer Datenpanne nicht
benachrichtigt und kann fuer einen Vorfall im Tenant des Kunden nicht haftbar gemacht werden.

---

## 3. Verarbeitete personenbezogene Daten

Die Loesung verarbeitet ausschliesslich gewoehnliche personenbezogene Daten im Sinne von
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
| id_conseillere (Beraterin) | M365-E-Mail | Ja | Weiterleitung des PDF an die zustaendige Beraterin | Art. 6 Abs. 1 lit. b DSGVO |
| date_debut_parcours (Startdatum) | Datum | Ja | Berechnung der Massnahmedauer, PDF-Deckblatt | Art. 6 Abs. 1 lit. b DSGVO |
| date_prochain_rdv (naechster Termin) | Datum | Ja | Automatischer Versand der Einladung J-5 | Art. 6 Abs. 1 lit. b DSGVO |
| statut (Status) | Auswahl | Ja | Filterung aktiver Teilnehmer in den Flows | Art. 6 Abs. 1 lit. b DSGVO |

Hinweis: Das Feld "Title" der Liste (Format "Vorname Nachname") wird automatisch durch
Power Automate generiert. Es enthaelt personenbezogene Daten und unterliegt denselben
Aufbewahrungsregeln wie die uebrigen Felder.

### 3.2 Liste "Profils" (Profile)

| Feld | Typ | Pflichtfeld | Zweck | Rechtsgrundlage |
|---|---|---|---|---|
| id_participant (Teilnehmer-ID) | Ganzzahl | Ja | Fremdschluessel zur Teilnehmerliste | Art. 6 Abs. 1 lit. b DSGVO |
| plan_a | Langer Text | Nein | Hauptberuflicher Plan - dokumentiert durch die Beraterin | Art. 6 Abs. 1 lit. b DSGVO |
| plan_b | Langer Text | Nein | Alternativer beruflicher Plan - dokumentiert durch die Beraterin | Art. 6 Abs. 1 lit. b DSGVO |
| marketingplan | Langer Text | Nein | Strategie zur Stellensuche - dokumentiert durch die Beraterin | Art. 6 Abs. 1 lit. b DSGVO |
| zielmarkt | Langer Text | Nein | Zielbranche(n) - dokumentiert durch die Beraterin | Art. 6 Abs. 1 lit. b DSGVO |
| date_creation (Erstellungsdatum) | Datum/Uhrzeit | Ja | Technische Nachverfolgbarkeit | Art. 6 Abs. 1 lit. b DSGVO |
| date_modification (Aenderungsdatum) | Datum/Uhrzeit | Nein | Technische Nachverfolgbarkeit | Art. 6 Abs. 1 lit. b DSGVO |

Hinweis: Die vier Inhaltsfelder (plan_a, plan_b, marketingplan, zielmarkt) sind optional.
Ihre Befuellung liegt im Ermessen der Beraterin und des Teilnehmers. Sie koennen sensible
Informationen zu den beruflichen Vorhaben des Teilnehmers enthalten.

### 3.3 Liste "BilansMensuels" (Monatsberichte)

| Feld | Typ | Pflichtfeld | Zweck | Rechtsgrundlage |
|---|---|---|---|---|
| id_participant (Teilnehmer-ID) | Ganzzahl | Ja | Fremdschluessel zur Teilnehmerliste | Art. 6 Abs. 1 lit. b DSGVO |
| date_rdv (Termindatum) | Datum | Ja | Datum des zugehoerigen Monatstermins | Art. 6 Abs. 1 lit. b DSGVO |
| date_soumission (Einreichungsdatum) | Datum/Uhrzeit | Ja | Zeitstempel der Formulareinreichung | Art. 6 Abs. 1 lit. b DSGVO |
| bilan_general (allgemeiner Rueckblick) | Langer Text | Ja | Freier Rueckblick des Teilnehmers | Art. 6 Abs. 1 lit. b DSGVO |
| statut_objectifs (Zielstatus) | Auswahl | Nein | Selbsteinschaetzung des Teilnehmers zu seinen Zielen | Art. 6 Abs. 1 lit. b DSGVO |
| statut_objectifs_detail (Zielstatus Detail) | Langer Text | Nein | Naeheres zum Zielstatus | Art. 6 Abs. 1 lit. b DSGVO |
| was_lief_gut | Langer Text | Nein | Was gut lief (freie Angabe) | Art. 6 Abs. 1 lit. b DSGVO |
| wo_brauche_ich_unterstuetzung | Langer Text | Nein | Unterstuetzungsbedarf (freie Angabe) | Art. 6 Abs. 1 lit. b DSGVO |
| themen_naechster_termin | Langer Text | Nein | Vorgeschlagene Themen fuer den naechsten Termin | Art. 6 Abs. 1 lit. b DSGVO |
| sonstige_anmerkungen | Langer Text | Nein | Sonstige Hinweise | Art. 6 Abs. 1 lit. b DSGVO |

Hinweis: Von den 10 Feldern dieser Liste sind 7 optional. Der Teilnehmer entscheidet
selbst, was er mitteilen moechte. Die Loesung enthaelt keinerlei Mechanismus zur
Verfolgung einzelner Bewerbungen, keine Liste von Arbeitgeberkontakten und kein
Scoring oder Ranking der Teilnehmer.

### 3.4 Generierte PDF-Dokumente

Jede Ausfuehrung von Flow 2 (PDF-Generierung) erzeugt eine PDF-Datei, die in der
SharePoint-Dokumentenbibliothek "TransferMappes" gespeichert wird. Diese Datei:

- enthaelt die personenbezogenen Daten aus den drei oben genannten Listen
- wird nach dem Format benannt: TransferMappe_{Vorname}_{Nachname}_{YYYY-MM-DD}.pdf
- wird per E-Mail an die zugewiesene Beraterin (Feld id_conseillere) uebermittelt
- verbleibt im Tenant der Organisation und verlaesst diesen nicht

Das PDF-Dokument ist ein personenbezogenes Dokument im Sinne der DSGVO. Es unterliegt
denselben Aufbewahrungsfristen wie die zugrunde liegenden Daten.

### 3.5 Power Automate-Ausfuehrungsprotokolle

Die Power Automate-Flows erzeugen Ausfuehrungsprotokolle (Run History), die im Portal
make.powerautomate.com einsehbar sind. Diese Protokolle koennen enthalten:

- Namen und E-Mail-Adressen von Teilnehmern (als Parameter von Aktionen verwendet)
- Fehlercodes und technische Meldungen

Diese Protokolle werden von Microsoft gemaess den Einstellungen der M365-Lizenz der
Organisation aufbewahrt (in der Regel 28 Tage bei E3). Sie werden von der Loesung
nicht exportiert und verlassen den Tenant nicht.

---

## 4. Rechtsgrundlage der Verarbeitung

### 4.1 Hauptrechtsgrundlage: Vertragsdurchfuehrung (Art. 6 Abs. 1 lit. b DSGVO)

Die Verarbeitung ist erforderlich fuer die Durchfuehrung des Transfervertrags zwischen
der Transfergesellschaft und dem Teilnehmer im Rahmen von § 111 SGB III
(Sozialgesetzbuch Drittes Buch - Arbeitsfoerderung).

Die monatliche Begleitung (Monatsberichte, Berufsprofil, Termindaten) bildet den
eigentlichen Kern der Begleitungsleistung, der der Teilnehmer durch seinen Eintritt
in die Transfergesellschaft zugestimmt hat.

### 4.2 Ergaenzendes berechtigtes Interesse (Art. 6 Abs. 1 lit. f DSGVO)

Die automatische Erstellung von Begleitdokumenten (kumulatives PDF, Zielvereinbarungen)
dient auch einem berechtigten Interesse der Organisation: das Vorhandensein
einer dokumentarischen Begleitung, die den Anforderungen der Agentur fuer Arbeit
bei einer Pruefung genuegt. Dieses Interesse schraenkt die Rechte des Teilnehmers
nicht unangemessen ein, da die erhobenen Daten streng beruflich und zweckgebunden sind.

### 4.3 Keine Einwilligung als Rechtsgrundlage

Die Loesung stuetzt sich nicht auf die Einwilligung (Art. 6 Abs. 1 lit. a DSGVO)
als Hauptrechtsgrundlage. Die Einwilligung waere in diesem Kontext nicht geeignet, da
sie ein Machtungleichgewicht zwischen der Organisation und dem Teilnehmer schaffen
wuerde (Abhaengigkeitsverhaeltnis). Die Organisation darf keine "Einwilligung"
im Sinne der DSGVO fuer die Nutzung dieser Loesung einholen: die Vertragsrechtsgrundlage
(Art. 6 Abs. 1 lit. b DSGVO) ist hinreichend und robuster.

---

## 5. Speicherung und Loeschung personenbezogener Daten

### 5.1 Empfohlene Speicherfristen

| Datenkategorie | Empfohlene Frist | Fristbeginn | Begruendung |
|---|---|---|---|
| Teilnehmerdaten (Liste) | 12 Monate nach Massnahmeende | Datum Status "beendet" | Ende des vertraglichen SGB-III-Rahmens |
| Profile (Liste) | 12 Monate nach Massnahmeende | Datum Status "beendet" | Wie oben |
| Monatsberichte (Liste) | 12 Monate nach Massnahmeende | Datum Status "beendet" | Wie oben |
| Generierte PDFs (SharePoint) | 3 Jahre nach Massnahmeende | Datum Status "beendet" | Dokumentationsnachweis Agentur fuer Arbeit |
| Power Automate-Protokolle | 28 Tage (Microsoft) | Ausfuehrungsdatum | Automatisch gemaess M365 |

Hinweis: Die Frist von 3 Jahren fuer PDFs entspricht der allgemein anerkannten
Verjaeehrungsfrist fuer Vertragsstreitigkeiten nach deutschem Recht (§ 195 BGB).
Die Organisation muss diese Fristen an ihre eigenen gesetzlichen Pflichten anpassen,
insbesondere etwaige Anforderungen der Agentur fuer Arbeit hinsichtlich des
Nachweises der Begleitung.

### 5.2 Loeschverfahren (Loeschkonzept)

Die Loesung verfuegt ueber keine automatische Datenloeeschung. Die Organisation ist
verantwortlich fuer die Einrichtung eines geeigneten Verfahrens.

**Option 1 - Manuelle Loeeschung:**

Wenn ein Teilnehmer seine Massnahme abschliesst (Status wechselt auf "beendet"),
fuehrt der Administrator nach Ablauf der Speicherfrist folgende Schritte durch:

1. Loeschung des Eintrags in der Liste "Participants"
2. Loeschung des zugehoerigen Eintrags in "Profils" (Filterung nach id_participant)
3. Loeschung aller zugehoerigen Eintraege in "BilansMensuels" (Filterung nach id_participant)
4. Loeschung oder Archivierung des PDF-Ordners in der Bibliothek "TransferMappes"

**Option 2 - Halbautomatische Loeeschung (empfohlen):**

Erstellung eines woechentlich geplanten Power Automate-Flows, der:

1. Alle Teilnehmereintraege mit dem Status "beendet" abruft,
   deren Enddatum die konfigurierte Speicherfrist ueberschreitet
2. Die zugehoerigen Eintraege in allen drei Listen loescht
3. Einen Loeeschbericht an den Administrator sendet

Dieser ergaenzende Flow ist im Kit v0.1 nicht enthalten. Seine Entwicklung ist
im BACKLOG.md fuer eine spaeaetere Version vorgesehen.

**Option 3 - SharePoint-Aufbewahrungsrichtlinie:**

Microsoft 365 bietet konfigurierbare Aufbewahrungsrichtlinien ueber das
Microsoft Purview Compliance Center. Die Organisation kann eine Aufbewahrungsrichtlinie
fuer die SharePoint-Website TransferMappe mit automatischer Loeeschung nach der
gewaehlten Frist konfigurieren. Diese Option erfordert keine zusaetzliche Entwicklung,
setzt jedoch eine Microsoft 365-Lizenz mit Microsoft Purview voraus (in E3 verfuegbar).

### 5.3 Recht auf Loeeschung (Art. 17 DSGVO)

Bei einer Loeeschungsanfrage eines Teilnehmers wird das manuelle Verfahren (Option 1)
unverzueglich angewendet, ohne Ablauf der Speicherfrist. Siehe Abschnitt 6.

---

## 6. Rechte der betroffenen Personen

Teilnehmer haben gemaess Art. 15 bis 22 DSGVO folgende Rechte. Die Organisation
traegt die alleinige Verantwortung fuer deren Umsetzung.

### 6.1 Auskunftsrecht (Art. 15 DSGVO)

Der Teilnehmer kann eine Kopie aller seiner Daten anfordern. Der Administrator:

1. Exportiert den Eintrag aus der Liste "Participants" (CSV-Export ueber SharePoint)
2. Exportiert den Eintrag aus der Liste "Profils"
3. Exportiert alle Eintraege aus "BilansMensuels" fuer die entsprechende id_participant
4. Stellt das oder die generierten PDFs aus der Bibliothek "TransferMappes" bereit

### 6.2 Recht auf Berichtigung (Art. 16 DSGVO)

Der Administrator oder die Beraterin kann Eintraege direkt in den SharePoint-Listen
aendern. Die Versionierung ist fuer alle drei Listen aktiviert (Parameter
"versioning: true" im Schema), was eine Aufbewahrung des Aenderungsverlaufs ermoeglicht.

### 6.3 Recht auf Loeeschung (Art. 17 DSGVO)

Das unter Abschnitt 5.2 (Option 1) beschriebene manuelle Loeschverfahren ist anzuwenden.
Die Anfrage und die durchgefuehrte Massnahme sind zur Nachweisfuehrung zu dokumentieren.

Hinweis: Das Recht auf Loeeschung kann eingeschraenkt sein, wenn die Organisation
Begleitnachweise fuer die Agentur fuer Arbeit aufbewahren muss. In diesem Fall muss
die Organisation den Teilnehmer ueber den Grund der partiellen Ablehnung informieren
(Art. 17 Abs. 3 DSGVO).

### 6.4 Recht auf Einschraenkung der Verarbeitung (Art. 18 DSGVO)

Der Administrator setzt den Status des Teilnehmers in der Liste "Participants"
auf "gesperrt". Der Einladungs-Flow und der PDF-Generierungs-Flow schliessen automatisch
Teilnehmer aus, deren Status nicht "aktiv" ist. Es werden damit keine neuen Daten erzeugt.

### 6.5 Recht auf Datenuebertragbarkeit (Art. 20 DSGVO)

Die SharePoint-Listen ermoeglichten den Export im CSV-Format ueber die Standard-Oberflaeche.
Die generierten PDFs sind unmittelbar portierbar. Die Organisation kann dem Teilnehmer
auf Anfrage saemtliche Daten in diesen Standardformaten bereitstellen.

### 6.6 Widerspruchsrecht (Art. 21 DSGVO)

Im Kontext des SGB III ist das Widerspruchsrecht angesichts der vertraglichen
Rechtsgrundlage (Art. 6 Abs. 1 lit. b DSGVO) eingeschraenkt. Die Organisation muss
ihren DSB konsultieren, um zu bestimmen, in welchen Faellen ein Widerspruch zulaessig ist.

### 6.7 Kommunikationskanal fuer Anfragen

Die Organisation muss einen Kommunikationskanal fuer Betroffenenanfragen festlegen
und den Teilnehmern mitteilen (E-Mail an den DSB, Online-Formular, postalischer Weg).
Dieser Kanal muss in der Datenschutzinformation an die Teilnehmer enthalten sein
(siehe Abschnitt 11).

---

## 7. Technische und organisatorische Massnahmen (TOM)

### 7.1 In der Loesung integrierte Massnahmen

Folgende Massnahmen sind durch Konstruktion in outplacement-tracker umgesetzt:

| Massnahme | Umsetzung | Ebene |
|---|---|---|
| Datenverbleib im Tenant | Keine Daten verlassen den M365-Tenant - keine externe API, kein Drittanbieter-Connector | Architekturimmanent |
| Datensparsamkeit | 7 von 10 Feldern in BilansMensuels sind optional - kein Bewerbungs-Tracking | Konstruktionsbedingt |
| Datentrennung nach Organisation | Ein Tenant = eine Organisation - keine Zusammenfuehrung durch Konstruktion moeglich | Architekturimmanent |
| SharePoint-Versionierung | Vollstaendiger Aenderungsverlauf aller drei Listen | Im Schema aktiviert |
| Rollenbasierter SharePoint-Zugriff | Die Listen sind in einer SharePoint-Website mit konfigurierbaren Berechtigungen gehostet | Zu konfigurieren (siehe 7.2) |
| Keine PII in Einladungs-E-Mails | Die Teilnehmer-E-Mail enthaelt nur Vorname, Nachname, Termindatum und Forms-Link - kein Klartextverlauf | In den Templates umgesetzt |
| Power Automate-Ausfuehrungsprotokolle | Jede Ausfuehrung wird im Power Automate-Verlauf des Tenants protokolliert | Nativer M365-Standard |

### 7.2 Von der Organisation umzusetzende Massnahmen

Diese Massnahmen liegen in der Verantwortung der einsetzenden Organisation.

**Vor der Inbetriebnahme zwingend erforderlich:**

| Massnahme | Erforderliche Aktion | Referenz |
|---|---|---|
| Multi-Faktor-Authentifizierung (MFA) | MFA fuer alle Konten aktivieren, die Zugriff auf die SharePoint-Website TransferMappe haben | Microsoft Entra ID - Richtlinie fuer bedingten Zugriff |
| Eingeschraenkte SharePoint-Berechtigungen | Die Website TransferMappe muss privat sein - nur Beraterinnen und Administratoren als Mitglieder | SharePoint-Administration - Gruppenrechte |
| Freigegebenes Postfach als Absender | Freigegebenes Postfach anlegen (z.B. transfer@domain.de) - keine persoenliche Mitarbeiteradresse verwenden | Exchange Online - Administration |
| DLP (Data Loss Prevention) | DLP-Richtlinie konfigurieren, die die externe Weitergabe der SharePoint-Listen mit PII verhindert | Microsoft Purview - DLP-Richtlinien |
| Zugriff auf das Power Automate-Portal | Zugriff auf das Power Automate-Portal auf benannte Administratoren beschraenken | Microsoft Entra ID - Rollen |
| Information der Teilnehmer (Art. 13 DSGVO) | Datenschutzinformation an jeden Teilnehmer vor seiner Aufnahme in die Loesung aushaaendigen | DSGVO-Rechtspflicht |

**Dringend empfohlen:**

| Massnahme | Erforderliche Aktion | Referenz |
|---|---|---|
| Regelmaessige Zugriffsueberprueefung | Vierteljaehrliche Pruefung der Mitglieder der SharePoint-Gruppe TransferMappe | M365-Administration - Zugriffsueberprueefungen |
| M365-Auditprotokoll | M365-Auditprotokolle aktivieren und aufbewahren (SharePoint, Exchange, Power Automate) | Microsoft Purview - Audit |
| SharePoint-Sicherung | Microsoft 365 Backup oder eine zertifizierte Drittloesung aktivieren | Microsoft 365 Backup |
| Schulung der Beraterinnen | Nutzer in den bewaaehrten Praktiken der Datenverarbeitung in SharePoint schulen | Intern |
| Passwortrichtlinie | Eine Passwortrichtlinie gemaess BSI-Empfehlungen anwenden (mindestens 12 Zeichen) | Microsoft Entra ID |

---

## 8. Auftragsverarbeiter

### 8.1 Microsoft Corporation

Microsoft ist der einzige Auftragsverarbeiter im Rahmen dieser Loesung.

| Element | Detail |
|---|---|
| Bezeichnung | Microsoft Corporation |
| DSGVO-Rolle | Auftragsverarbeiter - Art. 4 Nr. 8 und Art. 28 DSGVO |
| Grundlage des AVV | Microsoft Online Services Data Processing Agreement (DPA), akzeptiert bei der M365-Buchung |
| Betroffene Dienste | SharePoint Online, Power Automate, Microsoft Forms, Exchange Online, Word Online |
| Datenzugriff | Microsoft greift nicht auf Inhalte zu, ausser auf Weisung der Organisation oder aufgrund gesetzlicher Verpflichtung |
| Zertifizierungen | ISO 27001, ISO 27018, SOC 1/2/3, branchenspezifische Zertifizierungen verfuegbar |

Die Organisation muss keinen zusaetzlichen AVV mit Microsoft abschliessen: Der Microsoft
Online Services DPA wird bei der M365-Buchung akzeptiert und deckt alle von dieser
Loesung genutzten Dienste ab.

Der Microsoft Online Services DPA ist verfuegbar unter:
https://www.microsoft.com/en-us/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA

### 8.2 Keine weiteren Auftragsverarbeiter

outplacement-tracker nutzt:

- keine externen Dritt-APIs (Analytics, Monitoring, KI, Uebersetzung usw.)
- keine Premium-Power-Automate-Connectoren, die Drittdienste einbinden
- keine von dem M365-Tenant der Organisation getrennte Hosting-Infrastruktur
- keine Dienste des Projektautors

Jede Weiterentwicklung der Loesung, die einen neuen Drittdienst einfuehrt, muss
einer Datenschutz-Folgenabschaetzung (DSFA, Art. 35 DSGVO) unterzogen werden, sofern
die betroffenen personenbezogenen Daten betroffen sind.

---

## 9. Datenuebermittlungen ausserhalb der Europaeischen Union

### 9.1 Datenhaltung bei Microsoft 365

Standardmaessig speichern Microsoft 365-Tenants, deren Region auf Europa konfiguriert ist,
Daten im Ruhezustand (Data at Rest) in den europaeischen Rechenzentren von Microsoft
(hauptsaechlich Niederlande und Irland, mit Sekundaerstandorten in Finnland und Oesterreich).

Microsoft hat die EU Data Boundary eingefuehrt, die gewaehrleistet, dass Daten der
meisten M365-Dienste (darunter SharePoint, Exchange, Power Automate) in Europa verbleiben -
einschliesslich Betriebs- und Diagnosevorgaengen. Dieser Perimeter gilt fuer M365-E3-Lizenzen
mit der Region Europaeische Union bei der Tenant-Erstellung.

Zur Pruefung der Tenant-Region: M365-Verwaltungsportal > Einstellungen >
Organisationsprofil > Land oder Region der Daten.

### 9.2 Keine Datenuebermittlung durch die Loesung

outplacement-tracker uebermittelt keine Daten ausserhalb des Microsoft 365-Tenants
der Organisation. Die Loesung kontaktiert keine externen Dienste.

### 9.3 Bei Unsicherheit ueber den Datenspeicherort

Wenn die Organisation nicht bestaetigen kann, dass ihr Tenant auf die Region EU
konfiguriert ist, muss sie dies vor dem Deployment pruefen und korrigieren. Ohne
Gewaehr fuer den Datenspeicherort koennte eine Uebermittlung in ein Drittland ohne
angemessene Rechtsgrundlage stattfinden (Art. 44 bis 49 DSGVO), was einen Verstoss
darstellen wuerde.

---

## 10. Benennung eines Datenschutzbeauftragten (DSB)

### 10.1 Wahrscheinliche Pflicht fuer Transfergesellschaften

Art. 37 DSGVO verpflichtet zur Benennung eines DSB in mehreren Faellen, darunter:

- wenn die Verarbeitung von einer Behoerde oder oeffentlichen Stelle durchgefuehrt wird
  (Art. 37 Abs. 1 lit. a DSGVO)
- wenn die Kerntaetigkeit in der umfangreichen regulaeren und systematischen
  Ueberwachung betroffener Personen besteht (Art. 37 Abs. 1 lit. b DSGVO)

Eine Transfergesellschaft, die gleichzeitig 1.500 bis 2.000 Teilnehmer betreut,
fuehrt mit grosser Wahrscheinlichkeit eine umfangreiche Verarbeitung mit regelmaessiger
Ueberwachung der betroffenen Personen durch. Die Pflicht zur Benennung eines DSB
ist damit aller Voraussicht nach gegeben.

Die nationale Ergaenzung durch § 38 BDSG verpflichtet ebenfalls zur Benennung eines
DSB, wenn die Organisation mindestens 20 Personen beschaeftigt, die staendig mit der
automatisierten Verarbeitung personenbezogener Daten befasst sind.

### 10.2 Rolle des DSB beim Deployment dieser Loesung

Der DSB der Organisation muss eingebunden werden:

- bei der Aktualisierung des Verzeichnisses der Verarbeitungstaetigkeiten (VVT, Abschnitt 11)
- bei der Erstellung der Datenschutzinformation fuer die Teilnehmer (Art. 13 DSGVO)
- bei der Pruefung der Notwendigkeit einer DSFA (Art. 35 DSGVO)
- bei regelmaessigen Zugriffs- und Sicherheitsueberpruefungen

---

## 11. Compliance-Checkliste vor dem Deployment

Die Organisation muss folgende Massnahmen vor der Inbetriebnahme der Loesung durchfuehren.

### 11.1 Zwingend erforderliche Massnahmen

- [ ] Pruefen, dass die Region des M365-Tenants auf die Europaeische Union konfiguriert ist
- [ ] SharePoint-Berechtigungen der Website TransferMappe auf privaten Zugriff konfigurieren
      (Mitgliedergruppe: nur Beraterinnen und Administratoren)
- [ ] MFA fuer alle Konten aktivieren, die Zugriff auf die SharePoint-Website TransferMappe haben
- [ ] Das freigegebene Absenderpostfach anlegen (z.B. transfer@domain.de) und
      jede persoenliche Adresse aus den Flow-Variablen entfernen
- [ ] Das Verzeichnis der Verarbeitungstaetigkeiten der Organisation (Art. 30 DSGVO)
      aktualisieren und diese Verarbeitungstaetigkeit erhaenzen
- [ ] Eine Datenschutzinformation fuer die Teilnehmer gemaess Art. 13 DSGVO erstellen
      und vor ihrer Aufnahme in die Loesung aushaaendigen; sie muss insbesondere enthalten:
      die erfassten Datenkategorien, die Zwecke, die Rechtsgrundlage,
      die Speicherfrist, die Betroffenenrechte und den DSB-Kontakt
- [ ] Das Loeschverfahren fuer Daten am Ende der Massnahme festlegen und dokumentieren
- [ ] Den DSB der Organisation in die Umsetzung einbeziehen
- [ ] Word-Template-Metadaten neutralisieren: die .docx-Datei vor dem Upload in SharePoint
      auf persoenliche Autorenangaben pruefen und bereinigen (Datei > Informationen >
      Auf Probleme pruefen > Dokument pruefen in Word)

### 11.2 Empfohlene Massnahmen

- [ ] Die Notwendigkeit einer DSFA (Datenschutz-Folgenabschaetzung, Art. 35 DSGVO)
      angesichts des Teilnehmervolumens und der Art der Begleitung bewerten
- [ ] Eine DLP-Richtlinie in Microsoft Purview fuer die SharePoint-Website TransferMappe konfigurieren
- [ ] M365-Auditprotokolle aktivieren und gemaess interner Richtlinie aufbewahren
- [ ] Eine Zugriffsueberprueefung fuer SharePoint mindestens einmal jaehrlich planen
- [ ] Das Verfahren zur Bearbeitung von Betroffenenanfragen dokumentieren
      (Frist 1 Monat, Art. 12 Abs. 3 DSGVO)
- [ ] Beraterinnen in guten Praktiken schulen: keine Kopie von Teilnehmerdaten
      auf privaten Geraeten, keine Weitergabe per ungesicherter E-Mail usw.

### 11.3 Anpassung der Konfiguration

- [ ] Konfigurationswerte der Flows (varSiteUrl, varSharedMailbox usw.)
      durch die tatsaechlichen Werte der Organisation vor der Aktivierung ersetzen
- [ ] E-Mail-Templates anpassen (Logo, Organisationsname, Kontaktdaten)
- [ ] Word-PDF-Template anpassen (Logo, Corporate Design), falls abweichend von 10 k Beratung

---

## 12. Datensparsamkeit: Gestaltungsprinzipien

Die Loesung wurde im Einklang mit dem Grundsatz der Datensparsamkeit und Zweckbindung
(Art. 5 Abs. 1 lit. c und e DSGVO) entwickelt. Folgende Gestaltungsentscheidungen belegen dies:

**Monatliches Formular (Microsoft Forms):**

- 6 Felder insgesamt, davon 5 optional
- Der Teilnehmer entscheidet frei, was er mitteilen moechte
- Kein Feld zur Verfolgung einzelner Bewerbungen
- Kein Feld fuer Arbeitgeberkontakte
- Kein Scoring oder Bewertungsmechanismus fuer Teilnehmer

**SharePoint-Listen:**

- Keine Finanzdaten (Gehalt, Abfindung, Hoehe der Leistungen)
- Keine Gesundheits- oder medizinischen Daten
- Keine Angaben zu den Gruenden der Kuendigung (Verhaeltnis zum frueheren Arbeitgeber)
- Kein Foto, kein Ausweisdokument, keine biometrischen Daten

**Automatische E-Mails:**

- Die Einladungs-E-Mail enthaelt nur Vorname, Nachname, Termindatum und den Forms-Link
- Die E-Mail an die Beraterin enthaelt das PDF als Anlage, jedoch keinen Datenverlauf
  im Klartext im Nachrichtenkoerper
- Keine persoenliche E-Mail-Adresse des Projektautors erscheint in den Templates

**Generiertes PDF:**

- Das PDF enthaelt ausschliesslich die in den Formularen eingegebenen Daten
- Es enthaelt keine versteckten persoenlichen Metadaten (die Word-Metadaten der .docx-Vorlage
  sind vom Administrator vor dem Upload zu pruefen und zu bereinigen)
- Es wird nur an die zustaendige Beraterin uebermittelt, nicht an das gesamte Team

**Einsichtnahme durch den Teilnehmer:**

- Der Teilnehmer gibt seine Monatsberichte selbst ueber Microsoft Forms ein
- Er kann sich an seine Beraterin wenden, um eine Kopie seiner Daten zu erhalten
- Er kann sein Recht auf Berichtigung durch Information an seine Beraterin oder den Administrator ausueben

---

## 13. Revisionshistorie

| Version | Datum | Aenderungen |
|---|---|---|
| 1.0 | 2026-05-05 | Erstfassung (franzoesisch) |
| 1.1 | 2026-05-06 | Vollstaendige Neufassung auf Deutsch (ADR-007) |
