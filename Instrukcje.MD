# Dodanie interpretera w Pycharm
1. Prawy dolny klikamy na \<No interpreter>
2. Add new Interpreter -> On Docker Compose
3. Server: Docker \
Configuration files: wybieramy docker compose w lokalizacji naszego projektu \
Service: backend
4. Klikamy Next, i wybieramy System Interpretes z /usr/local/bin/python3
5. Po chwili powinien nam się pojawić Remote Python 3.X Docker Compose (backend)
# Konfiguracja django server
Jeżeli chcemy właczyć serwer przez pycharma wystarczy w pycharmie wybrać domyslny Django server configuration.
# Podłączenie bazy danych
Na pasku po prawej wybieramy Database, klikamy New i wybieramy postgresql.
Host: localhost
Port: 5432
Authentication: User & Password
User: Użytkownik z .env.db
Password: Password z .env.db
Db: Db z .env.db