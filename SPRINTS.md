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

**Objectif** : produire le kit d'integration complet (implementation guides, scripts, templates, samples).
Livraison en mode blueprint sans tenant (ADR-006) : les Flows et Forms sont documentes
en implementation guides Markdown au lieu d'exports JSON.

**Livrables**

- [x] `templates/word/transfer_mappe_template_de.docx` : template Word DE avec 118 Content Controls
- [x] `templates/word/transfer_mappe_template_en.docx` : template Word EN avec 118 Content Controls
- [x] `templates/word/build_templates.py` : script de generation des templates
- [x] `sharepoint/lists_schema.json` : schema declaratif des 3 listes SharePoint
- [x] `sharepoint/setup_lists.ps1` : script PowerShell PnP idempotent
- [x] `forms/forms_construction_guide.md` : guide pas-a-pas pour creer les 4 formulaires
- [x] `power_automate/Flow_1_Invitation_J-5.md` : implementation guide du Flow J-5
- [x] `power_automate/Flow_2_Generation_PDF.md` : implementation guide du Flow PDF
- [x] `power_automate/IMPORT_GUIDE.md` : guide global de mise en place (7 etapes)
- [x] `samples/sample_pdf_output_de.pdf` : PDF cumulatif DE - Max Mustermann - 3 mois fictifs
- [x] `samples/sample_pdf_output_en.pdf` : PDF cumulatif EN - John Doe - 3 mois fictifs
- [x] `samples/build_samples.py` : script Python de generation des samples
- [x] `docs/DECISIONS.md` : ADR-006 (livraison blueprint sans tenant)

**Note ADR-006** : livraison en mode blueprint. Les Flows Power Automate et Microsoft Forms
sont documentes en implementation guides Markdown au lieu d'exports JSON importables.
Decision justifiee par l'absence de tenant Dev disponible dans le delai du sprint.
Deploiement reel par l'admin M365 du client en suivant les guides : 2 a 4 heures.

**Domaines mobilises**

- Microsoft 365 : implementation guides Flows et Forms, script PnP
- Architecture : coherence inter-listes, Tag values, expressions Power Automate
- Securite et DSGVO : donnees fictives anonymisees, pas de PII dans les guides

**Definition of done (ajustee par ADR-006)**

- Implementation guides valides et coherents avec les specs SharePoint et Word
- Scripts Python executes et valides (118 Content Controls par template, PDFs generes)
- Aucun email personnel ni PII reel dans les guides ou les samples
- Commit `feat: sprint 2 - integration kit (templates, scripts, implementation guides)`

---

## Sprint 3 : Documentation et livrables decisionnels

**Objectif** : produire les documents de presentation et de mise en place, finaliser la release v0.1.0.

**Livrables**

- [x] `docs/INSTALLATION.md` : guide pas-a-pas avec screenshots pour l'administrateur M365
- [x] `docs/ARCHITECTURE.md` : justification des choix techniques
- [x] `docs/PRIVACY.md` : note DSGVO/BDSG, modele de responsabilite, donnees collectees, retention
- [x] `docs/FAQ.md` : reponses aux questions previsibles cote conseillere et cote IT
- [x] `docs/PITCH.pdf` : 6 a 8 pages, pitch decisionnel pour la societe de reclassement
- [ ] `docs/images/` : screenshots, schema d'architecture, demo gif si possible (non livre en v0.1.0 - reporte BACKLOG v0.2)
- [x] `CHANGELOG.md` : entree v0.1.0
- [x] Tag git `v0.1.0`

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
