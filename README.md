# Group23-Backend
This is the code for the Django web server of the software engineering project. 

## Deployment
The code has been already deployed and may be accessed via the following URL:
https://group23.dcs.warwick.ac.uk/ (see documentation for usage).


## Local Deployment
There are a couple or prerequisites that are required for the following guide:
1. Python >=3.6
2. pip
3. git  

If you're missing any of the above, you'll need to install these first.

The next step is to clone the repository. Open up your Terminal and paste the following command:  
&nbsp;&nbsp;&nbsp;&nbsp; `git clone https://github.com/tludlow/Group23-Backend.git backend`  
From your current directory, you'll now be able to navigate into 
the repository by navigating into it:  
&nbsp;&nbsp;&nbsp;&nbsp; `cd backend`  


The next step is to install a database server.

### macOS
This guide assumes you're using macOS Catalina or later in which the default shell is now ZSH.

The script `macos.sh` has been provided to simplify the next stages of installation & setup.

To execute this script, navigate to the root of your local clone of this repository using Terminal (you should already be there). Then paste:  
&nbsp;&nbsp;&nbsp;&nbsp; `sh installation/macos.sh`  
You'll be prompted with the scripts that'll be installed - simply accept this by pressing the RETURN key. 

In essence, this script:
1. installs [Homebrew](https://brew.sh) - a package manager for macOS
2. installs [MariaDB](https://mariadb.org) - the database server we're going to use
3. creates the database `group23db`, sets environmental variables with the database configuration (database, username, password, host), creates the required tables & installs the requirements.

You should now be able to run:  
&nbsp;&nbsp;&nbsp;&nbsp; `python3 manage.py runserver`  
without any issues. 

The server should be accessable via `http://localhost:8000/`.

See the data section to import the dataset to the database.

### Data
The caviat is that there is no data at present in the database. Data can be added in two ways.
* If you navigate to  `http://localhost:8000/admin/` and select a table, you can manually enter data manually.
* Alternatively, you can import the entire set by running:  
&nbsp;&nbsp;&nbsp;&nbsp; `python3 access/importer.py`  
Note: This will take a long time. You may quit the importer at any time using [ctrl][c] and whilst the derivative trades table won't be complete, it should prove a sufficent basis for development.


### Windows
ahahahaha. 

###
If you'd like to deploy the backend locally, clone the repository, 
install the dependencies:  
&nbsp;&nbsp;&nbsp;&nbsp; `pip3 install -r requirements.txt`  
and start then server:  
&nbsp;&nbsp;&nbsp;&nbsp; `python3 manage.py runserver`

## Documentation
API documentation may be accessed via: https://group23.dcs.warwick.ac.uk/docs/. It utilises [slate](https://github.com/slatedocs/slate) and the source directory is located `backend/docs/api`.

The database schema is located in the root of this repository titled: `schema.md`.

## Interaction
Two scripts have been provided for convenience to interact with the API . 

You'll need to install the dependencies first:  
&nbsp;&nbsp;&nbsp;&nbsp; `pip3 install -r access/requirements.txt`  

The following scripts are available:
* `access/query.py` - Provides access to the API via Python (see API
  documentation for usage).
* `access/importer.py` - Allows for the importing of data to the database.
