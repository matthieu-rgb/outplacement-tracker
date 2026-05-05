# Guide de mise en place - outplacement-tracker v0.1

Ce guide decrit la procedure complete de deploiement de la solution sur un tenant
Microsoft 365. Il orchestre les autres guides du kit dans l'ordre correct.

Duree estimee : 2 a 4 heures pour un administrateur M365 competent.

---

## 1. Prerequis

### 1.1 Tenant et licences

- Tenant Microsoft 365 avec plan **E3 ou superieur** (requis pour Word Online Business et
  Power Automate inclus)
- Au moins un compte avec droits d'administration SharePoint et Power Automate
- Aucun connecteur Premium requis (la solution utilise uniquement des connecteurs standard E3)

### 1.2 Site SharePoint

Creer un site SharePoint dedie avant de commencer :

1. Aller sur `https://{tenant}.sharepoint.com`
2. Cliquer sur "Creer un site" > "Site d'equipe" (Team Site)
3. Nom du site : `TransferMappe` (ou le nom interne de votre organisation)
4. Acces : restreint aux conseilleres et a l'administrateur (les participants n'ont PAS acces)
5. URL resultante : `https://{tenant}.sharepoint.com/sites/TransferMappe`

### 1.3 Module PnP.PowerShell

Sur la machine de l'administrateur (Windows, PowerShell 7+) :

```powershell
Install-Module PnP.PowerShell -Force -Scope CurrentUser
```

### 1.4 Droits necessaires

| Qui | Droits requis |
|---|---|
| Compte admin deploiement | Site Collection Administrator sur le site TransferMappe |
| Compte service Power Automate | Membre du site (acces en lecture/ecriture aux listes) |
| Conseilleres | Membres du site (lecture des listes, reception des PDF) |
| Participants | Aucun acces au site SharePoint |

---

## 2. Etape 1 : Provisioning SharePoint

### 2.1 Executer le script PnP

```powershell
cd {chemin_vers_le_kit}
.\sharepoint\setup_lists.ps1 -SiteUrl "https://{tenant}.sharepoint.com/sites/TransferMappe"
```

Le script :
- Cree les 3 listes (Participants, Profils, BilansMensuels)
- Ajoute toutes les colonnes de chaque liste
- Active le versioning (5 versions)
- Affiche un recapitulatif

Le script est idempotent : il peut etre rejoue sans erreur si les listes existent deja.

### 2.2 Verifier le resultat

Dans le navigateur :
- Aller sur `https://{tenant}.sharepoint.com/sites/TransferMappe`
- Cliquer sur "Contenu du site" (Site contents)
- Verifier que les 3 listes sont presentes : Participants, Profils, BilansMensuels

### 2.3 Creer la bibliotheque de documents pour les PDFs

1. Sur le site SharePoint, cliquer "Nouveau" > "Bibliotheque de documents"
2. Nom : `TransferMappes`
3. Dans cette bibliotheque, creer un dossier `Templates`
4. Chemin final : `/sites/TransferMappe/TransferMappes/Templates/`

---

## 3. Etape 2 : Creation des formulaires Microsoft Forms

Suivre le guide detaille : `forms/forms_construction_guide.md`

Creer dans l'ordre :
1. Form onboarding DE : "Ihr Karriereprofil - Transfer Mappe"
2. Form onboarding EN : "Your Career Profile - Transfer Mappe"
3. Form bilan mensuel DE : "Ihr monatlicher Bericht - Transfer Mappe"
4. Form bilan mensuel EN : "Your Monthly Update - Transfer Mappe"

Apres creation, noter les URLs des Form 3 et Form 4 (bilan mensuel DE et EN).
Ces URLs seront utilisees dans les Flows.

---

## 4. Etape 3 : Upload des templates Word

1. Aller dans la bibliotheque de documents SharePoint : `/sites/TransferMappe/TransferMappes/Templates/`
2. Charger les deux fichiers du kit :
   - `templates/word/transfer_mappe_template_de.docx`
   - `templates/word/transfer_mappe_template_en.docx`
3. Verifier que les fichiers sont accessibles par le compte de service Power Automate
4. Copier le chemin exact de chaque fichier (il sera utilise dans le Flow 2)

Chemin attendu :
- DE : `/sites/TransferMappe/TransferMappes/Templates/transfer_mappe_template_de.docx`
- EN : `/sites/TransferMappe/TransferMappes/Templates/transfer_mappe_template_en.docx`

---

## 5. Etape 4 : Creation du Flow J-5 (Invitation)

Suivre le guide detaille : `power_automate/Flow_1_Invitation_J-5.md`

Points critiques :
- Configurer la shared mailbox avant de creer le Flow
- Renseigner les URLs des Forms 3 et 4 dans les variables `varFormUrlDE` et `varFormUrlEN`
- Tester avec un participant fictif avant mise en production

---

## 6. Etape 5 : Creation du Flow PDF (Generation)

Suivre le guide detaille : `power_automate/Flow_2_Generation_PDF.md`

Points critiques :
- Verifier que les templates Word sont dans SharePoint (etape 3) avant de creer le Flow
- Renseigner les chemins des templates dans `varTemplatePathDE` et `varTemplatePathEN`
- Les 118 Content Controls doivent tous etre renseignes dans l'action "Populate"
- Tester avec un participant fictif disposant d'au moins 1 bilan

---

## 7. Etape 6 : Test avec un participant fictif

### 7.1 Creer le participant de test

Dans la liste Participants, creer manuellement un enregistrement :

| Colonne | Valeur de test |
|---|---|
| nom | Testperson |
| prenom | Test |
| email | votre.adresse.test@{domaine} |
| langue | DE |
| id_conseillere | conseillere.test@{domaine} |
| date_debut_parcours | date d'aujourd'hui - 1 mois |
| date_prochain_rdv | date d'aujourd'hui + 5 jours (pour tester Flow J-5) |
| statut | actif |
| Title | Test Testperson |

### 7.2 Tester le Flow J-5

1. Aller dans Power Automate > Mes flux > TransferMappe - Invitation J-5
2. Cliquer "Executer" (Run) manuellement
3. Verifier que l'email d'invitation est recu sur votre adresse de test
4. Verifier le lien formulaire dans l'email

### 7.3 Tester le Flow PDF

1. Modifier le participant de test : `date_prochain_rdv` = aujourd'hui
2. Creer manuellement un bilan dans BilansMensuels (toutes les colonnes pertinentes)
3. Executer le Flow PDF manuellement
4. Verifier que le PDF est recu par la conseillere de test et sauvegarde dans SharePoint

### 7.4 Nettoyer apres le test

Supprimer le participant fictif et ses donnees de test apres validation.

---

## 8. Etape 7 : Mise en production

1. Desactiver le mode test dans les deux Flows
2. Creer les vrais participants dans la liste Participants
3. Communiquer les liens des formulaires d'onboarding aux participants
4. Verifier les Flows le premier jour de production (consulter les journaux d'execution)

---

## 9. Variables de configuration globales

Toutes les valeurs a ajuster pour votre organisation.

| Variable | Valeur a renseigner | Ou l'utiliser |
|---|---|---|
| `{tenant}` | Identifiant de votre tenant M365 (ex. contoso) | Partout dans les URLs |
| `{domaine}` | Domaine email de l'organisation (ex. contoso.de) | Adresses email |
| `SiteUrl` | URL complete du site SharePoint cree a l'etape 1 | setup_lists.ps1, variables Flow |
| `varSharedMailbox` | Adresse de la shared mailbox expeditrice | Flow 1 et Flow 2 |
| `varFormUrlDE` | URL du Form 3 (bilan mensuel DE) | Flow 1 |
| `varFormUrlEN` | URL du Form 4 (bilan mensuel EN) | Flow 1 |
| `varTemplatePathDE` | Chemin SharePoint du template Word DE | Flow 2 |
| `varTemplatePathEN` | Chemin SharePoint du template Word EN | Flow 2 |
| Adresse admin erreurs | Destinataire des emails d'erreur des Flows | Flow 1 et Flow 2 |

---

## 10. Troubleshooting frequent

### Le script PnP echoue avec "Access Denied"

Verifier que le compte PowerShell est Site Collection Administrator sur le site.
Dans SharePoint Admin Center : Sites > site TransferMappe > Permissions.

### Le Flow J-5 ne trouve aucun participant

Verifier le filtre OData sur `date_prochain_rdv`. La colonne doit etre de type DateOnly.
Si la colonne stocke une heure, ajuster le filtre (voir note dans Flow_1_Invitation_J-5.md).

### Le Flow PDF echoue sur "Populate a Microsoft Word template"

Verifier que :
- Le fichier .docx est accessible par le compte de service Power Automate
- Tous les 118 Content Controls sont renseignes (aucun champ vide dans l'action)
- Le fichier n'est pas ouvert par un autre utilisateur au moment du Flow

### Le PDF est vide ou mal forme

Verifier que les Tag values dans le .docx correspondent exactement aux noms de champs
dans l'action "Populate". Consulter `specs/word_template_structure.md` pour la liste
exhaustive.

### La shared mailbox ne peut pas envoyer

La shared mailbox doit avoir la permission "Send As" octroyee au compte de service.
Dans Exchange Admin Center : Destinataires > Boites aux lettres partagees > Permissions.

### Le Flow depasse 30 minutes pour 100 participants

Verifier les limites de concurrence de Power Automate (par defaut, la boucle
"Apply to each" traite les elements sequentiellement). Activer la concurrence
(max 50 en parallele) sur la boucle si le volume le necessite.
Attention : la concurrence parallele peut entrainer des conflits sur les variables
globales - preferer les variables dans la portee de la boucle.
