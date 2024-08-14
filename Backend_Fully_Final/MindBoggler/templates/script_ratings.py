import csv
from user.models import Rating
from user.models import UserManager
from user.models import Book
with open("templates\\Ratings2.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            user = UserManager.objects.get(id=int(row['User-ID']))
        except UserManager.DoesNotExist:
            continue

        try:
            book = Book.objects.get(isbn=row['ISBN'])
        except Book.DoesNotExist:
            continue
       
        rating = Rating.objects.create(
            user_id = user,
            isbn = book,
            rating = int(float(row['Book-Rating']))
        )
        rating.save()
           