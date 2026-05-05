# SharePoint Schema - outplacement-tracker v0.1

Schema des trois listes SharePoint constituant la base de donnees de la solution.

Conventions :
- Noms de listes : PascalCase
- Noms de colonnes : snake_case
- Types : notation Microsoft SharePoint (PnP PowerShell)
- Toutes les donnees restent dans le tenant client (ADR-001)

---

## Liste 1 : Participants

**Role** : une ligne par participant suivi. Table centrale, pivot de toute la solution.

**URL de la liste** : `{SiteURL}/Lists/Participants`

| Colonne              | Type SharePoint       | Obligatoire | Valeur par defaut  | Valeurs autorisees / Contraintes                         | Notes                                                      |
|----------------------|-----------------------|-------------|--------------------|---------------------------------------------------------|------------------------------------------------------------|
| `id`                 | ID (auto, built-in)   | oui (auto)  | -                  | Entier auto-incremente                                   | Cle primaire native SharePoint                             |
| `nom`                | Single line of text   | oui         | -                  | Max 255 caracteres                                       | Nom de famille                                             |
| `prenom`             | Single line of text   | oui         | -                  | Max 255 caracteres                                       | Prenom                                                     |
| `email`              | Single line of text   | oui         | -                  | Format email valide, max 255 caracteres                  | Adresse de contact unique par participant                  |
| `langue`             | Choice                | oui         | `DE`               | `DE` / `EN`                                             | Determine la langue des Forms, emails et template Word     |
| `id_conseillere`     | Single line of text   | oui         | -                  | Adresse email de la conseillere (compte M365)            | Utilisee pour router le PDF cumulatif                      |
| `date_debut_parcours`| Date and Time         | oui         | -                  | Date seule (pas d'heure), format ISO 8601               | Utilisee pour calculer la fin de parcours (max + 12 mois) |
| `date_prochain_rdv`  | Date and Time         | oui         | -                  | Date seule (pas d'heure), format ISO 8601               | Declencheur du Flow J-5 (invitation) et Flow J (PDF)       |
| `statut`             | Choice                | oui         | `actif`            | `actif` / `suspendu` / `termine`                        | `suspendu` = pause temporaire, `termine` = parcours clos   |
| `Title`              | Single line of text   | oui         | -                  | Format : "{prenom} {nom}"                               | Rempli automatiquement par le Flow a la creation. Sert de libelle lisible dans les vues SharePoint. |

**Index recommandes** :
- `email` : index pour recherche rapide par le Flow
- `statut` : index pour filtrer les participants actifs
- `date_prochain_rdv` : index pour le declencheur planifie du Flow

**Remarque DSGVO** : `email` est une donnee personnelle directement identifiante. Sa collecte est justifiee par la finalite du traitement (envoi du formulaire mensuel). Aucun champ supplementaire identifiant n'est present (pas de numero de securite sociale, pas de date de naissance, pas de numero de dossier Agentur fuer Arbeit).

---

## Liste 2 : Profils

**Role** : profil de carriere optionnel, saisi une fois en debut de parcours via le Forms onboarding. Zero ou un profil par participant.

**URL de la liste** : `{SiteURL}/Lists/Profils`

| Colonne                | Type SharePoint       | Obligatoire | Valeur par defaut | Valeurs autorisees / Contraintes | Notes                                                                |
|------------------------|-----------------------|-------------|-------------------|---------------------------------|----------------------------------------------------------------------|
| `id`                   | ID (auto, built-in)   | oui (auto)  | -                 | Entier auto-incremente           | Cle primaire                                                         |
| `id_participant`       | Number                | oui         | -                 | Entier >= 1                     | Cle etrangere vers `Participants.id`                                 |
| `plan_a`               | Multiple lines of text| non         | -                 | Texte libre, max 3 000 car.     | Objectif professionnel principal (Berufliche Zielsetzung Plan A)     |
| `plan_b`               | Multiple lines of text| non         | -                 | Texte libre, max 3 000 car.     | Objectif professionnel alternatif (Plan B)                           |
| `marketingplan`        | Multiple lines of text| non         | -                 | Texte libre, max 3 000 car.     | Positionnement, competences cles, USP du participant                 |
| `zielmarkt`            | Multiple lines of text| non         | -                 | Texte libre, max 3 000 car.     | Region, branche, taille d'entreprise ciblee                          |
| `date_creation`        | Date and Time         | oui         | `[now]`           | Date + heure ISO 8601           | Renseignee automatiquement par le Flow onboarding                    |
| `date_modification`    | Date and Time         | non         | -                 | Date + heure ISO 8601           | Mis a jour si le participant re-soumet le formulaire onboarding      |
| `Title`                | Single line of text   | oui         | -                 | Format : "Profil - {prenom_participant} {nom_participant}" | Rempli automatiquement par le Flow a la creation. Sert de libelle lisible dans les vues SharePoint. |

**Index recommandes** :
- `id_participant` : index pour lookup depuis le Flow

**Remarque DSGVO** : les champs `plan_a`, `plan_b`, `marketingplan`, `zielmarkt` contiennent des informations sur les ambitions professionnelles du participant. La base legale est le consentement du participant (le formulaire est optionnel, ADR-003). Ces donnees n'ont pas vocation a etre partagees hors du binome participant-conseillere.

---

## Liste 3 : BilansMensuels

**Role** : un enregistrement par bilan soumis. Zero a 12 bilans par participant (ADR-004, A1).

**URL de la liste** : `{SiteURL}/Lists/BilansMensuels`

| Colonne                          | Type SharePoint       | Obligatoire | Valeur par defaut | Valeurs autorisees / Contraintes                                                         | Notes                                                                  |
|----------------------------------|-----------------------|-------------|-------------------|-----------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| `id`                             | ID (auto, built-in)   | oui (auto)  | -                 | Entier auto-incremente                                                                   | Cle primaire                                                           |
| `id_participant`                 | Number                | oui         | -                 | Entier >= 1                                                                              | Cle etrangere vers `Participants.id`                                   |
| `date_rdv`                       | Date and Time         | oui         | -                 | Date seule ISO 8601                                                                      | Date du RDV auquel ce bilan est rattache                               |
| `date_soumission`                | Date and Time         | oui         | `[now]`           | Date + heure ISO 8601                                                                    | Renseignee automatiquement par le Flow au moment de la soumission Forms |
| `bilan_general`                  | Multiple lines of text| oui         | -                 | Texte libre, max 5 000 car.                                                             | Seul champ obligatoire (ADR-003). Resume libre du mois ecoule.         |
| `statut_objectifs`               | Choice                | non         | -                 | `vollstaendig_erreicht` / `teilweise_erreicht` / `nicht_erreicht` / `noch_nicht_relevant`| Statut des objectifs du mois precedent                                 |
| `statut_objectifs_detail`        | Multiple lines of text| non         | -                 | Texte libre, max 3 000 car.                                                             | Precisions libres sur le statut des objectifs                          |
| `was_lief_gut`                   | Multiple lines of text| non         | -                 | Texte libre, max 3 000 car.                                                             | Ce qui a bien fonctionne dans le mois                                  |
| `wo_brauche_ich_unterstuetzung`  | Multiple lines of text| non         | -                 | Texte libre, max 3 000 car.                                                             | Points sur lesquels le participant souhaite un soutien                 |
| `themen_naechster_termin`        | Multiple lines of text| non         | -                 | Texte libre, max 3 000 car.                                                             | Sujets a aborder au prochain RDV                                       |
| `sonstige_anmerkungen`           | Multiple lines of text| non         | -                 | Texte libre, max 3 000 car.                                                             | Remarques diverses                                                     |
| `Title`                          | Single line of text   | oui         | -                 | Format : "{date_rdv_ISO} - {prenom_participant} {nom_participant}", date au format YYYY-MM-DD pour garantir le tri lexicographique dans les vues SharePoint | Rempli automatiquement par le Flow a la creation. Sert de libelle lisible dans les vues SharePoint. |

**Index recommandes** :
- `id_participant` : index pour lookup depuis le Flow
- `date_rdv` : index pour tri chronologique lors de la generation du PDF

**Remarque DSGVO** : les bilans mensuels contiennent des donnees personnelles sensibles relatives a la situation professionnelle (et potentiellement personnelle) du participant. Base legale : execution du contrat de suivi en Transfergesellschaft. La liste n'est accessible qu'aux comptes M365 autorises par l'administrateur. Aucun partage externe prevu.

---

## Relations entre listes

```
Participants (id)
    |
    +-- 0..1 Profils (id_participant = Participants.id)
    |
    +-- 0..12 BilansMensuels (id_participant = Participants.id)
```

Note : SharePoint Online ne supporte pas les cles etrangeres natives avec contraintes d'integrite referentielle. Les relations sont gerees par les Power Automate Flows, qui verifient l'existence du `id_participant` avant insertion. En cas d'erreur, le Flow s'arrete et envoie une notification a l'administrateur.

---

## Parametres de site recommandes

- **Type de site** : SharePoint Communication Site ou Team Site dedie (pas le site racine)
- **Acces** : restreint aux membres de l'equipe (conseilleres + administrateur). Les participants n'ont pas acces direct au site.
- **Versioning** : activer le versioning des listes (5 versions minimum) pour audit trail
- **Audit** : activer les logs d'audit SharePoint (lecture et ecriture) pour conformite DSGVO
- **Retention** : a definir par la societe de reclassement selon leurs obligations legales (DSGVO + § 111 SGB III)
