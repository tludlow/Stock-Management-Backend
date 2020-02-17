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
if brew services list | grep "mysql" > /dev/null
then
  echo "✓ MySQL is running"
else
  brew services start mysql
  echo "✓ Started MySQL"
fi

# Ensure database exists
echo "CREATE DATABASE IF NOT EXISTS group23db;" | mysql -u root
echo "✓ Created group23db if it doesn't exist"

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

if [ ! -f "~/.zshenv" ]
then
    touch ~/.zshenv
fi

# Ensure environmental variables are set
name="$(grep 'DB_NAME' ~/.zshenv)"
if [ "$name" != "" ]
then
  echo "✓ Environmental variable exists: DB_NAME"
else
  echo $"DB_NAME='group23db'\nexport DB_NAME" >> ~/.zshenv
  echo "✓ Environmental variable set: DB_NAME"
fi

user="$(grep 'DB_USER' ~/.zshenv)"
if [ "$user" != "" ]
then
  echo "✓ Environmental variable exists: DB_USER"
else
  echo $"DB_USER='root'\nexport DB_USER" >> ~/.zshenv
  echo "✓ Environmental variable set: DB_USER"
fi

password="$(grep 'DB_PASSWORD' ~/.zshenv)"
if [ "$password" != "" ]
then
  echo "✓ Environmental variable exists: DB_PASSWORD"
else
  echo $"DB_PASSWORD=''\nexport DB_PASSWORD" >> ~/.zshenv
  echo "✓ Environmental variable set: DB_PASSWORD"
fi

host="$(grep 'DB_HOST' ~/.zshenv)"
if [ "$host" != "" ]
then
  echo "✓ Environmental variable exists: DB_HOST"
else
  echo $"DB_HOST='localhost'\nexport DB_HOST" >> ~/.zshenv
  echo "✓ Environmental variable set: DB_HOST"
fi

# Load new environmenal variables
source ~/.zshenv

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
