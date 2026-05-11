# Eyetracking System – Drowsiness Detection

System wizyjnej analizy stanu kierowcy, wykrywający oznaki zmęczenia na podstawie parametrów EAR (Eye Aspect Ratio) i PERCLOS (Percentage of Eye Closure).

## Funkcjonalności

- Detekcja twarzy i oczu z wykorzystaniem `dlib` oraz 68-punktowego modelu landmarków
- Dynamiczna kalibracja progu EAR przez interfejs użytkownika
- Obliczanie PERCLOS w przesuwnym oknie czasowym
- Nakładka OSD (On-Screen Display) z danymi w czasie rzeczywistym
- Wykres PERCLOS z progiem alarmowym i osią czasu
- Logowanie danych: zapis sekwencji wideo (`.avi`) i statystyk (`.csv`) do katalogu `logs/`

## Wymagania

- Python 3.10.12 (zalecany)
- Kamera (wbudowana lub USB)
- Dobre oświetlenie

# Instalacja

## Utworzenie środowiska wirtualnego
python3 -m venv venv

## Aktywacja (Linux / macOS)
source venv/bin/activate

## Aktywacja (Windows)
venv\Scripts\activate

## Instalacja zależności (należy odczekać dłuższą chwilę ok. 10 min)
pip install -r requirements.txt

# Instrukcja Obsługi

## Uruchomienie
python3 eye_tracking.py

## Kalibracja
Aplikacja umożliwia kalibrację progu EAR pod streukturę oka. Po uruchomieniu można wybrać przycisk "CALIBRATE" w oknie "Settings". System automatycznie wyliczy optymalny próg EAR, po kilku sekundach patrzenia na wprost kamery (należy unikać mrugania).

## Alarm 
Gdy parametr PERCLOS przekroczy ustawiony próg, system wygeneruje sygnał dźwiękowy oraz wyświetli czerwony alert na ekranie.

## Ustawienia: 
Za pomocą suwaków w oknie "Settings" można ręcznie modyfikować parametry w czasie rzeczywistym.

## Reset
Za pomocą przycisku "RESET" można wyzerować w oknie czasowym mrugnięcia i zliczony PERCLOS.

## Wyjście 
Należy nacisnąć klawisz ESC w oknie wideo, aby bezpiecznie zamknąć aplikację i zapisać logi.

# Struktura Projektu

- eye_tracking.py - Główny skrypt uruchomieniowy.
- utils/ear.py - Klasa EARManager (obliczenia i kalibracja).
- utils/perclos.py - Klasa Perclos (logika okna przesuwnego).
- utils/logger.py - Obsługa zapisu danych, OSD i wykresów.
- utils/settings.py - GUI do obsługi ustawień i przycisków.
- utils/face_module.py - Obsługa kamery i dlib.
- logs/ - Katalog na wygenerowane pliki logów i wideo.
