import time
import cv2
import keyboard
from ultralytics import YOLO

# ============================================
# CONFIGURAÇÕES
# ============================================

# Delay mínimo entre comandos (segundos) para não spammar teclas
COMMAND_COOLDOWN = 0.15

# Se quiser diminuir o uso de CPU/GPU, você pode rodar
# o modelo a cada N frames em vez de todo frame:
PREDICT_EVERY_N_FRAMES = 2

# ============================================
# CARREGA O MODELO
# ============================================

print("[INFO] Carregando modelo YOLOv8 (classificação)...")
model = YOLO("best.pt")

# model.names é um dict: {0: 'center', 1: 'down', ...}
class_names = model.names
print("[INFO] Classes aprendidas:", class_names)

# ============================================
# MAPEAMENTO CLASSE -> TECLA
# ============================================

def label_to_key(label: str):
    """
    Converte o nome da classe em uma tecla do teclado.
    'center' não manda nada.
    """
    mapping = {
        "up": "up",
        "down": "down",
        "left": "left",
        "right": "right",
        # "center" -> None (sem comando)
    }
    return mapping.get(label, None)

# ============================================
# LOOP PRINCIPAL: WEBCAM -> MODELO -> TECLAS
# ============================================

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERRO] Não conseguiu abrir a webcam.")
        return

    print("[INFO] Webcam aberta. Pressione 'q' na janela de vídeo para sair.")
    last_command_time = 0.0
    frame_count = 0

    last_label = None  # para debug / overlay

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERRO] Falha ao ler frame da webcam.")
            break

        frame_count += 1

        # Só roda o modelo a cada N frames para aliviar um pouco
        do_predict = (frame_count % PREDICT_EVERY_N_FRAMES == 0)

        if do_predict:
            # Chama o modelo de classificação
            # (YOLOv8 cuida do resize interno, mas imgsz ajuda a padronizar)
            results = model.predict(source=frame, imgsz=224, verbose=False)
            res = results[0]

            # Índice da classe com maior probabilidade
            top_idx = int(res.probs.top1)
            label = class_names[top_idx]
            conf = float(res.probs.top1conf)

            last_label = f"{label} ({conf:.2f})"

            # Decidir se manda tecla
            now = time.time()
            if now - last_command_time >= COMMAND_COOLDOWN:
                key = label_to_key(label)
                if key is not None:
                    # Envia uma "teclada" rápida
                    keyboard.press_and_release(key)
                    print(f"[CMD] {label} -> key '{key}' (conf={conf:.2f})")
                    last_command_time = now
                else:
                    # center (ou label desconhecida) -> sem comando
                    pass

        # Desenha texto na imagem pra você ver a predição
        if last_label is not None:
            cv2.putText(
                frame,
                f"Pred: {last_label}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

        cv2.imshow("PlayAble - Webcam", frame)

        # Sair com 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()