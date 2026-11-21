$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
Write-Host '香港随行预览：http://localhost:4173/'
Write-Host '保持本窗口运行；按 Ctrl+C 停止。若端口已占用，可直接打开上述地址。'
node server.mjs
