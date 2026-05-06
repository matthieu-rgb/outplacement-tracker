# Technical architecture - outplacement-tracker v0.1

Reference document for a technical architect or IT decision-maker evaluating the solution.

---

## Overview

### Purpose of the solution

outplacement-tracker digitalises the monthly progress tracking of participants in a Transfergesellschaft (German outplacement company under §111 SGB III). The solution automates two processes:

1. **J-5** : sending a monthly review form to the participant five days before their appointment
2. **Day of appointment** : generating a cumulative PDF (Transfer Mappe) delivered to the Beraterin before the appointment

All data remains within the client's Microsoft 365 tenant. No third-party service is involved.

### Architecture diagram

```
PARTICIPANT                 CLIENT M365 TENANT                        BERATERIN
-----------                 --------------------------                ---------

                            SharePoint Online
                            +-----------------+
                            | Participants    |
                            | Profils         |
                            | BilansMensuels  |
                            | TransferMappes/ | (document library)
                            +-----------------+
                                    |
[Onboarding    ]  --response-->  Microsoft Forms
[form          ]               (Forms 1/2)
[DE or EN      ]               No associated Flow
                               Manual entry into SP

[Monthly review]  <--J-5 email--  Power Automate
[form          ]                  Flow 1 : J-5 Invitation
[DE or EN      ]                  Trigger: Scheduled 07:00
                                  - Reads Participants (status=active, date=J+5)
                                  - Sends email via shared mailbox
                                  - Link to Form 3 or Form 4
                  --response-->  Microsoft Forms
                               (Forms 3/4)
                               Entry into BilansMensuels
                                  |
                                  v
                               Power Automate
                               Flow 2 : PDF Generation
                               Trigger: Scheduled 06:00
                               - Reads Participants (status=active, date=J)
                               - Reads Profils (id_participant)
                               - Reads BilansMensuels (id_participant, ASC sort)
                               - Populates Word template (118 Content Controls)
                               - Converts Word -> PDF (native E3)
                               - Saves PDF to SharePoint
                               - Sends PDF by email          --PDF-->  [Beraterin]

M365 ADMIN
----------
PnP.PowerShell (one-time setup)
  -> Creates the 3 SharePoint lists
  -> Idempotent script, safe to re-run
```

### Data flow

```
Forms form
    |
    v (response stored in Forms)
    |--> Manual processing or Flow -> SharePoint list BilansMensuels or Profils

SharePoint Participants (source of truth)
    |
    +--> Flow 1 : reads date_prochain_rdv, sends email
    +--> Flow 2 : reads participant + profile + reviews, generates PDF

Generated PDF
    |
    +--> Outlook email (attachment) -> Beraterin
    +--> SharePoint file (archival) -> TransferMappes/{Nom_Prenom}/
```

---

## Components

### Microsoft Forms

**Role** : collects participant responses (onboarding and monthly reviews) via a URL link distributed by email or manually. No M365 account required for the respondent.

**Rationale** :
- Native M365 E3, no additional cost
- Responsive interface on mobile and desktop, no installation required
- The public sharing link allows access without an M365 account, covering participants who do not have one
- The "Microsoft Forms" connector in Power Automate reads responses directly

**Rejected alternatives** :

| Alternative | Reason for rejection |
|---|---|
| Custom web form (React, Vue) | Requires hosting, maintenance, authentication: outside the scope of an M365 kit |
| Typeform / Google Forms | Data outside the tenant, not DSGVO-compliant for a German employment context |
| PowerApps canvas app | Requires a PowerApps licence (not included in standard E3) |
| SharePoint list form | Interface poorly suited to participants (non-technical users), no simple public sharing link |

**Known limitations** :
- No complex conditional branching (acceptable: forms have at most 7 linear questions)
- No pre-population of previous responses (out of scope for v0.1)
- Limit of 200 questions per form and 50,000 responses per form (well above the target volume)

---

### SharePoint Online (lists)

**Role** : operational database for the solution. Three lists store participants, career profiles and monthly reviews. A document library stores generated PDFs and Word templates.

**Rationale** :
- Native M365 E3, natively integrated in Power Automate without a premium connector
- The SharePoint connector in Power Automate is standard and supports OData filters, sorting and pagination
- Native permission management (participants have no access to the site)
- Item versioning enabled (5 versions retained per item)
- Compatible with PnP.PowerShell for reproducible and idempotent provisioning

**Rejected alternatives** :

| Alternative | Reason for rejection |
|---|---|
| Excel Online (.xlsx file) | No transactions, concurrent write conflicts, no OData filter support in Power Automate |
| Dataverse | Requires a premium Power Platform licence (not included in standard E3) |
| Azure SQL / SQL Azure | Requires an Azure subscription, a premium connector, network management |
| Access (Access App) | Retired by Microsoft since 2018 |

**Known limitations** :
- SharePoint lists do not support true foreign keys with referential integrity constraints. The `id_participant` (Number) relationship in Profils and BilansMensuels is an application-level convention, not enforced by SharePoint.
- Standard SharePoint limit: 30 million items per list (no impact at the target volume of 2,000 participants x 12 reviews = 24,000 items)
- OData filtering on `DateTime` columns in DateOnly mode can produce unexpected behaviour depending on the tenant timezone (see troubleshooting in INSTALLATION.md)

---

### Power Automate (cloud Flows)

**Role** : orchestration of the two automated processes. Flow 1 (J-5 Invitation) sends invitation emails. Flow 2 (PDF Generation) produces and distributes the cumulative PDF.

**Rationale** :
- Included in M365 E3, no separate premium Power Automate licence
- The SharePoint, Office 365 Outlook and Word Online (Business) connectors are standard connectors available in E3
- The "Populate a Microsoft Word template" and "Convert to PDF" actions are available in the Word Online (Business) connector, included in E3
- Scheduled triggers are available in E3
- Graphical debugging interface (execution history, action-by-action detail)

**Rejected alternatives** :

| Alternative | Reason for rejection |
|---|---|
| Azure Logic Apps | Requires an Azure subscription, per-execution billing |
| n8n self-hosted | Requires a server, maintenance, outside the client's M365 ecosystem |
| Azure Functions (Node.js/Python) | Same Azure dependency, plus development complexity |
| Scheduled PowerShell scripts | No native error handling, no monitoring interface, fragile in production |
| Power Automate Desktop | Requires a premium Power Automate licence with a desktop agent |

**Known limitations** :
- Cloud Flows in E3 have a maximum execution duration of 30 days (no impact here)
- The "Apply to each" loop is sequential by default: for 100 participants, the PDF Flow can take 20 to 30 minutes. Concurrency can be enabled (see INSTALLATION.md)
- No JSON export of Flows without a tenant (ADR-006): Flows are documented as Markdown blueprints, not directly importable files in v0.1
- SharePoint "Get items" connector limit: 5,000 items per call. For the target volume (2,000 participants), set the threshold to 2,000 in the action or enable pagination

---

### Word templates with Content Controls

**Role** : document templates (.docx) containing 118 Plain Text Content Controls, each identified by a unique Tag value. Power Automate injects data from SharePoint lists into these Content Controls via the "Populate a Microsoft Word template" action, then converts the populated document to PDF.

**Rationale** :
- The "Populate a Microsoft Word template" action from the Word Online (Business) connector is available in E3 and supports Plain Text Content Controls with Tag values
- Content Controls allow a faithfully structured Word output (layout, fonts, logo) that cannot be reproduced with basic programmatic PDF generation
- The .docx format remains editable by the client (layout, logo, colours) without touching the Flows

**Rejected alternatives** :

| Alternative | Reason for rejection |
|---|---|
| Mail Merge tags (`<<field>>`) | Not supported by the Power Automate "Populate" action |
| `{{field}}` tags (Handlebars style) | Not natively supported by Word or Power Automate |
| PDF generation via HTML + WeasyPrint / Puppeteer | Requires an external runtime, outside the M365 ecosystem |
| PDF generation via Adobe PDF Services | Premium connector, additional cost |
| LaTeX / Pandoc | Outside the M365 ecosystem, requires a server |

**Known limitations** :
- "Repeating Section" Content Controls (for loops) are not supported by the Power Automate "Populate" action. The approach used is to statically create 12 monthly review sections in the template (one per possible month), and inject an empty string for non-existent reviews. This means the template has a fixed 12-section structure, with visible blank space at the end of the document if the participant has fewer than 12 reviews.
- Building a .docx with correct Content Controls requires access to Microsoft Word (Content Controls cannot be created correctly by python-docx or by an agent without a Word runtime). The kit templates are built by Python script with python-docx and validated by programmatic assertion.
- Modifying a Tag value in the .docx after going live requires updating the corresponding Flow.

---

### Outlook / Shared mailbox

**Role** : sending emails to the participant (J-5 invitation) and to the Beraterin (PDF on the day of the appointment), from a generic organisational address.

**Rationale** :
- The Office 365 Outlook connector is standard in E3
- The "Send an email (V2)" action supports sending "From" a shared mailbox if the service account has the "Send As" permission
- The generic sender address (`transfer@{domain}.de`) avoids accidental replies to a named account
- The shared mailbox is native M365, no additional cost for an E3 tenant

**Rejected alternatives** :

| Alternative | Reason for rejection |
|---|---|
| SendGrid / Mailgun | Third-party service, data potentially outside the tenant, premium connector required in Power Automate |
| SMTP relay via Azure | Requires an Azure subscription, complex configuration |
| Named M365 account as sender | Governance issue if the account changes or is disabled |
| Microsoft Graph API | Requires an Azure App registration and a custom connector (not standard E3) |

**Known limitations** :
- Exchange Online E3 limit: 10,000 recipients per day for external sending (well above the target volume of ~100 sends per day)
- Emails are sent in HTML. If the participant has disabled HTML in their email client, the link button will render as plain text (correct behaviour: the link remains clickable).

---

## Structural decisions

Summary of the project's Architecture Decision Records. Full document: `docs/DECISIONS.md`.

### ADR-001 : Microsoft 365-only stack

The solution relies exclusively on Microsoft 365 E3 services (Forms, SharePoint, Power Automate, Word, Outlook). No external dependencies.

Main reasons: the German Transfergesellschaft context uses M365 near-universally, DSGVO compliance is achieved by design (data stays in the client tenant), and the marginal cost is zero (licences already paid).

Evaluated alternatives (Google Workspace, self-hosted n8n, custom Node.js) were rejected on grounds of DSGVO compliance, maintenance cost or mismatch with the client context.

### ADR-002 : Handwritten signatures preserved on Zielvereinbarungen

Signature fields in the cumulative PDF are left blank. The document is printed at the appointment, physically signed, and scanned if the organisation wishes to retain a digital copy.

Rationale: eIDAS-compliant electronic signature solutions (DocuSign, Microsoft eSign, Adobe Sign) involve either a premium licence or a third-party service. Handwritten signatures are legally sufficient for Zielvereinbarungen within the meaning of §111 SGB III.

Integration of an eSign module is documented in the backlog for v0.2.

### ADR-003 : Declarative, open monthly review

Six fields in the monthly form, one mandatory (general review). The participant decides what to share.

Rationale: the Transfer Mappe is a tool for the participant-Beraterin relationship, not a surveillance tool. An overly prescriptive form would reduce the response rate and is inconsistent with the spirit of the programme. Minimising the data collected also strengthens DSGVO compliance.

### ADR-004 : 12-month journey limit

The Word template includes 12 monthly sections. This limit is consistent with the legal ceiling of §111 SGB III (maximum duration of a Transfergesellschaft: 12 months).

### ADR-005 : Word templates specified before being built

Word template specifications (structure of the 118 Content Controls, Tag values, Power Automate mapping) were delivered in Sprint 1 as Markdown files. Building the actual .docx files is a separate task requiring access to Microsoft Word or python-docx.

### ADR-006 : Sprint 2 delivered in blueprint mode

In the absence of a Microsoft 365 Developer Program tenant during Sprint 2, Power Automate Flows and Microsoft Forms are not exported as importable JSON but documented as Markdown implementation guides (action by action, exact expressions).

Practical consequence: deployment takes 1 to 2 hours rather than 30 minutes (if JSON files were importable). Functional quality is not affected.

---

## Security and DSGVO

### Data perimeter

All processed data remains within the client's Microsoft 365 tenant:
- Form responses: stored in Microsoft Forms (client tenant)
- Participant data and reviews: SharePoint lists (client tenant)
- Generated PDFs: SharePoint document library (client tenant)
- Sent emails: Exchange Online of the client tenant

No data transits through a third-party service. No external webhooks. No connections to external APIs.

### Data minimisation (DSGVO Art. 5.1.c)

The solution collects only the data necessary for the tracking process:
- Participant side: first name, last name, email, language, start date, appointment date, status
- Profile side: career data entered voluntarily, all optional
- Review side: monthly review (the only mandatory field), five optional fields

Microsoft Forms are configured in anonymous mode (disable "Record name"): responses are not linked to an M365 account.

### Data access

| Actor | Access |
|---|---|
| Participants | No access to the SharePoint site. Access only to their public Forms |
| Beraterinnen | Members of the SharePoint site. Read access to lists, receive PDFs by email |
| Administrator | Site owner. Full access |
| Power Automate service account | Site member. Read/write access to lists and libraries |

Participants have no access to other participants' data. SharePoint lists are not publicly exposed.

### Processing responsibility

The kit is a tool, not a service. The author processes no personal data of participants. The outplacement company deploying the kit is the data controller under DSGVO, within the limits of the M365 tenant it administers.

The deploying organisation is responsible for concluding an Auftragsverarbeitungsvertrag (AVV - data processing agreement) with Microsoft for the processing of personal data via M365, in accordance with DSGVO Art. 28. Microsoft provides standard contractual terms under their M365 Data Processing Agreement.

### Data retention

No automatic retention policy is implemented in v0.1. The deploying organisation is responsible for defining and applying its own data retention and deletion policy (recommendation: delete SharePoint records and PDFs at the end of the participant's journey, after any applicable statutory retention periods).

---

## Scalability

### Target volumes and limits

| Component | Target volume | Service limit | Headroom |
|---|---|---|---|
| Simultaneous participants | 2,000 | 30 million items per SharePoint list | Very large |
| Total monthly reviews | 24,000 (2,000 x 12) | 30 million items per list | Very large |
| Emails sent per day | ~100 (working days) | 10,000 recipients/day Exchange Online E3 | Large |
| PDFs generated per day | ~100 | Power Automate limit: execution duration, not volume | Acceptable |
| Forms forms | 4 forms | 200 questions / 50,000 responses per form | Large |
| Flow concurrency | Sequential by default | 50 in parallel (Apply to each) | Adjustable |

### Flow execution times

**Flow 1 - J-5 Invitation** : approximately 1 to 2 seconds per participant (SharePoint call + email send). For 100 participants per day: 2 to 3 minutes.

**Flow 2 - PDF Generation** : approximately 15 to 20 seconds per participant (read profile + reviews + populate Word + convert PDF + save to SharePoint + send email). For 100 participants: 25 to 30 minutes in sequential mode. With concurrency enabled (20 in parallel): approximately 5 to 8 minutes.

### Scaling up

For volumes above 2,000 simultaneous participants or 100 PDFs per day:
- Enable concurrency on "Apply to each" loops (up to 50 in parallel)
- Increase "Maximum number of items" in "Get items" actions (default: 100, max: 5,000 per call)
- For volumes above 5,000 participants, implement pagination in SharePoint actions (property `odata-skiptoken`)
- Exchange Online limits (10,000 emails/day) are not a limiting factor for the target volume

---

## Known limitations and planned improvements

### Limitations of v0.1

**Fixed review sections in the PDF** : the Word template contains exactly 12 monthly sections. Unused sections appear blank at the end of the document. Power Automate does not support "Repeating Section" Content Controls for dynamic section count generation.

**No JSON import of Flows** : due to the absence of a Dev tenant during Sprint 2 (ADR-006), Flows are delivered as Markdown blueprints rather than importable JSON files. JSON export will be produced at the time of the first real deployment.

**Relationships without referential integrity** : the join between `BilansMensuels.id_participant` and `Participants.ID` is an application-level convention. SharePoint does not enforce referential integrity. Manually deleting a participant without deleting their reviews creates orphaned records.

**No review deduplication** : if a participant submits the monthly form twice before the same appointment, two BilansMensuels records are created. The Beraterin will see two reviews for the same period in the PDF. Handling this case is the administrator's responsibility (manual deletion of the duplicate).

### Planned improvements (backlog)

**v0.2 - eSign module** (ADR-002) : integration of an optional electronic signature module for Zielvereinbarungen, via Microsoft eSign or an eIDAS-compatible connector. Conditional on the existence of an appropriate licence at the client.

**v0.2 - Opt-in personal tracker** (ADR-003) : optional module allowing the participant to log their applications and contacts on an ongoing basis, with aggregation in the cumulative PDF. Envisaged architecture: two additional SharePoint lists (Candidatures, Contacts) and a consolidation Flow.

**v0.1.1 - JSON export of Flows** : once deployed on a real tenant, export Flows as JSON to facilitate subsequent deployments.

---

## Dependencies

### Required licences

| Service | Minimum licence | Included in E3 |
|---|---|---|
| Microsoft Forms | M365 E1 | Yes |
| SharePoint Online | M365 E1 | Yes |
| Power Automate (standard connectors) | M365 E3 | Yes |
| Word Online (Business) - Power Automate connector | M365 E3 | Yes |
| Office 365 Outlook - Power Automate connector | M365 E1 | Yes |
| Exchange Online (shared mailbox) | M365 E1 | Yes |

No premium Power Automate connectors are used. The solution is fully compatible with a standard M365 E3 plan.

### Deployment tools (setup only)

| Tool | Version | Usage |
|---|---|---|
| PowerShell | 7.x | Running the SharePoint provisioning script |
| PnP.PowerShell | Latest stable | SharePoint list provisioning (one-time setup) |

PnP.PowerShell is required only for the initial deployment. It is not used in production.

### Runtime dependencies

No external runtime dependencies. The solution operates exclusively with the Microsoft 365 services of the client tenant. No external server, no third-party API keys, no additional hosting service.
