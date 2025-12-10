import time
import cv2
import argparse
import keyboard
from ultralytics import YOLO


# Delay mínimo entre comandos (segundos) para não spammar teclas
COMMAND_COOLDOWN = 0.15

PREDICT_EVERY_N_FRAMES = 2 # Processa o modelo a cada N frames para aliviar CPU/GPU

print("[INFO] Carregando modelo YOLOv8 (classificação)...")
model = YOLO("./classification/best.pt")

class_names = model.names
print("[INFO] Classes aprendidas:", class_names)



def main(key_mappings):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERRO] Não conseguiu abrir a webcam.")
        return

    # Define o nome da janela para ser reutilizado
    window_name = "PlayAble - Webcam"
    # Cria a janela com a propriedade AUTOSIZE para que ela se ajuste perfeitamente ao frame
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    print(f"[INFO] Webcam aberta. Pressione 'ESC' ou feche a janela ('X') para sair.")
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
            # Chama o modelo de classificação (YOLOv8 cuida do resize interno, mas imgsz ajuda a padronizar)
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
                key = key_mappings.get(label) # Usa o mapeamento recebido
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

        cv2.imshow(window_name, frame)

        # Pressionar a tecla 'ESC' (código 27) ou clicar no botão 'X' da janela (getWindowProperty retorna < 1)
        if cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    # Configura o parser de argumentos para receber os mapeamentos de teclas
    parser = argparse.ArgumentParser(description="PlayAble - Head Movement Detection")
    parser.add_argument("--up", type=str, default="up", help="Tecla para o movimento 'up'")
    parser.add_argument("--down", type=str, default="down", help="Tecla para o movimento 'down'")
    parser.add_argument("--left", type=str, default="left", help="Tecla para o movimento 'left'")
    parser.add_argument("--right", type=str, default="right", help="Tecla para o movimento 'right'")
    args = parser.parse_args()

    custom_key_mappings = {
        "up": args.up,
        "down": args.down,
        "left": args.left,
        "right": args.right,
        # "center" continua não fazendo nada (None)
    }

    print("[INFO] Mapeamentos de tecla utilizados:", custom_key_mappings)
    main(key_mappings=custom_key_mappings)