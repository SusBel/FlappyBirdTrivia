import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def face_id_scan(model):
    cap = cv2.VideoCapture(0)  # Open the camera
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
        
        cv2.imshow("Face ID Scan - Press 'q' to cancel", frame)
        if len(faces) > 0:
            model.face_scanned = True
            break  # Face detected
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # Cancel scanning on 'q'
    cap.release()
    cv2.destroyAllWindows()
