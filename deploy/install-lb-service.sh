#!/usr/bin/env bash
# Install and enable the systemd service "lb" for the FastAPI backend on Ubuntu.
set -euo pipefail

SERVICE_NAME="lb"
SERVICE_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lb.service"
SERVICE_DST="/etc/systemd/system/${SERVICE_NAME}.service"
# Default: parent of deploy/ (the backend root), unless an absolute path is passed.
DEFAULT_APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="${1:-$DEFAULT_APP_DIR}"
UVICORN_BIN="${APP_DIR}/.venv/bin/uvicorn"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Run as root: sudo bash deploy/install-lb-service.sh [APP_DIR]"
  exit 1
fi

if [[ ! -f "${APP_DIR}/app/main.py" ]]; then
  echo "Backend not found at: ${APP_DIR}"
  echo "Your server path looks like: /var/www/api.lamborghinichile.cl/public_html"
  echo "Usage: sudo bash deploy/install-lb-service.sh /var/www/api.lamborghinichile.cl/public_html"
  exit 1
fi

if [[ ! -x "${UVICORN_BIN}" ]]; then
  echo "Missing venv/uvicorn at ${UVICORN_BIN}"
  echo "Create it first:"
  echo "  cd ${APP_DIR}"
  echo "  python3 -m venv .venv"
  echo "  .venv/bin/pip install -r requirements.txt"
  exit 1
fi

if [[ ! -f "${APP_DIR}/.env" ]]; then
  echo "Warning: ${APP_DIR}/.env not found. Copy .env.example and set production values."
fi

TMP_UNIT="$(mktemp)"
sed \
  -e "s|/opt/lb/backend|${APP_DIR}|g" \
  "${SERVICE_SRC}" > "${TMP_UNIT}"

install -m 644 "${TMP_UNIT}" "${SERVICE_DST}"
rm -f "${TMP_UNIT}"

# Ensure upload directory is writable by the service user
mkdir -p "${APP_DIR}/uploads"
chown -R www-data:www-data "${APP_DIR}/uploads" || true

systemctl daemon-reload
systemctl enable "${SERVICE_NAME}.service"
systemctl restart "${SERVICE_NAME}.service"
systemctl --no-pager --full status "${SERVICE_NAME}.service"

echo
echo "Service '${SERVICE_NAME}' installed and enabled (starts on boot)."
echo "Useful commands:"
echo "  sudo systemctl status ${SERVICE_NAME}"
echo "  sudo systemctl restart ${SERVICE_NAME}"
echo "  sudo journalctl -u ${SERVICE_NAME} -f"
