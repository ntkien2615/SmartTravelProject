# Script để chạy Flask backend và Streamlit cùng lúc
# Run Flask backend and Streamlit together

Write-Host "Starting SmartTravel with Flask backend..." -ForegroundColor Green

# Start Flask backend in background
Write-Host "Starting Flask backend on port 5000..." -ForegroundColor Cyan
Start-Process python -ArgumentList "flask_backend.py" -WindowStyle Hidden

# Wait for Flask to start
Start-Sleep -Seconds 2

# Start Streamlit
Write-Host "Starting Streamlit on port 8501..." -ForegroundColor Cyan
python -m streamlit run .\smarttravel.py --server.port 8501

# Wait for Streamlit to start
Start-Sleep -Seconds 2
Write-Host "SmartTravel is running!" -ForegroundColor Green

# Note: Press Ctrl+C to stop. You may need to manually kill the Flask process
Write-Host "To stop Flask backend, run: Stop-Process -Name python -Force" -ForegroundColor Yellow
