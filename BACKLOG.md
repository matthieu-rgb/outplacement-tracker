# BACKLOG.md

Ideas and features outside the v0.1 scope. Do NOT implement in v0.1.

Any proposed addition raised during a sprint lands here, not in the code. The Tech Lead arbitrates.

---

## v0.2 planned

### Optional personal application tracker

An **opt-in** module for Teilnehmer who wish to log their applications and contacts on an ongoing basis. Strictly voluntary and reserved for the Teilnehmer's personal use. The data is visible neither to the Beraterin nor to the management of the Transfergesellschaft.

Rationale: some Teilnehmer appreciate a tracking tool for their own use. v0.1 does not include one to avoid the surveillance trap, but an opt-in version respects individual choice.

### Aggregated reporting for the Beraterin

A SharePoint dashboard listing monitored Teilnehmer with:

- Date of next appointment
- Status of the last review received (submitted / not submitted / overdue)
- Qualitative trend over the past 3 months

No individual data aggregated for analytical purposes. Operational view only.

### eIDAS-compliant electronic signature

DocuSign, Adobe Sign, or Microsoft eSign integration for Zielvereinbarungen. Requires a premium licence and involves eIDAS compliance. Out of scope for v0.1 by design.

---

## v0.3+ planned

### Qualifikationen und Zeugnisse module

A structured SharePoint space for uploading and classifying the Teilnehmer's certificates, qualifications, and attestations. Search, tagging, and export.

### Expense claims (Rechnung an die Transfer GmbH)

A separate form for expense reimbursement requests (transport, training, equipment). Validated by the Beraterin. Monthly accounting export.

### Dedicated mobile application

A Microsoft Power Apps or Teams App allowing the Teilnehmer to complete the monthly review from a mobile device, with push reminders.

### Teams integration for appointments

A Teams Meeting link generated automatically with each monthly appointment. J-1 notification and day-of reminder.

### Multi-tenancy and per-organisation customisation

For groups of Transfergesellschaften or holding structures. Not relevant for v0.1.

---

## Definitively rejected ideas

### Mandatory logging of every application and contact

Rejected. See `docs/DECISIONS.md` ADR-003. Incompatible with the spirit of the Transfer Mappe and the trust relationship between Teilnehmer and Beraterin.

### Hosting by the author on a personal VPS

Rejected. See initial project discussion. Incompatible with the "community contribution" position and represents a disproportionate DSGVO commitment for the author.

### Automatic reminder on non-submission

Rejected. The Teilnehmer chooses whether to submit. No pressure, no reminder, no "you have not submitted" notification. Responsibility for follow-up remains with the Beraterin.

### Teilnehmer "performance" score

Categorically rejected. The Transfer Mappe is not an evaluation tool and outplacement is not a competition.
