set -e

flask --app src.app db upgrade
gunicorn src.app:app 