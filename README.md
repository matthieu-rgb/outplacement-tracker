# outplacement-tracker

> A Microsoft 365-native solution for digitalising the monthly progress tracking of participants in a Transfergesellschaft, while preserving the human dimension of the participant-Beraterin relationship.

## Context

German Transfergesellschaften (outplacement companies operating under §111 SGB III) support participants over 6 to 12 months through monthly appointments with a Beraterin. Tracking is typically done via a paper-based "Transfer Mappe" or a manually completed PDF, neither of which fits a digital workflow.

This solution provides a lightweight alternative: a monthly form sent five days before each appointment, a cumulative PDF generated automatically on the morning of the appointment, with no surveillance and no mandatory entry for every individual action.

## How it works

```
J-5 before appointment  -> the participant receives an email with a Forms link
                           and freely summarises their month

Day of appointment      -> the Beraterin receives a cumulative PDF containing
                           the participant's full history and the current
                           monthly summary
```

Six fields in the monthly form, one mandatory. The participant decides what to share. The Beraterin arrives prepared. The PDF belongs to the participant.

## Technical stack

- **Microsoft Forms** for forms (DE and EN)
- **SharePoint** for the database and lists
- **Power Automate** for orchestration (J-5 invitation + PDF generation)
- **Word template** for the cumulative PDF output
- **Outlook** for notification delivery

All data remains within the client's Microsoft 365 tenant. No data leaves the tenant. Compatible with a standard E3 plan, no premium connectors required.

## Deployment

See `docs/INSTALLATION.md` (produced in sprint 3).

Summary:
1. Import the SharePoint schema via the PnP PowerShell script
2. Import the two Microsoft Forms
3. Import the two Power Automate Flows
4. Upload the Word template to SharePoint
5. Adjust variables (sender mailbox, default Beraterin)

Estimated deployment time: 1 to 2 hours for a Microsoft 365 administrator.

## Status

| Sprint | Objective | Status |
|--------|-----------|--------|
| 1 | Business foundations (schemas, templates, content) | Done |
| 2 | Automation (Power Automate, setup scripts) | Done |
| 3 | Documentation and deliverables (PITCH.pdf, INSTALLATION.md) | Done - release v0.1.0 |

## Licence

MIT. Free to use, modify and redistribute.

## Author

Matthieu Riegert ([@matthieu-rgb](https://github.com/matthieu-rgb)) - 2026

Personal project, delivered without warranty or support commitment.
