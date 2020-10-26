
#### Key Features
- 1 . CSV Batch Member Import. Duplicates won't be upload.
- 2 . Manual Add Members. Duplicates not accepted
- 3 . Edit and Update Members



# Steps for Set Up
``` 
 1. git clone https://github.com/jasonjets/mpulse.git

 2.  cd app

 3. pip3 install -r requirements.txt

 4. python3 manage.py migrate

 5. python3 manage.py runserver

 6. Login to http://127.0.0.1:8000

 7. Empty tables for re-test $python manage.py flush

May need $python manage.py migrate --run-syncdb

```
