#! /bin/bash
# Auto execute RSS_Artical_sql.py
. /etc/profile
cd /alidata/django-sites/LandsBlog
cp /alidata/django-sites/LandsBlog/db.sqlite3 /alidata/django-sites/LandsBlog/db_old.sqlite3
python RSS_Artical_sql.py
