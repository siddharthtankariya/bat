from rest_framework import generics,status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from voicetext.models import Voice,Segment,StatusEnum
from rest_framework.permissions import IsAuthenticated
from voicetext.api.serializers import VoiceSerializer,SegmentSerializer
from voicetext.api.pagination import SmallSetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from voicetext.api.validation import validate
import logging

logger = logging.getLogger()
loggerp = logging.getLogger()


class VoiceViewSet(viewsets.ModelViewSet):
    queryset = Voice.objects.all()
    lookup_field = "voice_id"
    serializer_class = VoiceSerializer
    permission_classes = [IsAuthenticated]




class SegmentCreateAPIView(generics.CreateAPIView):
    queryset = Segment.objects.all()
    serializer_class =  SegmentSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self,serializer):
    #     request_user = self.request.user
    #     kwarg_voiceid = self.kwargs.get("voice_id")
    #     voice = get_object_or_404(Voice,voice_id=kwarg_voiceid)
    #     serializer.save() 
        
class SegmentListView(APIView):
    queryset = Segment.objects.all()
    serializer_class =  SegmentSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request):
        logger.info("Request from annotator{0} ".format(request.user.username))
        v = Voice.objects.filter(transcriber=self.request.user,status = StatusEnum.PROCESSING).first()
        if v:
            logger.info("clearing backlog for the user.")
            segment_v = Segment.objects.filter(voice_id = v.voice_id,status= StatusEnum.PROCESSING).order_by("created_at").first()
            if segment_v is None:
                segment_v = Segment.objects.filter(voice_id = v.voice_id,status= StatusEnum.AVAILABLE).order_by("created_at").first()
                segment_v.status = StatusEnum.PROCESSING;
                Segment.save(segment_v)
            serializer_context = {"request": request}
            logger.info("sending data to annotator{0} with voice id {1}".format(request.user.username,v.voice_id))
            serializer = self.serializer_class(segment_v, context=serializer_context)
            return Response(serializer.data, status=status.HTTP_200_OK)
       
        voice = Voice.objects.filter(status=StatusEnum.AVAILABLE).order_by("created_at").first() # change status to available

        if voice:
            segment = Segment.objects.filter(voice_id = voice.voice_id,status= StatusEnum.AVAILABLE).order_by("created_at").first()

            if  segment:
                segment.status = StatusEnum.PROCESSING
                Segment.save(segment)

                voice.status = StatusEnum.PROCESSING
                voice.transcriber = self.request.user
                Voice.save(voice)
                serializer_context = {"request": request}
                serializer = self.serializer_class(segment, context=serializer_context)
                logger.info("sending data to annotator{0} with voice id {1}".format(request.user.username,v.voice_id))
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                logger.warn("No content for annotator {0}".format(request.user.username))
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            logger.warn("No content for annotator {0}".format(request.user.username))
            return Response(status=status.HTTP_204_NO_CONTENT)
           


class SegmentAPIView(APIView):
    queryset = Segment.objects.all()
    serializer_class =  SegmentSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request,pk):
        loggerp.info("got request for segment_id {0}".format(pk))
        segment = get_object_or_404(Segment,pk = pk)
        user = request.user
        segment.text = request.data['text']
        loggerp.info("translation for segment_id {0} is {1}".format(pk,segment.text))
        if segment.text: 
            if validate(segment.text):
                try:
                    v = Voice.objects.filter(pk = segment.voice_id.voice_id).first()
                    segment.status = StatusEnum.PROCESSED
                    print("saving segment ", segment.segment_id, "with status ", segment.status,"and voice",v.voice_id)
                    Segment.save(segment)
                    seg_count = Segment.objects.filter(voice_id= v.voice_id,status=StatusEnum.AVAILABLE).count()
                    print("remaining segments for voiceId :",v.voice_id,"are",seg_count)
                    if seg_count == 0:
                        v.status = StatusEnum.PROCESSED
                        v.transcriber = user
                        Voice.save(v)
                    serializer_context = {"request": request}
                    serializer = self.serializer_class(segment, context=serializer_context)
                    loggerp.info("translation saved for segment_id{0}".format(pk))
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except:
                    loggerp.warn("Some error occured in DB while saving instance :{0}",pk)
                    return Response(status= status.HTTP_400_BAD_REQUEST)
            else:
                logger.info("validation failed for segment_id {0}".format(pk))
                return Response(status= status.HTTP_400_BAD_REQUEST,data= {'message':"validation Failed"})

    
