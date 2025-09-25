import cv2
import time
import os
import subprocess
from datetime import datetime

# ----------------------------
# PARÁMETROS CONFIGURABLES
# ----------------------------
RECORD_DURATION = 120 * 60        # duración de grabación tras detectar movimiento (en segundos), en este caso 2 horas
MOTION_THRESHOLD = 5000           # sensibilidad de detección
OUTPUT_DIR = "recorded_videos"    # carpeta de salida
os.makedirs(OUTPUT_DIR, exist_ok=True) # crear si no existe

FRAME_WIDTH = 640 # ancho del frame
FRAME_HEIGHT = 480 # alto del frame
FPS = 20         # frames por segundo

# Dispositivos de audio por cámara (dshow)
AUDIO_DEVICES = {
    0: 'audio=Micrófono (FaceCam 1000X)', # cambiar si es necesario, solo usar un microfono para ambas camaras
    1: 'audio=Micrófono (FaceCam 1000X)' # cambiar si es necesario
}

# Dispositivos de vídeo para FFmpeg (dshow)
VIDEO_DEVICES = {
    0: 'video=HP High Definition 1MP Webcam', # cambiar si es necesario, puedes agregar más cámaras
    1: 'video=FaceCam 1000X' # cambiar si es necesario, puedes agregar más cámaras
}

# ----------------------------
# FUNCIONES AUXILIARES
# ----------------------------
def configurar_camara(index):
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW) # Usar CAP_DSHOW en Windows
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH) # Ancho
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT) # Alto
    if not cap.isOpened():
        return None
    print(f"[INFO] Cámara {index} abierta correctamente.")
    return cap

# Iniciar grabación de audio con FFmpeg
def iniciar_audio_ffmpeg(cam_idx, timestamp):
    wav_out = os.path.join(OUTPUT_DIR, f"cam{cam_idx}_audio_{timestamp}.wav") # archivo de salida
    cmd = [
        "ffmpeg", "-y", # sobrescribir sin preguntar
        "-f", "dshow", # formato de entrada
        "-i", AUDIO_DEVICES[cam_idx], # dispositivo de audio
        "-t", str(RECORD_DURATION + 5), # duración (un poco más para seguridad)
        wav_out # archivo de salida
    ]
    return subprocess.Popen(cmd)

def muxear(cam_idx, timestamp):
    avi = os.path.join(OUTPUT_DIR, f"cam{cam_idx}_{timestamp}.avi")
    wav = os.path.join(OUTPUT_DIR, f"cam{cam_idx}_audio_{timestamp}.wav")
    mkv = os.path.join(OUTPUT_DIR, f"cam{cam_idx}_{timestamp}.mkv")
    if not os.path.exists(avi) or not os.path.exists(wav) or os.path.getsize(wav) < 1000:
        print(f"[ERROR] No válido para cámara {cam_idx}. Omite muxear.")
        return
    cmd = [
        "ffmpeg", "-y",
        "-i", avi,
        "-i", wav,
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "aac",
        "-shortest", mkv
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(avi)
    os.remove(wav)

# ----------------------------
# FUNCIÓN PRINCIPAL
# ----------------------------
def main():
    # 1) Abrir cámaras
    caps = [configurar_camara(0), configurar_camara(1)]
    if not any(caps):
        print("[ERROR] No se pudo abrir ninguna cámara.")
        return

    # 2) Inicializar fondo para detección
    prev = {}
    for idx, cap in enumerate(caps):
        if cap:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            prev[idx] = cv2.GaussianBlur(gray, (21,21), 0)

    # 3) Estados y buffers
    recording     = {0: False, 1: False}
    writers       = {0: None, 1: None}
    audio_procs   = {0: None, 1: None}
    timestamp_cam = {0: None, 1: None}
    end_time      = {0: 0, 1: 0}

    print("Detección iniciada en cámaras 0 y 1. Esperando movimiento...")

    while True:
        now = time.time()
        frames, threshs = {}, {}
        movimiento_global = False

        # 4) Detectar movimiento
        for idx, cap in enumerate(caps):
            if not cap:
                continue
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21,21), 0)
            delta = cv2.absdiff(prev[idx], gray)
            th = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
            th = cv2.dilate(th, None, iterations=2)
            contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if any(cv2.contourArea(c) >= MOTION_THRESHOLD for c in contours):
                movimiento_global = True

            prev[idx] = gray
            frames[idx] = frame
            threshs[idx] = th

        # 5) Iniciar grabación en ambas si hay movimiento
        if movimiento_global and not any(recording.values()):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Movimiento detectado → iniciando grabación en ambas cámaras.")
            for idx in (0, 1):
                if caps[idx]:
                    # cerrar previos
                    if writers[idx]:
                        writers[idx].release()
                    if audio_procs[idx]:
                        audio_procs[idx].terminate()
                        audio_procs[idx].wait()
                    # iniciar video
                    avi_path = os.path.join(OUTPUT_DIR, f"cam{idx}_{ts}.avi")
                    writers[idx] = cv2.VideoWriter(
                        avi_path,
                        cv2.VideoWriter_fourcc(*'XVID'),
                        FPS,
                        (FRAME_WIDTH, FRAME_HEIGHT)
                    )
                    recording[idx] = True
                    end_time[idx] = now + RECORD_DURATION
                    timestamp_cam[idx] = ts
                    # iniciar audio
                    audio_procs[idx] = iniciar_audio_ffmpeg(idx, ts)

        # 6) Escribir frames y detener si expiró
        for idx in (0, 1):
            if recording[idx]:
                frame = frames.get(idx)
                if frame is not None:
                    ts_txt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cv2.putText(frame, ts_txt, (10, FRAME_HEIGHT-10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
                    writers[idx].write(frame)
				# aquí cuando expira
                if now >= end_time[idx]:
                    print(f"[INFO] Grabación terminada en cámara {idx}. Procesando...")
                    recording[idx] = False

					# Cerrar video
                    if writers[idx]:
                        writers[idx].release()
                        writers[idx] = None

					# Cerrar audio
                    if audio_procs[idx]:
                        audio_procs[idx].terminate()
                        audio_procs[idx].wait()
                        audio_procs[idx] = None

					# Mezclar audio + video (espera 1s por seguridad)
                    ts = timestamp_cam[idx]
                    if ts:
                        time.sleep(1)
                        muxear(idx, ts)
                        timestamp_cam[idx] = None

        # 7) Mostrar vídeo y umbral
        for idx in frames:
            cv2.imshow(f"Cámara {idx}", frames[idx])
            cv2.imshow(f"Umbral {idx}", threshs[idx])

        # 8) Parada suave: stop.flag o tecla 'q'
        key = cv2.waitKey(1) & 0xFF
               # 8) Parada suave: stop.flag o tecla 'q'
        key = cv2.waitKey(1) & 0xFF
        if os.path.exists("stop.flag") or key == ord('q'):
            motivo = "stop.flag" if os.path.exists("stop.flag") else "'q' pulsada"
            print(f"[INFO] {motivo}, cerrando grabaciones...")

            # 1) Eliminar la flag (solo si existía)
            if os.path.exists("stop.flag"):
                os.remove("stop.flag")

            # 2) Terminar video writers activos
            for idx in (0, 1):
                if recording[idx]:
                    writers[idx].release()
                    recording[idx] = False

            # 3) Terminar procesos FFmpeg de audio
            for idx in (0, 1):
                if audio_procs[idx]:
                    audio_procs[idx].terminate()
                    audio_procs[idx].wait()
                    audio_procs[idx] = None

            break
        if key == ord('q'):
            print("[INFO] 'q' pulsada, cerrando grabaciones...")
            break

    # 9) Al cerrar: esperar audio y muxear
    for idx in (0, 1):
        if audio_procs[idx]:
            audio_procs[idx].wait()
        if writers[idx]:
            writers[idx].release()
        ts = timestamp_cam[idx]
        if ts:
            time.sleep(1)
            muxear(idx, ts)

    # 10) Limpieza final
    for cap in caps:
        if cap: cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
