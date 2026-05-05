# Transfer Mappe Template DE - Specification de construction

Ce fichier documente exactement le contenu et la mise en page du template Word allemand
`transfer_mappe_template_de.docx` a construire manuellement dans Microsoft Word.

Pour la liste exhaustive des Content Controls et Tag values, voir :
`specs/word_template_structure.md`

Pour les instructions de construction dans Word, voir la section
"Instructions de construction du .docx" dans `specs/word_template_structure.md`.

---

## Metadonnees du fichier

- **Nom du fichier** : `transfer_mappe_template_de.docx`
- **Format** : Office Open XML (.docx), Word 2016 ou superieur
- **Langue du document** : Deutsch (de-DE)
- **Mise en page** : A4 portrait, marges 2.5 cm
- **A stocker dans SharePoint** : `/sites/TransferMappe/Templates/transfer_mappe_template_de.docx`

---

## Page de garde

**Contenu (de haut en bas) :**

```
[Logo de la societe - image placee manuellement par l'administrateur]
[Espace vertical]

TRANSFER MAPPE
[Content Control : doc_titre - Plain Text]

[Filet horizontal bleu #003DA5, epaisseur 2pt]

Teilnehmer/in :    [Content Control : participant_prenom] [Content Control : participant_nom]
Beraterin :        [Content Control : conseillere_nom]
Beginn :           [Content Control : participant_date_debut]
Erstellt am :      [Content Control : doc_date_generation]

[Espace vertical]
[Pied de page de garde - mention de confidentialite]
Vertraulich - Nur für den internen Gebrauch
```

**Styles appliques :**
- "TRANSFER MAPPE" : Heading 1, centre, 24pt, #003DA5, majuscules
- Labels ("Teilnehmer/in :", etc.) : Normal, gras
- Valeurs (Content Controls) : Normal, non gras

---

## Section 1 : Karriereprofil

**Titre de section :** `1. Karriereprofil` (Heading 1)

**Sous-titre :** `Berufliche Zielsetzung` (Heading 2)

**Contenu :**

```
Plan A - Berufliches Hauptziel
[Content Control : profil_plan_a]

Plan B - Berufliches Alternativziel
[Content Control : profil_plan_b]

Berufliches Profil und Stärken (Marketingplan)
[Content Control : profil_marketingplan]

Zielmarkt
[Content Control : profil_zielmarkt]
```

**Comportement si profil non rempli :**
Le Flow injecte "Nicht angegeben" dans chaque Content Control vide.
La section reste visible dans le PDF.

**Saut de page** apres la section Karriereprofil.

---

## Sections 2 a 13 : Monatsberichte (Bilans mensuels 01 a 12)

Chaque section est identique en structure. Remplacer `NN` par `01`, `02`, ..., `12`.

**Titre de section :** `Monatsbericht NN` (Heading 1)

**Contenu :**

```
Termin :           [Content Control : bilan_NN_date_rdv]
Eingereicht am :   [Content Control : bilan_NN_date_soumission]

Monatlicher Rückblick *
[Content Control : bilan_NN_bilan_general]

Stand der vereinbarten Ziele
[Content Control : bilan_NN_statut_objectifs]
[Content Control : bilan_NN_statut_objectifs_detail]

Was lief gut?
[Content Control : bilan_NN_was_lief_gut]

Wo brauche ich Unterstützung?
[Content Control : bilan_NN_wo_brauche_ich]

Themen für den nächsten Termin
[Content Control : bilan_NN_themen_naechster_termin]

Sonstige Anmerkungen
[Content Control : bilan_NN_sonstige_anmerkungen]
```

**Bloc Zielvereinbarung / Unterschriften (zone fixe, pas de Content Control) :**

```
[Filet horizontal gris #cccccc]

Zielvereinbarung - Unterschriften

Datum : .............................

Teilnehmer/in :                             Beraterin :

_________________________________           _________________________________
[Content Control : participant_prenom]      [Content Control : conseillere_nom]
[Content Control : participant_nom]
```

Note : les lignes de signature sont des bordures de paragraphe (bas), pas des underscores texte.
Note : `participant_prenom`, `participant_nom`, `conseillere_nom` sont les memes Content Controls que sur la page de garde. Word autorise plusieurs instances du meme Tag value dans un document - toutes seront remplies par la meme valeur par Power Automate.

**Saut de page** apres chaque section bilan (sauf la derniere).

---

## Pied de page global (toutes pages sauf page de garde)

```
Transfer Mappe | [Content Control : participant_prenom] [Content Control : participant_nom] | Vertraulich
                                                                              Page X sur Y
```

Note : le numero de page (X sur Y) est un champ Word natif (`{ PAGE }` et `{ NUMPAGES }`), pas un Content Control.

---

## Styles de mise en forme

| Element                        | Police      | Taille | Couleur  | Graisse | Alignement |
|--------------------------------|-------------|--------|----------|---------|------------|
| Titre principal (page de garde)| Calibri     | 24pt   | #003DA5  | Gras    | Centre     |
| Heading 1 (titres de section)  | Calibri     | 16pt   | #003DA5  | Gras    | Gauche     |
| Heading 2 (sous-titres)        | Calibri     | 13pt   | #003DA5  | Gras    | Gauche     |
| Labels de champs               | Calibri     | 11pt   | #333333  | Gras    | Gauche     |
| Contenu (Content Controls)     | Calibri     | 11pt   | #333333  | Normal  | Gauche     |
| Texte signature                | Calibri     | 10pt   | #666666  | Normal  | Gauche     |
| Pied de page                   | Calibri     | 9pt    | #999999  | Normal  | Justifie   |

**Couleur d'accent** : #003DA5 (bleu corporate, identique a la Transfer Mappe 10k Beratung)
**Couleur texte principal** : #333333 (gris fonce, evite le noir pur pour la lisibilite)

---

## Checklist de validation avant depot dans SharePoint

- [ ] Tous les 118 Content Controls sont presents (6 page de garde + 4 profil + 108 bilans)
- [ ] Chaque Content Control est de type "Plain Text" (pas Rich Text, pas Date Picker)
- [ ] Chaque Tag value correspond exactement a la liste dans `specs/word_template_structure.md`
- [ ] Le document s'ouvre sans erreur dans Word Online (tester via SharePoint)
- [ ] L'action "Populate a Microsoft Word template" dans Power Automate detecte bien tous les champs
- [ ] Un test de generation avec des donnees fictives produit un PDF lisible
- [ ] Les blocs signature sont visibles et correctement places en bas de chaque section bilan
