#/bin/sh

# python main.py
uwsgi --http=:8000 --wsgi-file=main.py --callable=app