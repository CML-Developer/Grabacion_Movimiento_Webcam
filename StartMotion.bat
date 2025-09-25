@echo off
REM —————————————————————————————————————————————
REM StartMotion.bat
REM Activa o crea el venv, instala requirements y ejecuta motion_recorder.py con pythonw.
REM —————————————————————————————————————————————

REM 1) Ir a la carpeta donde está tu proyecto
cd /d C:\Users\TuUsuario\Documents\Grabaciones
echo [DEBUG] Directorio actual: %CD%

REM 2) Verificar si existe venv, si no, crearlo
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] No existe entorno virtual. Creando...
    python -m venv venv
    if ERRORLEVEL 1 (
        echo [ERROR] Falló la creación del entorno virtual.
        pause
        exit /b 1
    )
    echo [DEBUG] Entorno virtual creado correctamente.
)

REM 3) Activar entorno virtual
call venv\Scripts\activate
if ERRORLEVEL 1 (
    echo [ERROR] No se pudo activar el entorno virtual.
    pause
    exit /b 1
)
echo [DEBUG] Entorno virtual activado.

REM 4) Instalar dependencias si no están instaladas
if exist requirements.txt (
    echo [INFO] Instalando dependencias desde requirements.txt...
    pip install --upgrade pip
    pip install -r requirements.txt
)

REM 5) Verificar que pythonw.exe exista
if not exist "venv\Scripts\pythonw.exe" (
    echo [ERROR] No se encuentra pythonw.exe en venv\Scripts.
    pause
    exit /b 1
)
echo [DEBUG] pythonw.exe encontrado.

REM 6) Verificar que motion_recorder.py exista
if not exist "motion_recorder.py" (
    echo [ERROR] No se encuentra motion_recorder.py en %CD%.
    pause
    exit /b 1
)
echo [DEBUG] motion_recorder.py encontrado.

REM 7) Ejecutar el script en modo headless (pythonw no abre ventana de consola)
start "" "%~dp0venv\Scripts\pythonw.exe" "%~dp0motion_recorder.py"
if ERRORLEVEL 1 (
    echo [ERROR] Falló al lanzar motion_recorder.py con pythonw.
    pause
    exit /b 1
)
echo [DEBUG] motion_recorder.py lanzado con pythonw.exe (sin ventana).
exit /b 0
