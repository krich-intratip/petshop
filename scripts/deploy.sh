#!/usr/bin/env bash
# deploy.sh — Deploy petshop to DigitalOcean droplet
# Usage: ./scripts/deploy.sh [DROPLET_IP]
#
# Prerequisites on the droplet:
#   - Docker + Docker Compose installed
#   - Project cloned from GitHub
#   - docker.env configured with DJANGO_SECRET_KEY + DJANGO_ALLOWED_HOSTS

set -euo pipefail

DROPLET_IP="${1:?Usage: $0 DROPLET_IP}"
REMOTE="root@${DROPLET_IP}"
PROJECT_DIR="/root/petshop"

echo "=== Deploying to ${DROPLET_IP} ==="

echo ">>> Pushing code to droplet..."
rsync -avz --delete \
  --exclude='env/' \
  --exclude='.git/' \
  --exclude='db.sqlite3' \
  --exclude='__pycache__/' \
  --exclude='media/_tmp_import/' \
  ./ "${REMOTE}:${PROJECT_DIR}/"

echo ">>> Building and starting containers..."
ssh "${REMOTE}" "cd ${PROJECT_DIR} && \
  docker compose --profile prod down && \
  docker compose --profile prod up --build -d"

echo ">>> Waiting for containers to start..."
sleep 10

echo ">>> Checking container status..."
ssh "${REMOTE}" "cd ${PROJECT_DIR} && docker compose --profile prod ps"

echo ""
echo "=== Deploy complete! ==="
echo ">>> Website: http://${DROPLET_IP}/"
echo ">>> Admin:   http://${DROPLET_IP}/admin/"
echo ""
echo "NOTE: If media images are missing, run on the droplet:"
echo "  ssh ${REMOTE}"
echo "  cd ${PROJECT_DIR}"
echo "  docker compose --profile prod exec web python manage.py shell -c \"exec(open('scripts/seed_all.py', encoding='utf-8').read())\""
