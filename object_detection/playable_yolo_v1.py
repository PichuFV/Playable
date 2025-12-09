import cv2
from ultralytics import YOLO
from pynput.keyboard import Key, Controller
from collections import deque
import torch

# Carrega o modelo YOLOv8 treinado
model = YOLO("best.pt")

# Mapeamento: nome da classe -> tecla
# (use exatamente os nomes do Roboflow: 'up', 'down', 'left', 'right', 'center')
command_to_key = {
    "up": Key.up,
    "down": Key.down,
    "left": Key.right,
    "right": Key.left,
    "center": None
}

keyboard = Controller()
current_key = None

SMOOTHING_WINDOW = 5
pred_queue = deque(maxlen=SMOOTHING_WINDOW)


def apply_command(command):
    global current_key
    new_key = command_to_key.get(command, None)

    # center = solta qualquer tecla
    if command == "center" or new_key is None:
        if current_key is not None:
            keyboard.release(current_key)
            current_key = None
        return

    # Se mudou de direção, solta a anterior
    if current_key is not None and current_key != new_key:
        keyboard.release(current_key)

    # Pressiona a nova tecla se ainda não estiver pressionada
    if current_key != new_key:
        keyboard.press(new_key)
        current_key = new_key


# Abre webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Não foi possível abrir a webcam.")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # espelha a imagem para ficar mais intuitivo
        frame = cv2.flip(frame, 1)

        # roda o modelo no frame
        results = model(frame, verbose=False)[0]

        # Default: se não detectar nada, considera 'center'
        label = "center"

        if results.boxes is not None and len(results.boxes) > 0:
            boxes = results.boxes
            # pega a detecção com maior confiança
            best_idx = int(torch.argmax(boxes.conf).item())
            cls_id = int(boxes.cls[best_idx].item())
            label = model.names[cls_id]

            # desenhar bounding box (opcional)
            x1, y1, x2, y2 = boxes.xyxy[best_idx].int().tolist()
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Suavização temporal
        pred_queue.append(label)
        if len(pred_queue) == SMOOTHING_WINDOW:
            counts = {}
            for p in pred_queue:
                counts[p] = counts.get(p, 0) + 1
            smooth_label = max(counts, key=counts.get)
        else:
            smooth_label = label

        apply_command(smooth_label)

        cv2.putText(frame, f"Pred: {label} | Smooth: {smooth_label}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 0), 2)

        cv2.imshow("PlayAble - YOLO Head Pose", frame)

        # 'q' pra sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    if current_key is not None:
        keyboard.release(current_key)
    cap.release()
    cv2.destroyAllWindows()