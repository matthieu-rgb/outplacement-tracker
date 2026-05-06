# SECURITY_REVIEWS.md

Append-only log of security and DSGVO compliance reviews for the outplacement-tracker project.

Each entry is definitive. Do not modify existing entries.
To correct a previous assessment, add a new entry.

---

## Entries

---

### REV-001

**Date:** 2026-05-05
**Deliverable:** docs/PRIVACY.md (initial creation v1.0)
**Auditor:** DSGVO/Security Agent
**Verdict:** APPROVED

**Checklist:**

- [x] Personal data hardcoded in code, documentation, or examples: NONE
      (samples use Max Mustermann / John Doe, confirmed in samples/README.md)
- [x] Samples anonymised: YES (Max Mustermann DE, John Doe EN, Maria Schmidt for Beraterin)
- [x] Unjustified transfer outside the EU: NONE (architecture 100% within client M365 tenant)
- [x] Documentation explicitly states that data remains within the client tenant: YES (sections 2, 8, 9)
- [x] Restrictive SharePoint permissions documented as defaults: YES (section 7.2 and checklist 11.1)
- [x] Responsibility model documented (author processes no data): YES (section 2 - full chain)
- [x] Power Automate Flows - PII in logs: RISK DOCUMENTED and accepted (section 3.5 - Microsoft 28-day logs)
- [x] Emails with minimal data: YES (section 12 - detailed analysis of email templates)

**Observations:**

1. The responsibility chain (section 2) conforms to the expected model. The author is
   clearly excluded from the processing chain. The absence of an author/deployer
   Auftragsverarbeitungsvertrag is justified and documented.

2. The legal basis Art. 6(1)(b) DSGVO retained for all fields is correct in the
   SGB III context. The non-use of consent as the primary legal basis is explicitly
   justified (section 4.3) - a rigorous approach.

3. The handling of Power Automate logs (section 3.5) raises an important point:
   these logs may contain PII (Teilnehmer name and email).
   This point is documented and acceptable because it is inherent to the M365
   platform and the logs remain within the tenant. Organisations are advised to restrict
   access to the Power Automate portal (section 7.2).

4. The mention of the EU Data Boundary (section 9.1) is correct for M365 E3 licences
   with an EU region. The requirement to verify the tenant region is included in
   the checklist (section 11.1) - a critical point, well handled.

5. The likelihood of a mandatory DSB (Datenschutzbeauftragter) for Transfergesellschaften
   is correctly argued (Art. 37 DSGVO + § 38 BDSG) without absolute certainty,
   which is the legally honest position.

6. The deletion procedure (section 5.2) offers three options, one of which is automated
   and not yet delivered (BACKLOG). This transparency is correct.

**Residual risks identified (accepted):**

- Power Automate logs contain transient PII. Risk inherent to the platform, outside
  the solution scope, documented.
- The DPIA (Art. 35) is not conducted by the author: correct, it belongs to the
  deploying organisation. It is referenced in the checklist (section 11.2).
- The metadata of the .docx template files may contain the author's name
  (Word owner property). Point flagged in section 12 for deployment.

**Adjustments requested:** NONE

---

### REV-002

**Date:** 2026-05-06
**Deliverable:** docs/PRIVACY.md (full rewrite v1.1 - German language, ADR-007)
**Auditor:** DSGVO/Security Agent
**Verdict:** APPROVED

**Context:**

Full rewrite of PRIVACY.md from the French version (v1.0) to the German version
(v1.1), in accordance with the language policy ADR-007. The document targets the
DSB (Datenschutzbeauftragter) and the legal department of a German Transfergesellschaft
deploying the solution.

**Checklist on deliverable v1.1:**

- [x] Personal data hardcoded in the document: NONE
      (no real email address, no real name - examples use transfer@domain.de)
- [x] Samples anonymised: YES (not directly applicable to PRIVACY.md - no data examples)
- [x] Unjustified transfer outside the EU mentioned or introduced: NONE
- [x] Document explicitly states that data remains within the client tenant: YES (sections 2, 8, 9)
- [x] Restrictive SharePoint permissions documented: YES (sections 7.1, 7.2, 11.1)
- [x] Responsibility model (author processes no data): YES (section 2 - full chain preserved)
- [x] PII in Power Automate logs: RISK DOCUMENTED and accepted (section 3.5)
- [x] Emails with minimal data: YES (section 12)

**Observations on translation quality and adaptation:**

1. DSGVO/BDSG terminology correctly and consistently applied:
   Verantwortlicher, Auftragsverarbeiter, AVV, betroffene Person, personenbezogene Daten,
   VVT, DSFA, DSB, Loeschkonzept, Datensparsamkeit, Zweckbindung, Speicherbegrenzung, TOM,
   DSGVO, BDSG, SCC. No unjustified French or English term remains.

2. Legal references conform to standard German form:
   Art. 6 Abs. 1 lit. b DSGVO, Art. 37 Abs. 1 lit. b DSGVO, § 38 BDSG, § 195 BGB,
   § 111 SGB III. Format correct.

3. Section 11.1 (mandatory checklist) adds one item compared to v1.0: neutralising
   Word template metadata before upload. This point was mentioned in section 12 of
   v1.0 but was not in the checklist. This is an improvement consistent with the
   REV-001 recommendation (residual Word risk).

4. The responsibility chain (section 2.1) is fully preserved, with the clear
   position of Matthieu Riegert as neither Verantwortlicher nor Auftragsverarbeiter.
   The absence of an Auftragsverarbeitungsvertrag with the author is maintained and documented.

5. The substantive content is identical to v1.0: no data removed, no purpose added.
   This is a translation with terminological adaptation, not a scope change.

6. The formal register (Sie) is used only in sections addressing the reader directly.
   The remainder of the document is in the third person. Correct.

7. The revision history (section 13) correctly records both versions:
   v1.0 initial creation (French, 2026-05-05) and v1.1 German rewrite (2026-05-06).

**Residual risks identified (unchanged from REV-001):**

- Power Automate logs contain transient PII (28 days). Documented, inherent to
  the M365 platform, outside the solution scope.
- The DSFA (Art. 35 DSGVO) belongs to the deploying organisation. Referenced in 11.2.
- .docx metadata: now included in the mandatory checklist (11.1).
  Residual risk reduced compared to REV-001.

**Adjustments requested:** NONE

---

### REV-003

**Date:** 2026-05-06
**Deliverable:** docs/PRIVACY.md (cross-review encoding/terminology v1.1)
**Auditor:** DSGVO/Security Agent
**Verdict:** APPROVED after corrections

**Context:**

Targeted review of docs/PRIVACY.md v1.1 under three angles:
(1) encoding of German characters (umlauts, eszett),
(2) accuracy of DSGVO/BDSG terminology,
(3) factual accuracy of the law applicable to Transfergesellschaften.

**Review results:**

**Encoding:**

Four anomalies detected and corrected:

- Line 71: "tragt" -> "traegt" (conjugation of "tragen" - missing umlaut)
- Line 302: "ermoeglichten" (Praeteritum) -> grammatical error
  (Praesens required), not an encoding artefact, detected during the systematic pass.
  Corrected: ermoeglichten -> ermoeglichten (Praesens).
- Line 376: "ausser" -> missing eszett - residual encoding artefact
- Line 390: "Uebersetzung" -> unconverted "Ue" sequence - residual artefact

No other "ae"/"oe"/"ue" artefact remains outside technical field names between
backticks and French SharePoint list identifiers (langue, nom,
prenom, id_conseillere, etc.) which are legitimate technical identifiers without umlauts.

**DSGVO/BDSG terminology:**

Terminology compliant throughout the document. Points verified:
- Verantwortlicher (Art. 4 Nr. 7 DSGVO): correct
- Auftragsverarbeiter (Art. 4 Nr. 8 DSGVO): correct
- Auftragsverarbeitungsvertrag / AVV (Art. 28 DSGVO): correct
- Datenschutz-Folgenabschaetzung / DSFA (Art. 35 DSGVO): correct
- personenbezogene Daten (Art. 4 Nr. 1 DSGVO): correct
- Verzeichnis der Verarbeitungstaetigkeiten / VVT (Art. 30 DSGVO): correct
- betroffene Person (Art. 4 Nr. 1 DSGVO): correct
- Datenschutzbeauftragter / DSB (Art. 37 DSGVO): correct
- technische und organisatorische Massnahmen / TOM (Art. 32 DSGVO): correct
- Article citations in standard German form (Art. X Abs. Y lit. Z DSGVO): correct

**Factual accuracy:**

- Art. 6 Abs. 1 lit. b DSGVO as the primary legal basis in the § 111 SGB III context:
  correct. The contractual relationship between the Transfergesellschaft and the Teilnehmer
  (Transfervertrag) justifies this legal basis for all operational processing.

- Art. 6 Abs. 1 lit. f DSGVO (legitimate interest) for documentation vis-a-vis the
  Agentur fuer Arbeit: correct. The need for documentary evidence in inspections
  constitutes a recognised legitimate interest.

- 3-year retention period for PDFs, based on § 195 BGB (general limitation period):
  correct for service contracts.

- § 38 BDSG (mandatory DSB from 20 persons processing automated data): correct.
  National supplement consistent with DSGVO Art. 37.

- Microsoft EU Data Boundary for E3 tenants with EU region: correct at the time of
  writing. Subject to changes in Microsoft's policy.

- 28-day retention for Power Automate logs under E3 licence: correct per current
  Microsoft documentation.

- The caveat on the right to erasure limited by the documentation obligation
  vis-a-vis the Agentur fuer Arbeit (Art. 17 Abs. 3 DSGVO): correct and well formulated.

- Absence of special category data within the meaning of Art. 9 DSGVO in the
  solution scope: confirmed by analysis of the three list fields.

**Residual risks:** unchanged (cf. REV-001, REV-002).

**Adjustments requested:** 4 encoding/grammar corrections applied directly.
No substantive adjustment required.

---

### REV-004

**Date:** 2026-05-06
**Deliverable:** sharepoint/setup_lists.ps1 (post-translation comment review)
**Auditor:** DSGVO/Security Agent
**Verdict:** APPROVED

**Context:**

Review triggered by translation of inline comments and Write-Host strings from French
to German. Five specific checkpoints were evaluated.

**Checklist:**

- [x] No sensitive data in comments: CONFIRMED
      Only domain reference is contoso.sharepoint.com (Microsoft canonical demo tenant,
      not a real or customer tenant). No email address, no token, no credential,
      no real tenant URL anywhere in the file.
- [x] German translation introduces no new information vs French original: CONFIRMED
      All comments are operational/documentary. No bypass technique, no workaround,
      no security-relevant information introduced. The inline comment on line 122
      ("DateOnly per CAML erzwingen") accurately describes the code and carries no risk.
- [x] Placeholder values remain clearly marked: CONFIRMED
      The script uses $SiteUrl as a mandatory parameter passed at runtime (line 17).
      The .EXAMPLE block uses contoso.sharepoint.com as a demo value per PowerShell
      documentation convention. No {curly brace} placeholders were used or removed.
      The /sites/TransferMappe path fragment in the Write-Host guidance block (line 255)
      is a project-wide site name, not a secret.
- [x] Idempotency claim documented: CONFIRMED
      Line 6 states the guarantee explicitly. All six helper functions implement it via
      Get-PnP* -ErrorAction SilentlyContinue followed by null guard and early return
      (Ensure-List line 33, column functions lines 59, 77, 95, 114, 140). Code matches claim.
- [x] Functional code unmodified by translation: CONFIRMED
      Cmdlet names, parameter names and values, variable names, conditional logic,
      type references, -ErrorAction flags, -Required:$req pattern,
      [Microsoft.SharePoint.Client.DateTimeFieldFormatType]::DateOnly enum reference,
      and Invoke-PnPQuery calls are all intact. Translation touched only comment blocks
      and Write-Host string literals.

**Observations:**

1. The column DisplayName values (nom, prenom, email, id_conseillere, etc.) are
   intentionally kept in French. These are SharePoint field identifiers defined in the
   data model ADR. The translation effort correctly left them untouched.

2. The script provisions schema only - no personal data is hardcoded or passed at
   provisioning time. PII will only appear in these lists at runtime, within the
   client tenant.

3. Connect-PnPOnline -Interactive (line 166) uses browser-based interactive
   authentication. No service principal secret or application password is embedded.
   This is the correct approach for a script distributed as open source.

**DSGVO angle:**

The lists created (Participants, Profils, BilansMensuels) will hold personal data
including name, email, and appointment dates of Transfergesellschaft participants.
The script itself is schema-only and contains no PII. Data processing responsibility
lies with the deploying organisation per the responsibility chain documented in
docs/PRIVACY.md section 2.

**Residual risks identified:** NONE specific to this file.

**Adjustments requested:** NONE

---
