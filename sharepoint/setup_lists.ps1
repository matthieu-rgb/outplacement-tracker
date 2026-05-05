<#
.SYNOPSIS
    Provisioning des listes SharePoint pour outplacement-tracker v0.1
.DESCRIPTION
    Cree les 3 listes SharePoint (Participants, Profils, BilansMensuels) et leurs colonnes.
    Idempotent : peut etre rejoue sans erreur si les listes existent deja.
.PARAMETER SiteUrl
    URL du site SharePoint cible (ex: https://contoso.sharepoint.com/sites/TransferMappe)
.EXAMPLE
    .\setup_lists.ps1 -SiteUrl "https://contoso.sharepoint.com/sites/TransferMappe"
.PREREQUIS
    Module PnP.PowerShell installe : Install-Module PnP.PowerShell -Force
    Connexion active : Connect-PnPOnline -Url $SiteUrl -Interactive
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$SiteUrl
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# -------------------------------------------------------
# Fonctions utilitaires
# -------------------------------------------------------

function Ensure-List {
    param(
        [string]$Title,
        [string]$Description
    )
    $existing = Get-PnPList -Identity $Title -ErrorAction SilentlyContinue
    if ($null -ne $existing) {
        Write-Host "[SKIP] Liste '$Title' existe deja." -ForegroundColor Yellow
        return $existing
    }
    Write-Host "[CREATE] Liste '$Title'..." -ForegroundColor Cyan
    $list = New-PnPList -Title $Title -Template GenericList -Url "Lists/$Title" -ErrorAction Stop
    Set-PnPList -Identity $Title -Description $Description
    Write-Host "  -> Cree." -ForegroundColor Green
    return $list
}

function Enable-Versioning {
    param([string]$ListTitle, [int]$MajorVersions = 5)
    Set-PnPList -Identity $ListTitle -EnableVersioning $true -MajorVersions $MajorVersions
    Write-Host "  [VERSIONING] Active sur '$ListTitle' ($MajorVersions versions)." -ForegroundColor DarkGray
}

function Add-TextColumnIfNotExists {
    param(
        [string]$ListTitle,
        [string]$InternalName,
        [string]$DisplayName,
        [switch]$Required,
        [int]$MaxLength = 255
    )
    $existing = Get-PnPField -List $ListTitle -Identity $InternalName -ErrorAction SilentlyContinue
    if ($null -ne $existing) {
        Write-Host "  [SKIP] Colonne '$InternalName' existe deja sur '$ListTitle'." -ForegroundColor Yellow
        return
    }
    $req = if ($Required) { $true } else { $false }
    Add-PnPField -List $ListTitle -InternalName $InternalName -DisplayName $DisplayName `
        -Type Text -AddToDefaultView -Required:$req | Out-Null
    Write-Host "  [+] Colonne Text '$InternalName' cree sur '$ListTitle'." -ForegroundColor Green
}

function Add-NoteColumnIfNotExists {
    param(
        [string]$ListTitle,
        [string]$InternalName,
        [string]$DisplayName,
        [switch]$Required
    )
    $existing = Get-PnPField -List $ListTitle -Identity $InternalName -ErrorAction SilentlyContinue
    if ($null -ne $existing) {
        Write-Host "  [SKIP] Colonne '$InternalName' existe deja sur '$ListTitle'." -ForegroundColor Yellow
        return
    }
    $req = if ($Required) { $true } else { $false }
    Add-PnPField -List $ListTitle -InternalName $InternalName -DisplayName $DisplayName `
        -Type Note -AddToDefaultView -Required:$req | Out-Null
    Write-Host "  [+] Colonne Note '$InternalName' cree sur '$ListTitle'." -ForegroundColor Green
}

function Add-NumberColumnIfNotExists {
    param(
        [string]$ListTitle,
        [string]$InternalName,
        [string]$DisplayName,
        [switch]$Required
    )
    $existing = Get-PnPField -List $ListTitle -Identity $InternalName -ErrorAction SilentlyContinue
    if ($null -ne $existing) {
        Write-Host "  [SKIP] Colonne '$InternalName' existe deja sur '$ListTitle'." -ForegroundColor Yellow
        return
    }
    $req = if ($Required) { $true } else { $false }
    Add-PnPField -List $ListTitle -InternalName $InternalName -DisplayName $DisplayName `
        -Type Number -AddToDefaultView -Required:$req | Out-Null
    Write-Host "  [+] Colonne Number '$InternalName' cree sur '$ListTitle'." -ForegroundColor Green
}

function Add-DateColumnIfNotExists {
    param(
        [string]$ListTitle,
        [string]$InternalName,
        [string]$DisplayName,
        [switch]$Required,
        [switch]$DateOnly
    )
    $existing = Get-PnPField -List $ListTitle -Identity $InternalName -ErrorAction SilentlyContinue
    if ($null -ne $existing) {
        Write-Host "  [SKIP] Colonne '$InternalName' existe deja sur '$ListTitle'." -ForegroundColor Yellow
        return
    }
    $req = if ($Required) { $true } else { $false }
    $field = Add-PnPField -List $ListTitle -InternalName $InternalName -DisplayName $DisplayName `
        -Type DateTime -AddToDefaultView -Required:$req
    if ($DateOnly) {
        # Forcer DateOnly via CAML
        $field.DisplayFormat = [Microsoft.SharePoint.Client.DateTimeFieldFormatType]::DateOnly
        $field.Update()
        Invoke-PnPQuery
    }
    Write-Host "  [+] Colonne DateTime '$InternalName' cree sur '$ListTitle'." -ForegroundColor Green
}

function Add-ChoiceColumnIfNotExists {
    param(
        [string]$ListTitle,
        [string]$InternalName,
        [string]$DisplayName,
        [switch]$Required,
        [string[]]$Choices,
        [string]$Default = ""
    )
    $existing = Get-PnPField -List $ListTitle -Identity $InternalName -ErrorAction SilentlyContinue
    if ($null -ne $existing) {
        Write-Host "  [SKIP] Colonne '$InternalName' existe deja sur '$ListTitle'." -ForegroundColor Yellow
        return
    }
    $req = if ($Required) { $true } else { $false }
    Add-PnPField -List $ListTitle -InternalName $InternalName -DisplayName $DisplayName `
        -Type Choice -AddToDefaultView -Required:$req -Choices $Choices | Out-Null
    if ($Default -ne "") {
        $field = Get-PnPField -List $ListTitle -Identity $InternalName
        $field.DefaultValue = $Default
        $field.Update()
        Invoke-PnPQuery
    }
    Write-Host "  [+] Colonne Choice '$InternalName' cree sur '$ListTitle'." -ForegroundColor Green
}

# -------------------------------------------------------
# Connexion
# -------------------------------------------------------

Write-Host ""
Write-Host "======================================================" -ForegroundColor White
Write-Host " outplacement-tracker v0.1 - Provisioning SharePoint  " -ForegroundColor White
Write-Host "======================================================" -ForegroundColor White
Write-Host ""

Connect-PnPOnline -Url $SiteUrl -Interactive
Write-Host "Connecte a : $SiteUrl" -ForegroundColor Green
Write-Host ""

# -------------------------------------------------------
# Liste 1 : Participants
# -------------------------------------------------------

Write-Host "--- Liste : Participants ---" -ForegroundColor White
Ensure-List -Title "Participants" -Description "Un enregistrement par participant suivi. Table centrale de la solution outplacement-tracker."
Enable-Versioning -ListTitle "Participants" -MajorVersions 5

Add-TextColumnIfNotExists    -ListTitle "Participants" -InternalName "nom"                -DisplayName "Nom"                          -Required
Add-TextColumnIfNotExists    -ListTitle "Participants" -InternalName "prenom"             -DisplayName "Prenom"                       -Required
Add-TextColumnIfNotExists    -ListTitle "Participants" -InternalName "email"              -DisplayName "Email"                        -Required
Add-ChoiceColumnIfNotExists  -ListTitle "Participants" -InternalName "langue"             -DisplayName "Langue"                       -Required `
    -Choices @("DE", "EN") -Default "DE"
Add-TextColumnIfNotExists    -ListTitle "Participants" -InternalName "id_conseillere"     -DisplayName "Conseillere (email M365)"      -Required
Add-DateColumnIfNotExists    -ListTitle "Participants" -InternalName "date_debut_parcours" -DisplayName "Date debut parcours"          -Required -DateOnly
Add-DateColumnIfNotExists    -ListTitle "Participants" -InternalName "date_prochain_rdv"  -DisplayName "Date prochain RDV"            -Required -DateOnly
Add-ChoiceColumnIfNotExists  -ListTitle "Participants" -InternalName "statut"             -DisplayName "Statut"                       -Required `
    -Choices @("actif", "suspendu", "termine") -Default "actif"

Write-Host ""

# -------------------------------------------------------
# Liste 2 : Profils
# -------------------------------------------------------

Write-Host "--- Liste : Profils ---" -ForegroundColor White
Ensure-List -Title "Profils" -Description "Profil de carriere optionnel, un par participant."
Enable-Versioning -ListTitle "Profils" -MajorVersions 5

Add-NumberColumnIfNotExists  -ListTitle "Profils" -InternalName "id_participant"    -DisplayName "ID Participant"      -Required
Add-NoteColumnIfNotExists    -ListTitle "Profils" -InternalName "plan_a"            -DisplayName "Plan A"
Add-NoteColumnIfNotExists    -ListTitle "Profils" -InternalName "plan_b"            -DisplayName "Plan B"
Add-NoteColumnIfNotExists    -ListTitle "Profils" -InternalName "marketingplan"     -DisplayName "Marketingplan"
Add-NoteColumnIfNotExists    -ListTitle "Profils" -InternalName "zielmarkt"         -DisplayName "Zielmarkt"
Add-DateColumnIfNotExists    -ListTitle "Profils" -InternalName "date_creation"     -DisplayName "Date creation"       -Required
Add-DateColumnIfNotExists    -ListTitle "Profils" -InternalName "date_modification" -DisplayName "Date modification"

Write-Host ""

# -------------------------------------------------------
# Liste 3 : BilansMensuels
# -------------------------------------------------------

Write-Host "--- Liste : BilansMensuels ---" -ForegroundColor White
Ensure-List -Title "BilansMensuels" -Description "Un enregistrement par bilan mensuel soumis. Zero a 12 par participant."
Enable-Versioning -ListTitle "BilansMensuels" -MajorVersions 5

Add-NumberColumnIfNotExists  -ListTitle "BilansMensuels" -InternalName "id_participant"                 -DisplayName "ID Participant"                -Required
Add-DateColumnIfNotExists    -ListTitle "BilansMensuels" -InternalName "date_rdv"                       -DisplayName "Date RDV"                      -Required -DateOnly
Add-DateColumnIfNotExists    -ListTitle "BilansMensuels" -InternalName "date_soumission"                -DisplayName "Date soumission"               -Required
Add-NoteColumnIfNotExists    -ListTitle "BilansMensuels" -InternalName "bilan_general"                  -DisplayName "Bilan general"                 -Required
Add-ChoiceColumnIfNotExists  -ListTitle "BilansMensuels" -InternalName "statut_objectifs"               -DisplayName "Statut objectifs" `
    -Choices @("vollstaendig_erreicht", "teilweise_erreicht", "nicht_erreicht", "noch_nicht_relevant")
Add-NoteColumnIfNotExists    -ListTitle "BilansMensuels" -InternalName "statut_objectifs_detail"        -DisplayName "Statut objectifs detail"
Add-NoteColumnIfNotExists    -ListTitle "BilansMensuels" -InternalName "was_lief_gut"                   -DisplayName "Was lief gut"
Add-NoteColumnIfNotExists    -ListTitle "BilansMensuels" -InternalName "wo_brauche_ich_unterstuetzung"  -DisplayName "Wo brauche ich Unterstuetzung"
Add-NoteColumnIfNotExists    -ListTitle "BilansMensuels" -InternalName "themen_naechster_termin"        -DisplayName "Themen naechster Termin"
Add-NoteColumnIfNotExists    -ListTitle "BilansMensuels" -InternalName "sonstige_anmerkungen"           -DisplayName "Sonstige Anmerkungen"

Write-Host ""

# -------------------------------------------------------
# Recapitulatif
# -------------------------------------------------------

Write-Host "======================================================" -ForegroundColor White
Write-Host " Provisioning termine.                                 " -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor White
Write-Host ""
Write-Host "Listes creees (ou deja existantes) :" -ForegroundColor White

$lists = @("Participants", "Profils", "BilansMensuels")
foreach ($l in $lists) {
    $list = Get-PnPList -Identity $l -ErrorAction SilentlyContinue
    if ($null -ne $list) {
        $fields = Get-PnPField -List $l | Where-Object { -not $_.Hidden -and -not $_.ReadOnlyField }
        Write-Host "  [OK] $l - $($fields.Count) colonnes visibles" -ForegroundColor Green
    } else {
        Write-Host "  [ERREUR] $l non trouve !" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Prochaines etapes :" -ForegroundColor White
Write-Host "  1. Creer les formulaires Microsoft Forms (voir forms/forms_construction_guide.md)" -ForegroundColor DarkGray
Write-Host "  2. Deposer les templates Word dans /sites/TransferMappe/Templates/" -ForegroundColor DarkGray
Write-Host "  3. Creer les Flows Power Automate (voir power_automate/)" -ForegroundColor DarkGray
Write-Host ""
