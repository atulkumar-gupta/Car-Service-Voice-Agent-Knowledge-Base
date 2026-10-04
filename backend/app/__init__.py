"""
AutoAssist — AI Voice Agent for Car Service Provider.

This package contains the backend implementation of an AI voice agent
that performs an initial customer assessment for a car service provider.

Modules:
    - config: Application settings loaded from environment variables.
    - rag: Retrieval-Augmented Generation over the car-service knowledge base.
    - agent: Core LLM agent with safety rules and emergency detection.
    - voice: Speech-to-Text (Whisper) and Text-to-Speech (OpenAI TTS).
    - models: Pydantic request/response schemas.
    - main: FastAPI application entrypoint.

Important:
    This agent performs an INITIAL ASSESSMENT only.
    It must NEVER present a diagnosis as certain.
    It must ALWAYS recommend professional inspection when appropriate.
"""

__version__ = "1.0.0"
__author__ = "AutoAssist Team"
__all__ = [
    "config",
    "rag",
    "agent",
    "voice",
    "models",
    "main",
]