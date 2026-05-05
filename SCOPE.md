# SCOPE.md

Document de reference pour le perimetre du projet `outplacement-tracker` v0.1.

**Tout ce qui n'est pas dans ce document est OUT.**

Toute proposition d'evolution ou d'idee qui sort de ce perimetre va dans `BACKLOG.md`, jamais dans le code de la v0.1.

---

## 1. Objectif du projet

Livrer un **kit installable** permettant a une societe de reclassement allemande (Transfergesellschaft) de digitaliser le suivi mensuel de ses participants, en s'appuyant exclusivement sur Microsoft 365.

Le kit est publie en open source sur GitHub. La societe de reclassement decide librement de l'utiliser ou non. L'auteur ne fournit ni service d'hebergement ni support technique apres livraison.

## 2. Utilisateurs cibles

- **Le participant** : personne suivie en Transfergesellschaft. Recoit un mail mensuel, remplit un formulaire en 5 minutes.
- **La conseillere (Beraterin)** : recoit un PDF cumulatif le matin du rendez-vous mensuel. N'a aucun outil specifique a installer.
- **L'administrateur Microsoft 365 du client** : deploie le kit en suivant la documentation.

## 3. Fonctionnalites IN scope

### 3.1 Onboarding du participant (optionnel)

Formulaire Microsoft Forms (versions DE et EN) permettant au participant de saisir, s'il le souhaite, un profil de carriere comprenant :

- Berufliche Zielsetzung (Plan A / Plan B)
- Marketingplan (positionnement, competences cles)
- Zielmarkt (region, branche, taille d'entreprise)

Ce formulaire est rempli **une fois** au debut du parcours et reste modifiable. Il n'est pas obligatoire.

### 3.2 Bilan mensuel

Formulaire Microsoft Forms court (versions DE et EN) envoye automatiquement par mail au participant **5 jours avant chaque rendez-vous**. Six champs, un seul obligatoire :

1. Bilan general du mois (texte libre, **obligatoire**)
2. Statut des objectifs precedents (choix : vollstaendig erreicht / teilweise erreicht / nicht erreicht / noch nicht relevant + texte libre)
3. Was lief gut (texte libre, optionnel)
4. Wo brauche ich Unterstuetzung (texte libre, optionnel)
5. Themen fuer den naechsten Termin (texte libre, optionnel)
6. Sonstige Anmerkungen (texte libre, optionnel)

Le participant decide de ce qu'il partage.

### 3.3 Generation du PDF cumulatif

Power Automate Flow declenche **le matin du jour du RDV** :

- Recupere les donnees du participant (profil + tous les bilans mensuels precedents)
- Remplit un template Word avec content controls
- Convertit en PDF via l'action native Power Automate
- Envoie le PDF par mail a la conseillere
- Sauvegarde une copie dans SharePoint dans le dossier du participant

Le PDF empile les bilans mensuels dans l'ordre chronologique. Il contient des emplacements de signature vides pour la Zielvereinbarung (signatures preservees en mode manuscrit, voir `DECISIONS.md` ADR-002).

### 3.4 Bilingue DE/EN

L'ensemble de la solution est disponible en **deux versions distinctes** :

- Microsoft Forms DE et Forms EN (2 formulaires d'onboarding, 2 formulaires de bilan)
- Templates d'email DE et EN (invitation J-5 et notification conseillere J)
- Templates Word de PDF cumulatif DE et EN

Le choix de la langue est determine par un champ `Sprache` de la liste SharePoint Participants.

### 3.5 Livrables documentaires

- `README.md` (pitch GitHub)
- `docs/PITCH.pdf` (pitch decisionnel pour 10 k Beratung et equivalents)
- `docs/INSTALLATION.md` (guide pas-a-pas pour l'administrateur M365)
- `docs/ARCHITECTURE.md` (justification technique des choix)
- `docs/PRIVACY.md` (note RGPD/DSGVO, modele de responsabilite)
- `docs/FAQ.md`

## 4. Fonctionnalites OUT scope (vont dans BACKLOG.md)

- Saisie continue des candidatures et contacts (rejetee, voir `DECISIONS.md` ADR-003)
- Signature electronique conforme eIDAS
- Reporting agrege multi-participants pour la conseillere ou la direction
- Numerisation de la section "Qualifikationen und Zeugnisse"
- Note de frais (Rechnung an die Transfer GmbH)
- Notifications push, application mobile, integration Teams
- Versioning ou historisation des modifications du profil
- Gestion multi-conseilleres avec affectation dynamique
- Tracker personnel optionnel de candidatures (envisage pour v0.2)

## 5. Contraintes techniques

- Compatible plan Microsoft 365 E3 standard (pas de Power Automate Premium, pas de Dataverse, pas d'AI Builder)
- Donnees hebergees dans le tenant du client uniquement
- Compatible avec un tenant **EU Data Boundary** Microsoft 365
- Volume cible : jusqu'a 2 000 participants suivis simultanement, soit ~100 envois par jour ouvre

## 6. Hypotheses retenues

Voir `docs/ASSUMPTIONS.md` pour le detail. En synthese :

- Duree maximale d'un parcours : 12 mois (§ 111 SGB III)
- Signatures sur Zielvereinbarung : preservees en mode manuscrit
- Suivi mensuel : declaratif libre, pas de tracking d'activites detaillees

## 7. Criteres de "done"

La v0.1 est consideree comme livree lorsque :

- [ ] Le repo GitHub contient l'integralite des fichiers listes dans la section 3.5
- [ ] Le PDF de pitch est genere et integre dans `docs/`
- [ ] La solution a ete testee de bout en bout dans un tenant Microsoft 365 Developer Program
- [ ] Au moins 5 sample PDFs de sortie sont disponibles dans `samples/`
- [ ] Un Loom ou GIF de demonstration est integre au README ou au pitch
- [ ] Le tag `v0.1.0` est cree sur le repo GitHub
- [ ] Le `CHANGELOG.md` mentionne la release initiale

## 8. Engagement de l'auteur

- L'auteur ne fournit aucun service d'hebergement
- L'auteur ne fournit aucun support technique apres livraison
- L'auteur ne traite aucune donnee personnelle de participants
- L'auteur ne signe aucun AVV (Auftragsverarbeitungsvertrag)
- Toute utilisation est sous la responsabilite du deployeur final

Ce projet est un **don a la communaute**, pas une prestation.
