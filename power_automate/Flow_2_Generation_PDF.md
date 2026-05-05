# Flow 2 : Generation PDF le jour du RDV

outplacement-tracker v0.1 - Implementation guide (blueprint sans tenant)

Ce document permet a un administrateur Microsoft 365 de reconstruire ce Flow
a partir de zero, action par action, sans import JSON.

---

## Vue d'ensemble

| Parametre | Valeur |
|---|---|
| Nom du Flow | TransferMappe - Generation PDF |
| Declencheur | Planifie (tous les jours a 06h00) |
| Fonction | Pour chaque participant actif dont le RDV est aujourd'hui : recuperer profil + bilans, remplir le template Word, convertir en PDF, envoyer a la conseillere, sauvegarder dans SharePoint |
| Frequence | Quotidien |
| Connexions requises | SharePoint, Word Online (Business), Office 365 Outlook |

Le Flow se declenche 1h avant le Flow J-5 (06h00 vs 07h00) pour eviter toute collision.

---

## Etape 1 : Creer le Flow

1. Aller sur make.powerautomate.com
2. Cliquer sur "Creer" > "Flux planifie"
3. Renseigner :
   - Nom : `TransferMappe - Generation PDF`
   - Heure de debut : `06:00`
   - Repeter toutes les : `1 jour`
4. Cliquer sur "Creer"

---

## Etape 2 : Variables de configuration

Ajouter 4 actions "Initialiser une variable" en debut de Flow.

| Nom de variable | Type | Valeur initiale | Description |
|---|---|---|---|
| varSiteUrl | String | `https://{tenant}.sharepoint.com/sites/TransferMappe` | URL du site SharePoint |
| varSharedMailbox | String | `transfer@{domaine}.de` | Adresse expeditrice |
| varTemplatePathDE | String | `/sites/TransferMappe/TransferMappes/Templates/transfer_mappe_template_de.docx` | Chemin SharePoint du template Word DE |
| varTemplatePathEN | String | `/sites/TransferMappe/TransferMappes/Templates/transfer_mappe_template_en.docx` | Chemin SharePoint du template Word EN |

---

## Etape 3 : Calculer la date du jour

- Action : **Composer** (Data Operations > Composer)
- Nom de l'action : `Date_aujourdhui`
- Entrees (expression) :

```
formatDateTime(utcNow(), 'yyyy-MM-dd')
```

---

## Etape 4 : Recuperer les participants actifs avec RDV aujourd'hui

- Action : **Obtenir des elements** (SharePoint)
- Nom de l'action : `Get_participants_rdv_auj`
- Site : `variables('varSiteUrl')`
- Nom de la liste : `Participants`
- Filtrer la requete :

```
statut eq 'actif' and date_prochain_rdv eq '@{outputs('Date_aujourdhui')}'
```

- Nombre maximal d'elements : `100`

---

## Etape 5 : Pour chaque participant (boucle principale)

- Action : **Appliquer a chacun**
- Nom de l'action : `Pour_chaque_participant_rdv`
- Entree : `value` de `Get_participants_rdv_auj`

### Action 5.1 : Recuperer le profil du participant

- Action : **Obtenir des elements** (SharePoint)
- Nom de l'action : `Get_profil`
- Site : `variables('varSiteUrl')`
- Nom de la liste : `Profils`
- Filtrer la requete :

```
id_participant eq @{items('Pour_chaque_participant_rdv')?['ID']}
```

- Nombre maximal d'elements : `1`

Note : `ID` est la colonne id auto-generee par SharePoint (entier). Ne pas confondre avec `id_participant`.

### Action 5.2 : Recuperer tous les bilans du participant (tries par date ASC)

- Action : **Obtenir des elements** (SharePoint)
- Nom de l'action : `Get_bilans`
- Site : `variables('varSiteUrl')`
- Nom de la liste : `BilansMensuels`
- Filtrer la requete :

```
id_participant eq @{items('Pour_chaque_participant_rdv')?['ID']}
```

- Trier par : `date_rdv` - Croissant (ASC)
- Nombre maximal d'elements : `12`

### Action 5.3 : Choisir le chemin du template selon la langue

- Action : **Condition**
- Nom de l'action : `Condition_langue_pdf`
- Condition : `items('Pour_chaque_participant_rdv')?['langue']` est egal a `EN`
- Branche "Si oui" : initialiser une variable `varTemplatePath` = `variables('varTemplatePathEN')`
- Branche "Si non" : initialiser une variable `varTemplatePath` = `variables('varTemplatePathDE')`

Note : declarer `varTemplatePath` comme String vide dans l'etape 2 avant de l'affecter ici.

### Action 5.4 : Remplir le template Word (Populate a Microsoft Word template)

- Action : **Remplir un modele Microsoft Word** (Word Online (Business))
- Nom de l'action : `Remplir_template`
- Emplacement : `SharePoint`
- Bibliotheque de documents : `Documents` (ou le nom de votre bibliotheque)
- Fichier : `variables('varTemplatePath')`

#### Mapping des Content Controls

Chaque ligne ci-dessous correspond a un champ dans l'action Power Automate.
La colonne "Expression" est l'expression dynamique a saisir dans le champ correspondant.

**Page de garde (6 Content Controls)**

| Content Control (Tag value) | Expression Power Automate |
|---|---|
| `doc_titre` | `if(equals(items('Pour_chaque_participant_rdv')?['langue'], 'EN'), 'Transfer Portfolio', 'Transfer Mappe')` |
| `participant_prenom` | `items('Pour_chaque_participant_rdv')?['prenom']` |
| `participant_nom` | `items('Pour_chaque_participant_rdv')?['nom']` |
| `participant_date_debut` | `formatDateTime(items('Pour_chaque_participant_rdv')?['date_debut_parcours'], 'dd.MM.yyyy')` |
| `conseillere_nom` | `items('Pour_chaque_participant_rdv')?['id_conseillere']` |
| `doc_date_generation` | `formatDateTime(utcNow(), 'dd.MM.yyyy')` |

**Section Profil (4 Content Controls)**

La valeur "Nicht angegeben" / "Not provided" est injectee si le champ est vide.

| Content Control (Tag value) | Expression Power Automate |
|---|---|
| `profil_plan_a` | `if(equals(length(body('Get_profil')?['value']), 0), if(equals(items('Pour_chaque_participant_rdv')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben'), coalesce(body('Get_profil')?['value'][0]?['plan_a'], if(equals(items('Pour_chaque_participant_rdv')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben')))` |
| `profil_plan_b` | `if(equals(length(body('Get_profil')?['value']), 0), if(equals(items('Pour_chaque_participant_rdv')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben'), coalesce(body('Get_profil')?['value'][0]?['plan_b'], if(equals(items('Pour_chaque_participant_rdv')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben')))` |
| `profil_marketingplan` | `if(equals(length(body('Get_profil')?['value']), 0), if(equals(items('Pour_chaque_participant_rdv')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben'), coalesce(body('Get_profil')?['value'][0]?['marketingplan'], if(equals(items('Pour_chaque_participant_rdv')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben')))` |
| `profil_zielmarkt` | `if(equals(length(body('Get_profil')?['value']), 0), if(equals(items('Pour_chaque_participant_rdv')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben'), coalesce(body('Get_profil')?['value'][0]?['zielmarkt'], if(equals(items('Pour_chaque_participant_rdv')?['langue'], 'EN'), 'Not provided', 'Nicht angegeben')))` |

**Mapping statut_objectifs -> libelle visible**

Le code interne SharePoint est traduit en libelle lisible. Utiliser la fonction `switch` dans une action Composer precedant le remplissage du template, ou directement en expression dans le champ :

```
if(equals(items('Pour_chaque_participant_rdv')?['langue'], 'EN'),
  switch(body('Get_bilans')?['value'][0]?['statut_objectifs'],
    'vollstaendig_erreicht', 'Fully achieved',
    'teilweise_erreicht', 'Partially achieved',
    'nicht_erreicht', 'Not achieved',
    'noch_nicht_relevant', 'Not yet relevant',
    ''),
  switch(body('Get_bilans')?['value'][0]?['statut_objectifs'],
    'vollstaendig_erreicht', 'Vollständig erreicht',
    'teilweise_erreicht', 'Teilweise erreicht',
    'nicht_erreicht', 'Nicht erreicht',
    'noch_nicht_relevant', 'Noch nicht relevant',
    ''))
```

Note : remplacer `[0]` par `[1]`, `[2]`, etc. selon le numero de bilan concerne.

**Sections Bilan 01 a 12 (9 Content Controls x 12 = 108)**

Le pattern est identique pour chaque bilan. Remplacer `NN` par `01` a `12` et `[N-1]` par l'index tableau correspondant (bilan 01 = index 0, bilan 12 = index 11).

Si le bilan N n'existe pas (tableau plus court que N), injecter une chaine vide `""`.

Pattern pour `bilan_NN_*` (exemple avec bilan 01, index 0) :

| Content Control | Expression |
|---|---|
| `bilan_01_date_rdv` | `if(greater(length(body('Get_bilans')?['value']), 0), formatDateTime(body('Get_bilans')?['value'][0]?['date_rdv'], 'dd.MM.yyyy'), '')` |
| `bilan_01_date_soumission` | `if(greater(length(body('Get_bilans')?['value']), 0), formatDateTime(body('Get_bilans')?['value'][0]?['date_soumission'], 'dd.MM.yyyy'), '')` |
| `bilan_01_bilan_general` | `if(greater(length(body('Get_bilans')?['value']), 0), coalesce(body('Get_bilans')?['value'][0]?['bilan_general'], ''), '')` |
| `bilan_01_statut_objectifs` | `if(greater(length(body('Get_bilans')?['value']), 0), [expression switch langue/code ci-dessus avec index 0], '')` |
| `bilan_01_statut_objectifs_detail` | `if(greater(length(body('Get_bilans')?['value']), 0), coalesce(body('Get_bilans')?['value'][0]?['statut_objectifs_detail'], ''), '')` |
| `bilan_01_was_lief_gut` | `if(greater(length(body('Get_bilans')?['value']), 0), coalesce(body('Get_bilans')?['value'][0]?['was_lief_gut'], ''), '')` |
| `bilan_01_wo_brauche_ich` | `if(greater(length(body('Get_bilans')?['value']), 0), coalesce(body('Get_bilans')?['value'][0]?['wo_brauche_ich_unterstuetzung'], ''), '')` |
| `bilan_01_themen_naechster_termin` | `if(greater(length(body('Get_bilans')?['value']), 0), coalesce(body('Get_bilans')?['value'][0]?['themen_naechster_termin'], ''), '')` |
| `bilan_01_sonstige_anmerkungen` | `if(greater(length(body('Get_bilans')?['value']), 0), coalesce(body('Get_bilans')?['value'][0]?['sonstige_anmerkungen'], ''), '')` |

Pour bilan 02 (index 1), remplacer `[0]` par `[1]` et `greater(..., 0)` par `greater(..., 1)` dans chaque expression.

Pour bilan 12 (index 11) : `greater(length(body('Get_bilans')?['value']), 11)` et `[11]`.

**Tableau recapitulatif des seuils par bilan**

| Bilan | Index tableau | Condition de presence |
|---|---|---|
| 01 | 0 | `greater(length(body('Get_bilans')?['value']), 0)` |
| 02 | 1 | `greater(length(body('Get_bilans')?['value']), 1)` |
| 03 | 2 | `greater(length(body('Get_bilans')?['value']), 2)` |
| 04 | 3 | `greater(length(body('Get_bilans')?['value']), 3)` |
| 05 | 4 | `greater(length(body('Get_bilans')?['value']), 4)` |
| 06 | 5 | `greater(length(body('Get_bilans')?['value']), 5)` |
| 07 | 6 | `greater(length(body('Get_bilans')?['value']), 6)` |
| 08 | 7 | `greater(length(body('Get_bilans')?['value']), 7)` |
| 09 | 8 | `greater(length(body('Get_bilans')?['value']), 8)` |
| 10 | 9 | `greater(length(body('Get_bilans')?['value']), 9)` |
| 11 | 10 | `greater(length(body('Get_bilans')?['value']), 10)` |
| 12 | 11 | `greater(length(body('Get_bilans')?['value']), 11)` |

### Action 5.5 : Convertir le document Word en PDF

- Action : **Convertir un document Word en PDF** (Word Online (Business))
- Nom de l'action : `Convertir_en_PDF`
- Entree : sortie de l'action `Remplir_template` (contenu du fichier)

Note : cette action est disponible dans le connecteur Word Online (Business) inclus en E3.
Elle ne requiert pas de licence Power Automate Premium.

### Action 5.6 : Sauvegarder le PDF dans SharePoint

- Action : **Creer un fichier** (SharePoint > Creer un fichier)
- Nom de l'action : `Sauvegarder_PDF`
- Site : `variables('varSiteUrl')`
- Chemin du dossier : `/TransferMappes/@{items('Pour_chaque_participant_rdv')?['nom']}_@{items('Pour_chaque_participant_rdv')?['prenom']}/`
- Nom du fichier :

```
TransferMappe_@{items('Pour_chaque_participant_rdv')?['prenom']}_@{items('Pour_chaque_participant_rdv')?['nom']}_@{outputs('Date_aujourdhui')}.pdf
```

- Contenu du fichier : sortie du corps de l'action `Convertir_en_PDF`

Note : creer manuellement la bibliotheque de documents `TransferMappes` dans SharePoint
avant la premiere execution du Flow. Le sous-dossier par participant est cree automatiquement.

### Action 5.7 : Envoyer le PDF a la conseillere

- Action : **Envoyer un e-mail (V2)** (Office 365 Outlook)
- Nom de l'action : `Envoyer_PDF_conseillere`
- De : `variables('varSharedMailbox')`
- A : `items('Pour_chaque_participant_rdv')?['id_conseillere']`

**Objet (template DE, valeur par defaut) :**

```
Transfer Mappe - @{items('Pour_chaque_participant_rdv')?['prenom']} @{items('Pour_chaque_participant_rdv')?['nom']} - Termin heute @{formatDateTime(items('Pour_chaque_participant_rdv')?['date_prochain_rdv'], 'dd.MM.yyyy')}
```

**Corps HTML (DE) :**

```html
<!DOCTYPE html>
<html lang="de">
<body style="font-family: Arial, sans-serif; font-size: 14px; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px;">

  <p>Guten Morgen,</p>

  <p>im Anhang finden Sie die aktuelle Transfer Mappe von
  <strong>@{items('Pour_chaque_participant_rdv')?['prenom']} @{items('Pour_chaque_participant_rdv')?['nom']}</strong>
  für den Beratungstermin heute, <strong>@{formatDateTime(items('Pour_chaque_participant_rdv')?['date_prochain_rdv'], 'dd.MM.yyyy')}</strong>.</p>

  <p>Das Dokument enthält:</p>
  <ul>
    <li>Das Karriereprofil des Teilnehmers (falls ausgefüllt)</li>
    <li>Alle bisher eingereichten Monatsberichte in chronologischer Reihenfolge</li>
    <li>Freie Unterschriftenfelder für die Zielvereinbarung</li>
  </ul>

  <p>Eine Kopie wurde in SharePoint gespeichert:<br>
    <a href="@{body('Sauvegarder_PDF')?['Path']}" style="color: #003DA5;">Zum Dokument in SharePoint</a>
  </p>

  <p>Mit freundlichen Grüßen,<br>Transfer Mappe System</p>

  <hr style="border: none; border-top: 1px solid #dddddd; margin: 30px 0;">
  <p style="font-size: 11px; color: #999999;">Diese E-Mail wurde automatisch generiert.</p>

</body>
</html>
```

**Piece jointe :**

- Dans l'action "Envoyer un e-mail (V2)", cliquer sur "Afficher les options avancees"
- Joindre : activer "Pieces jointes"
- Nom : `TransferMappe_@{items('Pour_chaque_participant_rdv')?['prenom']}_@{items('Pour_chaque_participant_rdv')?['nom']}_@{outputs('Date_aujourdhui')}.pdf`
- Contenu : sortie du corps de `Convertir_en_PDF`

---

## Etape 6 : Gestion d'erreurs

Hors de la boucle principale, ajouter :

- Action : **Envoyer un e-mail (V2)**
- Nom de l'action : `Notifier_erreur_PDF`
- Run after : **a echoue**
- A : adresse administrateur
- Objet : `ERREUR - Flow TransferMappe Generation PDF`
- Corps :

```
Une erreur s'est produite dans le Flow "TransferMappe - Generation PDF".

Date : @{utcNow()}

Verifier les journaux d'execution Power Automate.
Un ou plusieurs participants n'ont pas recu leur PDF ce matin.

Lien : https://make.powerautomate.com
```

---

## Recapitulatif des actions du Flow (dans l'ordre)

```
[Declencheur planifie - 06:00 quotidien]
  |
  +-- [Initialiser variable] varSiteUrl
  +-- [Initialiser variable] varSharedMailbox
  +-- [Initialiser variable] varTemplatePathDE
  +-- [Initialiser variable] varTemplatePathEN
  +-- [Initialiser variable] varTemplatePath  (String, vide)
  +-- [Composer] Date_aujourdhui  (formatDateTime utcNow yyyy-MM-dd)
  +-- [Obtenir des elements] Get_participants_rdv_auj  (filtre statut=actif AND date=aujourdhui)
  +-- [Appliquer a chacun] Pour_chaque_participant_rdv
        |
        +-- [Obtenir des elements] Get_profil  (filtre id_participant)
        +-- [Obtenir des elements] Get_bilans  (filtre id_participant, tri date_rdv ASC)
        +-- [Condition] Condition_langue_pdf  (langue == EN ?)
              +-- [Si oui] varTemplatePath = varTemplatePathEN
              +-- [Si non] varTemplatePath = varTemplatePathDE
        +-- [Remplir un modele Word] Remplir_template  (118 Content Controls)
        +-- [Convertir Word en PDF] Convertir_en_PDF
        +-- [Creer un fichier] Sauvegarder_PDF  (SharePoint /TransferMappes/...)
        +-- [Envoyer un e-mail] Envoyer_PDF_conseillere  (avec piece jointe PDF)
  |
  +-- [Envoyer e-mail] Notifier_erreur_PDF  (Run after: failed)
```

---

## Precautions et points d'attention

- Verifier que les templates Word (.docx) sont deposes dans SharePoint sous le chemin
  `/sites/TransferMappe/TransferMappes/Templates/` avant la premiere execution
- L'action "Populate a Microsoft Word template" necessite que tous les 118 Content Controls
  soient renseignes. Ne jamais laisser un champ vide dans l'action : injecter `""` si le
  bilan n'existe pas
- La bibliotheque `TransferMappes` doit exister dans SharePoint avant la premiere execution
- L'adresse `id_conseillere` dans Participants est l'email M365 de la conseillere.
  Power Automate peut l'utiliser directement comme destinataire
- Taille maximale recommandee du PDF : 10 MB. Un PDF 12 mois de bilans textuels reste
  largement en dessous de cette limite
- Le Flow traite les participants sequentiellement. Pour 100 participants par jour, prevoir
  un temps d'execution d'environ 20 a 30 minutes
- Ne jamais modifier le template Word (.docx) en cours de production sans tester sur
  un participant de test : tout changement de Tag value necessite une mise a jour du Flow
