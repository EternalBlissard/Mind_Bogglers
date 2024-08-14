
import csv
from user.models import Book

with open("templates\Books2.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Image-URL-L']==None or row['Image-URL-L']=='':
            continue
        book = Book.objects.create(
            isbn=row['ISBN'],
            title=row['Book-Title'],
            author=row['Book-Author'],
            year=row['Year-Of-Publication'],
            publisher=row['Publisher'],
            image_s=row['Image-URL-S'],
            image_m=row['Image-URL-M'],
            image_l=row['Image-URL-L']
        )
        book.save()