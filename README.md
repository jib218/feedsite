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

### Setup Database

- python3 manage.py migrate
- python3 manage.py createsuperuser
- Create users by calling /admin

### Update feeds

Run "python3 manage.py updatefeeds" in a cron job. It updates the feeds and 
deletes old entries.

If a feed cannot be updated, "Bozo" is true. 
