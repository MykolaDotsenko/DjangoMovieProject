from django.db import models

# Create your models here.
class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    rating = models.FloatField(default=5.0)
    create_date = models.DateField(blank=True)
    wiki_link = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    contact_email = models.EmailField( blank=True)
    logo = models.ImageField( upload_to='logos/', blank=True, null=True)

    creator = models.ForeignKey("Person", related_name="pl_list", on_delete=models.CASCADE, blank=True, default=None, null=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    portrait = models.ImageField(upload_to="persons")
    birth_date = models.DateField(blank=True)
    wiki_link = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=100)
    languages = models.ManyToManyField(ProgrammingLanguage, blank=True, related_name="projects")
    start_date = models.DateField(blank=True)
    deadline_date = models.DateField(blank=True)

    def __str__(self):
        return self.title