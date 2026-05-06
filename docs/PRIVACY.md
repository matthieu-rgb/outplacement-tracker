# PRIVACY.md - Protection des donnees personnelles

outplacement-tracker v0.1 - Document a destination des organisations deployant cette solution

---

## 1. Portee et objet de ce document

Ce document s'adresse aux Transfergesellschaften et societes de reclassement professionnel
qui deploient la solution outplacement-tracker dans leur tenant Microsoft 365.

Il decrit :

- les donnees personnelles traitees par la solution et leurs finalites
- la base legale de chaque traitement
- les durees de conservation recommandees
- les droits des personnes concernees et leur mode d'exercice
- les mesures techniques et organisationnelles (TOM) applicables
- la chaine de responsabilite sous le RGPD et le BDSG

Ce document ne constitue pas un avis juridique. Chaque organisation deployant la solution
doit le completer et l'adapter a sa propre situation, en lien avec son DPD (Datenschutzbeauftragter)
ou son conseil juridique.

---

## 2. Modele de responsabilite (Verantwortlichkeit)

### 2.1 Chaine de responsabilite

```
[Participant (Teilnehmer)]
   |
   Personne concernee au sens de l'Art. 4(1) DSGVO.
   Titulaire des droits Art. 15 a 22 DSGVO.
   |
   v
[Societe de reclassement / Transfergesellschaft]
   |
   RESPONSABLE DE TRAITEMENT (Verantwortlicher) au sens de l'Art. 4(7) DSGVO.
   Determine les finalites et les moyens du traitement.
   Tient le Verzeichnis der Verarbeitungstatigkeiten (Art. 30 DSGVO).
   Informe les participants (Art. 13 DSGVO).
   Garantit l'exercice des droits (Art. 15-22 DSGVO).
   Signe l'AVV avec Microsoft (voir section 8).
   |
   v
[Matthieu Riegert - auteur du projet]
   |
   N'EST NI RESPONSABLE DE TRAITEMENT NI SOUS-TRAITANT.
   Livre un kit open source sous licence libre.
   Ne traite, ne stocke, ne consulte et n'accede a aucune donnee personnelle.
   N'a aucun acces au tenant Microsoft 365 de l'organisation deployant la solution.
   Aucun AVV ne doit etre signe avec l'auteur.
   |
   v
[Microsoft Corporation]
   |
   SOUS-TRAITANT (Auftragsverarbeiter) au sens de l'Art. 4(8) et Art. 28 DSGVO.
   Le Data Processing Agreement (DPA) Microsoft Online Services constitue l'AVV
   au sens de l'Art. 28 DSGVO. Ce DPA est accepte par l'organisation lors de la
   souscription aux services Microsoft 365.
   Microsoft heberge les donnees dans le tenant de l'organisation.
   L'EU Data Boundary Microsoft garantit la residence des donnees en Europe
   (voir section 9).
```

### 2.2 Consequence pratique

L'organisation deployant outplacement-tracker est seule responsable de traitement.
Elle assume integralement :

- la tenue du registre des activites de traitement (Art. 30 DSGVO)
- l'information des participants avant leur entree dans la solution (Art. 13 DSGVO)
- la reponse aux demandes d'exercice de droits des participants (Art. 15-22 DSGVO)
- la mise en oeuvre des mesures de securite appropriees (Art. 32 DSGVO)
- la notification d'une violation de donnees a l'autorite de controle (Art. 33 DSGVO),
  en Allemagne le Bundesbeauftragter fuer den Datenschutz und die Informationsfreiheit
  (BfDI) ou l'autorite de Land competente selon le siege de l'organisation

L'auteur du projet ne signe aucun AVV, n'est pas notifie en cas de violation,
et ne peut pas etre tenu responsable d'un incident survenu dans le tenant client.

---

## 3. Donnees personnelles traitees

La solution traite exclusivement des donnees personnelles ordinaires au sens de l'Art. 4(1) DSGVO.
Aucune categorie speciale de donnees au sens de l'Art. 9 DSGVO n'est collectee
(pas de donnees de sante, d'origine raciale ou ethnique, d'opinions politiques, etc.).

### 3.1 Liste "Participants"

| Champ | Type | Obligatoire | Finalite | Base legale |
|---|---|---|---|---|
| nom | Texte | Oui | Identification du participant, generation du PDF | Art. 6(1)(b) DSGVO |
| prenom | Texte | Oui | Identification du participant, generation du PDF | Art. 6(1)(b) DSGVO |
| email | Texte | Oui | Envoi de l'invitation mensuelle automatique | Art. 6(1)(b) DSGVO |
| langue | Choix (DE/EN) | Oui | Adaptation linguistique des communications | Art. 6(1)(b) DSGVO |
| id_conseillere | Email M365 | Oui | Routage du PDF vers la conseillere concernee | Art. 6(1)(b) DSGVO |
| date_debut_parcours | Date | Oui | Calcul de la duree du parcours, page de garde PDF | Art. 6(1)(b) DSGVO |
| date_prochain_rdv | Date | Oui | Declenchement automatique de l'invitation J-5 | Art. 6(1)(b) DSGVO |
| statut | Choix | Oui | Filtrage des participants actifs dans les Flows | Art. 6(1)(b) DSGVO |

Note : le champ "Title" de la liste (format "Prenom Nom") est genere automatiquement
par Power Automate. Il contient des donnees personnelles et est soumis aux memes
regles de conservation que les autres champs.

### 3.2 Liste "Profils"

| Champ | Type | Obligatoire | Finalite | Base legale |
|---|---|---|---|---|
| id_participant | Entier | Oui | Cle etrangere vers Participants | Art. 6(1)(b) DSGVO |
| plan_a | Texte long | Non | Plan de carriere principal - documente par la conseillere | Art. 6(1)(b) DSGVO |
| plan_b | Texte long | Non | Plan de carriere alternatif - documente par la conseillere | Art. 6(1)(b) DSGVO |
| marketingplan | Texte long | Non | Strategie de recherche d'emploi - documente par la conseillere | Art. 6(1)(b) DSGVO |
| zielmarkt | Texte long | Non | Secteur(s) cible(s) - documente par la conseillere | Art. 6(1)(b) DSGVO |
| date_creation | Date/heure | Oui | Tracabilite technique | Art. 6(1)(b) DSGVO |
| date_modification | Date/heure | Non | Tracabilite technique | Art. 6(1)(b) DSGVO |

Note : les quatre champs de contenu (plan_a, plan_b, marketingplan, zielmarkt) sont
optionnels. Leur remplissage est laisse a l'appreciation de la conseillere et du participant.
Ils peuvent contenir des informations sensibles sur les projets professionnels du participant.

### 3.3 Liste "BilansMensuels"

| Champ | Type | Obligatoire | Finalite | Base legale |
|---|---|---|---|---|
| id_participant | Entier | Oui | Cle etrangere vers Participants | Art. 6(1)(b) DSGVO |
| date_rdv | Date | Oui | Date du RDV mensuel correspondant | Art. 6(1)(b) DSGVO |
| date_soumission | Date/heure | Oui | Horodatage de la soumission du formulaire | Art. 6(1)(b) DSGVO |
| bilan_general | Texte long | Oui | Bilan libre redige par le participant | Art. 6(1)(b) DSGVO |
| statut_objectifs | Choix | Non | Auto-evaluation du participant sur ses objectifs | Art. 6(1)(b) DSGVO |
| statut_objectifs_detail | Texte long | Non | Precisions sur le statut des objectifs | Art. 6(1)(b) DSGVO |
| was_lief_gut | Texte long | Non | Ce qui a bien fonctionne (declaratif libre) | Art. 6(1)(b) DSGVO |
| wo_brauche_ich_unterstuetzung | Texte long | Non | Besoins de soutien (declaratif libre) | Art. 6(1)(b) DSGVO |
| themen_naechster_termin | Texte long | Non | Themes proposes pour le prochain RDV | Art. 6(1)(b) DSGVO |
| sonstige_anmerkungen | Texte long | Non | Remarques libres | Art. 6(1)(b) DSGVO |

Note : sur les 10 champs de cette liste, 7 sont optionnels. Le participant decide
lui-meme de ce qu'il souhaite partager. La solution ne contient aucun mecanisme de
tracking de candidatures individuelles, aucune liste de contacts employeurs, aucun
scoring ou classement de participants.

### 3.4 Fichiers PDF generes

Chaque execution du Flow 2 (Generation PDF) produit un fichier PDF stocke dans la
bibliotheque de documents SharePoint "TransferMappes". Ce fichier :

- contient les donnees personnelles des trois listes ci-dessus
- est nomme selon le format : TransferMappe_{Prenom}_{Nom}_{YYYY-MM-DD}.pdf
- est envoye par email a la conseillere assignee (champ id_conseillere)
- reste stocke dans le tenant de l'organisation et ne quitte pas celui-ci

Le fichier PDF est un document personnel au sens du RGPD. Il est soumis aux memes
durees de conservation que les donnees source.

### 3.5 Journaux Power Automate

Les Flows Power Automate genererent des journaux d'execution (run history) accessibles
dans le portail make.powerautomate.com. Ces journaux peuvent contenir :

- des noms et adresses email de participants (utilises comme parametres des actions)
- des codes d'erreur et messages techniques

Ces journaux sont conserves par Microsoft selon les parametres de la licence M365 de
l'organisation (generalement 28 jours pour E3). Ils ne sont pas exportes par la solution
et ne quittent pas le tenant.

---

## 4. Base legale du traitement

### 4.1 Base legale principale : execution d'un contrat (Art. 6(1)(b) DSGVO)

Le traitement est necessaire a l'execution du contrat de transfert entre la
Transfergesellschaft et le participant, dans le cadre defini par le paragraphe 111 SGB III
(Sozialgesetzbuch Drittes Buch - Arbeitsfoerderung).

Le suivi mensuel (bilans, profil de carriere, dates de rendez-vous) constitue la
substance meme de la prestation d'accompagnement a laquelle le participant a consenti
en integrant la Transfergesellschaft.

### 4.2 Interet legitime complementaire (Art. 6(1)(f) DSGVO)

La generation automatique de documents de suivi (PDF cumulatif, Zielvereinbarungen)
repond egalement a un interet legitime de l'organisation : disposer d'un suivi
documentaire conforme aux exigences de l'Agentur fuer Arbeit en cas de controle.
Cet interet ne prive pas le participant de droits disproportionnes compte tenu du
caractere strictement professionnel et finalise des donnees collectees.

### 4.3 Absence de consentement comme base legale

La solution ne repose pas sur le consentement (Art. 6(1)(a) DSGVO) comme base legale
principale. Le consentement ne serait pas adapte dans ce contexte car il creerait
une asymetrie de pouvoir entre l'organisation et le participant (relation de dependance).
L'organisation ne doit pas recueillir un "consentement" au sens du RGPD pour l'utilisation
de cette solution : la base legale contractuelle (Art. 6(1)(b)) est suffisante et plus robuste.

---

## 5. Conservation et suppression des donnees

### 5.1 Durees de conservation recommandees

| Donnee | Duree recommandee | Point de depart | Justification |
|---|---|---|---|
| Donnees Participants (liste) | 12 mois apres fin du parcours | Date statut "termine" | Fin du cadre contractuel SGB III |
| Profils (liste) | 12 mois apres fin du parcours | Date statut "termine" | Idem |
| BilansMensuels (liste) | 12 mois apres fin du parcours | Date statut "termine" | Idem |
| PDFs generes (SharePoint) | 3 ans apres fin du parcours | Date statut "termine" | Documentation Agentur fuer Arbeit |
| Journaux Power Automate | 28 jours (Microsoft) | Date d'execution | Automatique selon M365 |

Note : la duree de 3 ans pour les PDFs correspond a la prescription generalement
admise pour les litiges contractuels en droit allemand (§ 195 BGB). L'organisation
doit adapter ces durees en fonction de ses propres obligations legales, notamment
les eventuelles exigences de l'Agentur fuer Arbeit pour les preuves de suivi.

### 5.2 Procedure de suppression

La solution ne comporte pas de suppression automatique des donnees. L'organisation
est responsable de mettre en place une procedure adaptee.

**Option 1 - Suppression manuelle** :

Lorsqu'un participant termine son parcours (statut passe a "termine"), l'administrateur :

1. Supprime l'enregistrement dans la liste "Participants" apres la duree de conservation
2. Supprime l'enregistrement correspondant dans "Profils" (filtrer par id_participant)
3. Supprime les enregistrements correspondants dans "BilansMensuels" (filtrer par id_participant)
4. Supprime ou archive le dossier PDF dans la bibliotheque "TransferMappes"

**Option 2 - Suppression semi-automatisee (recommandee)** :

Creer un Flow Power Automate planifie hebdomadaire qui :

1. Recupere tous les enregistrements Participants dont le statut est "termine"
   et dont la date de fin depasse la duree de conservation configuree
2. Supprime les enregistrements associes dans les trois listes
3. Envoie un rapport de suppression a l'administrateur

Ce Flow complementaire n'est pas fourni dans le kit v0.1. Son developpement est
prevu dans le BACKLOG.md pour une version ulterieure.

**Option 3 - Politique de retention SharePoint** :

Microsoft 365 propose des politiques de retention configurables via le Centre de
conformite Microsoft Purview. L'organisation peut configurer une politique de retention
sur le site SharePoint TransferMappe avec suppression automatique apres la duree choisie.
Cette option ne necessite pas de developpement supplementaire mais requiert une licence
Microsoft 365 incluant Microsoft Purview (disponible en E3).

### 5.3 Droit a l'effacement (Art. 17 DSGVO)

En cas de demande d'effacement d'un participant, la procedure manuelle (Option 1) est
utilisee immediatement, sans attendre l'echeance de conservation. Voir section 6.

---

## 6. Droits des personnes concernees

Les participants disposent des droits suivants en vertu des Art. 15 a 22 DSGVO.
L'organisation est seule responsable de leur mise en oeuvre.

### 6.1 Droit d'acces (Art. 15 DSGVO - Auskunftsrecht)

Le participant peut demander une copie de toutes ses donnees. L'administrateur :

1. Exporte l'enregistrement depuis la liste "Participants" (export CSV depuis SharePoint)
2. Exporte l'enregistrement depuis la liste "Profils"
3. Exporte tous les enregistrements depuis "BilansMensuels" correspondant a son id_participant
4. Fournit le ou les PDFs generes disponibles dans la bibliotheque "TransferMappes"

### 6.2 Droit de rectification (Art. 16 DSGVO - Berichtigungsrecht)

L'administrateur ou la conseillere peuvent modifier directement les enregistrements
dans les listes SharePoint. La versioning est activee sur les trois listes (parametre
"versioning: true" dans le schema), ce qui permet de conserver l'historique des modifications.

### 6.3 Droit a l'effacement (Art. 17 DSGVO - Recht auf Loeschung)

Appliquer la procedure de suppression manuelle decrite en section 5.2 (Option 1).
Conserver une trace de la demande et de l'action effectuee pour demontrer la conformite.

Note : le droit a l'effacement peut etre limite si l'organisation doit conserver
des preuves de suivi pour l'Agentur fuer Arbeit. Dans ce cas, l'organisation doit
informer le participant du motif de refus partiel (Art. 17(3) DSGVO).

### 6.4 Droit a la limitation du traitement (Art. 18 DSGVO - Einschraenkungsrecht)

L'administrateur passe le statut du participant a "suspendu" dans la liste "Participants".
Le Flow d'invitation et le Flow de generation PDF excluent automatiquement les participants
dont le statut n'est pas "actif". Aucune nouvelle donnee n'est donc generee.

### 6.5 Droit a la portabilite (Art. 20 DSGVO - Datenuebertragbarkeit)

Les listes SharePoint permettent l'export en CSV via l'interface standard.
Les PDFs generes sont directement portables. L'organisation peut fournir
l'ensemble des donnees dans ces formats standards a la demande du participant.

### 6.6 Droit d'opposition (Art. 21 DSGVO - Widerspruchsrecht)

Dans le contexte SGB III, le droit d'opposition est limite compte tenu de la base
legale contractuelle (Art. 6(1)(b)). L'organisation doit consulter son DPD
pour determiner les cas ou l'opposition est recevable.

### 6.7 Canal de reception des demandes

L'organisation doit definir et communiquer aux participants un canal de reception
des demandes (email DPD, formulaire en ligne, courrier). Ce canal doit figurer
dans l'information vie privee fournie aux participants (voir section 11).

---

## 7. Mesures techniques et organisationnelles (TOM)

### 7.1 Mesures integrees a la solution

Les mesures suivantes sont implementees par construction dans outplacement-tracker :

| Mesure | Implementation | Niveau |
|---|---|---|
| Residence des donnees dans le tenant | Aucune donnee ne sort du tenant M365 - pas d'API externe, pas de connecteur tiers | Integre par architecture |
| Minimisation des donnees | 7 des 10 champs BilansMensuels sont optionnels - pas de tracking de candidatures | Integre par conception |
| Separation des donnees par organisation | Un tenant = une organisation - pas de mutualisation possible par construction | Integre par architecture |
| Versioning SharePoint | Historique de toutes les modifications sur les trois listes | Active dans le schema |
| Acces base sur les roles SharePoint | Les listes sont hebergees dans un site SharePoint dont les permissions sont configurables | A configurer (voir 7.2) |
| Aucune PII dans les emails d'invitation | L'email participant ne contient que prenom, nom, date RDV et lien Forms - pas d'historique en clair | Integre dans les templates |
| Journaux d'execution Power Automate | Chaque execution est tracee dans l'historique Power Automate du tenant | Natif M365 |

### 7.2 Mesures que l'organisation doit mettre en place

Ces mesures sont de la responsabilite de l'organisation deployant la solution.

**Mesures obligatoires avant mise en production :**

| Mesure | Action requise | Reference |
|---|---|---|
| Authentification multi-facteurs (MFA) | Activer l'MFA pour tous les comptes ayant acces au site SharePoint TransferMappe | Microsoft Entra ID - Politique d'acces conditionnel |
| Permissions SharePoint restrictives | Le site TransferMappe doit etre en acces prive - membres uniquement : conseillers et administrateurs | Administration SharePoint - droits par groupe |
| Shared mailbox expeditrice | Creer une boite partagee (ex. transfer@domaine.de) - ne pas utiliser l'adresse personnelle d'un employe | Exchange Online - Administration |
| DLP (Data Loss Prevention) | Configurer une politique DLP empechant le partage externe des listes SharePoint contenant des PII | Microsoft Purview - Politiques DLP |
| Acces au portail Power Automate | Restreindre l'acces au portail Power Automate aux administrateurs designes | Microsoft Entra ID - Roles |
| Information des participants (Art. 13) | Remettre une notice d'information vie privee a chaque participant avant son entree dans la solution | Obligation legale DSGVO |

**Mesures fortement recommandees :**

| Mesure | Action requise | Reference |
|---|---|---|
| Revue periodique des acces | Auditer trimestriellement les membres du groupe SharePoint TransferMappe | Administration M365 - Revues d'acces |
| Audit Log M365 | Activer et conserver les journaux d'audit M365 (SharePoint, Exchange, Power Automate) | Microsoft Purview - Audit |
| Sauvegarde SharePoint | Activer la sauvegarde Microsoft 365 Backup ou une solution tierce certifiee | Microsoft 365 Backup |
| Formation des conseillers | Former les utilisateurs aux bonnes pratiques de traitement des donnees dans SharePoint | Interne |
| Politique de mot de passe | Appliquer une politique de mot de passe conforme aux recommandations BSI (minimum 12 caracteres) | Microsoft Entra ID |

---

## 8. Sous-traitants (Auftragsverarbeiter)

### 8.1 Microsoft Corporation

Microsoft est le seul sous-traitant dans le cadre de cette solution.

| Element | Detail |
|---|---|
| Denomination | Microsoft Corporation |
| Role DSGVO | Sous-traitant (Auftragsverarbeiter) - Art. 4(8) et Art. 28 DSGVO |
| Base de l'AVV | Data Processing Agreement (DPA) Microsoft Online Services, accepte lors de la souscription M365 |
| Prestations concernees | SharePoint Online, Power Automate, Microsoft Forms, Exchange Online, Word Online |
| Acces aux donnees | Microsoft n'accede pas au contenu des donnees sauf instruction de l'organisation ou obligation legale |
| Certifications | ISO 27001, ISO 27018, SOC 1/2/3, certifications specifiques au secteur disponibles |

L'organisation n'a pas a signer d'AVV supplementaire avec Microsoft : le DPA Microsoft
Online Services est accepte lors de la souscription M365 et couvre l'ensemble des
services utilises par cette solution.

Le DPA Microsoft Online Services est disponible a l'adresse :
https://www.microsoft.com/en-us/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA

### 8.2 Aucun autre sous-traitant

outplacement-tracker n'utilise :

- aucune API externe tierce (analytics, monitoring, IA, traduction, etc.)
- aucun connecteur Power Automate Premium impliquant un service tiers
- aucune infrastructure d'hebergement distincte du tenant M365 de l'organisation
- aucun service de l'auteur du projet

Toute evolution de la solution introduisant un nouveau service tiers devra faire
l'objet d'une evaluation DPIA (Art. 35 DSGVO) si les donnees traitees sont concernees.

---

## 9. Transferts de donnees hors Union europeenne

### 9.1 Residence des donnees Microsoft 365

Par defaut, les tenants Microsoft 365 dont la region est configuree en Europe stockent
les donnees au repos (data at rest) dans les datacenters europeens de Microsoft
(principalement Pays-Bas et Irlande, avec centres secondaires en Finlande et Autriche).

Microsoft a deploye l'EU Data Boundary, qui garantit que les donnees de la majorite
des services M365 (dont SharePoint, Exchange, Power Automate) restent en Europe y compris
pour les operations et les diagnostics. Ce perimetre s'applique aux licences M365 E3
avec region configuree sur l'Union europeenne lors de la creation du tenant.

Pour verifier la region du tenant : portail d'administration M365 > Parametres > Profil
de l'organisation > Pays ou region des donnees.

### 9.2 Absence de transfert par la solution

outplacement-tracker ne procede a aucun transfert de donnees en dehors du tenant
Microsoft 365 de l'organisation. La solution ne contacte aucun service externe.

### 9.3 En cas de doute sur la residence des donnees

Si l'organisation ne peut pas confirmer que son tenant est configure en region UE,
elle doit le verifier et le corriger avant le deploiement. En l'absence de garantie
sur la residence, un transfert hors UE pourrait avoir lieu sans base legale adequat
(Art. 44-49 DSGVO), ce qui constituerait une violation.

---

## 10. Designation d'un DPD (Datenschutzbeauftragter)

### 10.1 Obligation probable pour les Transfergesellschaften

L'Art. 37 DSGVO impose la designation d'un DPD dans plusieurs cas, dont :

- lorsque le traitement est effectue par un organisme public (Art. 37(1)(a))
- lorsque le traitement implique un suivi regulier et systematique de personnes
  a grande echelle (Art. 37(1)(b))

Une Transfergesellschaft gerant 1 500 a 2 000 participants simultanement effectue
vraisemblablement un traitement a grande echelle impliquant un suivi regulier des personnes.
La designation d'un DPD est donc tres probablement obligatoire.

Le complement national allemand (§ 38 BDSG) impose egalement la designation d'un DPD
lorsque l'organisme emploie au moins 20 personnes s'occupant en permanence du traitement
automatise de donnees personnelles.

### 10.2 Role du DPD dans le deploiement de cette solution

Le DPD de l'organisation doit etre associe :

- a la mise a jour du Verzeichnis der Verarbeitungstatigkeiten (voir section 11)
- a la redaction de l'information vie privee destinee aux participants (Art. 13 DSGVO)
- a l'evaluation de la necessite d'une DPIA (Art. 35 DSGVO)
- aux revues periodiques d'acces et de securite

---

## 11. Checklist de mise en conformite avant deploiement

L'organisation doit effectuer les actions suivantes avant la mise en production de la solution.

### 11.1 Actions obligatoires

- [ ] Verifier que la region du tenant M365 est configuree sur l'Union europeenne
- [ ] Configurer les permissions SharePoint du site TransferMappe en acces prive
      (groupe membres : conseillers et administrateurs uniquement)
- [ ] Activer l'MFA pour tous les comptes ayant acces au site SharePoint TransferMappe
- [ ] Creer la shared mailbox expeditrice (ex. transfer@domaine.de) et supprimer
      toute adresse personnelle des variables des Flows
- [ ] Mettre a jour le Verzeichnis der Verarbeitungstatigkeiten de l'organisation
      (Art. 30 DSGVO) en ajoutant cette activite de traitement
- [ ] Rediger et remettre une notice d'information vie privee aux participants
      avant leur entree dans la solution (Art. 13 DSGVO), indiquant notamment :
      les categories de donnees collectees, les finalites, la base legale,
      la duree de conservation, les droits et le contact DPD
- [ ] Definir et documenter la procedure de suppression des donnees en fin de parcours
- [ ] Associer le DPD de l'organisation a la mise en oeuvre

### 11.2 Actions recommandees

- [ ] Evaluer la necessite d'une DPIA (Datenschutz-Folgenabschatzung, Art. 35 DSGVO)
      au regard du volume de participants et de la nature du suivi
- [ ] Configurer une politique DLP dans Microsoft Purview pour le site SharePoint TransferMappe
- [ ] Activer les journaux d'audit M365 et les conserver selon la politique interne
- [ ] Planifier une revue des acces SharePoint au moins une fois par an
- [ ] Documenter la procedure de reponse aux demandes d'exercice de droits (delai 1 mois, Art. 12(3) DSGVO)
- [ ] Former les conseillers aux bonnes pratiques : pas de copie de donnees participants
      sur des postes personnels, pas de partage par email non securise, etc.

### 11.3 Adaptation du contenu

- [ ] Remplacer les valeurs de configuration des Flows (varSiteUrl, varSharedMailbox, etc.)
      par les valeurs reelles de l'organisation avant activation
- [ ] Adapter les templates email (logo, nom de l'organisation, coordonnees de contact)
- [ ] Adapter le template Word PDF (logo, identite visuelle) si different de 10 k Beratung

---

## 12. Minimisation des donnees : principes de conception

La solution a ete concue dans le respect du principe de minimisation des donnees
(Art. 5(1)(c) DSGVO - Datensparsamkeit). Les choix de conception suivants en temoignent :

**Formulaire mensuel (Microsoft Forms) :**

- 6 champs au total, dont 5 optionnels
- Le participant decide librement de ce qu'il souhaite partager
- Aucun champ de suivi de candidatures individuelles
- Aucun champ de contacts employeurs
- Aucun mecanisme de scoring ou d'evaluation des participants

**Listes SharePoint :**

- Aucune donnee financiere (salaire, indemnite, montant des allocations)
- Aucune donnee de sante ou medicale
- Aucune donnee sur les raisons du licenciement (relation employeur d'origine)
- Aucune photo, document d'identite ou donnee biometrique

**Emails automatiques :**

- L'email d'invitation ne contient que le prenom, nom, date du RDV et le lien Forms
- L'email a la conseillere contient le PDF en piece jointe mais pas d'historique
  de donnees en clair dans le corps du message
- Aucune adresse email personnelle de l'auteur du projet n'apparait dans les templates

**PDF genere :**

- Le PDF contient uniquement les donnees saisies dans les formulaires
- Il ne contient pas de metadonnees personnelles cachees (les metadonnees Word sont
  a verifier lors de la construction du template .docx)
- Il n'est transmis qu'a la conseillere concernee, pas a l'ensemble de l'equipe

**Droit de regard du participant :**

- Le participant saisit lui-meme ses bilans mensuels via Microsoft Forms
- Il peut contacter sa conseillere pour obtenir une copie de ses donnees
- Il peut exercer son droit de rectification en informant sa conseillere ou l'administrateur

---

## 13. Historique des revisions

| Version | Date | Modifications |
|---|---|---|
| 1.0 | 2026-05-05 | Creation initiale |
