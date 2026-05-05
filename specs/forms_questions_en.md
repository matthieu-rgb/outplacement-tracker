# Forms - Questions in English (EN)

Exact specification of the two Microsoft Forms in English version.
This is a 1:1 translation of `forms_questions_de.md`. All SharePoint column mappings are identical.

Conventions :
- Mandatory field indicated by (*) in the question title
- Optional fields : no asterisk
- Column names remain snake_case identical to the DE version (no translation of technical names)
- Question order = display order in the form

---

## Form 1 : Onboarding - Career Profile (EN)

**Form name** : Your Career Profile - Transfer Mappe

**Introduction text** (displayed at the top of the form) :

> This short questionnaire helps your advisor understand you and your goals better.
> All fields are optional - you decide what you want to share. You can fill in this form again at any time to update your information.
> All information remains confidential and will be used exclusively in the context of your career transition support.

---

### Question 1 - Plan A : Primary Career Goal

**Type** : Multiple lines of text
**Mandatory** : no
**Title** : Your primary career goal (Plan A)
**Description / subtext** : What professional direction would you like to pursue? What kind of position are you looking for? In which sector or region?
**Placeholder** : Example: Project Manager in mechanical engineering, Rhine-Saar-Luxembourg region, companies with 200+ employees
**Target SharePoint column** : `Profils.plan_a`

---

### Question 2 - Plan B : Alternative Career Goal

**Type** : Multiple lines of text
**Mandatory** : no
**Title** : Your alternative career goal (Plan B)
**Description / subtext** : If Plan A does not work out - what alternative professional direction would also be of interest to you?
**Placeholder** : Example: Self-employment as a consultant, or transition to the public sector
**Target SharePoint column** : `Profils.plan_b`

---

### Question 3 - Marketing Plan

**Type** : Multiple lines of text
**Mandatory** : no
**Title** : Your professional profile and strengths
**Description / subtext** : What are your core competencies? What makes you particularly attractive to employers? Which experiences or qualifications do you want to highlight?
**Placeholder** : Example: 15 years of experience in automotive electronics, specialised in CAN-Bus and diagnostics, leadership experience with teams up to 8 people, fluent in German and French
**Target SharePoint column** : `Profils.marketingplan`

---

### Question 4 - Target Market

**Type** : Multiple lines of text
**Mandatory** : no
**Title** : Your target market
**Description / subtext** : In what environment would you like to work? Think about region, sector, company size or type of organisation.
**Placeholder** : Example: Saarland / Lorraine / Luxembourg, automotive or mechanical engineering, mid-sized companies (100-500 employees)
**Target SharePoint column** : `Profils.zielmarkt`

---

**Confirmation text** (displayed after submission) :

> Thank you for your input. Your career profile has been saved and is available to your advisor.
> You can fill in this form again at any time to update your information.

---

## Form 2 : Monthly Review (EN)

**Form name** : Your Monthly Update - Transfer Mappe

**Introduction text** (displayed at the top of the form) :

> Please take 5 minutes to complete this short update before your next appointment with your advisor.
> Only the first question is mandatory. All other fields are optional - you decide what you want to share.
> This information helps your advisor prepare for your session.

---

### Question 1 - General Review (*)

**Type** : Multiple lines of text
**Mandatory** : yes
**Title** : How was your month? (*)
**Description / subtext** : Please briefly describe how the past month went - professionally and/or personally, whatever feels relevant to you.
**Placeholder** : Your update here...
**Target SharePoint column** : `BilansMensuels.bilan_general`

---

### Question 2 - Objective Status

**Type** : Choice + free text complement

**Part 2a - Choice**
**Mandatory** : no
**Title** : How are you progressing on the agreed objectives?
**Description / subtext** : Think about the goals you agreed on with your advisor at your last session.
**Options** (single choice) :
- Fully achieved
- Partially achieved
- Not achieved
- Not yet relevant
**Target SharePoint column** : `BilansMensuels.statut_objectifs`
**Value mapping** :
  - "Fully achieved" -> `vollstaendig_erreicht`
  - "Partially achieved" -> `teilweise_erreicht`
  - "Not achieved" -> `nicht_erreicht`
  - "Not yet relevant" -> `noch_nicht_relevant`

**Part 2b - Free text**
**Mandatory** : no
**Title** : Would you like to add any details?
**Description / subtext** : (optional) A brief explanation or context for your answer above.
**Placeholder** : Your details here...
**Target SharePoint column** : `BilansMensuels.statut_objectifs_detail`

---

### Question 3 - What went well

**Type** : Multiple lines of text
**Mandatory** : no
**Title** : What went well this month?
**Description / subtext** : (optional) What positive developments, successes or progress have you experienced?
**Placeholder** : Your answer here...
**Target SharePoint column** : `BilansMensuels.was_lief_gut`

---

### Question 4 - Where I need support

**Type** : Multiple lines of text
**Mandatory** : no
**Title** : Where do you need support?
**Description / subtext** : (optional) In which areas would you welcome help or support - from your advisor or otherwise?
**Placeholder** : Your answer here...
**Target SharePoint column** : `BilansMensuels.wo_brauche_ich_unterstuetzung`

---

### Question 5 - Topics for the next session

**Type** : Multiple lines of text
**Mandatory** : no
**Title** : What topics would you like to discuss at the next session?
**Description / subtext** : (optional) What is particularly important to you for your next conversation?
**Placeholder** : Your answer here...
**Target SharePoint column** : `BilansMensuels.themen_naechster_termin`

---

### Question 6 - Additional remarks

**Type** : Multiple lines of text
**Mandatory** : no
**Title** : Any other remarks?
**Description / subtext** : (optional) Is there anything else you would like to share that is not covered above?
**Placeholder** : Your answer here...
**Target SharePoint column** : `BilansMensuels.sonstige_anmerkungen`

---

**Confirmation text** (displayed after submission) :

> Thank you for your update. Your advisor will read it before your session.
> We look forward to seeing you soon.

---

## Forms configuration notes

- **Sharing** : "Anyone with the link can respond" (link generated by the J-5 Flow, one unique link per participant per month)
- **Anonymity** : disable "Record name" if participants do not have a M365 account (form accessible without login)
- **Submission limit** : 1 response per link (Power Automate generates a unique link per invitation)
- **Interface language** : English
- **Export** : responses are retrieved via the Microsoft Forms connector in Power Automate, not via manual Excel export

## Value mapping note (EN -> SharePoint)

The EN form uses English labels visible to the participant, but the values stored in SharePoint (`BilansMensuels.statut_objectifs`) use the same German-origin internal codes as the DE form. This ensures a single, consistent data model regardless of the participant's language. The Power Automate Flow maps the English label to the correct internal code at submission time.

| EN label displayed  | Internal code stored in SharePoint |
|---------------------|-------------------------------------|
| Fully achieved      | `vollstaendig_erreicht`             |
| Partially achieved  | `teilweise_erreicht`                |
| Not achieved        | `nicht_erreicht`                    |
| Not yet relevant    | `noch_nicht_relevant`               |
