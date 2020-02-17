
# Group23-Backend
This is the code for the Django web server of the software engineering project. 

## Deployment
The code has been already deployed and may be accessed via the following URL:
https://group23.dcs.warwick.ac.uk/ (see documentation for usage).

### Local Deployment
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


## Testing
Tests can be run by performing the command: `python manage.py test`.
Tests are written within the ./api/tests.py file.