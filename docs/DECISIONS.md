# DECISIONS.md

Architecture Decision Records (ADR) du projet `outplacement-tracker`.

Chaque decision structurante du projet est enregistree ici au format suivant :

- **Contexte** : pourquoi se pose la question
- **Alternatives** : options envisagees
- **Decision** : choix retenu
- **Consequences** : ce qui en decoule

Toute modification d'un ADR doit faire l'objet d'un nouvel ADR (statut "Supersede").

---

## ADR-001 : Choix de la stack technique

**Statut** : Accepte
**Date** : 2026-05-05

### Contexte

Plusieurs stacks sont envisageables pour delivrer un suivi mensuel automatise avec generation de PDF cumulatif :

- Microsoft 365 (Forms + SharePoint + Power Automate)
- Google Workspace (Forms + Sheets + Apps Script)
- n8n self-hosted avec PostgreSQL et Tally
- Solution custom Node.js sur VPS

### Alternatives evaluees

| Stack | Cout | DSGVO | Maintenance | Adapte au contexte allemand |
|---|---|---|---|---|
| Microsoft 365 | 0 (deja paye) | Native | Quasi nulle | Tres fort |
| Google Workspace | 0 si deja en place | OK | Faible | Moyen |
| n8n self-hosted | ~30 EUR/mois | A gerer (AVV requis) | Forte | Faible (souverainete moins evidente) |
| Custom Node.js | Variable | A gerer | Forte | Faible |

### Decision

**Microsoft 365** est retenu comme stack unique.

### Consequences

- La solution s'integre dans l'ecosysteme deja deploye chez la majorite des Transfergesellschaften allemandes
- Aucune dependance externe (tout reste dans le tenant client)
- Conformite DSGVO acquise par construction
- L'auteur du projet n'a aucune responsabilite d'hebergement ou de support
- Le client peut faire evoluer la solution avec ses propres equipes IT
- Compatible plan E3 standard, sans connecteur premium

---

## ADR-002 : Signatures sur Zielvereinbarungen

**Statut** : Accepte
**Date** : 2026-05-05

### Contexte

Les Zielvereinbarungen entre participant et conseillere sont des documents avec valeur quasi-contractuelle, lies au cadre du § 111 SGB III. Leur tracabilite peut etre demandee par l'Agentur fuer Arbeit en cas de controle. Ils sont actuellement signes manuellement par les deux parties.

### Alternatives evaluees

1. **Signature electronique conforme eIDAS** (DocuSign, Adobe Sign, Microsoft eSign)
2. **Signature electronique simple** dans Power Automate (champs texte)
3. **Signature manuscrite preservee** : PDF genere avec emplacements vides, imprime, signe, scanne

### Decision

**Option 3** : signature manuscrite preservee.

Le PDF cumulatif contient des emplacements de signature vides en bas de chaque Zielvereinbarung. Le document est imprime au RDV, signe physiquement par les deux parties, scanne et reverse dans SharePoint si la societe le souhaite.

### Consequences

- Aucune licence premium requise (pas de DocuSign, pas de Microsoft eSign payant)
- Conformite legale preservee (signatures manuscrites legalement suffisantes pour ce type de document)
- Charge minimale au RDV (impression et scan, deja maitrises par toute societe)
- Latitude pour la societe de basculer vers eSign en v0.2 si elle le souhaite
- Ajoute dans `BACKLOG.md` : module eSign optionnel pour v0.2+

---

## ADR-003 : Approche du suivi mensuel

**Statut** : Accepte
**Date** : 2026-05-05

### Contexte

Plusieurs approches du suivi mensuel ont ete envisagees, depuis le tracking detaille de chaque candidature et contact jusqu'au bilan declaratif libre.

La Transfer Mappe d'origine (10 k Beratung GmbH, version 2026 V1) precise explicitement en page 2 que le document appartient au participant et est un outil a son service, pas un outil de surveillance.

### Alternatives evaluees

1. **Saisie continue obligatoire** : le participant saisit chaque candidature et chaque contact au fil de l'eau via 3 formulaires distincts
2. **Formulaire mensuel structure detaille** : 15 a 20 champs obligatoires couvrant toutes les dimensions
3. **Bilan mensuel declaratif libre** : 6 champs, 1 seul obligatoire, le participant decide de ce qu'il partage

### Decision

**Option 3** : bilan mensuel declaratif libre.

Six champs dans le formulaire mensuel (bilan general, statut des objectifs, ce qui a bien marche, soutien necessaire, themes pour le RDV, autres remarques). Seul le bilan general est obligatoire. Tous les autres sont optionnels.

### Consequences

- Architecture technique simplifiee (une seule liste SharePoint pour les bilans, au lieu de quatre listes pour le tracking detaille)
- Mise en place plus rapide
- Conformite RGPD/DSGVO renforcee (minimisation des donnees collectees)
- Respect de la dimension humaine de la relation participant-conseillere
- La conseillere garde sa responsabilite d'orienter, pas de controler
- Ajoute dans `BACKLOG.md` : module tracker personnel optionnel et opt-in pour v0.2

---

## ADR-004 : Duree maximale du parcours

**Statut** : Accepte
**Date** : 2026-05-05

### Contexte

Le PDF cumulatif empile les bilans mensuels chronologiquement. Le template Word doit dimensionner le nombre de sections mensuelles a empiler.

### Decision

**12 mois** maximum, conforme au cadre legal allemand (§ 111 SGB III qui plafonne la duree d'une Transfergesellschaft a 12 mois).

### Consequences

- Le template Word inclut jusqu'a 12 sections mensuelles avec un mecanisme de boucle Power Automate
- Si une societe gere des cas plus longs (rare), il suffit d'ajouter des sections au template
- Pas de limite technique cote Power Automate ou SharePoint (volume largement compatible)

---

## ADR-005 : Organisation projet en sub-agents

**Statut** : Accepte
**Date** : 2026-05-05

### Contexte

Le projet implique plusieurs domaines d'expertise (Microsoft 365, securite, redaction, design). Une approche generaliste avec un seul agent Claude Code risque de produire un livrable moyen sur tout sans exceller nulle part.

### Decision

Le projet utilise une architecture en **6 sub-agents specialises** (Tech Lead, M365 Expert, Software Architect, Security/DSGVO, Technical Writer, Design/Frontend).

Chaque agent est defini dans `.claude/agents/`. Le Tech Lead orchestre les autres et arbitre.

### Consequences

- Travail cloisonne par domaine, qualite plus elevee
- Reviews croisees obligatoires (au moins 2 reviewers par livrable critique)
- Discipline projet renforcee : SCOPE, BACKLOG, DECISIONS, SPRINTS sont les fichiers sacres
- Effort initial de mise en place plus eleve, mais retombees fortes en qualite et en reproductibilite
