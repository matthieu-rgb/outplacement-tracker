# ASSUMPTIONS.md

Hypotheses metier prises pour le projet `outplacement-tracker` v0.1.

L'auteur n'a pas eu d'acces direct a l'equipe metier d'une Transfergesellschaft pour valider en detail les specifications. Les hypotheses ci-dessous ont ete prises sur la base :

- De la lecture attentive de la "Transfer Mappe" v2026 V1 de 10 k Beratung GmbH
- Du cadre legal allemand des Transfergesellschaften (§ 111 SGB III)
- Des pratiques observees dans le secteur de l'outplacement en Allemagne

Toute societe deployant cette solution est invitee a valider et ajuster ces hypotheses selon ses propres pratiques. La solution est suffisamment souple pour le permettre.

---

## A1 : Duree maximale d'un parcours

**Hypothese** : 12 mois maximum.

**Source** : § 111 SGB III, qui plafonne la duree legale d'une Transfergesellschaft a 12 mois.

**Impact** : le template Word et les Power Automate Flows sont dimensionnes pour empiler jusqu'a 12 bilans mensuels.

**Ajustable** : oui, en modifiant la limite dans le template Word et la boucle Power Automate.

---

## A2 : Frequence des rendez-vous

**Hypothese** : un rendez-vous par mois entre le participant et la conseillere.

**Source** : pratique standard observee dans le secteur, coherent avec la duree d'un parcours typique.

**Impact** : le formulaire de bilan est envoye une fois par mois, 5 jours avant le RDV.

**Ajustable** : oui, en modifiant le declencheur du Power Automate Flow d'invitation et la liste des dates de RDV dans SharePoint.

---

## A3 : Nature du suivi mensuel

**Hypothese** : le suivi mensuel est principalement declaratif et libre. Le participant resume ce qu'il souhaite partager. Aucun tracker obligatoire de candidatures ou de contacts.

**Source** : la Transfer Mappe d'origine precise explicitement que le document appartient au participant. La relation conseillere-participant repose sur la confiance, pas sur la surveillance.

**Impact** : le formulaire mensuel comporte 6 champs dont 5 sont optionnels.

**Ajustable** : oui, en ajoutant ou retirant des champs dans le Microsoft Forms.

---

## A4 : Signatures sur les Zielvereinbarungen

**Hypothese** : les signatures restent manuscrites. Le PDF cumulatif contient des emplacements de signature vides, le document est imprime, signe et scanne au RDV.

**Source** : signatures manuscrites legalement suffisantes pour ce type de document interne en Allemagne. Decision retenue par sobriete (pas de licence eSign premium).

**Impact** : aucun connecteur premium requis, pas de DocuSign ou Adobe Sign.

**Ajustable** : oui, une evolution vers eSign est documentee dans `BACKLOG.md` pour la v0.2.

---

## A5 : Volume cible

**Hypothese** : la solution est dimensionnee pour 1 500 a 2 000 participants suivis simultanement par une societe de reclassement.

**Source** : volume mentionne par l'utilisateur initial du projet.

**Impact** : ~75 a 100 envois d'emails par jour ouvre, largement compatible avec les limites Outlook (10 000 mails/jour).

**Ajustable** : oui, jusqu'a plusieurs dizaines de milliers de participants sans modification de l'architecture.

---

## A6 : Profil de l'administrateur deployeur

**Hypothese** : la societe de reclassement dispose d'un administrateur Microsoft 365 capable de :

- Creer des listes SharePoint (ou executer un script PowerShell PnP)
- Importer des Microsoft Forms
- Importer des Power Automate Flows
- Configurer les variables (boite mail expediteur, conseillere par defaut)

**Source** : profil standard d'un administrateur M365 en entreprise allemande.

**Impact** : la documentation `INSTALLATION.md` est ecrite a destination de ce profil, pas d'un utilisateur final.

**Ajustable** : non. Si l'administrateur n'a pas ces competences, la societe doit faire appel a un prestataire ou former en interne.

---

## A7 : Identite visuelle du PDF de sortie

**Hypothese** : la societe de reclassement souhaite que le PDF cumulatif respecte une identite visuelle proche de leur Transfer Mappe papier (sobre, bleu corporate, typo serif pour les titres).

**Source** : observation de la Transfer Mappe 10 k Beratung GmbH v2026 V1.

**Impact** : le template Word est concu avec un design sobre et personnalisable. Les couleurs et logos sont ajustables sans modifier l'architecture.

**Ajustable** : oui, le template Word est librement modifiable.

---

## A8 : Cadre RGPD/DSGVO

**Hypothese** : la societe de reclassement est responsable de traitement au sens du RGPD pour les donnees des participants. L'auteur du projet n'est ni responsable ni sous-traitant.

**Source** : la solution est livree comme un kit open source. L'auteur ne traite aucune donnee.

**Impact** : aucun AVV (Auftragsverarbeitungsvertrag) entre l'auteur et la societe de reclassement. La societe de reclassement assume integralement la responsabilite du traitement.

**Ajustable** : non. Si une societe souhaite externaliser le deploiement et l'exploitation, elle doit faire appel a un prestataire qui signera un AVV avec elle.
