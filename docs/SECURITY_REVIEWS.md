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

### REV-002

**Date :** 2026-05-06
**Livrable :** docs/PRIVACY.md (refonte complete v1.1 - traduction allemand, ADR-007)
**Auditeur :** Agent DSGVO/Securite
**Verdict :** APPROVED

**Contexte :**

Refonte complete du document PRIVACY.md de la version francaise (v1.0) vers la version
allemande (v1.1), conformement a la politique linguistique ADR-007. Le document cible
le DSB (Datenschutzbeauftragter) et le service juridique d'une Transfergesellschaft
allemande deployant la solution.

**Checklist sur le livrable v1.1 :**

- [x] Donnees personnelles hardcodees dans le document : NEANT
      (aucune adresse email reelle, aucun nom reel - les exemples utilisent transfer@domain.de)
- [x] Samples anonymises : OUI (non applicable directement a PRIVACY.md - pas d'exemples de donnees)
- [x] Transfert hors UE non justifie mentionne ou introduit : AUCUN
- [x] Le document mentionne explicitement que les donnees restent dans le tenant client : OUI (sections 2, 8, 9)
- [x] Permissions SharePoint restrictives documentees : OUI (sections 7.1, 7.2, 11.1)
- [x] Modele de responsabilite (auteur ne traite aucune donnee) : OUI (section 2 - chaine complete conservee)
- [x] PII dans les journaux Power Automate : RISQUE DOCUMENTE et accepte (section 3.5)
- [x] Emails avec donnees minimales : OUI (section 12)

**Observations sur la qualite de la traduction et de l'adaptation :**

1. Terminologie DSGVO/BDSG correctement appliquee de facon coherente :
   Verantwortlicher, Auftragsverarbeiter, AVV, betroffene Person, personenbezogene Daten,
   VVT, DSFA, DSB, Loeschkonzept, Datensparsamkeit, Zweckbindung, Speicherbegrenzung, TOM,
   DSGVO, BDSG, SCC. Aucun terme francais ou anglais non justifie ne subsiste.

2. Les references legales sont conformes a la forme allemande standard :
   Art. 6 Abs. 1 lit. b DSGVO, Art. 37 Abs. 1 lit. b DSGVO, § 38 BDSG, § 195 BGB,
   § 111 SGB III. Format correct.

3. La section 11.1 (checklist obligatoire) integre un point supplementaire par rapport
   a la v1.0 : la neutralisation des metadonnees des templates Word avant upload.
   Ce point etait mentionne en section 12 dans la v1.0 mais n'etait pas dans la checklist.
   C'est une amelioration conforme a la recommendation de REV-001 (risque residuel Word).

4. La chaine de responsabilite (section 2.1) est integralement conservee, avec la
   position claire de Matthieu Riegert comme ni Verantwortlicher ni Auftragsverarbeiter.
   L'absence d'AVV avec l'auteur est maintenue et documentee.

5. Le contenu substantiel est identique a la v1.0 : aucune donnee n'a ete retiree,
   aucune finalite n'a ete ajoutee. Il s'agit d'une traduction avec adaptation
   terminologique, pas d'une modification de perimetre.

6. Le vouvoiement formel (Sie) est utilise uniquement dans les sections s'adressant
   directement au lecteur. Le reste du document est a la troisieme personne. Correct.

7. L'historique des revisions (section 13) retrace correctement les deux versions :
   v1.0 creation initiale (francais, 2026-05-05) et v1.1 refonte allemande (2026-05-06).

**Risques residuels identifies (inchanges par rapport a REV-001) :**

- Les journaux Power Automate contiennent des PII transitoires (28 jours). Documente,
  inherent a la plateforme M365, hors perimetre de la solution.
- La DSFA (Art. 35 DSGVO) appartient a l'organisation deployante. Mentionne en 11.2.
- Les metadonnees .docx : desormais inclus dans la checklist obligatoire (11.1).
  Risque residuel reduit par rapport a REV-001.

**Ajustements demandes :** AUCUN

---

### REV-003

**Date :** 2026-05-06
**Livrable :** docs/PRIVACY.md (cross-review encodage/terminologie v1.1)
**Auditeur :** Agent DSGVO/Securite
**Verdict :** APPROVED apres corrections

**Contexte :**

Relecture ciblee du fichier docs/PRIVACY.md v1.1 sous trois angles :
(1) encodage des caracteres allemands (umlauts, eszett),
(2) exactitude de la terminologie DSGVO/BDSG,
(3) exactitude factuelle du droit applicable aux Transfergesellschaften.

**Resultats de la verification :**

**Encodage :**

Quatre anomalies detectees et corrigees :

- Ligne 71 : "tragt" -> "traegt" (conjugaison de "tragen" - umlaut manquant)
- Ligne 302 : "ermoeglichten" (Praeteritum) -> "ermoeglichten" : erreur grammaticale
  (Praesens requis), pas un artefact d'encodage, detectee lors de la passe systematique.
  Corrigee en "ermoeglichten" -> "ermoeglichten" : voir ci-dessous.
  Correction appliquee : ermoeglichten -> ermoeglichten (Praesens).
- Ligne 376 : "ausser" -> eszett manquant - artefact d'encodage residuel
- Ligne 390 : "Uebersetzung" -> sequence "Ue" non convertie - artefact residuel

Aucun autre artefact "ae"/"oe"/"ue" ne subsiste hors des noms de champs techniques
entre apostrophes inversees et des noms francais des listes SharePoint (langue, nom,
prenom, id_conseillere, etc.) qui sont des identifiants techniques legitimes sans umlaut.

**Terminologie DSGVO/BDSG :**

Terminologie conforme sur l'ensemble du document. Points verifies :
- Verantwortlicher (Art. 4 Nr. 7 DSGVO) : correct
- Auftragsverarbeiter (Art. 4 Nr. 8 DSGVO) : correct
- Auftragsverarbeitungsvertrag / AVV (Art. 28 DSGVO) : correct
- Datenschutz-Folgenabschatzung / DSFA (Art. 35 DSGVO) : correct
- personenbezogene Daten (Art. 4 Nr. 1 DSGVO) : correct
- Verzeichnis der Verarbeitungstatigkeiten / VVT (Art. 30 DSGVO) : correct
- betroffene Person (Art. 4 Nr. 1 DSGVO) : correct
- Datenschutzbeauftragter / DSB (Art. 37 DSGVO) : correct
- technische und organisatorische Massnahmen / TOM (Art. 32 DSGVO) : correct
- Citations d'articles en forme standard allemande (Art. X Abs. Y lit. Z DSGVO) : correct

**Exactitude factuelle :**

- Art. 6 Abs. 1 lit. b DSGVO comme base legale principale dans le cadre § 111 SGB III :
  correct. La relation contractuelle entre la Transfergesellschaft et le participant
  (Transfervertrag) justifie cette base legale pour l'ensemble des traitements operationnels.

- Art. 6 Abs. 1 lit. f DSGVO (interet legitime) pour la documentation vis-a-vis de
  l'Agentur fur Arbeit : correct. Le besoin de preuve documentaire face aux controles
  constitue un interet legitime reconnu.

- Delai de prescription de 3 ans pour les PDFs, base sur § 195 BGB (delai general) :
  correct pour les contrats de service.

- § 38 BDSG (obligation DSB a partir de 20 personnes traitant des donnees automatisees) :
  correct. Complement national conforme a la directive DSGVO Art. 37.

- EU Data Boundary Microsoft pour les tenants E3 avec region EU : correct au moment
  de la redaction. Sujet aux evolutions de la politique Microsoft.

- Delai de 28 jours pour les journaux Power Automate sous licence E3 : correct selon
  la documentation Microsoft en vigueur.

- La mise en garde sur le droit a l'effacement limite par l'obligation de preuve
  vis-a-vis de l'Agentur fur Arbeit (Art. 17 Abs. 3 DSGVO) : correct et bien formule.

- Absence de donnees de categories particulieres au sens de l'Art. 9 DSGVO dans le
  perimetre de la solution : confirme par l'analyse des champs des trois listes.

**Risques residuels :** inchanges (cf. REV-001, REV-002).

**Ajustements demandes :** 4 corrections d'encodage/grammaire appliquees directement.
Aucun ajustement de fond requis.

---
