# Step 1: Start all containers, including ngrok
docker-compose up -d --build

# Step 2: Wait for ngrok to be ready
Write-Host "Waiting for ngrok to start..."
Start-Sleep -Seconds 5

# Step 3: Get public ngrok URL
try {
    $response = Invoke-WebRequest -Uri "http://localhost:4040/api/tunnels" -UseBasicParsing
    $json = $response.Content | ConvertFrom-Json
    $ngrokUrl = $json.tunnels | Where-Object { $_.proto -eq "https" } | Select-Object -ExpandProperty public_url

    if (-not $ngrokUrl) {
        throw "Unable to retrieve ngrok URL."
    }

    Write-Host "NGROK URL: $ngrokUrl"
} catch {
    Write-Error "Failed to get ngrok URL from API."
    exit 1
}

# Step 4: Write NGROK_URL to .env
".env file updated with ngrok URL" | Out-Host
"NGROK_URL=$ngrokUrl" | Set-Content -Encoding UTF8 .env

# Step 5: Rebuild and restart only the services that need the NGROK_URL
docker-compose up -d --build auth_server client_server resource_server
