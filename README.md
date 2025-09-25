🤖 Sistema de Grabación de Movimiento
Este proyecto es una solución simple y efectiva para la videovigilancia, diseñada para grabar video y audio de una o más cámaras solo cuando se detecta movimiento. Es ideal para monitorear un área específica sin llenar el disco duro con horas de video innecesario.

📁 Estructura del Proyecto
El proyecto se compone de los siguientes archivos y carpetas esenciales:

motion_recorder.py: El corazón del sistema. Es el script de Python que gestiona la detección de movimiento y la grabación de video y audio.

requirements.txt: Un archivo de texto que lista las librerías de Python necesarias para que el script funcione.

StartMotion.bat: Un script de Windows que inicia el programa de manera discreta en segundo plano.

StopMotion.bat: Un script de Windows para detener la grabación de forma segura.

ApagarPantalla.bat: Un script opcional que apaga el monitor sin detener el programa.

ffmpeg: Una carpeta que contiene el poderoso software para grabar audio y combinar el audio con el video.

nircmd: Una carpeta que contiene una herramienta para controlar la pantalla.

⚙️ Requisitos y Configuración Inicial
Para que el sistema funcione a la perfección, necesitas hacer una configuración inicial.

1. Preparar FFmpeg y nircmd
Descomprime las carpetas de ffmpeg y nircmd en la misma ubicación que el resto de los archivos del proyecto.

Agrega FFmpeg a las Variables de Entorno (PATH). Esto permite que el sistema operativo encuentre el programa ffmpeg.exe sin importar dónde te encuentres.

Busca "Editar las variables de entorno del sistema" en el menú de inicio.

Haz clic en "Variables de entorno...".

En la sección "Variables del sistema", busca la variable Path y haz doble clic sobre ella.

Haz clic en Nuevo y añade la ruta a la carpeta bin de tu ffmpeg (por ejemplo: C:\Users\TuUsuario\Documents\Proyecto\ffmpeg\bin).

2. Modificar Rutas en los Scripts
Abre los siguientes archivos .bat y actualiza la ruta con la dirección de tu carpeta de proyecto.

StartMotion.bat

cd /d C:\Users\TuUsuario\Documents\Proyecto\

StopMotion.bat

echo STOP > C:\Users\TuUsuario\Documents\Proyecto\stop.flag

ApagarPantalla.bat

C:\Users\TuUsuario\Documents\Proyecto\nircmd\nircmd.exe monitor off

📸 Configurar Cámaras y Micrófonos
El script motion_recorder.py necesita los nombres exactos de tus dispositivos de video y audio.

1. Obtener los nombres de tus dispositivos
Abre una terminal de Windows (PowerShell o Símbolo del sistema) y ejecuta este comando para ver una lista de todos tus dispositivos:

ffmpeg -list_devices true -f dshow -i dummy

En la salida de la terminal, verás los nombres de tus cámaras y micrófonos. Copia los nombres exactos de los dispositivos que deseas usar.

2. Modificar el script motion_recorder.py
Abre el archivo motion_recorder.py y busca las siguientes secciones. Reemplaza los nombres de ejemplo con los que obtuviste en el paso anterior.

# Dispositivos de audio por cámara (dshow)
AUDIO_DEVICES = {
    0: 'audio=NOMBRE_DE_TU_MICROFONO_1', # Ejemplo: 'audio=Micrófono (FaceCam 1000X)'
    1: 'audio=NOMBRE_DE_TU_MICROFONO_2' # Si solo usas un micrófono para ambas, usa el mismo nombre
}

# Dispositivos de vídeo para FFmpeg (dshow)
VIDEO_DEVICES = {
    0: 'video=NOMBRE_DE_TU_CAMARA_1', # Ejemplo: 'video=HP High Definition 1MP Webcam'
    1: 'video=NOMBRE_DE_TU_CAMARA_2'
}

▶️ Uso del Sistema
Para iniciar la grabación: Haz doble clic en StartMotion.bat. Este script se encargará de todo.

Para detener la grabación: Haz doble clic en StopMotion.bat. El sistema detectará el comando de parada y finalizará la grabación de forma segura, procesando los archivos.

Para apagar la pantalla: Haz doble clic en ApagarPantalla.bat. Esto apagará el monitor, pero el programa de grabación continuará funcionando en segundo plano.

🛠️ Explicación Técnica
Detección de Movimiento: El script compara fotogramas de video continuos para encontrar cambios significativos. Si la diferencia es grande (supera el MOTION_THRESHOLD), inicia la grabación.

Grabación Simultánea: El video se graba usando OpenCV y el audio se captura al mismo tiempo con un proceso separado de FFmpeg. Esto asegura que ambos flujos se graben en alta calidad.

Mezcla de Archivos: Una vez que la grabación se detiene, el programa utiliza FFmpeg para combinar el archivo de video (.avi) y el de audio (.wav) en un solo archivo final (.mkv) con audio y video sincronizados. Los archivos temporales se eliminan automáticamente.