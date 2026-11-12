# Backend — Lamborghini Colección API

FastAPI service with layered architecture (API → services → repositories → domain).

## Database (local)

MySQL database `lb` as `root` without password:

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -e "CREATE DATABASE IF NOT EXISTS lb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

Connection (`.env`):

```env
DATABASE_URL=mysql+pymysql://root@127.0.0.1:3306/lb
PERSISTENCE=sql
```

### Migrations

```bash
cd backend
.\.venv\Scripts\activate
alembic upgrade head
```

## Run

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 7776
```

## Ubuntu production (`lb` systemd + MySQL)

Production path example: `/var/www/api.lamborghinichile.cl/public_html`

### MySQL (fix Ubuntu error 1698)

On Ubuntu, `root@localhost` uses socket auth, so PyMySQL cannot connect as `root`.
Create a dedicated user (run with `sudo mysql`):

```bash
sudo mysql -e "
CREATE DATABASE IF NOT EXISTS lb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'lb'@'localhost' IDENTIFIED BY 'CHANGE_ME_STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON lb.* TO 'lb'@'localhost';
FLUSH PRIVILEGES;
"
```

In `.env`:

```env
DATABASE_URL=mysql+pymysql://lb:CHANGE_ME_STRONG_PASSWORD@127.0.0.1:3306/lb
PERSISTENCE=sql
DEBUG=false
```

Then migrate:

```bash
cd /var/www/api.lamborghinichile.cl/public_html
.venv/bin/alembic upgrade head
```

### systemd service (`lb`)

```bash
cd /var/www/api.lamborghinichile.cl/public_html
sudo bash deploy/install-lb-service.sh
# or explicitly:
# sudo bash deploy/install-lb-service.sh /var/www/api.lamborghinichile.cl/public_html
```

Runs: `uvicorn app.main:app --host 0.0.0.0 --port 7776`

```bash
sudo systemctl status lb
sudo systemctl restart lb
sudo journalctl -u lb -f
```

Docs locally: `http://127.0.0.1:7776/docs`

### Reverse proxy (public HTTPS)

`https://api.lamborghinichile.cl/docs` only works if Apache/Nginx proxies to `127.0.0.1:7776`.
Sample configs: `deploy/apache-api.lamborghinichile.cl.conf` and `deploy/nginx-api.lamborghinichile.cl.conf`.

Detect web server:

```bash
sudo ss -tlnp | grep -E ':80|:443'
```

Apache quick path:

```bash
sudo a2enmod proxy proxy_http headers rewrite ssl
# Prefer editing the existing vhost for api.lamborghinichile.cl and add:
#   ProxyPreserveHost On
#   RequestHeader set X-Forwarded-Proto "https"
#   ProxyPass / http://127.0.0.1:7776/
#   ProxyPassReverse / http://127.0.0.1:7776/
sudo apache2ctl configtest && sudo systemctl reload apache2
```

## Tests

```bash
pytest
```

Tests force `PERSISTENCE=memory` via `tests/conftest.py`.

## Default admin

- Email: `admin@example.com`
- Password: `Admin123!`
