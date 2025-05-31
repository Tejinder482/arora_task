from rest_framework import serializers
from .models import PatientMessage


class MessageInputSerializer(serializers.Serializer):
    """Serializer for message input data"""
    name = serializers.CharField(
        max_length=200, 
        help_text="Patient's full name (e.g., 'John Doe')"
    )
    mobile = serializers.CharField(
        max_length=20, 
        help_text="Patient's mobile number with country code (e.g., '+1234567890')"
    )
    message = serializers.CharField(
        help_text="Medical message from the patient (e.g., 'I have severe chest pain and difficulty breathing')"
    )

    def validate_mobile(self, value):
        """Validate mobile number format"""
        if not value.strip():
            raise serializers.ValidationError("Mobile number cannot be empty")
        return value

    def validate_message(self, value):
        """Validate message content"""
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Message must be at least 5 characters long")
        return value


class HistoryMessageSerializer(serializers.Serializer):
    """Serializer for patient message history"""
    message = serializers.CharField(help_text="Previous message content")
    category = serializers.CharField(help_text="AI-classified category")
    confidence = serializers.FloatField(help_text="AI confidence score (0.0-1.0)")
    timestamp = serializers.CharField(help_text="Message timestamp")


class CurrentResultSerializer(serializers.Serializer):
    """Serializer for current classification result"""
    category = serializers.ChoiceField(
        choices=[
            ('emergency', 'Emergency'),
            ('routine', 'Routine'),
            ('followup', 'Follow-up'),
            ('other', 'Other')
        ],
        help_text="AI-classified category"
    )
    confidence = serializers.FloatField(
        min_value=0.0, 
        max_value=1.0,
        help_text="AI confidence score between 0.0 and 1.0"
    )


class MessageResponseSerializer(serializers.Serializer):
    """Serializer for API response"""
    success = serializers.BooleanField(
        help_text="Indicates if the request was successful"
    )
    current_result = CurrentResultSerializer(
        help_text="Current message classification result"
    )
    history = HistoryMessageSerializer(
        many=True,
        help_text="Previous messages from the same patient"
    )
    ai_response = serializers.CharField(
        help_text="Raw AI model response"
    )
    timestamp = serializers.CharField(
        help_text="Time when the message was processed (HH:MM format)"
    )


class ErrorResponseSerializer(serializers.Serializer):
    """Serializer for error responses"""
    success = serializers.BooleanField(
        default=False,
        help_text="Always false for error responses"
    )
    error = serializers.CharField(
        help_text="Error message describing what went wrong"
    )


class PatientMessageSerializer(serializers.ModelSerializer):
    """Serializer for PatientMessage model"""
    
    class Meta:
        model = PatientMessage
        fields = ['id', 'name', 'mobile', 'message', 'category', 'confidence', 'created_at']
        read_only_fields = ['id', 'created_at'] 