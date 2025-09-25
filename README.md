Sistema de Grabación de Movimiento

Este proyecto es una solucion simple y efectiva para la videovigilancia, diseñada para grabar video y audio de una o mas camaras solo cuando se detecta movimiento. Es ideal para monitorear un area especifica sin llenar el disco duro con horas de video innecesario.

Estructura del Proyecto

El proyecto se compone de los siguientes archivos y carpetas esenciales:

motion_recorder.py: El corazon del sistema. Es el script de Python que gestiona la deteccion de movimiento y la grabacion de video y audio.

requirements.txt: Un archivo de texto que lista las librerias de Python necesarias para que el script funcione.

StartMotion.bat: Un script de Windows para iniciar el programa de manera discreta en segundo plano.

StopMotion.bat: Un script de Windows para detener la grabacion de forma segura.

ApagarPantalla.bat: Un script opcional que apaga el monitor sin detener el programa.

ffmpeg: Una carpeta que contiene el poderoso software para grabar audio y combinar el audio con el video.

nircmd: Una carpeta que contiene una herramienta para controlar la pantalla.

Requisitos y Configuracion Inicial

Para que el sistema funcione a la perfeccion, necesitas hacer una configuracion inicial.

Preparar FFmpeg y nircmd

Descomprime las carpetas de ffmpeg y nircmd en la misma ubicacion que el resto de los archivos del proyecto.

Agrega FFmpeg a las Variables de Entorno (PATH). Esto permite que el sistema operativo encuentre el programa ffmpeg.exe sin importar donde te encuentres.

Busca "Editar las variables de entorno del sistema" en el menu de inicio.

Haz clic en "Variables de entorno...".

En la seccion "Variables del sistema", busca la variable Path y haz doble clic sobre ella.

Haz clic en Nuevo y anade la ruta a la carpeta bin de tu ffmpeg (por ejemplo: C:\Users\TuUsuario\Documents\Proyecto\ffmpeg\bin).

Modificar Rutas en los Scripts

Abre los siguientes archivos .bat y actualiza la ruta con la direccion de tu carpeta de proyecto.

@REM en StartMotion.bat
cd /d C:\Users\TuUsuario\Documents\Proyecto\

@REM en StopMotion.bat
echo STOP > C:\Users\TuUsuario\Documents\Proyecto\stop.flag

@REM en ApagarPantalla.bat
C:\Users\TuUsuario\Documents\Proyecto\nircmd\nircmd.exe monitor off

Configurar Camaras y Microfonos

El script motion_recorder.py necesita los nombres exactos de tus dispositivos de video y audio.

Obtener los nombres de tus dispositivos

Abre una terminal de Windows (PowerShell o Simbolo del sistema) y ejecuta este comando para ver una lista de todos tus dispositivos:

ffmpeg -list_devices true -f dshow -i dummy

En la salida de la terminal, veras los nombres de tus camaras y microfonos. Copia los nombres exactos de los dispositivos que deseas usar.

Modificar el script motion_recorder.py

Abre el archivo motion_recorder.py y busca las siguientes secciones. Reemplaza los nombres de ejemplo con los que obtuviste en el paso anterior.

Dispositivos de audio por camara (dshow)
AUDIO_DEVICES = {
0: 'audio=NOMBRE_DE_TU_MICROFONO_1', # Ejemplo: 'audio=Microfono (FaceCam 1000X)'
1: 'audio=NOMBRE_DE_TU_MICROFONO_2' # Si solo usas un microfono para ambas, usa el mismo nombre
}

Dispositivos de video para FFmpeg (dshow)
VIDEO_DEVICES = {
0: 'video=NOMBRE_DE_TU_CAMARA_1', # Ejemplo: 'video=HP High Definition 1MP Webcam'
1: 'video=NOMBRE_DE_TU_CAMARA_2'
}

Uso del Sistema

Para iniciar la grabacion: Haz doble clic en StartMotion.bat. Este script se encargara de todo, ¡y el programa se ejecutara sin mostrar una ventana de consola!

Para detener la grabacion: Haz doble clic en StopMotion.bat. El sistema detectara el comando de parada y finalizara la grabacion de forma segura, procesando los archivos.

Para apagar la pantalla: Haz doble clic en ApagarPantalla.bat. Esto apagara el monitor, pero el programa de grabacion continuara funcionando en segundo plano.

Explicacion Tecnica

Deteccion de Movimiento: El script compara fotogramas de video continuos para encontrar cambios significativos. Si la diferencia es grande (supera el MOTION_THRESHOLD), inicia la grabacion.

Grabacion Simultanea: El video se graba usando OpenCV y el audio se captura al mismo tiempo con un proceso separado de FFmpeg. Esto asegura que ambos flujos se graben en alta calidad.

Mezcla de Archivos: Una vez que la grabacion se detiene, el programa utiliza FFmpeg para combinar el archivo de video (.avi) y el de audio (.wav) en un solo archivo final (.mkv) con audio y video sincronizados. Los archivos temporales se eliminan automaticamente.