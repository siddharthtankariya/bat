from django.db.models.signals import post_save
from django.db.models import signals
from django.dispatch import receiver
from pydub import AudioSegment
from pydub.silence import split_on_silence
from django.conf import settings
import math

from voicetext.models import Voice,StatusEnum,Segment

@receiver(post_save, sender=Voice)
def create_segments_for_audio(sender,instance,*args,**kargs):
    
    if instance and instance.segmented == False:
        print("segmenting voice")
        instance.segmented = True
        voice_to_segment = AudioSegment.from_file(settings.VOICE_DATA_PATH+instance.voice_note , "mp3")
        print("Trying to split the audio file")
        chunks = split_on_silence(voice_to_segment,min_silence_len=500,silence_thresh= -16,keep_silence=100)
        print("instance length",len(chunks))
        instance.segment_count = len(chunks)
        target_length = 20 * 1000
        output_chunks = [chunks[0]]
        for chunk in chunks[1:]:
            print(len(chunk))
            if len(output_chunks[-1]) < target_length:
                output_chunks[-1] += chunk
            else:
                # if the last output chunk is longer than the target length,
                # we can start a new one
                output_chunks.append(chunk)
        
        import os,errno
        try:
            os.makedirs(settings.VOICE_SEGMENT+"{0}".format(instance.voice_id))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        
        for i, chunk in enumerate(chunks):
            chunk.export(settings.VOICE_SEGMENT+"{0}/chunk{1}.mp3".format(instance.voice_id,i), format="mp3")
            Segment.save(Segment(status = StatusEnum.AVAILABLE,voice_id = instance,voice_path = settings.VOICE_SEGMENT+"{0}/chunk{1}.mp3".format(instance.voice_id,i)))

        instance.status = StatusEnum.AVAILABLE
        Voice.save(instance)
    else:
        print("voice already segmented")
            