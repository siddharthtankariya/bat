from rest_framework import serializers
from voicetext.models import Voice,Segment


class VoiceSerializer(serializers.ModelSerializer):
    transcriber = serializers.StringRelatedField(read_only = True)
    created_at = serializers.SerializerMethodField(read_only = True)
    segment_count = serializers.SerializerMethodField(read_only = False)
    voice_id = serializers.StringRelatedField(read_only = True)
    segmented = serializers.StringRelatedField(read_only = True)
    status = serializers.StringRelatedField(read_only = True)
    attempt = serializers.StringRelatedField(read_only = True)
    
    class Meta:
        model = Voice
        fields = "__all__"


    def get_created_at(self,instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_segment_count(self,instance):
        return instance.segment_count
    

    



class SegmentSerializer(serializers.ModelSerializer):

    created_at = serializers.SerializerMethodField(read_only = True)
    voice_id = serializers.StringRelatedField(read_only = True)
    voice_path = serializers.StringRelatedField(read_only = False)
    status = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = Segment
        fields = "__all__"
        
    def get_created_at(self,instance):
        return instance.created_at.strftime("%B %d, %Y")

