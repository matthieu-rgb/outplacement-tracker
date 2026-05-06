# SharePoint Schema - outplacement-tracker v0.1

Schema der drei SharePoint-Listen, die die Datenbasis der Lösung bilden.

Konventionen:
- Listennamen: PascalCase
- Spaltennamen: snake_case
- Typen: Microsoft SharePoint-Notation (PnP PowerShell)
- Alle Daten verbleiben im Tenant des Kunden (ADR-001)

---

## Liste 1: Participants

**Funktion**: eine Zeile pro begleitetem Teilnehmer. Zentrale Tabelle, Dreh- und Angelpunkt der gesamten Lösung.

**Listen-URL**: `{SiteURL}/Lists/Participants`

| Spalte               | SharePoint-Typ        | Pflichtfeld  | Standardwert       | Zulässige Werte / Einschränkungen                        | Hinweise                                                   |
|----------------------|-----------------------|--------------|--------------------|----------------------------------------------------------|------------------------------------------------------------|
| `id`                 | ID (auto, built-in)   | ja (auto)    | -                  | Automatisch inkrementierte Ganzzahl                      | Nativer Primärschlüssel von SharePoint                     |
| `nom`                | Single line of text   | ja           | -                  | Max. 255 Zeichen                                         | Nachname                                                   |
| `prenom`             | Single line of text   | ja           | -                  | Max. 255 Zeichen                                         | Vorname                                                    |
| `email`              | Single line of text   | ja           | -                  | Gültiges E-Mail-Format, max. 255 Zeichen                 | Eindeutige Kontaktadresse pro Teilnehmer                   |
| `langue`             | Choice                | ja           | `DE`               | `DE` / `EN`                                             | Bestimmt die Sprache der Formulare, E-Mails und des Word-Templates |
| `id_conseillere`     | Single line of text   | ja           | -                  | E-Mail-Adresse der Beraterin (M365-Konto)                | Wird für die Weiterleitung des kumulativen PDFs verwendet  |
| `date_debut_parcours`| Date and Time         | ja           | -                  | Datum ohne Uhrzeit, Format ISO 8601                      | Wird zur Berechnung des Begleitungsendes verwendet (max. +12 Monate) |
| `date_prochain_rdv`  | Date and Time         | ja           | -                  | Datum ohne Uhrzeit, Format ISO 8601                      | Auslöser des Flow J-5 (Einladung) und Flow J (PDF)         |
| `statut`             | Choice                | ja           | `actif`            | `actif` / `suspendu` / `termine`                        | `suspendu` = vorübergehende Pause, `termine` = abgeschlossener Begleitungsprozess |
| `Title`              | Single line of text   | ja           | -                  | Format: "{prenom} {nom}"                                | Wird automatisch vom Flow bei der Erstellung befüllt. Dient als lesbares Label in SharePoint-Ansichten. |

**Empfohlene Indizes**:
- `email`: Index für schnelle Suche durch den Flow
- `statut`: Index zur Filterung aktiver Teilnehmer
- `date_prochain_rdv`: Index für den geplanten Auslöser des Flows

**DSGVO-Hinweis**: `email` ist ein direkt identifizierendes personenbezogenes Datum. Die Erhebung ist durch den Verarbeitungszweck gerechtfertigt (Versand des monatlichen Formulars). Es sind keine weiteren identifizierenden Felder vorhanden (keine Sozialversicherungsnummer, kein Geburtsdatum, keine Vorgangsnummer der Agentur für Arbeit).

---

## Liste 2: Profils

**Funktion**: optionales Karriereprofil, einmalig zu Beginn des Begleitungsprozesses über das Onboarding-Formular erfasst. Null oder ein Profil pro Teilnehmer.

**Listen-URL**: `{SiteURL}/Lists/Profils`

| Spalte                 | SharePoint-Typ        | Pflichtfeld  | Standardwert      | Zulässige Werte / Einschränkungen | Hinweise                                                             |
|------------------------|-----------------------|--------------|-------------------|-----------------------------------|----------------------------------------------------------------------|
| `id`                   | ID (auto, built-in)   | ja (auto)    | -                 | Automatisch inkrementierte Ganzzahl | Primärschlüssel                                                    |
| `id_participant`       | Number                | ja           | -                 | Ganzzahl >= 1                     | Fremdschlüssel zu `Participants.id`                                  |
| `plan_a`               | Multiple lines of text| nein         | -                 | Freitext, max. 3.000 Zeichen      | Berufliches Hauptziel (Berufliche Zielsetzung Plan A)                |
| `plan_b`               | Multiple lines of text| nein         | -                 | Freitext, max. 3.000 Zeichen      | Berufliches Alternativziel (Plan B)                                  |
| `marketingplan`        | Multiple lines of text| nein         | -                 | Freitext, max. 3.000 Zeichen      | Positionierung, Kernkompetenzen, USP des Teilnehmers                 |
| `zielmarkt`            | Multiple lines of text| nein         | -                 | Freitext, max. 3.000 Zeichen      | Angestrebte Region, Branche, Unternehmensgröße                       |
| `date_creation`        | Date and Time         | ja           | `[now]`           | Datum + Uhrzeit ISO 8601          | Wird automatisch vom Onboarding-Flow befüllt                         |
| `date_modification`    | Date and Time         | nein         | -                 | Datum + Uhrzeit ISO 8601          | Wird aktualisiert, wenn der Teilnehmer das Onboarding-Formular erneut einreicht |
| `Title`                | Single line of text   | ja           | -                 | Format: "Profil - {prenom_participant} {nom_participant}" | Wird automatisch vom Flow bei der Erstellung befüllt. Dient als lesbares Label in SharePoint-Ansichten. |

**Empfohlene Indizes**:
- `id_participant`: Index für den Lookup durch den Flow

**DSGVO-Hinweis**: Die Felder `plan_a`, `plan_b`, `marketingplan`, `zielmarkt` enthalten Informationen über die beruflichen Ziele des Teilnehmers. Rechtsgrundlage ist die Einwilligung des Teilnehmers (das Formular ist optional, ADR-003). Diese Daten sind nicht zur Weitergabe außerhalb des Teilnehmer-Berater-Tandems bestimmt.

---

## Liste 3: BilansMensuels

**Funktion**: ein Datensatz pro eingereichtem Monatsbericht. Null bis 12 Berichte pro Teilnehmer (ADR-004, A1).

**Listen-URL**: `{SiteURL}/Lists/BilansMensuels`

| Spalte                           | SharePoint-Typ        | Pflichtfeld  | Standardwert      | Zulässige Werte / Einschränkungen                                                        | Hinweise                                                               |
|----------------------------------|-----------------------|--------------|-------------------|------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| `id`                             | ID (auto, built-in)   | ja (auto)    | -                 | Automatisch inkrementierte Ganzzahl                                                      | Primärschlüssel                                                        |
| `id_participant`                 | Number                | ja           | -                 | Ganzzahl >= 1                                                                            | Fremdschlüssel zu `Participants.id`                                    |
| `date_rdv`                       | Date and Time         | ja           | -                 | Datum ISO 8601                                                                           | Datum des Termins, dem dieser Bericht zugeordnet ist                   |
| `date_soumission`                | Date and Time         | ja           | `[now]`           | Datum + Uhrzeit ISO 8601                                                                 | Wird automatisch vom Flow zum Zeitpunkt der Forms-Einreichung befüllt  |
| `bilan_general`                  | Multiple lines of text| ja           | -                 | Freitext, max. 5.000 Zeichen                                                             | Einziges Pflichtfeld (ADR-003). Freie Zusammenfassung des vergangenen Monats. |
| `statut_objectifs`               | Choice                | nein         | -                 | `vollstaendig_erreicht` / `teilweise_erreicht` / `nicht_erreicht` / `noch_nicht_relevant` | Status der Ziele des Vormonats                                         |
| `statut_objectifs_detail`        | Multiple lines of text| nein         | -                 | Freitext, max. 3.000 Zeichen                                                             | Freie Erläuterung zum Zielstatus                                       |
| `was_lief_gut`                   | Multiple lines of text| nein         | -                 | Freitext, max. 3.000 Zeichen                                                             | Was im Monat gut funktioniert hat                                      |
| `wo_brauche_ich_unterstuetzung`  | Multiple lines of text| nein         | -                 | Freitext, max. 3.000 Zeichen                                                             | Bereiche, in denen der Teilnehmer Unterstützung wünscht                |
| `themen_naechster_termin`        | Multiple lines of text| nein         | -                 | Freitext, max. 3.000 Zeichen                                                             | Themen für den nächsten Termin                                         |
| `sonstige_anmerkungen`           | Multiple lines of text| nein         | -                 | Freitext, max. 3.000 Zeichen                                                             | Sonstige Anmerkungen                                                   |
| `Title`                          | Single line of text   | ja           | -                 | Format: "{date_rdv_ISO} - {prenom_participant} {nom_participant}", Datum im Format YYYY-MM-DD zur Sicherstellung der lexikografischen Sortierung in SharePoint-Ansichten | Wird automatisch vom Flow bei der Erstellung befüllt. Dient als lesbares Label in SharePoint-Ansichten. |

**Empfohlene Indizes**:
- `id_participant`: Index für den Lookup durch den Flow
- `date_rdv`: Index für die chronologische Sortierung bei der PDF-Generierung

**DSGVO-Hinweis**: Die Monatsberichte enthalten sensible personenbezogene Daten zur beruflichen (und möglicherweise persönlichen) Situation des Teilnehmers. Rechtsgrundlage: Erfüllung des Begleitungsvertrags in der Transfergesellschaft. Die Liste ist nur für M365-Konten zugänglich, die vom Administrator autorisiert wurden. Eine externe Weitergabe ist nicht vorgesehen.

---

## Beziehungen zwischen den Listen

```
Participants (id)
    |
    +-- 0..1 Profils (id_participant = Participants.id)
    |
    +-- 0..12 BilansMensuels (id_participant = Participants.id)
```

Hinweis: SharePoint Online unterstützt keine nativen Fremdschlüssel mit referenzieller Integritätsprüfung. Die Beziehungen werden durch die Power Automate Flows verwaltet, die vor dem Einfügen die Existenz der `id_participant` prüfen. Im Fehlerfall stoppt der Flow und sendet eine Benachrichtigung an den Administrator.

---

## Empfohlene Websiteeinstellungen

- **Website-Typ**: SharePoint Communication Site oder dedizierte Team Site (nicht die Stammwebsite)
- **Zugriff**: auf Teammitglieder beschränkt (Beraterinnen + Administrator). Teilnehmer haben keinen direkten Zugriff auf die Website.
- **Versionierung**: Listenversionierung aktivieren (mindestens 5 Versionen) für den Audit Trail
- **Audit**: SharePoint-Auditprotokolle aktivieren (Lesen und Schreiben) für die DSGVO-Konformität
- **Aufbewahrung**: durch die Transfergesellschaft gemäß ihren gesetzlichen Pflichten festzulegen (DSGVO + § 111 SGB III)
