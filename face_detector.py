import cv2
import pyautogui
import mediapipe as mp
import time

def dashed_line(img, pt1, pt2, color, thickness=1, dash_length=10):
    x1, y1 = pt1
    x2, y2 = pt2

    dist = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

    dashes = int(dist // dash_length)

    for i in range(dashes + 1):
        start_x = int(x1 + (x2 - x1) * i / dashes)
        start_y = int(y1 + (y2 - y1) * i / dashes)
        end_x = int(x1 + (x2 - x1) * (i + 0.5) / dashes)
        end_y = int(y1 + (y2 - y1) * (i + 0.5) / dashes)

        cv2.line(img, (start_x, start_y), (end_x, end_y), color, thickness)

#-twarz-------------------------------------------------------------------------- #
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cam = cv2.VideoCapture(0)
#-Dłoń--------------------------------------------------------------------------- #
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils
#-Dłoń--------------------------------------------------------------------------- #
last_click = 0.0 
click_cooldown = 0.5


if not cam.isOpened(): # Kamerka nie została otworzona 
    print("Nie wykryto kamerki")
    exit()

#-Główna pętla------------------------------------------------------------------- #
while True:
    ret, frame = cam.read()
    if not ret:
        print("Nie wykryto kamerki")
        break

    frame = cv2.flip(frame, 1)
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #--- Rysowanie siatki ------------------------------------------------------- #
    h_frame, w_frame, _ = frame.shape
    cell_w = w_frame // 3
    cell_h = h_frame // 3

    dashed_line(frame, (cell_w, 0), (cell_w, h_frame), (255, 0, 0), 1, 30)
    dashed_line(frame, (2*cell_w, 0), (2*cell_w, h_frame), (255, 0, 0), 1, 30)

    dashed_line(frame, (0, cell_h), (w_frame, cell_h), (255, 0, 0), 1, 30)
    dashed_line(frame, (0, 2*cell_h), (w_frame, 2*cell_h), (255, 0, 0), 1, 30)
    
    #-Detekcja twarzy ----------------------------------------------------------- #
    face_detection = face_cascade.detectMultiScale(
        grey_frame,
        scaleFactor= 1.1,
        minNeighbors= 3,
        minSize= (18, 18)
    )

    #-Obrys twarzy -------------------------------------------------------------- #
    face_points = None

    for (x, y, w, h) in face_detection:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 128, 0), 2)
        cv2.putText(frame, 'Face detected', (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 128, 0), 2)

        points_p = {
            "top_left": (x, y),
            "top_right": (x + w, y),
            "bottom_left": (x, y + h),
            "bottom_right": (x + w, y + h),
            "middle_top": (x + w // 2, y),
            "middle_bottom": (x + w // 2, y + h),
            "middle_left": (x, y + h // 2),
            "middle_right": (x + w, y + h // 2)
        }

        center_x = x + w // 2
        center_y = y + h // 2
        points_p["center"] = (center_x, center_y)

        for name, point in points_p.items():
            if name != "center":
                cv2.circle(frame, point, 4,(57, 255, 20), -1)

        cv2.line(frame, (center_x - 12, center_y), (center_x + 12, center_y),
                (0, 215, 255), 1, cv2.LINE_AA)
        cv2.line(frame, (center_x, center_y - 12), (center_x, center_y + 12),
                (0, 215, 255), 1, cv2.LINE_AA)
        
        #-Sterowanie kursorem ------------------------------------------------------ #
        if points_p:
            col_position = 1 if center_x < cell_w else 2 if center_x < 2 * cell_w else 3
            row_position = 1 if center_y < cell_h else 2 if center_y < 2 * cell_h else 3

            center_cell_x = cell_w + cell_w // 2
            center_cell_y = cell_h + cell_h // 2

            dx = center_x - center_cell_x
            dy = center_y - center_cell_y

            if abs(dx) < 10:
                dx = 0
            if abs(dy) < 10:
                dy = 0

            move_x = int(dx * 0.4)
            move_y = int(dy * 0.4)

            if move_x != 0 or move_y != 0:
                pyautogui.moveRel(move_x, move_y)

            cv2.putText(frame, f"Grid pos: ({col_position}, {row_position})",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
    #- Wykrywanie dłoni------------------------------------------------------------------- #
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # współrzędne dłoni
            x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w_frame)
            y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h_frame)
            x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w_frame)
            y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h_frame)

            center_hand_x = (x_min + x_max) // 2
            center_hand_y = (y_min + y_max) // 2

            col_position_hand = 1 if center_hand_x < cell_w else 2 if center_hand_x < 2 * cell_w else 3
            row_position_hand = 1 if center_hand_y < cell_h else 2 if center_hand_y < 2 * cell_h else 3

        if (col_position_hand, row_position_hand) in [(1, 2), (3, 2)]:
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(frame, "Hand", (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        current_time = time.time()
        if current_time - last_click > click_cooldown:
            if (col_position_hand == 1 and row_position_hand == 2):
                pyautogui.mouseDown(button='left')
                pyautogui.mouseUp(button='left')
                print("Klik lewy")

            elif (col_position_hand == 3 and row_position_hand == 2):
                pyautogui.mouseDown(button='right')
                pyautogui.mouseUp(button='right')
                print("Klik prawy")
                                
    cv2.imshow("Interface", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Wychodzenie z programu")
        break

cam.release()
cv2.destroyAllWindows()