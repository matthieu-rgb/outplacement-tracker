# BACKLOG.md

Idees et fonctionnalites en dehors du scope v0.1. Ne PAS implementer dans la v0.1.

Toute proposition d'ajout en cours de sprint atterrit ici, pas dans le code. Le Tech Lead arbitre.

---

## v0.2 envisage

### Tracker personnel optionnel de candidatures

Module **opt-in** pour les participants qui souhaitent saisir au fil de l'eau leurs candidatures et contacts. Strictement volontaire et reserve a un usage personnel du participant. Les donnees ne sont visibles ni de la conseillere ni de la direction de la societe de reclassement.

Justification : certains participants apprecient un outil de tracking pour eux-memes. La v0.1 n'en propose pas pour eviter le piege de la surveillance, mais une version opt-in respecte le choix individuel.

### Reporting agrege pour la conseillere

Tableau de bord SharePoint listant les participants suivis avec :

- Date du prochain RDV
- Statut du dernier bilan recu (rempli / non rempli / en retard)
- Tendance qualitative sur les 3 derniers mois

Pas de donnees individuelles agregees a usage analytique. Vue operationnelle uniquement.

### Signature electronique conforme eIDAS

Integration DocuSign, Adobe Sign ou Microsoft eSign pour les Zielvereinbarungen. Demande une licence premium et engage la conformite eIDAS. Hors-scope v0.1 par sobriete.

---

## v0.3+ envisage

### Module Qualifikationen und Zeugnisse

Espace SharePoint structure pour le depot et la classification des certificats, diplomes et attestations du participant. Recherche, tagging, export.

### Note de frais (Rechnung an die Transfer GmbH)

Forms separe pour les demandes de remboursement de frais (transport, formation, equipement). Validation par la conseillere. Export comptable mensuel.

### Application mobile dediee

App Microsoft Power Apps ou Teams App permettant au participant de remplir son bilan mensuel depuis son telephone, avec rappels push.

### Integration Teams pour les RDV

Lien Teams Meeting genere automatiquement avec chaque RDV mensuel. Notification J-1, rappel le jour J.

### Multi-tenancy et personnalisation par societe

Pour les regroupements de Transfergesellschaften ou les holdings. Pas pertinent en v0.1.

---

## Idees ecartees definitivement

### Saisie obligatoire de chaque candidature et contact

Rejetee. Voir `docs/DECISIONS.md` ADR-003. Incompatible avec l'esprit de la Transfer Mappe et la confiance participant-conseillere.

### Hebergement par l'auteur sur un VPS personnel

Rejetee. Voir conversation initiale du projet. Incompatible avec la position de "don a la communaute" et engagement DSGVO disproportionne pour l'auteur.

### Mecanisme de relance automatique en cas de non-remplissage

Rejetee. Le participant choisit de remplir ou non. Pas de pression, pas de relance, pas de notification "vous n'avez pas rempli". La responsabilite du suivi reste a la conseillere.

### Score de "performance" du participant

Rejetee categoriquement. La Transfer Mappe n'est pas un outil d'evaluation et l'outplacement n'est pas une competition.
