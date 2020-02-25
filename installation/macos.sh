#!/bin/zsh

# Ensure Python >=3.6 is installed
python_version="$(python3 -c 'import sys; print(sys.version_info>=(3,6))')" || { echo "Python 3 isn't installed."; exit 1; }
if [ "$python_version" == "True" ]
then
  echo "✓ Python >= 3.6 exists"
else
  echo "Your version of Python does not meet the minimum requirement of 3.6."
  exit 1
fi

# Ensure homebrew is installed
if [ $(command -v brew) != "" ]
then
  echo "✓ Homebrew exists"
else
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  echo "✓ Installed Homebrew"
fi

# Ensure MySQL is installed
if brew ls --versions mysql > /dev/null
then
  echo "✓ MySQL"
else
  brew install mysql
  echo "✓ Installed MySQL"
fi

# Ensure MySQL service started
brew services start mysql > /dev/null
echo "✓ Started MySQL"

# Ensure database exists
echo "CREATE DATABASE IF NOT EXISTS group23db;" | mysql -u root
echo "✓ Created group23db if it doesn't exist"

# Update .env 
echo $"DB_NAME='group23db'\nDB_USER='root'\nDB_PASSWORD=''\nDB_HOST='localhost'" > ../backend/.env

# Install backend requirements
pip3 install -r requirements.txt > /dev/null
if [ "$?" == "1" ]
then
  echo "✗ Error occured installing backend requirements."
  echo "Try: pip3 install -r requirements.txt"
  exit 1
else
  echo "✓ Installed backend requirements"
fi

# Install access requirements
pip3 install -r access/requirements.txt > /dev/null
if [ "$?" == "1" ]
then
  echo "✗ Error occured installing access requirements."
  echo "Try: pip3 install -r access/requirements.txt"
  exit 1
else
  echo "✓ Installed access requirements"
fi

# Create tables & superuser
python3 manage.py migrate > /dev/null
if [ "$?" == "1" ]
then
  echo "✗ Error occured making database tables."
  echo "Try: python3 manage.py migrate"
  exit 1
else
  echo "✓ Created database tables"
fi

root="$(python3 manage.py shell -c """from django.contrib.auth.models import User; print(User.objects.filter(username='root').exists())""")"
if [ "$root" == "True" ]
then
  echo "✓ User root exists"
else
  python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'a@b.c', 'root')"
  echo "✓ Created root user"
fi

exit 0
