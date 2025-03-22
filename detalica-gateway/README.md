### Commands for Windows

- New-Service -Name "DetalicaGateway2" -BinaryPathName "C:\Users\hvang\projects\fiscal-mk\detalica-gateway\dist\printer_client/exe"
- Start-Service -Name "DetalicaGateway2"
- Set-Service -Name "DetalicaGateway2" -StartupType Automatic
