# ASSUMPTIONS.md

Business assumptions made for the `outplacement-tracker` v0.1 project.

The author did not have direct access to the business team of a Transfergesellschaft to validate the specifications in detail. The assumptions below were made on the basis of:

- A close reading of the "Transfer Mappe" v2026 V1 from 10 k Beratung GmbH
- The German legal framework for Transfergesellschaften (SS 111 SGB III)
- Practices observed in the German outplacement sector

Any organisation deploying this solution is invited to validate and adjust these assumptions according to its own practices. The solution is flexible enough to accommodate this.

---

## A1 : Maximum programme duration

**Hypothesis**: 12 months maximum.

**Source**: SS 111 SGB III, which caps the legal duration of a Transfergesellschaft at 12 months.

**Impact**: the Word template and the Power Automate Flows are sized to stack up to 12 monthly reviews.

**Adjustable**: yes, by modifying the limit in the Word template and the Power Automate loop.

---

## A2 : Appointment frequency

**Hypothesis**: one appointment per month between the Teilnehmer and the Beraterin.

**Source**: standard practice observed in the sector, consistent with the duration of a typical programme.

**Impact**: the review form is sent once a month, 5 days before the appointment.

**Adjustable**: yes, by modifying the trigger of the invitation Power Automate Flow and the list of appointment dates in SharePoint.

---

## A3 : Nature of monthly monitoring

**Hypothesis**: monthly monitoring is primarily declarative and open-ended. The Teilnehmer summarises what they choose to share. No mandatory tracker for applications or contacts.

**Source**: the original Transfer Mappe states explicitly that the document belongs to the Teilnehmer. The Beraterin-Teilnehmer relationship is based on trust, not surveillance.

**Impact**: the monthly form has 6 fields, of which 5 are optional.

**Adjustable**: yes, by adding or removing fields in the Microsoft Forms form.

---

## A4 : Signatures on Zielvereinbarungen

**Hypothesis**: signatures remain handwritten. The cumulative PDF contains blank signature slots; the document is printed, signed, and scanned at the appointment.

**Source**: handwritten signatures are legally sufficient for this type of internal document in Germany. Decision retained for simplicity (no premium eSign licence).

**Impact**: no premium connector required, no DocuSign or Adobe Sign.

**Adjustable**: yes, an evolution towards eSign is documented in `BACKLOG.md` for v0.2.

---

## A5 : Target volume

**Hypothesis**: the solution is sized for 1,500 to 2,000 Teilnehmer tracked simultaneously by a Transfergesellschaft.

**Source**: volume specified by the initial project stakeholder.

**Impact**: approximately 75 to 100 email sends per working day, well within Outlook limits (10,000 emails/day).

**Adjustable**: yes, up to several tens of thousands of Teilnehmer without architectural changes.

---

## A6 : Profile of the deploying administrator

**Hypothesis**: the Transfergesellschaft has a Microsoft 365 administrator capable of:

- Creating SharePoint lists (or running a PnP PowerShell script)
- Importing Microsoft Forms
- Importing Power Automate Flows
- Configuring variables (sender mailbox, default Beraterin)

**Source**: standard profile of an M365 administrator in a German organisation.

**Impact**: `INSTALLATION.md` is written for this profile, not for an end user.

**Adjustable**: no. If the administrator does not have these competencies, the organisation must engage an external provider or train internally.

---

## A7 : Visual identity of the output PDF

**Hypothesis**: the Transfergesellschaft expects the cumulative PDF to reflect a visual identity close to their paper Transfer Mappe (sober, corporate blue, serif typeface for headings).

**Source**: observation of the Transfer Mappe from 10 k Beratung GmbH v2026 V1.

**Impact**: the Word template is designed with a sober and customisable layout. Colours and logos are adjustable without modifying the architecture.

**Adjustable**: yes, the Word template is freely editable.

---

## A8 : DSGVO/BDSG framework

**Hypothesis**: the Transfergesellschaft is the data controller (Verantwortlicher) within the meaning of the DSGVO for Teilnehmer data. The project author is neither controller nor processor.

**Source**: the solution is delivered as an open source kit. The author processes no data.

**Impact**: no Auftragsverarbeitungsvertrag between the author and the Transfergesellschaft. The Transfergesellschaft assumes full responsibility for data processing.

**Adjustable**: no. If an organisation wishes to outsource deployment and operation, it must engage a provider who will sign an Auftragsverarbeitungsvertrag with it.
