from django.db import models
from django.conf import settings
from enum import IntEnum
# Create your models here.


class StatusEnum(IntEnum):
    AVAILABLE = 0
    PROCESSING = 1
    PROCESSED = 2
    BLOCKED = 3

    @classmethod
    def choices(cls):
        return [(key.value,key.name) for key in cls]
    

class Voice(models.Model):
    voice_id = models.AutoField(primary_key = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transcriber = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name="voicetext",null = True)
    
    voice_note = models.CharField(max_length = 500)
    attempt = models.IntegerField(default=0)
    segmented = models.BooleanField(default=False)
    segment_count = models.IntegerField(default=0)
    status = models.IntegerField(choices=StatusEnum.choices(),default=StatusEnum.BLOCKED)
    

    def __str__(self):
        return self.voice_note



class Segment(models.Model):
    
    segment_id = models.AutoField(primary_key = True)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)
    voice_id = models.ForeignKey(Voice,on_delete=models.CASCADE,related_name="voiceid")
    voice_path = models.CharField(max_length = 500)
    status = models.IntegerField(choices=StatusEnum.choices(),default=StatusEnum.AVAILABLE)

    def __str__(self):
        return self.voice_path




