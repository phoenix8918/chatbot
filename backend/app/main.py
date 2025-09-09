import os
import boto3
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import ChatRequest, ChatResponse

app = FastAPI(title="Chatbot Backend", version="1.0.0")

# CORS (allow all in dev; restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In prod, restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS SageMaker config (from env variables for security)
SAGEMAKER_ENDPOINT = os.getenv("SAGEMAKER_ENDPOINT_NAME", "your-endpoint-name")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

# Initialize SageMaker Runtime client
sagemaker_runtime = boto3.client("sagemaker-runtime", region_name=AWS_REGION)

@app.get("/health")
def health():
    return {"status": "ok"}

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from frontend
            data = await websocket.receive_text()

            # Send request to SageMaker endpoint
            try:
                # response = sagemaker_runtime.invoke_endpoint(
                #     EndpointName=SAGEMAKER_ENDPOINT,
                #     ContentType="application/json",  # depends on model
                #     Body=data.encode("utf-8")
                # )

                # result = response["Body"].read().decode("utf-8")

                result = 'Hello from SageMaker!'  # Mock response for testing

                # Send result back to frontend
                await websocket.send_text(result)

                # Mark completion
                await websocket.send_text("[END]")

            except Exception as e:
                await websocket.send_text(f"Error: {str(e)}")
                await websocket.send_text("[END]")
    except WebSocketDisconnect:
        print("Client disconnected")
