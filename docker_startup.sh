#!/bin/bash
while !/dev/tcp/db/3306
do
    sleep 1
done
pip install requests
pip install numpy
python manage.py makemigrations
python manage.py migrate
root="$(python manage.py shell -c """from django.contrib.auth.models import User; print(User.objects.filter(username='root').exists())""")"
if [ "$root" != "True" ]
then
  python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'a@b.c', 'root')"
fi
python manage.py runserver 0.0.0.0:8000
