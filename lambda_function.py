import os
import boto3
import json
from datetime import datetime
from decimal import Decimal

def lambda_handler(event, context):
    try:
        # Initialize AWS services
        lex_client = boto3.client('lexv2-runtime')
        comprehend = boto3.client('comprehend')
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE_NAME'])

        print("Incoming Event:", json.dumps(event, indent=2))

        # Extract user message from request attributes
        request_attributes = event.get('requestAttributes', {})
        user_message = event.get('inputTranscript', '')

        # Extract intent data and sessionId(user phone number) from the event
        session_state = event.get('sessionState', {})
        intent = session_state.get('intent', {})
        intent_name = intent.get('name', '')
        sessionId = event.get('sessionId', '')
        user_phone = "+"+sessionId.split(":")[-1]

        print("User Phone:", user_phone)
        print("User Message:", user_message)
        
        if intent_name == 'QnABotIntent':
            print("QnABotIntent triggered")
            
            # Get sentiment analysis from Comprehend for the user message
            sentiment_response = comprehend.detect_sentiment(
                Text=user_message,
                LanguageCode='en'
            )

            # Get Dream Interpretation from lex
            messages = event.get('messages', [])
            interpretation = request_attributes.get('x-amz-lex:qnA-search-response', '')

            # Get the last message from Lex as the interpretation
            if messages:
                interpretation = messages[-1].get('content', '')
            
            if not interpretation:
                interpretation = "I apologize, but I couldn't generate an interpretation for your dream at this time."

            # Get sentiment analysis on interpretation
            sentiment_response_lex = comprehend.detect_sentiment(
                Text=interpretation,
                LanguageCode='en'
            )

            # Store in DynamoDB only for QnABotIntent
            try:
                table.put_item(
                    Item={
                        'PhoneNumber': user_phone,
                        'Dream Text': user_message,
                        'Date': datetime.utcnow().isoformat(),
                        'DreamSentiment': sentiment_response['Sentiment'],
                        'DreamSentimentScores': {
                            'Positive': Decimal(str(sentiment_response['SentimentScore']['Positive'])),
                            'Negative': Decimal(str(sentiment_response['SentimentScore']['Negative'])),
                            'Neutral': Decimal(str(sentiment_response['SentimentScore']['Neutral'])),
                            'Mixed': Decimal(str(sentiment_response['SentimentScore']['Mixed']))
                        },
                        'DreamInterpretation': interpretation,
                        'Interpretation Sentiment': sentiment_response_lex['Sentiment'],
                        'Interpretation SentimentScores': {
                            'Positive': Decimal(str(sentiment_response_lex['SentimentScore']['Positive'])),
                            'Negative': Decimal(str(sentiment_response_lex['SentimentScore']['Negative'])),
                            'Neutral': Decimal(str(sentiment_response_lex['SentimentScore']['Neutral'])),
                            'Mixed': Decimal(str(sentiment_response_lex['SentimentScore']['Mixed']))
                        }
                    }
                )
            except Exception as e:
                print(f"Error storing in DynamoDB: {str(e)}")
            
            # Return response in Lex channel integration format
            return {
                'sessionState': {
                    'sessionAttributes': event.get('sessionAttributes', {}),
                    'intent': {
                        'name': intent_name,
                        'state': 'Fulfilled',
                        'confirmationState': 'Confirmed'
                    },
                    'dialogAction': {
                        'type': 'Close'
                    }
                },
                'messages': [{
                    'contentType': 'PlainText',
                    'content': interpretation
                }]
            }

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'sessionState': session_state if 'session_state' in locals() else {},
            'messages': [{
                'contentType': 'PlainText',
                'content': "Sorry, I encountered an error processing your request."
            }]
        }