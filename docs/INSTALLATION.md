# Guide d'installation - outplacement-tracker v0.1

Guide de deploiement pas-a-pas pour un administrateur Microsoft 365.
Duree estimee : 1 a 2 heures.

---

## Prerequis

### Tenant et licences

- Tenant Microsoft 365 avec plan **E3 ou superieur**
  - Requis pour : Word Online (Business), Power Automate inclus, Exchange Online
  - Aucun connecteur Power Automate Premium n'est utilise
- Au moins un compte avec les roles suivants :
  - SharePoint Administrator (pour creer le site et les listes)
  - Exchange Administrator (pour configurer la shared mailbox)
  - Compte de service dedie pour les Flows Power Automate (recommande : compte non nominatif, ex. `service-transfermappe@{domaine}`)

### Outils requis sur la machine de l'administrateur

- **PowerShell 7+** : [https://github.com/PowerShell/PowerShell/releases](https://github.com/PowerShell/PowerShell/releases)
- **Module PnP.PowerShell** (installation unique) :

```powershell
Install-Module PnP.PowerShell -Force -Scope CurrentUser
```

- Navigateur moderne avec acces a `https://admin.microsoft.com`, `https://make.powerautomate.com`, `https://forms.microsoft.com`

### Repertoire de travail

Cloner ou telecharger le kit sur la machine de l'administrateur :

```
/chemin/vers/outplacement-tracker/
  sharepoint/
    setup_lists.ps1
    lists_schema.json
  templates/word/
    transfer_mappe_template_de.docx
    transfer_mappe_template_en.docx
  forms/
    forms_construction_guide.md
  power_automate/
    Flow_1_Invitation_J-5.md
    Flow_2_Generation_PDF.md
```

---

## Etape 1 - Creer le site SharePoint

### 1.1 Creer le site

1. Aller sur `https://{tenant}-admin.sharepoint.com` (SharePoint Admin Center)
2. Cliquer sur **Sites actifs** > **Creer** > **Site d'equipe** (Team Site)
3. Renseigner :
   - Nom du site : `TransferMappe`
   - Adresse du site : `transfermappe` (URL resultante : `https://{tenant}.sharepoint.com/sites/transfermappe`)
   - Propriétaires du site : le compte administrateur et le compte de service Power Automate
   - Langue : selon preference (n'affecte pas les donnees)
   - Parametres de confidentialite : **Prive** (les participants n'ont aucun acces)
4. Cliquer sur **Terminer**

L'URL du site (appelee `SiteUrl` dans la suite) est : `https://{tenant}.sharepoint.com/sites/transfermappe`

### 1.2 Configurer les permissions

Dans le site cree, aller dans **Parametres** > **Autorisations du site** :

| Compte | Role SharePoint |
|---|---|
| Administrateur deploiement | Proprietaire (Site Collection Admin) |
| Compte de service Power Automate | Membre (lecture + ecriture listes et bibliotheques) |
| Conseilleres | Membre (lecture des listes, reception des PDF) |
| Participants | Aucun acces au site |

---

## Etape 2 - Provisioning des listes SharePoint

### 2.1 Ouvrir PowerShell 7 et se connecter

```powershell
Connect-PnPOnline -Url "https://{tenant}.sharepoint.com/sites/transfermappe" -Interactive
```

Une fenetre de login s'ouvre. Utiliser le compte administrateur M365. Accepter les permissions demandees par PnP.PowerShell (premiere connexion uniquement).

### 2.2 Executer le script de provisioning

```powershell
# Depuis le repertoire du kit
.\sharepoint\setup_lists.ps1 -SiteUrl "https://{tenant}.sharepoint.com/sites/transfermappe"
```

Le script est **idempotent** : il peut etre rejoue sans erreur si les listes existent deja. Il affiche dans la console ce qu'il cree et ce qu'il ignore.

### 2.3 Verifier le resultat

En sortie du script, la console doit afficher :

```
[OK] Participants - N colonnes visibles
[OK] Profils - N colonnes visibles
[OK] BilansMensuels - N colonnes visibles
```

Dans le navigateur, aller sur `https://{tenant}.sharepoint.com/sites/transfermappe` > **Contenu du site** et verifier que les 3 listes sont presentes.

### 2.4 Structure des listes creees

**Liste Participants** (table centrale, une ligne par participant) :

| Colonne | Type | Requis | Note |
|---|---|---|---|
| Title | Text | Oui | Format : `{prenom} {nom}` |
| nom | Text | Oui | |
| prenom | Text | Oui | |
| email | Text | Oui | Email du participant |
| langue | Choice | Oui | DE ou EN, defaut : DE |
| id_conseillere | Text | Oui | Email M365 de la conseillere |
| date_debut_parcours | DateTime (DateOnly) | Oui | |
| date_prochain_rdv | DateTime (DateOnly) | Oui | Mis a jour apres chaque RDV |
| statut | Choice | Oui | actif / suspendu / termine |

**Liste Profils** (profil de carriere optionnel, zero ou une ligne par participant) :

| Colonne | Type | Requis |
|---|---|---|
| id_participant | Number | Oui |
| plan_a | Note (multiline) | Non |
| plan_b | Note (multiline) | Non |
| marketingplan | Note (multiline) | Non |
| zielmarkt | Note (multiline) | Non |
| date_creation | DateTime | Oui |
| date_modification | DateTime | Non |

**Liste BilansMensuels** (zero a douze bilans par participant) :

| Colonne | Type | Requis |
|---|---|---|
| id_participant | Number | Oui |
| date_rdv | DateTime (DateOnly) | Oui |
| date_soumission | DateTime | Oui |
| bilan_general | Note (multiline) | Oui |
| statut_objectifs | Choice | Non |
| statut_objectifs_detail | Note (multiline) | Non |
| was_lief_gut | Note (multiline) | Non |
| wo_brauche_ich_unterstuetzung | Note (multiline) | Non |
| themen_naechster_termin | Note (multiline) | Non |
| sonstige_anmerkungen | Note (multiline) | Non |

---

## Etape 3 - Creer la bibliotheque de documents

La bibliotheque stocke les PDFs generes et les templates Word.

1. Sur le site SharePoint, cliquer **Nouveau** > **Bibliotheque de documents**
2. Nom : `TransferMappes`
3. Cliquer sur **Creer**
4. Dans la bibliotheque `TransferMappes`, cliquer **Nouveau** > **Dossier**
5. Nom du dossier : `Templates`

Structure attendue dans SharePoint :

```
/sites/transfermappe/TransferMappes/
  Templates/       <- templates Word
  Nom_Prenom/      <- cree automatiquement par le Flow lors de la premiere generation
```

---

## Etape 4 - Deposer les templates Word

1. Dans la bibliotheque SharePoint, naviguer vers `TransferMappes/Templates/`
2. Cliquer **Charger** > **Fichiers**
3. Selectionner les deux fichiers depuis le kit :
   - `templates/word/transfer_mappe_template_de.docx`
   - `templates/word/transfer_mappe_template_en.docx`
4. Verifier que les deux fichiers sont visibles dans le dossier `Templates`

Chemins SharePoint resultants (a utiliser dans le Flow 2) :

```
/sites/transfermappe/TransferMappes/Templates/transfer_mappe_template_de.docx
/sites/transfermappe/TransferMappes/Templates/transfer_mappe_template_en.docx
```

Verifier que le compte de service Power Automate peut ouvrir ces fichiers (Acces membre sur la bibliotheque).

---

## Etape 5 - Creer les formulaires Microsoft Forms

Suivre le guide detaille : `forms/forms_construction_guide.md`

Les 4 formulaires sont crees sur le compte de service (ou la boite partagee), pas sur un compte nominatif.

### 5.1 Se connecter a Microsoft Forms

Aller sur `https://forms.microsoft.com` avec le compte de service.

### 5.2 Creer les 4 formulaires dans l'ordre

| # | Titre | Langue | Usage |
|---|---|---|---|
| 1 | Ihr Karriereprofil - Transfer Mappe | DE | Onboarding (une fois) |
| 2 | Your Career Profile - Transfer Mappe | EN | Onboarding (une fois) |
| 3 | Ihr monatlicher Bericht - Transfer Mappe | DE | Bilan mensuel |
| 4 | Your Monthly Update - Transfer Mappe | EN | Bilan mensuel |

Pour chaque formulaire, suivre la procedure detaillee dans `forms/forms_construction_guide.md` (structure des questions, textes exacts, messages de confirmation).

### 5.3 Configuration post-creation (applicable aux 4 formulaires)

Dans les **Parametres** de chaque formulaire :

- **Partage** : choisir "Jeder mit dem Link kann antworten" / "Anyone with the link can respond". Ne pas restreindre aux comptes M365 (les participants n'ont pas de compte M365).
- **Enregistrement du nom** : desactiver "Record name" (minimisation des donnees DSGVO).
- **Reponses multiples** : ne pas cocher "Une reponse par personne" (le Flow envoie un lien a chaque RDV).

### 5.4 Recuperer les URLs des formulaires 3 et 4

Pour les Forms 3 et 4 (bilans mensuels uniquement) :

1. Ouvrir le formulaire
2. Cliquer **Partager** > **Copier le lien**
3. Conserver ces deux URLs : elles seront utilisees dans les variables des Flows

Exemple de format d'URL Forms :
```
https://forms.office.com/r/XXXXXXXXXX
```

Les formulaires 1 et 2 (onboarding) ne sont pas utilises par les Flows. Leur lien est communique manuellement par la conseillere en debut de parcours.

---

## Etape 6 - Creer le Flow J-5 (invitation)

Suivre le guide detaille : `power_automate/Flow_1_Invitation_J-5.md`

### 6.1 Prerequis avant de creer le Flow

- La shared mailbox expeditrice doit etre configuree (voir Etape 8)
- Les URLs des Forms 3 et 4 doivent etre disponibles (voir Etape 5.4)

### 6.2 Creer le Flow

1. Aller sur `https://make.powerautomate.com` avec le compte de service
2. Cliquer **Creer** > **Flux planifie**
3. Nom : `TransferMappe - Invitation J-5`
4. Heure de debut : `07:00`, Repeter toutes les : `1 jour`
5. Construire les actions dans l'ordre defini dans `Flow_1_Invitation_J-5.md`

### 6.3 Variables a renseigner obligatoirement

Dans les actions "Initialiser une variable" en debut de Flow :

| Variable | Valeur a renseigner |
|---|---|
| `varSiteUrl` | `https://{tenant}.sharepoint.com/sites/transfermappe` |
| `varSharedMailbox` | Adresse de la shared mailbox (ex. `transfer@{domaine}.de`) |
| `varFormUrlDE` | URL du Form 3 (bilan mensuel DE) |
| `varFormUrlEN` | URL du Form 4 (bilan mensuel EN) |

### 6.4 Configurer la gestion d'erreurs

Ajouter l'action `Notifier_erreur` hors de la boucle, avec **Run after : a echoue**.
Renseigner l'adresse email de l'administrateur en destinataire.

### 6.5 Sauvegarder et activer le Flow

Cliquer **Enregistrer** puis verifier que le Flow est en statut **Actif**.

---

## Etape 7 - Creer le Flow PDF (generation)

Suivre le guide detaille : `power_automate/Flow_2_Generation_PDF.md`

### 7.1 Prerequis avant de creer le Flow

- Les templates Word doivent etre deposes dans SharePoint (voir Etape 4)
- La bibliotheque `TransferMappes` doit exister (voir Etape 3)

### 7.2 Creer le Flow

1. Sur `https://make.powerautomate.com`
2. Cliquer **Creer** > **Flux planifie**
3. Nom : `TransferMappe - Generation PDF`
4. Heure de debut : `06:00`, Repeter toutes les : `1 jour`
5. Construire les actions dans l'ordre defini dans `Flow_2_Generation_PDF.md`

Le Flow PDF se declenche a 06h00, une heure avant le Flow Invitation (07h00), pour eviter toute collision.

### 7.3 Variables a renseigner obligatoirement

| Variable | Valeur a renseigner |
|---|---|
| `varSiteUrl` | `https://{tenant}.sharepoint.com/sites/transfermappe` |
| `varSharedMailbox` | Adresse de la shared mailbox |
| `varTemplatePathDE` | `/sites/transfermappe/TransferMappes/Templates/transfer_mappe_template_de.docx` |
| `varTemplatePathEN` | `/sites/transfermappe/TransferMappes/Templates/transfer_mappe_template_en.docx` |

### 7.4 Renseigner les 118 Content Controls

L'action "Remplir un modele Microsoft Word" requiert le mapping complet des 118 Content Controls. Voir le tableau exhaustif dans `power_automate/Flow_2_Generation_PDF.md`, section "Mapping des Content Controls".

Ne jamais laisser un champ vide dans cette action : injecter `""` pour les bilans inexistants.

### 7.5 Sauvegarder et activer le Flow

Cliquer **Enregistrer** puis verifier que le Flow est en statut **Actif**.

---

## Etape 8 - Configurer la shared mailbox

### 8.1 Creer la shared mailbox (si elle n'existe pas)

1. Aller sur `https://admin.microsoft.com` > **Exchange** > **Destinataires** > **Boites aux lettres partagees**
2. Cliquer **Ajouter une boite aux lettres partagee**
3. Nom d'affichage : `Transfer Mappe`
4. Adresse email : `transfer@{domaine}.de` (ou selon convention interne)
5. Cliquer **Enregistrer**

### 8.2 Accorder la permission "Send As" au compte de service

1. Dans Exchange Admin Center, ouvrir la shared mailbox `transfer@{domaine}.de`
2. Cliquer sur l'onglet **Delegation**
3. Sous **Envoyer en tant que (Send As)**, cliquer **Modifier**
4. Ajouter le compte de service Power Automate
5. Enregistrer

Attendre 5 a 15 minutes que la permission se propage avant de tester.

### 8.3 Verifier

Sur `https://outlook.office.com` avec le compte de service, verifier que la shared mailbox apparait dans la liste des boites. Sinon, l'ajouter manuellement : **Parametres** > **Ouvrir une autre boite aux lettres**.

---

## Etape 9 - Test avec un participant fictif

Cette etape valide le bon fonctionnement bout-en-bout avant la mise en production.

### 9.1 Creer le participant de test

Dans la liste SharePoint `Participants`, cliquer **Nouveau** et renseigner :

| Colonne | Valeur |
|---|---|
| Title | `Test Testperson` |
| nom | `Testperson` |
| prenom | `Test` |
| email | votre adresse email personnelle (pour recevoir le mail de test) |
| langue | `DE` |
| id_conseillere | votre adresse email (pour recevoir le PDF) |
| date_debut_parcours | date d'aujourd'hui - 1 mois |
| date_prochain_rdv | date d'aujourd'hui + 5 jours |
| statut | `actif` |

### 9.2 Tester le Flow J-5

1. Dans Power Automate, ouvrir `TransferMappe - Invitation J-5`
2. Cliquer **Executer** (execution manuelle)
3. Verifier dans la boite de reception que l'email d'invitation est recu
4. Cliquer le lien dans l'email pour confirmer qu'il ouvre le bon formulaire Forms

### 9.3 Creer un bilan de test

Dans la liste SharePoint `BilansMensuels`, cliquer **Nouveau** et renseigner :

| Colonne | Valeur |
|---|---|
| Title | `2026-05-01 - Test Testperson` |
| id_participant | `{ID SharePoint du participant de test}` |
| date_rdv | date d'aujourd'hui |
| date_soumission | date d'aujourd'hui |
| bilan_general | `Bilan de test - a supprimer` |

L'ID SharePoint du participant est visible dans l'URL lors de l'edition de l'element (parametre `ID=...`).

### 9.4 Modifier la date du RDV et tester le Flow PDF

1. Dans la liste Participants, modifier le participant de test : `date_prochain_rdv` = aujourd'hui
2. Dans Power Automate, ouvrir `TransferMappe - Generation PDF`
3. Cliquer **Executer** (execution manuelle)
4. Verifier :
   - L'email avec le PDF en piece jointe est recu par la conseillere de test
   - Le PDF est sauvegarde dans `TransferMappes/Testperson_Test/`
   - Le PDF est lisible et contient les donnees du bilan de test

### 9.5 Verifier les journaux d'execution

Dans Power Automate, ouvrir chaque Flow et consulter **Historique des executions** (28 derniers jours). Une execution reussie affiche le statut "Reussi" en vert. En cas d'echec, cliquer sur l'execution pour voir le detail de l'action en erreur.

### 9.6 Nettoyer apres le test

Supprimer dans SharePoint :
- L'element de la liste `Participants` (participant de test)
- L'element de la liste `BilansMensuels` (bilan de test)
- Le dossier `TransferMappes/Testperson_Test/` et son contenu

---

## Etape 10 - Nettoyage et mise en production

### 10.1 Verifications finales avant ouverture

- [ ] Les deux Flows sont en statut "Actif"
- [ ] La shared mailbox envoie correctement (test reussi a l'etape 9)
- [ ] Les templates Word sont accessibles par le compte de service
- [ ] Les 4 formulaires Forms sont en acces public (lien sans compte requis)
- [ ] Les donnees de test sont supprimees des 3 listes SharePoint

### 10.2 Creer les vrais participants

Dans la liste SharePoint `Participants`, creer un enregistrement par participant.
Le champ `date_prochain_rdv` doit etre renseigne pour que les Flows s'activent.

### 10.3 Distribuer les liens des formulaires d'onboarding

Les conseilleres communiquent manuellement le lien du Form 1 (DE) ou Form 2 (EN) aux participants en debut de parcours. Ces formulaires ne sont pas envoyes automatiquement par les Flows.

### 10.4 Surveiller les premiers jours de production

Consulter les **Historiques d'execution** des deux Flows dans Power Automate les 3 premiers jours ouvres. En cas d'echec, une notification email est envoyee automatiquement a l'administrateur (action `Notifier_erreur` configuree a l'etape 6.4 et 7.5).

---

## Variables de configuration

Recapitulatif de toutes les valeurs a ajuster. A conserver dans un document interne securise.

| Variable | Valeur a renseigner | Utilisation |
|---|---|---|
| `{tenant}` | Identifiant du tenant M365 (ex. `contoso`) | Toutes les URLs SharePoint et admin |
| `{domaine}` | Domaine email de l'organisation (ex. `contoso.de`) | Adresses email, shared mailbox |
| `SiteUrl` | URL complete du site (ex. `https://contoso.sharepoint.com/sites/transfermappe`) | Script PowerShell, variables Flow |
| `varSharedMailbox` | Adresse expeditrice (ex. `transfer@contoso.de`) | Flow 1 et Flow 2 |
| `varFormUrlDE` | URL du Form 3 - bilan mensuel DE | Flow 1 |
| `varFormUrlEN` | URL du Form 4 - bilan mensuel EN | Flow 1 |
| `varTemplatePathDE` | `/sites/transfermappe/TransferMappes/Templates/transfer_mappe_template_de.docx` | Flow 2 |
| `varTemplatePathEN` | `/sites/transfermappe/TransferMappes/Templates/transfer_mappe_template_en.docx` | Flow 2 |
| Adresse admin erreurs | Email de l'administrateur (destinataire des alertes) | Flow 1 et Flow 2 |
| Compte de service | Email du compte service Power Automate | Connexions Power Automate, Send As |

---

## Troubleshooting

### Le script PnP echoue avec "Access Denied"

**Cause** : le compte PowerShell n'est pas Site Collection Administrator sur le site.

**Solution** : dans le SharePoint Admin Center, aller sur **Sites actifs** > selectionner le site TransferMappe > **Appartenance** > ajouter le compte comme proprietaire.

---

### Le script PnP echoue avec "The remote server returned an error: (403)"

**Cause** : le module PnP.PowerShell utilise une version d'authentification incompatible avec les parametres du tenant (MFA, Conditional Access).

**Solution** : s'assurer d'utiliser `-Interactive` comme methode de connexion. Verifier que les politiques de Conditional Access du tenant autorisent les applications tierces sur le poste de l'administrateur.

---

### Le Flow J-5 ne trouve aucun participant alors que la date correspond

**Cause** : le filtre OData sur `date_prochain_rdv` peut echouer si la colonne stocke une valeur DateTime avec heure (meme `T00:00:00Z`).

**Solution** : dans l'action `Get_participants_J5`, remplacer le filtre OData par :

```
statut eq 'actif' and date_prochain_rdv ge '@{outputs('Calculer_date_cible')}T00:00:00Z' and date_prochain_rdv lt '@{outputs('Calculer_date_cible')}T23:59:59Z'
```

---

### Le Flow PDF echoue sur l'action "Remplir un modele Microsoft Word"

**Causes possibles et solutions** :

1. **Fichier template introuvable** : verifier le chemin exact dans `varTemplatePathDE` / `varTemplatePathEN`. Le chemin est sensible a la casse et ne doit pas inclure l'URL du site en prefixe.

2. **Fichier ouvert par un autre utilisateur** : l'action echoue si le .docx est en cours d'edition dans Word Online. S'assurer que personne ne modifie le fichier pendant l'execution du Flow.

3. **Content Control manquant** : si un Tag value dans le .docx ne correspond pas exactement au champ renseigne dans l'action Power Automate, le Flow echoue. Verifier la correspondance exacte des Tag values (liste exhaustive dans `specs/word_template_structure.md`).

4. **Champ vide dans l'action** : tous les 118 champs doivent etre renseignes. Injecter `""` pour les bilans inexistants plutot que de laisser le champ vide.

---

### La shared mailbox ne peut pas envoyer (erreur "Send As" refusee)

**Cause** : la permission "Send As" n'est pas encore propagee, ou le compte de service n'est pas dans la liste.

**Solution** :
1. Dans Exchange Admin Center, verifier que le compte de service est bien dans la delegation "Send As" de la shared mailbox
2. Attendre 15 minutes pour la propagation
3. Si le probleme persiste, supprimer et re-ajouter la permission

---

### Le PDF est genere mais vide ou avec des champs non remplis

**Cause** : des Content Controls dans le template .docx ont des Tag values qui ne correspondent pas exactement aux expressions Power Automate.

**Solution** : ouvrir le .docx dans Word, activer l'affichage des Content Controls (Developer > Design Mode), et verifier les Tag values de chaque Content Control. Les comparer avec la liste dans `specs/word_template_structure.md`.

---

### Le Flow depasse le delai d'execution pour un grand volume de participants

**Contexte** : Power Automate traite par defaut les elements d'une boucle "Apply to each" sequentiellement. Pour 100 participants, le Flow PDF peut prendre 20 a 30 minutes.

**Solution** : activer la concurrence sur la boucle principale :
1. Dans la boucle "Pour_chaque_participant_rdv", cliquer les trois points > **Parametres**
2. Activer **Controle de concurrence**, regler sur 10 a 20 (ne pas depasser 50)
3. Attention : avec la concurrence activee, utiliser des variables locales a la boucle et non des variables globales

---

### Un participant recoit l'invitation mais pas en bonne langue

**Cause** : la colonne `langue` de cet enregistrement dans Participants n'est pas correctement renseignee.

**Solution** : dans la liste SharePoint `Participants`, verifier la valeur de la colonne `langue` pour ce participant. La valeur doit etre exactement `DE` ou `EN` (majuscules, sans espace).
