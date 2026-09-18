@echo off
chcp 65001 >nul
title M-CREDIT 360 - BUILD DOCKER CONTAINER (GREENNODE CLOUD)
color 0A

echo =====================================================================
echo   M-CREDIT 360 - DOCKER CONTAINER BUILD FOR GREENNODE CLOUD
echo   Team 22 - Hattrick (MSB AI Hackathon 2026)
echo   Leader: Michael Nguyen
echo =====================================================================
echo.

echo [1/3] Kiem tra ket noi Docker Engine...
docker version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] Canh bao: Docker Engine chua duoc khoi dong tren may.
    echo [*] Neu Sếp muon chay Docker local, hay bat Docker Desktop truoc.
    echo [*] Tuy nhien ma nguon da san sang 100% de day len GreenNode VCR Registry!
    echo.
) else (
    echo [OK] Docker Engine dang hoat dong!
    echo.
    echo [2/3] Dang build Docker Image: vcr.vngcloud.vn/111480-abp114553/zalo-bot-gateway:v1 ...
    docker build -t vcr.vngcloud.vn/111480-abp114553/zalo-bot-gateway:v1 -f Dockerfile.zalo .
    echo.
    echo [3/3] Build hoan tat! Chay lenh sau de day len GreenNode Cloud:
    echo     docker push vcr.vngcloud.vn/111480-abp114553/zalo-bot-gateway:v1
)

echo.
echo =====================================================================
echo   CAC FILE DOCKER DA SAN SANG TRONG THU MUC:
echo   1. Dockerfile.zalo (Chay rieng le Gateway Zalo Bot 24/7)
echo   2. Dockerfile (Tich hop AgentBase + Zalo Bot chay chung Port 8080)
echo   3. docker-compose.yml (Khoi chay 1-Click bang lenh docker-compose up -d)
echo =====================================================================
pause
