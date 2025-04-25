# documents/models.py
from django.db import models



# Create your models here.
class Stream(models.Model):

    # Creeating stream model streams can be add through admin pannel

    name = models.CharField(max_length =100)

    def __str__(self):
        return self.name


class Department(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

    # creating department model department choices can be added at admin pannel

    name = models.CharField(max_length =100)

    def __str__(self):
        return f"{self.stream} - {self.name}"



class DocumentCategory(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


class DocumentType(models.Model):
    documentCategory = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE)

    # Creating DocumentType model choices can be added in admin pannel
    name = models.CharField(max_length = 20)

    def __str__(self):
        return f"{self.documentCategory} - {self.name}"
    


class Document(models.Model):
    department = models.ForeignKey('documents.Department', on_delete=models.CASCADE)
    documentType = models.ForeignKey('documents.DocumentType', on_delete=models.CASCADE)
    owner_email = models.EmailField()
    owner_id = models.IntegerField()

    name = models.CharField(max_length = 50)
    file = models.FileField(upload_to='uploads/', max_length=100)
    
    def __str__(self):
        return f" {self.name} - [{self.department} - {self.documentType}]"
    
