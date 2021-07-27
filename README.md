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







