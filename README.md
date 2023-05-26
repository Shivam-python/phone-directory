# phone-directory

# Pre-Requirement

Python
pip

# How to run the Application

Set Up a Virtual Environment https://docs.python.org/3/library/venv.html

- Install the requirements : 
    - pip install -r requirements.txt

- Migrate Project Model to the Database. Run following commands in order :  
    - python manage.py makemigrations
    - python manage.py migrate

- Run the Project 
    - python manage.py runserver


# 100 contacts dummy CSV has been added to import dummy contacts
- To import dummy contact for testing, run 
    - In linux/mac : python manage.py shell < import_contacts.py
    - In windows : python manage.py shell << import_contacts.py

