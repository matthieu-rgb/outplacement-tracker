# outplacement-tracker

> Solution cle-en-main basee sur Microsoft 365 pour digitaliser le suivi mensuel des participants en Transfergesellschaft, en preservant la dimension humaine de la relation participant-conseiller.

## Le contexte

Les societes de reclassement allemandes (Transfergesellschaften) accompagnent les participants pendant 6 a 12 mois via des rendez-vous mensuels avec un conseiller. Le suivi se fait souvent dans une "Transfer Mappe" papier ou un PDF a remplir manuellement, peu adaptee au flux numerique d'aujourd'hui.

Cette solution propose une alternative legere : un formulaire mensuel envoye 5 jours avant chaque RDV, un PDF cumulatif genere automatiquement le matin du rendez-vous, le tout sans flicage et sans saisie obligatoire de chaque action.

## Le principe

```
J-5 avant RDV    -> le participant recoit un mail avec un lien Forms
                    et y resume librement son mois
                    
Jour J du RDV    -> la conseillere recoit un PDF cumulatif avec
                    l'historique complet du participant et le
                    bilan du mois ecoule
```

Six champs dans le formulaire mensuel, un seul obligatoire. Le participant decide de ce qu'il partage. La conseillere arrive preparee. Le PDF appartient au participant.

## Stack technique

- **Microsoft Forms** pour les formulaires (DE et EN)
- **SharePoint** pour la base de donnees et les listes
- **Power Automate** pour l'orchestration (envoi J-5 + generation PDF)
- **Word template** pour le rendu du PDF cumulatif
- **Outlook** pour l'envoi des notifications

Tout reste dans le tenant Microsoft 365 du client. Aucune donnee ne sort. Compatible plan E3 standard, sans connecteur premium.

## Pour deployer

Voir `docs/INSTALLATION.md` (genere au sprint 3).

Resume :
1. Importer le schema SharePoint via le script PowerShell PnP
2. Importer les deux Microsoft Forms
3. Importer les deux Power Automate Flows
4. Deposer le template Word dans SharePoint
5. Ajuster les variables (boite mail expediteur, conseillere par defaut)

Temps de deploiement estime : 1 a 2 heures pour un administrateur Microsoft 365.

## Pour les developpeurs

Le projet utilise une architecture en sub-agents specialises pour Claude Code. Voir `.claude/agents/` pour les definitions de chaque role.

```bash
# A la racine du repo
claude
> demarre le sprint 1
```

Le Tech Lead orchestrera le travail, deleguera aux specialistes, et reviendra vers toi pour validation.

## Statut

| Sprint | Objectif | Statut |
|--------|----------|--------|
| 1 | Fondations metier (schemas, templates, contenus) | A demarrer |
| 2 | Automatisation (Power Automate, scripts setup) | A venir |
| 3 | Documentation et livrables (PITCH.pdf, INSTALLATION.md) | A venir |

## Licence

MIT. Libre d'utilisation, modification et redistribution.

## Auteur

Matthieu Riegert ([@matthieu-rgb](https://github.com/matthieu-rgb)) - 2026

Projet personnel, livre sans garantie ni engagement de support.
