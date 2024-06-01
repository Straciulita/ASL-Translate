import os
import cv2
import mediapipe as mp

# Initializarea Mediapipe pentru detectarea mainilor
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Definirea directorului in care vor fi stocate datele
DATA_DIR = './data'

# Numarul total de clase
number_of_classes = 31
# Numarul total de imagini pentru fiecare clasa
dataset_size = 50

# Capturarea video de la camera web (indexul 0 pentru prima cameră disponibila)
cap = cv2.VideoCapture(0)

# Inițializarea detectorului de mâini
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Iterarea prin fiecare clasa pentru a colecta datele
for j in range(number_of_classes):
    # Verificarea dacă directorul pentru clasa curentă există și, dacă nu, crearea lui
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    # Afisarea unui mesaj pe ecran pentru utilizator
    print('Collecting data for class {}'.format(j))

    # Așteptarea ca utilizatorul să fie pregătit să colecteze datele și să apese tasta 'q'
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)

        # Detectarea mâinii în imagine
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Desenarea punctelor de reper ale mâinii pe imagine
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    # Colectarea datelor pentru clasa curenta
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        # Salvarea imaginii în directorul corespunzător clasei și cu un nume de fișier unic
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)

        # Detectarea mâinii în imagine
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Desenarea punctelor de reper ale mâinii pe imagine
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('frame', frame)
        cv2.waitKey(25)

        counter += 1

# Eliberarea resurselor și închiderea ferestrelor OpenCV
cap.release()
cv2.destroyAllWindows()
