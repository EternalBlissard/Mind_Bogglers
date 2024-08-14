import csv
from user.models import UserManager
from passlib.hash import pbkdf2_sha256
with open("templates\\UserUpdated2.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Age']==None or row['Age']=='' or row['Age']=='NaN':
            user = UserManager.objects.create(
                location = row['Location'],
                username=row['username'],
                password = pbkdf2_sha256.encrypt(row['passwd'],rounds=12000,salt_size=32)
            )
            user.save()
        else:
            user = UserManager.objects.create(
                location = row['Location'],
                username=row['username'],
                password = pbkdf2_sha256.encrypt(row['passwd'],rounds=12000,salt_size=32),
                age = int(float(row['Age']))
            )
            user.save()