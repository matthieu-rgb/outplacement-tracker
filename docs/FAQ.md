# FAQ - outplacement-tracker

Häufig gestellte Fragen für zwei Zielgruppen: die Beraterinnen, die die Lösung täglich nutzen,
und die IT- / M365-Administratoren, die sie bereitstellen.

---

## Für Beraterinnen

### Wann erhalte ich das PDF?

Der PDF-Generierungsflow erstellt das PDF am Morgen des Termintags und sendet es per E-Mail
an die Beraterin, die im Feld `id_conseillere` des Teilnehmers eingetragen ist. Das PDF wird
außerdem automatisch in der Dokumentbibliothek `TransferMappes` in SharePoint gespeichert.

### Muss der Teilnehmer das Formular ausfüllen?

Nein. Das Feld `bilan_general` (Gesamtbewertung des Monats) ist das einzige Pflichtfeld
im Monatsbericht-Formular. Die fünf weiteren Felder sind optional. Der Teilnehmer entscheidet
selbst, was er mitteilt.

### Was passiert, wenn der Teilnehmer das Formular nicht ausfüllt?

Das PDF wird trotzdem generiert. Es enthält den vollständigen Verlauf der Vorermonate.
Im Abschnitt des laufenden Monats wird angegeben, dass für diesen Zeitraum kein Monatsbericht
eingereicht wurde. Der Termin kann normal stattfinden.

### Kann ich auf die Antworten direkt in SharePoint zugreifen?

Ja, sofern Sie Mitgliedszugriff auf die SharePoint-Website `TransferMappe` haben.
Die Monatsberichte sind in der Liste `BilansMensuels` gespeichert. Profile und Ziele befinden
sich in der Liste `Profils`.

### Ist das PDF nach dem Termin noch zugänglich?

Ja. Jedes generierte PDF wird in der Dokumentbibliothek `TransferMappes` in SharePoint
nach Teilnehmer geordnet gespeichert. Es bleibt zugänglich, solange die Daten des Teilnehmers
nicht gelöscht wurden.

### Kann ein Teilnehmer die Daten anderer Teilnehmer einsehen?

Nein. Teilnehmer haben keinen Zugriff auf die SharePoint-Website. Sie interagieren
ausschließlich über Microsoft Forms-Formulare, die individuell sind und keinen Zugriff
auf andere Daten gewahren.

### Wie kann ich das Formular anpassen, wenn ich zusätzliche Fragen hinzufügen möchte?

Die Anpassung des Formulars erfolgt über die Microsoft Forms-Oberfläche. Nach dem Hinzufügen
einer Frage sind folgende Schritte erforderlich: 1) die entsprechende Spalte in der
SharePoint-Liste `BilansMensuels` hinzufügen, 2) den entsprechenden Content Control in
der Word-Vorlage hinzufügen, 3) die Aktion "Populate" im PDF-Generierungsflow aktualisieren.
Die Benennungskonventionen sind in `specs/sharepoint_schema.md` und `specs/word_template_structure.md`
dokumentiert.

### Ist das Formular in mehreren Sprachen verfügbar?

Ja. Es gibt zwei Versionen des Monatsbericht-Formulars: eine auf Deutsch (DE) und eine
auf Englisch (EN). Die Sprache des an einen Teilnehmer gesendeten Formulars wird durch
das Feld `langue` in der Liste `Participants` bestimmt.

---

## Für die IT / M365-Administration

### Welche Lizenzvoraussetzungen gibt es?

Ein Microsoft 365 E3-Plan oder höher ist erforderlich. Die Lösung verwendet ausschließlich
Standard-Connectoren, die in E3 enthalten sind: SharePoint, Outlook, Word Online Business
und Power Automate (Seeded-Plan). Es werden keine Premium-Connectoren benötigt.

### Wie lange dauert die Bereitstellung?

Zwischen 2 und 4 Stunden für einen kompetenten M365-Administrator, der die Anleitungen
des Kits befolgt. Das PnP PowerShell-Skript stellt die SharePoint-Listen in wenigen
Minuten bereit. Der längste Teil ist die manuelle Erstellung der Flows in Power Automate
(siehe `power_automate/IMPORT_GUIDE.md`).

### Kann die Bereitstellung ohne PowerShell erfolgen?

Technisch ja. Die SharePoint-Listen können manuell über die Weboberfläche erstellt werden.
Das Skript `sharepoint/setup_lists.ps1` wird jedoch dringend empfohlen, da es idempotent ist
und die Konsistenz der Spalten gewährleistet. Die manuelle Alternative ist in
`specs/sharepoint_schema.md` dokumentiert.

### Benötigt das Kit eine Azure AD-Anwendungsregistrierung?

Nein. Die Power Automate-Flows verwenden ausschließlich Standard-Connectoren, die sich
über das Administratordienstkonto authentifizieren. Eine Anwendungsregistrierung in
Azure AD ist nicht erforderlich.

### Wie werden die Word-Vorlagen aktualisiert?

Die neue `.docx`-Datei in die SharePoint-Bibliothek unter
`/sites/TransferMappe/TransferMappes/Templates/` hochladen. Die Flows lesen die Datei
bei jeder Ausführung: Die Aktualisierung wird sofort übernommen, ohne die Flows ändern
zu müssen. Die Tag-Werte der Content Controls müssen unverändert bleiben, solange die
Struktur beibehalten wird.

### Was passiert, wenn ein Flow fehlschlägt?

Beide Flows senden eine Fehler-E-Mail an die in der Variablen `varAdminEmail` konfigurierte
Administratoradresse. Den vollständigen Ausführungsverlauf finden Sie in Power Automate
unter **Power Automate > Meine Flows** > den Flow auswählen > "Ausführungsverlauf (28 Tage)".

### Kann der Zugriff auf bestimmte Beraterinnen eingeschränkt werden?

Ja. Die SharePoint-Berechtigungen werden auf Ebene der Website und der Listen verwaltet.
Jede Beraterin kann auf ihre eigenen Teilnehmer beschrankt werden, indem gefilterte
Ansichten auf `id_conseillere` mit eingeschränkten Berechtigungen kombiniert werden.
Für eine strikte Segmentierung werden separate SharePoint-Gruppen pro Beraterin empfohlen.
Siehe die Microsoft-Dokumentation zu SharePoint-Berechtigungen.

### Wie werden die Daten eines Teilnehmers nach Abschluss des Beratungsprozesses gelöscht?

Die Daten verteilen sich auf 3 SharePoint-Listen (`Participants`, `Profils`, `BilansMensuels`)
und die Dokumentbibliothek `TransferMappes` (PDFs). Die manuelle Löschung ist über die
SharePoint-Oberfläche möglich. Ein automatischer Losch-Flow, der nach Ablauf der
Aufbewahrungsfrist ausgelost wird, ist in `BACKLOG.md` (v0.2) dokumentiert.

### Ist die Lösung DSGVO-konform?

Die Lösung wird im Microsoft 365-Tenant des Kunden bereitgestellt. Es werden keine Daten
außerhalb des Tenants übertragen. Die Organisation, die die Lösung bereitstellt, ist
Verantwortlicher im Sinne der DSGVO und trägt die vollständige Verantwortung für die
Erfüllung der Compliance-Anforderungen. Details zu den erhobenen Daten, den anwendbaren
Rechtsgrundlagen und dem Verantwortlichkeitsmodell finden Sie in `docs/PRIVACY.md`.

### Können mehrere Beraterinnen für verschiedene Teilnehmer zuständig sein?

Ja. Das Feld `id_conseillere` wird individuell für jeden Teilnehmer in der Liste `Participants`
ausgefüllt. Jeder Teilnehmer kann einer anderen Beraterin zugewiesen werden. Der
PDF-Generierungsflow sendet das PDF an die Adresse `id_conseillere` des jeweiligen Teilnehmers.
