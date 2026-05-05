# Word Template Structure - Transfer Mappe v0.1

Specification complete du template Word pour la generation du PDF cumulatif.
Ce document est la reference pour :
- La construction manuelle du .docx dans Microsoft Word
- La creation des Content Controls avec leurs Tag values
- La configuration de l'action "Populate a Microsoft Word template" dans Power Automate

---

## Contexte technique

Power Automate (plan E3, sans premium) utilise l'action native **"Populate a Microsoft Word template"** du connecteur Word Online (Business). Cette action remplace les Content Controls du template par les valeurs injectees.

**Contraintes de compatibilite** :
- Seuls les Content Controls de type **Plain Text** (`<w:sdt>` avec `<w:tag w:val="..."/>`) sont supportes par cette action
- Les Content Controls de type Rich Text, Image, Date Picker ou Dropdown ne sont PAS injectes par Power Automate
- Le Tag value (`w:val`) est l'identifiant que Power Automate utilise pour la correspondance : il doit etre unique dans le document et exactement identique au nom de champ configure dans le Flow
- Les sections de bilan mensuel (repetees 1 a 12 fois) utilisent le mecanisme de boucle : chaque instance de bilan est injectee dans un Content Control distinct (bilan_01_, bilan_02_, etc.)

---

## Structure generale du document

```
[Page de garde]
  - Titre du document
  - Nom et prenom du participant
  - Date de debut du parcours
  - Conseillere responsable
  - Date de generation du PDF

[Section 1 : Profil de carriere]
  - Plan A
  - Plan B
  - Marketingplan
  - Zielmarkt
  - (Section affichee meme si vide, avec mention "Non renseigne")

[Section 2 : Zielvereinbarung - Bilan 01]
  - Date du RDV
  - Bilan general
  - Statut des objectifs
  - Statut des objectifs - detail
  - Was lief gut
  - Wo brauche ich Unterstuetzung
  - Themen naechster Termin
  - Sonstige Anmerkungen
  - [Bloc signature - emplacement vide manuscrit]

[Section 3 : Zielvereinbarung - Bilan 02]
  ... (meme structure)

[...]

[Section 13 : Zielvereinbarung - Bilan 12]
  ... (meme structure)

[Pied de page global]
  - Mention de confidentialite
  - Numero de page / total
```

---

## Inventaire complet des Content Controls

### Page de garde

| Tag value (w:val)         | Type       | Source SharePoint                        | Valeur si vide            |
|---------------------------|------------|------------------------------------------|---------------------------|
| `doc_titre`               | Plain Text | Fixe (DE : "Transfer Mappe", EN : "Transfer Portfolio") | - |
| `participant_prenom`      | Plain Text | `Participants.prenom`                    | -                         |
| `participant_nom`         | Plain Text | `Participants.nom`                       | -                         |
| `participant_date_debut`  | Plain Text | `Participants.date_debut_parcours` (DD.MM.YYYY) | -                   |
| `conseillere_nom`         | Plain Text | Derive de `Participants.id_conseillere` (nom affiche M365) | - |
| `doc_date_generation`     | Plain Text | Date du jour au moment du declenchement du Flow (DD.MM.YYYY) | - |

---

### Section Profil de carriere

| Tag value (w:val)         | Type       | Source SharePoint                        | Valeur si vide               |
|---------------------------|------------|------------------------------------------|------------------------------|
| `profil_plan_a`           | Plain Text | `Profils.plan_a`                         | DE: "Nicht angegeben" / EN: "Not provided" |
| `profil_plan_b`           | Plain Text | `Profils.plan_b`                         | DE: "Nicht angegeben" / EN: "Not provided" |
| `profil_marketingplan`    | Plain Text | `Profils.marketingplan`                  | DE: "Nicht angegeben" / EN: "Not provided" |
| `profil_zielmarkt`        | Plain Text | `Profils.zielmarkt`                      | DE: "Nicht angegeben" / EN: "Not provided" |

---

### Sections Bilan mensuel (repetees 12 fois)

Le prefixe `bilan_NN_` ou `NN` va de `01` a `12` identifie chaque bilan dans le document.
Power Automate injecte les bilans dans l'ordre chronologique croissant (`date_rdv` ASC).
Les sections correspondant a des bilans non encore soumis sont laissees vides ou masquees (voir note ci-dessous).

**Exemple pour le bilan 01 :**

| Tag value (w:val)                   | Type       | Source SharePoint                              | Valeur si vide / non soumis    |
|-------------------------------------|------------|------------------------------------------------|--------------------------------|
| `bilan_01_date_rdv`                 | Plain Text | `BilansMensuels.date_rdv` (DD.MM.YYYY)        | Laisser vide                   |
| `bilan_01_date_soumission`          | Plain Text | `BilansMensuels.date_soumission` (DD.MM.YYYY) | Laisser vide                   |
| `bilan_01_bilan_general`            | Plain Text | `BilansMensuels.bilan_general`                | Laisser vide                   |
| `bilan_01_statut_objectifs`         | Plain Text | `BilansMensuels.statut_objectifs` (libelle traduit) | Laisser vide             |
| `bilan_01_statut_objectifs_detail`  | Plain Text | `BilansMensuels.statut_objectifs_detail`      | Laisser vide                   |
| `bilan_01_was_lief_gut`             | Plain Text | `BilansMensuels.was_lief_gut`                 | Laisser vide                   |
| `bilan_01_wo_brauche_ich`           | Plain Text | `BilansMensuels.wo_brauche_ich_unterstuetzung`| Laisser vide                   | Note : Tag value abrege volontairement (max 64 car. recommande pour Power Automate) ; le Flow fait la correspondance |
| `bilan_01_themen_naechster_termin`  | Plain Text | `BilansMensuels.themen_naechster_termin`      | Laisser vide                   |
| `bilan_01_sonstige_anmerkungen`     | Plain Text | `BilansMensuels.sonstige_anmerkungen`         | Laisser vide                   |

**Meme structure pour bilans 02 a 12** (remplacer `01` par `02`, `03`, ..., `12`).

**Liste exhaustive de tous les Tag values des bilans :**

```
bilan_01_date_rdv               bilan_07_date_rdv
bilan_01_date_soumission        bilan_07_date_soumission
bilan_01_bilan_general          bilan_07_bilan_general
bilan_01_statut_objectifs       bilan_07_statut_objectifs
bilan_01_statut_objectifs_detail bilan_07_statut_objectifs_detail
bilan_01_was_lief_gut           bilan_07_was_lief_gut
bilan_01_wo_brauche_ich         bilan_07_wo_brauche_ich
bilan_01_themen_naechster_termin bilan_07_themen_naechster_termin
bilan_01_sonstige_anmerkungen   bilan_07_sonstige_anmerkungen

bilan_02_date_rdv               bilan_08_date_rdv
bilan_02_date_soumission        bilan_08_date_soumission
bilan_02_bilan_general          bilan_08_bilan_general
bilan_02_statut_objectifs       bilan_08_statut_objectifs
bilan_02_statut_objectifs_detail bilan_08_statut_objectifs_detail
bilan_02_was_lief_gut           bilan_08_was_lief_gut
bilan_02_wo_brauche_ich         bilan_08_wo_brauche_ich
bilan_02_themen_naechster_termin bilan_08_themen_naechster_termin
bilan_02_sonstige_anmerkungen   bilan_08_sonstige_anmerkungen

bilan_03_date_rdv               bilan_09_date_rdv
bilan_03_date_soumission        bilan_09_date_soumission
bilan_03_bilan_general          bilan_09_bilan_general
bilan_03_statut_objectifs       bilan_09_statut_objectifs
bilan_03_statut_objectifs_detail bilan_09_statut_objectifs_detail
bilan_03_was_lief_gut           bilan_09_was_lief_gut
bilan_03_wo_brauche_ich         bilan_09_wo_brauche_ich
bilan_03_themen_naechster_termin bilan_09_themen_naechster_termin
bilan_03_sonstige_anmerkungen   bilan_09_sonstige_anmerkungen

bilan_04_date_rdv               bilan_10_date_rdv
bilan_04_date_soumission        bilan_10_date_soumission
bilan_04_bilan_general          bilan_10_bilan_general
bilan_04_statut_objectifs       bilan_10_statut_objectifs
bilan_04_statut_objectifs_detail bilan_10_statut_objectifs_detail
bilan_04_was_lief_gut           bilan_10_was_lief_gut
bilan_04_wo_brauche_ich         bilan_10_wo_brauche_ich
bilan_04_themen_naechster_termin bilan_10_themen_naechster_termin
bilan_04_sonstige_anmerkungen   bilan_10_sonstige_anmerkungen

bilan_05_date_rdv               bilan_11_date_rdv
bilan_05_date_soumission        bilan_11_date_soumission
bilan_05_bilan_general          bilan_11_bilan_general
bilan_05_statut_objectifs       bilan_11_statut_objectifs
bilan_05_statut_objectifs_detail bilan_11_statut_objectifs_detail
bilan_05_was_lief_gut           bilan_11_was_lief_gut
bilan_05_wo_brauche_ich         bilan_11_wo_brauche_ich
bilan_05_themen_naechster_termin bilan_11_themen_naechster_termin
bilan_05_sonstige_anmerkungen   bilan_11_sonstige_anmerkungen

bilan_06_date_rdv               bilan_12_date_rdv
bilan_06_date_soumission        bilan_12_date_soumission
bilan_06_bilan_general          bilan_12_bilan_general
bilan_06_statut_objectifs       bilan_12_statut_objectifs
bilan_06_statut_objectifs_detail bilan_12_statut_objectifs_detail
bilan_06_was_lief_gut           bilan_12_was_lief_gut
bilan_06_wo_brauche_ich         bilan_12_wo_brauche_ich
bilan_06_themen_naechster_termin bilan_12_themen_naechster_termin
bilan_06_sonstige_anmerkungen   bilan_12_sonstige_anmerkungen
```

**Total Content Controls** : 6 (page de garde) + 4 (profil) + 108 (12 x 9 bilans) = **118 Content Controls**

---

### Bloc signature (dans chaque section bilan)

Le bloc signature n'est PAS un Content Control injecte par Power Automate. C'est une zone fixe du template Word, presente sur chaque page de bilan.

**Structure du bloc (en bas de chaque section bilan, dans le template) :**

```
Zielvereinbarung - Unterschriften

Datum: .......................

Teilnehmer/in:                          Beraterin:

_________________________________       _________________________________
{{participant_prenom}} {{participant_nom}}   {{conseillere_nom}}
```

Note : les lignes de signature sont dessinées avec un filet bas de paragraphe (bordure Word), pas avec des underscores en texte brut. Les noms sont injectes via Content Controls (`participant_prenom`, `participant_nom`, `conseillere_nom` - les memes que sur la page de garde, referencables plusieurs fois dans le document).

---

## Mapping statut_objectifs -> libelle affiche dans le PDF

Le Flow traduit le code interne SharePoint en libelle lisible avant injection dans le Content Control.

| Code SharePoint              | Libelle DE                | Libelle EN                |
|------------------------------|---------------------------|---------------------------|
| `vollstaendig_erreicht`      | Vollständig erreicht      | Fully achieved            |
| `teilweise_erreicht`         | Teilweise erreicht        | Partially achieved        |
| `nicht_erreicht`             | Nicht erreicht            | Not achieved              |
| `noch_nicht_relevant`        | Noch nicht relevant       | Not yet relevant          |
| (vide, non soumis)           | -                         | -                         |

---

## Instructions de construction du .docx dans Microsoft Word

### Etape 1 : Creer le fichier

1. Ouvrir Word, nouveau document vierge
2. Mettre en page : A4, marges 2.5 cm sur tous les cotes
3. Definir les styles :
   - "Heading 1" : Calibri 18pt, gras, couleur #003DA5 (bleu corporate)
   - "Heading 2" : Calibri 14pt, gras, couleur #003DA5
   - "Normal" : Calibri 11pt, couleur #333333, interligne 1.15
   - "SignatureLine" : style personnalise, pas de puces, bordure bas 0.5pt #666666

### Etape 2 : Inserer les Content Controls

Pour chaque Content Control :
1. Aller dans Ruban > Developpeur > Controls > "Plain Text Content Control" (Aa)
2. Cliquer sur "Properties" (icone cle)
3. Renseigner :
   - **Title** : libelle lisible (ex. "Bilan general - Mois 01")
   - **Tag** : valeur exacte du Tag value (ex. `bilan_01_bilan_general`)
4. Cocher "Remove content control when contents are edited" : NON
5. Style : "Normal" par defaut

### Etape 3 : Activer l'onglet Developpeur (si absent)

Fichier > Options > Personnaliser le Ruban > cocher "Developpeur"

### Etape 4 : Sauvegarder en format .docx

Fichier > Enregistrer sous > Format : "Document Word (.docx)"
Ne PAS sauvegarder en .doc (ancien format) ni en .dotx (template Word) - Power Automate requiert un .docx standard.

### Etape 5 : Deposer le fichier dans SharePoint

Le template doit etre stocke dans une bibliotheque SharePoint accessible par le compte de service Power Automate (ex. /sites/TransferMappe/Templates/transfer_mappe_template_de.docx).

---

## Structure XML de reference pour un Content Control (extrait)

Cet extrait XML montre la structure attendue dans le document .docx. Il est fourni a titre de reference pour validation ou construction programmatique.

```xml
<w:sdt>
  <w:sdtPr>
    <w:tag w:val="bilan_01_bilan_general"/>
    <w:alias w:val="Bilan general - Mois 01"/>
    <w:showingPlcHdr/>
    <w:text/>
  </w:sdtPr>
  <w:sdtContent>
    <w:p>
      <w:r>
        <w:rPr>
          <w:rStyle w:val="PlaceholderText"/>
        </w:rPr>
        <w:t>Bilan general du mois</w:t>
      </w:r>
    </w:p>
  </w:sdtContent>
</w:sdt>
```

---

## Notes importantes pour Power Automate

1. **Action a utiliser** : "Populate a Microsoft Word template" du connecteur "Word Online (Business)"
2. **Chemin du template** : pointer vers le .docx dans SharePoint (pas OneDrive)
3. **Champs dynamiques** : Power Automate detecte automatiquement tous les Content Controls du template et propose leurs Tag values comme champs a remplir dans l'action
4. **Champs vides** : si un champ n'est pas renseigne (bilan non soumis, profil vide), injecter une chaine vide `""` - ne jamais laisser le champ manquant dans l'action Power Automate
5. **Conversion PDF** : apres l'action "Populate", utiliser l'action "Convert Word Document to PDF" du meme connecteur Word Online (Business) - disponible en E3 sans premium
6. **Ordre des bilans** : trier les bilans par `date_rdv` ASC avant la boucle d'injection dans Power Automate
