import os
import json
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Wczytaj dane z JSON
with open("data.json", "r") as file:
    data = json.load(file)

images = []
labels = []

for idx, item in enumerate(data["items"]):
    genre = item["track"].get("genre")  # Bezpieczne pobieranie gatunku
    if not genre:
        continue  # Pomijamy elementy bez gatunku
    image_filename = f"image{idx}.jpg"  # Przyjmujemy format plików jako image0.jpg, image1.jpg, ...
    image_path = os.path.join("images", image_filename)
    if os.path.exists(image_path):
        images.append(image_path)
        labels.append(genre)
    else:
        print(f"Brak pliku: {image_filename}")

if not images or not labels:
    raise ValueError("Brak danych do przetworzenia! Upewnij się, że folder 'images' zawiera poprawne pliki.")

# Zakoduj etykiety
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)

# Wczytaj i przeskaluj obrazy
image_size = (128, 128)
X = []

for image_path in images:
    img = load_img(image_path, target_size=image_size)
    img_array = img_to_array(img) / 255.0
    X.append(img_array)

X = np.array(X)
y = tf.keras.utils.to_categorical(labels_encoded)

# Podziel dane na treningowe, walidacyjne i testowe
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)  # 70% trening, 30% reszta
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)  # 15% walidacja, 15% testy

# Zbuduj model CNN
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(label_encoder.classes_), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Trenowanie modelu
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=10,
    batch_size=32
)

# Testowanie modelu
print("\nOcena modelu na danych testowych:")
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Dokładność na zbiorze testowym: {test_accuracy * 100:.2f}%")

# Przykłady predykcji
print("\nPrzykładowe przewidywania:")
example_indices = np.random.choice(len(X_test), size=5, replace=False)  # 5 losowych przykładów
for i in example_indices:
    img_array = X_test[i]
    true_label = label_encoder.classes_[np.argmax(y_test[i])]
    predicted_label = label_encoder.classes_[np.argmax(model.predict(img_array[np.newaxis, ...]))]
    print(f"Prawdziwy gatunek: {true_label}, Przewidywany gatunek: {predicted_label}")

# Zapisz model i label_encoder
model.save("genre_prediction_model.h5")
with open("label_encoder.json", "w") as f:
    json.dump(label_encoder.classes_.tolist(), f)
