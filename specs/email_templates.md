# Email Templates - outplacement-tracker v0.1

Quatre templates d'email utilises par les deux Power Automate Flows.
Les variables entre doubles accolades `{{variable}}` sont injectees par Power Automate au moment de l'envoi.

Conventions :
- `{{prenom}}` : champ `Participants.prenom`
- `{{nom}}` : champ `Participants.nom`
- `{{date_rdv}}` : champ `Participants.date_prochain_rdv`, formate DD.MM.YYYY
- `{{lien_formulaire}}` : lien unique Microsoft Forms genere par le Flow J-5
- `{{nom_conseillere}}` : derive de `Participants.id_conseillere` (nom affiche du compte M365)
- `{{prenom_participant}}` : champ `Participants.prenom`
- `{{nom_participant}}` : champ `Participants.nom`
- `{{lien_pdf_sharepoint}}` : URL du fichier PDF dans la bibliotheque SharePoint du participant

---

## Template 1 : Invitation J-5 (DE)

**Declencheur** : Flow J-5, cinq jours avant `date_prochain_rdv`, langue = `DE`
**Expediteur** : boite generique configuree par l'administrateur (ex. transfer@societe.de)
**Destinataire** : `Participants.email`

**Objet** :
```
Ihr naechster Beratungstermin am {{date_rdv}} - Bitte Kurzbericht ausfullen
```

**Corps (texte brut, compatible avec les clients mail sans HTML) :**
```
Guten Tag {{prenom}} {{nom}},

Ihr naechster Beratungstermin findet am {{date_rdv}} statt.

Um diesen Termin optimal vorzubereiten, bitten wir Sie, bis zum Vortag kurz folgende Fragen zu beantworten (ca. 5 Minuten):

{{lien_formulaire}}

Nur die erste Frage ist Pflichtangabe. Alle anderen Felder sind freiwillig.

Wenn Sie Fragen haben oder den Termin verschieben muessen, wenden Sie sich bitte an Ihre Beraterin.

Mit freundlichen Gruessen,
Ihr Transfer-Team


---
Diese E-Mail wurde automatisch generiert. Bitte antworten Sie nicht direkt auf diese Nachricht.
```

**Corps (HTML) :**
```html
<!DOCTYPE html>
<html lang="de">
<body style="font-family: Arial, sans-serif; font-size: 14px; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px;">

  <p>Guten Tag {{prenom}} {{nom}},</p>

  <p>Ihr naechster Beratungstermin findet am <strong>{{date_rdv}}</strong> statt.</p>

  <p>Um diesen Termin optimal vorzubereiten, bitten wir Sie, bis zum Vortag kurz folgende Fragen zu beantworten (ca. 5 Minuten):</p>

  <p style="text-align: center; margin: 30px 0;">
    <a href="{{lien_formulaire}}"
       style="background-color: #003DA5; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">
      Zum Monatsbericht
    </a>
  </p>

  <p style="font-size: 12px; color: #666666;">Nur die erste Frage ist Pflichtangabe. Alle anderen Felder sind freiwillig.</p>

  <p>Wenn Sie Fragen haben oder den Termin verschieben muessen, wenden Sie sich bitte an Ihre Beraterin.</p>

  <p>Mit freundlichen Gruessen,<br>Ihr Transfer-Team</p>

  <hr style="border: none; border-top: 1px solid #dddddd; margin: 30px 0;">
  <p style="font-size: 11px; color: #999999;">Diese E-Mail wurde automatisch generiert. Bitte antworten Sie nicht direkt auf diese Nachricht.</p>

</body>
</html>
```

---

## Template 2 : Invitation J-5 (EN)

**Declencheur** : Flow J-5, cinq jours avant `date_prochain_rdv`, langue = `EN`
**Expediteur** : boite generique configuree par l'administrateur
**Destinataire** : `Participants.email`

**Objet** :
```
Your next appointment on {{date_rdv}} - Please complete your monthly update
```

**Corps (texte brut) :**
```
Dear {{prenom}} {{nom}},

Your next appointment with your advisor is scheduled for {{date_rdv}}.

To help prepare for this session, we kindly ask you to answer a few short questions before the day before your appointment (approx. 5 minutes):

{{lien_formulaire}}

Only the first question is mandatory. All other fields are optional.

If you have any questions or need to reschedule your appointment, please contact your advisor directly.

Kind regards,
Your Transfer Team


---
This email was generated automatically. Please do not reply directly to this message.
```

**Corps (HTML) :**
```html
<!DOCTYPE html>
<html lang="en">
<body style="font-family: Arial, sans-serif; font-size: 14px; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px;">

  <p>Dear {{prenom}} {{nom}},</p>

  <p>Your next appointment with your advisor is scheduled for <strong>{{date_rdv}}</strong>.</p>

  <p>To help prepare for this session, we kindly ask you to answer a few short questions before the day before your appointment (approx. 5 minutes):</p>

  <p style="text-align: center; margin: 30px 0;">
    <a href="{{lien_formulaire}}"
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

## Template 3 : Notification conseillere le jour du RDV (DE)

**Declencheur** : Flow J (generation PDF), le matin du jour du RDV, langue de la conseillere = `DE` (ou par defaut)
**Expediteur** : boite generique configuree par l'administrateur
**Destinataire** : `Participants.id_conseillere` (compte M365 de la conseillere)

**Objet** :
```
Transfer Mappe - {{prenom_participant}} {{nom_participant}} - Termin heute {{date_rdv}}
```

**Corps (texte brut) :**
```
Guten Morgen,

im Anhang finden Sie die aktuelle Transfer Mappe von {{prenom_participant}} {{nom_participant}} fuer den Beratungstermin heute, {{date_rdv}}.

Das Dokument enthaelt:
- Das Karriereprofil des Teilnehmers (falls ausgefuellt)
- Alle bisher eingereichten Monatsberichte in chronologischer Reihenfolge
- Freie Unterschriftenfelder fuer die Zielvereinbarung

Eine Kopie wurde in SharePoint gespeichert:
{{lien_pdf_sharepoint}}

Mit freundlichen Gruessen,
Transfer Mappe System


---
Diese E-Mail wurde automatisch generiert.
```

**Corps (HTML) :**
```html
<!DOCTYPE html>
<html lang="de">
<body style="font-family: Arial, sans-serif; font-size: 14px; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px;">

  <p>Guten Morgen,</p>

  <p>im Anhang finden Sie die aktuelle Transfer Mappe von <strong>{{prenom_participant}} {{nom_participant}}</strong> fuer den Beratungstermin heute, <strong>{{date_rdv}}</strong>.</p>

  <p>Das Dokument enthaelt:</p>
  <ul>
    <li>Das Karriereprofil des Teilnehmers (falls ausgefuellt)</li>
    <li>Alle bisher eingereichten Monatsberichte in chronologischer Reihenfolge</li>
    <li>Freie Unterschriftenfelder fuer die Zielvereinbarung</li>
  </ul>

  <p>Eine Kopie wurde in SharePoint gespeichert:<br>
    <a href="{{lien_pdf_sharepoint}}" style="color: #003DA5;">Zum Dokument in SharePoint</a>
  </p>

  <p>Mit freundlichen Gruessen,<br>Transfer Mappe System</p>

  <hr style="border: none; border-top: 1px solid #dddddd; margin: 30px 0;">
  <p style="font-size: 11px; color: #999999;">Diese E-Mail wurde automatisch generiert.</p>

</body>
</html>
```

---

## Template 4 : Notification conseillere le jour du RDV (EN)

**Declencheur** : Flow J (generation PDF), le matin du jour du RDV, langue participant = `EN`
**Expediteur** : boite generique configuree par l'administrateur
**Destinataire** : `Participants.id_conseillere` (compte M365 de la conseillere)

**Note** : la langue du participant determine quelle version du template Word est utilisee. La notification a la conseillere est elle-meme toujours en DE (langue de travail interne). Ce template EN est fourni pour les structures bilingues qui souhaitent aussi notifier la conseillere en anglais.

**Objet** :
```
Transfer Mappe - {{prenom_participant}} {{nom_participant}} - Appointment today {{date_rdv}}
```

**Corps (texte brut) :**
```
Good morning,

please find attached the current Transfer Mappe for {{prenom_participant}} {{nom_participant}}, for today's appointment on {{date_rdv}}.

The document includes:
- The participant's career profile (if completed)
- All monthly updates submitted so far, in chronological order
- Blank signature fields for the Zielvereinbarung

A copy has been saved in SharePoint:
{{lien_pdf_sharepoint}}

Kind regards,
Transfer Mappe System


---
This email was generated automatically.
```

**Corps (HTML) :**
```html
<!DOCTYPE html>
<html lang="en">
<body style="font-family: Arial, sans-serif; font-size: 14px; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px;">

  <p>Good morning,</p>

  <p>please find attached the current Transfer Mappe for <strong>{{prenom_participant}} {{nom_participant}}</strong>, for today's appointment on <strong>{{date_rdv}}</strong>.</p>

  <p>The document includes:</p>
  <ul>
    <li>The participant's career profile (if completed)</li>
    <li>All monthly updates submitted so far, in chronological order</li>
    <li>Blank signature fields for the Zielvereinbarung</li>
  </ul>

  <p>A copy has been saved in SharePoint:<br>
    <a href="{{lien_pdf_sharepoint}}" style="color: #003DA5;">View document in SharePoint</a>
  </p>

  <p>Kind regards,<br>Transfer Mappe System</p>

  <hr style="border: none; border-top: 1px solid #dddddd; margin: 30px 0;">
  <p style="font-size: 11px; color: #999999;">This email was generated automatically.</p>

</body>
</html>
```

---

## Notes de configuration Power Automate

- **Expediteur** : utiliser une shared mailbox (ex. transfer@societe.de) configuree par l'administrateur M365. Ne pas utiliser le compte personnel d'un utilisateur.
- **Encodage** : UTF-8 pour tous les templates. Les umlauts allemands (ae, oe, ue, ss) sont supportes nativement par Outlook et les clients IMAP courants.
- **Piece jointe** (Template 3 et 4) : le PDF cumulatif est attache via l'action "Add an attachment" de Power Automate. Taille maximale recommandee : 10 MB (largement suffisant pour un PDF 12 mois).
- **Lien formulaire** (Template 1 et 2) : le lien est genere par l'action "Get the response details" ou via une variable prefigurée. Il n'est pas reutilisable entre participants.
- **Test** : toujours tester l'envoi avec une adresse de test avant mise en production. Ne jamais mettre une adresse personnelle reelle dans les variables de test.
