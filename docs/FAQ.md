# FAQ - outplacement-tracker

Questions frequentes pour deux publics : les conseillers qui utilisent la solution au quotidien,
et les administrateurs M365 qui la deployent.

---

## Pour les conseillers / Beraterinnen

### Quand est-ce que je recois le PDF ?

Le Flow 2 genere le PDF le matin du jour du rendez-vous et l'envoie par email a la conseillere
designee dans le champ `id_conseillere` du participant. Le PDF est egalement sauvegarde
automatiquement dans la bibliotheque `TransferMappes` de SharePoint.

### Le participant est-il oblige de remplir le formulaire ?

Non. Le champ `bilan_general` (Gesamtbewertung des Monats) est le seul champ obligatoire
dans le formulaire de bilan mensuel. Les cinq autres champs sont optionnels. Le participant
decide de ce qu'il partage.

### Que se passe-t-il si le participant ne remplit pas le formulaire ?

Le PDF est genere quand meme. Il contient l'historique complet des mois precedents.
La section du mois en cours indique qu'aucun bilan n'a ete soumis pour cette periode.
Le RDV peut avoir lieu normalement.

### Puis-je acceder aux reponses directement dans SharePoint ?

Oui, sous reserve d'avoir des droits Membre sur le site SharePoint `TransferMappe`.
Les bilans sont stockes dans la liste `BilansMensuels`. Les profils et objectifs sont
dans la liste `Profils`.

### Le PDF est-il accessible apres le rendez-vous ?

Oui. Chaque PDF genere est sauvegarde dans la bibliotheque de documents `TransferMappes`
de SharePoint, organise par participant. Il reste accessible tant que les donnees
du participant n'ont pas ete supprimees.

### Un participant peut-il voir les donnees des autres participants ?

Non. Les participants n'ont aucun acces au site SharePoint. Ils interagissent uniquement
via les formulaires Microsoft Forms, qui sont individuels et ne donnent acces a aucune
autre donnee.

### Comment modifier le formulaire si j'ai des questions supplementaires ?

La modification du formulaire se fait dans l'interface Microsoft Forms. Apres ajout d'une
question, il faut : 1) ajouter la colonne correspondante dans la liste SharePoint `BilansMensuels`,
2) ajouter le Content Control correspondant dans le template Word, 3) mettre a jour
l'action "Populate" dans le Flow 2. Voir `specs/sharepoint_schema.md` et
`specs/word_template_structure.md` pour les conventions de nommage.

### Le formulaire est-il disponible en plusieurs langues ?

Oui. Il existe deux versions du formulaire de bilan mensuel : une en allemand (DE) et
une en anglais (EN). La langue du formulaire envoye a un participant est determinee par
le champ `langue` dans la liste `Participants`.

---

## Pour l'equipe IT / administrateur M365

### Quels sont les prerequis de licences ?

Un plan Microsoft 365 E3 ou superieur est requis. La solution utilise exclusivement des
connecteurs standard inclus dans E3 : SharePoint, Outlook, Word Online Business, et
Power Automate (plan seeded). Aucun connecteur Premium n'est necessaire.

### Combien de temps prend le deploiement ?

Entre 2 et 4 heures pour un administrateur M365 competent, en suivant les guides
du kit. Le script PowerShell PnP provisionne les listes SharePoint en quelques minutes.
La partie la plus longue est la construction manuelle des Flows dans Power Automate
(voir `power_automate/IMPORT_GUIDE.md`).

### Peut-on deployer sans PowerShell ?

Techniquement oui. Les listes SharePoint peuvent etre creees manuellement via l'interface
web. Le script `sharepoint/setup_lists.ps1` est fortement recommande car il est idempotent
et garantit la coherence des colonnes. L'alternative manuelle est documentee dans
`specs/sharepoint_schema.md`.

### Est-ce que le kit necessite une application Azure AD ?

Non. Les Flows Power Automate utilisent uniquement des connecteurs standard qui s'authentifient
via le compte de service de l'administrateur. Aucune inscription d'application dans
Azure AD n'est requise.

### Comment mettre a jour les templates Word ?

Deposer le nouveau fichier `.docx` dans la bibliotheque SharePoint a l'emplacement
`/sites/TransferMappe/TransferMappes/Templates/`. Les Flows lisent le fichier a chaque
execution : la mise a jour est prise en compte immediatement, sans modifier les Flows.
Les Tag values des Content Controls doivent rester identiques si la structure est preservee.

### Que se passe-t-il si un Flow echoue ?

Les deux Flows envoient un email d'erreur a l'adresse administrateur configuree dans
la variable `varAdminEmail`. L'historique d'execution complet est consultable dans
Power Automate sous "Mes flux" > selectionner le Flow > "Historique des executions (28 jours)".

### Peut-on limiter l'acces a certaines conseillers seulement ?

Oui. Les droits SharePoint sont geres au niveau du site et des listes. Chaque conseillere
peut etre limitee a ses propres participants en combinant des vues filtrees sur `id_conseillere`
et des droits restreints. Pour une segmentation stricte, des groupes SharePoint distincts
par conseillere sont recommandes. Voir la documentation Microsoft sur les permissions SharePoint.

### Comment supprimer les donnees d'un participant apres fin de parcours ?

Les donnees sont reparties sur 3 listes SharePoint (`Participants`, `Profils`, `BilansMensuels`)
et dans la bibliotheque `TransferMappes` (PDFs). La suppression manuelle est possible
depuis l'interface SharePoint. Un Flow de suppression automatique declanche apres
expiration de la periode de retention est documente dans `BACKLOG.md` (v0.2).

### La solution est-elle conforme au DSGVO ?

La solution est deployee dans le tenant Microsoft 365 du client. Aucune donnee ne sort
du tenant. L'organisation qui deploie la solution est responsable de traitement (Verantwortlicher)
au sens du DSGVO et assume integralement les obligations de conformite. Voir `docs/PRIVACY.md`
pour le detail des donnees collectees, les bases juridiques applicables et le modele
de responsabilite.

### Peut-on avoir plusieurs conseillers pour des participants differents ?

Oui. Le champ `id_conseillere` est renseigne individuellement pour chaque participant
dans la liste `Participants`. Chaque participant peut etre assigne a un(e) conseiller(e)
different(e). Le Flow 2 envoie le PDF a l'adresse `id_conseillere` du participant concerne.
