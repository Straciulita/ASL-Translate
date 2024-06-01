import pickle
import os
import numpy as np
import cv2
import mediapipe as mp
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Inițializarea Mediapipe pentru detectarea mainilor
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Configurarea Mediapipe pentru detectarea statica a imaginilor si setarea pragului de detecție
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Definirea directorului în care sunt stocate datele
DATA_DIR = './data'

# Inițializarea listelor pentru stocarea datelor și etichetelor
data = []
labels = []

try:
    # Iterarea prin fiecare director din directorul de date
    for dir_ in os.listdir(DATA_DIR):
        # Iterarea prin fiecare imagine din directorul curent
        for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
            data_aux = []  # Lista auxiliara pentru stocarea datelor pentru fiecare imagine
            x_ = []  # Lista auxiliara pentru stocarea coordonatelor x
            y_ = []  # Lista auxiliara pentru stocarea coordonatelor y

            # Citirea imaginii
            img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Procesarea imaginii cu Mediapipe Hands
            results = hands.process(img_rgb)
            if results.multi_hand_landmarks:
                # Iterarea prin fiecare mana detectata in imagine
                for hand_landmarks in results.multi_hand_landmarks:
                    # Iterarea prin fiecare punct de reper al mainii
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y

                        x_.append(x)
                        y_.append(y)

                    # Calcularea pozitiei relative a fiecarui punct de reper fata de marginea stanga-sus
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                # Adaugarea datelor și etichetei corespunzatoare in listele finale
                data.append(data_aux)
                labels.append(dir_)

    # Ajustarea dimensiunilor fiecărui eșantion la dimensiunea maximă
    max_len = max(len(sample) for sample in data)
    data_adjusted = []
    for sample in data:
        if len(sample) < max_len:
            sample += [0] * (max_len - len(sample))
        data_adjusted.append(sample)

    # Conversia listelor de date și etichete în numpy arrays
    data = np.array(data_adjusted)
    labels = np.array(labels)

    # Salvarea datelor și etichetelor intr-un fișier Pickle
    with open('data.pickle', 'wb') as f:
        pickle.dump({'data': data, 'labels': labels}, f)

except Exception as e:
    print(f"Eroare: {e}")

# Divizarea datelor în setul de antrenare și cel de testare
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Scalarea datelor pentru a le aduce la aceeași scară
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

# Antrenarea modelului RandomForestClassifier
model = RandomForestClassifier()
model.fit(x_train_scaled, y_train)

# Evaluarea performanței modelului
y_predict = model.predict(x_test_scaled)
score = accuracy_score(y_predict, y_test)
print('{}% of samples were classified correctly !'.format(score * 100))

# Salvarea modelului antrenat și a scaler-ului în fișierul "model.p"
with open('model.p', 'wb') as f:
    pickle.dump({'model': model, 'scaler': scaler}, f)
