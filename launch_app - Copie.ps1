# ═══════════════════════════════════════════════════════════════════════════
# OPTIPICK - Lanceur d'application Streamlit (PowerShell)
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "╔═══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                    🚀 OPTIPICK - Streamlit App                           ║" -ForegroundColor Cyan
Write-Host "║                                                                           ║" -ForegroundColor Cyan
Write-Host "║ L'application se lance à http://localhost:8501                           ║" -ForegroundColor Green
Write-Host "║ Appuyez sur Ctrl+C pour arrêter                                          ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Aller au répertoire du projet
Set-Location $PSScriptRoot

# Lancer Streamlit
& streamlit run app_streamlit.py
