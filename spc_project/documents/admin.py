from django.contrib import admin
from documents.models import Stream, Department, DocumentCategory, DocumentType, Document

# Register your models here.

admin.site.register(Stream);
admin.site.register(Department);
admin.site.register(Document);
admin.site.register(DocumentType);
admin.site.register(DocumentCategory);