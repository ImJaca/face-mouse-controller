# Sterowanie myszką za pomocą ruchów twarzy i gestów dłoni

Aplikacja napisana w języku **Python**, umożliwiająca sterowanie kursorem myszy przy pomocy **ruchów głowy oraz gestów dłoni**, wykrywanych przez kamerę komputerową.

Program analizuje obraz z kamery w czasie rzeczywistym, wykrywa **twarz użytkownika oraz dłoń**, a następnie zamienia ich położenie na ruch kursora i kliknięcia myszy.

---

# Funkcjonalności

* sterowanie kursorem myszy za pomocą **ruchów głowy**
* wykonywanie **kliknięcia lewego i prawego przycisku myszy** przy pomocy gestów dłoni
* **detekcja twarzy w czasie rzeczywistym**
* **śledzenie dłoni przy użyciu MediaPipe**
* interfejs wizualny z **siatką sterowania 3×3**
* zabezpieczenie przed wielokrotnym kliknięciem (**cooldown**)

---

# Zasada działania

Program przetwarza kolejne klatki obrazu z kamery i analizuje je przy pomocy metod przetwarzania obrazu.

## 1. Uruchomienie kamery

Po uruchomieniu programu inicjalizowana jest kamera internetowa.
Jeśli kamera nie zostanie wykryta, w konsoli pojawia się odpowiedni komunikat.

Każda klatka obrazu jest:

* odbijana lustrzanie (aby sterowanie było bardziej intuicyjne),
* konwertowana do skali szarości na potrzeby detekcji twarzy.

---

## 2. Siatka sterowania

Na obraz z kamery nakładana jest **siatka 3×3** złożona z przerywanych linii.

Siatka pełni funkcję punktu odniesienia dla:

* ruchów twarzy
* położenia dłoni

Środkowa komórka siatki jest traktowana jako **pozycja neutralna kursora**.

---

## 3. Detekcja twarzy

Do wykrywania twarzy wykorzystany został klasyfikator **Haar Cascade** z biblioteki OpenCV.

Po wykryciu twarzy program:

* rysuje prostokąt wokół twarzy
* wyznacza jej środek
* oblicza punkty referencyjne

Środek twarzy jest następnie wykorzystywany do sterowania kursorem myszy.

---

## 4. Sterowanie kursorem

Pozycja środka twarzy jest porównywana ze środkiem siatki.

Na tej podstawie obliczane jest przesunięcie kursora.

Przykład działania:

| Ruch głowy | Ruch kursora   |
| ---------- | -------------- |
| w prawo    | kursor w prawo |
| w lewo     | kursor w lewo  |
| w górę     | kursor w górę  |
| w dół      | kursor w dół   |

Aby uniknąć drgania kursora zastosowano **minimalny próg ruchu** ignorujący bardzo małe przesunięcia.

Ruch kursora realizowany jest przy pomocy biblioteki **PyAutoGUI**.

---

## 5. Wykrywanie dłoni

Do detekcji dłoni wykorzystano bibliotekę **MediaPipe Hands**, która wykrywa **21 punktów charakterystycznych dłoni**.

Na podstawie tych punktów obliczany jest:

* obszar dłoni
* środek dłoni
* pozycja dłoni względem siatki sterowania

---

## 6. Gesty kliknięcia

Kliknięcia myszy wykonywane są poprzez umieszczenie dłoni w odpowiednim polu siatki.

| Pozycja dłoni w siatce       | Akcja                               |
| ---------------------------- | ----------------------------------- |
| lewa środkowa komórka (1,2)  | kliknięcie lewym przyciskiem myszy  |
| prawa środkowa komórka (3,2) | kliknięcie prawym przyciskiem myszy |

Aby zapobiec wielokrotnemu klikaniu zastosowano mechanizm **cooldown wynoszący 0.5 sekundy**.

---

# Interfejs programu

Okno aplikacji wyświetla:

* obraz z kamery
* siatkę sterowania 3×3
* obrys wykrytej twarzy
* obrys wykrytej dłoni
* punkty referencyjne twarzy
* aktualną pozycję twarzy w siatce

Program można zakończyć naciskając klawisz:

q

---

# Wykorzystane biblioteki

Projekt został zrealizowany przy użyciu następujących bibliotek:

* Python
* OpenCV
* MediaPipe
* PyAutoGUI
