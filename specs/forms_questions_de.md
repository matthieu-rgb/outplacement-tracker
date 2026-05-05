# Forms - Questions en allemand (DE)

Specification exacte des deux Microsoft Forms en version allemande.
Ces questions sont recopiees telles quelles dans Microsoft Forms lors du deploiement.

Conventions :
- Champ obligatoire signale par (*) dans le titre de la question
- Champs optionnels : pas d'asterisque
- Caracteres speciaux : ae = ae, oe = oe, ue = ue, ss = ss dans les noms de colonnes ; les umlauts sont utilises dans le texte visible par le participant
- Ordre des questions = ordre d'affichage dans le formulaire

---

## Form 1 : Onboarding - Profil de carriere (DE)

**Nom du formulaire** : Ihr Karriereprofil - Transfer Mappe

**Texte d'introduction** (affiche en haut du formulaire) :

> Dieser kurze Fragebogen hilft Ihrer Beraterin, Sie und Ihre Ziele besser zu verstehen.
> Die Angaben sind freiwillig - Sie entscheiden, was Sie teilen moechten. Sie koennen dieses Formular jederzeit erneut ausfullen, um Ihre Angaben zu aktualisieren.
> Alle Informationen bleiben vertraulich und werden ausschliesslich im Rahmen Ihrer Begleitung verwendet.

---

### Question 1 - Plan A : Berufliches Hauptziel

**Type** : Mehrzeiliger Text (Multiple lines of text)
**Obligatoire** : non
**Titre** : Ihr berufliches Hauptziel (Plan A)
**Description / sous-texte** : Welche berufliche Richtung moechten Sie anstreben? Welche Art von Stelle suchen Sie? In welcher Branche oder Region?
**Placeholder** : Beispiel: Projektmanager im Maschinenbau, Rhein-Saar-Region, Unternehmen ab 200 Mitarbeitern
**Colonne SharePoint cible** : `Profils.plan_a`

---

### Question 2 - Plan B : Berufliches Alternativziel

**Type** : Mehrzeiliger Text
**Obligatoire** : non
**Titre** : Ihr berufliches Alternativziel (Plan B)
**Description / sous-texte** : Falls Plan A nicht greift - welche alternative berufliche Richtung waere fuer Sie ebenfalls interessant?
**Placeholder** : Beispiel: Selbststandigkeit als Berater, oder Wechsel in den oeffentlichen Dienst
**Colonne SharePoint cible** : `Profils.plan_b`

---

### Question 3 - Marketingplan

**Type** : Mehrzeiliger Text
**Obligatoire** : non
**Titre** : Ihr berufliches Profil und Ihre Staerken
**Description / sous-texte** : Was sind Ihre zentralen Kompetenzen? Was macht Sie fuer Arbeitgeber besonders interessant? Welche Erfahrungen oder Qualifikationen heben Sie hervor?
**Placeholder** : Beispiel: 15 Jahre Erfahrung in der Fahrzeugelektronik, spezialisiert auf CAN-Bus und Diagnose, Fuehrungserfahrung mit Teams bis 8 Personen, Deutsch und Franzoesisch fliessend
**Colonne SharePoint cible** : `Profils.marketingplan`

---

### Question 4 - Zielmarkt

**Type** : Mehrzeiliger Text
**Obligatoire** : non
**Titre** : Ihr Zielmarkt
**Description / sous-texte** : In welchem Umfeld moechten Sie arbeiten? Denken Sie an Region, Branche, Unternehmensgroesse oder Unternehmenstyp.
**Placeholder** : Beispiel: Saarland / Lothringen / Luxemburg, Automobilindustrie oder Maschinenbau, mittelstaendische Unternehmen (100-500 Mitarbeiter)
**Colonne SharePoint cible** : `Profils.zielmarkt`

---

**Texte de confirmation** (affiche apres soumission) :

> Vielen Dank fuer Ihre Angaben. Ihr Karriereprofil wurde gespeichert und steht Ihrer Beraterin zur Verfuegung.
> Sie koennen dieses Formular jederzeit erneut ausfullen, um Ihre Angaben zu aktualisieren.

---

## Form 2 : Bilan mensuel (DE)

**Nom du formulaire** : Ihr monatlicher Bericht - Transfer Mappe

**Texte d'introduction** (affiche en haut du formulaire) :

> Bitte nehmen Sie sich 5 Minuten Zeit, um diesen kurzen Bericht vor Ihrem naechsten Beratungstermin auszufuellen.
> Nur die erste Frage ist Pflichtangabe. Alle anderen Felder sind freiwillig - Sie entscheiden, was Sie teilen moechten.
> Diese Informationen helfen Ihrer Beraterin, den Termin gezielt vorzubereiten.

---

### Question 1 - Bilan general (*)

**Type** : Mehrzeiliger Text
**Obligatoire** : oui
**Titre** : Wie war Ihr Monat? (*)
**Description / sous-texte** : Bitte beschreiben Sie kurz, wie der vergangene Monat verlaufen ist - beruflich und/oder persoenllich, was auch immer Ihnen wichtig erscheint.
**Placeholder** : Ihr Bericht hier...
**Colonne SharePoint cible** : `BilansMensuels.bilan_general`

---

### Question 2 - Statut des objectifs

**Type** : Choix (Choice) + complement texte libre

**Partie 2a - Choix**
**Obligatoire** : non
**Titre** : Wie stehen Sie bei den vereinbarten Zielen?
**Description / sous-texte** : Denken Sie an die Ziele, die Sie beim letzten Termin mit Ihrer Beraterin vereinbart haben.
**Options** (choix unique) :
- Vollstaendig erreicht
- Teilweise erreicht
- Nicht erreicht
- Noch nicht relevant
**Colonne SharePoint cible** : `BilansMensuels.statut_objectifs`
**Mapping valeurs** :
  - "Vollstaendig erreicht" -> `vollstaendig_erreicht`
  - "Teilweise erreicht" -> `teilweise_erreicht`
  - "Nicht erreicht" -> `nicht_erreicht`
  - "Noch nicht relevant" -> `noch_nicht_relevant`

**Partie 2b - Texte libre**
**Obligatoire** : non
**Titre** : Moechten Sie dazu etwas erlaeutern?
**Description / sous-texte** : (optional) Kurze Erklaerung oder Kontext zu Ihrer Antwort oben.
**Placeholder** : Ihre Erlaeuterung hier...
**Colonne SharePoint cible** : `BilansMensuels.statut_objectifs_detail`

---

### Question 3 - Was lief gut

**Type** : Mehrzeiliger Text
**Obligatoire** : non
**Titre** : Was lief in diesem Monat gut?
**Description / sous-texte** : (optional) Welche positiven Entwicklungen, Erfolge oder Fortschritte haben Sie erlebt?
**Placeholder** : Ihre Antwort hier...
**Colonne SharePoint cible** : `BilansMensuels.was_lief_gut`

---

### Question 4 - Wo brauche ich Unterstuetzung

**Type** : Mehrzeiliger Text
**Obligatoire** : non
**Titre** : Wo brauchen Sie Unterstuetzung?
**Description / sous-texte** : (optional) In welchen Bereichen wuerden Sie sich Hilfe oder Unterstuetzung wuenschen - von Ihrer Beraterin oder anderweitig?
**Placeholder** : Ihre Antwort hier...
**Colonne SharePoint cible** : `BilansMensuels.wo_brauche_ich_unterstuetzung`

---

### Question 5 - Themen fuer den naechsten Termin

**Type** : Mehrzeiliger Text
**Obligatoire** : non
**Titre** : Welche Themen moechten Sie beim naechsten Termin besprechen?
**Description / sous-texte** : (optional) Was liegt Ihnen besonders am Herzen fuer das naechste Gespraech?
**Placeholder** : Ihre Antwort hier...
**Colonne SharePoint cible** : `BilansMensuels.themen_naechster_termin`

---

### Question 6 - Sonstige Anmerkungen

**Type** : Mehrzeiliger Text
**Obligatoire** : non
**Titre** : Sonstige Anmerkungen
**Description / sous-texte** : (optional) Haben Sie noch etwas, das Sie mitteilen moechten und das oben nicht abgedeckt ist?
**Placeholder** : Ihre Antwort hier...
**Colonne SharePoint cible** : `BilansMensuels.sonstige_anmerkungen`

---

**Texte de confirmation** (affiche apres soumission) :

> Vielen Dank fuer Ihren Bericht. Ihre Beraterin wird diesen vor Ihrem Termin lesen.
> Wir freuen uns darauf, Sie bald zu sehen.

---

## Notes de configuration Forms

- **Partage** : "Jeder mit dem Link kann antworten" (lien genere par le Flow J-5, un lien par participant par mois)
- **Anonymat** : desactiver "Antworten aufzeichnen" pour le nom du compte Microsoft si les participants n'ont pas de compte M365 (formulaire accessible sans connexion)
- **Limite de soumissions** : 1 reponse par lien (Power Automate genere un lien unique par invitation)
- **Langue d'interface** : Deutsch
- **Export** : les reponses sont recuperees via le connecteur Microsoft Forms dans Power Automate, pas en export manuel Excel
