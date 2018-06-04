# feedsite

My personal rssreader based on django.

## TODO:

- Add categories.
- Write tests...
- Group feed items that are similar. Only show the latest item in detail.
- Apply machine learning for an optional bubble grasping my reading behavior.

## Setup

requirements.txt contains needed python packages.
Important if you set up this reader on a public server:

- export DJANGO_DEBUG=False
- export DJANGO_SECRET_KEY=\<somethingrandom\>
- python3 manage.py check --deploy and fix warnings

### Database

- python3 manage.py migrate
- python3 manage.py createsuperuser
- Create users by calling /admin

### Update feeds

Run "python3 manage.py updatefeeds" in a cron job. It updates the feeds and 
deletes old entries.

If a feed cannot be updated, "Bozo" is true.

### Server

Digital Ocean explains quite well how to deploy such a django site together 
with nginx and gunicorn. Database can stay SQLite.

[Link to Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)

### Android Chrome

Adjust static/feedsite/site.webmanifest for pinning feedsite to the
Android home screen with Chrome.
