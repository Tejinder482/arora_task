from django.shortcuts import render
from .models import PatientMessage
from .aimodel import generate_response
from .serializers import (
    MessageInputSerializer, 
    MessageResponseSerializer, 
    ErrorResponseSerializer
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
import re

# Create your views here.
def chat_page(request):
    """Render the chat page"""
    return render(request, "chat.html")

@swagger_auto_schema(
    method='get',
    operation_summary="API Overview",
    operation_description="Get information about available API endpoints and documentation links.",
    responses={
        200: openapi.Response(
            description="API overview information",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'version': openapi.Schema(type=openapi.TYPE_STRING),
                    'endpoints': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'submit_message': openapi.Schema(type=openapi.TYPE_STRING),
                            'swagger_ui': openapi.Schema(type=openapi.TYPE_STRING),
                            'redoc': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    ),
                    'categories': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING)
                    )
                }
            )
        )
    },
    tags=['API Information'],
)
@api_view(["GET"])
def api_overview(request):
    """
    API Overview - Get information about available endpoints
    """
    return JsonResponse({
        'message': 'Medical Message Classification API',
        'version': 'v1.0.0',
        'description': 'AI-powered medical message classification using DeepSeek-R1 model',
        'endpoints': {
            'submit_message': '/submit-message/ (POST)',
            'swagger_ui': '/swagger/',
            'redoc': '/redoc/',
            'api_overview': '/api/',
        },
        'categories': ['emergency', 'routine', 'followup', 'other'],
        'features': [
            'AI-powered classification',
            'Patient message history',
            'Confidence scoring',
            'Real-time processing'
        ]
    })

@swagger_auto_schema(
    method='post',
    operation_summary="Classify Medical Message",
    operation_description="""
    Submit a patient's medical message for AI-powered classification.
    
    The system uses DeepSeek-R1 model to automatically categorize messages into:
    - **emergency**: Life-threatening situations requiring immediate attention
    - **routine**: Normal medical care that can wait  
    - **followup**: Messages about previous treatments or appointments
    - **other**: Non-medical or administrative messages
    
    The API also returns the patient's message history based on mobile number.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'mobile', 'message'],
        properties={
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Patient's full name",
                example="John Doe"
            ),
            'mobile': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Patient's mobile number with country code",
                example="+1234567890"
            ),
            'message': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Medical message from the patient",
                example="I have severe chest pain and difficulty breathing"
            ),
        }
    ),
    responses={
        200: openapi.Response(
            description="Message successfully classified",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    'current_result': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'category': openapi.Schema(type=openapi.TYPE_STRING, example="emergency"),
                            'confidence': openapi.Schema(type=openapi.TYPE_NUMBER, example=0.95)
                        }
                    ),
                    'history': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'message': openapi.Schema(type=openapi.TYPE_STRING),
                                'category': openapi.Schema(type=openapi.TYPE_STRING),
                                'confidence': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'timestamp': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        )
                    ),
                    'ai_response': openapi.Schema(type=openapi.TYPE_STRING, example="emergency\n95%"),
                    'timestamp': openapi.Schema(type=openapi.TYPE_STRING, example="14:25")
                }
            )
        ),
        400: openapi.Response(
            description="Invalid input data",
            schema=ErrorResponseSerializer
        ),
        500: openapi.Response(
            description="Server error or AI model unavailable",
            schema=ErrorResponseSerializer
        )
    },
    tags=['Medical Classification'],
)
@csrf_exempt
@api_view(["POST"])
def submit_message(request):
    """
    Submit a medical message for AI classification
    
    This endpoint accepts a patient's medical message and returns:
    - AI classification category (emergency/routine/followup/other)
    - Confidence score (0.0 to 1.0)
    - Patient's message history
    - Raw AI response
    """
    try:
        if request.content_type == 'application/json':
            serializer = MessageInputSerializer(data=json.loads(request.body))
        else:
            serializer = MessageInputSerializer(data=request.POST)
        
        if not serializer.is_valid():
            return JsonResponse({
                'success': False,
                'error': 'Invalid input data',
                'details': serializer.errors
            }, status=400)
        
        validated_data = serializer.validated_data
        name = validated_data['name']
        mobile = validated_data['mobile'] 
        message = validated_data['message']

        ai_response = generate_response(message)
        
        category = "other"
        confidence = 0.5 
        
        try:
            lines = ai_response.strip().split('\n')
            if len(lines) >= 2:
                category = lines[0].strip().lower()
                confidence_str = lines[1].strip().rstrip('%')
                confidence = float(confidence_str) / 100.0 if confidence_str.replace('.', '').isdigit() else 0.5
            
            if category not in ['emergency', 'routine', 'followup', 'other']:
                category_match = re.search(r'CATEGORY:\s*(\w+)', ai_response, re.IGNORECASE)
                if category_match:
                    category = category_match.group(1).lower()
                    
                confidence_match = re.search(r'CONFIDENCE:\s*([\d.]+)', ai_response, re.IGNORECASE)
                if confidence_match:
                    confidence = float(confidence_match.group(1))
                    
        except Exception as parse_error:
            print(f"Error parsing AI response: {parse_error}")
            category = "other"
            confidence = 0.5
        
        previous_messages = PatientMessage.objects.filter(mobile=mobile).order_by('-created_at')
        
        patient = PatientMessage.objects.create(
            name=name, 
            mobile=mobile, 
            message=message, 
            category=category,
            confidence=confidence
        )
        
        history = []
        for prev_msg in previous_messages:
            history.append({
                "message": prev_msg.message,
                "category": prev_msg.category,
                "confidence": prev_msg.confidence,
                "timestamp": prev_msg.created_at.strftime("%Y-%m-%d %H:%M")
            })
        
        response_data = {
            'success': True,
            'current_result': {
                'category': category,
                'confidence': confidence
            },
            'history': history,
            'ai_response': ai_response,
            'timestamp': patient.created_at.strftime("%H:%M")
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
