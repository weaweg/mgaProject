Aplikacja jest uruchamiana w kontenerze Docker przy użyciu gunicorn. <br>

W celu uruchomienia należy użyć następujących poleceń w folderze głównym aplikacji: <br/>
* docker compose up -d
* docker compose exec api python manage.py createsuperuser

Następnie w konsoli wpisać potrzebne dane do utworzenia konta administratora<br>

Uwierzytelnianie odbywa się za pomocą Basic Authentication
Adres do komunikacji to http://127.0.0.1:8000/api
