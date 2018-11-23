# Udacity Item Catalog
Udaciry FSND Fourth project
This is a full stack app built with python flask, sqlalchemy and jinja2, users are able to log in using their google account through oauth. authenticated user can create/edit/delete item's 




## screenshots
index:
![](https://i.imgur.com/NsqCs1E.png) 


add item:
![](https://i.imgur.com/P3VgWle.png) 

item preview:
![](https://i.imgur.com/Danh34u.png) 



## Obtaining Google OAuth Cred

* Create a project in https://console.developers.google.com
* go to Credentials -> OAuth consent screen and fill it with the appropriate information
* go to Credentials -> OAuth 2.0 client IDs and edit it to add your authorized javascript origins and authroized redirect urls, my app work with http://localhost:5000/ in both fields.
* download the config and place it in the root directory of the project


## Install & Run
* Python 2.7
* install project dependencies:
	`pip install -r requirements.txt`
* create database and populate it.
`python database_setup.py`
`python database_populate.py`

* Run
`python project.py`

* visit http://localhost:5000/ 

## Notes
I implemented the image handling for items images,
and used the random string generation used in the course to defend against csrf attack.

## Reference
the google oauth code used to authenticate the user is the same that was used in the course.
https://github.com/udacity/ud330

	
