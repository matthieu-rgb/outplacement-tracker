# Flow 1 : Einladung J-5

outplacement-tracker v0.1 - Implementierungsanleitung (Blueprint ohne Tenant)

Dieses Dokument ermoeglicht einem Microsoft 365-Administrator, diesen Flow
von Grund auf neu zu erstellen, Aktion fuer Aktion, ohne JSON-Import.

---

## Uebersicht

| Parameter | Wert |
|---|---|
| Name des Flows | TransferMappe - Invitation J-5 |
| Ausloeseer | Geplant (taeglich um 07:00 Uhr) |
| Funktion | Fuer jeden aktiven Teilnehmer mit einem Termin in 5 Tagen eine Einladungs-E-Mail mit dem Link zum entsprechenden Forms-Formular senden |
| Haeufigkeit | Taeglich |
| Erforderliche Verbindungen | SharePoint, Office 365 Outlook |

---

## Schritt 1 : Flow erstellen

1. Auf make.powerautomate.com gehen
2. "Erstellen" > "Geplanter Cloud-Flow" anklicken
3. Folgendes eingeben :
   - Name : `TransferMappe - Invitation J-5`
   - Startzeit : `07:00`
   - Wiederholen alle : `1 Tag`
4. "Erstellen" anklicken

---

## Schritt 2 : Konfigurationsvariablen

Am Anfang des Flows 4 Aktionen "Variable initialisieren" hinzufuegen (eine je Variable).

| Variablenname | Typ | Anfangswert | Beschreibung |
|---|---|---|---|
| varSiteUrl | String | `https://{tenant}.sharepoint.com/sites/TransferMappe` | URL der SharePoint-Website - {tenant} ersetzen |
| varSharedMailbox | String | `transfer@{domaine}.de` | Absenderadresse - vom Administrator konfiguriertes Shared Mailbox |
| varFormUrlDE | String | `{URL des monatlichen Berichtsformulars DE}` | Aus Formular 3 kopieren (siehe forms_construction_guide.md) |
| varFormUrlEN | String | `{URL des monatlichen Berichtsformulars EN}` | Aus Formular 4 kopieren |

---

## Schritt 3 : Zieldatum berechnen (heute + 5 Tage)

- Aktion : **Verfassen** (Datenvorgaenge > Verfassen)
- Name der Aktion : `Datum_berechnen`
- Eingaben (Ausdruck) :

```
addDays(utcNow(), 5, 'yyyy-MM-dd')
```

Dieser Ausdruck gibt das Datum in 5 Tagen im Format `YYYY-MM-DD` zurueck (z.B. `2026-05-10`).

---

## Schritt 4 : Aktive Teilnehmer mit Termin in 5 Tagen abrufen

- Aktion : **Elemente abrufen** (SharePoint > Elemente abrufen)
- Name der Aktion : `Get_participants_J5`
- Website : `variables('varSiteUrl')`
- Listenname : `Participants`
- Abfrage filtern (OData) :

```
statut eq 'actif' and date_prochain_rdv eq '@{outputs('Datum_berechnen')}'
```

Hinweis : Der Datumswert muss genau dem in SharePoint gespeicherten Format entsprechen (DateOnly ISO 8601). Wenn die Spalte `date_prochain_rdv` eine Uhrzeit enthaelt (auch 00:00:00Z), den Filter entsprechend anpassen oder `startswith` verwenden.

- Maximale Anzahl von Elementen : `100` (entsprechend dem Teilnehmervolumen anpassen)

---

## Schritt 5 : Fuer jeden Teilnehmer (Apply to each)

- Aktion : **Auf jedes anwenden** (Steuerung > Auf jedes anwenden)
- Name der Aktion : `Fuer_jeden_Teilnehmer`
- Eingabe : `value` der Aktion `Get_participants_J5`

### Aktion 5.1 : Bedingung fuer die Sprache

- Aktion : **Bedingung** (Steuerung > Bedingung)
- Name der Aktion : `Bedingung_Sprache`
- Bedingung :

```
items('Fuer_jeden_Teilnehmer')?['langue']
```

... ist gleich ...

```
EN
```

#### Zweig "Wenn ja" (Sprache EN)

Weiter zu Aktion 5.2 mit :
- `varFormUrl` = `variables('varFormUrlEN')`
- E-Mail-Vorlage = Vorlage 2 (EN)

#### Zweig "Wenn nein" (Sprache DE, Standardwert)

Weiter zu Aktion 5.2 mit :
- `varFormUrl` = `variables('varFormUrlDE')`
- E-Mail-Vorlage = Vorlage 1 (DE)

### Aktion 5.2 : Einladungs-E-Mail senden

Diese Aktion in **jedem** der beiden Zweige (ja/nein) der Bedingung anlegen.

- Aktion : **E-Mail senden (V2)** (Office 365 Outlook > E-Mail senden (V2))
- Name der Aktion : `Einladung_senden_DE` oder `Einladung_senden_EN`
- Von (From) : `variables('varSharedMailbox')`
- An (To) : `items('Fuer_jeden_Teilnehmer')?['email']`

**Version DE - Betreff :**

```
Ihr nächster Beratungstermin am @{formatDateTime(items('Fuer_jeden_Teilnehmer')?['date_prochain_rdv'], 'dd.MM.yyyy')} - Bitte Kurzbericht ausfüllen
```

**Version DE - Inhalt (HTML) :**

```html
<!DOCTYPE html>
<html lang="de">
<body style="font-family: Arial, sans-serif; font-size: 14px; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px;">

  <p>Guten Tag @{items('Fuer_jeden_Teilnehmer')?['prenom']} @{items('Fuer_jeden_Teilnehmer')?['nom']},</p>

  <p>Ihr nächster Beratungstermin findet am <strong>@{formatDateTime(items('Fuer_jeden_Teilnehmer')?['date_prochain_rdv'], 'dd.MM.yyyy')}</strong> statt.</p>

  <p>Um diesen Termin optimal vorzubereiten, bitten wir Sie, bis zum Vortag kurz folgende Fragen zu beantworten (ca. 5 Minuten):</p>

  <p style="text-align: center; margin: 30px 0;">
    <a href="@{variables('varFormUrlDE')}"
       style="background-color: #003DA5; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">
      Zum Monatsbericht
    </a>
  </p>

  <p style="font-size: 12px; color: #666666;">Nur die erste Frage ist Pflichtangabe. Alle anderen Felder sind freiwillig.</p>

  <p>Wenn Sie Fragen haben oder den Termin verschieben müssen, wenden Sie sich bitte an Ihre Beraterin.</p>

  <p>Mit freundlichen Grüßen,<br>Ihr Transfer-Team</p>

  <hr style="border: none; border-top: 1px solid #dddddd; margin: 30px 0;">
  <p style="font-size: 11px; color: #999999;">Diese E-Mail wurde automatisch generiert. Bitte antworten Sie nicht direkt auf diese Nachricht.</p>

</body>
</html>
```

**Version EN - Betreff :**

```
Your next appointment on @{formatDateTime(items('Fuer_jeden_Teilnehmer')?['date_prochain_rdv'], 'dd.MM.yyyy')} - Please complete your monthly update
```

**Version EN - Inhalt (HTML) :**

```html
<!DOCTYPE html>
<html lang="en">
<body style="font-family: Arial, sans-serif; font-size: 14px; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px;">

  <p>Dear @{items('Fuer_jeden_Teilnehmer')?['prenom']} @{items('Fuer_jeden_Teilnehmer')?['nom']},</p>

  <p>Your next appointment with your advisor is scheduled for <strong>@{formatDateTime(items('Fuer_jeden_Teilnehmer')?['date_prochain_rdv'], 'dd.MM.yyyy')}</strong>.</p>

  <p>To help prepare for this session, we kindly ask you to answer a few short questions at least the day before your appointment (approx. 5 minutes):</p>

  <p style="text-align: center; margin: 30px 0;">
    <a href="@{variables('varFormUrlEN')}"
       style="background-color: #003DA5; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">
      Complete my monthly update
    </a>
  </p>

  <p style="font-size: 12px; color: #666666;">Only the first question is mandatory. All other fields are optional.</p>

  <p>If you have any questions or need to reschedule your appointment, please contact your advisor directly.</p>

  <p>Kind regards,<br>Your Transfer Team</p>

  <hr style="border: none; border-top: 1px solid #dddddd; margin: 30px 0;">
  <p style="font-size: 11px; color: #999999;">This email was generated automatically. Please do not reply directly to this message.</p>

</body>
</html>
```

---

## Schritt 6 : Fehlerbehandlung

Eine Benachrichtigungsaktion fuer den Fall eines Flow-Fehlers hinzufuegen.

1. Ausserhalb der Schleife "Fuer jeden Teilnehmer" eine Aktion hinzufuegen :
   - Aktion : **E-Mail senden (V2)**
   - Name der Aktion : `Fehler_benachrichtigen`
   - "Ausfuehren nach" (Run after) konfigurieren : nur **"fehlgeschlagen"** ankreuzen
   - An : E-Mail-Adresse des Administrators (zu konfigurieren)
   - Betreff : `FEHLER - Flow TransferMappe Invitation J-5`
   - Inhalt :

```
Im Flow "TransferMappe - Invitation J-5" ist ein Fehler aufgetreten.

Datum : @{utcNow()}

Die Power Automate-Ausfuehrungsprotokolle fuer Details pruefen.

Direktlink : https://make.powerautomate.com
```

---

## Zusammenfassung der Flow-Aktionen (in Reihenfolge)

```
[Geplanter Ausloeseer - 07:00 taeglich]
  |
  +-- [Variable initialisieren] varSiteUrl
  +-- [Variable initialisieren] varSharedMailbox
  +-- [Variable initialisieren] varFormUrlDE
  +-- [Variable initialisieren] varFormUrlEN
  +-- [Verfassen] Datum_berechnen  (addDays +5)
  +-- [Elemente abrufen] Get_participants_J5  (Filter statut=actif AND date=Zieldatum)
  +-- [Auf jedes anwenden] Fuer_jeden_Teilnehmer
        |
        +-- [Bedingung] Bedingung_Sprache  (langue == EN ?)
              |
              +-- [Wenn ja] Einladung_senden_EN (HTML EN, varFormUrlEN)
              +-- [Wenn nein] Einladung_senden_DE (HTML DE, varFormUrlDE)
  |
  +-- [E-Mail senden] Fehler_benachrichtigen  (Run after: fehlgeschlagen)
```

---

## Hinweise und zu beachtende Punkte

- Zuerst mit einem einzelnen Testteilnehmer (fiktive E-Mail-Adresse) testen, bevor die Loesung in Produktion geht
- Das Shared Mailbox muss die Berechtigung "Senden als" fuer das Power Automate-Dienstkonto haben
- Der Forms-Link muss im Modus "Jeder kann antworten" sein (Zugriff ohne M365-Konto erforderlich)
- Teilnehmer erhalten keine Kopie ihrer eigenen Antwort (kein "Reply-To" auf dem generischen Postfach)
- Bei mehr als 100 Teilnehmern pro Tag die "Maximale Anzahl von Elementen" erhoehen und die Limits der Power Automate-Aktion pruefen (max. 5.000 Elemente pro SharePoint-Aufruf)
- Der OData-Filter auf `date_prochain_rdv` setzt voraus, dass diese Spalte vom Typ DateOnly ist. Wenn sie eine Uhrzeit enthaelt (z.B. `2026-05-10T00:00:00Z`), funktioniert der Filter `eq` moeglicherweise nicht. In diesem Fall verwenden :

```
statut eq 'actif' and date_prochain_rdv ge '@{outputs('Datum_berechnen')}T00:00:00Z' and date_prochain_rdv lt '@{outputs('Datum_berechnen')}T23:59:59Z'
```
