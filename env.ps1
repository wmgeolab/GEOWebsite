$Env:DEBUG="true"
$Env:DB_NAME="C:/geoLab/GEOWebsite/test.sqlite3"
$Env:DB_ENGINE="django.db.backends.sqlite3"
$Env:CAS_SERVER_URL="https://cas.wm.edu/cas/"
python cms/manage.py uploadexample C:\geoLab\GEOWebsite\cms\school_app\management\commands\mexico_cleanv2.000