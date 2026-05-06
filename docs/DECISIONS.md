# DECISIONS.md

Architecture Decision Records (ADR) for the `outplacement-tracker` project.

Each structural decision is recorded here in the following format:

- **Context**: why the question arises
- **Alternatives**: options considered
- **Decision**: the chosen approach
- **Consequences**: what follows from it

Any modification to an existing ADR requires a new ADR with status "Supersedes".

---

## ADR-001: Technical Stack Selection

**Status**: Accepted
**Date**: 2026-05-05

### Context

Several stacks were viable for delivering automated monthly tracking with cumulative PDF generation:

- Microsoft 365 (Forms + SharePoint + Power Automate)
- Google Workspace (Forms + Sheets + Apps Script)
- Self-hosted solution (n8n + PostgreSQL)
- Custom Node.js solution on a VPS

### Alternatives Evaluated

| Stack | Cost | DSGVO | Maintenance | Fit for German context |
|---|---|---|---|---|
| Microsoft 365 | 0 (already licensed) | Native | Near zero | Very strong |
| Google Workspace | 0 if already in place | Adequate | Low | Moderate |
| Self-hosted | ~30 EUR/month | Must be managed (AVV required) | High | Weak |
| Custom Node.js | Variable | Must be managed | High | Weak |

### Decision

**Microsoft 365** is selected as the sole stack.

### Consequences

- The solution integrates into the ecosystem already deployed by the majority of German Transfergesellschaften.
- No external dependencies: everything remains within the client tenant.
- DSGVO compliance is satisfied by construction.
- The project author bears no responsibility for hosting or support.
- The client can extend the solution using its own IT teams.
- Compatible with the standard E3 plan, without premium connectors.

---

## ADR-002: Signatures on Zielvereinbarungen

**Status**: Accepted
**Date**: 2026-05-05

### Context

Zielvereinbarungen between a Teilnehmer and a Beraterin carry near-contractual weight under the framework of Paragraph 111 SGB III. The Agentur fuer Arbeit may request evidence of these documents during an audit. They are currently signed manually by both parties.

### Alternatives Evaluated

1. **eIDAS-compliant electronic signature** (DocuSign, Adobe Sign, Microsoft eSign)
2. **Simple electronic signature** within Power Automate (text fields)
3. **Preserved handwritten signature**: the generated PDF includes blank signature fields, is printed, signed physically by both parties, scanned, and stored in SharePoint if the organisation chooses to do so

### Decision

**Option 3**: preserved handwritten signature.

The cumulative PDF includes blank signature fields at the bottom of each Zielvereinbarung. The document is printed at the appointment, signed by both parties, scanned, and uploaded to SharePoint at the client's discretion.

### Consequences

- No premium licence required (no DocuSign, no paid Microsoft eSign).
- Legal compliance preserved: handwritten signatures are legally sufficient for this document type.
- Minimal burden at the appointment: printing and scanning are already routine in any organisation.
- The client retains the option to switch to eSign in v0.2 if desired.
- Added to `BACKLOG.md`: optional eSign module for v0.2 and later.

---

## ADR-003: Monthly Reporting Approach

**Status**: Accepted
**Date**: 2026-05-05

### Context

Several approaches to monthly reporting were considered, ranging from detailed tracking of every application and contact to a free-form declarative summary.

The original Transfer Mappe explicitly states that the document belongs to the Teilnehmer and is a tool in their service, not a surveillance instrument.

### Alternatives Evaluated

1. **Mandatory continuous entry**: the Teilnehmer logs each application and each contact in real time via three separate forms.
2. **Detailed structured monthly form**: 15 to 20 mandatory fields covering all dimensions.
3. **Free-form declarative monthly review**: 6 fields, only one mandatory; the Teilnehmer decides what to share.

### Decision

**Option 3**: free-form declarative monthly review.

Six fields in the monthly form (general summary, objective status, what went well, support needed, topics for the next appointment, other remarks). Only the general summary is mandatory. All other fields are optional.

### Consequences

- Simplified technical architecture: one SharePoint list for reviews instead of four lists for detailed tracking.
- Faster deployment.
- Stronger DSGVO compliance through data minimisation.
- Respect for the human dimension of the Teilnehmer-Beraterin relationship.
- The Beraterin retains responsibility for guiding, not monitoring.
- Added to `BACKLOG.md`: optional opt-in personal tracker module for v0.2.

---

## ADR-004: Maximum Programme Duration

**Status**: Accepted
**Date**: 2026-05-05

### Context

The cumulative PDF stacks monthly reviews in chronological order. The Word template must account for the maximum number of monthly sections to be generated.

### Decision

**12 months** maximum, consistent with the German legal framework (Paragraph 111 SGB III caps the duration of a Transfergesellschaft at 12 months).

### Consequences

- The Word template includes up to 12 monthly sections, statically embedded in the .docx file (one section per possible month). Power Automate injects an empty string for months without a review. Note: "Repeating Section" Content Controls that would allow a dynamic loop are not supported by the Power Automate "Populate a Microsoft Word template" action.
- If an organisation handles longer cases (rare), adding sections to the template is sufficient.
- No technical limit on the Power Automate or SharePoint side: volume is well within platform capacity.

---

## ADR-005: Replacement of Binary .docx Files with Construction Specs in Sprint 1

**Status**: Accepted
**Date**: 2026-05-05

### Context

The Sprint 1 deliverable included two .docx files with Word Content Controls (`transfer_mappe_template_de.docx` and `transfer_mappe_template_en.docx`). A .docx file containing Word Content Controls is a binary Office Open XML format. It cannot be produced correctly by an agent without access to a Microsoft Word runtime or a specialised python-docx library.

### Alternatives Evaluated

1. Generate a minimal .docx via python-docx (without valid Content Controls) -- risk of breaking the Power Automate connector.
2. Deliver exhaustive Markdown specifications documenting the exact structure, and defer .docx construction to Sprint 2 within a real tenant.
3. Deliver an empty .docx without Content Controls as a placeholder.

### Decision

**Option 2**: construction specs in `.md` format are delivered in Sprint 1. The construction of the actual .docx files, with valid Content Controls, is a Sprint 2 task (prerequisite before Power Automate Flows can be tested).

### Consequences

- The specs `templates/word/transfer_mappe_template_de_spec.md` and `transfer_mappe_template_en_spec.md` document all 118 Content Controls exactly: their Tag values, XML structure, and step-by-step Word construction instructions.
- Construction of each .docx is estimated at 30 minutes for a competent M365 administrator.
- No loss of deliverable quality: the specs are more usable than malformed .docx files.
- Sprint 2 begins with the construction and validation of the .docx files in a Developer Program tenant.

---

## ADR-006: Sprint 2 Delivery in Blueprint Mode Without a Microsoft 365 Tenant

**Status**: Accepted
**Date**: 2026-05-05

### Context

No Microsoft 365 Developer Program tenant was available during Sprint 2. Options explored (Visual Studio Dev Essentials, Business Basic trial) did not materialise within the sprint timeframe.

### Alternatives Evaluated

1. Block the sprint until a tenant is obtained (indefinite delay).
2. Produce manually simulated JSON exports (risk of undetected errors; Power Automate JSON is difficult to review without a graphical interface).
3. Deliver a "blueprint": detailed implementation guides in Markdown, plus assets that can be constructed and validated locally.

### Decision

**Option 3**: delivery in blueprint mode.

Power Automate Flows and Microsoft Forms are not exported as JSON but documented as implementation guides -- Markdown documents precise enough for an M365 administrator to reconstruct Flows and Forms from scratch, action by action.

Word templates are built via a Python script (python-docx) and validated locally (118 Content Controls verified by assertion). Sample PDFs are generated locally via LibreOffice headless.

### Consequences

- The kit is fully deliverable without a tenant.
- Deployment on a real tenant takes 1 to 2 hours instead of 30 minutes (had the JSON been directly importable).
- Implementation guides are independently verifiable: each Power Automate action is documented with its exact parameters and expressions.
- The Sprint 2 "done" criterion is adjusted to: "implementation guides validated and internally consistent", rather than "end-to-end tests in a Dev tenant".
- If a tenant becomes available after delivery, the guides can be implemented and then exported as JSON for a future v0.1.1.
- No loss of domain quality: the reference specs (`sharepoint_schema.md`, `word_template_structure.md`, `forms_questions_*.md`, `email_templates.md`) remain the source of truth, and the blueprint guides are derived directly from them.

---

## ADR-007: Language Policy by Document

**Status**: Accepted -- partially superseded by ADR-008 (governance documents)
**Date**: 2026-05-06

### Context

Project documents had been produced without an explicit language policy. The result was an inconsistent mix: PITCH.pdf partly in French despite targeting German decision-makers; README.md in French despite targeting international GitHub visitors; INSTALLATION.md in French despite targeting an M365 administrator in Germany.

Language policy must be derived from the intended audience of each document, not from the author's drafting preference.

### Decision

Each document is written in the language of its target audience.

| Document | Target audience | Language |
|---|---|---|
| README.md | GitHub visitors (international) | English |
| CHANGELOG.md | Developers (international) | English |
| docs/ARCHITECTURE.md | IT architects and decision-makers (international) | English |
| docs/INSTALLATION.md | Client M365 administrator (Germany) | Deutsch |
| docs/FAQ.md | Client advisors and IT team (Germany) | Deutsch |
| docs/PRIVACY.md | Client DPO and legal department (Germany) | Deutsch |
| docs/PITCH.pdf | Decision-makers at the outplacement firm (Germany) | Deutsch |
| SCOPE.md, SPRINTS.md, BACKLOG.md, ASSUMPTIONS.md, DECISIONS.md, docs/SECURITY_REVIEWS.md | Author (internal use) | French (unchanged) |
| .claude/agents/* | Author (internal use) | French (unchanged) |

### Consequences

- German documents use correct umlauts and domain vocabulary (Transfergesellschaft, Zielvereinbarung, Beraterin, Teilnehmer, Bericht).
- English documents use sober professional British English, without marketing language.
- Internal documents (author use) remain in French, unchanged.
- Technical specs in `specs/` and implementation guides in `power_automate/` and `forms/` are outside the scope of this decision: their target audience is the author and their language is discretionary.
- ADR-007 applies retroactively: non-compliant existing documents are rewritten.

---

## ADR-008: Final Language Policy

**Status**: Accepted -- supersedes ADR-007 on governance document language
**Date**: 2026-05-06

### Context

ADR-007 classified governance documents (SCOPE, SPRINTS, BACKLOG, ASSUMPTIONS, DECISIONS, SECURITY_REVIEWS) as internal-author documents and kept them in French. This is inconsistent for an open-source repository: GitHub visitors cannot read French by default, and the target market (Germany) does not speak French either. Public governance documents belong to the repository audience, not the author.

### Decision

All public governance documents move to English. Only client-facing documents remain in German.

| Document | Audience | Language |
|---|---|---|
| README.md | GitHub visitors (international) | English |
| CHANGELOG.md | International developers | English |
| SCOPE.md | Project governance | English |
| SPRINTS.md | Project governance | English |
| BACKLOG.md | Project governance | English |
| docs/ARCHITECTURE.md | Technical reviewers (international) | English |
| docs/ASSUMPTIONS.md | Project governance | English |
| docs/DECISIONS.md | Project governance | English |
| docs/SECURITY_REVIEWS.md | Project governance | English |
| docs/INSTALLATION.md | M365 admin of the client | Deutsch |
| docs/FAQ.md | Client advisors and IT | Deutsch |
| docs/PRIVACY.md | Client DPO / legal | Deutsch |
| docs/PITCH.pdf | Decision-makers at 10 k Beratung | Deutsch |
| .claude/agents/* | Internal (gitignored, private) | French |

### Consequences

- All governance documents are rewritten in British English (not translated literally: clean reformulation).
- German domain vocabulary is preserved as-is throughout (Transfergesellschaft, Zielvereinbarung, etc.).
- Client-facing documents (INSTALLATION.md, FAQ.md, PRIVACY.md, PITCH.pdf) remain in German unchanged.
- Internal Claude agent definitions remain in French (gitignored).
- ADR-007 is partially superseded on the governance document category. Its decisions on client-facing (German) and public-technical (English) documents remain valid.

---

## ADR-009: Language Policy Extended to All Repository Files

**Status**: Accepted -- extends ADR-008 to all tracked files
**Date**: 2026-05-06

### Context

ADR-008 established the language policy for governance documents and client-facing documents. It did not cover implementation artefacts: Power Automate guides, Forms construction guides, SharePoint schema, Word template specs, scripts, and sample files. These files were still in French (the original working language of the author), which is inconsistent with a public repository targeting German-speaking organisations.

### Decision

Language policy is extended to all tracked repository files. The target language for each file type is derived from its intended audience.

| File type / path | Audience | Language |
|---|---|---|
| power_automate/*.md | M365 admin of the client | Deutsch |
| forms/*.md | M365 admin of the client | Deutsch |
| sharepoint/setup_lists.ps1 (comments) | M365 admin of the client | Deutsch |
| specs/sharepoint_schema.md | M365 admin / technical reviewer | Deutsch |
| specs/word_template_structure.md | M365 admin / technical reviewer | Deutsch |
| specs/forms_questions_de.md (meta-text) | M365 admin | Deutsch |
| templates/word/*_de_spec.md | M365 admin | Deutsch |
| specs/email_templates.md (preamble and meta-labels) | M365 admin (bilingual reference) | English (neutral -- file covers both DE and EN templates) |
| specs/forms_questions_en.md | M365 admin | English (already compliant) |
| templates/word/*_en_spec.md | M365 admin | English |
| samples/build_samples.py (comments) | Developer | English |
| samples/README.md | Developer / GitHub visitor | English |

### Exceptions

- specs/forms_questions_en.md: no modification needed, already in English.
- specs/email_templates.md: preamble and meta-labels in English (neutral), because the file contains both DE and EN templates. Using German meta-text would artificially favour the DE half.
- Technical identifiers are not translatable regardless of file language: SharePoint column names, Content Control tag values, Power Automate variable names, and action names used inside expressions remain in their original form. Power Automate action names that used French words (Pour_chaque_participant, etc.) are renamed to German equivalents consistently across all guide files.

### Consequences

- All public files in the repository are now in the language of their target audience.
- No French text remains in any tracked file (except internal .claude/agents/* which are gitignored).
- ADR-009 applies retroactively: all non-compliant files are rewritten as part of this patch.
