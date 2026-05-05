# Samples - outplacement-tracker v0.1

Ce dossier contient des documents d'exemple generes avec des donnees fictives
et anonymisees a des fins de demonstration.

## Fichiers disponibles

| Fichier | Description |
|---|---|
| `sample_pdf_output_de.pdf` | PDF cumulatif DE - Max Mustermann - 3 mois fictifs |
| `sample_pdf_output_en.pdf` | PDF cumulatif EN - John Doe - 3 mois fictifs |
| `sample_output_de.docx` | Document Word source (DE) avant conversion |
| `sample_output_en.docx` | Document Word source (EN) avant conversion |
| `build_samples.py` | Script Python de generation |

## Donnees fictives

Toutes les donnees sont integralement fictives. Aucune personne reelle n'est representee.

**Participant DE :** Max Mustermann, Beraterin Maria Schmidt
**Participant EN :** John Doe, Advisor Maria Schmidt

Trois mois de bilans sont inclus (janvier a mars 2026). Les sections bilan 04 a 12
sont vides, illustrant le comportement du template pour les mois non encore soumis.

## Regenerer les samples

Prerequis : python-docx installe, LibreOffice present sur la machine.

```bash
cd /chemin/vers/outplacement-tracker
python3 samples/build_samples.py
```

Sur une machine sans LibreOffice, le script produit les .docx mais pas les PDF.
Ouvrir les .docx dans Microsoft Word et exporter en PDF manuellement.

## Note DSGVO

Ces fichiers ne contiennent aucune donnee personnelle reelle.
Les noms "Max Mustermann" et "John Doe" sont des noms generiques conventionnels
utilises comme donnees de demonstration dans le contexte germanique et anglosaxon.
Aucune adresse email, numero de dossier ou information identifiante reelle n'est presente.
