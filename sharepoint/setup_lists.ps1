<#
.SYNOPSIS
    Bereitstellung der SharePoint-Listen fuer outplacement-tracker v0.1
.DESCRIPTION
    Erstellt die 3 SharePoint-Listen (Participants, Profils, BilansMensuels) und ihre Spalten.
    Idempotent: kann ohne Fehler erneut ausgefuehrt werden, wenn die Listen bereits vorhanden sind.
.PARAMETER SiteUrl
    URL der Ziel-SharePoint-Website (Bsp.: https://contoso.sharepoint.com/sites/TransferMappe)
.EXAMPLE
    .\setup_lists.ps1 -SiteUrl "https://contoso.sharepoint.com/sites/TransferMappe"
.PREREQUIS
    Modul PnP.PowerShell installiert: Install-Module PnP.PowerShell -Force
    Aktive Verbindung: Connect-PnPOnline -Url $SiteUrl -Interactive
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$SiteUrl
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# -------------------------------------------------------
# Hilfsfunktionen
# -------------------------------------------------------

function Ensure-List {
    param(
        [string]$Title,
        [string]$Description
    )
    $existing = Get-PnPList -Identity $Title -ErrorAction SilentlyContinue
    if ($null -ne $existing) {
        Write-Host "[SKIP] Liste '$Title' bereits vorhanden." -ForegroundColor Yellow
        return $existing
    }
    Write-Host "[CREATE] Liste '$Title'..." -ForegroundColor Cyan
    $list = New-PnPList -Title $Title -Template GenericList -Url "Lists/$Title" -ErrorAction Stop
    Set-PnPList -Identity $Title -Description $Description
    Write-Host "  -> Erstellt." -ForegroundColor Green
    return $list
}

function Enable-Versioning {
    param([string]$ListTitle, [int]$MajorVersions = 5)
    Set-PnPList -Identity $ListTitle -EnableVersioning $true -MajorVersions $MajorVersions
    Write-Host "  [VERSIONING] Aktiviert fuer '$ListTitle' ($MajorVersions Versionen)." -ForegroundColor DarkGray
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
        Write-Host "  [SKIP] Spalte '$InternalName' bereits vorhanden in '$ListTitle'." -ForegroundColor Yellow
        return
    }
    $req = if ($Required) { $true } else { $false }
    Add-PnPField -List $ListTitle -InternalName $InternalName -DisplayName $DisplayName `
        -Type Text -AddToDefaultView -Required:$req | Out-Null
    Write-Host "  [+] Text-Spalte '$InternalName' erstellt in '$ListTitle'." -ForegroundColor Green
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
        Write-Host "  [SKIP] Spalte '$InternalName' bereits vorhanden in '$ListTitle'." -ForegroundColor Yellow
        return
    }
    $req = if ($Required) { $true } else { $false }
    Add-PnPField -List $ListTitle -InternalName $InternalName -DisplayName $DisplayName `
        -Type Note -AddToDefaultView -Required:$req | Out-Null
    Write-Host "  [+] Note-Spalte '$InternalName' erstellt in '$ListTitle'." -ForegroundColor Green
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
        Write-Host "  [SKIP] Spalte '$InternalName' bereits vorhanden in '$ListTitle'." -ForegroundColor Yellow
        return
    }
    $req = if ($Required) { $true } else { $false }
    Add-PnPField -List $ListTitle -InternalName $InternalName -DisplayName $DisplayName `
        -Type Number -AddToDefaultView -Required:$req | Out-Null
    Write-Host "  [+] Number-Spalte '$InternalName' erstellt in '$ListTitle'." -ForegroundColor Green
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
        Write-Host "  [SKIP] Spalte '$InternalName' bereits vorhanden in '$ListTitle'." -ForegroundColor Yellow
        return
    }
    $req = if ($Required) { $true } else { $false }
    $field = Add-PnPField -List $ListTitle -InternalName $InternalName -DisplayName $DisplayName `
        -Type DateTime -AddToDefaultView -Required:$req
    if ($DateOnly) {
        # DateOnly per CAML erzwingen
        $field.DisplayFormat = [Microsoft.SharePoint.Client.DateTimeFieldFormatType]::DateOnly
        $field.Update()
        Invoke-PnPQuery
    }
    Write-Host "  [+] DateTime-Spalte '$InternalName' erstellt in '$ListTitle'." -ForegroundColor Green
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
        Write-Host "  [SKIP] Spalte '$InternalName' bereits vorhanden in '$ListTitle'." -ForegroundColor Yellow
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
    Write-Host "  [+] Choice-Spalte '$InternalName' erstellt in '$ListTitle'." -ForegroundColor Green
}

# -------------------------------------------------------
# Verbindung
# -------------------------------------------------------

Write-Host ""
Write-Host "======================================================" -ForegroundColor White
Write-Host " outplacement-tracker v0.1 - Provisioning SharePoint  " -ForegroundColor White
Write-Host "======================================================" -ForegroundColor White
Write-Host ""

Connect-PnPOnline -Url $SiteUrl -Interactive
Write-Host "Verbunden mit: $SiteUrl" -ForegroundColor Green
Write-Host ""

# -------------------------------------------------------
# Liste 1 : Participants
# -------------------------------------------------------

Write-Host "--- Liste: Participants ---" -ForegroundColor White
Ensure-List -Title "Participants" -Description "Ein Datensatz pro betreutem Teilnehmer. Zentrale Tabelle der outplacement-tracker-Loesung."
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

Write-Host "--- Liste: Profils ---" -ForegroundColor White
Ensure-List -Title "Profils" -Description "Optionales Karriereprofil, ein Datensatz pro Teilnehmer."
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

Write-Host "--- Liste: BilansMensuels ---" -ForegroundColor White
Ensure-List -Title "BilansMensuels" -Description "Ein Datensatz pro eingereichtem Monatsbericht. Null bis zwoelf pro Teilnehmer."
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
# Zusammenfassung
# -------------------------------------------------------

Write-Host "======================================================" -ForegroundColor White
Write-Host " Bereitstellung abgeschlossen.                         " -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor White
Write-Host ""
Write-Host "Erstellte (oder bereits vorhandene) Listen:" -ForegroundColor White

$lists = @("Participants", "Profils", "BilansMensuels")
foreach ($l in $lists) {
    $list = Get-PnPList -Identity $l -ErrorAction SilentlyContinue
    if ($null -ne $list) {
        $fields = Get-PnPField -List $l | Where-Object { -not $_.Hidden -and -not $_.ReadOnlyField }
        Write-Host "  [OK] $l - $($fields.Count) sichtbare Spalten" -ForegroundColor Green
    } else {
        Write-Host "  [FEHLER] $l nicht gefunden!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Naechste Schritte:" -ForegroundColor White
Write-Host "  1. Microsoft Forms-Formulare erstellen (siehe forms/forms_construction_guide.md)" -ForegroundColor DarkGray
Write-Host "  2. Word-Templates in /sites/TransferMappe/Templates/ ablegen" -ForegroundColor DarkGray
Write-Host "  3. Power Automate Flows erstellen (siehe power_automate/)" -ForegroundColor DarkGray
Write-Host ""
