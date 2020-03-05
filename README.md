
# Group23-Backend

This is the code for the Django web server of the software engineering project.

## Contributing

There is now a basic overview of Django, what each file is for and ideas on how
to extend what we have at the moment. You can view the guide
[here](https://github.com/tludlow/Group23-Backend/blob/master/guide.pdf).

As well as this you can
[join Monday](https://group651.monday.com/users/sign_up?invitationId=8988391078060137000)
to see what else needs to be completed & more importantly, let others know what
you're doing so we don't end up with code duplication. The tasks listed at
present aren't conclusive, therefore, feel free to append.

Once you've completed coding a section, you should then make a pull request
(basics of this are mentioned in the guide, however, please ask if you're
struggling!).


## Cloning The Repository

First you need to fork the
[repository](https://github.com/tludlow/Group23-Backend) and press fork, this
will create your own copy.

The next step is to clone the repository. Open up your Terminal and paste the
following command (remember to insert your GitHub username):  
&nbsp;&nbsp;&nbsp;&nbsp;
`git clone https://github.com/<YOUR  GITHUB USERNAME>/Group23-Backend.git backend`

From your current directory, you'll now be able to navigate into your local
repository:   
&nbsp;&nbsp;&nbsp;&nbsp;
`cd backend`

Finally, you're going to want to add a remote parent to your local repository,
so that you can retrieve updates made by other group members:  
&nbsp;&nbsp;&nbsp;&nbsp;
`git remote add parent https://github.com/tludlow/Group23-Backend.git`

You can get any updates to the master branch using the following command (you'll
be alerted via Slack when a pull request has been merged):  
&nbsp;&nbsp;&nbsp;&nbsp;
`git pull parent master`


## Docker Deployment

Docker allows for multiple developers to create their code in the same environment
([read more](https://medium.com/better-programming/why-and-how-to-use-docker-for-development-a156c1de3b24)).


Assuming you're using macOS or Windows, you're going to need to install
[Docker Desktop](https://www.docker.com/products/docker-desktop).

In the root of the repository, you should be able to run:  
&nbsp;&nbsp;&nbsp;&nbsp;
`docker-compose up`

You can verify that the server is running via visiting: http://localhost:8000/.

The server can be stopped using [ctrl][c].

### Data
See the data section for the different ways to insert data.

* You can set the credentials to access the admin panel by running:  
&nbsp;&nbsp;&nbsp;&nbsp;
`docker-compose run web python manage.py createsuperuser`  
* To import the sample data set you'll need to run the following command:  
&nbsp;&nbsp;&nbsp;&nbsp;
`docker-compose run web bash -c "cd access; pip install -r requirements.txt; python importer.py"`

## Native Deployment

There are a couple or prerequisites that are required for the following guide:

1. Python >=3.6
2. pip

If you're missing any of the above, you'll need to install these first.

### Local Environment Variables
To connect to the database you must provide your database information inside of
a file named `.env` (within the root of the repository). The contents of this
file should be as follows:  
&nbsp;&nbsp;&nbsp;&nbsp; `DB_NAME="group23db"`  
&nbsp;&nbsp;&nbsp;&nbsp; `DB_USER=<USERNAME SET IN SETUP>`  
&nbsp;&nbsp;&nbsp;&nbsp; `DB_PASS=<PASSWORD SET IN SETUP>`  
&nbsp;&nbsp;&nbsp;&nbsp; `DB_HOST="localhost"`  
&nbsp;&nbsp;&nbsp;&nbsp; `DB_PORT="3306"`  
You should create the `.env` file in the root of the repository once you have
installed the database server.

The next step is to install a database server.

### macOS
This guide assumes you're using macOS Catalina or later in which the default
shell is ZSH.

The shell script `macos.sh` has been provided to simplify the next stages of
installation & setup.

To execute this script, navigate to the root of your local clone of this
repository using Terminal (you should already be there). Then paste:  
&nbsp;&nbsp;&nbsp;&nbsp;
`sh installation/macos.sh`

You may be prompted with the scripts that'll be installed - simply accept this
by pressing the RETURN key.

In essence, this script:

1. installs [Homebrew](https://brew.sh) - a package manager for macOS

2. installs [MySQL](https://www.mysql.com) - the database server we're going to
   use

3. creates the database `group23db`, creates the required tables & installs the
   requirements.

Now, create the `.env` file.

You should be able to run:  
&nbsp;&nbsp;&nbsp;&nbsp;
`python3 manage.py runserver`

The server should be accessable via: http://localhost:8000/.

NOTE: You're going to get a 404 error because there is currently no homepage.
You still have access to the API - see documentation for usage:
http://localhost:8000/docs/.

See the data section to import the dataset to the database.

### Windows
We're going to install MariaDB.

If you've got a 64-bit machine download:
[64-bit](https://downloads.mariadb.org/interstitial/mariadb-10.4.12/winx64-packages/mariadb-10.4.12-winx64.msi/from/http%3A//mariadb.mirror.triple-it.nl/)

If you've got a 32-bit machine download:
[32-bit](https://downloads.mariadb.org/interstitial/mariadb-10.4.12/win32-packages/mariadb-10.4.12-win32.msi/from/http%3A//mariadb.mirror.triple-it.nl/)

Follow the installation process by clicking `Next`. Upon reaching the `Default
instance properties`, set the password as `root` and continue clicking `Next`.

You'll have additional program `MySQL Client` installed. Open this and enter the
password `root`.

We need to create the group23db database. In order to do this copy the following
SQL:  
&nbsp;&nbsp;&nbsp;&nbsp;
`CREATE DATABASE IF NOT EXISTS group23db;`

You should get a response saying `Query OK`. If so, exit the program.
Open PowerShell and navigate to the root of the respository (if you've closed
it). We're going to install the requirements for our applications. There are two
sets of requirements - the main set for our Django application and another set
required by the scripts in `access`.  
&nbsp;&nbsp;&nbsp;&nbsp;
`pip3 install -r requirements.txt`  
&nbsp;&nbsp;&nbsp;&nbsp;
`pip3 install -r access/requirements.txt`

Now let's create the tables required by our application:  
&nbsp;&nbsp;&nbsp;&nbsp;
`python3 manage.py makemigrations`  
&nbsp;&nbsp;&nbsp;&nbsp;
`python3 manage.py migrate`

Finally, let's create a user so that you're able to access the admin panel.

Execute the following command and enter some credentials (e.g. root):  
&nbsp;&nbsp;&nbsp;&nbsp;
`python3 manage.py createsuperuser`

Now, create the `.env` file.

You should be able to run:  
&nbsp;&nbsp;&nbsp;&nbsp;
`python3 manage.py runserver`

The server should be accessable via: http://localhost:8000/.

NOTE: You're going to get a 404 error because there is currently no homepage.
You still have access to the API - see documentation for usage:
http://localhost:8000/docs/.

See the data section to import the dataset to the database.

### Notes
Once a pull request has been merged, the version deployment on the
DCS server will not automatically be updated.

## Data

Data can be added to the database in two ways.

* If you navigate to http://localhost:8000/admin/ and select a table, you can
enter data manually. The username and password if you've followed the above
installation steps will be `root`.

* Alternatively, you can import the entire data set. You can download it
[here](https://drive.google.com/open?id=1qUfmmqi22YMCp7R0KIyZfj4vKYw3PqcC).
Once downloaded, unzip the data set and place the unzipped directory `data` in
the root of your repository. Git will ignore both this directory and it's
zipped counterpart. You can then import the data set via executing:  
&nbsp;&nbsp;&nbsp;&nbsp;
`cd access`  
&nbsp;&nbsp;&nbsp;&nbsp;
`python3 importer.py`  
Note: This will take a long time. You may quit the importer at any time using
[ctrl][c] and whilst the derivative trades table won't be complete, it should
prove a sufficent basis for development.

## Documentation

API documentation may be accessed via: https://group23.dcs.warwick.ac.uk/docs/.
It utilises [slate](https://github.com/slatedocs/slate) and the source directory
is located `docs/api/source`.

## Interaction

Two scripts have been provided for convenience to interact with the API.
If you've followed the above setup then you'll already have the required
requirements, however, if you haven't you'll need to install first:  
&nbsp;&nbsp;&nbsp;&nbsp;
`pip3 install -r access/requirements.txt`

The following scripts are available:
*  `access/query.py` - Provides access to the API via Python (see API
documentation for usage).
*  `access/importer.py` - Allows for the importing of data to the database.

## Testing

Tests can be run by performing the command: `python3 manage.py test`. Tests are
written within the `api/tests.py` file.
