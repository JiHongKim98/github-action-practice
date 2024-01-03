from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Book(models.Model):
    name = models.CharField(max_length=255)

    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name="book"
    )
