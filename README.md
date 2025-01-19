
# SomniSense - A Dream Analyzer Chatbot 🌌


## Project Overview
SomniSense is an intelligent dream analyzer chatbot designed to interpret and analyze user inputs about their dreams. Built using AWS GenAI services, the chatbot leverages advanced machine learning models to provide insightful and meaningful dream interpretations. By combining a conversational interface with robust backend processing, SomniSense ensures an engaging and scalable user experience.

## Features

🌟 Dream Analysis with GenAI

- Uses Amazon Bedrock for generating responses based on pre-trained foundation models.

💬 Conversational Interface

- Built with Amazon Lex for natural and intuitive interactions.

📊 Sentiment & Entity Analysis

- Integrates Amazon Comprehend for understanding user inputs.

🔍 Advanced Search

- Implements Amazon OpenSearch Service for enhanced search capabilities.

📡 Real-Time Interaction

- Powered by Twilio for seamless and immediate communication.

📦 Data Storage & Metrics

- Stores user data and analysis results in Amazon DynamoDB.
- Tracks logs and metrics with Amazon CloudWatch for monitoring and debugging.

## Architecture




## Prerequisites

- AWS account with access to Bedrock.
- Twilio account for real-time interaction.

## Setup in a Nutshell

Step 1 - Setup a knowledge base in AWS Bedrock with S3 as data source containing dataset. A vector database in OpenSearch will be created while creating knowledge base.

Step 2 - Build Lex Chatbot, with a inbuit GenAI intent connecting it to bedrock. Set a channel integration with Twilio.

Step 3 - Create a Dynamodb Table for storing user data.

Step 4 - Deploy a Lambda function with access to Comprehend, Dynamodb, and Cloudwatch for sentiment analysis, storing user data, and storing logs respectively. (For code check lambda_function.py )

Step 5 - Select the fullfillment option in GenAI intent created previously. Use Lambda function for fulfillment. Also specify the Lambda function created in the Lex chatbot (See References below)


## References

- Blog - https://tinyurl.com/4uhav5nf by Mattiamazzari

- Video - https://tinyurl.com/y2xxckp8 by Tiny Technical Tutorials

## Future Improvements

- Integrating multi-language support for global users.
- Adding a user-friendly web interface for easier interaction.
- Improving response generation with fine-tuned models on dream-related datasets.
- Adding dashboard based on user's dream pattern data.