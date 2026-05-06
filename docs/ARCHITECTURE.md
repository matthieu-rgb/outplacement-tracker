# Architecture technique - outplacement-tracker v0.1

Document de reference pour un architecte technique ou un decideur IT evaluant la solution.

---

## Vue d'ensemble

### Objectif de la solution

outplacement-tracker digitalise le suivi mensuel de participants en Transfergesellschaft (structure allemande de reclassement professionnel, cadre § 111 SGB III). La solution automatise deux processus :

1. **J-5** : envoi d'un formulaire de bilan mensuel au participant cinq jours avant son rendez-vous
2. **Jour J** : generation d'un PDF cumulatif (Transfer Mappe) remis a la conseillere avant le rendez-vous

Toutes les donnees restent dans le tenant Microsoft 365 du client. Aucun service tiers n'est implique.

### Diagramme d'architecture

```
PARTICIPANT                 TENANT M365 CLIENT                    CONSEILLERE
-----------                 --------------------------            -----------

                            SharePoint Online
                            +-----------------+
                            | Participants    |
                            | Profils         |
                            | BilansMensuels  |
                            | TransferMappes/ | (bibliotheque docs)
                            +-----------------+
                                    |
[Formulaire    ]  --reponse-->  Microsoft Forms
[onboarding    ]               (Forms 1/2)
[DE ou EN      ]               Pas de Flow associe
                               Saisie manuelle dans SP

[Formulaire    ]  <--email J-5--  Power Automate
[bilan mensuel ]                  Flow 1 : Invitation J-5
[DE ou EN      ]                  Declencheur : Planifie 07h00
                                  - Lit Participants (statut=actif, date=J+5)
                                  - Envoie email via shared mailbox
                                  - Lien vers Form 3 ou Form 4
                  --reponse-->  Microsoft Forms
                               (Forms 3/4)
                               Saisie dans BilansMensuels
                                  |
                                  v
                               Power Automate
                               Flow 2 : Generation PDF
                               Declencheur : Planifie 06h00
                               - Lit Participants (statut=actif, date=J)
                               - Lit Profils (id_participant)
                               - Lit BilansMensuels (id_participant, tri ASC)
                               - Populate Word template (118 Content Controls)
                               - Convertit Word -> PDF (natif E3)
                               - Sauvegarde PDF dans SharePoint
                               - Envoie PDF par email          --PDF-->  [Conseillere]

ADMIN M365
----------
PnP.PowerShell (setup unique)
  -> Cree les 3 listes SharePoint
  -> Script idempotent, rejoue sans erreur
```

### Flux de donnees

```
Formulaire Forms
    |
    v (reponse stockee dans Forms)
    |-- > Traitement manuel ou par Flow -> SharePoint Liste BilansMensuels ou Profils
    
SharePoint Participants (source de verite)
    |
    +-- > Flow 1 : lit date_prochain_rdv, envoie email
    +-- > Flow 2 : lit participant + profil + bilans, genere PDF

PDF genere
    |
    +-- > Email Outlook (piece jointe) -> conseillere
    +-- > Fichier SharePoint (archivage) -> TransferMappes/{Nom_Prenom}/
```

---

## Composants

### Microsoft Forms

**Role** : collecte des reponses des participants (onboarding et bilans mensuels) via un lien URL distribue par email ou manuellement. Aucun compte M365 requis pour le repondant.

**Pourquoi ce choix** :
- Natif M365 E3, aucun cout additionnel
- Interface responsive sur mobile et desktop sans installation
- Le lien de partage public permet l'acces sans compte M365, ce qui couvre les participants qui n'en ont pas
- Le connecteur "Microsoft Forms" dans Power Automate permet de lire les reponses directement

**Alternatives rejetees** :

| Alternative | Raison du rejet |
|---|---|
| Formulaire web custom (React, Vue) | Necessite un hebergement, maintenance, authentification : hors perimetre d'un kit M365 |
| Typeform / Google Forms | Donnees hors tenant, non conformes DSGVO pour un contexte d'emploi allemand |
| PowerApps canvas app | Necessite une licence PowerApps (hors plan E3 standard) |
| SharePoint list form | Interface peu adaptee aux participants (non informaticiens), pas de lien de partage public simple |

**Limites connues** :
- Pas de branchement conditionnel complexe (acceptable : les formulaires ont au maximum 7 questions lineaires)
- Pas de logique de pre-remplissage des reponses precedentes (hors scope v0.1)
- Limite de 200 questions par formulaire et 50 000 reponses par formulaire (largement suffisant pour le volume cible)

---

### SharePoint Online (listes)

**Role** : base de donnees operationnelle de la solution. Trois listes stockent les participants, les profils de carriere et les bilans mensuels. Une bibliotheque de documents stocke les PDFs generes et les templates Word.

**Pourquoi ce choix** :
- Natif M365 E3, integre nativement dans Power Automate sans connecteur premium
- Le connecteur SharePoint dans Power Automate est standard et supporte les filtres OData, le tri, la pagination
- Gestion des permissions native (les participants n'ont aucun acces au site)
- Versioning des elements active (5 versions conservees par element)
- Compatible avec PnP.PowerShell pour un provisioning reproductible et idempotent

**Alternatives rejetees** :

| Alternative | Raison du rejet |
|---|---|
| Excel Online (fichier .xlsx) | Pas de transactions, conflits d'ecriture simultanee, pas de filtre OData dans Power Automate |
| Dataverse | Necessite une licence Power Platform premium (hors E3 standard) |
| SQL Azure / Azure SQL | Necessite un abonnement Azure, un connecteur premium, une gestion reseau |
| Access (Access App) | Retire du service par Microsoft depuis 2018 |

**Limites connues** :
- Les listes SharePoint ne supportent pas les vraies cles etrangeres avec contraintes d'integrite referentielle. La relation `id_participant` (Number) dans Profils et BilansMensuels est une convention applicative, non enforced par SharePoint.
- Limite standard SharePoint : 30 millions d'elements par liste (sans impact au volume cible de 2 000 participants x 12 bilans = 24 000 elements)
- Le filtre OData sur les colonnes `DateTime` en mode DateOnly peut produire des comportements inattendus selon la timezone du tenant (voir troubleshooting dans INSTALLATION.md)

---

### Power Automate (Flows cloud)

**Role** : orchestration des deux processus automatises. Flow 1 (Invitation J-5) envoie les emails d'invitation. Flow 2 (Generation PDF) produit et distribue le PDF cumulatif.

**Pourquoi ce choix** :
- Inclus dans M365 E3, sans license Power Automate premium separee
- Les connecteurs SharePoint, Office 365 Outlook et Word Online (Business) sont des connecteurs standard disponibles en E3
- L'action "Remplir un modele Microsoft Word" (Populate a Microsoft Word template) et "Convertir en PDF" sont disponibles dans le connecteur Word Online (Business), inclus E3
- La planification (Schedule trigger) est disponible en E3
- Interface graphique de debug (historique d'executions, detail action par action)

**Alternatives rejetees** :

| Alternative | Raison du rejet |
|---|---|
| Azure Logic Apps | Necessite un abonnement Azure, facturation a l'execution |
| n8n self-hosted | Necessite un serveur, maintenance, hors ecosysteme M365 du client |
| Azure Functions (Node.js/Python) | Meme problematique Azure, plus la complexite de developpement |
| Scripts PowerShell planifies | Pas de gestion d'erreurs native, pas d'interface de monitoring, fragile en production |
| Power Automate Desktop | Necessite une licence Power Automate premium avec agent desktop |

**Limites connues** :
- Les Flows cloud en E3 ont une limite d'execution de 30 jours par execution (sans impact ici)
- La boucle "Apply to each" est sequentielle par defaut : pour 100 participants, le Flow PDF peut durer 20 a 30 minutes. La concurrence peut etre activee (voir INSTALLATION.md)
- Pas d'export JSON des Flows possible sans tenant (ADR-006) : les Flows sont documentes sous forme de blueprints Markdown, pas de fichiers importables directs en v0.1
- Limite du connecteur SharePoint "Get items" : 5 000 elements par appel. Pour le volume cible (2 000 participants), configurer le seuil a 2 000 dans l'action ou utiliser la pagination

---

### Templates Word avec Content Controls

**Role** : modeles de document (.docx) contenant 118 Content Controls de type Plain Text, chacun identifie par un Tag value unique. Power Automate injecte les donnees des listes SharePoint dans ces Content Controls via l'action "Populate a Microsoft Word template", puis convertit le document rempli en PDF.

**Pourquoi ce choix** :
- L'action "Populate a Microsoft Word template" du connecteur Word Online (Business) est disponible en E3 et supporte les Content Controls Plain Text avec Tag values
- Les Content Controls permettent un rendu Word fidelement structure (mise en page, polices, logo) impossible a reproduire avec une generation PDF programmatique basique
- Le format .docx reste modifiable par le client (mise en page, logo, couleurs) sans toucher aux Flows

**Alternatives rejetees** :

| Alternative | Raison du rejet |
|---|---|
| Balises Mail Merge (`<<champ>>`) | Non supportees par l'action "Populate" de Power Automate |
| Balises `{{champ}}` (style Handlebars) | Non supportees nativement par Word ni par Power Automate |
| Generation PDF via HTML + WeasyPrint / Puppeteer | Necessite un runtime externe, hors ecosysteme M365 |
| PDF generation via Adobe PDF Services | Connecteur premium, cout additionnel |
| LaTeX / Pandoc | Hors ecosysteme M365, necessite un serveur |

**Limites connues** :
- Les Content Controls "Repeating Section" (pour les boucles) ne sont pas supportes par l'action "Populate" de Power Automate. La solution retenue est de creer statiquement 12 sections bilan dans le template (une par mois possible), et d'injecter une chaine vide pour les bilans inexistants. Cela implique que le template a une structure fixe a 12 sections, avec du blanc visible en fin de document si le participant a moins de 12 bilans.
- La construction du .docx avec Content Controls corrects necessite un acces a Microsoft Word (les Content Controls ne peuvent pas etre crees correctement par python-docx ni par un agent sans runtime Word). Les templates du kit sont construits par script Python avec python-docx et valides par assertion programmatique.
- Modifier un Tag value dans le .docx apres mise en production necessite de mettre a jour le Flow correspondant.

---

### Outlook / Shared mailbox

**Role** : envoi des emails au participant (invitation J-5) et a la conseillere (PDF le jour du RDV), depuis une adresse generique de l'organisation.

**Pourquoi ce choix** :
- Le connecteur Office 365 Outlook est standard en E3
- L'action "Envoyer un e-mail (V2)" supporte l'envoi "De" (From) depuis une shared mailbox si le compte de service dispose de la permission "Send As"
- L'adresse expeditrice generique (`transfer@{domaine}.de`) evite les reponses accidentelles vers un compte nomme
- La shared mailbox est native M365, sans cout additionnel pour un tenant E3

**Alternatives rejetees** :

| Alternative | Raison du rejet |
|---|---|
| SendGrid / Mailgun | Service tiers, donnees potentiellement hors tenant, connecteur premium requis dans Power Automate |
| SMTP relay via Azure | Necessite un abonnement Azure, configuration complexe |
| Compte M365 nominatif comme expediteur | Probleme de gouvernance si le compte change ou est desactive |
| Microsoft Graph API | Necessite une Azure App registration et un connecteur custom (hors E3 standard) |

**Limites connues** :
- Limite Exchange Online E3 : 10 000 destinataires par jour pour l'envoi externe (largement au-dessus du volume cible de ~100 envois/jour)
- Les emails sont envoyés en HTML. Si le participant a desactive le HTML dans son client email, le bouton de lien sera rendu en texte brut (comportement correct : le lien reste cliquable).

---

## Decisions structurantes

Synthese des Architecture Decision Records du projet. Document complet : `docs/DECISIONS.md`.

### ADR-001 : Stack Microsoft 365 uniquement

La solution s'appuie exclusivement sur des services Microsoft 365 E3 (Forms, SharePoint, Power Automate, Word, Outlook). Aucune dependance externe.

Raisons principales : le contexte Transfergesellschaft allemand utilise quasi-universellement M365, la conformite DSGVO est acquise par construction (donnees dans le tenant client), et le cout marginal est nul (licences deja payees).

Les alternatives evaluees (Google Workspace, n8n self-hosted, Node.js custom) ont ete rejetees pour des raisons de compliance DSGVO, de cout de maintenance ou d'inadaptation au contexte client.

### ADR-002 : Signatures manuscrites preservees sur les Zielvereinbarungen

Les emplacements de signature dans le PDF cumulatif sont laisses vides. Le document est imprime au RDV, signe physiquement, et scanne si l'organisation souhaite conserver une copie numerique.

Raison : les solutions de signature electronique conforme eIDAS (DocuSign, Microsoft eSign, Adobe Sign) impliquent soit une licence premium, soit un service tiers. Les signatures manuscrites sont legalement suffisantes pour les Zielvereinbarungen au sens du § 111 SGB III.

L'integration d'un module eSign est documentee dans le backlog pour une v0.2.

### ADR-003 : Bilan mensuel declaratif libre

Six champs dans le formulaire mensuel, un seul obligatoire (bilan general). Le participant decide de ce qu'il partage.

Raison : la Transfer Mappe est un outil de la relation participant-conseillere, pas un outil de surveillance. Un formulaire trop contraignant reduirait le taux de reponse et n'est pas coherent avec l'esprit du dispositif. La minimisation des donnees collectees renforce egalement la conformite DSGVO.

### ADR-004 : Limite de 12 mois de parcours

Le template Word inclut 12 sections mensuelles. Cette limite est conforme au plafond legal du § 111 SGB III (duree maximale d'une Transfergesellschaft : 12 mois).

### ADR-005 : Templates Word specifies avant d'etre construits

Les specifications des templates Word (structure des 118 Content Controls, Tag values, mapping Power Automate) ont ete livrees en Sprint 1 sous forme de fichiers Markdown. La construction des .docx reels est une tache separee necessitant un acces a Microsoft Word ou a python-docx.

### ADR-006 : Livraison Sprint 2 en mode blueprint

En l'absence de tenant Microsoft 365 Developer Program disponible au moment du Sprint 2, les Flows Power Automate et Microsoft Forms ne sont pas exportes en JSON importable mais documentes sous forme de guides d'implementation Markdown (action par action, expressions exactes).

Consequence pratique : le deploiement prend 1 a 2 heures plutot que 30 minutes (si les JSON etaient importables). La qualite fonctionnelle n'est pas affectee.

---

## Securite et DSGVO

### Perimetre des donnees

Toutes les donnees traitees restent dans le tenant Microsoft 365 du client :
- Reponses des formulaires : stockees dans Microsoft Forms (tenant client)
- Donnees participants et bilans : listes SharePoint (tenant client)
- PDFs generes : bibliotheque SharePoint (tenant client)
- Emails envoyes : Exchange Online du tenant client

Aucune donnee ne transite par un service tiers. Aucun webhook externe. Aucune connexion a une API externe.

### Minimisation des donnees (DSGVO Art. 5.1.c)

La solution collecte uniquement les donnees necessaires au processus de suivi :
- Cote participant : nom, prenom, email, langue, date debut, date RDV, statut
- Cote profil : donnees de carriere saisies voluntairement, toutes optionnelles
- Cote bilans : bilan mensuel (seul champ obligatoire), cinq champs optionnels

Les formulaires Microsoft Forms sont configures en mode anonyme (desactivation du "Record name") : la reponse n'est pas liee a un compte M365.

### Acces aux donnees

| Acteur | Acces |
|---|---|
| Participants | Aucun acces au site SharePoint. Acces uniquement a leurs formulaires Forms publics |
| Conseilleres | Membres du site SharePoint. Lecture des listes, reception des PDFs par email |
| Administrateur | Proprietaire du site. Acces complet |
| Compte de service Power Automate | Membre du site. Lecture/ecriture listes et bibliotheques |

Les participants n'ont aucun acces aux donnees des autres participants. Les listes SharePoint ne sont pas exposees publiquement.

### Responsabilite de traitement

Le kit est un outil, pas un service. L'auteur ne traite aucune donnee personnelle de participants. La societe de reclassement qui deploie le kit est responsable de traitement au sens du DSGVO, dans les limites du tenant M365 qu'elle administre.

L'organisation deploieuse est responsable de la conclusion d'un Auftragsverarbeitungsvertrag (AVV) avec Microsoft pour le traitement des donnees personnelles via M365, conformement au DSGVO Art. 28. Microsoft propose des termes contractuels standard dans le cadre de leur Data Processing Agreement M365.

### Retention des donnees

Aucune politique de retention automatique n'est implementee en v0.1. L'organisation deploieuse est responsable de definir et appliquer sa propre politique de conservation et suppression des donnees (recommandation : supprimer les enregistrements SharePoint et les PDFs au terme du parcours, apres les delais de conservation legaux applicables).

---

## Scalabilite

### Volumes cibles et limites

| Composant | Volume cible | Limite du service | Marge |
|---|---|---|---|
| Participants simultanes | 2 000 | 30 millions d'elements par liste SharePoint | Tres large |
| Bilans mensuels total | 24 000 (2 000 x 12) | 30 millions d'elements par liste | Tres large |
| Envois email par jour | ~100 (ouvres) | 10 000 destinataires/jour Exchange Online E3 | Large |
| PDFs generes par jour | ~100 | Limite Power Automate : duree execution, pas volume | Acceptable |
| Formulaires Forms | 4 formulaires | 200 questions / 50 000 reponses par formulaire | Large |
| Concurrence Flow | Sequentiel par defaut | 50 en parallele (Apply to each) | Ajustable |

### Temps d'execution des Flows

**Flow 1 - Invitation J-5** : environ 1 a 2 secondes par participant (appel SharePoint + envoi email). Pour 100 participants par jour : 2 a 3 minutes.

**Flow 2 - Generation PDF** : environ 15 a 20 secondes par participant (lecture profil + bilans + populate Word + conversion PDF + sauvegarde SharePoint + envoi email). Pour 100 participants : 25 a 30 minutes en mode sequentiel. En activant la concurrence (20 en parallele) : environ 5 a 8 minutes.

### Passage a l'echelle

Pour des volumes superieurs a 2 000 participants simultanes ou 100 PDFs par jour :
- Activer la concurrence sur les boucles "Apply to each" (jusqu'a 50 en parallele)
- Augmenter le "Nombre maximal d'elements" dans les actions "Get items" (defaut : 100, max : 5 000 par appel)
- Pour des volumes superieurs a 5 000 participants, implementer la pagination dans les actions SharePoint (propriete `odata-skiptoken`)
- Les limites Exchange Online (10 000 emails/jour) ne sont pas un facteur limitant pour le volume cible

---

## Limites connues et evolutions prevues

### Limites de la v0.1

**Sections bilan fixes dans le PDF** : le template Word contient exactement 12 sections mensuelles. Les sections non utilisees apparaissent vides en fin de document. Power Automate ne supporte pas les Content Controls "Repeating Section" pour une generation dynamique du nombre de sections.

**Pas d'import JSON des Flows** : en raison de l'absence de tenant Dev pendant le Sprint 2 (ADR-006), les Flows sont livres sous forme de blueprints Markdown et non de fichiers JSON importables. L'export JSON sera produit lors du premier deploiement reel.

**Relations sans contrainte d'integrite** : la jointure entre `BilansMensuels.id_participant` et `Participants.ID` est une convention applicative. SharePoint ne garantit pas l'integrite referentielle. Une suppression manuelle d'un participant sans supprimer ses bilans cree des enregistrements orphelins.

**Pas de deduplication des bilans** : si un participant soumet deux fois le formulaire mensuel avant le meme RDV, deux enregistrements BilansMensuels sont crees. La conseillere verra deux bilans pour la meme periode dans le PDF. La gestion de ce cas est a la charge de l'administrateur (suppression manuelle du doublon).

### Evolutions prevues (backlog)

**v0.2 - Module eSign** (ADR-002) : integration d'un module de signature electronique optionnel pour les Zielvereinbarungen, via Microsoft eSign ou un connecteur compatible eIDAS. Conditionnel a l'existence d'une licence appropriee chez le client.

**v0.2 - Tracker personnel opt-in** (ADR-003) : module optionnel permettant au participant de saisir ses candidatures et contacts au fil de l'eau, avec agregation dans le PDF cumulatif. Architecture envisagee : deux listes SharePoint supplementaires (Candidatures, Contacts) et un Flow de consolidation.

**v0.1.1 - Export JSON des Flows** : une fois deploye sur un tenant reel, exporter les Flows en JSON pour faciliter les deploiements ultérieurs.

---

## Dependances

### Licences requises

| Service | Licence minimum | Inclus dans E3 |
|---|---|---|
| Microsoft Forms | M365 E1 | Oui |
| SharePoint Online | M365 E1 | Oui |
| Power Automate (connecteurs standard) | M365 E3 | Oui |
| Word Online (Business) - connecteur Power Automate | M365 E3 | Oui |
| Office 365 Outlook - connecteur Power Automate | M365 E1 | Oui |
| Exchange Online (shared mailbox) | M365 E1 | Oui |

Aucun connecteur Power Automate Premium n'est utilise. La solution est integralement compatible avec un plan M365 E3 standard.

### Outils de deploiement (setup uniquement)

| Outil | Version | Usage |
|---|---|---|
| PowerShell | 7.x | Execution du script de provisioning SharePoint |
| PnP.PowerShell | Derniere version stable | Provisioning des listes SharePoint (setup unique) |

PnP.PowerShell n'est requis que pour le deploiement initial. Il n'est pas utilise en production.

### Dependances de runtime

Aucune dependance externe de runtime. La solution fonctionne exclusivement avec les services Microsoft 365 du tenant client. Aucun serveur externe, aucune cle API tierce, aucun service d'hebergement supplementaire.
