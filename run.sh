sudo chown -R $USER:$USER .
appName=personal_journal

if [[ $1 == 'build' ]]; then
    docker image prune -f --all
    DOCKER_BUILDKIT=1 docker compose -f docker_compose.yml build
elif [[ $1 == 'start' ]]; then
    docker compose -f docker_compose.yml up --remove-orphans
elif [[ $1 == 'user' ]]; then
    docker compose -f docker_compose.yml exec $appName python manage.py createsuperuser --username=admin --email=personal_journal@gmail.com
fi
