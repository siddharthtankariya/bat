from django.db.models.signals import post_save
from django.db.models import signals
from django.dispatch import receiver
from pydub import AudioSegment
from pydub.silence import split_on_silence
from django.conf import settings
import math

from voicetext.models import Voice,StatusEnum,Segment
import logging

logger = logging.getLogger("voice-pipeline")

@receiver(post_save, sender=Voice)
def create_segments_for_audio(sender,instance,*args,**kargs):
    
    if instance and instance.segmented == False:
        logger.info("recieved request to segment voice : {0}".format(instance.voice_id))
        instance.segmented = True
        voice_to_segment = AudioSegment.from_file(settings.VOICE_DATA_PATH+instance.voice_note , "mp3")
        chunks = split_on_silence(voice_to_segment,min_silence_len=500,silence_thresh= -16,keep_silence=100)
        instance.segment_count = len(chunks)
        logger.info("segmenting voice {0} into {1} segments".format(instance.voice_id,instance.segment_count))
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
        logger.info("segmentation done")
        Voice.save(instance)
    else:
        logger.info("Voice is already segmented")
            