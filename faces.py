# faces.py
import os
import face_recognition
from PIL import Image, ImageDraw
import numpy as np

KNOWN_ENCODINGS_FILE = "known_encodings.npz"

def save_uploaded_file(uploaded_file, target_dir):
    filename = uploaded_file.name
    target_path = os.path.join(target_dir, filename)
    with open(target_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return target_path

def encode_known_faces(known_dir="known_faces"):
    labels = []
    encodings = []
    for fname in os.listdir(known_dir):
        if not fname.lower().endswith((".jpg",".jpeg",".png")):
            continue
        path = os.path.join(known_dir, fname)
        label = os.path.splitext(fname)[0]
        image = face_recognition.load_image_file(path)
        face_locations = face_recognition.face_locations(image)
        if len(face_locations) == 0:
            print(f"No face found in {fname}; skipping.")
            continue
        face_encoding = face_recognition.face_encodings(image, known_face_locations=face_locations)[0]
        labels.append(label)
        encodings.append(face_encoding)
    if encodings:
        np_enc = np.stack(encodings)
        np.savez(KNOWN_ENCODINGS_FILE, encodings=np_enc, labels=np.array(labels))
    return len(encodings)

def load_known_encodings():
    if not os.path.exists(KNOWN_ENCODINGS_FILE):
        return [], []
    data = np.load(KNOWN_ENCODINGS_FILE, allow_pickle=True)
    encodings = data["encodings"]
    labels = data["labels"].tolist()
    return encodings, labels

def recognize_faces_in_image(image_path, tolerance=0.5):
    known_encodings, known_labels = load_known_encodings()
    if len(known_encodings) == 0:
        return None, []

    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    matches = []
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_idx = int(np.argmin(distances))
        best_distance = float(distances[best_idx])
        if best_distance <= tolerance:
            name = known_labels[best_idx]
        else:
            name = "Unknown"
        draw.rectangle(((left, top), (right, bottom)), outline=(0,255,0), width=3)
        draw.text((left, bottom + 5), f"{name} ({best_distance:.2f})", fill=(255,255,255))
        matches.append((name, best_distance))
    del draw
    annotated_path = image_path + ".annotated.jpg"
    pil_image.save(annotated_path)
    return annotated_path, matches
