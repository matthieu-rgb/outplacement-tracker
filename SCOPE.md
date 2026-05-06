# SCOPE.md

Reference document for the scope of the `outplacement-tracker` v0.1 project.

**Everything not listed in this document is OUT.**

Any proposed change or feature outside this scope goes into `BACKLOG.md`, never into v0.1 code.

---

## 1. Project objective

Deliver an installable kit that enables a German Transfergesellschaft to digitalise the monthly monitoring of its Teilnehmer, using Microsoft 365 exclusively.

The kit is published as open source on GitHub. The Transfergesellschaft decides freely whether to use it. The author provides neither hosting nor technical support after delivery.

## 2. Target users

- **The Teilnehmer**: the person enrolled in the Transfergesellschaft. Receives a monthly email and fills in a form in approximately five minutes.
- **The Beraterin**: receives a cumulative PDF on the morning of the monthly appointment. No specific tooling to install.
- **The client's Microsoft 365 administrator**: deploys the kit by following the documentation.

## 3. Features IN scope

### 3.1 Teilnehmer onboarding (optional)

A Microsoft Forms form (DE and EN versions) allowing the Teilnehmer to enter, if they wish, a career profile comprising:

- Berufliche Zielsetzung (Plan A / Plan B)
- Marketingplan (positioning, key competencies)
- Zielmarkt (region, sector, company size)

The Teilnehmer completes this form **once** at the start of the programme; it remains editable. It is not mandatory.

### 3.2 Monthly review

A short Microsoft Forms form (DE and EN versions) sent automatically by email to the Teilnehmer **5 days before each appointment**. Six fields, one mandatory:

1. General review of the month (free text, **mandatory**)
2. Status of previous objectives (choice: vollstaendig erreicht / teilweise erreicht / nicht erreicht / noch nicht relevant + free text)
3. Was lief gut (free text, optional)
4. Wo brauche ich Unterstuetzung (free text, optional)
5. Themen fuer den naechsten Termin (free text, optional)
6. Sonstige Anmerkungen (free text, optional)

The Teilnehmer decides what they share.

### 3.3 Cumulative PDF generation

A Power Automate Flow triggered **on the morning of the appointment day**:

- Retrieves the Teilnehmer data (profile + all previous monthly reviews)
- Populates a Word template using content controls
- Converts to PDF via the native Power Automate action
- Sends the PDF by email to the Beraterin
- Saves a copy in SharePoint in the Teilnehmer's folder

The PDF stacks monthly reviews in chronological order. It contains blank signature slots for the Zielvereinbarung (signatures retained in handwritten form, see `DECISIONS.md` ADR-002).

### 3.4 Bilingual DE/EN

The entire solution is available in **two distinct versions**:

- Microsoft Forms DE and Forms EN (2 onboarding forms, 2 monthly review forms)
- Email templates DE and EN (J-5 invitation and Beraterin notification J)
- Cumulative PDF Word templates DE and EN

The language is determined by a `Sprache` field in the SharePoint Participants list.

### 3.5 Documentary deliverables

- `README.md` (GitHub pitch)
- `docs/PITCH.pdf` (decision-making pitch for 10 k Beratung and equivalent organisations)
- `docs/INSTALLATION.md` (step-by-step guide for the M365 administrator)
- `docs/ARCHITECTURE.md` (technical justification of design choices)
- `docs/PRIVACY.md` (DSGVO/BDSG note, responsibility model)
- `docs/FAQ.md`

## 4. Features OUT scope (go into BACKLOG.md)

- Continuous entry of applications and contacts (rejected, see `DECISIONS.md` ADR-003)
- eIDAS-compliant electronic signature
- Aggregated multi-Teilnehmer reporting for the Beraterin or management
- Digitalisation of the "Qualifikationen und Zeugnisse" section
- Expense claims (Rechnung an die Transfer GmbH)
- Push notifications, mobile application, Teams integration
- Versioning or change history for the profile
- Multi-Berater management with dynamic assignment
- Optional personal application tracker (considered for v0.2)

## 5. Technical constraints

- Compatible with a standard Microsoft 365 E3 plan (no Power Automate Premium, no Dataverse, no AI Builder)
- Data hosted exclusively in the client's tenant
- Compatible with a Microsoft 365 **EU Data Boundary** tenant
- Target volume: up to 2,000 Teilnehmer tracked simultaneously, approximately 100 sends per working day

## 6. Retained assumptions

See `docs/ASSUMPTIONS.md` for detail. In summary:

- Maximum programme duration: 12 months (SS 111 SGB III)
- Signatures on Zielvereinbarungen: retained in handwritten form
- Monthly monitoring: voluntary and declarative, no detailed activity tracking

## 7. Done criteria

v0.1 is considered delivered when:

- [ ] The GitHub repository contains all files listed in section 3.5
- [ ] The pitch PDF is generated and integrated into `docs/`
- [ ] The solution implementation guides (Flows, Forms) are valid and consistent with the SharePoint and Word specifications (ADR-006: adjusted criterion, Dev tenant test deferred post-delivery)
- [ ] At least 5 sample output PDFs are available in `samples/`
- [ ] A Loom or GIF demonstration is integrated into the README or the pitch
- [ ] The tag `v0.1.0` is created on the GitHub repository
- [ ] `CHANGELOG.md` mentions the initial release

## 8. Author commitments

- The author provides no hosting service
- The author provides no technical support after delivery
- The author processes no personal data belonging to Teilnehmer
- The author signs no Auftragsverarbeitungsvertrag
- All use is the sole responsibility of the final deploying organisation

This project is a **contribution to the community**, not a commercial service.
