Aplikacja jest uruchamiana w kontenerze Docker przy użyciu gunicorn. <br>

W celu przygotowania należy uruchomić następujące polecenie w folderze głównym aplikacji: <br/>
* docker compose run api python manage.py createsuperuser<br>

Następnie w konsoli wpisać potrzebne dane do utworzenia konta administratora<br>

Aby uruchomić kontener i aplikację należy użyć polecenie
* docker compose run

Uwierzytelnianie odbywa się za pomocą Basic Authentication
Adres do komunikacji to http://127.0.0.1:8000/api
