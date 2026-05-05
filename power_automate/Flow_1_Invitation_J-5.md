# Flow 1 : Invitation J-5

outplacement-tracker v0.1 - Implementation guide (blueprint sans tenant)

Ce document permet a un administrateur Microsoft 365 de reconstruire ce Flow
a partir de zero, action par action, sans import JSON.

---

## Vue d'ensemble

| Parametre | Valeur |
|---|---|
| Nom du Flow | TransferMappe - Invitation J-5 |
| Declencheur | Planifie (tous les jours a 07h00) |
| Fonction | Pour chaque participant actif avec un RDV dans 5 jours, envoyer l'email d'invitation avec le lien vers le formulaire Forms correspondant |
| Frequence | Quotidien |
| Connexions requises | SharePoint, Office 365 Outlook |

---

## Etape 1 : Creer le Flow

1. Aller sur make.powerautomate.com
2. Cliquer sur "Creer" > "Flux planifie"
3. Renseigner :
   - Nom : `TransferMappe - Invitation J-5`
   - Heure de debut : `07:00`
   - Repeter toutes les : `1 jour`
4. Cliquer sur "Creer"

---

## Etape 2 : Variables de configuration

En debut de Flow, ajouter 4 actions "Initialiser une variable" (une par variable).

| Nom de variable | Type | Valeur initiale | Description |
|---|---|---|---|
| varSiteUrl | String | `https://{tenant}.sharepoint.com/sites/TransferMappe` | URL du site SharePoint - remplacer {tenant} |
| varSharedMailbox | String | `transfer@{domaine}.de` | Adresse expeditrice - shared mailbox configuree par l'admin |
| varFormUrlDE | String | `{URL du Forms bilan mensuel DE}` | Copier depuis le Form 3 (voir forms_construction_guide.md) |
| varFormUrlEN | String | `{URL du Forms bilan mensuel EN}` | Copier depuis le Form 4 |

---

## Etape 3 : Calculer la date cible (aujourd'hui + 5 jours)

- Action : **Composer** (Data Operations > Composer)
- Nom de l'action : `Calculer_date_cible`
- Entrees (expression) :

```
addDays(utcNow(), 5, 'yyyy-MM-dd')
```

Cette expression retourne la date dans 5 jours au format `YYYY-MM-DD` (ex. `2026-05-10`).

---

## Etape 4 : Recuperer les participants actifs avec RDV dans 5 jours

- Action : **Obtenir des elements** (SharePoint > Obtenir des elements)
- Nom de l'action : `Get_participants_J5`
- Site : `variables('varSiteUrl')`
- Nom de la liste : `Participants`
- Filtrer la requete (OData) :

```
statut eq 'actif' and date_prochain_rdv eq '@{outputs('Calculer_date_cible')}'
```

Note : la valeur de date doit correspondre exactement au format stocke dans SharePoint (DateOnly ISO 8601). Si la colonne `date_prochain_rdv` stocke une heure (meme 00:00:00Z), ajuster le filtre en consequence ou utiliser `startswith`.

- Nombre maximal d'elements : `100` (ajuster selon le volume de participants)

---

## Etape 5 : Pour chaque participant (Apply to each)

- Action : **Appliquer a chacun** (Control > Appliquer a chacun)
- Nom de l'action : `Pour_chaque_participant`
- Entree : `value` de l'action `Get_participants_J5`

### Action 5.1 : Condition sur la langue

- Action : **Condition** (Control > Condition)
- Nom de l'action : `Condition_langue`
- Condition :

```
items('Pour_chaque_participant')?['langue']
```

... est egal a ...

```
EN
```

#### Branche "Si oui" (langue EN)

Passer a l'action 5.2 avec :
- `varFormUrl` = `variables('varFormUrlEN')`
- Template email = Template 2 (EN)

#### Branche "Si non" (langue DE, valeur par defaut)

Passer a l'action 5.2 avec :
- `varFormUrl` = `variables('varFormUrlDE')`
- Template email = Template 1 (DE)

### Action 5.2 : Envoyer l'email d'invitation

Creer cette action dans **chacune** des deux branches (oui/non) de la condition.

- Action : **Envoyer un e-mail (V2)** (Office 365 Outlook > Envoyer un e-mail (V2))
- Nom de l'action : `Envoyer_invitation_DE` ou `Envoyer_invitation_EN`
- De (From) : `variables('varSharedMailbox')`
- A (To) : `items('Pour_chaque_participant')?['email']`

**Version DE - Objet :**

```
Ihr nächster Beratungstermin am @{formatDateTime(items('Pour_chaque_participant')?['date_prochain_rdv'], 'dd.MM.yyyy')} - Bitte Kurzbericht ausfüllen
```

**Version DE - Corps (HTML) :**

```html
<!DOCTYPE html>
<html lang="de">
<body style="font-family: Arial, sans-serif; font-size: 14px; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px;">

  <p>Guten Tag @{items('Pour_chaque_participant')?['prenom']} @{items('Pour_chaque_participant')?['nom']},</p>

  <p>Ihr nächster Beratungstermin findet am <strong>@{formatDateTime(items('Pour_chaque_participant')?['date_prochain_rdv'], 'dd.MM.yyyy')}</strong> statt.</p>

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

**Version EN - Objet :**

```
Your next appointment on @{formatDateTime(items('Pour_chaque_participant')?['date_prochain_rdv'], 'dd.MM.yyyy')} - Please complete your monthly update
```

**Version EN - Corps (HTML) :**

```html
<!DOCTYPE html>
<html lang="en">
<body style="font-family: Arial, sans-serif; font-size: 14px; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px;">

  <p>Dear @{items('Pour_chaque_participant')?['prenom']} @{items('Pour_chaque_participant')?['nom']},</p>

  <p>Your next appointment with your advisor is scheduled for <strong>@{formatDateTime(items('Pour_chaque_participant')?['date_prochain_rdv'], 'dd.MM.yyyy')}</strong>.</p>

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

## Etape 6 : Gestion d'erreurs

Ajouter une action de notification en cas d'echec du Flow.

1. En dehors de la boucle "Pour chaque participant", ajouter une action :
   - Action : **Envoyer un e-mail (V2)**
   - Nom de l'action : `Notifier_erreur`
   - Configurer "Executer apres" (Run after) : cocher uniquement **"a echoue"**
   - A : adresse email de l'administrateur (a configurer)
   - Objet : `ERREUR - Flow TransferMappe Invitation J-5`
   - Corps :

```
Une erreur s'est produite dans le Flow "TransferMappe - Invitation J-5".

Date : @{utcNow()}

Verifier les journaux d'execution Power Automate pour le detail.

Lien direct : https://make.powerautomate.com
```

---

## Recapitulatif des actions du Flow (dans l'ordre)

```
[Declencheur planifie - 07:00 quotidien]
  |
  +-- [Initialiser variable] varSiteUrl
  +-- [Initialiser variable] varSharedMailbox
  +-- [Initialiser variable] varFormUrlDE
  +-- [Initialiser variable] varFormUrlEN
  +-- [Composer] Calculer_date_cible  (addDays +5)
  +-- [Obtenir des elements] Get_participants_J5  (filtre statut=actif AND date=cible)
  +-- [Appliquer a chacun] Pour_chaque_participant
        |
        +-- [Condition] Condition_langue  (langue == EN ?)
              |
              +-- [Si oui] Envoyer_invitation_EN (HTML EN, varFormUrlEN)
              +-- [Si non] Envoyer_invitation_DE (HTML DE, varFormUrlDE)
  |
  +-- [Envoyer e-mail] Notifier_erreur  (Run after: failed)
```

---

## Precautions et points d'attention

- Tester d'abord avec un seul participant de test (adresse email fictive) avant mise en production
- La shared mailbox doit avoir la permission "Send As" pour le compte de service Power Automate
- Le lien Forms doit etre en mode "Tout le monde peut repondre" (acces sans compte M365 requis)
- Les participants ne reoivent pas leur propre reponse en copie (pas de "Reply-To" sur la mailbox generique)
- En cas de volume superieur a 100 participants par jour, augmenter le "Nombre maximal d'elements" et verifier les limites de l'action Power Automate (5 000 elements max par appel SharePoint)
- Le filtre OData sur `date_prochain_rdv` suppose que cette colonne est de type DateOnly. Si elle inclut une heure (ex. `2026-05-10T00:00:00Z`), le filtre `eq` peut ne pas fonctionner. Dans ce cas, utiliser :

```
statut eq 'actif' and date_prochain_rdv ge '@{outputs('Calculer_date_cible')}T00:00:00Z' and date_prochain_rdv lt '@{outputs('Calculer_date_cible')}T23:59:59Z'
```
