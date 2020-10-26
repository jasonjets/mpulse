
#### mPulse Member Management
- 1 . CSV Batch Member Import. 
    a. Duplicates loaded into "Conflict" section

- 2 . Manual Add Members. 
    a. Duplicates return "Already exist
- 3 . Edit and Update Members


# Steps for Local Setup
``` 
 0. Create and start virtual env.

 1. git clone https://github.com/jasonjets/mpulse.git

 2.  cd into app folder

 3. pip3 install -r requirements.txt

 4. python3 manage.py migrate

 5. python3 manage.py runserver

 6. View http://127.0.0.1:8000

 6.a. May need $python manage.py migrate --run-syncdb

 7. Empty tables for re-test $python manage.py flush

May need $python manage.py migrate --run-syncdb

```
