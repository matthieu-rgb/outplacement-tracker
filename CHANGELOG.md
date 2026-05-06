# Changelog

Toutes les modifications notables de ce projet sont documentees dans ce fichier.

Format : [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versionnage : [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [0.1.0] - 2026-05-05

Release initiale. Couvre l'ensemble des livrables des Sprints 1, 2 et 3.

### Added

**Specifications metier (Sprint 1)**

- `specs/sharepoint_schema.md` : schema complet des 3 listes SharePoint (Participants, Profils,
  BilansMensuels) - colonnes, types, valeurs par defaut
- `specs/forms_questions_de.md` : questions exactes des formulaires onboarding et bilan mensuel
  en allemand
- `specs/forms_questions_en.md` : version anglaise 1:1 des formulaires
- `specs/email_templates.md` : 4 templates d'email (invitation J-5 DE/EN, notification
  conseillere jour J DE/EN)
- `specs/word_template_structure.md` : structure du template Word avec liste des 118 Content
  Controls et leurs Tag values

**Templates Word (Sprint 2)**

- `templates/word/transfer_mappe_template_de.docx` : template Word DE avec 118 Content Controls
- `templates/word/transfer_mappe_template_en.docx` : template Word EN avec 118 Content Controls
- `templates/word/build_templates.py` : script Python de construction des templates (python-docx,
  118 Content Controls valides par assertion)

**Kit d'integration (Sprint 2)**

- `sharepoint/lists_schema.json` : schema declaratif des 3 listes SharePoint
- `sharepoint/setup_lists.ps1` : script PowerShell PnP idempotent de provisioning SharePoint
- `forms/forms_construction_guide.md` : guide pas-a-pas pour la creation des 4 formulaires
  Microsoft Forms
- `power_automate/Flow_1_Invitation_J-5.md` : implementation guide du Flow d'invitation J-5
- `power_automate/Flow_2_Generation_PDF.md` : implementation guide du Flow de generation PDF
- `power_automate/IMPORT_GUIDE.md` : guide global de deploiement en 7 etapes

**Echantillons (Sprint 2)**

- `samples/sample_pdf_output_de.pdf` : PDF cumulatif DE - Max Mustermann - 3 mois fictifs
- `samples/sample_pdf_output_en.pdf` : PDF cumulatif EN - John Doe - 3 mois fictifs
- `samples/build_samples.py` : script Python de generation des samples via LibreOffice headless

**Documentation (Sprint 3)**

- `docs/INSTALLATION.md` : guide de deploiement pas-a-pas pour l'administrateur M365
- `docs/ARCHITECTURE.md` : description de l'architecture technique et justification des choix
- `docs/PRIVACY.md` : note DSGVO/BDSG - donnees collectees, bases juridiques, retention,
  modele de responsabilite
- `docs/FAQ.md` : reponses aux questions frequentes - conseillers et equipe IT
- `docs/ASSUMPTIONS.md` : hypotheses metier du projet (A1 a A8)
- `docs/DECISIONS.md` : Architecture Decision Records ADR-001 a ADR-006
- `docs/PITCH.pdf` : document de presentation de la solution pour les decideurs (6-8 pages)
- `docs/SECURITY_REVIEWS.md` : journal append-only des revues de securite et conformite DSGVO

### Notes

**Mode blueprint (ADR-006)**

Les Flows Power Automate et les formulaires Microsoft Forms sont livres sous forme
d'implementation guides Markdown et non comme des exports JSON importables. La raison :
aucun tenant Microsoft 365 Developer Program n'etait disponible pendant le Sprint 2.
Les guides sont suffisamment detailles (action par action, expressions exactes) pour
permettre a un administrateur M365 de reconstruire les Flows et Forms a partir de zero.
Duree estimee : 2 a 4 heures.

Si un tenant devient disponible, les guides peuvent etre implementes puis les Flows
exportes en JSON pour une future release v0.1.1.

**Signatures manuscrites (ADR-002)**

Le PDF cumulatif contient des emplacements de signature vides en bas de chaque
Zielvereinbarung. Le workflow de signature physique est preserve : impression au RDV,
signature manuscrite par les deux parties, scan et archivage optionnel dans SharePoint.
Aucune licence de signature electronique n'est requise. Une evolution vers eSign est
documentee dans `BACKLOG.md` pour la v0.2.

[0.1.0]: https://github.com/matthieu-rgb/outplacement-tracker/releases/tag/v0.1.0
