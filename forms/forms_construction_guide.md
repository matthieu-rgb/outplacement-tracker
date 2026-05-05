# Guide de construction des formulaires Microsoft Forms

outplacement-tracker v0.1 - Sprint 2

Ce guide permet a un administrateur Microsoft 365 de reconstruire les 4 formulaires
de la solution a partir de zero. Temps estime : 10 a 15 minutes par formulaire.

---

## 1. Vue d'ensemble

| # | Nom du formulaire | Langue | Cas d'usage |
|---|---|---|---|
| 1 | Ihr Karriereprofil - Transfer Mappe | DE | Onboarding participant, rempli une fois en debut de parcours |
| 2 | Your Career Profile - Transfer Mappe | EN | Idem, version anglaise |
| 3 | Ihr monatlicher Bericht - Transfer Mappe | DE | Bilan mensuel, envoye par le Flow J-5 |
| 4 | Your Monthly Update - Transfer Mappe | EN | Idem, version anglaise |

Les formulaires 1 et 2 (onboarding) sont optionnels et remplis par le participant
une seule fois. Les formulaires 3 et 4 (bilan mensuel) sont envoyes automatiquement
par le Flow J-5 cinq jours avant chaque rendez-vous mensuel.

Chaque formulaire est independant dans Microsoft Forms. Il n'y a pas de dependance
technique entre eux.

---

## 2. Prerequis

- Compte Microsoft 365 avec licence E3 ou superieure
- Acces a Microsoft Forms (forms.microsoft.com)
- Les 4 formulaires doivent etre crees sur le compte de service ou la boite partagee
  de l'organisation (pas sur un compte personnel)

---

## 3. Form 1 : Onboarding DE - "Ihr Karriereprofil - Transfer Mappe"

### 3.1 Creer le formulaire

1. Aller sur forms.microsoft.com
2. Cliquer sur "Neues Formular"
3. Titre du formulaire : `Ihr Karriereprofil - Transfer Mappe`
4. Description / texte d'introduction (coller le texte suivant tel quel) :

```
Dieser kurze Fragebogen hilft Ihrer Beraterin, Sie und Ihre Ziele besser zu verstehen.
Die Angaben sind freiwillig - Sie entscheiden, was Sie teilen möchten. Sie können dieses Formular jederzeit erneut ausfüllen, um Ihre Angaben zu aktualisieren.
Alle Informationen bleiben vertraulich und werden ausschliesslich im Rahmen Ihrer Begleitung verwendet.
```

### 3.2 Question 1 - Plan A

- Cliquer sur "Frage hinzufuegen"
- Type de question : **Mehrzeiliger Text**
- Titre : `Ihr berufliches Hauptziel (Plan A)`
- Sous-titre / description : `Welche berufliche Richtung möchten Sie anstreben? Welche Art von Stelle suchen Sie? In welcher Branche oder Region?`
- Placeholder : `Beispiel: Projektmanager im Maschinenbau, Rhein-Saar-Region, Unternehmen ab 200 Mitarbeitern`
- Obligatoire : **Non**
- Colonne SharePoint cible : `Profils.plan_a`

### 3.3 Question 2 - Plan B

- Type de question : **Mehrzeiliger Text**
- Titre : `Ihr berufliches Alternativziel (Plan B)`
- Sous-titre / description : `Falls Plan A nicht greift - welche alternative berufliche Richtung wäre für Sie ebenfalls interessant?`
- Placeholder : `Beispiel: Selbstständigkeit als Berater, oder Wechsel in den öffentlichen Dienst`
- Obligatoire : **Non**
- Colonne SharePoint cible : `Profils.plan_b`

### 3.4 Question 3 - Marketingplan

- Type de question : **Mehrzeiliger Text**
- Titre : `Ihr berufliches Profil und Ihre Stärken`
- Sous-titre / description : `Was sind Ihre zentralen Kompetenzen? Was macht Sie für Arbeitgeber besonders interessant? Welche Erfahrungen oder Qualifikationen heben Sie hervor?`
- Placeholder : `Beispiel: 15 Jahre Erfahrung in der Fahrzeugelektronik, spezialisiert auf CAN-Bus und Diagnose, Führungserfahrung mit Teams bis 8 Personen, Deutsch und Französisch fließend`
- Obligatoire : **Non**
- Colonne SharePoint cible : `Profils.marketingplan`

### 3.5 Question 4 - Zielmarkt

- Type de question : **Mehrzeiliger Text**
- Titre : `Ihr Zielmarkt`
- Sous-titre / description : `In welchem Umfeld möchten Sie arbeiten? Denken Sie an Region, Branche, Unternehmensgröße oder Unternehmenstyp.`
- Placeholder : `Beispiel: Saarland / Lothringen / Luxemburg, Automobilindustrie oder Maschinenbau, mittelständische Unternehmen (100-500 Mitarbeiter)`
- Obligatoire : **Non**
- Colonne SharePoint cible : `Profils.zielmarkt`

### 3.6 Message de confirmation (apres soumission)

Dans les parametres du formulaire (icone engrenage > "Bestätigung") :

```
Vielen Dank für Ihre Angaben. Ihr Karriereprofil wurde gespeichert und steht Ihrer Beraterin zur Verfügung.
Sie können dieses Formular jederzeit erneut ausfüllen, um Ihre Angaben zu aktualisieren.
```

---

## 4. Form 2 : Onboarding EN - "Your Career Profile - Transfer Mappe"

Meme procedure que le Form 1, avec les textes anglais ci-dessous.

### 4.1 Creer le formulaire

- Titre : `Your Career Profile - Transfer Mappe`
- Texte d'introduction :

```
This short questionnaire helps your advisor understand you and your goals better.
All fields are optional - you decide what you want to share. You can fill in this form again at any time to update your information.
All information remains confidential and will be used exclusively in the context of your career transition support.
```

### 4.2 Question 1 - Plan A

- Type : **Multiple lines of text**
- Titre : `Your primary career goal (Plan A)`
- Description : `What professional direction would you like to pursue? What kind of position are you looking for? In which sector or region?`
- Placeholder : `Example: Project Manager in mechanical engineering, Rhine-Saar-Luxembourg region, companies with 200+ employees`
- Obligatoire : **No**
- Colonne SharePoint cible : `Profils.plan_a`

### 4.3 Question 2 - Plan B

- Type : **Multiple lines of text**
- Titre : `Your alternative career goal (Plan B)`
- Description : `If Plan A does not work out - what alternative professional direction would also be of interest to you?`
- Placeholder : `Example: Self-employment as a consultant, or transition to the public sector`
- Obligatoire : **No**
- Colonne SharePoint cible : `Profils.plan_b`

### 4.4 Question 3 - Marketing Plan

- Type : **Multiple lines of text**
- Titre : `Your professional profile and strengths`
- Description : `What are your core competencies? What makes you particularly attractive to employers? Which experiences or qualifications do you want to highlight?`
- Placeholder : `Example: 15 years of experience in automotive electronics, specialised in CAN-Bus and diagnostics, leadership experience with teams up to 8 people, fluent in German and French`
- Obligatoire : **No**
- Colonne SharePoint cible : `Profils.marketingplan`

### 4.5 Question 4 - Target Market

- Type : **Multiple lines of text**
- Titre : `Your target market`
- Description : `In what environment would you like to work? Think about region, sector, company size or type of organisation.`
- Placeholder : `Example: Saarland / Lorraine / Luxembourg, automotive or mechanical engineering, mid-sized companies (100-500 employees)`
- Obligatoire : **No**
- Colonne SharePoint cible : `Profils.zielmarkt`

### 4.6 Message de confirmation

```
Thank you for your input. Your career profile has been saved and is available to your advisor.
You can fill in this form again at any time to update your information.
```

---

## 5. Form 3 : Bilan mensuel DE - "Ihr monatlicher Bericht - Transfer Mappe"

### 5.1 Creer le formulaire

- Titre : `Ihr monatlicher Bericht - Transfer Mappe`
- Texte d'introduction :

```
Bitte nehmen Sie sich 5 Minuten Zeit, um diesen kurzen Bericht vor Ihrem nächsten Beratungstermin auszufüllen.
Nur die erste Frage ist Pflichtangabe. Alle anderen Felder sind freiwillig - Sie entscheiden, was Sie teilen möchten.
Diese Informationen helfen Ihrer Beraterin, den Termin gezielt vorzubereiten.
```

### 5.2 Question 1 - Bilan general (*)

- Type : **Mehrzeiliger Text**
- Titre : `Wie war Ihr Monat? (*)`
- Description : `Bitte beschreiben Sie kurz, wie der vergangene Monat verlaufen ist - beruflich und/oder persönlich, was auch immer Ihnen wichtig erscheint.`
- Placeholder : `Ihr Bericht hier...`
- Obligatoire : **Oui**
- Colonne SharePoint cible : `BilansMensuels.bilan_general`

### 5.3 Question 2a - Statut des objectifs (choix)

- Type : **Auswahl (Choice)**
- Titre : `Wie stehen Sie bei den vereinbarten Zielen?`
- Description : `Denken Sie an die Ziele, die Sie beim letzten Termin mit Ihrer Beraterin vereinbart haben.`
- Options (choix unique, une seule reponse possible) :
  - `Vollständig erreicht`
  - `Teilweise erreicht`
  - `Nicht erreicht`
  - `Noch nicht relevant`
- Obligatoire : **Non**
- Colonne SharePoint cible : `BilansMensuels.statut_objectifs`
- Note : le Flow mappe ces libelles vers les codes internes (vollstaendig_erreicht, etc.)

### 5.4 Question 2b - Precisions sur les objectifs (texte libre)

- Type : **Mehrzeiliger Text**
- Titre : `Möchten Sie dazu etwas erläutern?`
- Description : `(optional) Kurze Erklärung oder Kontext zu Ihrer Antwort oben.`
- Placeholder : `Ihre Erläuterung hier...`
- Obligatoire : **Non**
- Colonne SharePoint cible : `BilansMensuels.statut_objectifs_detail`

### 5.5 Question 3 - Was lief gut

- Type : **Mehrzeiliger Text**
- Titre : `Was lief in diesem Monat gut?`
- Description : `(optional) Welche positiven Entwicklungen, Erfolge oder Fortschritte haben Sie erlebt?`
- Placeholder : `Ihre Antwort hier...`
- Obligatoire : **Non**
- Colonne SharePoint cible : `BilansMensuels.was_lief_gut`

### 5.6 Question 4 - Wo brauche ich Unterstuetzung

- Type : **Mehrzeiliger Text**
- Titre : `Wo brauchen Sie Unterstützung?`
- Description : `(optional) In welchen Bereichen würden Sie sich Hilfe oder Unterstützung wünschen - von Ihrer Beraterin oder anderweitig?`
- Placeholder : `Ihre Antwort hier...`
- Obligatoire : **Non**
- Colonne SharePoint cible : `BilansMensuels.wo_brauche_ich_unterstuetzung`

### 5.7 Question 5 - Themen fuer den naechsten Termin

- Type : **Mehrzeiliger Text**
- Titre : `Welche Themen möchten Sie beim nächsten Termin besprechen?`
- Description : `(optional) Was liegt Ihnen besonders am Herzen für das nächste Gespräch?`
- Placeholder : `Ihre Antwort hier...`
- Obligatoire : **Non**
- Colonne SharePoint cible : `BilansMensuels.themen_naechster_termin`

### 5.8 Question 6 - Sonstige Anmerkungen

- Type : **Mehrzeiliger Text**
- Titre : `Sonstige Anmerkungen`
- Description : `(optional) Haben Sie noch etwas, das Sie mitteilen möchten und das oben nicht abgedeckt ist?`
- Placeholder : `Ihre Antwort hier...`
- Obligatoire : **Non**
- Colonne SharePoint cible : `BilansMensuels.sonstige_anmerkungen`

### 5.9 Message de confirmation

```
Vielen Dank für Ihren Bericht. Ihre Beraterin wird diesen vor Ihrem Termin lesen.
Wir freuen uns darauf, Sie bald zu sehen.
```

---

## 6. Form 4 : Bilan mensuel EN - "Your Monthly Update - Transfer Mappe"

### 6.1 Creer le formulaire

- Titre : `Your Monthly Update - Transfer Mappe`
- Texte d'introduction :

```
Please take 5 minutes to complete this short update before your next appointment with your advisor.
Only the first question is mandatory. All other fields are optional - you decide what you want to share.
This information helps your advisor prepare for your session.
```

### 6.2 Question 1 - General Review (*)

- Type : **Multiple lines of text**
- Titre : `How was your month? (*)`
- Description : `Please briefly describe how the past month went - professionally and/or personally, whatever feels relevant to you.`
- Placeholder : `Your update here...`
- Obligatoire : **Yes**
- Colonne SharePoint cible : `BilansMensuels.bilan_general`

### 6.3 Question 2a - Objective status (choice)

- Type : **Choice**
- Titre : `How are you progressing on the agreed objectives?`
- Description : `Think about the goals you agreed on with your advisor at your last session.`
- Options (single choice) :
  - `Fully achieved`
  - `Partially achieved`
  - `Not achieved`
  - `Not yet relevant`
- Obligatoire : **No**
- Colonne SharePoint cible : `BilansMensuels.statut_objectifs`
- Note : the Flow maps these labels to internal codes (vollstaendig_erreicht, etc.)

### 6.4 Question 2b - Details on objectives (free text)

- Type : **Multiple lines of text**
- Titre : `Would you like to add any details?`
- Description : `(optional) A brief explanation or context for your answer above.`
- Placeholder : `Your details here...`
- Obligatoire : **No**
- Colonne SharePoint cible : `BilansMensuels.statut_objectifs_detail`

### 6.5 Question 3 - What went well

- Type : **Multiple lines of text**
- Titre : `What went well this month?`
- Description : `(optional) What positive developments, successes or progress have you experienced?`
- Placeholder : `Your answer here...`
- Obligatoire : **No**
- Colonne SharePoint cible : `BilansMensuels.was_lief_gut`

### 6.6 Question 4 - Where I need support

- Type : **Multiple lines of text**
- Titre : `Where do you need support?`
- Description : `(optional) In which areas would you welcome help or support - from your advisor or otherwise?`
- Placeholder : `Your answer here...`
- Obligatoire : **No**
- Colonne SharePoint cible : `BilansMensuels.wo_brauche_ich_unterstuetzung`

### 6.7 Question 5 - Topics for the next session

- Type : **Multiple lines of text**
- Titre : `What topics would you like to discuss at the next session?`
- Description : `(optional) What is particularly important to you for your next conversation?`
- Placeholder : `Your answer here...`
- Obligatoire : **No**
- Colonne SharePoint cible : `BilansMensuels.themen_naechster_termin`

### 6.8 Question 6 - Additional remarks

- Type : **Multiple lines of text**
- Titre : `Any other remarks?`
- Description : `(optional) Is there anything else you would like to share that is not covered above?`
- Placeholder : `Your answer here...`
- Obligatoire : **No**
- Colonne SharePoint cible : `BilansMensuels.sonstige_anmerkungen`

### 6.9 Confirmation message

```
Thank you for your update. Your advisor will read it before your session.
We look forward to seeing you soon.
```

---

## 7. Configuration post-creation

Ces parametres s'appliquent a chacun des 4 formulaires.

### 7.1 Partage

Dans les parametres du formulaire (bouton "Teilen" / "Share") :

- Choisir "Jeder mit dem Link kann antworten" / "Anyone with the link can respond"
- Ne pas cocher "Nur Personen in meiner Organisation" - les participants n'ont pas necessairement un compte M365

### 7.2 Anonymat

- Desactiver l'enregistrement du nom Microsoft 365 du repondant
- Dans Parametres : decocher "Antworten aufzeichnen" / "Record name"
- Raison : les participants n'ont pas de compte M365, et le DSGVO impose la minimisation des donnees

### 7.3 Langue d'interface

- Form 1 et 3 : Sprache = Deutsch
- Form 2 et 4 : Language = English
- Regler dans Parametres du formulaire > Langue

### 7.4 Limite de soumissions

- Ne pas cocher "Nur eine Antwort pro Person" / "One response per person"
- Le Flow genere un lien unique par invitation. La limitation de reponses est geree par le Flow, pas par Forms.

---

## 8. Integration avec Power Automate

Apres creation des 4 formulaires :

1. Recuperer l'URL de chaque formulaire depuis le bouton "Teilen" > "Link zum Teilen"
2. Ces URLs sont configurees comme variables dans les deux Flows :
   - `varFormUrlDE` : URL du Form 3 (bilan mensuel DE)
   - `varFormUrlEN` : URL du Form 4 (bilan mensuel EN)
3. Les formulaires d'onboarding (Form 1 et 2) ne sont pas envoyes automatiquement.
   Leur lien est communique manuellement par la conseillere en debut de parcours.
4. Les reponses sont recuperees via le connecteur "Microsoft Forms" dans Power Automate,
   pas via export Excel manuel.

Pour le detail de la configuration des Flows, voir :
- `power_automate/Flow_1_Invitation_J-5.md`
- `power_automate/Flow_2_Generation_PDF.md`
