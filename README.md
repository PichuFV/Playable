# Playable

Aplicação que permite **controlar jogos usando movimentos da cabeça** capturados pela webcam.  
Os comandos reconhecidos são: **up, down, left, right e center**, mapeados para as setas do teclado.

O repositório está organizado em duas abordagens:

- `classification/` → versão atual (recomendada), usando **YOLOv8-Classification** treinado no dataset **BIWI Head Pose** processado.
- `object_detection/` → versão inicial, usando **YOLOv8 Object Detection** com bounding boxes rotuladas manualmente.

---

## ⚙️ Tecnologias utilizadas

- **Python 3**
- **YOLOv8 (Ultralytics)** – classificação e detecção
- **OpenCV** – captura de vídeo da webcam
- **keyboard** (ou `pynput`) – envio das teclas de seta para o sistema
- **Roboflow** – preparação e download do dataset de classificação
- Dataset base: **BIWI Kinect Head Pose Database**

---

## 💻 Pré-requisitos

- Python 3.9+ instalado
- `pip` funcionando
- Webcam conectada
- (Opcional) Ambiente virtual (`venv`)

---

## 🚀 Como rodar

- Abra um terminal (**cmd** ou PowerShell)
- Acesse a pasta do projeto: cd PlayAble\classification
- Instale as dependências: pip install ultralytics opencv-python keyboard
- Execute o script: python playable_yolo_v2.py

---

## 👥 Autores
- Fabio Vivarelli
- Joao Vitor Gimenes dos Santos
- Nathan Henrique Guimaraes de Oliveira

🔗 link documento: 
https://docs.google.com/document/d/1wMyEvz9D6zS1NS_ht-npzFNCHC1FpZvB/edit?usp=sharing&ouid=108627184187957663801&rtpof=true&sd=true
