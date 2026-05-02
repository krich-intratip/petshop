#!/bin/sh
set -e
mkdir -p /app/media
if [ -n "$DJANGO_SQLITE_PATH" ]; then
  mkdir -p "$(dirname "$DJANGO_SQLITE_PATH")"
fi
python manage.py migrate --noinput

SEED_MARKER=/app/media/.seeded
if [ ! -f "$SEED_MARKER" ]; then
  echo "=== First run: seeding database ==="
  python manage.py shell -c "exec(open('scripts/seed_all.py', encoding='utf-8').read())" || echo "Seed failed — continuing anyway"
  touch "$SEED_MARKER"
  echo "=== Seed complete ==="
fi

if [ -n "$DJANGO_ENABLE_WHITENOISE" ]; then
  python manage.py collectstatic --noinput 2>/dev/null || true
fi

exec "$@"
