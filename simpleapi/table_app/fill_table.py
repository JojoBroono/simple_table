from models import TableRow
from datetime import date, timedelta
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simpleapi.settings")

django.setup()
d = timedelta(days=1)
dt = date(2019, 1, 1)

for i in range(30):
    dt += d
    name = f"name{i}"
    r = TableRow(dt=dt, name=name, amount=i*2, distance=i % 12)
    r.save()