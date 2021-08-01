# MeetingSchedulingSystem
A simple web application to maintain and schedule meetings for a business. The system provides support for both admin and client users. 



**Dependencies:**

The system is built using  [Python 3.8.10](https://www.python.org/downloads/). The system will also make use of the [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [SQLAlchemy](https://www.sqlalchemy.org/) modules. Flask is a micro web development framework and SQLAlchemy is a SQL toolkit. Both can be installed via pip, as shown below.

```shell
pip install Flask
pip install SQLAlchemy
```

You may also need to install the following packages as well:

```shell
pip install Flask-WTF
pip install WTForms
pip install email_validator
pip install flask_sqlalchemy
```

Windows users will most likely need to set the appropriate path variable, if there is a warning message after the pip install for flask that the failure to set path. The path should be similar to below.

```
C:\Users\Zachery Smith\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\LocalCache\local-packages\Python38\Scripts
```



In order to run the system via the command line an environment variable must be created. 

For MacOS/Unix:

```shell
export FLASK_APP = app.py
```

For Windows cmd:

```shell
set FLASK_APP = app.py
```

For Windows PowerShell:

```shell
$env:FLASK_APP = "app.py"
```

You can then run the application via the command line by using:

```shell
flask run
```

You can also run the application using python: 

```shell
python app.py
```



**Database Testing:**

For development/testing with the database you can run the `builddb.py` script to add data to the database and also as a means of resetting the database. For dynamic testing with the database, please use the following commands to help query the database after you have dynamically added data to it. 

```shell
PS C:\Users\Zachery Smith\Desktop\Documents\Behrend\SWENG455\Project\MeetingSchedulingSystem> python .\builddb.py
PS C:\Users\Zachery Smith\Desktop\Documents\Behrend\SWENG455\Project\MeetingSchedulingSystem> python 
Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from mss import db 
>>> from mss.models import *
>>> db.session.query(User).filter(User.email == 'zachery.smith@pss.com').first()    
Admin: Zachery Smith
>>> exit()
```









