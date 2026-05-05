# SPRINTS.md

Plan de travail decoupe en 3 sprints. Chaque sprint produit des livrables concrets et testables.

---

## Sprint 1 : Fondations metier

**Objectif** : produire l'ensemble des specifications metier et des assets de base, prets a etre consommes par les sprints suivants.

**Livrables**

- [x] `specs/sharepoint_schema.md` : schema complet des listes SharePoint (colonnes, types, valeurs par defaut)
- [x] `specs/forms_questions_de.md` : questions exactes du Forms onboarding et bilan mensuel en allemand
- [x] `specs/forms_questions_en.md` : version anglaise 1:1
- [x] `specs/email_templates.md` : 4 templates d'email (invitation J-5 DE/EN, notification conseillere J DE/EN)
- [x] `specs/word_template_structure.md` : structure du template Word avec liste des content controls et leurs Tag values
- [x] `templates/word/transfer_mappe_template_de_spec.md` : spec de construction du template Word DE (voir note ci-dessous)
- [x] `templates/word/transfer_mappe_template_en_spec.md` : spec de construction du template Word EN (voir note ci-dessous)

**Domaines mobilises**

- Architecture : structure des donnees, coherence inter-listes
- Microsoft 365 : faisabilite Forms, content controls Word compatibles Power Automate
- Redaction : questions et emails, registre de langue allemand metier
- Securite et DSGVO : revue des donnees collectees (minimisation, pas de PII inutile)

**Note sur les templates Word** : les fichiers .docx binaires ne peuvent pas etre generes par un agent sans runtime Word. A la place, des specs de construction detaillees ont ete produites (`*_spec.md`). Ces specs documentent exactement les Content Controls, Tag values, styles et structure XML necessaires pour construire le .docx manuellement dans Word en 30 minutes. La construction des .docx reels est une tache Sprint 2 (test en tenant Dev).

**Definition of done**

- Tous les fichiers `specs/` valides techniquement
- Templates Word ouvrables sans erreur dans Word et compatibles avec l'action "Populate a Microsoft Word template" de Power Automate
- Aucun champ ne collecte de donnee personnelle non justifiee
- Commit `feat: sprint 1 - business specs and templates`

---

## Sprint 2 : Automatisation Power Platform

**Objectif** : produire les exports Power Automate, le script de provisioning SharePoint, et tester l'ensemble dans un tenant Microsoft 365 Developer Program.

**Livrables**

- [ ] `power_automate/Flow_1_Invitation_J-5.json` : export du Flow J-5 importable
- [ ] `power_automate/Flow_2_Generation_PDF.json` : export du Flow de generation PDF
- [ ] `power_automate/IMPORT_GUIDE.md` : procedure d'import dans Power Automate, variables a ajuster
- [ ] `sharepoint/lists_schema.json` : schema declaratif des listes
- [ ] `sharepoint/setup_lists.ps1` : script PowerShell PnP pour creer les listes en une commande
- [ ] `forms/form_onboarding_de.json` : structure du Forms onboarding DE (export ou specification d'import)
- [ ] `forms/form_onboarding_en.json`
- [ ] `forms/form_bilan_mensuel_de.json`
- [ ] `forms/form_bilan_mensuel_en.json`
- [ ] `samples/sample_pdf_output_de.pdf` : exemple de PDF cumulatif sur 3 mois fictifs
- [ ] `samples/sample_pdf_output_en.pdf` : version EN

**Domaines mobilises**

- Microsoft 365 : construction et export des Flows et Forms, script PnP
- Architecture : revue de l'enchainement des Flows et de la coherence des donnees
- Securite et DSGVO : audit des Flows (logs, gestion des erreurs, pas de fuite d'email)

**Definition of done**

- Solution testee en bout-en-bout dans un tenant Dev avec 3 participants fictifs et 3 mois de bilans
- Sample PDFs generes par le vrai systeme, pas a la main
- Aucun email personnel n'apparait dans les Flows, les emails ou la documentation
- Commit `feat: sprint 2 - power platform automation and tested samples`

---

## Sprint 3 : Documentation et livrables decisionnels

**Objectif** : produire les documents de presentation et de mise en place, finaliser la release v0.1.0.

**Livrables**

- [ ] `docs/INSTALLATION.md` : guide pas-a-pas avec screenshots pour l'administrateur M365
- [ ] `docs/ARCHITECTURE.md` : justification des choix techniques
- [ ] `docs/PRIVACY.md` : note DSGVO/BDSG, modele de responsabilite, donnees collectees, retention
- [ ] `docs/FAQ.md` : reponses aux questions previsibles cote conseillere et cote IT
- [ ] `docs/PITCH.pdf` : 6 a 8 pages, pitch decisionnel pour la societe de reclassement
- [ ] `docs/images/` : screenshots, schema d'architecture, demo gif si possible
- [ ] `CHANGELOG.md` : entree v0.1.0
- [ ] Tag git `v0.1.0`

**Domaines mobilises**

- Redaction : ensemble des documents
- Design : pitch PDF (HTML/CSS), schemas, mise en page
- Microsoft 365 : revue technique de INSTALLATION.md et ARCHITECTURE.md
- Securite et DSGVO : revue de PRIVACY.md

**Definition of done**

- Tous les documents sont valides techniquement
- PITCH.pdf est genere, ouvrable, conforme a l'identite visuelle definie
- Le repo est public, le tag v0.1.0 est pousse
- Le CHANGELOG est a jour
- Commit `chore: release v0.1.0`

---

## Regles de fonctionnement

1. **Pas de saut de sprint.** Le sprint N+1 ne demarre pas tant que le sprint N n'est pas en "done".
2. **Pas d'ajout de livrable en cours de sprint.** Toute idee va dans `BACKLOG.md`.
3. **Chaque livrable critique fait l'objet d'une review** dans son domaine.
4. **Tout retard ou blocage** est documente dans `docs/DECISIONS.md` (nouvel ADR si necessaire).
