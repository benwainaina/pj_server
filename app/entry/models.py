from django.db import models
import uuid
from user.models import UserModel

""" For simplicity, the categories will be global and all users will see all the available categories """
class EntryCategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    class Meta:
        verbose_name = 'Entry Categories'
        verbose_name_plural = 'Entry Categories'
        
    def __str__(self) -> str:
        return self.category_name

# Create your models here.
class Entry(models.Model):
    # owner of the entry
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    
    # entry id
    entry_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    # the title of the entry
    title = models.CharField(max_length=100)

    # the contents of the entry
    content = models.CharField(max_length=100)

    # the category of the entry
    category = models.ForeignKey(
        EntryCategory,
        on_delete=models.CASCADE
    )

    # the date when the entry was created
    date = models.DateTimeField()
    
    class Meta:
        verbose_name = 'Entries'
        verbose_name_plural = 'Entries'
