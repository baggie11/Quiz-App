# #
# # Copyright (c) 2024–2025, Daily
# #
# # SPDX-License-Identifier: BSD 2-Clause License
# #

# import os

# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.frames.frames import LLMRunFrame
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.server import (
#     WebsocketServerParams,
#     WebsocketServerTransport,
# )

# SYSTEM_INSTRUCTION = f"""
# "You are Gemini Chatbot, a friendly, helpful robot.

# Your goal is to demonstrate your capabilities in a succinct way.

# Your output will be converted to audio so don't include special characters in your answers.

# Respond to what the user said in a creative and helpful way. Keep your responses brief. One or two sentences at most.
# """


# async def run_bot_websocket_server():
#     ws_transport = WebsocketServerTransport(
#         params=WebsocketServerParams(
#             serializer=ProtobufFrameSerializer(),
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             session_timeout=60 * 3,  # 3 minutes
#         )
#     )

#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         voice_id="Puck",  # Aoede, Charon, Fenrir, Kore, Puck
#         transcribe_model_audio=True,
#         system_instruction=SYSTEM_INSTRUCTION,
#     )

#     context = LLMContext(
#         [
#             {
#                 "role": "user",
#                 "content": "Start by greeting the user warmly and introducing yourself.",
#             }
#         ],
#     )
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI events for Pipecat client UI
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     pipeline = Pipeline(
#         [
#             ws_transport.input(),
#             context_aggregator.user(),
#             rtvi,
#             llm,  # LLM
#             ws_transport.output(),
#             context_aggregator.assistant(),
#         ]
#     )

#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Kick off the conversation.
#         await task.queue_frames([LLMRunFrame()])

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("Pipecat Client connected")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("Pipecat Client disconnected")
#         await task.cancel()

#     @ws_transport.event_handler("on_session_timeout")
#     async def on_session_timeout(transport, client):
#         logger.info(f"Entering in timeout for {client.remote_address}")
#         await task.cancel()

#     runner = PipelineRunner()

#     await runner.run(task)

import os
import sys
import asyncio
from dotenv import load_dotenv
from loguru import logger

# Pipecat Core
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor

# Services
from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
from pipecat.services.whisper.stt import WhisperSTTService 

from pipecat.serializers.protobuf import ProtobufFrameSerializer
from pipecat.transports.websocket.server import (
    WebsocketServerParams,
    WebsocketServerTransport,
)

load_dotenv(override=True)

# Configure Logger
logger.remove()
logger.add(sys.stderr, level="INFO")

SYSTEM_INSTRUCTION = """
You are Gemini Chatbot, a friendly, helpful robot.
Your goal is to demonstrate your capabilities in a succinct way.
Your output will be converted to audio so don't include special characters.
Keep your responses brief. One or two sentences at most.
"""

async def run_bot_websocket_server():
    # 1. Transport Setup (Audio In -> Whisper, Audio Out <- Gemini)
    ws_transport = WebsocketServerTransport(
        params=WebsocketServerParams(
            serializer=ProtobufFrameSerializer(),
            audio_in_enabled=True,
            audio_out_enabled=True,
            add_wav_header=False,
            vad_analyzer=SileroVADAnalyzer(),
            session_timeout=180,
        )
    )

    # 2. Whisper STT (Configured for your Docker Container)
    # Note: Ensure the API endpoint in your Docker container matches the base_url
    stt = WhisperSTTService(
        model="base",
        # Uncomment and update the URL to your Docker container address
        # base_url="http://localhost:8000/v1" 
    )

    # 3. Gemini Live Setup (Handles Brain + TTS)
    llm = GeminiLiveLLMService(
        api_key=os.getenv("GOOGLE_API_KEY"),
        voice_id="Puck",  # Options: Aoede, Charon, Fenrir, Kore, Puck
        transcribe_model_audio=True, 
        system_instruction=SYSTEM_INSTRUCTION,
    )

    # 4. Context & RTVI
    context = LLMContext(
        [
            {
                "role": "user",
                "content": "Start by greeting the user warmly and introducing yourself.",
            }
        ],
    )
    context_aggregator = LLMContextAggregatorPair(context)
    rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

    # 5. The Pipeline
    # Transport (Audio) -> Whisper (Text) -> Gemini (Audio Out)
    pipeline = Pipeline(
        [
            ws_transport.input(),        # User voice in
            stt,                         # Whisper transcribes to text
            rtvi,                        # Events/Signals
            context_aggregator.user(),   # Text moves to context
            llm,                         # Gemini generates voice & text
            ws_transport.output(),       # Audio out to user
            context_aggregator.assistant(),
        ]
    )

    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
        observers=[RTVIObserver(rtvi)],
    )

    # --- Event Handlers ---

    @rtvi.event_handler("on_client_ready")
    async def on_client_ready(rtvi):
        logger.info("Pipecat client ready.")
        await rtvi.set_bot_ready()
        # Initial greeting trigger
        await task.queue_frames([LLMRunFrame()])

    @ws_transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info(f"Client connected: {client.remote_address}")

    @ws_transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Client disconnected")
        await task.cancel()

    runner = PipelineRunner()
    await runner.run(task)

if __name__ == "__main__":
    asyncio.run(run_bot_websocket_server())
