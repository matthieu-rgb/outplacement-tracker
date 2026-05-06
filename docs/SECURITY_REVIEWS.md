# SECURITY_REVIEWS.md

Journal append-only des revues de securite et de conformite DSGVO du projet outplacement-tracker.

Chaque entree est definitive. Ne pas modifier les entrees existantes.
Pour corriger une evaluation anterieure, ajouter une nouvelle entree.

---

## Entrees

---

### REV-001

**Date :** 2026-05-05
**Livrable :** docs/PRIVACY.md (creation initiale v1.0)
**Auditeur :** Agent DSGVO/Securite
**Verdict :** APPROVED

**Checklist :**

- [x] Donnees personnelles hardcodees dans le code, la doc, ou les exemples : NEANT
      (samples utilises Max Mustermann / John Doe, confirme dans samples/README.md)
- [x] Samples anonymises : OUI (Max Mustermann DE, John Doe EN, Maria Schmidt pour conseillere)
- [x] Transfert hors UE non justifie : AUCUN (architecture 100% tenant client M365)
- [x] La doc mentionne explicitement que les donnees restent dans le tenant client : OUI (sections 2, 8, 9)
- [x] Permissions SharePoint restrictives par defaut documentees : OUI (section 7.2 et checklist 11.1)
- [x] Modele de responsabilite documente (auteur ne traite aucune donnee) : OUI (section 2 - chaine complete)
- [x] Flows Power Automate - PII dans les journaux : RISQUE DOCUMENTE et accepte (section 3.5 - journaux 28j Microsoft)
- [x] Emails avec donnees minimales : OUI (section 12 - analyse detaillee des templates email)

**Observations :**

1. La chaine de responsabilite (section 2) est conforme au modele attendu. L'auteur est
   clairement exclu de la chaine de traitement. L'absence d'AVV auteur/deployeur est justifiee
   et documentee.

2. La base legale Art. 6(1)(b) DSGVO retenue pour tous les champs est correcte dans
   le cadre SGB III. La non-utilisation du consentement comme base legale principale
   est explicitement justifiee (section 4.3) - approche rigoureuse.

3. Le traitement des journaux Power Automate (section 3.5) contient une observation
   importante : ces journaux peuvent contenir des PII (nom, email de participants).
   Ce point est documente et acceptable car il est inherent a la plateforme M365
   et les journaux restent dans le tenant. L'organisation est invitee a restreindre
   l'acces au portail Power Automate (section 7.2).

4. La mention de l'EU Data Boundary (section 9.1) est correcte pour les licences
   M365 E3 avec region UE. La condition de verification de la region tenant
   est incluse dans la checklist (section 11.1) - point critique bien traite.

5. La probabilite de l'obligation de DPD pour les Transfergesellschaften est
   correctement arguee (Art. 37 DSGVO + § 38 BDSG) sans certitude absolue,
   ce qui est la position juridiquement honnete.

6. La procedure de suppression (section 5.2) propose trois options dont une automatisee
   non encore livree (BACKLOG). Cette transparence est correcte.

**Risques residuels identifies (acceptes) :**

- Les journaux Power Automate contiennent des PII transitoires. Risque inherent a la
  plateforme, hors perimetre de la solution, documente.
- La DPIA (Art. 35) n'est pas realisee par l'auteur : c'est correct, elle appartient
  a l'organisation deployante. Elle est mentionnee dans la checklist (section 11.2).
- La metadonnee des fichiers .docx templates peut contenir le nom de l'auteur
  (proprietaire Word). Point signale en section 12 pour le deploiement.

**Ajustements demandes :** AUCUN

---
