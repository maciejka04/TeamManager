# TeamManager – System Zarządzania Zespołem

Aplikacja webowa oparta na frameworku Django, umożliwiająca zarządzanie zespołami, projektami oraz zadaniami. Projekt realizuje wymagania dotyczące izolacji danych między zespołami, tablicy Kanban oraz integracji z zewnętrznymi systemami poprzez REST API.

---

## Funkcjonalności

### 1. Użytkownicy i Profile
* **System Kont:** Rejestracja, logowanie oraz resetowanie hasła (linki widoczne w konsoli serwera).
* **Profil Użytkownika:** Edycja danych ("O mnie") oraz wgrywanie awatara (ImageField) widocznego przy zadaniach.

### 2. Struktura Organizacyjna
* **Zespoły:** Możliwość tworzenia zespołów (twórca zostaje właścicielem).
* **Członkostwo:** Właściciel może dodawać innych użytkowników do zespołu przez login/email.
* **Projekty:** Grupowanie zadań w ramach konkretnych zespołów.
* **Izolacja:** Użytkownik ma dostęp tylko do danych zespołów, do których należy (zabezpieczenie 403/404).

### 3. Zarządzanie Zadaniami (Kanban)
* **Tablica Projektu:** Zadania wyświetlane w kolumnach (To Do, In Progress, Done).
* **Szczegóły:** Tytuł, opis, priorytet (High/Medium/Low), data wykonania (Due Date).
* **Interakcja:** Możliwość dodawania komentarzy oraz załączników (plików) do zadań.

### 4. Dashboard i API
* **Dashboard:** Widok startowy z listą zespołów i sekcją "Moje pilne zadania".
* **REST API:** * `GET /api/projects/{id}/stats/` – statystyki ukończenia zadań.
    * `GET /api/my-tasks/` – lista własnych zadań z filtrowaniem.
    * Uwierzytelnianie: JWT.
    * Dokumentacja: Swagger UI.

---

## Technologie i Wymagania Techniczne

* **Backend:** Django, Django Rest Framework.
* **Dokumentacja API:** drf-spectacular.
* **Linter:** Ruff (konfiguracja w pliku pyproject.toml / ruff.toml).
* **Baza danych:** SQLite (lub inna zgodna z Django).
* **Optymalizacja:** Zastosowanie `select_related` i `prefetch_related` w celu uniknięcia problemu N+1.

---

## Instalacja

### 1. Przygotowanie środowiska
```bash
# Stworzenie i aktywacja środowiska wirtualnego
python -m venv Venn
source venv/bin/activate  # Linux/macOS
# lub
venv\Scripts\activate     # Windows

# Instalacja zależności
pip install -r requirements.txt
```


### 2. Konfiguracja bazy i mediów
```bash
chmod +x manage.sh
./manage.sh migrate
./manage.sh createsuperuser
```

### 3. Budowanie i uruchomienie 
```bash
docker compose up --build

Aplikacja dostępna pod adresem http://0.0.0.0:8000/login
```
### 4. Jakość Kodu i Testy
```bash
docker-compose up -d 
docker-compose exec backend ruff check .
```
### 5. Testy Automatyczne
```bash
docker-compose up -d 
docker-compose exec backend python manage.py test
```
