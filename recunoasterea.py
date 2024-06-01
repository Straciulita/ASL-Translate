import pickle
import cv2
import mediapipe as mp
import numpy as np
import time
import warnings

# Suprimarea mesajelor de avertisment
warnings.filterwarnings("ignore")

# Încărcarea modelului și a scaler-ului din fișierele pickle
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']
scaler = model_dict['scaler']

# Capturarea video de la camera web (indexul 0 pentru prima cameră disponibilă)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Nu s-a putut deschide camera.")
    exit()

# Initializarea Mediapipe pentru detectarea mainilor
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3, max_num_hands=2)  # Configurarea Mediapipe

# Dicționarul de etichete pentru caracterul prezis
labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'TE IUBESC', 26:'DA', 27:'NU', 28:'SPATIU', 29:'STERGE', 30:'MULTUMESC'}

# Variabile pentru gestionarea timpului
start_time = time.time()
interval_sec = 2  # Intervalul de timp în secunde între afișarea literei detectate

# Bucla infinită pentru captura video și procesarea datelor
while True:
    ret, frame = cap.read()  # Capturați cadru

    H, W, _ = frame.shape  # Dimensiunile cadrului

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertiți în RGB

    results = hands.process(frame_rgb)  # Procesarea datelor cu Mediapipe Hands

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            data_aux = []  # Lista pentru stocarea datelor pentru fiecare mână
            x_ = []  # Lista pentru stocarea coordonatelor x
            y_ = []  # Lista pentru stocarea coordonatelor y

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

                # Desenarea punctelor de reper pe imagine
                cx = int(x * W)
                cy = int(y * H)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)  # Desenați un cerc pentru fiecare punct de reper

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

            # Verificați dacă datele auxiliare au dimensiunea corectă pentru scalare
            if len(data_aux) == 42:
                data_aux = np.array(data_aux + [0] * 42).reshape(1, -1)
                # Aplicați scalarea pe datele auxiliare
                data_aux_scaled = scaler.transform(data_aux)

                # Predicția caracterului
                prediction = model.predict(data_aux_scaled)

                predicted_character = labels_dict[int(prediction[0])]  # Eticheta prezisă

                # Desenarea dreptunghiului în jurul mâinii
                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)

                # Afișarea etichetei mâinii detectate
                cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

                # Verificarea dacă a trecut intervalul de timp și afișarea literei în fișier
                if time.time() - start_time >= interval_sec:
                    with open('output.txt', 'a') as f:
                        if predicted_character == 'SPATIU':
                            f.write(" ")
                        elif predicted_character == 'STERGE':
                            f.seek(f.tell() - 1, 0)
                            f.truncate()
                        else:
                            f.write(predicted_character)
                    start_time = time.time()  # Reinițializarea timpului de start

    # Afișarea cadrului
    cv2.imshow('frame', frame)

    # Așteptarea apăsării tastei 'q' pentru a ieși din buclă
    if cv2.waitKey(25) == ord('q'):
        break

# Eliberarea resurselor
cap.release()
cv2.destroyAllWindows()
