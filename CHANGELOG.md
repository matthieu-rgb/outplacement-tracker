# Changelog

All notable changes to this project are documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [0.1.0] - 2026-05-05

Initial release. Covers all deliverables from Sprints 1, 2 and 3.

### Added

**Business specifications (Sprint 1)**

- `specs/sharepoint_schema.md` : complete schema for the 3 SharePoint lists (Participants, Profils,
  BilansMensuels) - columns, types, default values
- `specs/forms_questions_de.md` : exact questions for the onboarding and monthly review forms
  in German
- `specs/forms_questions_en.md` : 1:1 English version of the forms
- `specs/email_templates.md` : 4 email templates (J-5 invitation DE/EN, Beraterin notification
  day-of DE/EN)
- `specs/word_template_structure.md` : structure of the Word template with the list of 118 Content
  Controls and their Tag values

**Word templates (Sprint 2)**

- `templates/word/transfer_mappe_template_de.docx` : DE Word template with 118 Content Controls
- `templates/word/transfer_mappe_template_en.docx` : EN Word template with 118 Content Controls
- `templates/word/build_templates.py` : Python build script for the templates (python-docx,
  118 Content Controls validated by assertion)

**Integration kit (Sprint 2)**

- `sharepoint/lists_schema.json` : declarative schema for the 3 SharePoint lists
- `sharepoint/setup_lists.ps1` : idempotent PnP PowerShell script for SharePoint provisioning
- `forms/forms_construction_guide.md` : step-by-step guide for creating the 4 Microsoft Forms
- `power_automate/Flow_1_Invitation_J-5.md` : implementation guide for the J-5 invitation Flow
- `power_automate/Flow_2_Generation_PDF.md` : implementation guide for the PDF generation Flow
- `power_automate/IMPORT_GUIDE.md` : global deployment guide in 7 steps

**Samples (Sprint 2)**

- `samples/sample_pdf_output_de.pdf` : cumulative PDF DE - Max Mustermann - 3 fictional months
- `samples/sample_pdf_output_en.pdf` : cumulative PDF EN - John Doe - 3 fictional months
- `samples/build_samples.py` : Python script to generate samples via headless LibreOffice

**Documentation (Sprint 3)**

- `docs/INSTALLATION.md` : step-by-step deployment guide for the M365 administrator
- `docs/ARCHITECTURE.md` : technical architecture description and rationale for design decisions
- `docs/PRIVACY.md` : DSGVO/BDSG note - data collected, legal bases, retention,
  responsibility model
- `docs/FAQ.md` : answers to frequently asked questions - Beraterinnen and IT team
- `docs/ASSUMPTIONS.md` : project business assumptions (A1 to A8)
- `docs/DECISIONS.md` : Architecture Decision Records ADR-001 to ADR-006
- `docs/PITCH.pdf` : solution presentation document for decision-makers (6-8 pages)
- `docs/SECURITY_REVIEWS.md` : append-only log of security and DSGVO compliance reviews

### Notes

**Blueprint mode (ADR-006)**

The Power Automate Flows and Microsoft Forms are delivered as Markdown implementation guides
rather than importable JSON exports. The reason: no Microsoft 365 Developer Program tenant
was available during Sprint 2. The guides are sufficiently detailed (action by action,
exact expressions) to allow an M365 administrator to rebuild the Flows and Forms from scratch.
Estimated duration: 2 to 4 hours.

If a tenant becomes available, the guides can be implemented and the Flows exported as JSON
for a future release v0.1.1.

**Handwritten signatures (ADR-002)**

The cumulative PDF contains empty signature fields at the bottom of each Zielvereinbarung.
The physical signature workflow is preserved: print at the appointment, handwritten signature
by both parties, optional scan and archival in SharePoint. No electronic signature licence
is required. A migration to eSign is documented in `BACKLOG.md` for v0.2.

[0.1.0]: https://github.com/matthieu-rgb/outplacement-tracker/releases/tag/v0.1.0
