from django.db import models
from django.core.validators import MinValueValidator
import random
import string


def generate_unique_id():
    length = 16

    while True:
        id_unique = "".join(random.choices(string.digits + string.ascii_letters, k=length))
        if (Book.objects.filter(id=id_unique).count() == 0):
            break
    return id_unique


class Book(models.Model):
    id = models.CharField(max_length=16, default=generate_unique_id, unique=True, primary_key=True)
    name = models.CharField(max_length=64, blank=False, null=False)
    year = models.PositiveIntegerField(null=False, validators=[MinValueValidator(2000)])
    author = models.CharField(max_length=64)
    summary = models.CharField(max_length=255)
    publisher = models.CharField(max_length=64)
    pageCount = models.IntegerField(null=False)
    readPage = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    reading = models.BooleanField(default=False)
    insertedAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}, Name: {self.name}\n" \
            f"Year: {self.year}\n" \
            f"Author: {self.author}\n" \
            f"Summary: {(self.summary[:30] + '...') if len(self.summary) > 30 else self.summary}\n" \
            f"Publisher: {self.publisher}\n" \
            f"Page Count: {self.pageCount}\n" \
            f"Read Page: {self.readPage}\n" \
            f"Finished: {self.finished}\n" \
            f"Reading: {self.reading}\n"
