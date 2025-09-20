@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul

echo AtCoder Test Tool starting...

REM 仮想環境のディレクトリ名
set VENV_DIR=venv

REM 仮想環境が存在するかチェック
if not exist "%VENV_DIR%" (
    echo Virtual environment not found. Creating...
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo Error: Failed to create virtual environment.
        echo Please check if Python is installed.
        pause
        exit /b 1
    )
    echo Virtual environment created.
)

REM 仮想環境をアクティベート
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b 1
)

REM 必要なパッケージのリスト
set PACKAGES=keyboard beautifulsoup4 numpy

REM 依存関係のチェックとインストール
set NEED_INSTALL=0

python -c "import keyboard" 2>nul
if errorlevel 1 set NEED_INSTALL=1

python -c "import bs4" 2>nul
if errorlevel 1 set NEED_INSTALL=1

python -c "import numpy" 2>nul
if errorlevel 1 set NEED_INSTALL=1

if !NEED_INSTALL! equ 1 (
    echo Installing dependencies...
    pip install %PACKAGES%
    if errorlevel 1 (
        echo Error: Failed to install dependencies.
        pause
        exit /b 1
    )
    echo Dependencies installation completed.
)

REM main.pyを実行
echo Starting application...
python main.py

REM エラーが発生した場合は一時停止
if errorlevel 1 (
    echo Error: An error occurred while running the application.
    pause
)