

# # import os
# # import sys

# # from dotenv import load_dotenv
# # from loguru import logger
# # from pipecat.audio.vad.silero import SileroVADAnalyzer
# # from pipecat.frames.frames import LLMRunFrame
# # from pipecat.pipeline.pipeline import Pipeline
# # from pipecat.pipeline.runner import PipelineRunner
# # from pipecat.pipeline.task import PipelineParams, PipelineTask
# # from pipecat.processors.aggregators.llm_context import LLMContext
# # from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# # from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# # from pipecat.serializers.protobuf import ProtobufFrameSerializer
# # from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# # from pipecat.transports.websocket.fastapi import (
# #     FastAPIWebsocketParams,
# #     FastAPIWebsocketTransport,
# # )

# # load_dotenv(override=True)

# # logger.remove(0)
# # logger.add(sys.stderr, level="DEBUG")


# # SYSTEM_INSTRUCTION = f"""
# # "You are Gemini Chatbot, a friendly, helpful robot.

# # Your goal is to demonstrate your capabilities in a succinct way.

# # Your output will be converted to audio so don't include special characters in your answers.

# # Respond to what the user said in a creative and helpful way. Keep your responses brief. One or two sentences at most.
# # """


# # async def run_bot(websocket_client):
# #     ws_transport = FastAPIWebsocketTransport(
# #         websocket=websocket_client,
# #         params=FastAPIWebsocketParams(
# #             audio_in_enabled=True,
# #             audio_out_enabled=True,
# #             add_wav_header=False,
# #             vad_analyzer=SileroVADAnalyzer(),
# #             serializer=ProtobufFrameSerializer(),
# #         ),
# #     )

# #     llm = GeminiLiveLLMService(
# #         api_key=os.getenv("GOOGLE_API_KEY"),
# #         voice_id="Puck",  # Aoede, Charon, Fenrir, Kore, Puck
# #         transcribe_model_audio=True,
# #         system_instruction=SYSTEM_INSTRUCTION,
# #     )

# #     context = LLMContext(
# #         [
# #             {
# #                 "role": "user",
# #                 "content": "Start by greeting the user warmly and introducing yourself.",
# #             }
# #         ],
# #     )
# #     context_aggregator = LLMContextAggregatorPair(context)

# #     RTVI events for Pipecat client UI
# #     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

# #     pipeline = Pipeline(
# #         [
# #             ws_transport.input(),
# #             context_aggregator.user(),
# #             rtvi,
# #             llm,  # LLM
# #             ws_transport.output(),
# #             context_aggregator.assistant(),
# #         ]
# #     )

# #     task = PipelineTask(
# #         pipeline,
# #         params=PipelineParams(
# #             enable_metrics=True,
# #             enable_usage_metrics=True,
# #         ),
# #         observers=[RTVIObserver(rtvi)],
# #     )

# #     @rtvi.event_handler("on_client_ready")
# #     async def on_client_ready(rtvi):
# #         logger.info("Pipecat client ready.")
# #         await rtvi.set_bot_ready()
# #         Kick off the conversation.
# #         await task.queue_frames([LLMRunFrame()])

# #     @ws_transport.event_handler("on_client_connected")
# #     async def on_client_connected(transport, client):
# #         logger.info("Pipecat Client connected")

# #     @ws_transport.event_handler("on_client_disconnected")
# #     async def on_client_disconnected(transport, client):
# #         logger.info("Pipecat Client disconnected")
# #         await task.cancel()

# #     runner = PipelineRunner(handle_sigint=False)

# #     await runner.run(task)

# # import os
# # import sys

# # from dotenv import load_dotenv
# # from loguru import logger
# # from pipecat.audio.vad.silero import SileroVADAnalyzer
# # from pipecat.frames.frames import LLMRunFrame
# # from pipecat.pipeline.pipeline import Pipeline
# # from pipecat.pipeline.runner import PipelineRunner
# # from pipecat.pipeline.task import PipelineParams, PipelineTask
# # from pipecat.processors.aggregators.llm_context import LLMContext
# # from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# # from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# # from pipecat.serializers.protobuf import ProtobufFrameSerializer
# # from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# # 1. Import the Whisper STT Service
# # from pipecat.services.whisper import WhisperSTTService
# # from pipecat.transports.websocket.fastapi import (
# #     FastAPIWebsocketParams,
# #     FastAPIWebsocketTransport,
# # )

# # load_dotenv(override=True)

# # logger.remove(0)
# # logger.add(sys.stderr, level="DEBUG")

# # SYSTEM_INSTRUCTION = """
# # You are Gemini Chatbot, a friendly, helpful robot.
# # Your goal is to demonstrate your capabilities in a succinct way.
# # Your output will be converted to audio so don't include special characters in your answers.
# # Respond to what the user said in a creative and helpful way. Keep your responses brief. One or two sentences at most.
# # """

# # async def run_bot(websocket_client):
# #     ws_transport = FastAPIWebsocketTransport(
# #         websocket=websocket_client,
# #         params=FastAPIWebsocketParams(
# #             audio_in_enabled=True,
# #             audio_out_enabled=True,
# #             add_wav_header=False,
# #             vad_analyzer=SileroVADAnalyzer(),
# #             serializer=ProtobufFrameSerializer(),
# #         ),
# #     )

# #     2. Initialize Whisper STT pointed at your Docker container
# #     Replace 'http://localhost:9000' with your actual Docker container address
# #     stt = WhisperSTTService(
# #         url="http://localhost:11435/v1", 
# #         model="base"
# #     )

# #     llm = GeminiLiveLLMService(
# #         api_key=os.getenv("GOOGLE_API_KEY"),
# #         voice_id="Puck",
# #         3. CRITICAL: Disable internal transcription to use external Whisper text
# #         transcribe_model_audio=False,
# #         system_instruction=SYSTEM_INSTRUCTION,
# #     )

# #     context = LLMContext(
# #         [
# #             {
# #                 "role": "user",
# #                 "content": "Start by greeting the user warmly and introducing yourself.",
# #             }
# #         ],
# #     )
# #     context_aggregator = LLMContextAggregatorPair(context)

# #     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

# #     4. Insert STT into the pipeline before the context aggregator
# #     pipeline = Pipeline(
# #         [
# #             ws_transport.input(),
# #             stt,                     # Added ASR stage
# #             context_aggregator.user(),
# #             rtvi,
# #             llm,
# #             ws_transport.output(),
# #             context_aggregator.assistant(),
# #         ]
# #     )

# #     task = PipelineTask(
# #         pipeline,
# #         params=PipelineParams(
# #             enable_metrics=True,
# #             enable_usage_metrics=True,
# #         ),
# #         observers=[RTVIObserver(rtvi)],
# #     )

# #     @rtvi.event_handler("on_client_ready")
# #     async def on_client_ready(rtvi):
# #         logger.info("Pipecat client ready.")
# #         await rtvi.set_bot_ready()
# #         await task.queue_frames([LLMRunFrame()])

# #     @ws_transport.event_handler("on_client_connected")
# #     async def on_client_connected(transport, client):
# #         logger.info("Pipecat Client connected")

# #     @ws_transport.event_handler("on_client_disconnected")
# #     async def on_client_disconnected(transport, client):
# #         logger.info("Pipecat Client disconnected")
# #         await task.cancel()

# #     runner = PipelineRunner(handle_sigint=False)

# #     await runner.run(task)

# # bot_fast_api.py
# #
# # Copyright (c) 2024-2026, Daily
# #
# # SPDX-License-Identifier: BSD 2-Clause License
# #

# # """Pipecat Flows: Local Whisper ASR + Gemini LLM"""

# # import os
# # import aiohttp
# # import json
# # from dotenv import load_dotenv
# # from loguru import logger
# # from pipecat.audio.vad.silero import SileroVADAnalyzer
# # from pipecat.frames.frames import LLMRunFrame, TextFrame
# # from pipecat.pipeline.pipeline import Pipeline
# # from pipecat.pipeline.runner import PipelineRunner
# # from pipecat.pipeline.task import PipelineParams, PipelineTask
# # from pipecat.processors.aggregators.llm_context import LLMContext
# # from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# # from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# # from pipecat.processors.frame_processor import FrameProcessor
# # from pipecat.serializers.protobuf import ProtobufFrameSerializer
# # from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# # from pipecat.transports.websocket.fastapi import (
# #     FastAPIWebsocketParams,
# #     FastAPIWebsocketTransport,
# # )

# # load_dotenv(override=True)

# # # Node API configuration
# # NODE_API_URL = "http://localhost:3000"


# # async def fetch_questions_from_api(session_code: str = "H6TU") -> list:
# #     """Fetch questions from Node API endpoint"""
# #     try:
# #         async with aiohttp.ClientSession() as session:
# #             async with session.get(
# #                 f"{NODE_API_URL}/api/sessions/{session_code}/questions",
# #                 timeout=aiohttp.ClientTimeout(total=5)
# #             ) as response:
# #                 if response.status == 200:
# #                     data = await response.json()
                    
# #                     # Check if response has expected format
# #                     if data.get("status") == "ok" and "data" in data:
# #                         questions_data = data["data"]
# #                         logger.info(f"✅ Successfully fetched {len(questions_data)} questions from API")
# #                         return questions_data
# #                     else:
# #                         logger.error(f"❌ Unexpected API response format: {data}")
# #                         return []
# #                 else:
# #                     logger.error(f"❌ API returned status {response.status}")
# #                     return []
# #     except Exception as e:
# #         logger.error(f"❌ Error fetching questions: {e}")
# #         return []

# # def format_question_for_llm(question_data: dict) -> str:
# #     """Format a question from API into LLM-readable format"""
# #     question_text = question_data.get("question_text", "Unknown question")
# #     options = question_data.get("question_options", [])
    
# #     # Find correct answer
# #     correct_options = [opt for opt in options if opt.get("is_correct")]
# #     correct_answer = correct_options[0].get("option_text", "Unknown") if correct_options else "Unknown"
    
# #     # Format options
# #     options_text = ""
# #     for i, opt in enumerate(options, 1):
# #         option_text = opt.get("option_text", f"Option {i}")
# #         is_correct = opt.get("is_correct", False)
# #         options_text += f"  {i}. {option_text}"
# #         if is_correct:
# #             options_text += " ✓"
# #         options_text += "\n"
    
# #     return f"""Question: {question_text}
# # Options:
# # {options_text}
# # Answer: {correct_answer}"""

# # async def run_bot(websocket_client,session_code: str = "H6TU"):
# #     """This function runs the bot pipeline for a WebSocket connection"""
# #     print(f"🤖 Starting bot for session: {session_code}")
# #     # Fetch questions from Node API before creating the bot
# #     api_questions_data = await fetch_questions_from_api(session_code)
    
# #     if not api_questions_data:
# #         logger.warning("⚠️ No questions fetched from API, using fallback")
# #         # Create fallback questions
# #         formatted_questions = """Question: What is the capital of France?
# # Options:
# #   1. Mumbai
# #   2. Delhi ✓
# #   3. Kolkata
# # Answer: Delhi

# # Question: Which planet is known as the Red Planet?
# # Options:
# #   1. Venus
# #   2. Mars ✓
# #   3. Jupiter
# # Answer: Mars"""
# #     else:
# #         # Format all questions for LLM
# #         formatted_questions = "\n\n".join([
# #             format_question_for_llm(q) for q in api_questions_data
# #         ])
# #         print(formatted_questions)
    
# #     # Create dynamic system instruction with fetched questions
# #     system_instruction = f"""You are an interactive quiz master and Q&A assistant.

# # I will provide you with quiz questions, their options, and correct answers. Your primary role is to ask these questions conversationally.

# # QUESTIONS DATABASE:
# # {formatted_questions}

# # CRITICAL INSTRUCTIONS FOR QUIZ MASTER MODE:
# # 1. START BY ASKING: Begin by greeting and asking if the user would like to take a quiz or answer questions.

# # 2. WHEN USER SAYS YES TO QUIZ:
# #    - Ask ONE question at a time from the database above
# #    - Clearly state the question
# #    - List ALL the options properly (A, B, C, etc.)
# #    - Wait for their answer
# #    - After they answer, give brief feedback and move to next question

# # 3. WHEN USER ASKS TO REPEAT:
# #    - If user says "repeat", "say that again", "what were the options", "can you repeat the question", or similar:
# #    - REPEAT THE ENTIRE QUESTION with all options clearly
# #    - Use the exact same wording as before
# #    - Example: "Sure! Let me repeat that. The question was: [question text]. Your options are: A) [option 1], B) [option 2], C) [option 3]"

# # 4. WHEN USER ASKS FOR OPTIONS AGAIN:
# #    - If user asks "what are the options", "options please", "choices again":
# #    - Repeat JUST the options clearly: "The options are: A) [option 1], B) [option 2], C) [option 3]"

# # 5. ANSWERING USER QUESTIONS:
# #    - If user asks a question that matches one in the database, provide the correct answer
# #    - Example: If user asks "What's the capital of India?", answer "Delhi" and explain

# # 6. CONVERSATIONAL RULES:
# #    - Be friendly, encouraging, and conversational
# #    - Use phrases like: "Great question!", "Let me think...", "Here's what I know..."
# #    - Keep responses brief for audio
# #    - After quiz ends, thank them and ask if they want more questions

# # 7. HANDLING UNKNOWN QUESTIONS:
# #    - If question isn't in database: "That's interesting! I don't have that in my quiz database, but I can ask you questions about [relevant topic from database]"

# # 8. QUIZ FLOW EXAMPLE:
# #    - You: "Would you like to try a quiz?"
# #    - User: "Yes"
# #    - You: "Great! First question: What is the capital of India? Options: A) Mumbai, B) Delhi, C) Kolkata"
# #    - User: "Can you repeat the options?"
# #    - You: "Of course! The options are: A) Mumbai, B) Delhi, C) Kolkata"
# #    - User: "B"
# #    - You: "Correct! Delhi is the capital of India. Next question: [next question]"

# # Start by greeting and offering a quiz session!"""
    
# #     # Create WebSocket transport
# #     ws_transport = FastAPIWebsocketTransport(
# #         websocket=websocket_client,
# #         params=FastAPIWebsocketParams(
# #             audio_in_enabled=True,
# #             audio_out_enabled=True,
# #             add_wav_header=False,
# #             vad_analyzer=SileroVADAnalyzer(),
# #             serializer=ProtobufFrameSerializer(),
# #         ),
# #     )

# #     # Create LLM service with fetched questions in system prompt
# #     llm = GeminiLiveLLMService(
# #         api_key=os.getenv("GOOGLE_API_KEY"),
# #         voice_id="Puck",
# #         transcribe_model_audio=True,
# #         system_instruction=system_instruction,
# #     )

# #     # Create conversation context
# #     context = LLMContext(
# #         [
# #             {
# #                 "role": "system",
# #                 "content": system_instruction
# #             },
# #             {
# #                 "role": "user",
# #                 "content": "Greet the user warmly. Ask them if you can start asking them the quiz questions."
# #             }
# #         ],
# #     )
# #     context_aggregator = LLMContextAggregatorPair(context)

# #     # RTVI for monitoring
# #     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

# #     # Build the pipeline
# #     pipeline = Pipeline(
# #         [
# #             ws_transport.input(),          # Receive audio from WebSocket
# #             context_aggregator.user(),     # Add user messages to context
# #             rtvi,                          # RTVI monitoring
# #             llm,                           # Gemini LLM with TTS
# #             ws_transport.output(),         # Send audio back via WebSocket
# #             context_aggregator.assistant(), # Add bot responses to context
# #         ]
# #     )

# #     # Create pipeline task
# #     task = PipelineTask(
# #         pipeline,
# #         params=PipelineParams(
# #             enable_metrics=True,
# #             enable_usage_metrics=True,
# #         ),
# #         observers=[RTVIObserver(rtvi)],
# #     )

# #     # Event handlers
# #     @rtvi.event_handler("on_client_ready")
# #     async def on_client_ready(rtvi):
# #         logger.info("✅ Pipecat client ready.")
# #         await rtvi.set_bot_ready()
# #         # Start the conversation
# #         await task.queue_frames([LLMRunFrame()])

# #     @ws_transport.event_handler("on_client_connected")
# #     async def on_client_connected(transport, client):
# #         logger.info("✅ Client connected via WebSocket")
# #         logger.info(f"📚 Bot loaded {len(api_questions_data) if api_questions_data else 0} questions from API")
# #         # Log first few questions for debugging
# #         if api_questions_data:
# #             for i, q in enumerate(api_questions_data[:3]):
# #                 question_text = q.get("question_text", "N/A")
# #                 correct_option = next((opt for opt in q.get("question_options", []) if opt.get("is_correct")), {})
# #                 correct_answer = correct_option.get("option_text", "Unknown")
# #                 logger.debug(f"  {i+1}. Q: {question_text}")
# #                 logger.debug(f"     A: {correct_answer}")

# #     @ws_transport.event_handler("on_client_disconnected")
# #     async def on_client_disconnected(transport, client):
# #         logger.info("❌ Client disconnected")
# #         await task.cancel()

# #     # Create and run the pipeline runner
# #     runner = PipelineRunner(handle_sigint=False)
    
# #     try:
# #         await runner.run(task)
# #     except Exception as e:
# #         logger.error(f"Error in pipeline: {e}")
# #         raise




# #===================================== FINAL WORKING CODE ==================================================================



# # import os
# # import aiohttp
# # import json
# # from typing import Optional, List
# # from dotenv import load_dotenv
# # from loguru import logger
# # from pipecat.audio.vad.silero import SileroVADAnalyzer
# # from pipecat.frames.frames import LLMRunFrame, TextFrame
# # from pipecat.pipeline.pipeline import Pipeline
# # from pipecat.pipeline.runner import PipelineRunner
# # from pipecat.pipeline.task import PipelineParams, PipelineTask
# # from pipecat.processors.aggregators.llm_context import LLMContext
# # from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# # from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# # from pipecat.serializers.protobuf import ProtobufFrameSerializer
# # from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# # from pipecat.transports.websocket.fastapi import (
# #     FastAPIWebsocketParams,
# #     FastAPIWebsocketTransport,
# # )

# # # Import FlowManager and related classes
# # from pipecat_flows import FlowManager, FlowResult, NodeConfig

# # load_dotenv(override=True)

# # # Node API configuration
# # NODE_API_URL = "http://localhost:3000"

# # # Predefined list of valid session codes
# # VALID_SESSIONS = [
# #     "H6TU",  # History Quiz
# #     "MTH4",  # Math Quiz
# #     "SCI8",  # Science Quiz
# #     "GEO2",  # Geography Quiz
# #     "ART9",  # Art Quiz
# #     "SPT5",  # Sports Quiz
# # ]

# # # Session descriptions for better UX
# # SESSION_DESCRIPTIONS = {
# #     "H6TU": "History Quiz - Test your knowledge of world history",
# #     "MTH4": "Math Quiz - Challenge your mathematical skills",
# #     "SCI8": "Science Quiz - Explore scientific discoveries",
# #     "GEO2": "Geography Quiz - Travel the world through questions",
# #     "ART9": "Art & Culture Quiz - Discover art and culture",
# #     "SPT5": "Sports Quiz - Test your sports knowledge",
# # }


# # # ============================================================================
# # # Type Definitions
# # # ============================================================================

# # class SessionCodeResult(FlowResult):
# #     """Result from session code validation"""
# #     session_code: str
# #     is_valid: bool
# #     description: str = ""


# # class QuizDataResult(FlowResult):
# #     """Result from fetching quiz data"""
# #     questions: list
# #     session_code: str
# #     session_name: str = ""


# # class UserResponseResult(FlowResult):
# #     """Result from user's answer"""
# #     question_index: int
# #     user_answer: str
# #     is_correct: bool
# #     correct_answer: str


# # class QuizProgressResult(FlowResult):
# #     """Current quiz progress"""
# #     current_question: int
# #     total_questions: int
# #     score: int
# #     session_code: str


# # # ============================================================================
# # # API Integration Functions
# # # ============================================================================

# # async def fetch_questions_from_api(session_code: str) -> list:
# #     """Fetch questions from Node API endpoint"""
# #     try:
# #         async with aiohttp.ClientSession() as session:
# #             async with session.get(
# #                 f"{NODE_API_URL}/api/sessions/{session_code}/questions",
# #                 timeout=aiohttp.ClientTimeout(total=5)
# #             ) as response:
# #                 if response.status == 200:
# #                     data = await response.json()
                    
# #                     # Check if response has expected format
# #                     if data.get("status") == "ok" and "data" in data:
# #                         questions_data = data["data"]
# #                         logger.info(f"✅ Successfully fetched {len(questions_data)} questions for session {session_code}")
# #                         return questions_data
# #                     else:
# #                         logger.error(f"❌ Unexpected API response format: {data}")
# #                         return []
# #                 else:
# #                     logger.error(f"❌ API returned status {response.status} for session {session_code}")
# #                     return []
# #     except Exception as e:
# #         logger.error(f"❌ Error fetching questions for session {session_code}: {e}")
# #         return []


# # def format_question_for_llm(question_data: dict) -> str:
# #     """Format a question from API into LLM-readable format"""
# #     question_text = question_data.get("question_text", "Unknown question")
# #     options = question_data.get("question_options", [])
    
# #     # Find correct answer
# #     correct_options = [opt for opt in options if opt.get("is_correct")]
# #     correct_answer = correct_options[0].get("option_text", "Unknown") if correct_options else "Unknown"
    
# #     # Format options
# #     options_text = ""
# #     for i, opt in enumerate(options, 1):
# #         option_text = opt.get("option_text", f"Option {i}")
# #         is_correct = opt.get("is_correct", False)
# #         options_text += f"  {i}. {option_text}"
# #         if is_correct:
# #             options_text += " ✓"
# #         options_text += "\n"
    
# #     return f"""Question: {question_text}
# # Options:
# # {options_text}
# # Answer: {correct_answer}"""


# # # ============================================================================
# # # Pre-action Handlers
# # # ============================================================================

# # async def validate_session_code(action: dict, flow_manager: FlowManager) -> None:
# #     """Validate the session code entered by user"""
# #     user_input = flow_manager.state.get("user_session_input", "").upper().strip()
# #     logger.info(f"🔍 Validating session code: {user_input}")
    
# #     if user_input in VALID_SESSIONS:
# #         flow_manager.state["session_code"] = user_input
# #         flow_manager.state["session_description"] = SESSION_DESCRIPTIONS.get(user_input, "")
# #         flow_manager.state["session_valid"] = True
# #         logger.info(f"✅ Valid session code: {user_input}")
# #     else:
# #         flow_manager.state["session_valid"] = False
# #         logger.warning(f"❌ Invalid session code: {user_input}")
        
# #         # Store suggestions for similar codes
# #         suggestions = []
# #         for valid_code in VALID_SESSIONS:
# #             if user_input and valid_code.startswith(user_input[:2]):
# #                 suggestions.append(valid_code)
# #         flow_manager.state["suggested_codes"] = suggestions


# # async def load_quiz_data(action: dict, flow_manager: FlowManager) -> None:
# #     """Load quiz questions from API for validated session"""
# #     session_code = flow_manager.state.get("session_code", "")
# #     if not session_code:
# #         logger.error("No session code to load questions for")
# #         return
    
# #     logger.info(f"📚 Loading quiz data for session: {session_code}")
    
# #     api_questions_data = await fetch_questions_from_api(session_code)
# #     flow_manager.state["quiz_questions"] = api_questions_data
# #     flow_manager.state["total_questions"] = len(api_questions_data)
# #     flow_manager.state["current_question"] = 0
# #     flow_manager.state["score"] = 0
    
# #     if not api_questions_data:
# #         logger.warning("⚠️ No questions loaded from API, using fallback")
# #         flow_manager.state["use_fallback"] = True
# #     else:
# #         logger.info(f"✅ Loaded {len(api_questions_data)} questions")


# # async def prepare_question(action: dict, flow_manager: FlowManager) -> None:
# #     """Prepare current question for asking"""
# #     questions = flow_manager.state.get("quiz_questions", [])
# #     current_idx = flow_manager.state.get("current_question", 0)
    
# #     if current_idx < len(questions):
# #         question_data = questions[current_idx]
# #         flow_manager.state["current_question_data"] = question_data
# #         logger.info(f"📝 Preparing question {current_idx + 1}: {question_data.get('question_text', 'Unknown')[:50]}...")
# #     else:
# #         flow_manager.state["current_question_data"] = None


# # # ============================================================================
# # # Direct Functions for Flow Nodes
# # # ============================================================================

# # async def provide_session_code(
# #     flow_manager: FlowManager, 
# #     session_code: str
# # ) -> tuple[SessionCodeResult, NodeConfig]:
# #     """
# #     User provides a session code.
    
# #     Args:
# #         session_code (str): The session code entered by user
# #     """
# #     # Store user input for validation
# #     flow_manager.state["user_session_input"] = session_code
    
# #     # Validate the session code
# #     session_code_upper = session_code.upper().strip()
# #     is_valid = session_code_upper in VALID_SESSIONS
# #     description = SESSION_DESCRIPTIONS.get(session_code_upper, "")
    
# #     result = SessionCodeResult(
# #         session_code=session_code_upper,
# #         is_valid=is_valid,
# #         description=description
# #     )
    
# #     if is_valid:
# #         flow_manager.state["session_code"] = session_code_upper
# #         flow_manager.state["session_description"] = description
# #         return result, create_session_confirmation_node()
# #     else:
# #         return result, create_invalid_session_node()


# # async def confirm_session_start(flow_manager: FlowManager) -> tuple[SessionCodeResult, NodeConfig]:
# #     """
# #     User confirms they want to start the session.
# #     """
# #     session_code = flow_manager.state.get("session_code", "")
# #     description = flow_manager.state.get("session_description", "")
    
# #     result = SessionCodeResult(
# #         session_code=session_code,
# #         is_valid=True,
# #         description=description
# #     )
    
# #     return result, create_loading_quiz_node()


# # async def try_different_session(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
# #     """
# #     User wants to try a different session code.
# #     """
# #     return None, create_welcome_node()


# # async def start_quiz_session(flow_manager: FlowManager) -> tuple[QuizDataResult, NodeConfig]:
# #     """
# #     Start the quiz session with loaded questions.
# #     """
# #     session_code = flow_manager.state.get("session_code", "")
# #     questions = flow_manager.state.get("quiz_questions", [])
# #     description = flow_manager.state.get("session_description", "")
    
# #     result = QuizDataResult(
# #         questions=questions,
# #         session_code=session_code,
# #         session_name=description
# #     )
    
# #     if len(questions) > 0:
# #         return result, create_ask_question_node()
# #     else:
# #         return result, create_no_questions_node()


# # async def answer_question(
# #     flow_manager: FlowManager, 
# #     user_answer: str
# # ) -> tuple[UserResponseResult, NodeConfig]:
# #     """
# #     Process user's answer to current question.
    
# #     Args:
# #         user_answer (str): User's answer (could be "A", "1", "Delhi", etc.)
# #     """
# #     current_idx = flow_manager.state.get("current_question", 0)
# #     question_data = flow_manager.state.get("current_question_data", {})
# #     questions = flow_manager.state.get("quiz_questions", [])
    
# #     # Get correct answer
# #     options = question_data.get("question_options", [])
# #     correct_options = [opt for opt in options if opt.get("is_correct")]
# #     correct_answer = correct_options[0].get("option_text", "") if correct_options else ""
    
# #     # Simple answer checking
# #     user_answer_clean = user_answer.strip().lower()
# #     correct_answer_clean = correct_answer.strip().lower()
# #     is_correct = user_answer_clean in correct_answer_clean or correct_answer_clean in user_answer_clean
    
# #     # Update score
# #     if is_correct:
# #         flow_manager.state["score"] = flow_manager.state.get("score", 0) + 1
    
# #     result = UserResponseResult(
# #         question_index=current_idx,
# #         user_answer=user_answer,
# #         is_correct=is_correct,
# #         correct_answer=correct_answer
# #     )
    
# #     # Move to next question or finish
# #     if current_idx + 1 < len(questions):
# #         flow_manager.state["current_question"] = current_idx + 1
# #         return result, create_feedback_and_next_node()
# #     else:
# #         return result, create_quiz_complete_node()


# # async def repeat_question(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
# #     """
# #     User wants to hear the question again.
# #     """
# #     return None, create_repeat_question_node()


# # async def skip_question(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
# #     """
# #     User wants to skip current question.
# #     """
# #     current_idx = flow_manager.state.get("current_question", 0)
# #     questions = flow_manager.state.get("quiz_questions", [])
    
# #     if current_idx + 1 < len(questions):
# #         flow_manager.state["current_question"] = current_idx + 1
# #         return None, create_ask_question_node()
# #     else:
# #         return None, create_quiz_complete_node()


# # async def end_quiz(flow_manager: FlowManager) -> tuple[QuizProgressResult, NodeConfig]:
# #     """
# #     User wants to end the quiz early.
# #     """
# #     total = flow_manager.state.get("total_questions", 0)
# #     answered = flow_manager.state.get("current_question", 0) + 1
# #     score = flow_manager.state.get("score", 0)
# #     session_code = flow_manager.state.get("session_code", "")
    
# #     result = QuizProgressResult(
# #         current_question=answered,
# #         total_questions=total,
# #         score=score,
# #         session_code=session_code
# #     )
    
# #     return result, create_quiz_complete_node()


# # # ============================================================================
# # # Node Creation Functions
# # # ============================================================================

# # def create_welcome_node() -> NodeConfig:
# #     """Create welcome node asking for session code"""
# #     return NodeConfig(
# #         name="welcome",
# #         role_messages=[
# #             {
# #                 "role": "system",
# #                 "content": """You are a friendly quiz master. Your role is to help users access quiz sessions."""
# #             }
# #         ],
# #         task_messages=[
# #             {
# #                 "role": "system",
# #                 "content": """Welcome the user to the Quiz Portal!
                
# #                 We have different quiz sessions available. To get started, I need you to provide a session code.
                
# #                 Available sessions:
# #                 - H6TU: History Quiz
# #                 - MTH4: Math Quiz  
# #                 - SCI8: Science Quiz
# #                 - GEO2: Geography Quiz
# #                 - ART9: Art & Culture Quiz
# #                 - SPT5: Sports Quiz
                
# #                 Please tell me your session code (for example: "H6TU" or "MTH4").
                
# #                 You can also ask "What sessions are available?" to hear the list again."""
# #             }
# #         ],
# #         functions=[provide_session_code],
# #     )


# # def create_session_confirmation_node() -> NodeConfig:
# #     """Create node to confirm session details"""
# #     return NodeConfig(
# #         name="session_confirm",
# #         task_messages=[
# #             {
# #                 "role": "system",
# #                 "content": """Confirm the session details with the user.
                
# #                 Format:
# #                 1. Acknowledge the session code (e.g., "Great! I found session H6TU")
# #                 2. Read the session description
# #                 3. Ask if they want to start this session
                
# #                 Example: "Great! I found session H6TU - History Quiz. 
# #                 This session tests your knowledge of world history. 
# #                 Would you like to start this quiz session?"""
# #             }
# #         ],
# #         functions=[confirm_session_start, try_different_session],
# #     )


# # def create_invalid_session_node() -> NodeConfig:
# #     """Create node for invalid session code"""
# #     return NodeConfig(
# #         name="invalid_session",
# #         task_messages=[
# #             {
# #                 "role": "system",
# #                 "content": """The session code provided is not valid.
                
# #                 Tell the user:
# #                 1. Apologize that the session code wasn't found
# #                 2. List the available session codes again
# #                 3. Ask them to try a different code or ask for help
                
# #                 Be helpful and encouraging."""
# #             }
# #         ],
# #         functions=[provide_session_code],
# #     )


# # def create_loading_quiz_node() -> NodeConfig:
# #     """Create node while loading quiz data"""
# #     return NodeConfig(
# #         name="loading_quiz",
# #         task_messages=[
# #             {
# #                 "role": "system", 
# #                 "content": "Tell the user you're loading their quiz session. Say something like: 'Perfect! Loading your quiz session now...'"
# #             }
# #         ],
# #         pre_actions=[
# #             {
# #                 "type": "function",
# #                 "handler": load_quiz_data,
# #             },
# #         ],
# #         post_actions=[
# #             {
# #                 "type": "function",
# #                 "handler": lambda a, fm: fm.transition_to(create_start_quiz_node())
# #             },
# #         ],
# #     )


# # def create_start_quiz_node() -> NodeConfig:
# #     """Create node to start the actual quiz"""
# #     return NodeConfig(
# #         name="start_quiz",
# #         task_messages=[
# #             {
# #                 "role": "system",
# #                 "content": """Briefly explain what to expect in the quiz and ask if they're ready to start.
                
# #                 Example: "I've loaded your quiz session! You'll be asked multiple choice questions. 
# #                 Just say the letter or number of your answer. Ready to begin?"""
# #             }
# #         ],
# #         functions=[start_quiz_session],
# #     )


# # def create_ask_question_node() -> NodeConfig:
# #     """Create node to ask current question"""
# #     return NodeConfig(
# #         name="ask_question",
# #         task_messages=[
# #             {
# #                 "role": "system",
# #                 "content": """ASK THE CURRENT QUESTION from the quiz database.
                
# #                 Format:
# #                 1. State the question number and total (e.g., "Question 1 of 5:")
# #                 2. Clearly state the question
# #                 3. List all options with letters (A, B, C, D) or numbers (1, 2, 3, 4)
# #                 4. Wait for their answer
                
# #                 Example: "Question 1 of 5: What is the capital of France? 
# #                 A) London, B) Berlin, C) Paris, D) Madrid"
                
# #                 IMPORTANT: Use the actual question and options from the loaded quiz data."""
# #             }
# #         ],
# #         pre_actions=[
# #             {
# #                 "type": "function", 
# #                 "handler": prepare_question,
# #             },
# #         ],
# #         functions=[answer_question, repeat_question, skip_question, end_quiz],
# #     )


# # def create_repeat_question_node() -> NodeConfig:
# #     """Create node to repeat the current question"""
# #     return NodeConfig(
# #         name="repeat_question",
# #         task_messages=[
# #             {
# #                 "role": "system",
# #                 "content": """Repeat the current question and options clearly.
# #                 Say: "Let me repeat that. [Question text]. The options are: [list options]"
# #                 Then wait for their answer."""
# #             }
# #         ],
# #         functions=[answer_question, skip_question, end_quiz],
# #     )


# # def create_feedback_and_next_node() -> NodeConfig:
# #     """Create node to give feedback and move to next question"""
# #     return NodeConfig(
# #         name="feedback_next",
# #         task_messages=[
# #             {
# #                 "role": "system",
# #                 "content": """Give brief feedback on their last answer.
# #                 If correct: "That's right! [Brief explanation or encouragement]"
# #                 If incorrect: "Actually, the correct answer is [correct answer]. [Brief explanation]"
                
# #                 Then say: "Let's move to the next question." and proceed."""
# #             }
# #         ],
# #         functions=[],  # Auto-proceeds after feedback
# #         post_actions=[
# #             {
# #                 "type": "function",
# #                 "handler": lambda a, fm: fm.transition_to(create_ask_question_node())
# #             },
# #         ],
# #     )


# # def create_quiz_complete_node() -> NodeConfig:
# #     """Create node for quiz completion"""
# #     return NodeConfig(
# #         name="quiz_complete",
# #         task_messages=[
# #             {
# #                 "role": "system",
# #                 "content": """Thank them for completing the quiz!
# #                 Share their score: "You got [score] out of [total] correct in the [session name]!"
# #                 Give encouraging feedback based on score.
# #                 Ask if they'd like to try another session or have any questions."""
# #             }
# #         ],
# #         post_actions=[
# #             {
# #                 "type": "end_conversation",
# #             },
# #         ],
# #     )


# # def create_no_questions_node() -> NodeConfig:
# #     """Create node when no questions are available"""
# #     return NodeConfig(
# #         name="no_questions",
# #         task_messages=[
# #             {
# #                 "role": "system",
# #                 "content": """Apologize that no questions are available for this session at the moment.
# #                 Suggest they try a different session code or try again later.
# #                 List the available session codes again."""
# #             }
# #         ],
# #         functions=[try_different_session, end_quiz],
# #     )


# # # ============================================================================
# # # Global Functions (available in all nodes)
# # # ============================================================================

# # async def list_available_sessions(flow_manager: FlowManager) -> tuple[dict, None]:
# #     """List all available session codes"""
# #     sessions_list = []
# #     for code in VALID_SESSIONS:
# #         description = SESSION_DESCRIPTIONS.get(code, "")
# #         sessions_list.append(f"{code}: {description}")
    
# #     return {
# #         "sessions": VALID_SESSIONS,
# #         "descriptions": SESSION_DESCRIPTIONS,
# #         "formatted_list": "\n".join(sessions_list)
# #     }, None


# # async def get_session_info(flow_manager: FlowManager) -> tuple[dict, None]:
# #     """Get current session information"""
# #     return {
# #         "session_code": flow_manager.state.get("session_code", "Not selected"),
# #         "session_description": flow_manager.state.get("session_description", ""),
# #         "total_questions": flow_manager.state.get("total_questions", 0),
# #         "current_question": flow_manager.state.get("current_question", 0) + 1,
# #         "score": flow_manager.state.get("score", 0),
# #         "questions_loaded": len(flow_manager.state.get("quiz_questions", []))
# #     }, None


# # async def get_question_hint(flow_manager: FlowManager) -> tuple[str, None]:
# #     """Provide a hint for current question"""
# #     question_data = flow_manager.state.get("current_question_data", {})
# #     question_text = question_data.get("question_text", "")
    
# #     # Simple hint based on question length or content
# #     if "capital" in question_text.lower():
# #         return "Think about countries and their main cities", None
# #     elif "year" in question_text.lower() or "century" in question_text.lower():
# #         return "Consider historical time periods", None
# #     else:
# #         return "Think about the main topic mentioned in the question", None


# # # ============================================================================
# # # Main Bot Function with Flow Manager
# # # ============================================================================

# # async def run_bot(websocket_client, initial_session_code: Optional[str] = None):
# #     """Run the quiz bot with session code validation"""
# #     print(f"🤖 Starting quiz bot")
    
# #     # Create WebSocket transport
# #     ws_transport = FastAPIWebsocketTransport(
# #         websocket=websocket_client,
# #         params=FastAPIWebsocketParams(
# #             audio_in_enabled=True,
# #             audio_out_enabled=True,
# #             add_wav_header=False,
# #             vad_analyzer=SileroVADAnalyzer(),
# #             serializer=ProtobufFrameSerializer(),
# #         ),
# #     )

# #     # Create LLM service
# #     llm = GeminiLiveLLMService(
# #         api_key=os.getenv("GOOGLE_API_KEY"),
# #         voice_id="Puck",
# #         transcribe_model_audio=True,
# #         system_instruction="You are a quiz master assistant. Help users access and navigate quiz sessions.",
# #     )

# #     # Create conversation context
# #     context = LLMContext()
# #     context_aggregator = LLMContextAggregatorPair(context)

# #     # RTVI for monitoring
# #     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

# #     # Build the pipeline
# #     pipeline = Pipeline(
# #         [
# #             ws_transport.input(),          # Receive audio from WebSocket
# #             context_aggregator.user(),     # Add user messages to context
# #             rtvi,                          # RTVI monitoring
# #             llm,                           # Gemini LLM with TTS
# #             ws_transport.output(),         # Send audio back via WebSocket
# #             context_aggregator.assistant(), # Add bot responses to context
# #         ]
# #     )

# #     # Create pipeline task
# #     task = PipelineTask(
# #         pipeline,
# #         params=PipelineParams(
# #             enable_metrics=True,
# #             enable_usage_metrics=True,
# #             allow_interruptions=True,
# #         ),
# #         observers=[RTVIObserver(rtvi)],
# #     )

# #     # Initialize flow manager
# #     flow_manager = FlowManager(
# #         task=task,
# #         llm=llm,
# #         context_aggregator=context_aggregator,
# #         transport=ws_transport,
# #         global_functions=[list_available_sessions, get_session_info, get_question_hint],
# #     )
    
# #     # If initial session code provided, pre-validate it
# #     if initial_session_code and initial_session_code.upper() in VALID_SESSIONS:
# #         flow_manager.state["session_code"] = initial_session_code.upper()
# #         flow_manager.state["session_description"] = SESSION_DESCRIPTIONS.get(
# #             initial_session_code.upper(), ""
# #         )
# #         flow_manager.state["session_valid"] = True
# #         start_node = create_session_confirmation_node()
# #     else:
# #         start_node = create_welcome_node()

# #     # Event handlers
# #     @rtvi.event_handler("on_client_ready")
# #     async def on_client_ready(rtvi):
# #         logger.info("✅ Pipecat client ready.")
# #         await rtvi.set_bot_ready()
# #         # Initialize the flow
# #         await flow_manager.initialize(start_node)

# #     @ws_transport.event_handler("on_client_connected")
# #     async def on_client_connected(transport, client):
# #         logger.info("✅ Client connected via WebSocket")
# #         if initial_session_code:
# #             logger.info(f"📋 Initial session code provided: {initial_session_code}")

# #     @ws_transport.event_handler("on_client_disconnected")
# #     async def on_client_disconnected(transport, client):
# #         logger.info("❌ Client disconnected")
# #         await task.cancel()

# #     # Create and run the pipeline runner
# #     runner = PipelineRunner(handle_sigint=False)
    
# #     try:
# #         await runner.run(task)
# #     except Exception as e:
# #         logger.error(f"Error in pipeline: {e}")
# #         raise


# # # ============================================================================
# # # Updated Helper Functions
# # # ============================================================================

# # def create_quiz_system_prompt(session_code: str, questions_data: list) -> str:
# #     """Create dynamic system prompt based on session and questions"""
# #     session_desc = SESSION_DESCRIPTIONS.get(session_code, f"Session {session_code}")
    
# #     if not questions_data:
# #         return f"""You are a quiz master for {session_desc}. 
# #         No questions are available for this session at the moment. 
# #         Apologize and suggest trying a different session."""
    
# #     formatted_questions = "\n\n".join([
# #         format_question_for_llm(q) for q in questions_data
# #     ])
    
# #     return f"""You are an interactive quiz master for {session_desc}.

# # QUESTIONS DATABASE:
# # {formatted_questions}

# # INSTRUCTIONS:
# # 1. Ask ONE question at a time from the database
# # 2. Clearly state question number and total
# # 3. List options clearly (A, B, C, etc.)
# # 4. Accept answers as letters or numbers
# # 5. Provide feedback after each answer
# # 6. Keep responses conversational and encouraging
# # 7. Mention the session topic when appropriate"""

# import os
# import aiohttp
# import json
# from typing import Optional
# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.frames.frames import LLMRunFrame, TextFrame
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# # Import FlowManager and related classes (assuming you have them or need to implement)
# from pipecat_flows import FlowManager, FlowResult, NodeConfig

# load_dotenv(override=True)

# # Node API configuration
# NODE_API_URL = "http://localhost:3000"


# # ============================================================================
# # Type Definitions
# # ============================================================================

# class QuizDataResult(FlowResult):
#     """Result from fetching quiz data"""
#     questions: list
#     session_code: str


# class UserResponseResult(FlowResult):
#     """Result from user's answer"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str


# class QuizProgressResult(FlowResult):
#     """Current quiz progress"""
#     current_question: int
#     total_questions: int
#     score: int

# class SessionDataResults(FlowResult):
#     """Result from fetching session data"""
#     sessions: list
#     total: int


# # ============================================================================
# # API Integration Functions
# # ============================================================================

# async def fetch_questions_from_api(session_code: str = "H6TU") -> list:
#     """Fetch questions from Node API endpoint"""
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f"{NODE_API_URL}/api/sessions/{session_code}/questions",
#                 timeout=aiohttp.ClientTimeout(total=5)
#             ) as response:
#                 if response.status == 200:
#                     data = await response.json()
                    
#                     # Check if response has expected format
#                     if data.get("status") == "ok" and "data" in data:
#                         questions_data = data["data"]
#                         logger.info(f"✅ Successfully fetched {len(questions_data)} questions from API")
#                         return questions_data
#                     else:
#                         logger.error(f"❌ Unexpected API response format: {data}")
#                         return []
#                 else:
#                     logger.error(f"❌ API returned status {response.status}")
#                     return []
#     except Exception as e:
#         logger.error(f"❌ Error fetching questions: {e}")
#         return []

# async def fetch_sessions_from_api() -> list:
#     """Fetch sessions from Node API endpoint"""
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f"{NODE_API_URL}/api/session/getSessions",
#                 timeout=aiohttp.ClientTimeout(total=5)
#             ) as response:
#                 if response.status == 200:
#                     data = await response.json()
                    
#                     # Updated: Check for "success" instead of "status"
#                     if data.get("success") and "data" in data:  # Changed "status" to "success"
#                         sessions_data = data["data"]
#                         logger.info(f"✅ Successfully fetched {len(sessions_data)} sessions from API")
#                         return sessions_data
#                     else:
#                         logger.error(f"❌ Unexpected API response format: {data}")
#                         return []
#                 else:
#                     logger.error(f"❌ API returned status {response.status}")
#                     return []
#     except Exception as e:
#         logger.error(f"❌ Error fetching sessions: {e}")
#         return []


# def format_question_for_llm(question_data: dict) -> str:
#     """Format a question from API into LLM-readable format"""
#     question_text = question_data.get("question_text", "Unknown question")
#     options = question_data.get("question_options", [])
    
#     # Find correct answer
#     correct_options = [opt for opt in options if opt.get("is_correct")]
#     correct_answer = correct_options[0].get("option_text", "Unknown") if correct_options else "Unknown"
    
#     # Format options
#     options_text = ""
#     for i, opt in enumerate(options, 1):
#         option_text = opt.get("option_text", f"Option {i}")
#         is_correct = opt.get("is_correct", False)
#         options_text += f"  {i}. {option_text}"
#         if is_correct:
#             options_text += " ✓"
#         options_text += "\n"
    
#     return f"""Question: {question_text}
# Options:
# {options_text}
# Answer: {correct_answer}"""


# # ============================================================================
# # Pre-action Handlers
# # ============================================================================

# # async def load_quiz_data(action: dict, flow_manager: FlowManager) -> None:
# #     """Load quiz questions from API before starting"""
# #     session_code = flow_manager.state.get("session_code", "H6TU")
# #     logger.info(f"📚 Loading quiz data for session: {session_code}")
    
# #     api_questions_data = await fetch_questions_from_api(session_code)
# #     flow_manager.state["quiz_questions"] = api_questions_data
# #     flow_manager.state["total_questions"] = len(api_questions_data)
# #     flow_manager.state["current_question"] = 0
# #     flow_manager.state["score"] = 0
    
# #     if not api_questions_data:
# #         logger.warning("⚠️ No questions loaded from API, using fallback")
# #         flow_manager.state["use_fallback"] = True
# #     else:
# #         logger.info(f"✅ Loaded {len(api_questions_data)} questions")

# async def load_questions_for_session(action: dict, flow_manager: FlowManager) -> None:
#     """Load questions for the current session from API"""
#     session_code = flow_manager.state.get("session_code", "")
    
#     if not session_code:
#         logger.error("❌ No session code found in state")
#         return
    
#     logger.info(f"📚 Loading questions for session: {session_code}")
    
#     api_questions_data = await fetch_questions_from_api(session_code)
#     flow_manager.state["quiz_questions"] = api_questions_data
#     flow_manager.state["total_questions"] = len(api_questions_data)
#     flow_manager.state["current_question"] = 0
#     flow_manager.state["score"] = 0
    
#     if not api_questions_data:
#         logger.warning("⚠️ No questions loaded from API")
#         flow_manager.state["use_fallback"] = True
#     else:
#         logger.info(f"✅ Loaded {len(api_questions_data)} questions")


# async def prepare_question(action: dict, flow_manager: FlowManager) -> None:
#     """Prepare current question for asking"""
#     questions = flow_manager.state.get("quiz_questions", [])
#     current_idx = flow_manager.state.get("current_question", 0)
    
#     if current_idx < len(questions):
#         question_data = questions[current_idx]
#         flow_manager.state["current_question_data"] = question_data
#         formatted_question = format_question_for_llm(question_data)
        
#         logger.info(f"📝 Preparing question {current_idx + 1}: {question_data.get('question_text', 'Unknown')[:50]}...")
#     else:
#         flow_manager.state["current_question_data"] = None

# async def load_session_data(action: dict, flow_manager: FlowManager) -> None:
#     """Load all available sessions from the node API"""
#     api_sessions_data = await fetch_sessions_from_api()
#     flow_manager.state["sessions"] = api_sessions_data
#     flow_manager.state["total_sessions"] = len(api_sessions_data)

#     if not api_sessions_data:
#         logger.warning("⚠️ No sessions loaded from API, using fallback")
#         flow_manager.state["use_fallback"] = True
#     else:
#         logger.info(f"✅ Loaded {len(api_sessions_data)} sessions")


# # ============================================================================
# # Direct Functions for Flow Nodes
# # ============================================================================

# # async def start_quiz_session(flow_manager: FlowManager) -> tuple[QuizDataResult, NodeConfig]:
# #     """
# #     User wants to start a quiz session.
# #     """
# #     # Quiz data already loaded in pre-action
# #     questions = flow_manager.state.get("quiz_questions", [])
# #     total = len(questions)
    
# #     result = QuizDataResult(questions=questions, session_code=flow_manager.state.get("session_code", "H6TU"))
    
# #     if total > 0:
# #         return result, create_ask_question_node()
# #     else:
# #         return result, create_no_questions_node()

# # async def start_quiz_session(flow_manager : FlowManager) -> tuple[SessionDataResults, NodeConfig]:
# #     """User tells the session code and you validate the session"""

# #     sessions = flow_manager.state.get("sessions",[])
# #     total = len(sessions)
# #     result = SessionDataResults(sessions=sessions, total=total)

# #     if total > 0:
# #         if flow_manager.state.get("session_code", "") in sessions:
# #             return result, create_ask_question_node()
# #         else:
# #             return result, create_no_questions_node()
# #     else:
# #         return result, create_no_questions_node()

# from pipecat.frames.frames import LLMRunFrame

# async def prepare_and_set_question(action: dict, flow_manager: FlowManager) -> None:
#     questions = flow_manager.state.get("quiz_questions", [])
#     idx = flow_manager.state.get("current_question", 0)

#     if idx >= len(questions):
#         return

#     q = questions[idx]
#     formatted = format_question_for_llm(q)
#     question_part = formatted.split("Answer:")[0].strip()

#     prompt = f"""
#     Read the following question aloud clearly and confidently.

#     Question {idx + 1}:
#     {question_part}

#     After reading, wait silently for the user's answer.
#     """

#     # ✅ Inject into LLM context
#     flow_manager.context_aggregator.context.add_message(
#         role="system",
#         content=prompt
#     )

#     # ✅ Trigger Gemini inference (THIS is what causes speech)
#     await flow_manager.task.queue_frames([LLMRunFrame()])

#     flow_manager.state["current_question_data"] = q




# async def start_quiz_session(
#     flow_manager: FlowManager, 
#     session_code: Optional[str] = None
# ) -> tuple[SessionDataResults, NodeConfig]:
#     """User tells the session code and you validate the session"""
    
#     # Use provided session_code or get from state
#     if session_code:
#         flow_manager.state["session_code"] = session_code
#     else:
#         session_code = flow_manager.state.get("session_code", "")
    
#     sessions = flow_manager.state.get("sessions", [])
#     total = len(sessions)
    
#     # Check if session code exists in sessions
#     session_exists = any(
#         session.get("join_code") == session_code or 
#         session.get("session_code") == session_code 
#         for session in sessions
#     )
    
#     result = SessionDataResults(sessions=sessions, total=total)

#     if total > 0 and session_exists:
#         logger.info("going to create ask question node")
#         logger.info(f"📚 Loading questions for session: {session_code}")
#         api_questions_data = await fetch_questions_from_api(session_code)
        
#         if api_questions_data:
#             flow_manager.state["quiz_questions"] = api_questions_data
#             flow_manager.state["total_questions"] = len(api_questions_data)
#             flow_manager.state["current_question"] = 0
#             flow_manager.state["score"] = 0
#             logger.info(f"✅ Loaded {len(api_questions_data)} questions")
            
            
#             # Go straight to question preparation
#             return result, create_ask_question_node()
#         else:
#             logger.warning("⚠️ No questions found for this session")
#             return result, create_no_questions_node()
#     else:
#         logger.info("going to create no questions node")
#         return result, create_no_questions_node()
    


# async def answer_question(
#     flow_manager: FlowManager, 
#     user_answer: str
# ) -> tuple[UserResponseResult, NodeConfig]:
#     """
#     Process user's answer to current question.
    
#     Args:
#         user_answer (str): User's answer (could be "A", "1", "Delhi", etc.)
#     """
#     current_idx = flow_manager.state.get("current_question", 0)
#     question_data = flow_manager.state.get("current_question_data", {})
#     questions = flow_manager.state.get("quiz_questions", [])
    
#     # Get correct answer
#     options = question_data.get("question_options", [])
#     correct_options = [opt for opt in options if opt.get("is_correct")]
#     correct_answer = correct_options[0].get("option_text", "") if correct_options else ""
    
#     # Simple answer checking (in production, you'd want more robust matching)
#     user_answer_clean = user_answer.strip().lower()
#     correct_answer_clean = correct_answer.strip().lower()
#     is_correct = user_answer_clean in correct_answer_clean or correct_answer_clean in user_answer_clean
    
#     # Update score
#     if is_correct:
#         flow_manager.state["score"] = flow_manager.state.get("score", 0) + 1
    
#     result = UserResponseResult(
#         question_index=current_idx,
#         user_answer=user_answer,
#         is_correct=is_correct,
#         correct_answer=correct_answer
#     )
    
#     # Move to next question or finish
#     if current_idx + 1 < len(questions):
#         flow_manager.state["current_question"] = current_idx + 1
#         return result, create_feedback_and_next_node()
#     else:
#         return result, create_quiz_complete_node()


# async def repeat_question(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
#     """
#     User wants to hear the question again.
#     """
#     return None, create_repeat_question_node()


# async def skip_question(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
#     """
#     User wants to skip current question.
#     """
#     current_idx = flow_manager.state.get("current_question", 0)
#     questions = flow_manager.state.get("quiz_questions", [])
    
#     if current_idx + 1 < len(questions):
#         flow_manager.state["current_question"] = current_idx + 1
#         return None, create_ask_question_node()
#     else:
#         return None, create_quiz_complete_node()


# async def end_quiz(flow_manager: FlowManager) -> tuple[QuizProgressResult, NodeConfig]:
#     """
#     User wants to end the quiz early.
#     """
#     total = flow_manager.state.get("total_questions", 0)
#     answered = flow_manager.state.get("current_question", 0) + 1
#     score = flow_manager.state.get("score", 0)
    
#     result = QuizProgressResult(
#         current_question=answered,
#         total_questions=total,
#         score=score
#     )
    
#     return result, create_quiz_complete_node()


# # ============================================================================
# # Node Creation Functions
# # ============================================================================

# def create_welcome_node() -> NodeConfig:
#     """Create welcome node with quiz invitation"""
#     return NodeConfig(
#         name="welcome",
#         role_messages=[
#             {
#                 "role": "system",
#                 "content": """You are a friendly quiz master. Your role is to engage users in a fun quiz session.
#                 Be enthusiastic, encouraging, and clear in your speech."""
#             }
#         ],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Welcome the user warmly to the quiz session. 
#                 You're first job is to get the session code from the user and validate the session.
#                 If the session is valid, then ask the user if they want to start the quiz.
#                 " """
#             }
#         ],
#         pre_actions=[
#             {
#                 "type": "function",
#                 "handler": load_session_data, #load_quiz_data
#             },
#         ],
#         functions=[start_quiz_session],
#     )



# # def create_ask_question_node() -> NodeConfig:
# #     """Create node to ask current question"""
# #     return NodeConfig(
# #         name="ask_question",
# #         task_messages=[
# #              {
# #                 "role": "system",
# #                 "content": """Always read the {flow_manager.state["current_question_instruction"]} from the database. the question is loaded using a pre set function"""
# #             }
# #         ],
# #         pre_actions=[
# #             {
# #                 "type": "function", 
# #                 "handler": prepare_and_set_question,
# #             },
# #         ],
# #         functions=[answer_question, repeat_question, skip_question, end_quiz],
# #     )

# def create_ask_question_node() -> NodeConfig:
#     return NodeConfig(
#         name="ask_question",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "Ask the following quiz question clearly and wait for the user's answer:\n\n"
#                     "{quiz_questions}"
#                 ),
#             }
#         ],
#         functions=[answer_question, repeat_question, skip_question, end_quiz],
#     )



# def create_repeat_question_node() -> NodeConfig:
#     """Create node to repeat the current question"""
#     return NodeConfig(
#         name="repeat_question",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Repeat the current question and options clearly.
#                 Say: "Let me repeat that. [Question text]. The options are: [list options]"
#                 Then wait for their answer."""
#             }
#         ],
#         functions=[answer_question, skip_question, end_quiz],
#     )


# def create_feedback_and_next_node() -> NodeConfig:
#     """Create node to give feedback and move to next question"""
#     return NodeConfig(
#         name="feedback_next",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Give brief feedback on their last answer.
#                 If correct: "That's right! [Brief explanation or encouragement]"
#                 If incorrect: "Actually, the correct answer is [correct answer]. [Brief explanation]"
                
#                 Then say: "Let's move to the next question." and proceed."""
#             }
#         ],
#         functions=[],  # Auto-proceeds after feedback
#         post_actions=[
#             {
#                 "type": "function",
#                 "handler": lambda a, fm: fm.transition_to(create_ask_question_node())
#             },
#         ],
#     )


# def create_quiz_complete_node() -> NodeConfig:
#     """Create node for quiz completion"""
#     return NodeConfig(
#         name="quiz_complete",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Thank them for completing the quiz!
#                 Share their score: "You got [score] out of [total] correct!"
#                 Give encouraging feedback based on score.
#                 Ask if they'd like to try another session or have any questions."""
#             }
#         ],
#         post_actions=[
#             {
#                 "type": "end_conversation",
#             },
#         ],
#     )


# def create_no_questions_node() -> NodeConfig:
#     """Create node when no questions are available"""
#     return NodeConfig(
#         name="no_questions",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Apologize that no questions are available at the moment.
#                 Suggest they try again later or contact support.
#                 Offer to answer any general knowledge questions you have in your database."""
#             }
#         ],
#         functions=[end_quiz],
#     )


# # ============================================================================
# # Global Functions (available in all nodes)
# # ============================================================================

# async def get_session_info(flow_manager: FlowManager) -> tuple[dict, None]:
#     """Get current session information"""
#     return {
#         "session_code": flow_manager.state.get("session_code", "H6TU"),
#         "total_questions": flow_manager.state.get("total_questions", 0),
#         "current_question": flow_manager.state.get("current_question", 0) + 1,
#         "score": flow_manager.state.get("score", 0)
#     }, None


# async def get_question_hint(flow_manager: FlowManager) -> tuple[str, None]:
#     """Provide a hint for current question"""
#     question_data = flow_manager.state.get("current_question_data", {})
#     # Could implement hint logic based on question type
#     return "Think about the main topic of the question", None


# # ============================================================================
# # Main Bot Function with Flow Manager
# # ============================================================================

# async def run_bot(websocket_client, session_code: str = "H6TU"):
#     """Run the quiz bot with flow management"""
#     print(f"🤖 Starting quiz bot for session: {session_code}")
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create LLM service
#     llm = GeminiLiveLLMService(
#     api_key=os.getenv("GOOGLE_API_KEY"),
#     config={
#         "system_instruction": "You are QuizMaster AI, an engaging quiz host. Be energetic, clear, and supportive. Speak naturally in a conversational tone."
#     }
# )

#     # Create conversation context
#     context = LLMContext()
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),          # Receive audio from WebSocket
#             context_aggregator.user(),     # Add user messages to context
#             rtvi,                          # RTVI monitoring
#             llm,                           # Gemini LLM with TTS
#             ws_transport.output(),         # Send audio back via WebSocket
#             context_aggregator.assistant(), # Add bot responses to context
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#             allow_interruptions=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Initialize flow manager
#     flow_manager = FlowManager(
#         task=task,
#         llm=llm,
#         context_aggregator=context_aggregator,
#         transport=ws_transport,
#         global_functions=[get_session_info, get_question_hint],
#     )
    
#     # Store session code in state
#     flow_manager.state["session_code"] = session_code

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Initialize the flow with welcome node
#         await flow_manager.initialize(create_welcome_node())

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise


# # ============================================================================
# # Helper function to format quiz data for LLM context
# # ============================================================================

# def create_quiz_system_prompt(questions_data: list) -> str:
#     """Create dynamic system prompt based on quiz questions"""
#     if not questions_data:
#         return """You are a quiz master. No questions are available at the moment. 
#         Apologize and offer to answer general knowledge questions."""
    
#     formatted_questions = "\n\n".join([
#         format_question_for_llm(q) for q in questions_data
#     ])
    
#     return f"""You are an interactive quiz master.

# QUESTIONS DATABASE:
# {formatted_questions}

# INSTRUCTIONS:
# 1. Ask ONE question at a time from the database
# 2. Clearly state question number and options
# 3. Accept answers as letters (A, B, C) or numbers (1, 2, 3)
# 4. Provide feedback after each answer
# 5. Keep responses conversational and encouraging"""


# # ============================================================================
# # Alternative: Simple version without FlowManager dependency
# # ============================================================================

# async def run_bot_simple(websocket_client, session_code: str = "H6TU"):
#     """Simpler version without FlowManager for quick implementation"""
#     print(f"🤖 Starting simple quiz bot for session: {session_code}")
    
#     # Fetch questions
#     questions_data = await fetch_questions_from_api(session_code)
#     system_prompt = create_quiz_system_prompt(questions_data)
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create LLM service with dynamic system prompt
#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         voice_id="Puck",
#         transcribe_model_audio=True,
#         system_instruction=system_prompt,
#     )

#     # Create conversation context
#     context = LLMContext(
#         [
#             {
#                 "role": "system",
#                 "content": system_prompt
#             },
#             {
#                 "role": "user",
#                 "content": "Greet the user warmly. Ask them if you can start asking them the quiz questions. Start with the first question from the database."
#             }
#         ],
#     )
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),          # Receive audio from WebSocket
#             context_aggregator.user(),     # Add user messages to context
#             rtvi,                          # RTVI monitoring
#             llm,                           # Gemini LLM with TTS
#             ws_transport.output(),         # Send audio back via WebSocket
#             context_aggregator.assistant(), # Add bot responses to context
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         await task.queue_frames([LLMRunFrame()])

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")
#         logger.info(f"📚 Loaded {len(questions_data)} questions")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise




# import os
# import sys

# from dotenv import load_dotenv
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
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# load_dotenv(override=True)

# logger.remove(0)
# logger.add(sys.stderr, level="DEBUG")


# SYSTEM_INSTRUCTION = f"""
# "You are Gemini Chatbot, a friendly, helpful robot.

# Your goal is to demonstrate your capabilities in a succinct way.

# Your output will be converted to audio so don't include special characters in your answers.

# Respond to what the user said in a creative and helpful way. Keep your responses brief. One or two sentences at most.
# """


# async def run_bot(websocket_client):
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
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

#     RTVI events for Pipecat client UI
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
#         Kick off the conversation.
#         await task.queue_frames([LLMRunFrame()])

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("Pipecat Client connected")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("Pipecat Client disconnected")
#         await task.cancel()

#     runner = PipelineRunner(handle_sigint=False)

#     await runner.run(task)

# import os
# import sys

# from dotenv import load_dotenv
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
# 1. Import the Whisper STT Service
# from pipecat.services.whisper import WhisperSTTService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# load_dotenv(override=True)

# logger.remove(0)
# logger.add(sys.stderr, level="DEBUG")

# SYSTEM_INSTRUCTION = """
# You are Gemini Chatbot, a friendly, helpful robot.
# Your goal is to demonstrate your capabilities in a succinct way.
# Your output will be converted to audio so don't include special characters in your answers.
# Respond to what the user said in a creative and helpful way. Keep your responses brief. One or two sentences at most.
# """

# async def run_bot(websocket_client):
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     2. Initialize Whisper STT pointed at your Docker container
#     Replace 'http://localhost:9000' with your actual Docker container address
#     stt = WhisperSTTService(
#         url="http://localhost:11435/v1", 
#         model="base"
#     )

#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         voice_id="Puck",
#         3. CRITICAL: Disable internal transcription to use external Whisper text
#         transcribe_model_audio=False,
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

#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     4. Insert STT into the pipeline before the context aggregator
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),
#             stt,                     # Added ASR stage
#             context_aggregator.user(),
#             rtvi,
#             llm,
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
#         await task.queue_frames([LLMRunFrame()])

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("Pipecat Client connected")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("Pipecat Client disconnected")
#         await task.cancel()

#     runner = PipelineRunner(handle_sigint=False)

#     await runner.run(task)

# bot_fast_api.py
#
# Copyright (c) 2024-2026, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

# """Pipecat Flows: Local Whisper ASR + Gemini LLM"""

# import os
# import aiohttp
# import json
# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.frames.frames import LLMRunFrame, TextFrame
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.processors.frame_processor import FrameProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# load_dotenv(override=True)

# # Node API configuration
# NODE_API_URL = "http://localhost:3000"


# async def fetch_questions_from_api(session_code: str = "H6TU") -> list:
#     """Fetch questions from Node API endpoint"""
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f"{NODE_API_URL}/api/sessions/{session_code}/questions",
#                 timeout=aiohttp.ClientTimeout(total=5)
#             ) as response:
#                 if response.status == 200:
#                     data = await response.json()
                    
#                     # Check if response has expected format
#                     if data.get("status") == "ok" and "data" in data:
#                         questions_data = data["data"]
#                         logger.info(f"✅ Successfully fetched {len(questions_data)} questions from API")
#                         return questions_data
#                     else:
#                         logger.error(f"❌ Unexpected API response format: {data}")
#                         return []
#                 else:
#                     logger.error(f"❌ API returned status {response.status}")
#                     return []
#     except Exception as e:
#         logger.error(f"❌ Error fetching questions: {e}")
#         return []

# def format_question_for_llm(question_data: dict) -> str:
#     """Format a question from API into LLM-readable format"""
#     question_text = question_data.get("question_text", "Unknown question")
#     options = question_data.get("question_options", [])
    
#     # Find correct answer
#     correct_options = [opt for opt in options if opt.get("is_correct")]
#     correct_answer = correct_options[0].get("option_text", "Unknown") if correct_options else "Unknown"
    
#     # Format options
#     options_text = ""
#     for i, opt in enumerate(options, 1):
#         option_text = opt.get("option_text", f"Option {i}")
#         is_correct = opt.get("is_correct", False)
#         options_text += f"  {i}. {option_text}"
#         if is_correct:
#             options_text += " ✓"
#         options_text += "\n"
    
#     return f"""Question: {question_text}
# Options:
# {options_text}
# Answer: {correct_answer}"""

# async def run_bot(websocket_client,session_code: str = "H6TU"):
#     """This function runs the bot pipeline for a WebSocket connection"""
#     print(f"🤖 Starting bot for session: {session_code}")
#     # Fetch questions from Node API before creating the bot
#     api_questions_data = await fetch_questions_from_api(session_code)
    
#     if not api_questions_data:
#         logger.warning("⚠️ No questions fetched from API, using fallback")
#         # Create fallback questions
#         formatted_questions = """Question: What is the capital of France?
# Options:
#   1. Mumbai
#   2. Delhi ✓
#   3. Kolkata
# Answer: Delhi

# Question: Which planet is known as the Red Planet?
# Options:
#   1. Venus
#   2. Mars ✓
#   3. Jupiter
# Answer: Mars"""
#     else:
#         # Format all questions for LLM
#         formatted_questions = "\n\n".join([
#             format_question_for_llm(q) for q in api_questions_data
#         ])
#         print(formatted_questions)
    
#     # Create dynamic system instruction with fetched questions
#     system_instruction = f"""You are an interactive quiz master and Q&A assistant.

# I will provide you with quiz questions, their options, and correct answers. Your primary role is to ask these questions conversationally.

# QUESTIONS DATABASE:
# {formatted_questions}

# CRITICAL INSTRUCTIONS FOR QUIZ MASTER MODE:
# 1. START BY ASKING: Begin by greeting and asking if the user would like to take a quiz or answer questions.

# 2. WHEN USER SAYS YES TO QUIZ:
#    - Ask ONE question at a time from the database above
#    - Clearly state the question
#    - List ALL the options properly (A, B, C, etc.)
#    - Wait for their answer
#    - After they answer, give brief feedback and move to next question

# 3. WHEN USER ASKS TO REPEAT:
#    - If user says "repeat", "say that again", "what were the options", "can you repeat the question", or similar:
#    - REPEAT THE ENTIRE QUESTION with all options clearly
#    - Use the exact same wording as before
#    - Example: "Sure! Let me repeat that. The question was: [question text]. Your options are: A) [option 1], B) [option 2], C) [option 3]"

# 4. WHEN USER ASKS FOR OPTIONS AGAIN:
#    - If user asks "what are the options", "options please", "choices again":
#    - Repeat JUST the options clearly: "The options are: A) [option 1], B) [option 2], C) [option 3]"

# 5. ANSWERING USER QUESTIONS:
#    - If user asks a question that matches one in the database, provide the correct answer
#    - Example: If user asks "What's the capital of India?", answer "Delhi" and explain

# 6. CONVERSATIONAL RULES:
#    - Be friendly, encouraging, and conversational
#    - Use phrases like: "Great question!", "Let me think...", "Here's what I know..."
#    - Keep responses brief for audio
#    - After quiz ends, thank them and ask if they want more questions

# 7. HANDLING UNKNOWN QUESTIONS:
#    - If question isn't in database: "That's interesting! I don't have that in my quiz database, but I can ask you questions about [relevant topic from database]"

# 8. QUIZ FLOW EXAMPLE:
#    - You: "Would you like to try a quiz?"
#    - User: "Yes"
#    - You: "Great! First question: What is the capital of India? Options: A) Mumbai, B) Delhi, C) Kolkata"
#    - User: "Can you repeat the options?"
#    - You: "Of course! The options are: A) Mumbai, B) Delhi, C) Kolkata"
#    - User: "B"
#    - You: "Correct! Delhi is the capital of India. Next question: [next question]"

# Start by greeting and offering a quiz session!"""
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create LLM service with fetched questions in system prompt
#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         voice_id="Puck",
#         transcribe_model_audio=True,
#         system_instruction=system_instruction,
#     )

#     # Create conversation context
#     context = LLMContext(
#         [
#             {
#                 "role": "system",
#                 "content": system_instruction
#             },
#             {
#                 "role": "user",
#                 "content": "Greet the user warmly. Ask them if you can start asking them the quiz questions."
#             }
#         ],
#     )
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),          # Receive audio from WebSocket
#             context_aggregator.user(),     # Add user messages to context
#             rtvi,                          # RTVI monitoring
#             llm,                           # Gemini LLM with TTS
#             ws_transport.output(),         # Send audio back via WebSocket
#             context_aggregator.assistant(), # Add bot responses to context
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Start the conversation
#         await task.queue_frames([LLMRunFrame()])

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")
#         logger.info(f"📚 Bot loaded {len(api_questions_data) if api_questions_data else 0} questions from API")
#         # Log first few questions for debugging
#         if api_questions_data:
#             for i, q in enumerate(api_questions_data[:3]):
#                 question_text = q.get("question_text", "N/A")
#                 correct_option = next((opt for opt in q.get("question_options", []) if opt.get("is_correct")), {})
#                 correct_answer = correct_option.get("option_text", "Unknown")
#                 logger.debug(f"  {i+1}. Q: {question_text}")
#                 logger.debug(f"     A: {correct_answer}")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise




#===================================== FINAL WORKING CODE ==================================================================



# import os
# import aiohttp
# import json
# from typing import Optional, List
# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.frames.frames import LLMRunFrame, TextFrame
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# # Import FlowManager and related classes
# from pipecat_flows import FlowManager, FlowResult, NodeConfig

# load_dotenv(override=True)

# # Node API configuration
# NODE_API_URL = "http://localhost:3000"

# # Predefined list of valid session codes
# VALID_SESSIONS = [
#     "H6TU",  # History Quiz
#     "MTH4",  # Math Quiz
#     "SCI8",  # Science Quiz
#     "GEO2",  # Geography Quiz
#     "ART9",  # Art Quiz
#     "SPT5",  # Sports Quiz
# ]

# # Session descriptions for better UX
# SESSION_DESCRIPTIONS = {
#     "H6TU": "History Quiz - Test your knowledge of world history",
#     "MTH4": "Math Quiz - Challenge your mathematical skills",
#     "SCI8": "Science Quiz - Explore scientific discoveries",
#     "GEO2": "Geography Quiz - Travel the world through questions",
#     "ART9": "Art & Culture Quiz - Discover art and culture",
#     "SPT5": "Sports Quiz - Test your sports knowledge",
# }


# # ============================================================================
# # Type Definitions
# # ============================================================================

# class SessionCodeResult(FlowResult):
#     """Result from session code validation"""
#     session_code: str
#     is_valid: bool
#     description: str = ""


# class QuizDataResult(FlowResult):
#     """Result from fetching quiz data"""
#     questions: list
#     session_code: str
#     session_name: str = ""


# class UserResponseResult(FlowResult):
#     """Result from user's answer"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str


# class QuizProgressResult(FlowResult):
#     """Current quiz progress"""
#     current_question: int
#     total_questions: int
#     score: int
#     session_code: str


# # ============================================================================
# # API Integration Functions
# # ============================================================================

# async def fetch_questions_from_api(session_code: str) -> list:
#     """Fetch questions from Node API endpoint"""
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f"{NODE_API_URL}/api/sessions/{session_code}/questions",
#                 timeout=aiohttp.ClientTimeout(total=5)
#             ) as response:
#                 if response.status == 200:
#                     data = await response.json()
                    
#                     # Check if response has expected format
#                     if data.get("status") == "ok" and "data" in data:
#                         questions_data = data["data"]
#                         logger.info(f"✅ Successfully fetched {len(questions_data)} questions for session {session_code}")
#                         return questions_data
#                     else:
#                         logger.error(f"❌ Unexpected API response format: {data}")
#                         return []
#                 else:
#                     logger.error(f"❌ API returned status {response.status} for session {session_code}")
#                     return []
#     except Exception as e:
#         logger.error(f"❌ Error fetching questions for session {session_code}: {e}")
#         return []


# def format_question_for_llm(question_data: dict) -> str:
#     """Format a question from API into LLM-readable format"""
#     question_text = question_data.get("question_text", "Unknown question")
#     options = question_data.get("question_options", [])
    
#     # Find correct answer
#     correct_options = [opt for opt in options if opt.get("is_correct")]
#     correct_answer = correct_options[0].get("option_text", "Unknown") if correct_options else "Unknown"
    
#     # Format options
#     options_text = ""
#     for i, opt in enumerate(options, 1):
#         option_text = opt.get("option_text", f"Option {i}")
#         is_correct = opt.get("is_correct", False)
#         options_text += f"  {i}. {option_text}"
#         if is_correct:
#             options_text += " ✓"
#         options_text += "\n"
    
#     return f"""Question: {question_text}
# Options:
# {options_text}
# Answer: {correct_answer}"""


# # ============================================================================
# # Pre-action Handlers
# # ============================================================================

# async def validate_session_code(action: dict, flow_manager: FlowManager) -> None:
#     """Validate the session code entered by user"""
#     user_input = flow_manager.state.get("user_session_input", "").upper().strip()
#     logger.info(f"🔍 Validating session code: {user_input}")
    
#     if user_input in VALID_SESSIONS:
#         flow_manager.state["session_code"] = user_input
#         flow_manager.state["session_description"] = SESSION_DESCRIPTIONS.get(user_input, "")
#         flow_manager.state["session_valid"] = True
#         logger.info(f"✅ Valid session code: {user_input}")
#     else:
#         flow_manager.state["session_valid"] = False
#         logger.warning(f"❌ Invalid session code: {user_input}")
        
#         # Store suggestions for similar codes
#         suggestions = []
#         for valid_code in VALID_SESSIONS:
#             if user_input and valid_code.startswith(user_input[:2]):
#                 suggestions.append(valid_code)
#         flow_manager.state["suggested_codes"] = suggestions


# async def load_quiz_data(action: dict, flow_manager: FlowManager) -> None:
#     """Load quiz questions from API for validated session"""
#     session_code = flow_manager.state.get("session_code", "")
#     if not session_code:
#         logger.error("No session code to load questions for")
#         return
    
#     logger.info(f"📚 Loading quiz data for session: {session_code}")
    
#     api_questions_data = await fetch_questions_from_api(session_code)
#     flow_manager.state["quiz_questions"] = api_questions_data
#     flow_manager.state["total_questions"] = len(api_questions_data)
#     flow_manager.state["current_question"] = 0
#     flow_manager.state["score"] = 0
    
#     if not api_questions_data:
#         logger.warning("⚠️ No questions loaded from API, using fallback")
#         flow_manager.state["use_fallback"] = True
#     else:
#         logger.info(f"✅ Loaded {len(api_questions_data)} questions")


# async def prepare_question(action: dict, flow_manager: FlowManager) -> None:
#     """Prepare current question for asking"""
#     questions = flow_manager.state.get("quiz_questions", [])
#     current_idx = flow_manager.state.get("current_question", 0)
    
#     if current_idx < len(questions):
#         question_data = questions[current_idx]
#         flow_manager.state["current_question_data"] = question_data
#         logger.info(f"📝 Preparing question {current_idx + 1}: {question_data.get('question_text', 'Unknown')[:50]}...")
#     else:
#         flow_manager.state["current_question_data"] = None


# # ============================================================================
# # Direct Functions for Flow Nodes
# # ============================================================================

# async def provide_session_code(
#     flow_manager: FlowManager, 
#     session_code: str
# ) -> tuple[SessionCodeResult, NodeConfig]:
#     """
#     User provides a session code.
    
#     Args:
#         session_code (str): The session code entered by user
#     """
#     # Store user input for validation
#     flow_manager.state["user_session_input"] = session_code
    
#     # Validate the session code
#     session_code_upper = session_code.upper().strip()
#     is_valid = session_code_upper in VALID_SESSIONS
#     description = SESSION_DESCRIPTIONS.get(session_code_upper, "")
    
#     result = SessionCodeResult(
#         session_code=session_code_upper,
#         is_valid=is_valid,
#         description=description
#     )
    
#     if is_valid:
#         flow_manager.state["session_code"] = session_code_upper
#         flow_manager.state["session_description"] = description
#         return result, create_session_confirmation_node()
#     else:
#         return result, create_invalid_session_node()


# async def confirm_session_start(flow_manager: FlowManager) -> tuple[SessionCodeResult, NodeConfig]:
#     """
#     User confirms they want to start the session.
#     """
#     session_code = flow_manager.state.get("session_code", "")
#     description = flow_manager.state.get("session_description", "")
    
#     result = SessionCodeResult(
#         session_code=session_code,
#         is_valid=True,
#         description=description
#     )
    
#     return result, create_loading_quiz_node()


# async def try_different_session(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
#     """
#     User wants to try a different session code.
#     """
#     return None, create_welcome_node()


# async def start_quiz_session(flow_manager: FlowManager) -> tuple[QuizDataResult, NodeConfig]:
#     """
#     Start the quiz session with loaded questions.
#     """
#     session_code = flow_manager.state.get("session_code", "")
#     questions = flow_manager.state.get("quiz_questions", [])
#     description = flow_manager.state.get("session_description", "")
    
#     result = QuizDataResult(
#         questions=questions,
#         session_code=session_code,
#         session_name=description
#     )
    
#     if len(questions) > 0:
#         return result, create_ask_question_node()
#     else:
#         return result, create_no_questions_node()


# async def answer_question(
#     flow_manager: FlowManager, 
#     user_answer: str
# ) -> tuple[UserResponseResult, NodeConfig]:
#     """
#     Process user's answer to current question.
    
#     Args:
#         user_answer (str): User's answer (could be "A", "1", "Delhi", etc.)
#     """
#     current_idx = flow_manager.state.get("current_question", 0)
#     question_data = flow_manager.state.get("current_question_data", {})
#     questions = flow_manager.state.get("quiz_questions", [])
    
#     # Get correct answer
#     options = question_data.get("question_options", [])
#     correct_options = [opt for opt in options if opt.get("is_correct")]
#     correct_answer = correct_options[0].get("option_text", "") if correct_options else ""
    
#     # Simple answer checking
#     user_answer_clean = user_answer.strip().lower()
#     correct_answer_clean = correct_answer.strip().lower()
#     is_correct = user_answer_clean in correct_answer_clean or correct_answer_clean in user_answer_clean
    
#     # Update score
#     if is_correct:
#         flow_manager.state["score"] = flow_manager.state.get("score", 0) + 1
    
#     result = UserResponseResult(
#         question_index=current_idx,
#         user_answer=user_answer,
#         is_correct=is_correct,
#         correct_answer=correct_answer
#     )
    
#     # Move to next question or finish
#     if current_idx + 1 < len(questions):
#         flow_manager.state["current_question"] = current_idx + 1
#         return result, create_feedback_and_next_node()
#     else:
#         return result, create_quiz_complete_node()


# async def repeat_question(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
#     """
#     User wants to hear the question again.
#     """
#     return None, create_repeat_question_node()


# async def skip_question(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
#     """
#     User wants to skip current question.
#     """
#     current_idx = flow_manager.state.get("current_question", 0)
#     questions = flow_manager.state.get("quiz_questions", [])
    
#     if current_idx + 1 < len(questions):
#         flow_manager.state["current_question"] = current_idx + 1
#         return None, create_ask_question_node()
#     else:
#         return None, create_quiz_complete_node()


# async def end_quiz(flow_manager: FlowManager) -> tuple[QuizProgressResult, NodeConfig]:
#     """
#     User wants to end the quiz early.
#     """
#     total = flow_manager.state.get("total_questions", 0)
#     answered = flow_manager.state.get("current_question", 0) + 1
#     score = flow_manager.state.get("score", 0)
#     session_code = flow_manager.state.get("session_code", "")
    
#     result = QuizProgressResult(
#         current_question=answered,
#         total_questions=total,
#         score=score,
#         session_code=session_code
#     )
    
#     return result, create_quiz_complete_node()


# # ============================================================================
# # Node Creation Functions
# # ============================================================================

# def create_welcome_node() -> NodeConfig:
#     """Create welcome node asking for session code"""
#     return NodeConfig(
#         name="welcome",
#         role_messages=[
#             {
#                 "role": "system",
#                 "content": """You are a friendly quiz master. Your role is to help users access quiz sessions."""
#             }
#         ],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Welcome the user to the Quiz Portal!
                
#                 We have different quiz sessions available. To get started, I need you to provide a session code.
                
#                 Available sessions:
#                 - H6TU: History Quiz
#                 - MTH4: Math Quiz  
#                 - SCI8: Science Quiz
#                 - GEO2: Geography Quiz
#                 - ART9: Art & Culture Quiz
#                 - SPT5: Sports Quiz
                
#                 Please tell me your session code (for example: "H6TU" or "MTH4").
                
#                 You can also ask "What sessions are available?" to hear the list again."""
#             }
#         ],
#         functions=[provide_session_code],
#     )


# def create_session_confirmation_node() -> NodeConfig:
#     """Create node to confirm session details"""
#     return NodeConfig(
#         name="session_confirm",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Confirm the session details with the user.
                
#                 Format:
#                 1. Acknowledge the session code (e.g., "Great! I found session H6TU")
#                 2. Read the session description
#                 3. Ask if they want to start this session
                
#                 Example: "Great! I found session H6TU - History Quiz. 
#                 This session tests your knowledge of world history. 
#                 Would you like to start this quiz session?"""
#             }
#         ],
#         functions=[confirm_session_start, try_different_session],
#     )


# def create_invalid_session_node() -> NodeConfig:
#     """Create node for invalid session code"""
#     return NodeConfig(
#         name="invalid_session",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """The session code provided is not valid.
                
#                 Tell the user:
#                 1. Apologize that the session code wasn't found
#                 2. List the available session codes again
#                 3. Ask them to try a different code or ask for help
                
#                 Be helpful and encouraging."""
#             }
#         ],
#         functions=[provide_session_code],
#     )


# def create_loading_quiz_node() -> NodeConfig:
#     """Create node while loading quiz data"""
#     return NodeConfig(
#         name="loading_quiz",
#         task_messages=[
#             {
#                 "role": "system", 
#                 "content": "Tell the user you're loading their quiz session. Say something like: 'Perfect! Loading your quiz session now...'"
#             }
#         ],
#         pre_actions=[
#             {
#                 "type": "function",
#                 "handler": load_quiz_data,
#             },
#         ],
#         post_actions=[
#             {
#                 "type": "function",
#                 "handler": lambda a, fm: fm.transition_to(create_start_quiz_node())
#             },
#         ],
#     )


# def create_start_quiz_node() -> NodeConfig:
#     """Create node to start the actual quiz"""
#     return NodeConfig(
#         name="start_quiz",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Briefly explain what to expect in the quiz and ask if they're ready to start.
                
#                 Example: "I've loaded your quiz session! You'll be asked multiple choice questions. 
#                 Just say the letter or number of your answer. Ready to begin?"""
#             }
#         ],
#         functions=[start_quiz_session],
#     )


# def create_ask_question_node() -> NodeConfig:
#     """Create node to ask current question"""
#     return NodeConfig(
#         name="ask_question",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """ASK THE CURRENT QUESTION from the quiz database.
                
#                 Format:
#                 1. State the question number and total (e.g., "Question 1 of 5:")
#                 2. Clearly state the question
#                 3. List all options with letters (A, B, C, D) or numbers (1, 2, 3, 4)
#                 4. Wait for their answer
                
#                 Example: "Question 1 of 5: What is the capital of France? 
#                 A) London, B) Berlin, C) Paris, D) Madrid"
                
#                 IMPORTANT: Use the actual question and options from the loaded quiz data."""
#             }
#         ],
#         pre_actions=[
#             {
#                 "type": "function", 
#                 "handler": prepare_question,
#             },
#         ],
#         functions=[answer_question, repeat_question, skip_question, end_quiz],
#     )


# def create_repeat_question_node() -> NodeConfig:
#     """Create node to repeat the current question"""
#     return NodeConfig(
#         name="repeat_question",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Repeat the current question and options clearly.
#                 Say: "Let me repeat that. [Question text]. The options are: [list options]"
#                 Then wait for their answer."""
#             }
#         ],
#         functions=[answer_question, skip_question, end_quiz],
#     )


# def create_feedback_and_next_node() -> NodeConfig:
#     """Create node to give feedback and move to next question"""
#     return NodeConfig(
#         name="feedback_next",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Give brief feedback on their last answer.
#                 If correct: "That's right! [Brief explanation or encouragement]"
#                 If incorrect: "Actually, the correct answer is [correct answer]. [Brief explanation]"
                
#                 Then say: "Let's move to the next question." and proceed."""
#             }
#         ],
#         functions=[],  # Auto-proceeds after feedback
#         post_actions=[
#             {
#                 "type": "function",
#                 "handler": lambda a, fm: fm.transition_to(create_ask_question_node())
#             },
#         ],
#     )


# def create_quiz_complete_node() -> NodeConfig:
#     """Create node for quiz completion"""
#     return NodeConfig(
#         name="quiz_complete",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Thank them for completing the quiz!
#                 Share their score: "You got [score] out of [total] correct in the [session name]!"
#                 Give encouraging feedback based on score.
#                 Ask if they'd like to try another session or have any questions."""
#             }
#         ],
#         post_actions=[
#             {
#                 "type": "end_conversation",
#             },
#         ],
#     )


# def create_no_questions_node() -> NodeConfig:
#     """Create node when no questions are available"""
#     return NodeConfig(
#         name="no_questions",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Apologize that no questions are available for this session at the moment.
#                 Suggest they try a different session code or try again later.
#                 List the available session codes again."""
#             }
#         ],
#         functions=[try_different_session, end_quiz],
#     )


# # ============================================================================
# # Global Functions (available in all nodes)
# # ============================================================================

# async def list_available_sessions(flow_manager: FlowManager) -> tuple[dict, None]:
#     """List all available session codes"""
#     sessions_list = []
#     for code in VALID_SESSIONS:
#         description = SESSION_DESCRIPTIONS.get(code, "")
#         sessions_list.append(f"{code}: {description}")
    
#     return {
#         "sessions": VALID_SESSIONS,
#         "descriptions": SESSION_DESCRIPTIONS,
#         "formatted_list": "\n".join(sessions_list)
#     }, None


# async def get_session_info(flow_manager: FlowManager) -> tuple[dict, None]:
#     """Get current session information"""
#     return {
#         "session_code": flow_manager.state.get("session_code", "Not selected"),
#         "session_description": flow_manager.state.get("session_description", ""),
#         "total_questions": flow_manager.state.get("total_questions", 0),
#         "current_question": flow_manager.state.get("current_question", 0) + 1,
#         "score": flow_manager.state.get("score", 0),
#         "questions_loaded": len(flow_manager.state.get("quiz_questions", []))
#     }, None


# async def get_question_hint(flow_manager: FlowManager) -> tuple[str, None]:
#     """Provide a hint for current question"""
#     question_data = flow_manager.state.get("current_question_data", {})
#     question_text = question_data.get("question_text", "")
    
#     # Simple hint based on question length or content
#     if "capital" in question_text.lower():
#         return "Think about countries and their main cities", None
#     elif "year" in question_text.lower() or "century" in question_text.lower():
#         return "Consider historical time periods", None
#     else:
#         return "Think about the main topic mentioned in the question", None


# # ============================================================================
# # Main Bot Function with Flow Manager
# # ============================================================================

# async def run_bot(websocket_client, initial_session_code: Optional[str] = None):
#     """Run the quiz bot with session code validation"""
#     print(f"🤖 Starting quiz bot")
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create LLM service
#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         voice_id="Puck",
#         transcribe_model_audio=True,
#         system_instruction="You are a quiz master assistant. Help users access and navigate quiz sessions.",
#     )

#     # Create conversation context
#     context = LLMContext()
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),          # Receive audio from WebSocket
#             context_aggregator.user(),     # Add user messages to context
#             rtvi,                          # RTVI monitoring
#             llm,                           # Gemini LLM with TTS
#             ws_transport.output(),         # Send audio back via WebSocket
#             context_aggregator.assistant(), # Add bot responses to context
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#             allow_interruptions=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Initialize flow manager
#     flow_manager = FlowManager(
#         task=task,
#         llm=llm,
#         context_aggregator=context_aggregator,
#         transport=ws_transport,
#         global_functions=[list_available_sessions, get_session_info, get_question_hint],
#     )
    
#     # If initial session code provided, pre-validate it
#     if initial_session_code and initial_session_code.upper() in VALID_SESSIONS:
#         flow_manager.state["session_code"] = initial_session_code.upper()
#         flow_manager.state["session_description"] = SESSION_DESCRIPTIONS.get(
#             initial_session_code.upper(), ""
#         )
#         flow_manager.state["session_valid"] = True
#         start_node = create_session_confirmation_node()
#     else:
#         start_node = create_welcome_node()

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Initialize the flow
#         await flow_manager.initialize(start_node)

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")
#         if initial_session_code:
#             logger.info(f"📋 Initial session code provided: {initial_session_code}")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise


# # ============================================================================
# # Updated Helper Functions
# # ============================================================================

# def create_quiz_system_prompt(session_code: str, questions_data: list) -> str:
#     """Create dynamic system prompt based on session and questions"""
#     session_desc = SESSION_DESCRIPTIONS.get(session_code, f"Session {session_code}")
    
#     if not questions_data:
#         return f"""You are a quiz master for {session_desc}. 
#         No questions are available for this session at the moment. 
#         Apologize and suggest trying a different session."""
    
#     formatted_questions = "\n\n".join([
#         format_question_for_llm(q) for q in questions_data
#     ])
    
#     return f"""You are an interactive quiz master for {session_desc}.

# QUESTIONS DATABASE:
# {formatted_questions}

# INSTRUCTIONS:
# 1. Ask ONE question at a time from the database
# 2. Clearly state question number and total
# 3. List options clearly (A, B, C, etc.)
# 4. Accept answers as letters or numbers
# 5. Provide feedback after each answer
# 6. Keep responses conversational and encouraging
# 7. Mention the session topic when appropriate"""

# import os
# import aiohttp
# import json
# from typing import Optional
# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.frames.frames import LLMRunFrame, TextFrame
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# # Import FlowManager and related classes (assuming you have them or need to implement)
# from pipecat_flows import FlowManager, FlowResult, NodeConfig

# load_dotenv(override=True)

# # Node API configuration
# NODE_API_URL = "http://localhost:3000"


# # ============================================================================
# # Type Definitions
# # ============================================================================

# class QuizDataResult(FlowResult):
#     """Result from fetching quiz data"""
#     questions: list
#     session_code: str


# class UserResponseResult(FlowResult):
#     """Result from user's answer"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str


# class QuizProgressResult(FlowResult):
#     """Current quiz progress"""
#     current_question: int
#     total_questions: int
#     score: int

# class SessionDataResults(FlowResult):
#     """Result from fetching session data"""
#     sessions: list
#     total: int


# # ============================================================================
# # API Integration Functions
# # ============================================================================

# async def fetch_questions_from_api(session_code: str = "H6TU") -> list:
#     """Fetch questions from Node API endpoint"""
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f"{NODE_API_URL}/api/sessions/{session_code}/questions",
#                 timeout=aiohttp.ClientTimeout(total=5)
#             ) as response:
#                 if response.status == 200:
#                     data = await response.json()
                    
#                     # Check if response has expected format
#                     if data.get("status") == "ok" and "data" in data:
#                         questions_data = data["data"]
#                         logger.info(f"✅ Successfully fetched {len(questions_data)} questions from API")
#                         return questions_data
#                     else:
#                         logger.error(f"❌ Unexpected API response format: {data}")
#                         return []
#                 else:
#                     logger.error(f"❌ API returned status {response.status}")
#                     return []
#     except Exception as e:
#         logger.error(f"❌ Error fetching questions: {e}")
#         return []

# async def fetch_sessions_from_api() -> list:
#     """Fetch sessions from Node API endpoint"""
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f"{NODE_API_URL}/api/session/getSessions",
#                 timeout=aiohttp.ClientTimeout(total=5)
#             ) as response:
#                 if response.status == 200:
#                     data = await response.json()
                    
#                     # Updated: Check for "success" instead of "status"
#                     if data.get("success") and "data" in data:  # Changed "status" to "success"
#                         sessions_data = data["data"]
#                         logger.info(f"✅ Successfully fetched {len(sessions_data)} sessions from API")
#                         return sessions_data
#                     else:
#                         logger.error(f"❌ Unexpected API response format: {data}")
#                         return []
#                 else:
#                     logger.error(f"❌ API returned status {response.status}")
#                     return []
#     except Exception as e:
#         logger.error(f"❌ Error fetching sessions: {e}")
#         return []


# def format_question_for_llm(question_data: dict) -> str:
#     """Format a question from API into LLM-readable format"""
#     question_text = question_data.get("question_text", "Unknown question")
#     options = question_data.get("question_options", [])
    
#     # Find correct answer
#     correct_options = [opt for opt in options if opt.get("is_correct")]
#     correct_answer = correct_options[0].get("option_text", "Unknown") if correct_options else "Unknown"
    
#     # Format options
#     options_text = ""
#     for i, opt in enumerate(options, 1):
#         option_text = opt.get("option_text", f"Option {i}")
#         is_correct = opt.get("is_correct", False)
#         options_text += f"  {i}. {option_text}"
#         if is_correct:
#             options_text += " ✓"
#         options_text += "\n"
    
#     return f"""Question: {question_text}
# Options:
# {options_text}
# Answer: {correct_answer}"""


# # ============================================================================
# # Pre-action Handlers
# # ============================================================================

# # async def load_quiz_data(action: dict, flow_manager: FlowManager) -> None:
# #     """Load quiz questions from API before starting"""
# #     session_code = flow_manager.state.get("session_code", "H6TU")
# #     logger.info(f"📚 Loading quiz data for session: {session_code}")
    
# #     api_questions_data = await fetch_questions_from_api(session_code)
# #     flow_manager.state["quiz_questions"] = api_questions_data
# #     flow_manager.state["total_questions"] = len(api_questions_data)
# #     flow_manager.state["current_question"] = 0
# #     flow_manager.state["score"] = 0
    
# #     if not api_questions_data:
# #         logger.warning("⚠️ No questions loaded from API, using fallback")
# #         flow_manager.state["use_fallback"] = True
# #     else:
# #         logger.info(f"✅ Loaded {len(api_questions_data)} questions")

# async def load_questions_for_session(action: dict, flow_manager: FlowManager) -> None:
#     """Load questions for the current session from API"""
#     session_code = flow_manager.state.get("session_code", "")
    
#     if not session_code:
#         logger.error("❌ No session code found in state")
#         return
    
#     logger.info(f"📚 Loading questions for session: {session_code}")
    
#     api_questions_data = await fetch_questions_from_api(session_code)
#     flow_manager.state["quiz_questions"] = api_questions_data
#     flow_manager.state["total_questions"] = len(api_questions_data)
#     flow_manager.state["current_question"] = 0
#     flow_manager.state["score"] = 0
    
#     if not api_questions_data:
#         logger.warning("⚠️ No questions loaded from API")
#         flow_manager.state["use_fallback"] = True
#     else:
#         logger.info(f"✅ Loaded {len(api_questions_data)} questions")


# async def prepare_question(action: dict, flow_manager: FlowManager) -> None:
#     """Prepare current question for asking"""
#     questions = flow_manager.state.get("quiz_questions", [])
#     current_idx = flow_manager.state.get("current_question", 0)
    
#     if current_idx < len(questions):
#         question_data = questions[current_idx]
#         flow_manager.state["current_question_data"] = question_data
#         formatted_question = format_question_for_llm(question_data)
        
#         logger.info(f"📝 Preparing question {current_idx + 1}: {question_data.get('question_text', 'Unknown')[:50]}...")
#     else:
#         flow_manager.state["current_question_data"] = None

# async def load_session_data(action: dict, flow_manager: FlowManager) -> None:
#     """Load all available sessions from the node API"""
#     api_sessions_data = await fetch_sessions_from_api()
#     flow_manager.state["sessions"] = api_sessions_data
#     flow_manager.state["total_sessions"] = len(api_sessions_data)

#     if not api_sessions_data:
#         logger.warning("⚠️ No sessions loaded from API, using fallback")
#         flow_manager.state["use_fallback"] = True
#     else:
#         logger.info(f"✅ Loaded {len(api_sessions_data)} sessions")


# # ============================================================================
# # Direct Functions for Flow Nodes
# # ============================================================================

# # async def start_quiz_session(flow_manager: FlowManager) -> tuple[QuizDataResult, NodeConfig]:
# #     """
# #     User wants to start a quiz session.
# #     """
# #     # Quiz data already loaded in pre-action
# #     questions = flow_manager.state.get("quiz_questions", [])
# #     total = len(questions)
    
# #     result = QuizDataResult(questions=questions, session_code=flow_manager.state.get("session_code", "H6TU"))
    
# #     if total > 0:
# #         return result, create_ask_question_node()
# #     else:
# #         return result, create_no_questions_node()

# # async def start_quiz_session(flow_manager : FlowManager) -> tuple[SessionDataResults, NodeConfig]:
# #     """User tells the session code and you validate the session"""

# #     sessions = flow_manager.state.get("sessions",[])
# #     total = len(sessions)
# #     result = SessionDataResults(sessions=sessions, total=total)

# #     if total > 0:
# #         if flow_manager.state.get("session_code", "") in sessions:
# #             return result, create_ask_question_node()
# #         else:
# #             return result, create_no_questions_node()
# #     else:
# #         return result, create_no_questions_node()

# from pipecat.frames.frames import LLMRunFrame

# async def prepare_and_set_question(action: dict, flow_manager: FlowManager) -> None:
#     questions = flow_manager.state.get("quiz_questions", [])
#     idx = flow_manager.state.get("current_question", 0)

#     if idx >= len(questions):
#         return

#     q = questions[idx]
#     formatted = format_question_for_llm(q)
#     question_part = formatted.split("Answer:")[0].strip()

#     prompt = f"""
#     Read the following question aloud clearly and confidently.

#     Question {idx + 1}:
#     {question_part}

#     After reading, wait silently for the user's answer.
#     """

#     # ✅ Inject into LLM context
#     flow_manager.context_aggregator.context.add_message(
#         role="system",
#         content=prompt
#     )

#     # ✅ Trigger Gemini inference (THIS is what causes speech)
#     await flow_manager.task.queue_frames([LLMRunFrame()])

#     flow_manager.state["current_question_data"] = q




# async def start_quiz_session(
#     flow_manager: FlowManager, 
#     session_code: Optional[str] = None
# ) -> tuple[SessionDataResults, NodeConfig]:
#     """User tells the session code and you validate the session"""
    
#     # Use provided session_code or get from state
#     if session_code:
#         flow_manager.state["session_code"] = session_code
#     else:
#         session_code = flow_manager.state.get("session_code", "")
    
#     sessions = flow_manager.state.get("sessions", [])
#     total = len(sessions)
    
#     # Check if session code exists in sessions
#     session_exists = any(
#         session.get("join_code") == session_code or 
#         session.get("session_code") == session_code 
#         for session in sessions
#     )
    
#     result = SessionDataResults(sessions=sessions, total=total)

#     if total > 0 and session_exists:
#         logger.info("going to create ask question node")
#         logger.info(f"📚 Loading questions for session: {session_code}")
#         api_questions_data = await fetch_questions_from_api(session_code)
        
#         if api_questions_data:
#             flow_manager.state["quiz_questions"] = api_questions_data
#             flow_manager.state["total_questions"] = len(api_questions_data)
#             flow_manager.state["current_question"] = 0
#             flow_manager.state["score"] = 0
#             logger.info(f"✅ Loaded {len(api_questions_data)} questions")
            
            
#             # Go straight to question preparation
#             return result, create_ask_question_node()
#         else:
#             logger.warning("⚠️ No questions found for this session")
#             return result, create_no_questions_node()
#     else:
#         logger.info("going to create no questions node")
#         return result, create_no_questions_node()
    


# async def answer_question(
#     flow_manager: FlowManager, 
#     user_answer: str
# ) -> tuple[UserResponseResult, NodeConfig]:
#     """
#     Process user's answer to current question.
    
#     Args:
#         user_answer (str): User's answer (could be "A", "1", "Delhi", etc.)
#     """
#     current_idx = flow_manager.state.get("current_question", 0)
#     question_data = flow_manager.state.get("current_question_data", {})
#     questions = flow_manager.state.get("quiz_questions", [])
    
#     # Get correct answer
#     options = question_data.get("question_options", [])
#     correct_options = [opt for opt in options if opt.get("is_correct")]
#     correct_answer = correct_options[0].get("option_text", "") if correct_options else ""
    
#     # Simple answer checking (in production, you'd want more robust matching)
#     user_answer_clean = user_answer.strip().lower()
#     correct_answer_clean = correct_answer.strip().lower()
#     is_correct = user_answer_clean in correct_answer_clean or correct_answer_clean in user_answer_clean
    
#     # Update score
#     if is_correct:
#         flow_manager.state["score"] = flow_manager.state.get("score", 0) + 1
    
#     result = UserResponseResult(
#         question_index=current_idx,
#         user_answer=user_answer,
#         is_correct=is_correct,
#         correct_answer=correct_answer
#     )
    
#     # Move to next question or finish
#     if current_idx + 1 < len(questions):
#         flow_manager.state["current_question"] = current_idx + 1
#         return result, create_feedback_and_next_node()
#     else:
#         return result, create_quiz_complete_node()


# async def repeat_question(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
#     """
#     User wants to hear the question again.
#     """
#     return None, create_repeat_question_node()


# async def skip_question(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
#     """
#     User wants to skip current question.
#     """
#     current_idx = flow_manager.state.get("current_question", 0)
#     questions = flow_manager.state.get("quiz_questions", [])
    
#     if current_idx + 1 < len(questions):
#         flow_manager.state["current_question"] = current_idx + 1
#         return None, create_ask_question_node()
#     else:
#         return None, create_quiz_complete_node()


# async def end_quiz(flow_manager: FlowManager) -> tuple[QuizProgressResult, NodeConfig]:
#     """
#     User wants to end the quiz early.
#     """
#     total = flow_manager.state.get("total_questions", 0)
#     answered = flow_manager.state.get("current_question", 0) + 1
#     score = flow_manager.state.get("score", 0)
    
#     result = QuizProgressResult(
#         current_question=answered,
#         total_questions=total,
#         score=score
#     )
    
#     return result, create_quiz_complete_node()


# # ============================================================================
# # Node Creation Functions
# # ============================================================================

# def create_welcome_node() -> NodeConfig:
#     """Create welcome node with quiz invitation"""
#     return NodeConfig(
#         name="welcome",
#         role_messages=[
#             {
#                 "role": "system",
#                 "content": """You are a friendly quiz master. Your role is to engage users in a fun quiz session.
#                 Be enthusiastic, encouraging, and clear in your speech."""
#             }
#         ],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Welcome the user warmly to the quiz session. 
#                 You're first job is to get the session code from the user and validate the session.
#                 If the session is valid, then ask the user if they want to start the quiz.
#                 " """
#             }
#         ],
#         pre_actions=[
#             {
#                 "type": "function",
#                 "handler": load_session_data, #load_quiz_data
#             },
#         ],
#         functions=[start_quiz_session],
#     )



# # def create_ask_question_node() -> NodeConfig:
# #     """Create node to ask current question"""
# #     return NodeConfig(
# #         name="ask_question",
# #         task_messages=[
# #              {
# #                 "role": "system",
# #                 "content": """Always read the {flow_manager.state["current_question_instruction"]} from the database. the question is loaded using a pre set function"""
# #             }
# #         ],
# #         pre_actions=[
# #             {
# #                 "type": "function", 
# #                 "handler": prepare_and_set_question,
# #             },
# #         ],
# #         functions=[answer_question, repeat_question, skip_question, end_quiz],
# #     )

# def create_ask_question_node() -> NodeConfig:
#     """Create node to ask current question"""
#     return NodeConfig(
#         name="ask_question",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "You are asking the current question to the user. Wait for their answer."
#             }
#         ],
#         pre_actions=[
#             {
#                 "type": "function", 
#                 "handler": prepare_and_set_question,
#             },
#         ],
#         functions=[answer_question, repeat_question, skip_question, end_quiz],
#     )



# def create_repeat_question_node() -> NodeConfig:
#     """Create node to repeat the current question"""
#     return NodeConfig(
#         name="repeat_question",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Repeat the current question and options clearly.
#                 Say: "Let me repeat that. [Question text]. The options are: [list options]"
#                 Then wait for their answer."""
#             }
#         ],
#         functions=[answer_question, skip_question, end_quiz],
#     )


# def create_feedback_and_next_node() -> NodeConfig:
#     """Create node to give feedback and move to next question"""
#     return NodeConfig(
#         name="feedback_next",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Give brief feedback on their last answer.
#                 If correct: "That's right! [Brief explanation or encouragement]"
#                 If incorrect: "Actually, the correct answer is [correct answer]. [Brief explanation]"
                
#                 Then say: "Let's move to the next question." and proceed."""
#             }
#         ],
#         functions=[],  # Auto-proceeds after feedback
#         post_actions=[
#             {
#                 "type": "function",
#                 "handler": lambda a, fm: fm.transition_to(create_ask_question_node())
#             },
#         ],
#     )


# def create_quiz_complete_node() -> NodeConfig:
#     """Create node for quiz completion"""
#     return NodeConfig(
#         name="quiz_complete",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Thank them for completing the quiz!
#                 Share their score: "You got [score] out of [total] correct!"
#                 Give encouraging feedback based on score.
#                 Ask if they'd like to try another session or have any questions."""
#             }
#         ],
#         post_actions=[
#             {
#                 "type": "end_conversation",
#             },
#         ],
#     )


# def create_no_questions_node() -> NodeConfig:
#     """Create node when no questions are available"""
#     return NodeConfig(
#         name="no_questions",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Apologize that no questions are available at the moment.
#                 Suggest they try again later or contact support.
#                 Offer to answer any general knowledge questions you have in your database."""
#             }
#         ],
#         functions=[end_quiz],
#     )


# # ============================================================================
# # Global Functions (available in all nodes)
# # ============================================================================

# async def get_session_info(flow_manager: FlowManager) -> tuple[dict, None]:
#     """Get current session information"""
#     return {
#         "session_code": flow_manager.state.get("session_code", "H6TU"),
#         "total_questions": flow_manager.state.get("total_questions", 0),
#         "current_question": flow_manager.state.get("current_question", 0) + 1,
#         "score": flow_manager.state.get("score", 0)
#     }, None


# async def get_question_hint(flow_manager: FlowManager) -> tuple[str, None]:
#     """Provide a hint for current question"""
#     question_data = flow_manager.state.get("current_question_data", {})
#     # Could implement hint logic based on question type
#     return "Think about the main topic of the question", None


# # ============================================================================
# # Main Bot Function with Flow Manager
# # ============================================================================

# async def run_bot(websocket_client, session_code: str = "H6TU"):
#     """Run the quiz bot with flow management"""
#     print(f"🤖 Starting quiz bot for session: {session_code}")
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create LLM service
#     llm = GeminiLiveLLMService(
#     api_key=os.getenv("GOOGLE_API_KEY"),
#     config={
#         "system_instruction": "You are QuizMaster AI, an engaging quiz host. Be energetic, clear, and supportive. Speak naturally in a conversational tone."
#     }
# )

#     # Create conversation context
#     context = LLMContext()
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),          # Receive audio from WebSocket
#             context_aggregator.user(),     # Add user messages to context
#             rtvi,                          # RTVI monitoring
#             llm,                           # Gemini LLM with TTS
#             ws_transport.output(),         # Send audio back via WebSocket
#             context_aggregator.assistant(), # Add bot responses to context
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#             allow_interruptions=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Initialize flow manager
#     flow_manager = FlowManager(
#         task=task,
#         llm=llm,
#         context_aggregator=context_aggregator,
#         transport=ws_transport,
#         global_functions=[get_session_info, get_question_hint],
#     )
    
#     # Store session code in state
#     flow_manager.state["session_code"] = session_code

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Initialize the flow with welcome node
#         await flow_manager.initialize(create_welcome_node())

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise


# # ============================================================================
# # Helper function to format quiz data for LLM context
# # ============================================================================

# def create_quiz_system_prompt(questions_data: list) -> str:
#     """Create dynamic system prompt based on quiz questions"""
#     if not questions_data:
#         return """You are a quiz master. No questions are available at the moment. 
#         Apologize and offer to answer general knowledge questions."""
    
#     formatted_questions = "\n\n".join([
#         format_question_for_llm(q) for q in questions_data
#     ])
    
#     return f"""You are an interactive quiz master.

# QUESTIONS DATABASE:
# {formatted_questions}

# INSTRUCTIONS:
# 1. Ask ONE question at a time from the database
# 2. Clearly state question number and options
# 3. Accept answers as letters (A, B, C) or numbers (1, 2, 3)
# 4. Provide feedback after each answer
# 5. Keep responses conversational and encouraging"""


# # ============================================================================
# # Alternative: Simple version without FlowManager dependency
# # ============================================================================

# async def run_bot_simple(websocket_client, session_code: str = "H6TU"):
#     """Simpler version without FlowManager for quick implementation"""
#     print(f"🤖 Starting simple quiz bot for session: {session_code}")
    
#     # Fetch questions
#     questions_data = await fetch_questions_from_api(session_code)
#     system_prompt = create_quiz_system_prompt(questions_data)
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create LLM service with dynamic system prompt
#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         voice_id="Puck",
#         transcribe_model_audio=True,
#         system_instruction=system_prompt,
#     )

#     # Create conversation context
#     context = LLMContext(
#         [
#             {
#                 "role": "system",
#                 "content": system_prompt
#             },
#             {
#                 "role": "user",
#                 "content": "Greet the user warmly. Ask them if you can start asking them the quiz questions. Start with the first question from the database."
#             }
#         ],
#     )
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),          # Receive audio from WebSocket
#             context_aggregator.user(),     # Add user messages to context
#             rtvi,                          # RTVI monitoring
#             llm,                           # Gemini LLM with TTS
#             ws_transport.output(),         # Send audio back via WebSocket
#             context_aggregator.assistant(), # Add bot responses to context
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         await task.queue_frames([LLMRunFrame()])

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")
#         logger.info(f"📚 Loaded {len(questions_data)} questions")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise



# import os
# import aiohttp
# import json
# from typing import Optional
# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.frames.frames import LLMRunFrame, TextFrame
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# # Import FlowManager and related classes (assuming you have them or need to implement)
# from pipecat_flows import FlowManager, FlowResult, NodeConfig

# load_dotenv(override=True)

# # Node API configuration
# NODE_API_URL = "http://localhost:3000"


# # ============================================================================
# # Type Definitions
# # ============================================================================

# class QuizDataResult(FlowResult):
#     """Result from fetching quiz data"""
#     questions: list
#     session_code: str


# class UserResponseResult(FlowResult):
#     """Result from user's answer"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str


# class QuizProgressResult(FlowResult):
#     """Current quiz progress"""
#     current_question: int
#     total_questions: int
#     score: int

# class SessionDataResults(FlowResult):
#     """Result from fetching session data"""
#     sessions: list
#     total: int


# # ============================================================================
# # API Integration Functions
# # ============================================================================

# async def fetch_questions_from_api(session_code: str = "H6TU") -> list:
#     """Fetch questions from Node API endpoint"""
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f"{NODE_API_URL}/api/sessions/{session_code}/questions",
#                 timeout=aiohttp.ClientTimeout(total=5)
#             ) as response:
#                 if response.status == 200:
#                     data = await response.json()
                    
#                     # Check if response has expected format
#                     if data.get("status") == "ok" and "data" in data:
#                         questions_data = data["data"]
#                         logger.info(f"✅ Successfully fetched {len(questions_data)} questions from API")
#                         return questions_data
#                     else:
#                         logger.error(f"❌ Unexpected API response format: {data}")
#                         return []
#                 else:
#                     logger.error(f"❌ API returned status {response.status}")
#                     return []
#     except Exception as e:
#         logger.error(f"❌ Error fetching questions: {e}")
#         return []

# async def fetch_sessions_from_api() -> list:
#     """Fetch sessions from Node API endpoint"""
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f"{NODE_API_URL}/api/session/getSessions",
#                 timeout=aiohttp.ClientTimeout(total=5)
#             ) as response:
#                 if response.status == 200:
#                     data = await response.json()
                    
#                     # Updated: Check for "success" instead of "status"
#                     if data.get("success") and "data" in data:  # Changed "status" to "success"
#                         sessions_data = data["data"]
#                         logger.info(f"✅ Successfully fetched {len(sessions_data)} sessions from API")
#                         return sessions_data
#                     else:
#                         logger.error(f"❌ Unexpected API response format: {data}")
#                         return []
#                 else:
#                     logger.error(f"❌ API returned status {response.status}")
#                     return []
#     except Exception as e:
#         logger.error(f"❌ Error fetching sessions: {e}")
#         return []


# def format_question_for_llm(question_data: dict) -> str:
#     """Format a question from API into LLM-readable format"""
#     question_text = question_data.get("question_text", "Unknown question")
#     options = question_data.get("question_options", [])
    
#     # Find correct answer
#     correct_options = [opt for opt in options if opt.get("is_correct")]
#     correct_answer = correct_options[0].get("option_text", "Unknown") if correct_options else "Unknown"
    
#     # Format options
#     options_text = ""
#     for i, opt in enumerate(options, 1):
#         option_text = opt.get("option_text", f"Option {i}")
#         is_correct = opt.get("is_correct", False)
#         options_text += f"  {i}. {option_text}"
#         if is_correct:
#             options_text += " ✓"
#         options_text += "\n"
    
#     return f"""Question: {question_text}
# Options:
# {options_text}
# Answer: {correct_answer}"""


# # ============================================================================
# # Pre-action Handlers
# # ============================================================================

# # async def load_quiz_data(action: dict, flow_manager: FlowManager) -> None:
# #     """Load quiz questions from API before starting"""
# #     session_code = flow_manager.state.get("session_code", "H6TU")
# #     logger.info(f"📚 Loading quiz data for session: {session_code}")
    
# #     api_questions_data = await fetch_questions_from_api(session_code)
# #     flow_manager.state["quiz_questions"] = api_questions_data
# #     flow_manager.state["total_questions"] = len(api_questions_data)
# #     flow_manager.state["current_question"] = 0
# #     flow_manager.state["score"] = 0
    
# #     if not api_questions_data:
# #         logger.warning("⚠️ No questions loaded from API, using fallback")
# #         flow_manager.state["use_fallback"] = True
# #     else:
# #         logger.info(f"✅ Loaded {len(api_questions_data)} questions")

# async def load_questions_for_session(action: dict, flow_manager: FlowManager) -> None:
#     """Load questions for the current session from API"""
#     session_code = flow_manager.state.get("session_code", "")
    
#     if not session_code:
#         logger.error("❌ No session code found in state")
#         return
    
#     logger.info(f"📚 Loading questions for session: {session_code}")
    
#     api_questions_data = await fetch_questions_from_api(session_code)
#     flow_manager.state["quiz_questions"] = api_questions_data
#     flow_manager.state["total_questions"] = len(api_questions_data)
#     flow_manager.state["current_question"] = 0
#     flow_manager.state["score"] = 0
    
#     if not api_questions_data:
#         logger.warning("⚠️ No questions loaded from API")
#         flow_manager.state["use_fallback"] = True
#     else:
#         logger.info(f"✅ Loaded {len(api_questions_data)} questions")


# async def prepare_question(action: dict, flow_manager: FlowManager) -> None:
#     """Prepare current question for asking"""
#     questions = flow_manager.state.get("quiz_questions", [])
#     current_idx = flow_manager.state.get("current_question", 0)
    
#     if current_idx < len(questions):
#         question_data = questions[current_idx]
#         flow_manager.state["current_question_data"] = question_data
#         formatted_question = format_question_for_llm(question_data)
        
#         logger.info(f"📝 Preparing question {current_idx + 1}: {question_data.get('question_text', 'Unknown')[:50]}...")
#     else:
#         flow_manager.state["current_question_data"] = None

# async def load_session_data(action: dict, flow_manager: FlowManager) -> None:
#     """Load all available sessions from the node API"""
#     api_sessions_data = await fetch_sessions_from_api()
#     flow_manager.state["sessions"] = api_sessions_data
#     flow_manager.state["total_sessions"] = len(api_sessions_data)

#     if not api_sessions_data:
#         logger.warning("⚠️ No sessions loaded from API, using fallback")
#         flow_manager.state["use_fallback"] = True
#     else:
#         logger.info(f"✅ Loaded {len(api_sessions_data)} sessions")


# # ============================================================================
# # Direct Functions for Flow Nodes
# # ============================================================================

# # async def start_quiz_session(flow_manager: FlowManager) -> tuple[QuizDataResult, NodeConfig]:
# #     """
# #     User wants to start a quiz session.
# #     """
# #     # Quiz data already loaded in pre-action
# #     questions = flow_manager.state.get("quiz_questions", [])
# #     total = len(questions)
    
# #     result = QuizDataResult(questions=questions, session_code=flow_manager.state.get("session_code", "H6TU"))
    
# #     if total > 0:
# #         return result, create_ask_question_node()
# #     else:
# #         return result, create_no_questions_node()

# # async def start_quiz_session(flow_manager : FlowManager) -> tuple[SessionDataResults, NodeConfig]:
# #     """User tells the session code and you validate the session"""

# #     sessions = flow_manager.state.get("sessions",[])
# #     total = len(sessions)
# #     result = SessionDataResults(sessions=sessions, total=total)

# #     if total > 0:
# #         if flow_manager.state.get("session_code", "") in sessions:
# #             return result, create_ask_question_node()
# #         else:
# #             return result, create_no_questions_node()
# #     else:
# #         return result, create_no_questions_node()

# async def prepare_and_set_question(action: dict, flow_manager: FlowManager) -> None:
#     questions = flow_manager.state.get("quiz_questions", [])
#     current_idx = flow_manager.state.get("current_question", 0)

#     if current_idx < len(questions):
#         question_data = questions[current_idx]
#         formatted_question = format_question_for_llm(question_data)

#         question_part = formatted_question.split("Answer:")[0].strip()
#         total = len(questions)

#         spoken_question = f"""
#         Question {current_idx + 1} of {total}.
#         {question_part}

#         Read the question and options clearly.
#         Then wait silently for the user's answer.
#         """

#         # 🔥 THIS is the key line
#         flow_manager.state["current_question_prompt"] = spoken_question

#         flow_manager.state["current_question_data"] = question_data


# async def start_quiz_session(
#     flow_manager: FlowManager, 
#     session_code: Optional[str] = None
# ) -> tuple[SessionDataResults, NodeConfig]:
#     """User tells the session code and you validate the session"""
    
#     # Use provided session_code or get from state
#     if session_code:
#         flow_manager.state["session_code"] = session_code
#     else:
#         session_code = flow_manager.state.get("session_code", "")
    
#     sessions = flow_manager.state.get("sessions", [])
#     total = len(sessions)
    
#     # Check if session code exists in sessions
#     session_exists = any(
#         session.get("join_code") == session_code or 
#         session.get("session_code") == session_code 
#         for session in sessions
#     )
    
#     result = SessionDataResults(sessions=sessions, total=total)

#     if total > 0 and session_exists:
#         logger.info("going to create ask question node")
#         logger.info(f"📚 Loading questions for session: {session_code}")
#         api_questions_data = await fetch_questions_from_api(session_code)
        
#         if api_questions_data:
#             flow_manager.state["quiz_questions"] = api_questions_data
#             flow_manager.state["total_questions"] = len(api_questions_data)
#             flow_manager.state["current_question"] = 0
#             flow_manager.state["score"] = 0
#             logger.info(f"✅ Loaded {len(api_questions_data)} questions")
            
            
#             # Go straight to question preparation
#             return result, create_ask_question_node()
#         else:
#             logger.warning("⚠️ No questions found for this session")
#             return result, create_no_questions_node()
#     else:
#         logger.info("going to create no questions node")
#         return result, create_no_questions_node()
    


# async def answer_question(
#     flow_manager: FlowManager, 
#     user_answer: str
# ) -> tuple[UserResponseResult, NodeConfig]:
#     """
#     Process user's answer to current question.
    
#     Args:
#         user_answer (str): User's answer (could be "A", "1", "Delhi", etc.)
#     """
#     current_idx = flow_manager.state.get("current_question", 0)
#     question_data = flow_manager.state.get("current_question_data", {})
#     questions = flow_manager.state.get("quiz_questions", [])
    
#     # Get correct answer
#     options = question_data.get("question_options", [])
#     correct_options = [opt for opt in options if opt.get("is_correct")]
#     correct_answer = correct_options[0].get("option_text", "") if correct_options else ""
    
#     # Simple answer checking (in production, you'd want more robust matching)
#     user_answer_clean = user_answer.strip().lower()
#     correct_answer_clean = correct_answer.strip().lower()
#     is_correct = user_answer_clean in correct_answer_clean or correct_answer_clean in user_answer_clean
    
#     # Update score
#     if is_correct:
#         flow_manager.state["score"] = flow_manager.state.get("score", 0) + 1
    
#     result = UserResponseResult(
#         question_index=current_idx,
#         user_answer=user_answer,
#         is_correct=is_correct,
#         correct_answer=correct_answer
#     )
    
#     # Move to next question or finish
#     if current_idx + 1 < len(questions):
#         flow_manager.state["current_question"] = current_idx + 1
#         return result, create_feedback_and_next_node()
#     else:
#         return result, create_quiz_complete_node()


# async def repeat_question(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
#     """
#     User wants to hear the question again.
#     """
#     return None, create_repeat_question_node()


# async def skip_question(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
#     """
#     User wants to skip current question.
#     """
#     current_idx = flow_manager.state.get("current_question", 0)
#     questions = flow_manager.state.get("quiz_questions", [])
    
#     if current_idx + 1 < len(questions):
#         flow_manager.state["current_question"] = current_idx + 1
#         return None, create_ask_question_node()
#     else:
#         return None, create_quiz_complete_node()


# async def end_quiz(flow_manager: FlowManager) -> tuple[QuizProgressResult, NodeConfig]:
#     """
#     User wants to end the quiz early.
#     """
#     total = flow_manager.state.get("total_questions", 0)
#     answered = flow_manager.state.get("current_question", 0) + 1
#     score = flow_manager.state.get("score", 0)
    
#     result = QuizProgressResult(
#         current_question=answered,
#         total_questions=total,
#         score=score
#     )
    
#     return result, create_quiz_complete_node()


# # ============================================================================
# # Node Creation Functions
# # ============================================================================

# def create_welcome_node() -> NodeConfig:
#     """Create welcome node with quiz invitation"""
#     return NodeConfig(
#         name="welcome",
#         role_messages=[
#             {
#                 "role": "system",
#                 "content": """You are a friendly quiz master. Your role is to engage users in a fun quiz session.
#                 Be enthusiastic, encouraging, and clear in your speech."""
#             }
#         ],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Welcome the user warmly to the quiz session. 
#                 You're first job is to get the session code from the user and validate the session.
#                 If the session is valid, then ask the user if they want to start the quiz.
#                 " """
#             }
#         ],
#         pre_actions=[
#             {
#                 "type": "function",
#                 "handler": load_session_data, #load_quiz_data
#             },
#         ],
#         functions=[start_quiz_session],
#     )



# # def create_ask_question_node() -> NodeConfig:
# #     """Create node to ask current question"""
# #     return NodeConfig(
# #         name="ask_question",
# #         task_messages=[
# #              {
# #                 "role": "system",
# #                 "content": """Always read the  from the database. the question is loaded using a pre set function"""
# #             }
# #         ],
# #         pre_actions=[
# #             {
# #                 "type": "function", 
# #                 "handler": prepare_and_set_question,
# #             },
# #         ],
# #         functions=[answer_question, repeat_question, skip_question, end_quiz],
# #     )

# def create_ask_question_node() -> NodeConfig:
#     return NodeConfig(
#         name="ask_question",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "{current_question_prompt}"
#             }
#         ],
#         pre_actions=[
#             {
#                 "type": "function",
#                 "handler": prepare_and_set_question,
#             }
#         ],
#         functions=[answer_question, repeat_question, skip_question, end_quiz],
#     )



# def create_repeat_question_node() -> NodeConfig:
#     """Create node to repeat the current question"""
#     return NodeConfig(
#         name="repeat_question",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Repeat the current question and options clearly.
#                 Say: "Let me repeat that. [Question text]. The options are: [list options]"
#                 Then wait for their answer."""
#             }
#         ],
#         functions=[answer_question, skip_question, end_quiz],
#     )


# def create_feedback_and_next_node() -> NodeConfig:
#     """Create node to give feedback and move to next question"""
#     return NodeConfig(
#         name="feedback_next",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Give brief feedback on their last answer.
#                 If correct: "That's right! [Brief explanation or encouragement]"
#                 If incorrect: "Actually, the correct answer is [correct answer]. [Brief explanation]"
                
#                 Then say: "Let's move to the next question." and proceed."""
#             }
#         ],
#         functions=[],  # Auto-proceeds after feedback
#         post_actions=[
#             {
#                 "type": "function",
#                 "handler": lambda a, fm: fm.transition_to(create_ask_question_node())
#             },
#         ],
#     )


# def create_quiz_complete_node() -> NodeConfig:
#     """Create node for quiz completion"""
#     return NodeConfig(
#         name="quiz_complete",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Thank them for completing the quiz!
#                 Share their score: "You got [score] out of [total] correct!"
#                 Give encouraging feedback based on score.
#                 Ask if they'd like to try another session or have any questions."""
#             }
#         ],
#         post_actions=[
#             {
#                 "type": "end_conversation",
#             },
#         ],
#     )


# def create_no_questions_node() -> NodeConfig:
#     """Create node when no questions are available"""
#     return NodeConfig(
#         name="no_questions",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Apologize that no questions are available at the moment.
#                 Suggest they try again later or contact support.
#                 Offer to answer any general knowledge questions you have in your database."""
#             }
#         ],
#         functions=[end_quiz],
#     )


# # ============================================================================
# # Global Functions (available in all nodes)
# # ============================================================================

# async def get_session_info(flow_manager: FlowManager) -> tuple[dict, None]:
#     """Get current session information"""
#     return {
#         "session_code": flow_manager.state.get("session_code", "H6TU"),
#         "total_questions": flow_manager.state.get("total_questions", 0),
#         "current_question": flow_manager.state.get("current_question", 0) + 1,
#         "score": flow_manager.state.get("score", 0)
#     }, None


# async def get_question_hint(flow_manager: FlowManager) -> tuple[str, None]:
#     """Provide a hint for current question"""
#     question_data = flow_manager.state.get("current_question_data", {})
#     # Could implement hint logic based on question type
#     return "Think about the main topic of the question", None


# # ============================================================================
# # Main Bot Function with Flow Manager
# # ============================================================================

# async def run_bot(websocket_client, session_code: str = "H6TU"):
#     """Run the quiz bot with flow management"""
#     print(f"🤖 Starting quiz bot for session: {session_code}")
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create LLM service
#     llm = GeminiLiveLLMService(
#     api_key=os.getenv("GOOGLE_API_KEY"),
#     config={
#         "system_instruction": "You are QuizMaster AI, an engaging quiz host. Be energetic, clear, and supportive. Speak naturally in a conversational tone."
#     }
# )

#     # Create conversation context
#     context = LLMContext()
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),          # Receive audio from WebSocket
#             context_aggregator.user(),     # Add user messages to context
#             rtvi,                          # RTVI monitoring
#             llm,                           # Gemini LLM with TTS
#             ws_transport.output(),         # Send audio back via WebSocket
#             context_aggregator.assistant(), # Add bot responses to context
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#             allow_interruptions=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Initialize flow manager
#     flow_manager = FlowManager(
#         task=task,
#         llm=llm,
#         context_aggregator=context_aggregator,
#         transport=ws_transport,
#         global_functions=[get_session_info, get_question_hint],
#     )
    
#     # Store session code in state
#     flow_manager.state["session_code"] = session_code

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Initialize the flow with welcome node
#         await flow_manager.initialize(create_welcome_node())

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise


# # ============================================================================
# # Helper function to format quiz data for LLM context
# # ============================================================================

# def create_quiz_system_prompt(questions_data: list) -> str:
#     """Create dynamic system prompt based on quiz questions"""
#     if not questions_data:
#         return """You are a quiz master. No questions are available at the moment. 
#         Apologize and offer to answer general knowledge questions."""
    
#     formatted_questions = "\n\n".join([
#         format_question_for_llm(q) for q in questions_data
#     ])
    
#     return f"""You are an interactive quiz master.

# QUESTIONS DATABASE:
# {formatted_questions}

# INSTRUCTIONS:
# 1. Ask ONE question at a time from the database
# 2. Clearly state question number and options
# 3. Accept answers as letters (A, B, C) or numbers (1, 2, 3)
# 4. Provide feedback after each answer
# 5. Keep responses conversational and encouraging"""


# # ============================================================================
# # Alternative: Simple version without FlowManager dependency
# # ============================================================================

# async def run_bot_simple(websocket_client, session_code: str = "H6TU"):
#     """Simpler version without FlowManager for quick implementation"""
#     print(f"🤖 Starting simple quiz bot for session: {session_code}")
    
#     # Fetch questions
#     questions_data = await fetch_questions_from_api(session_code)
#     system_prompt = create_quiz_system_prompt(questions_data)
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create LLM service with dynamic system prompt
#     # llm = GeminiLiveLLMService(
#     #     api_key=os.getenv("GOOGLE_API_KEY"),
#     #     voice_id="Puck",
#     #     transcribe_model_audio=True,
#     #     system_instruction=system_prompt,
#     # )
#     llm = GeminiLiveLLMService(
#     api_key=os.getenv("GOOGLE_API_KEY"),
#     model="models/gemini-2.0-flash-live-preview",
# )


#     # Create conversation context
#     context = LLMContext([
#     {
#         "role": "system",
#         "content": "You are QuizMaster AI, an engaging quiz host. Speak clearly and energetically."
#     }
# ])

#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),          # Receive audio from WebSocket
#             context_aggregator.user(),     # Add user messages to context
#             rtvi,                          # RTVI monitoring
#             llm,                           # Gemini LLM with TTS
#             ws_transport.output(),         # Send audio back via WebSocket
#             context_aggregator.assistant(), # Add bot responses to context
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         await task.queue_frames([LLMRunFrame()])

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")
#         logger.info(f"📚 Loaded {len(questions_data)} questions")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise



# import os
# import aiohttp
# import json
# from typing import Optional, Dict, Any
# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.frames.frames import LLMRunFrame, TextFrame
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# # Import FlowManager and related classes
# from pipecat_flows import FlowManager, FlowResult, NodeConfig, FlowsFunctionSchema, FlowArgs

# load_dotenv(override=True)

# # Node API configuration
# NODE_API_URL = "http://localhost:3000"


# # ============================================================================
# # Type Definitions
# # ============================================================================

# class SessionDataResults(FlowResult):
#     """Result from fetching session data"""
#     sessions: list
#     total: int


# class UserResponseResult(FlowResult):
#     """Result from user's answer"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str


# class QuizProgressResult(FlowResult):
#     """Current quiz progress"""
#     current_question: int
#     total_questions: int
#     score: int


# # ============================================================================
# # API Integration Functions
# # ============================================================================

# async def fetch_questions_from_api(session_code: str = "H6TU") -> list:
#     """Fetch questions from Node API endpoint"""
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f"{NODE_API_URL}/api/sessions/{session_code}/questions",
#                 timeout=aiohttp.ClientTimeout(total=5)
#             ) as response:
#                 if response.status == 200:
#                     data = await response.json()
                    
#                     # Check if response has expected format
#                     if data.get("status") == "ok" and "data" in data:
#                         questions_data = data["data"]
#                         logger.info(f"✅ Successfully fetched {len(questions_data)} questions from API")
#                         return questions_data
#                     else:
#                         logger.error(f"❌ Unexpected API response format: {data}")
#                         return []
#                 else:
#                     logger.error(f"❌ API returned status {response.status}")
#                     return []
#     except Exception as e:
#         logger.error(f"❌ Error fetching questions: {e}")
#         return []


# async def fetch_sessions_from_api() -> list:
#     """Fetch sessions from Node API endpoint"""
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f"{NODE_API_URL}/api/session/getSessions",
#                 timeout=aiohttp.ClientTimeout(total=5)
#             ) as response:
#                 if response.status == 200:
#                     data = await response.json()
                    
#                     # Updated: Check for "success" instead of "status"
#                     if data.get("success") and "data" in data:  # Changed "status" to "success"
#                         sessions_data = data["data"]
#                         logger.info(f"✅ Successfully fetched {len(sessions_data)} sessions from API")
#                         return sessions_data
#                     else:
#                         logger.error(f"❌ Unexpected API response format: {data}")
#                         return []
#                 else:
#                     logger.error(f"❌ API returned status {response.status}")
#                     return []
#     except Exception as e:
#         logger.error(f"❌ Error fetching sessions: {e}")
#         return []


# def format_question_for_llm(question_data: dict) -> str:
#     """Format a question from API into LLM-readable format"""
#     question_text = question_data.get("question_text", "Unknown question")
#     options = question_data.get("question_options", [])
    
#     # Find correct answer
#     correct_options = [opt for opt in options if opt.get("is_correct")]
#     correct_answer = correct_options[0].get("option_text", "Unknown") if correct_options else "Unknown"
    
#     # Format options with letters
#     options_text = ""
#     letters = ["A", "B", "C", "D"]
#     for i, opt in enumerate(options[:4]):  # Limit to first 4 options
#         option_text = opt.get("option_text", f"Option {letters[i]}")
#         options_text += f"{letters[i]}. {option_text}\n"
    
#     return f"""QUESTION: {question_text}

# OPTIONS:
# {options_text}
# CORRECT ANSWER: {correct_answer}"""


# def create_question_context(question_data: dict, current_index: int, total_questions: int) -> str:
#     """Create context for the current question"""
#     question_text = question_data.get("question_text", "")
#     options = question_data.get("question_options", [])
    
#     # Format options with letters
#     formatted_options = []
#     letters = ["A", "B", "C", "D"]
#     for i, opt in enumerate(options[:4]):  # Limit to first 4 options
#         option_text = opt.get("option_text", f"Option {letters[i]}")
#         formatted_options.append(f"{letters[i]}. {option_text}")
    
#     return f"""You are currently on question {current_index + 1} of {total_questions}.

# CURRENT QUESTION: {question_text}

# OPTIONS:
# {chr(10).join(formatted_options)}

# Please read this question clearly and wait for the user's answer. 
# Accept answers in any format (letter, number, or full text)."""


# # ============================================================================
# # Pre-action Handlers
# # ============================================================================

# async def load_session_data(action: dict, flow_manager: FlowManager) -> None:
#     """Load all available sessions from the node API"""
#     api_sessions_data = await fetch_sessions_from_api()
#     flow_manager.state["sessions"] = api_sessions_data
#     flow_manager.state["total_sessions"] = len(api_sessions_data)

#     if not api_sessions_data:
#         logger.warning("⚠️ No sessions loaded from API")
#         flow_manager.state["use_fallback"] = True
#     else:
#         logger.info(f"✅ Loaded {len(api_sessions_data)} sessions")


# async def prepare_and_set_question(action: dict, flow_manager: FlowManager) -> None:
#     """Prepare current question and set it in the state"""
#     questions = flow_manager.state.get("quiz_questions", [])
#     current_idx = flow_manager.state.get("current_question", 0)
    
#     if current_idx < len(questions):
#         question_data = questions[current_idx]
#         total_questions = len(questions)
        
#         # Create the question context for the LLM
#         question_context = create_question_context(question_data, current_idx, total_questions)
        
#         # Store in state for the LLM to use
#         flow_manager.state["current_question_context"] = question_context
#         flow_manager.state["current_question_data"] = question_data
        
#         logger.info(f"📝 Prepared question {current_idx + 1}/{total_questions}")
#     else:
#         logger.warning(f"No question found at index {current_idx}")
#         flow_manager.state["current_question_context"] = ""
#         flow_manager.state["current_question_data"] = None


# # ============================================================================
# # Direct Functions for Flow Nodes
# # ============================================================================

# async def start_quiz_session(
#     args: FlowArgs, 
#     flow_manager: FlowManager
# ) -> tuple[SessionDataResults, NodeConfig]:
#     """User provides session code and we validate it"""
#     # Get session code from arguments
#     session_code = args.get("session_code", "").strip().upper()
    
#     if not session_code:
#         # Try to get from user message
#         session_code = flow_manager.state.get("session_code", "")
    
#     logger.info(f"📋 Validating session code: {session_code}")
    
#     # Fetch sessions to validate
#     sessions = flow_manager.state.get("sessions", [])
#     session_exists = False
    
#     for session in sessions:
#         if (session.get("join_code") == session_code or 
#             session.get("session_code") == session_code):
#             session_exists = True
#             break
    
#     if not session_exists:
#         logger.warning(f"❌ Invalid session code: {session_code}")
#         return SessionDataResults(sessions=[], total=0), create_invalid_session_node()
    
#     # Store session code
#     flow_manager.state["session_code"] = session_code
    
#     # Fetch questions for this session
#     logger.info(f"📚 Loading questions for session: {session_code}")
#     api_questions_data = await fetch_questions_from_api(session_code)
    
#     if api_questions_data:
#         flow_manager.state["quiz_questions"] = api_questions_data
#         flow_manager.state["total_questions"] = len(api_questions_data)
#         flow_manager.state["current_question"] = 0
#         flow_manager.state["score"] = 0
#         logger.info(f"✅ Loaded {len(api_questions_data)} questions")
        
#         # Go to ask question node
#         return SessionDataResults(sessions=sessions, total=len(sessions)), create_ask_question_node()
#     else:
#         logger.warning("⚠️ No questions found for this session")
#         return SessionDataResults(sessions=sessions, total=len(sessions)), create_no_questions_node()


# async def answer_question(
#     args: FlowArgs, 
#     flow_manager: FlowManager
# ) -> tuple[UserResponseResult, NodeConfig]:
#     """Process user's answer to current question"""
#     user_answer = args.get("answer", "").strip()
#     current_idx = flow_manager.state.get("current_question", 0)
#     question_data = flow_manager.state.get("current_question_data", {})
#     questions = flow_manager.state.get("quiz_questions", [])
    
#     logger.info(f"📝 Processing answer for question {current_idx + 1}: {user_answer}")
    
#     if not question_data:
#         logger.error("No current question data found")
#         return UserResponseResult(
#             question_index=current_idx,
#             user_answer=user_answer,
#             is_correct=False,
#             correct_answer=""
#         ), create_ask_question_node()
    
#     # Get correct answer from question data
#     options = question_data.get("question_options", [])
#     correct_options = [opt for opt in options if opt.get("is_correct")]
#     correct_answer_text = correct_options[0].get("option_text", "") if correct_options else ""
    
#     # Simple answer checking
#     user_answer_lower = user_answer.lower()
#     correct_answer_lower = correct_answer_text.lower()
    
#     # Map letter answers to option text
#     letters = ["A", "B", "C", "D"]
#     letter_to_option = {}
#     for i, opt in enumerate(options[:4]):
#         if i < len(letters):
#             letter_to_option[letters[i].lower()] = opt.get("option_text", "").lower()
    
#     # Check if answer matches correct option
#     is_correct = False
#     if user_answer_lower in letter_to_option:
#         # User answered with letter
#         is_correct = letter_to_option[user_answer_lower] == correct_answer_lower
#     elif user_answer_lower == str(current_idx + 1).lower():
#         # User answered with question number (not supported for correctness)
#         is_correct = False
#     else:
#         # User answered with text
#         is_correct = (user_answer_lower in correct_answer_lower or 
#                      correct_answer_lower in user_answer_lower)
    
#     # Update score
#     if is_correct:
#         flow_manager.state["score"] = flow_manager.state.get("score", 0) + 1
#         logger.info(f"✅ Correct! Score: {flow_manager.state['score']}")
#     else:
#         logger.info(f"❌ Incorrect. Correct answer: {correct_answer_text}")
    
#     result = UserResponseResult(
#         question_index=current_idx,
#         user_answer=user_answer,
#         is_correct=is_correct,
#         correct_answer=correct_answer_text
#     )
    
#     # Move to next question or finish
#     if current_idx + 1 < len(questions):
#         flow_manager.state["current_question"] = current_idx + 1
#         return result, create_feedback_and_next_node()
#     else:
#         return result, create_quiz_complete_node()


# async def repeat_question(args: FlowArgs, flow_manager: FlowManager) -> tuple[None, NodeConfig]:
#     """User wants to hear the question again"""
#     return None, create_ask_question_node()


# async def skip_question(args: FlowArgs, flow_manager: FlowManager) -> tuple[None, NodeConfig]:
#     """User wants to skip current question"""
#     current_idx = flow_manager.state.get("current_question", 0)
#     questions = flow_manager.state.get("quiz_questions", [])
    
#     if current_idx + 1 < len(questions):
#         flow_manager.state["current_question"] = current_idx + 1
#         return None, create_ask_question_node()
#     else:
#         return None, create_quiz_complete_node()


# async def end_quiz(args: FlowArgs, flow_manager: FlowManager) -> tuple[QuizProgressResult, NodeConfig]:
#     """User wants to end the quiz early"""
#     total = flow_manager.state.get("total_questions", 0)
#     answered = flow_manager.state.get("current_question", 0) + 1
#     score = flow_manager.state.get("score", 0)
    
#     result = QuizProgressResult(
#         current_question=answered,
#         total_questions=total,
#         score=score
#     )
    

#     return result, create_quiz_complete_node()

# async def load_quiz_data(action: dict, flow_manager: FlowManager) -> None:
#     """Load quiz questions from API before starting"""
#     session_code = flow_manager.state.get("session_code", "H6TU")
#     logger.info(f"📚 Loading quiz data for session: {session_code}")
    
#     api_questions_data = await fetch_questions_from_api(session_code)
#     flow_manager.state["quiz_questions"] = api_questions_data
#     flow_manager.state["total_questions"] = len(api_questions_data)
#     flow_manager.state["current_question"] = 0
#     flow_manager.state["score"] = 0
    
#     if not api_questions_data:
#         logger.warning("⚠️ No questions loaded from API, using fallback")
#         flow_manager.state["use_fallback"] = True
#     else:
#         logger.info(f"✅ Loaded {len(api_questions_data)} questions")


# # ============================================================================
# # Global Functions (must have 'flow_manager' as first parameter)
# # ============================================================================

# async def get_session_info(flow_manager: FlowManager) -> tuple[dict, None]:
#     """Get current session information - Direct function"""
#     return {
#         "session_code": flow_manager.state.get("session_code", ""),
#         "total_questions": flow_manager.state.get("total_questions", 0),
#         "current_question": flow_manager.state.get("current_question", 0) + 1,
#         "score": flow_manager.state.get("score", 0)
#     }, None


# async def get_question_hint(flow_manager: FlowManager) -> tuple[str, None]:
#     """Provide a hint for current question - Direct function"""
#     question_data = flow_manager.state.get("current_question_data", {})
#     question_text = question_data.get("question_text", "")
    
#     # Simple hint based on question length
#     if len(question_text) > 50:
#         return "This is a detailed question. Focus on the key terms mentioned.", None
#     else:
#         return "Think carefully about all the options before answering.", None


# # ============================================================================
# # Node Creation Functions
# # ============================================================================

# def create_welcome_node() -> NodeConfig:
#     """Create welcome node with quiz invitation"""
#     start_quiz_func = FlowsFunctionSchema(
#         name="start_quiz_session",
#         handler=start_quiz_session,
#         description="Start the quiz session with the provided session code",
#         properties={
#             "session_code": {
#                 "type": "string",
#                 "description": "The session code provided by the user"
#             }
#         },
#         required=["session_code"],
#     )
    
#     return NodeConfig(
#         name="welcome",
#         role_messages=[
#             {
#                 "role": "system",
#                 "content": """You are a friendly quiz master. Your role is to engage users in a fun quiz session.
#                 Be enthusiastic, encouraging, and clear in your speech."""
#             }
#         ],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Welcome the user warmly to the quiz session. 
#                 Ask the user for their session code. 
#                 Once they provide it, use the start_quiz_session function to validate and begin."""
#             }
#         ],
#         pre_actions=[
#             {
#                 "type": "function",
#                 "handler": load_session_data,
#             },
#         ],
#         functions=[start_quiz_func],
#     )


# def create_ask_question_node() -> NodeConfig:
#     """Create node to ask current question"""
#     answer_question_func = FlowsFunctionSchema(
#         name="answer_question",
#         handler=answer_question,
#         description="Process the user's answer to the current question",
#         properties={
#             "answer": {
#                 "type": "string",
#                 "description": "The user's answer (can be letter like 'A', 'B', 'C', 'D' or the full text)"
#             }
#         },
#         required=["answer"],
#     )
    
#     repeat_question_func = FlowsFunctionSchema(
#         name="repeat_question",
#         handler=repeat_question,
#         description="Repeat the current question",
#         properties={},
#         required=[],
#     )
    
#     skip_question_func = FlowsFunctionSchema(
#         name="skip_question",
#         handler=skip_question,
#         description="Skip the current question",
#         properties={},
#         required=[],
#     )
    
#     end_quiz_func = FlowsFunctionSchema(
#         name="end_quiz",
#         handler=end_quiz,
#         description="End the quiz session",
#         properties={},
#         required=[],
#     )
    
#     return NodeConfig(
#         name="ask_question",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "{current_question_context}"
#             }
#         ],
#         pre_actions=[
#             {
#                 "type": "function",
#                 "handler": load_quiz_data,
#             }
#         ],
#         functions=[answer_question_func, repeat_question_func, skip_question_func, end_quiz_func],
#     )


# def create_feedback_and_next_node() -> NodeConfig:
#     """Create node to give feedback and move to next question"""
#     return NodeConfig(
#         name="feedback_next",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Give brief feedback on their last answer.
#                 If correct: "That's right! [Brief encouragement]"
#                 If incorrect: "Actually, the correct answer was [correct answer]. [Brief explanation if available]"
                
#                 Then say: "Let's move to the next question." and proceed."""
#             }
#         ],
#         functions=[],
#         post_actions=[
#             {
#                 "type": "transition",
#                 "target": "ask_question"
#             },
#         ],
#     )


# def create_quiz_complete_node() -> NodeConfig:
#     """Create node for quiz completion"""
#     return NodeConfig(
#         name="quiz_complete",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Thank them for completing the quiz!
#                 Share their score: "You got {score} out of {total_questions} correct!"
#                 Give encouraging feedback based on their score.
#                 Ask if they'd like to try another session."""
#             }
#         ],
#         post_actions=[
#             {
#                 "type": "end_conversation",
#             },
#         ],
#     )


# def create_invalid_session_node() -> NodeConfig:
#     """Create node for invalid session code"""
#     start_quiz_func = FlowsFunctionSchema(
#         name="start_quiz_session",
#         handler=start_quiz_session,
#         description="Try again with a different session code",
#         properties={
#             "session_code": {
#                 "type": "string",
#                 "description": "The session code provided by the user"
#             }
#         },
#         required=["session_code"],
#     )
    
#     return NodeConfig(
#         name="invalid_session",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """The session code you provided is invalid. 
#                 Please check the code and try again, or ask for help."""
#             }
#         ],
#         functions=[start_quiz_func],
#     )


# def create_no_questions_node() -> NodeConfig:
#     """Create node when no questions are available"""
#     return NodeConfig(
#         name="no_questions",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """I'm sorry, but there are no questions available for this session at the moment.
#                 Please try a different session code or contact the quiz administrator."""
#             }
#         ],
#         post_actions=[
#             {
#                 "type": "end_conversation",
#             },
#         ],
#     )


# # ============================================================================
# # Main Bot Function
# # ============================================================================

# async def run_bot(websocket_client, session_code: Optional[str] = None):
#     """Run the quiz bot with flow management"""
#     logger.info(f"🤖 Starting quiz bot")
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create LLM service
#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         config={
#             "system_instruction": "You are QuizMaster AI, an engaging quiz host. Be energetic, clear, and supportive. Speak naturally in a conversational tone. Always speak out the questions and options clearly."
#         }
#     )

#     # Create conversation context
#     context = LLMContext()
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),          # Receive audio from WebSocket
#             context_aggregator.user(),     # Add user messages to context
#             rtvi,                          # RTVI monitoring
#             llm,                           # Gemini LLM with TTS
#             ws_transport.output(),         # Send audio back via WebSocket
#             context_aggregator.assistant(), # Add bot responses to context
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#             allow_interruptions=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Initialize flow manager - REMOVED global_functions since they were causing issues
#     flow_manager = FlowManager(
#         task=task,
#         llm=llm,
#         context_aggregator=context_aggregator,
#         transport=ws_transport,
#         # Removed: global_functions=[get_session_info, get_question_hint],
#     )
    
#     # Store initial session code if provided
#     if session_code:
#         flow_manager.state["session_code"] = session_code

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Initialize the flow with welcome node
#         await flow_manager.initialize(create_welcome_node())

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise


# # ============================================================================
# # Alternative: Simple version without FlowManager
# # ============================================================================

# async def run_bot_simple(websocket_client, session_code: str = "H6TU"):
#     """Simpler version without FlowManager - easier to debug"""
#     logger.info(f"🤖 Starting simple quiz bot for session: {session_code}")
    
#     # Fetch questions
#     questions_data = await fetch_questions_from_api(session_code)
    
#     if not questions_data:
#         logger.error("❌ No questions found for this session")
#         # Create a simple error message
#         error_context = LLMContext([
#             {
#                 "role": "system",
#                 "content": "You are a quiz assistant. Tell the user that no questions were found for their session code and ask them to try a different code."
#             }
#         ])
#     else:
#         # Create comprehensive system prompt with all questions
#         formatted_questions = "\n\n".join([format_question_for_llm(q) for q in questions_data])
        
#         system_prompt = f"""You are QuizMaster AI, an engaging quiz host. 
#         You will ask questions one by one from the following list. Start with the first question.

#         QUESTIONS:
#         {formatted_questions}

#         INSTRUCTIONS:
#         1. Start with: "Welcome to the quiz! Let's begin with question 1."
#         2. Read each question clearly with all options (A, B, C, D)
#         3. After reading, say: "What's your answer?"
#         4. Wait for their response
#         5. After each answer, say if it's correct or incorrect
#         6. If incorrect, provide the correct answer
#         7. Move to the next question
#         8. At the end, share their final score
        
#         Speak naturally and energetically!"""
        
#         error_context = LLMContext([
#             {
#                 "role": "system", 
#                 "content": system_prompt
#             },
#             {
#                 "role": "user",
#                 "content": "Let's start the quiz!"
#             }
#         ])
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create LLM service
#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         config={
#             "system_instruction": "You are QuizMaster AI, an engaging quiz host. Be energetic, clear, and supportive."
#         }
#     )

#     context_aggregator = LLMContextAggregatorPair(error_context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),
#             context_aggregator.user(),
#             rtvi,
#             llm,
#             ws_transport.output(),
#             context_aggregator.assistant(),
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         await task.queue_frames([LLMRunFrame()])
#         if questions_data:
#             logger.info(f"📚 Starting quiz with {len(questions_data)} questions")
#         else:
#             logger.warning("⚠️ No questions loaded, will inform user")

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise


#------- SESSION VALIDATION WORKED ------#
# import os
# import aiohttp
# import json
# from typing import Dict, Any, Optional
# from datetime import datetime

# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.audio.vad.vad_analyzer import VADParams
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# from pipecat_flows import (
#     FlowArgs,
#     FlowManager,
#     FlowResult,
#     FlowsFunctionSchema,
#     NodeConfig,
# )

# load_dotenv(override=True)

# # Node API configuration
# NODE_API_URL = os.getenv("NODE_API_URL", "http://localhost:3000")


# # ============================================================================
# # Type Definitions
# # ============================================================================

# class SessionValidationResult(FlowResult):
#     """Result type for session validation"""
#     valid: bool
#     total_questions: int


# class AnswerResult(FlowResult):
#     """Result type for answer processing"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str
#     score: int
#     total_questions: int


# class QuizCompleteResult(FlowResult):
#     """Result type for quiz completion"""
#     total_questions: int
#     correct_answers: int
#     score_percentage: float

# async def get_questions(session_code: str) -> Dict[str, Any]:
#     """Get questions for a session - simple standalone version"""
#     try:
#         url = f"http://localhost:3000/api/sessions/{session_code}/questions"
#         logger.info(f"🌐 Calling API: GET {url}")
        
#         timeout = aiohttp.ClientTimeout(total=10)
#         async with aiohttp.ClientSession(timeout=timeout) as session:
#             async with session.get(url) as response:
#                 logger.info(f"📊 API Response Status: {response.status}")
                
#                 if response.status == 200:
#                     data = await response.json()
#                     logger.info(f"✅ Got questions for session {session_code}")
#                     return data
#                 else:
#                     error_text = await response.text()
#                     logger.error(f"❌ API error {response.status}: {error_text}")
#                     return {
#                         "error": f"API error: {response.status}",
#                         "status": "error"
#                     }
#     except Exception as e:
#         logger.error(f"❌ Error getting questions: {e}")
#         return {"error": str(e), "status": "error"}

# # ============================================================================
# # API Client
# # ============================================================================

# class QuizAPIClient:
#     """Client for interacting with the Node.js quiz API"""
    
#     def __init__(self, base_url: str):
#         self.base_url = base_url
#         self.session: Optional[aiohttp.ClientSession] = None
    
#     async def __aenter__(self):
#         self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))
#         return self
    
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         if self.session:
#             await self.session.close()
    
#     async def validate_session(self, session_code: str) -> Dict[str, Any]:
#         """Validate session code and get quiz details"""
#         try:
#             async with self.session.get(
#                 f"{self.base_url}/api/session/{session_code}/check-exists"
#             ) as response:
#                 if response.status == 200:
#                     logger.info(f"Session {session_code} exists")
#                     data = await response.json()
#                     return {"valid": True, "error": ""}
#                 else:
#                     logger.error(f"API returned status {response.status}")
#                     return {"valid": False, "error": f"API error: {response.status}"}
#         except Exception as e:
#             logger.error(f"Error validating session: {e}")
#             return {"valid": False, "error": str(e)}
    
#     async def get_questionssss(self, session_code: str) -> Dict[str, Any]:
#         """Get questions for a session"""
#         try:
#             logger.info(f"Getting questions for session {session_code}")
#             async with self.session.get(
#                 f"http://localhost:3000/api/sessions/H6TU/questions"
#             ) as response:
#                 logger.info(f"API returned status {response.status}")
#                 if response.status == 200:
#                     logger.info(f"API returned status {response.status}")
#                     data = await response.json()
#                     logger.info(f"API returned data {data}")
#                     return data
#                 else:
#                     logger.error(f"API returned status {response.status}")
#                     return {"error": f"API error: {response.status}"}
#         except Exception as e:
#             logger.error(f"Error getting questions: {e}")
#             return {"error": str(e)}
    
#     async def submit_answer(self, session_code: str, question_id: str, answer: str) -> Dict[str, Any]:
#         """Submit answer for validation"""
#         try:
#             async with self.session.post(
#                 f"{self.base_url}/api/session/{session_code}/answer",
#                 json={"question_id": question_id, "answer": answer}
#             ) as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     return data
#                 else:
#                     logger.error(f"API returned status {response.status}")
#                     return {"correct": False, "error": f"API error: {response.status}"}
#         except Exception as e:
#             logger.error(f"Error submitting answer: {e}")
#             return {"correct": False, "error": str(e)}


# # ============================================================================
# # Helper Functions
# # ============================================================================

# def format_question_for_display(question_data: Dict[str, Any]) -> str:
#     """Format question for LLM display"""
#     question_text = question_data.get("question_text", "No question text")
#     options = question_data.get("question_options", [])
    
#     # Format options with letters
#     formatted_options = []
#     letters = ["A", "B", "C", "D", "E", "F"]
    
#     for i, option in enumerate(options[:6]):  # Limit to 6 options
#         option_text = option.get("option_text", f"Option {i+1}")
#         formatted_options.append(f"{letters[i]}. {option_text}")
    
#     options_text = "\n".join(formatted_options)
    
#     return f"Question: {question_text}\n\nOptions:\n{options_text}"


# def get_correct_answer(question_data: Dict[str, Any]) -> str:
#     """Get the correct answer for a question"""
#     options = question_data.get("question_options", [])
#     for option in options:
#         if option.get("is_correct", False):
#             return option.get("option_text", "")
#     return ""


# # ============================================================================
# # Flow Node Functions
# # ============================================================================

# def create_welcome_node() -> NodeConfig:
#     """Create the Welcome node."""
    
#     async def handle_validate_session(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[SessionValidationResult, NodeConfig]:
#         """Handler for validate_session function"""
#         session_code: str = args.get("session_code", "").strip().upper()
        
#         # Store session code in state
#         flow_manager.state["session_code"] = session_code
        
#         # Validate session via API
#         async with QuizAPIClient(NODE_API_URL) as client:
#             result = await client.validate_session(session_code)
#             logger.info(f"Session {session_code} validation result: {result}")
        
#         if result.get('valid'):
#             # Get questions for this session
#             questions_result = await get_questions(session_code)
            
#             if questions_result.get("status") == "ok" and "data" in questions_result:
#                 questions = questions_result["data"]
#                 logger.info(f"✅ Got questions for session {session_code}, {questions}")
#                 flow_manager.state["questions"] = questions
#                 flow_manager.state["total_questions"] = len(questions)
#                 flow_manager.state["current_question_index"] = 0
#                 flow_manager.state["score"] = 0
#                 flow_manager.state["start_time"] = datetime.now().isoformat()
                
#                 logger.info(f"✅ Loaded {len(questions)} questions for session {session_code}")
                
#                 return SessionValidationResult(
#                     valid=True,
#                     #quiz_title=result.get("quiz_title", "Quiz"),
#                     total_questions=len(questions)
#                 ), create_ask_question_node()
        
#         # If validation failed
#         return SessionValidationResult(
#             valid=False,
#             quiz_title="",
#             total_questions=0
#         ), create_invalid_session_node()
    
#     validate_session_func = FlowsFunctionSchema(
#         name="validate_session",
#         handler=handle_validate_session,
#         description="Validate the session code and load quiz questions",
#         properties={
#             "session_code": {
#                 "type": "string",
#                 "description": "The session code provided by the user"
#             }
#         },
#         required=["session_code"],
#     )
    
#     return NodeConfig(
#         name="welcome",
#         role_messages=[
#             {
#                 "role": "system",
#                 "content": "You are a friendly and enthusiastic quiz host. Your goal is to create a fun and engaging quiz experience. Be encouraging, clear, and maintain a positive energy throughout."
#             }
#         ],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "Welcome the user warmly to the quiz application! Introduce yourself as the quiz host and ask them to provide their session code. Explain that they need a valid session code to join a quiz. Be patient and encouraging."
#             }
#         ],
#         functions=[validate_session_func],
#     )


# def create_invalid_session_node() -> NodeConfig:
#     """Create node for invalid session code"""
    
#     async def handle_retry_session(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[SessionValidationResult, NodeConfig]:
#         """Handler for retry_session function"""
#         session_code: str = args.get("session_code", "").strip().upper()
#         flow_manager.state["session_code"] = session_code
        
#         async with QuizAPIClient(NODE_API_URL) as client:
#             result = await client.validate_session(session_code)
        
#         if result.get("valid"):
#             questions_result = await client.get_questions(session_code)
            
#             if questions_result.get("status") == "ok" and "data" in questions_result:
#                 questions = questions_result["data"]
#                 flow_manager.state["questions"] = questions
#                 flow_manager.state["total_questions"] = len(questions)
#                 flow_manager.state["current_question_index"] = 0
#                 flow_manager.state["score"] = 0
                
#                 return SessionValidationResult(
#                     valid=True,
#                     quiz_title=result.get("quiz_title", "Quiz"),
#                     total_questions=len(questions)
#                 ), create_instructions_node()
        
#         return SessionValidationResult(
#             valid=False,
#             quiz_title="",
#             total_questions=0
#         ), create_invalid_session_node()
    
#     retry_session_func = FlowsFunctionSchema(
#         name="retry_session",
#         handler=handle_retry_session,
#         description="Try again with a different session code",
#         properties={
#             "session_code": {
#                 "type": "string",
#                 "description": "The session code provided by the user"
#             }
#         },
#         required=["session_code"],
#     )
    
#     return NodeConfig(
#         name="invalid_session",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "The session code you provided is invalid or expired. Apologize and ask the user to check their code and try again. Be helpful and encouraging."
#             }
#         ],
#         functions=[retry_session_func],
#     )


# def create_instructions_node() -> NodeConfig:
#     """Create the Instructions node."""
    
#     async def handle_start_quiz(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[None, NodeConfig]:
#         """Handler for start_quiz function"""
#         return None, create_ask_question_node()
    
#     async def handle_exit_quiz(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[None, NodeConfig]:
#         """Handler for exit_quiz function"""
#         return None, create_goodbye_node()
    
#     start_quiz_func = FlowsFunctionSchema(
#         name="start_quiz",
#         handler=handle_start_quiz,
#         description="Start the quiz with the loaded questions",
#         properties={},
#         required=[],
#     )
    
#     exit_quiz_func = FlowsFunctionSchema(
#         name="exit_quiz",
#         handler=handle_exit_quiz,
#         description="Exit the quiz without starting",
#         properties={},
#         required=[],
#     )
    
#     return NodeConfig(
#         name="instructions",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "Welcome the user to the quiz! Explain the format: 1) You'll ask questions one at a time, 2) Each question has multiple choice options (A, B, C, D, etc.), 3) They can answer with the letter or the full text, 4) You'll provide immediate feedback after each answer, 5) Their score will be shown at the end. Ask if they're ready to begin."
#             }
#         ],
#         functions=[start_quiz_func, exit_quiz_func],
#     )


# # def create_ask_question_node() -> NodeConfig:
# #     """Create the Ask Question node."""
    
# #     async def handle_submit_answer(
# #         args: FlowArgs, flow_manager: FlowManager
# #     ) -> tuple[AnswerResult, NodeConfig]:
# #         """Handler for submit_answer function"""
# #         user_answer: str = args.get("answer", "").strip()
# #         session_code = flow_manager.state.get("session_code", "")
# #         current_index = flow_manager.state.get("current_question_index", 0)
# #         questions = flow_manager.state.get("questions", [])
# #         score = flow_manager.state.get("score", 0)
        
# #         if current_index >= len(questions):
# #             # Quiz is complete
# #             return AnswerResult(
# #                 question_index=current_index,
# #                 user_answer=user_answer,
# #                 is_correct=False,
# #                 correct_answer="",
# #                 score=score,
# #                 total_questions=len(questions)
# #             ), create_quiz_complete_node()
        
# #         current_question = questions[current_index]
# #         question_id = current_question.get("id", str(current_index))
        
# #         # Submit answer to API
# #         async with QuizAPIClient(NODE_API_URL) as client:
# #             result = await client.submit_answer(session_code, question_id, user_answer)
        
# #         is_correct = result.get("correct", False)
# #         correct_answer = result.get("correct_answer", get_correct_answer(current_question))
        
# #         # Update score
# #         if is_correct:
# #             score += 1
# #             flow_manager.state["score"] = score
        
# #         # Move to next question
# #         next_index = current_index + 1
# #         flow_manager.state["current_question_index"] = next_index
        
# #         result_obj = AnswerResult(
# #             question_index=current_index,
# #             user_answer=user_answer,
# #             is_correct=is_correct,
# #             correct_answer=correct_answer,
# #             score=score,
# #             total_questions=len(questions)
# #         )
        
# #         if next_index < len(questions):
# #             return result_obj, create_answer_feedback_node()
# #         else:
# #             return result_obj, create_quiz_complete_node()
    
# #     async def handle_repeat_question(
# #         args: FlowArgs, flow_manager: FlowManager
# #     ) -> tuple[None, NodeConfig]:
# #         """Handler for repeat_question function"""
# #         return None, create_ask_question_node()
    
# #     async def handle_skip_question(
# #         args: FlowArgs, flow_manager: FlowManager
# #     ) -> tuple[AnswerResult, NodeConfig]:
# #         """Handler for skip_question function"""
# #         current_index = flow_manager.state.get("current_question_index", 0)
# #         questions = flow_manager.state.get("questions", [])
# #         score = flow_manager.state.get("score", 0)
        
# #         # Move to next question
# #         next_index = current_index + 1
# #         flow_manager.state["current_question_index"] = next_index
        
# #         result = AnswerResult(
# #             question_index=current_index,
# #             user_answer="(skipped)",
# #             is_correct=False,
# #             correct_answer=get_correct_answer(questions[current_index]) if current_index < len(questions) else "",
# #             score=score,
# #             total_questions=len(questions)
# #         )
        
# #         if next_index < len(questions):
# #             return result, create_ask_question_node()
# #         else:
# #             return result, create_quiz_complete_node()
    
# #     submit_answer_func = FlowsFunctionSchema(
# #         name="submit_answer",
# #         handler=handle_submit_answer,
# #         description="Submit the user's answer for the current question",
# #         properties={
# #             "answer": {
# #                 "type": "string",
# #                 "description": "The user's answer (can be letter like 'A', 'B', etc. or full text)"
# #             }
# #         },
# #         required=["answer"],
# #     )
    
# #     repeat_question_func = FlowsFunctionSchema(
# #         name="repeat_question",
# #         handler=handle_repeat_question,
# #         description="Repeat the current question",
# #         properties={},
# #         required=[],
# #     )
    
# #     skip_question_func = FlowsFunctionSchema(
# #         name="skip_question",
# #         handler=handle_skip_question,
# #         description="Skip the current question",
# #         properties={},
# #         required=[],
# #     )
    
# #     return NodeConfig(
# #         name="ask_question",
# #         task_messages=[
# #             {
# #                 "role": "system",
# #                 "content": """You are now asking a quiz question. Follow these steps:
# # 1. Announce the question number (e.g., "Question 1 of 10")
# # 2. Read the question clearly from: {current_question_text}
# # 3. Read all the options clearly
# # 4. Ask "What's your answer?"
# # 5. Wait for their response

# # Be clear and enthusiastic!"""
# #             }
# #         ],
# #         pre_actions=[
# #             {
# #                 "type": "function",
# #                 "handler": lambda action, fm: prepare_current_question(action, fm)
# #             }
# #         ],
# #         functions=[submit_answer_func, repeat_question_func, skip_question_func],
# #     )

# # def create_ask_question_node() -> NodeConfig:
# #     return NodeConfig(
# #         name="ask_question",
# #         task_messages=[
# #             {
# #                 "role": "system",
# #                 "content": """You are now asking a quiz question. Follow these steps:
# # 1. Announce the question number (e.g., "Question 1 of 10")
# # 2. Read the question clearly from: {current_question_text}
# # 3. Read all the options clearly
# # 4. Ask "What's your answer?"
# # 5. Wait for their response

# # Be clear and enthusiastic!"""
# #             }
# #         ],
# #         pre_actions=[
# #             {
# #                 "type": "function",
# #                 "handler": lambda action, fm: prepare_current_question(action, fm)  # This should execute
# #             }
# #         ],
# #         functions=[submit_answer_func, repeat_question_func, skip_question_func],
# #     )

# def create_ask_question_node() -> NodeConfig:
#     """Create the Ask Question node."""
    
#     async def handle_submit_answer(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[AnswerResult, NodeConfig]:
#         """Handler for submit_answer function"""
#         user_answer: str = args.get("answer", "").strip()
#         current_index = flow_manager.state.get("current_question_index", 0)
#         questions = flow_manager.state.get("questions", [])
#         score = flow_manager.state.get("score", 0)
        
#         logger.info(f"📝 Processing answer for question {current_index + 1}: '{user_answer}'")
        
#         if current_index >= len(questions):
#             logger.info("🎉 Quiz is complete")
#             return AnswerResult(
#                 question_index=current_index,
#                 user_answer=user_answer,
#                 is_correct=False,
#                 correct_answer="",
#                 score=score,
#                 total_questions=len(questions)
#             ), create_quiz_complete_node()
        
#         current_question = questions[current_index]
        
#         # Check answer locally
#         is_correct = False
#         correct_answer = get_correct_answer(current_question)
        
#         # Simple answer checking
#         user_answer_lower = user_answer.strip().lower()
#         correct_answer_lower = correct_answer.lower()
        
#         # Check if answer matches correct answer or is a letter option
#         letters = ["a", "b", "c", "d", "e", "f"]
#         if user_answer_lower in letters:
#             # User answered with a letter, need to check which option it corresponds to
#             index = letters.index(user_answer_lower)
#             options = current_question.get("question_options", [])
#             if index < len(options):
#                 selected_option = options[index]
#                 is_correct = selected_option.get("is_correct", False)
#         elif user_answer_lower == correct_answer_lower:
#             # User answered with the exact text
#             is_correct = True
#         else:
#             # Check for partial match
#             is_correct = user_answer_lower in correct_answer_lower or correct_answer_lower in user_answer_lower
        
#         # Update score
#         if is_correct:
#             score += 1
#             flow_manager.state["score"] = score
#             logger.info(f"✅ Correct! Score: {score}")
#         else:
#             logger.info(f"❌ Incorrect. Correct answer: {correct_answer}")
        
#         # Store result for feedback
#         flow_manager.state["last_answer_result"] = {
#             "is_correct": is_correct,
#             "correct_answer": correct_answer,
#             "user_answer": user_answer
#         }
        
#         # Move to next question
#         next_index = current_index + 1
#         flow_manager.state["current_question_index"] = next_index
        
#         result_obj = AnswerResult(
#             question_index=current_index,
#             user_answer=user_answer,
#             is_correct=is_correct,
#             correct_answer=correct_answer,
#             score=score,
#             total_questions=len(questions)
#         )
        
#         if next_index < len(questions):
#             return result_obj, create_answer_feedback_node()
#         else:
#             return result_obj, create_quiz_complete_node()
    
#     async def handle_repeat_question(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[None, NodeConfig]:
#         """Handler for repeat_question function"""
#         logger.info("🔁 Repeating question")
#         return None, create_ask_question_node()
    
#     async def handle_skip_question(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[AnswerResult, NodeConfig]:
#         """Handler for skip_question function"""
#         current_index = flow_manager.state.get("current_question_index", 0)
#         questions = flow_manager.state.get("questions", [])
#         score = flow_manager.state.get("score", 0)
        
#         logger.info(f"⏭️ Skipping question {current_index + 1}")
        
#         # Store correct answer for feedback
#         correct_answer = ""
#         if current_index < len(questions):
#             correct_answer = get_correct_answer(questions[current_index])
#             flow_manager.state["last_answer_result"] = {
#                 "is_correct": False,
#                 "correct_answer": correct_answer,
#                 "user_answer": "(skipped)"
#             }
        
#         # Move to next question
#         next_index = current_index + 1
#         flow_manager.state["current_question_index"] = next_index
        
#         result = AnswerResult(
#             question_index=current_index,
#             user_answer="(skipped)",
#             is_correct=False,
#             correct_answer=correct_answer,
#             score=score,
#             total_questions=len(questions)
#         )
        
#         if next_index < len(questions):
#             return result, create_answer_feedback_node()
#         else:
#             return result, create_quiz_complete_node()
    
#     # Define the function schemas
#     submit_answer_func = FlowsFunctionSchema(
#         name="submit_answer",
#         handler=handle_submit_answer,
#         description="Submit the user's answer for the current question",
#         properties={
#             "answer": {
#                 "type": "string",
#                 "description": "The user's answer (can be letter like 'A', 'B', etc. or full text)"
#             }
#         },
#         required=["answer"],
#     )
    
#     repeat_question_func = FlowsFunctionSchema(
#         name="repeat_question",
#         handler=handle_repeat_question,
#         description="Repeat the current question",
#         properties={},
#         required=[],
#     )
    
#     skip_question_func = FlowsFunctionSchema(
#         name="skip_question",
#         handler=handle_skip_question,
#         description="Skip the current question",
#         properties={},
#         required=[],
#     )
    
#     return NodeConfig(
#         name="ask_question",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """You are now asking a quiz question. Follow these steps:
# 1. Announce the question number (e.g., "Question {current_question_number} of {total_questions}")
# 2. Read the question clearly from: {current_question_text}
# 3. Read all the options clearly
# 4. Ask "What's your answer?"
# 5. Wait for their response

# Be clear and enthusiastic!"""
#             }
#         ],
#         pre_actions=[
#             {
#                 "type": "function",
#                 "handler": lambda action, fm: prepare_current_question(action, fm)
#             }
#         ],
#         functions=[submit_answer_func, repeat_question_func, skip_question_func],
#     )

# async def prepare_current_question(action: Dict[str, Any], flow_manager: FlowManager) -> None:
#     """Prepare the current question for display"""
#     current_index = flow_manager.state.get("current_question_index", 0)
#     questions = flow_manager.state.get("questions", [])
#     logger.info(f"in the questions handler: {questions}")
    
#     if current_index < len(questions):
#         current_question = questions[current_index]
#         formatted_question = format_question_for_display(current_question)
        
#         # Store in state for template rendering
#         flow_manager.state["current_question_text"] = formatted_question
#         flow_manager.state["current_question_id"] = current_question.get("id", str(current_index))
        
#         logger.info(f"📝 Prepared question {current_index + 1}/{len(questions)}")
#     else:
#         flow_manager.state["current_question_text"] = "No more questions"
#         logger.warning("No more questions available")


# def create_answer_feedback_node() -> NodeConfig:
#     """Create the Answer Feedback node."""
    
#     async def handle_next_question(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[None, NodeConfig]:
#         """Handler for next_question function"""
#         return None, create_ask_question_node()
    
#     next_question_func = FlowsFunctionSchema(
#         name="next_question",
#         handler=handle_next_question,
#         description="Move to the next question",
#         properties={},
#         required=[],
#     )
    
#     return NodeConfig(
#         name="answer_feedback",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Provide feedback on their answer. Follow these rules:
# 1. If correct: "That's right! [Correct answer] is correct! [Brief positive reinforcement]"
# 2. If incorrect: "Actually, the correct answer is [correct answer]. [Brief explanation if available]"
# 3. Share their current score: "Your current score is [score] out of [total_questions]."
# 4. Then say: "Ready for the next question?" and proceed."""
#             }
#         ],
#         functions=[next_question_func],
#     )


# def create_quiz_complete_node() -> NodeConfig:
#     """Create the Quiz Complete node."""
    
#     async def handle_show_results(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[QuizCompleteResult, NodeConfig]:
#         """Handler for show_results function"""
#         total_questions = flow_manager.state.get("total_questions", 0)
#         score = flow_manager.state.get("score", 0)
#         score_percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
#         return QuizCompleteResult(
#             total_questions=total_questions,
#             correct_answers=score,
#             score_percentage=score_percentage
#         ), create_goodbye_node()
    
#     show_results_func = FlowsFunctionSchema(
#         name="show_results",
#         handler=handle_show_results,
#         description="Show the final quiz results",
#         properties={},
#         required=[],
#     )
    
#     return NodeConfig(
#         name="quiz_complete",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "Congratulations! You've completed the quiz. Take a moment to acknowledge their effort, then use the show_results function to display their final score."
#             }
#         ],
#         functions=[show_results_func],
#     )


# def create_goodbye_node() -> NodeConfig:
#     """Create the Goodbye node."""
#     return NodeConfig(
#         name="goodbye",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "Thank them for participating in the quiz. Share their final score in a positive and encouraging way. Give feedback based on their performance (excellent, good, or encouraging for next time). End with a warm farewell."
#             }
#         ],
#         post_actions=[{"type": "end_conversation"}],
#     )

# async def run_bot(websocket_client, session_code: Optional[str] = None):
#     """Run the quiz bot with flow management"""
#     logger.info(f"🤖 Starting quiz bot")
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create LLM service
#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         config={
#             "system_instruction": "You are QuizMaster AI, an engaging quiz host. Be energetic, clear, and supportive. Speak naturally in a conversational tone. Always speak out the questions and options clearly."
#         }
#     )

#     # Create conversation context
#     context = LLMContext()
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),          # Receive audio from WebSocket
#             context_aggregator.user(),     # Add user messages to context
#             rtvi,                          # RTVI monitoring
#             llm,                           # Gemini LLM with TTS
#             ws_transport.output(),         # Send audio back via WebSocket
#             context_aggregator.assistant(), # Add bot responses to context
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#             allow_interruptions=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Initialize flow manager - REMOVED global_functions since they were causing issues
#     flow_manager = FlowManager(
#         task=task,
#         llm=llm,
#         context_aggregator=context_aggregator,
#         transport=ws_transport,
#         # Removed: global_functions=[get_session_info, get_question_hint],
#     )
    
#     # Store initial session code if provided
#     if session_code:
#         flow_manager.state["session_code"] = session_code

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Initialize the flow with welcome node
#         await flow_manager.initialize(create_welcome_node())

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()
    
    

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise


"""
Quiz Application with Pipecat Flows using Gemini Multimodal Live LLM
Simplified version without pre-actions
"""

# import os
# import aiohttp
# import json
# from typing import Dict, Any, Optional
# from datetime import datetime

# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.audio.vad.vad_analyzer import VADParams
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# from pipecat_flows import (
#     FlowArgs,
#     FlowManager,
#     FlowResult,
#     FlowsFunctionSchema,
#     NodeConfig,
# )

# load_dotenv(override=True)

# # Node API configuration
# NODE_API_URL = os.getenv("NODE_API_URL", "http://localhost:3000")


# # ============================================================================
# # Type Definitions
# # ============================================================================

# class SessionValidationResult(FlowResult):
#     """Result type for session validation"""
#     valid: bool
#     total_questions: int


# class QuestionResult(FlowResult):
#     """Result type for question handling"""
#     question_index: int
#     question_text: str


# class AnswerResult(FlowResult):
#     """Result type for answer processing"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str
#     score: int


# class QuizCompleteResult(FlowResult):
#     """Result type for quiz completion"""
#     total_questions: int
#     correct_answers: int
#     score_percentage: float


# # ============================================================================
# # Helper Functions
# # ============================================================================

# async def get_questions(session_code: str) -> Dict[str, Any]:
#     """Get questions for a session"""
#     try:
#         url = f"http://localhost:3000/api/sessions/{session_code}/questions"
#         logger.info(f"🌐 Calling API: GET {url}")
        
#         timeout = aiohttp.ClientTimeout(total=10)
#         async with aiohttp.ClientSession(timeout=timeout) as session:
#             async with session.get(url) as response:
#                 logger.info(f"📊 API Response Status: {response.status}")
                
#                 if response.status == 200:
#                     data = await response.json()
#                     logger.info(f"✅ Got questions for session {session_code}")
                    
#                     # Check response format
#                     if isinstance(data, dict) and "data" in data:
#                         # Format: {"status": "ok", "data": [...]}
#                         return {"status": "ok", "data": data["data"]}
#                     elif isinstance(data, list):
#                         # Format: direct list of questions
#                         return {"status": "ok", "data": data}
#                     else:
#                         logger.error(f"❌ Unexpected response format: {data}")
#                         return {"status": "error", "error": "Unexpected format"}
#                 else:
#                     error_text = await response.text()
#                     logger.error(f"❌ API error {response.status}: {error_text}")
#                     return {"status": "error", "error": f"API error: {response.status}"}
#     except Exception as e:
#         logger.error(f"❌ Error getting questions: {e}")
#         return {"status": "error", "error": str(e)}


# def format_question_for_display(question_data: Dict[str, Any]) -> str:
#     """Format question for LLM display"""
#     question_text = question_data.get("question_text", "No question text")
#     options = question_data.get("question_options", [])
    
#     # Format options with letters
#     formatted_options = []
#     letters = ["A", "B", "C", "D", "E", "F"]
    
#     for i, option in enumerate(options[:6]):  # Limit to 6 options
#         option_text = option.get("option_text", f"Option {i+1}")
#         formatted_options.append(f"{letters[i]}. {option_text}")
    
#     options_text = "\n".join(formatted_options)
    
#     return f"QUESTION: {question_text}\n\nOPTIONS:\n{options_text}"


# def get_correct_answer(question_data: Dict[str, Any]) -> str:
#     """Get the correct answer for a question"""
#     options = question_data.get("question_options", [])
#     for option in options:
#         if option.get("is_correct", False):
#             return option.get("option_text", "")
#     return ""


# # ============================================================================
# # Flow Node Functions - NO PRE-ACTIONS, JUST FUNCTIONS
# # ============================================================================

# def create_welcome_node() -> NodeConfig:
#     """Create the Welcome node."""

#     async def handle_validate_session(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[SessionValidationResult, NodeConfig]:
#         """Handler for validate_session function"""
#         session_code: str = args.get("session_code", "").strip().upper()
        
#         logger.info(f"🔍 Validating session: {session_code}")
        
#         if not session_code:
#             logger.error("❌ No session code provided")
#             return SessionValidationResult(valid=False, total_questions=0), create_invalid_session_node()
        
#         # Store session code in state
#         flow_manager.state["session_code"] = session_code
        
#         # Get questions from API
#         questions_result = await get_questions(session_code)
        
#         logger.info(f"📊 Questions API result: {questions_result.get('status')}")
        
#         if questions_result.get("status") == "ok" and "data" in questions_result:
#             questions = questions_result["data"]
            
#             if questions and len(questions) > 0:
#                 # Store questions and initialize state
#                 flow_manager.state["questions"] = questions
#                 flow_manager.state["total_questions"] = len(questions)
#                 flow_manager.state["current_question_index"] = 0
#                 flow_manager.state["score"] = 0
                
#                 logger.info(f"✅ Loaded {len(questions)} questions for session {session_code}")
                
#                 # Go directly to ask question node
#                 return SessionValidationResult(
#                     valid=True,
#                     total_questions=len(questions)
#                 ), create_ask_question_node()
#             else:
#                 logger.error("❌ No questions found for session")
#                 return SessionValidationResult(valid=False, total_questions=0), create_no_questions_node()
#         else:
#             logger.error(f"❌ API error: {questions_result.get('error', 'Unknown error')}")
#             return SessionValidationResult(valid=False, total_questions=0), create_invalid_session_node()

#     validate_session_func = FlowsFunctionSchema(
#         name="validate_session",
#         handler=handle_validate_session,
#         description="Validate the session code and load quiz questions",
#         properties={
#             "session_code": {
#                 "type": "string",
#                 "description": "The session code provided by the user (e.g., H6TU)"
#             }
#         },
#         required=["session_code"],
#     )
    
#     return NodeConfig(
#         name="welcome",
#         role_messages=[
#             {
#                 "role": "system",
#                 "content": "You are a friendly and enthusiastic quiz host. Your goal is to create a fun and engaging quiz experience. Be encouraging, clear, and maintain a positive energy throughout."
#             }
#         ],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "Welcome the user warmly to the quiz application! Introduce yourself as the quiz host and ask them to provide their session code. Explain that they need a valid session code to join a quiz. Be patient and encouraging."
#             }
#         ],
#         functions=[validate_session_func],
#     )


# def create_invalid_session_node() -> NodeConfig:
#     """Create node for invalid session code"""
    
#     async def handle_retry_session(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[SessionValidationResult, NodeConfig]:
#         """Handler for retry_session function"""
#         session_code: str = args.get("session_code", "").strip().upper()
        
#         logger.info(f"🔄 Retrying validation for session: {session_code}")
        
#         if not session_code:
#             logger.error("❌ No session code provided in retry")
#             return SessionValidationResult(valid=False, total_questions=0), create_invalid_session_node()
        
#         flow_manager.state["session_code"] = session_code
        
#         # Get questions from API
#         questions_result = await get_questions(session_code)
        
#         if questions_result.get("status") == "ok" and "data" in questions_result:
#             questions = questions_result["data"]
            
#             if questions and len(questions) > 0:
#                 flow_manager.state["questions"] = questions
#                 flow_manager.state["total_questions"] = len(questions)
#                 flow_manager.state["current_question_index"] = 0
#                 flow_manager.state["score"] = 0
                
#                 logger.info(f"✅ Retry successful! Loaded {len(questions)} questions")
                
#                 # Go directly to ask question node
#                 return SessionValidationResult(
#                     valid=True,
#                     total_questions=len(questions)
#                 ), create_ask_question_node()
        
#         logger.error(f"❌ Retry failed for session {session_code}")
#         return SessionValidationResult(valid=False, total_questions=0), create_invalid_session_node()
    
#     retry_session_func = FlowsFunctionSchema(
#         name="retry_session",
#         handler=handle_retry_session,
#         description="Try again with a different session code",
#         properties={
#             "session_code": {
#                 "type": "string",
#                 "description": "The session code provided by the user"
#             }
#         },
#         required=["session_code"],
#     )
    
#     return NodeConfig(
#         name="invalid_session",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "The session code you provided is invalid or doesn't exist. Please check your code and try again. Be helpful and encouraging."
#             }
#         ],
#         functions=[retry_session_func],
#     )


# def create_no_questions_node() -> NodeConfig:
#     """Create node when no questions are available"""
#     return NodeConfig(
#         name="no_questions",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "The session exists but there are no questions available. Apologize and suggest trying a different session or contacting the quiz administrator."
#             }
#         ],
#         post_actions=[{"type": "end_conversation"}],
#     )


# def create_ask_question_node() -> NodeConfig:
#     """Create the Ask Question node."""
    
#     async def handle_ask_current_question(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[QuestionResult, NodeConfig]:
#         """Handler for ask_current_question function"""
#         current_index = flow_manager.state.get("current_question_index", 0)
#         questions = flow_manager.state.get("questions", [])
#         total_questions = len(questions)
        
#         logger.info(f"📝 Asking question {current_index + 1} of {total_questions}")
        
#         if current_index >= total_questions:
#             logger.info("🎉 No more questions, quiz complete")
#             return QuestionResult(
#                 question_index=current_index,
#                 question_text="Quiz Complete"
#             ), create_quiz_complete_node()
        
#         current_question = questions[current_index]
#         question_text = current_question.get("question_text", "No question text")
        
#         # Format the question for the LLM
#         formatted_question = format_question_for_display(current_question)
        
#         # Store current question data in state
#         flow_manager.state["current_question_data"] = current_question
#         flow_manager.state["current_question_index"] = current_index
#         flow_manager.state["current_question_number"] = current_index + 1
#         flow_manager.state["total_questions"] = total_questions
        
#         logger.info(f"✅ Prepared question: {question_text[:50]}...")
        
#         return QuestionResult(
#             question_index=current_index,
#             question_text=question_text
#         ), create_ask_question_display_node()

#     ask_current_question_func = FlowsFunctionSchema(
#         name="ask_current_question",
#         handler=handle_ask_current_question,
#         description="Ask the current quiz question",
#         properties={},
#         required=[],
#     )
    
#     return NodeConfig(
#         name="ask_question",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """You are now ready to ask a quiz question. 
#                 Use the ask_current_question function to begin."""
#             }
#         ],
#         functions=[ask_current_question_func],
#     )


# def create_ask_question_display_node() -> NodeConfig:
#     """Create node to display the question (after it's prepared)"""
    
#     async def handle_submit_answer(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[AnswerResult, NodeConfig]:
#         """Handler for submit_answer function"""
#         user_answer: str = args.get("answer", "").strip()
#         current_index = flow_manager.state.get("current_question_index", 0)
#         questions = flow_manager.state.get("questions", [])
#         score = flow_manager.state.get("score", 0)
        
#         logger.info(f"📝 Processing answer: '{user_answer}' for question {current_index + 1}")
        
#         if current_index >= len(questions):
#             logger.info("🎉 Quiz is complete")
#             return AnswerResult(
#                 question_index=current_index,
#                 user_answer=user_answer,
#                 is_correct=False,
#                 correct_answer="",
#                 score=score
#             ), create_quiz_complete_node()
        
#         current_question = flow_manager.state.get("current_question_data", {})
#         correct_answer = get_correct_answer(current_question)
        
#         # Simple answer checking
#         user_answer_lower = user_answer.strip().lower()
#         correct_answer_lower = correct_answer.lower()
        
#         # Check if answer is correct
#         is_correct = False
        
#         # Check letter answers
#         letters = ["a", "b", "c", "d", "e", "f"]
#         if user_answer_lower in letters:
#             index = letters.index(user_answer_lower)
#             options = current_question.get("question_options", [])
#             if index < len(options):
#                 selected_option = options[index]
#                 is_correct = selected_option.get("is_correct", False)
#         # Check text answers
#         elif user_answer_lower == correct_answer_lower:
#             is_correct = True
#         else:
#             # Partial match
#             is_correct = (user_answer_lower in correct_answer_lower or 
#                          correct_answer_lower in user_answer_lower)
        
#         # Update score
#         if is_correct:
#             score += 1
#             flow_manager.state["score"] = score
        
#         # Store result for feedback
#         flow_manager.state["last_answer_result"] = {
#             "is_correct": is_correct,
#             "correct_answer": correct_answer,
#             "user_answer": user_answer
#         }
        
#         # Move to next question
#         next_index = current_index + 1
#         flow_manager.state["current_question_index"] = next_index
        
#         result = AnswerResult(
#             question_index=current_index,
#             user_answer=user_answer,
#             is_correct=is_correct,
#             correct_answer=correct_answer,
#             score=score
#         )
        
#         if next_index < len(questions):
#             return result, create_answer_feedback_node()
#         else:
#             return result, create_quiz_complete_node()
    
#     submit_answer_func = FlowsFunctionSchema(
#         name="submit_answer",
#         handler=handle_submit_answer,
#         description="Submit the user's answer for the current question",
#         properties={
#             "answer": {
#                 "type": "string",
#                 "description": "The user's answer (can be letter like 'A', 'B', etc. or full text)"
#             }
#         },
#         required=["answer"],
#     )
    
#     return NodeConfig(
#         name="ask_question_display",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """You are now asking a quiz question. 

# First, say: "Question {current_question_number} of {total_questions}"

# Then read this question exactly:

# {current_question_display}

# Then say: "What's your answer?" and wait for their response.

# IMPORTANT: Read the question and options exactly as shown above."""
#             }
#         ],
#         functions=[submit_answer_func],
#     )


# def create_answer_feedback_node() -> NodeConfig:
#     """Create the Answer Feedback node."""
    
#     async def handle_next_question(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[QuestionResult, NodeConfig]:
#         """Handler for next_question function"""
#         logger.info("➡️ Moving to next question")
#         return QuestionResult(
#             question_index=flow_manager.state.get("current_question_index", 0),
#             question_text="Next question"
#         ), create_ask_question_node()
    
#     next_question_func = FlowsFunctionSchema(
#         name="next_question",
#         handler=handle_next_question,
#         description="Move to the next question",
#         properties={},
#         required=[],
#     )
    
#     return NodeConfig(
#         name="answer_feedback",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """Provide feedback on their answer:

# Last answer was correct: {last_answer_correct}
# Correct answer: {last_correct_answer}
# User's answer: {last_user_answer}
# Current score: {current_score}/{total_questions}

# If correct: "That's right! '{last_correct_answer}' is correct! Great job!"
# If incorrect: "Actually, the correct answer is '{last_correct_answer}'."

# Then say: "Your current score is {current_score} out of {total_questions}."

# Finally: "Ready for the next question?" and use the next_question function."""
#             }
#         ],
#         functions=[next_question_func],
#     )


# def create_quiz_complete_node() -> NodeConfig:
#     """Create the Quiz Complete node."""
    
#     async def handle_show_results(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[QuizCompleteResult, NodeConfig]:
#         """Handler for show_results function"""
#         total_questions = flow_manager.state.get("total_questions", 0)
#         score = flow_manager.state.get("score", 0)
#         score_percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
#         logger.info(f"🏁 Quiz complete! Score: {score}/{total_questions} ({score_percentage:.1f}%)")
        
#         return QuizCompleteResult(
#             total_questions=total_questions,
#             correct_answers=score,
#             score_percentage=score_percentage
#         ), create_goodbye_node()
    
#     show_results_func = FlowsFunctionSchema(
#         name="show_results",
#         handler=handle_show_results,
#         description="Show the final quiz results",
#         properties={},
#         required=[],
#     )
    
#     return NodeConfig(
#         name="quiz_complete",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "🎉 Congratulations! You've completed the quiz! Take a moment to acknowledge their effort and hard work. Then use the show_results function to display their final score in an encouraging way."
#             }
#         ],
#         functions=[show_results_func],
#     )


# def create_goodbye_node() -> NodeConfig:
#     """Create the Goodbye node."""
#     return NodeConfig(
#         name="goodbye",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "Thank them for playing the quiz! Share their final score and give encouraging feedback. If they did well, congratulate them! If they could improve, encourage them to try again. End with a warm farewell."
#             }
#         ],
#         post_actions=[{"type": "end_conversation"}],
#     )


# # ============================================================================
# # Helper function to prepare question display
# # ============================================================================

# async def prepare_question_display(flow_manager: FlowManager) -> str:
#     """Prepare the current question for display"""
#     current_index = flow_manager.state.get("current_question_index", 0)
#     questions = flow_manager.state.get("questions", [])
    
#     if current_index < len(questions):
#         current_question = questions[current_index]
#         formatted_question = format_question_for_display(current_question)
        
#         # Store in state for the display node
#         flow_manager.state["current_question_display"] = formatted_question
#         flow_manager.state["current_question_number"] = current_index + 1
#         flow_manager.state["total_questions"] = len(questions)
        
#         logger.info(f"✅ Prepared question display for index {current_index}")
#         return formatted_question
#     else:
#         flow_manager.state["current_question_display"] = "No more questions"
#         return "No more questions"


# # ============================================================================
# # Main Bot Function
# # ============================================================================

# async def run_bot(websocket_client, session_code: Optional[str] = None):
#     """Run the quiz bot with flow management"""
#     logger.info("🤖 Starting Quiz Bot")
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.5)),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create Gemini Multimodal Live LLM service
#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         config={
#             "system_instruction": """You are QuizMaster, a friendly, enthusiastic quiz host. 
#             You speak clearly and energetically at a moderate pace.
#             You always read questions and options aloud exactly as provided.
#             You provide encouraging feedback after each answer.
#             You maintain a positive and engaging tone throughout the quiz."""
#         }
#     )

#     # Create conversation context
#     context = LLMContext()
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),
#             rtvi,
#             context_aggregator.user(),
#             llm,
#             ws_transport.output(),
#             context_aggregator.assistant(),
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#             allow_interruptions=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Initialize flow manager
#     flow_manager = FlowManager(
#         task=task,
#         llm=llm,
#         context_aggregator=context_aggregator,
#         transport=ws_transport,
#     )
    
#     # Store initial session code if provided
#     # if session_code:
#     #     flow_manager.state["session_code"] = session_code

#     # Event handlers - Simple like podcast example
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Initialize the flow with welcome node
#         await flow_manager.initialize(create_welcome_node())

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise

# import os
# import aiohttp
# import json
# from typing import Dict, Any, Optional
# from datetime import datetime

# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.audio.vad.vad_analyzer import VADParams
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# from pipecat_flows import (
#     FlowArgs,
#     FlowManager,
#     FlowResult,
#     FlowsFunctionSchema,
#     NodeConfig,
# )

# load_dotenv(override=True)

# # Node API configuration
# NODE_API_URL = os.getenv("NODE_API_URL", "http://localhost:3000")


# # ============================================================================
# # Type Definitions
# # ============================================================================

# class SessionValidationResult(FlowResult):
#     """Result type for session validation"""
#     valid: bool
#     total_questions: int


# class QuestionResult(FlowResult):
#     """Result type for question handling"""
#     question_index: int
#     question_text: str


# class AnswerResult(FlowResult):
#     """Result type for answer processing"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str
#     score: int


# class QuizCompleteResult(FlowResult):
#     """Result type for quiz completion"""
#     total_questions: int
#     correct_answers: int
#     score_percentage: float


# # ============================================================================
# # Helper Functions
# # ============================================================================

# async def get_questions(session_code: str) -> Dict[str, Any]:
#     """Get questions for a session"""
#     try:
#         url = f"http://localhost:3000/api/sessions/{session_code}/questions"
#         logger.info(f"🌐 Calling API: GET {url}")
        
#         timeout = aiohttp.ClientTimeout(total=10)
#         async with aiohttp.ClientSession(timeout=timeout) as session:
#             async with session.get(url) as response:
#                 logger.info(f"📊 API Response Status: {response.status}")
                
#                 if response.status == 200:
#                     data = await response.json()
#                     logger.info(f"✅ Got questions for session {session_code}")
                    
#                     # Check response format
#                     if isinstance(data, dict) and "data" in data:
#                         # Format: {"status": "ok", "data": [...]}
#                         return {"status": "ok", "data": data["data"]}
#                     elif isinstance(data, list):
#                         # Format: direct list of questions
#                         return {"status": "ok", "data": data}
#                     else:
#                         logger.error(f"❌ Unexpected response format: {data}")
#                         return {"status": "error", "error": "Unexpected format"}
#                 else:
#                     error_text = await response.text()
#                     logger.error(f"❌ API error {response.status}: {error_text}")
#                     return {"status": "error", "error": f"API error: {response.status}"}
#     except Exception as e:
#         logger.error(f"❌ Error getting questions: {e}")
#         return {"status": "error", "error": str(e)}


# def format_question_for_display(question_data: Dict[str, Any]) -> str:
#     """Format question for LLM display"""
#     question_text = question_data.get("question_text", "No question text")
#     options = question_data.get("question_options", [])
    
#     # Format options with letters
#     formatted_options = []
#     letters = ["A", "B", "C", "D", "E", "F"]
    
#     for i, option in enumerate(options[:6]):  # Limit to 6 options
#         option_text = option.get("option_text", f"Option {i+1}")
#         formatted_options.append(f"{letters[i]}. {option_text}")
    
#     options_text = "\n".join(formatted_options)
    
#     return f"{question_text}\n\n{options_text}"


# def get_correct_answer(question_data: Dict[str, Any]) -> str:
#     """Get the correct answer for a question"""
#     options = question_data.get("question_options", [])
#     for option in options:
#         if option.get("is_correct", False):
#             return option.get("option_text", "")
#     return ""


# # ============================================================================
# # Flow Node Functions
# # ============================================================================

# def create_welcome_node() -> NodeConfig:
#     """Create the Welcome node."""

#     async def handle_validate_session(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[SessionValidationResult, NodeConfig]:
#         """Handler for validate_session function"""
#         session_code: str = args.get("session_code", "").strip().upper()
        
#         logger.info(f"🔍 Validating session: {session_code}")
        
#         if not session_code:
#             logger.error("❌ No session code provided")
#             return SessionValidationResult(valid=False, total_questions=0), create_invalid_session_node()
        
#         # Store session code in state
#         flow_manager.state["session_code"] = session_code
        
#         # Get questions from API
#         questions_result = await get_questions(session_code)
        
#         logger.info(f"📊 Questions API result: {questions_result.get('status')}")
        
#         if questions_result.get("status") == "ok" and "data" in questions_result:
#             questions = questions_result["data"]
            
#             if questions and len(questions) > 0:
#                 # Store questions and initialize state
#                 flow_manager.state["questions"] = questions
#                 flow_manager.state["total_questions"] = len(questions)
#                 flow_manager.state["current_question_index"] = 0
#                 flow_manager.state["score"] = 0
                
#                 logger.info(f"✅ Loaded {len(questions)} questions for session {session_code}")
                
#                 # Go directly to ask question node
#                 return SessionValidationResult(
#                     valid=True,
#                     total_questions=len(questions)
#                 ), create_ask_question_node()
#             else:
#                 logger.error("❌ No questions found for session")
#                 return SessionValidationResult(valid=False, total_questions=0), create_no_questions_node()
#         else:
#             logger.error(f"❌ API error: {questions_result.get('error', 'Unknown error')}")
#             return SessionValidationResult(valid=False, total_questions=0), create_invalid_session_node()

#     validate_session_func = FlowsFunctionSchema(
#         name="validate_session",
#         handler=handle_validate_session,
#         description="Validate the session code and load quiz questions",
#         properties={
#             "session_code": {
#                 "type": "string",
#                 "description": "The session code provided by the user (e.g., H6TU)"
#             }
#         },
#         required=["session_code"],
#     )
    
#     return NodeConfig(
#         name="welcome",
#         role_messages=[
#             {
#                 "role": "system",
#                 "content": "You are a friendly and enthusiastic quiz host. Your goal is to create a fun and engaging quiz experience. Be encouraging, clear, and maintain a positive energy throughout."
#             }
#         ],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "Welcome the user warmly to the quiz application! Introduce yourself as the quiz host and ask them to provide their session code. Explain that they need a valid session code to join a quiz. Be patient and encouraging."
#             }
#         ],
#         functions=[validate_session_func],
#     )


# def create_invalid_session_node() -> NodeConfig:
#     """Create node for invalid session code"""
    
#     async def handle_retry_session(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[SessionValidationResult, NodeConfig]:
#         """Handler for retry_session function"""
#         session_code: str = args.get("session_code", "").strip().upper()
        
#         logger.info(f"🔄 Retrying validation for session: {session_code}")
        
#         if not session_code:
#             logger.error("❌ No session code provided in retry")
#             return SessionValidationResult(valid=False, total_questions=0), create_invalid_session_node()
        
#         flow_manager.state["session_code"] = session_code
        
#         # Get questions from API
#         questions_result = await get_questions(session_code)
        
#         if questions_result.get("status") == "ok" and "data" in questions_result:
#             questions = questions_result["data"]
            
#             if questions and len(questions) > 0:
#                 flow_manager.state["questions"] = questions
#                 flow_manager.state["total_questions"] = len(questions)
#                 flow_manager.state["current_question_index"] = 0
#                 flow_manager.state["score"] = 0
                
#                 logger.info(f"✅ Retry successful! Loaded {len(questions)} questions")
                
#                 # Go directly to ask question node
#                 return SessionValidationResult(
#                     valid=True,
#                     total_questions=len(questions)
#                 ), create_ask_question_node()
        
#         logger.error(f"❌ Retry failed for session {session_code}")
#         return SessionValidationResult(valid=False, total_questions=0), create_invalid_session_node()
    
#     retry_session_func = FlowsFunctionSchema(
#         name="retry_session",
#         handler=handle_retry_session,
#         description="Try again with a different session code",
#         properties={
#             "session_code": {
#                 "type": "string",
#                 "description": "The session code provided by the user"
#             }
#         },
#         required=["session_code"],
#     )
    
#     return NodeConfig(
#         name="invalid_session",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "The session code you provided is invalid or doesn't exist. Please check your code and try again. Be helpful and encouraging."
#             }
#         ],
#         functions=[retry_session_func],
#     )


# def create_no_questions_node() -> NodeConfig:
#     """Create node when no questions are available"""
#     return NodeConfig(
#         name="no_questions",
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "The session exists but there are no questions available. Apologize and suggest trying a different session or contacting the quiz administrator."
#             }
#         ],
#         post_actions=[{"type": "end_conversation"}],
#     )


# def create_ask_question_node() -> NodeConfig:
#     """Create the Ask Question node."""
    
#     async def pre_prepare_question(flow_manager: FlowManager):
#         """Pre-action to prepare question data"""
#         current_index = flow_manager.state.get("current_question_index", 0)
#         questions = flow_manager.state.get("questions", [])
#         total_questions = len(questions)
        
#         logger.info(f"📝 Preparing question {current_index + 1} of {total_questions}")
        
#         if current_index < total_questions:
#             current_question = questions[current_index]
            
#             # Store current question data in state
#             flow_manager.state["current_question_data"] = current_question
#             flow_manager.state["current_question_number"] = current_index + 1
#             flow_manager.state["total_questions"] = total_questions
    
#     async def handle_ask_current_question(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[QuestionResult, NodeConfig]:
#         """Handler for ask_current_question function"""
#         current_index = flow_manager.state.get("current_question_index", 0)
#         questions = flow_manager.state.get("questions", [])
#         total_questions = len(questions)
        
#         logger.info(f"📝 Asking question {current_index + 1} of {total_questions}")
        
#         if current_index >= total_questions:
#             logger.info("🎉 No more questions, quiz complete")
#             return QuestionResult(
#                 question_index=current_index,
#                 question_text="Quiz Complete"
#             ), create_quiz_complete_node()
        
#         current_question = questions[current_index]
#         question_text = current_question.get("question_text", "No question text")
        
#         logger.info(f"✅ Moving to question display node")
        
#         return QuestionResult(
#             question_index=current_index,
#             question_text=question_text
#         ), create_ask_question_display_node()

#     ask_current_question_func = FlowsFunctionSchema(
#         name="ask_current_question",
#         handler=handle_ask_current_question,
#         description="Ask the current quiz question",
#         properties={},
#         required=[],
#     )
    
#     return NodeConfig(
#         name="ask_question",
#         pre_actions=[pre_prepare_question],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": """You are ready to ask a quiz question. Use the ask_current_question function to begin."""
#             }
#         ],
#         functions=[ask_current_question_func],
#     )


# def create_ask_question_display_node() -> NodeConfig:
#     """Create node to display the question (after it's prepared)"""
    
#     async def pre_ask_question(flow_manager: FlowManager):
#         """Pre-action to inject question into context for TTS"""
#         current_index = flow_manager.state.get("current_question_index", 0)
#         current_number = flow_manager.state.get("current_question_number", 1)
#         total = flow_manager.state.get("total_questions", 0)
#         current_question = flow_manager.state.get("current_question_data", {})
        
#         # Format the question
#         formatted_question = format_question_for_display(current_question)
        
#         # Create the full message to speak
#         question_message = f"Question {current_number} of {total}. {formatted_question}. What's your answer?"
        
#         logger.info(f"🔊 Speaking question: {question_message[:100]}...")
        
#         # Push this text to be spoken by TTS
#         from pipecat.frames.frames import TextFrame
#         await flow_manager.push_frame(TextFrame(text=question_message))
    
#     async def handle_submit_answer(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[AnswerResult, NodeConfig]:
#         """Handler for submit_answer function"""
#         user_answer: str = args.get("answer", "").strip()
#         current_index = flow_manager.state.get("current_question_index", 0)
#         questions = flow_manager.state.get("questions", [])
#         score = flow_manager.state.get("score", 0)
        
#         logger.info(f"📝 Processing answer: '{user_answer}' for question {current_index + 1}")
        
#         if current_index >= len(questions):
#             logger.info("🎉 Quiz is complete")
#             return AnswerResult(
#                 question_index=current_index,
#                 user_answer=user_answer,
#                 is_correct=False,
#                 correct_answer="",
#                 score=score
#             ), create_quiz_complete_node()
        
#         current_question = flow_manager.state.get("current_question_data", {})
#         correct_answer = get_correct_answer(current_question)
        
#         # Simple answer checking
#         user_answer_lower = user_answer.strip().lower()
#         correct_answer_lower = correct_answer.lower()
        
#         # Check if answer is correct
#         is_correct = False
        
#         # Check letter answers
#         letters = ["a", "b", "c", "d", "e", "f"]
#         if user_answer_lower in letters:
#             index = letters.index(user_answer_lower)
#             options = current_question.get("question_options", [])
#             if index < len(options):
#                 selected_option = options[index]
#                 is_correct = selected_option.get("is_correct", False)
#         # Check text answers
#         elif user_answer_lower == correct_answer_lower:
#             is_correct = True
#         else:
#             # Partial match
#             is_correct = (user_answer_lower in correct_answer_lower or 
#                          correct_answer_lower in user_answer_lower)
        
#         # Update score
#         if is_correct:
#             score += 1
#             flow_manager.state["score"] = score
        
#         # Store result for feedback
#         flow_manager.state["last_answer_result"] = {
#             "is_correct": is_correct,
#             "correct_answer": correct_answer,
#             "user_answer": user_answer
#         }
        
#         # Move to next question
#         next_index = current_index + 1
#         flow_manager.state["current_question_index"] = next_index
        
#         result = AnswerResult(
#             question_index=current_index,
#             user_answer=user_answer,
#             is_correct=is_correct,
#             correct_answer=correct_answer,
#             score=score
#         )
        
#         if next_index < len(questions):
#             return result, create_answer_feedback_node()
#         else:
#             return result, create_quiz_complete_node()
    
#     submit_answer_func = FlowsFunctionSchema(
#         name="submit_answer",
#         handler=handle_submit_answer,
#         description="Submit the user's answer for the current question",
#         properties={
#             "answer": {
#                 "type": "string",
#                 "description": "The user's answer (can be letter like 'A', 'B', etc. or full text)"
#             }
#         },
#         required=["answer"],
#     )
    
#     return NodeConfig(
#         name="ask_question_display",
#         pre_actions=[pre_ask_question],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "The question has been asked. Wait for the user's answer."
#             }
#         ],
#         functions=[submit_answer_func],
#     )


# def create_answer_feedback_node() -> NodeConfig:
#     """Create the Answer Feedback node."""
    
#     async def pre_give_feedback(flow_manager: FlowManager):
#         """Pre-action to provide feedback via TTS"""
#         last_result = flow_manager.state.get("last_answer_result", {})
#         is_correct = last_result.get("is_correct", False)
#         correct_answer = last_result.get("correct_answer", "")
#         user_answer = last_result.get("user_answer", "")
#         score = flow_manager.state.get("score", 0)
#         total = flow_manager.state.get("total_questions", 0)
        
#         # Create feedback message
#         if is_correct:
#             feedback = f"That's right! {correct_answer} is correct! Great job!"
#         else:
#             feedback = f"Actually, the correct answer is {correct_answer}."
        
#         feedback += f" Your current score is {score} out of {total}. Ready for the next question?"
        
#         logger.info(f"🔊 Speaking feedback: {feedback}")
        
#         # Push feedback to TTS
#         from pipecat.frames.frames import TextFrame
#         await flow_manager.push_frame(TextFrame(text=feedback))
    
#     async def handle_next_question(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[QuestionResult, NodeConfig]:
#         """Handler for next_question function"""
#         logger.info("➡️ Moving to next question")
#         return QuestionResult(
#             question_index=flow_manager.state.get("current_question_index", 0),
#             question_text="Next question"
#         ), create_ask_question_node()
    
#     next_question_func = FlowsFunctionSchema(
#         name="next_question",
#         handler=handle_next_question,
#         description="Move to the next question",
#         properties={},
#         required=[],
#     )
    
#     return NodeConfig(
#         name="answer_feedback",
#         pre_actions=[pre_give_feedback],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "Feedback has been given. Use the next_question function when ready."
#             }
#         ],
#         functions=[next_question_func],
#     )


# def create_quiz_complete_node() -> NodeConfig:
#     """Create the Quiz Complete node."""
    
#     async def pre_announce_completion(flow_manager: FlowManager):
#         """Pre-action to announce quiz completion"""
#         message = "Congratulations! You've completed the quiz!"
        
#         logger.info(f"🔊 Speaking: {message}")
        
#         from pipecat.frames.frames import TextFrame
#         await flow_manager.push_frame(TextFrame(text=message))
    
#     async def handle_show_results(
#         args: FlowArgs, flow_manager: FlowManager
#     ) -> tuple[QuizCompleteResult, NodeConfig]:
#         """Handler for show_results function"""
#         total_questions = flow_manager.state.get("total_questions", 0)
#         score = flow_manager.state.get("score", 0)
#         score_percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
#         logger.info(f"🏁 Quiz complete! Score: {score}/{total_questions} ({score_percentage:.1f}%)")
        
#         return QuizCompleteResult(
#             total_questions=total_questions,
#             correct_answers=score,
#             score_percentage=score_percentage
#         ), create_goodbye_node()
    
#     show_results_func = FlowsFunctionSchema(
#         name="show_results",
#         handler=handle_show_results,
#         description="Show the final quiz results",
#         properties={},
#         required=[],
#     )
    
#     return NodeConfig(
#         name="quiz_complete",
#         pre_actions=[pre_announce_completion],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "The quiz is complete. Use the show_results function to display the final score."
#             }
#         ],
#         functions=[show_results_func],
#     )


# def create_goodbye_node() -> NodeConfig:
#     """Create the Goodbye node."""
    
#     async def pre_say_goodbye(flow_manager: FlowManager):
#         """Pre-action to say goodbye and share results"""
#         total_questions = flow_manager.state.get("total_questions", 0)
#         score = flow_manager.state.get("score", 0)
#         score_percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
#         # Create personalized goodbye message
#         if score_percentage >= 80:
#             message = f"Excellent work! You scored {score} out of {total_questions}, that's {score_percentage:.0f}%! You really know your stuff!"
#         elif score_percentage >= 60:
#             message = f"Good job! You scored {score} out of {total_questions}, that's {score_percentage:.0f}%. Keep it up!"
#         else:
#             message = f"Thanks for playing! You scored {score} out of {total_questions}, that's {score_percentage:.0f}%. Don't worry, practice makes perfect!"
        
#         message += " Thanks for playing the quiz. Goodbye!"
        
#         logger.info(f"🔊 Speaking goodbye: {message}")
        
#         from pipecat.frames.frames import TextFrame
#         await flow_manager.push_frame(TextFrame(text=message))
    
#     return NodeConfig(
#         name="goodbye",
#         pre_actions=[pre_say_goodbye],
#         task_messages=[
#             {
#                 "role": "system",
#                 "content": "The quiz has ended. The farewell message has been delivered."
#             }
#         ],
#         post_actions=[{"type": "end_conversation"}],
#     )


# # ============================================================================
# # Main Bot Function
# # ============================================================================

# async def run_bot(websocket_client, session_code: Optional[str] = None):
#     """Run the quiz bot with flow management"""
#     logger.info("🤖 Starting Quiz Bot")
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.5)),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create Gemini Multimodal Live LLM service
#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         config={
#             "system_instruction": """You are QuizMaster, a friendly, enthusiastic quiz host. 
#             You speak clearly and energetically at a moderate pace.
#             You always read questions and options aloud exactly as provided.
#             You provide encouraging feedback after each answer.
#             You maintain a positive and engaging tone throughout the quiz."""
#         }
#     )

#     # Create conversation context
#     context = LLMContext()
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),
#             rtvi,
#             context_aggregator.user(),
#             llm,
#             ws_transport.output(),
#             context_aggregator.assistant(),
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#             allow_interruptions=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Initialize flow manager
#     flow_manager = FlowManager(
#         task=task,
#         llm=llm,
#         context_aggregator=context_aggregator,
#         transport=ws_transport,
#     )

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Initialize the flow with welcome node
#         await flow_manager.initialize(create_welcome_node())

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise


# import os
# import aiohttp
# import json
# from typing import Dict, Any, Optional
# from datetime import datetime

# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.audio.vad.vad_analyzer import VADParams
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# from pipecat_flows import (
#     FlowArgs,
#     FlowManager,
#     FlowResult,
#     FlowsFunctionSchema,
#     NodeConfig,
# )

# load_dotenv(override=True)

# # Node API configuration
# NODE_API_URL = os.getenv("NODE_API_URL", "http://localhost:3000")


# # ============================================================================
# # Type Definitions for Function Results
# # ============================================================================

# class SessionValidationResult(FlowResult):
#     """Result type for session validation"""
#     valid: bool
#     questions: list[Dict[str, Any]]
#     total_questions: int


# class QuestionResult(FlowResult):
#     """Result type for question handling"""
#     question_index: int
#     question_text: str


# class AnswerResult(FlowResult):
#     """Result type for answer processing"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str
#     score: int


# class QuizCompleteResult(FlowResult):
#     """Result type for quiz completion"""
#     total_questions: int
#     correct_answers: int
#     score_percentage: float


# # ============================================================================
# # Helper Functions
# # ============================================================================

# async def get_questions(session_code: str) -> Dict[str, Any]:
#     """Get questions for a session"""
#     try:
#         url = f"{NODE_API_URL}/api/sessions/{session_code}/questions"
#         logger.info(f"🌐 Calling API: GET {url}")
        
#         timeout = aiohttp.ClientTimeout(total=10)
#         async with aiohttp.ClientSession(timeout=timeout) as session:
#             async with session.get(url) as response:
#                 logger.info(f"📊 API Response Status: {response.status}")
                
#                 if response.status == 200:
#                     data = await response.json()
#                     logger.info(f"✅ Got questions for session {session_code}")
                    
#                     # Check response format
#                     if isinstance(data, dict) and "data" in data:
#                         return {"status": "ok", "data": data["data"]}
#                     elif isinstance(data, list):
#                         return {"status": "ok", "data": data}
#                     else:
#                         logger.error(f"❌ Unexpected response format: {data}")
#                         return {"status": "error", "error": "Unexpected format"}
#                 else:
#                     error_text = await response.text()
#                     logger.error(f"❌ API error {response.status}: {error_text}")
#                     return {"status": "error", "error": f"API error: {response.status}"}
#     except Exception as e:
#         logger.error(f"❌ Error getting questions: {e}")
#         return {"status": "error", "error": str(e)}


# def format_question_for_speech(question_data: Dict[str, Any]) -> str:
#     """Format question for natural speech"""
#     question_text = question_data.get("question_text", "No question text")
#     options = question_data.get("question_options", [])
    
#     # Format options with letters for speech
#     letters = ["A", "B", "C", "D", "E", "F"]
#     formatted_options = []
    
#     for i, option in enumerate(options[:6]):
#         option_text = option.get("option_text", f"Option {i+1}")
#         formatted_options.append(f"{letters[i]}: {option_text}")
    
#     options_text = ", ".join(formatted_options)
    
#     return f"{question_text}. Your options are: {options_text}"


# def get_correct_answer(question_data: Dict[str, Any]) -> str:
#     """Get the correct answer for a question"""
#     options = question_data.get("question_options", [])
#     for option in options:
#         if option.get("is_correct", False):
#             return option.get("option_text", "")
#     return ""


# # ============================================================================
# # Function Handlers
# # ============================================================================

# async def validate_session(args: FlowArgs, flow_manager: FlowManager) -> tuple[SessionValidationResult, NodeConfig]:
#     """Validate session code and load questions"""
#     session_code: str = args["session_code"].strip().upper()
    
#     logger.info(f"🔍 Validating session: {session_code}")
    
#     # Get questions from API
#     questions_result = await get_questions(session_code)
    
#     if questions_result.get("status") == "ok" and "data" in questions_result:
#         questions = questions_result["data"]
        
#         if questions and len(questions) > 0:
#             logger.info(f"✅ Loaded {len(questions)} questions")
#             logger.info(f"Questions: {questions}")
            
#             # Store in flow manager state
#             flow_manager.state["questions"] = questions
#             flow_manager.state["current_question_index"] = 0
#             flow_manager.state["score"] = 0
#             flow_manager.state["total_questions"] = len(questions)
            
#             result = SessionValidationResult(valid=True, total_questions=len(questions), questions=questions)
#             next_node = create_ask_question_node()
#             return result, next_node
    
#     logger.error("❌ Session validation failed")
#     result = SessionValidationResult(valid=False, total_questions=0, questions=[])
#     return result, create_invalid_session_node()


# async def load_and_speak_question(args: FlowArgs, flow_manager: FlowManager) -> tuple[QuestionResult, NodeConfig]:
#     """Load the current question and prepare to speak it"""
#     question_index = flow_manager.state.get("current_question_index", 0)
#     questions = flow_manager.state.get("questions", [])
#     total = flow_manager.state.get("total_questions", 0)
    
#     if question_index >= len(questions):
#         logger.info("🎉 No more questions")
#         return QuestionResult(
#             question_index=question_index,
#             question_text="Complete"
#         ), create_quiz_complete_node()
    
#     current_question = questions[question_index]
#     question_num = question_index + 1
    
#     # Format question for speech
#     formatted_question = format_question_for_speech(current_question)
    
#     # Store formatted question in state so LLM can access it
#     flow_manager.state["current_formatted_question"] = formatted_question
#     flow_manager.state["current_question_number"] = question_num
    
#     logger.info(f"📝 Loaded question {question_num}/{total}: {current_question.get('question_text', '')[:50]}...")
    
#     result = QuestionResult(
#         question_index=question_index,
#         question_text=formatted_question
#     )
    
#     # Move to speaking node
#     next_node = create_speak_question_node()
    
#     return result, next_node


# async def submit_answer(args: FlowArgs, flow_manager: FlowManager) -> tuple[AnswerResult, NodeConfig]:
#     """Process user's answer"""
#     user_answer: str = args["answer"].strip()
    
#     # Get data from flow manager state
#     question_index: int = flow_manager.state.get("current_question_index", 0)
#     questions: list = flow_manager.state.get("questions", [])
#     score: int = flow_manager.state.get("score", 0)
    
#     logger.info(f"📝 Processing answer: '{user_answer}' for question {question_index + 1}")
    
#     current_question = questions[question_index]
#     correct_answer = get_correct_answer(current_question)
    
#     # Check if answer is correct
#     user_answer_lower = user_answer.lower()
#     correct_answer_lower = correct_answer.lower()
    
#     is_correct = False
#     letters = ["a", "b", "c", "d", "e", "f"]
    
#     # Check letter answers
#     if user_answer_lower in letters:
#         index = letters.index(user_answer_lower)
#         options = current_question.get("question_options", [])
#         if index < len(options):
#             selected_option = options[index]
#             is_correct = selected_option.get("is_correct", False)
#     # Check text answers
#     elif user_answer_lower == correct_answer_lower:
#         is_correct = True
#     else:
#         # Partial match
#         is_correct = (user_answer_lower in correct_answer_lower or 
#                      correct_answer_lower in user_answer_lower)
    
#     # Update score
#     if is_correct:
#         score += 1
#         flow_manager.state["score"] = score
    
#     # Store feedback data
#     flow_manager.state["last_is_correct"] = is_correct
#     flow_manager.state["last_correct_answer"] = correct_answer
    
#     result = AnswerResult(
#         question_index=question_index,
#         user_answer=user_answer,
#         is_correct=is_correct,
#         correct_answer=correct_answer,
#         score=score
#     )
    
#     # Move to next question
#     next_index = question_index + 1
#     flow_manager.state["current_question_index"] = next_index
    
#     # Determine next node
#     if next_index < len(questions):
#         next_node = create_feedback_node()
#     else:
#         next_node = create_quiz_complete_node()
    
#     return result, next_node


# async def continue_to_next_question(args: FlowArgs, flow_manager: FlowManager) -> tuple[QuestionResult, NodeConfig]:
#     """Continue to next question"""
#     next_index = flow_manager.state.get("current_question_index", 0)
    
#     logger.info(f"➡️ Moving to question {next_index + 1}")
    
#     result = QuestionResult(
#         question_index=next_index,
#         question_text="Moving to next question"
#     )
    
#     next_node = create_ask_question_node()
    
#     return result, next_node


# async def end_quiz(args: FlowArgs, flow_manager: FlowManager) -> tuple[QuizCompleteResult, NodeConfig]:
#     """End the quiz"""
#     score = flow_manager.state.get("score", 0)
#     total = flow_manager.state.get("total_questions", 0)
    
#     logger.info(f"🏁 Quiz complete! Score: {score}/{total}")
    
#     result = QuizCompleteResult(
#         total_questions=total,
#         correct_answers=score,
#         score_percentage=(score / total * 100) if total > 0 else 0
#     )
    
#     return result, create_goodbye_node()


# # ============================================================================
# # Function Schemas
# # ============================================================================

# validate_session_schema = FlowsFunctionSchema(
#     name="validate_session",
#     description="Validate the session code and load quiz questions",
#     properties={
#         "session_code": {
#             "type": "string",
#             "description": "The session code provided by the user (e.g., H6TU)"
#         }
#     },
#     required=["session_code"],
#     handler=validate_session,
# )

# load_and_speak_question_schema = FlowsFunctionSchema(
#     name="load_and_speak_question",
#     description="Load the current question and speak it to the user",
#     properties={},
#     required=[],
#     handler=load_and_speak_question,
# )

# submit_answer_schema = FlowsFunctionSchema(
#     name="submit_answer",
#     description="Submit the user's answer for the current question",
#     properties={
#         "answer": {
#             "type": "string",
#             "description": "The user's answer (letter A-F or full text)"
#         }
#     },
#     required=["answer"],
#     handler=submit_answer,
# )

# continue_schema = FlowsFunctionSchema(
#     name="continue_to_next_question",
#     description="Continue to the next question",
#     properties={},
#     required=[],
#     handler=continue_to_next_question,
# )

# end_quiz_schema = FlowsFunctionSchema(
#     name="end_quiz",
#     description="End the quiz and show final results",
#     properties={},
#     required=[],
#     handler=end_quiz,
# )


# # ============================================================================
# # Node Configurations
# # ============================================================================

# def create_welcome_node() -> NodeConfig:
#     """Create the welcome node"""
#     return {
#         "name": "welcome",
#         "role_messages": [
#             {
#                 "role": "system",
#                 "content": "You are QuizMaster, a friendly and enthusiastic quiz host. You speak clearly and energetically. Be encouraging and maintain positive energy throughout."
#             }
#         ],
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": "Welcome the user to the quiz! Introduce yourself as QuizMaster and ask them to provide their session code. Explain they need a valid session code to start."
#             }
#         ],
#         "functions": [validate_session_schema],
#     }


# def create_invalid_session_node() -> NodeConfig:
#     """Create node for invalid session"""
#     return {
#         "name": "invalid_session",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": "The session code is invalid or doesn't exist. Apologize politely and ask them to try again with a valid session code."
#             }
#         ],
#         "functions": [validate_session_schema],
#     }


# def create_ask_question_node() -> NodeConfig:
#     """Create node to prepare to ask a question"""
    
#     return {
#         "name": "ask_question",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """You need to ask the user a quiz question.

# Use the load_and_speak_question function to load and prepare the next question."""
#             }
#         ],
#         "functions": [load_and_speak_question_schema],
#     }


# def create_speak_question_node() -> NodeConfig:
#     """Create node to actually speak the question"""
    
#     return {
#         "name": "speak_question",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Now speak the quiz question to the user. The question has been loaded into the state:

# Question number: {current_question_number}
# Total questions: {total_questions}
# Formatted question: {current_formatted_question}

# SPEAK THIS OUT LOUD:
# "Question {current_question_number} of {total_questions}. {current_formatted_question}. What's your answer?"

# Make sure to read ALL the options clearly. The user is LISTENING, not reading."""
#             }
#         ],
#         "functions": [submit_answer_schema],
#     }


# def create_feedback_node() -> NodeConfig:
#     """Create feedback node - uses flow manager state"""
    
#     return {
#         "name": "feedback",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Provide feedback on the user's answer using the flow state:
# - last_is_correct: {last_is_correct}
# - last_correct_answer: {last_correct_answer}
# - score: {score}
# - total_questions: {total_questions}

# If last_is_correct is True:
#   Say: "That's right! [last_correct_answer] is correct! Great job!"
# If last_is_correct is False:
#   Say: "Actually, the correct answer is [last_correct_answer]."

# Then say: "Your current score is [score] out of [total_questions]."

# Ask if they're ready for the next question, then use the continue_to_next_question function."""
#             }
#         ],
#         "functions": [continue_schema],
#     }


# def create_quiz_complete_node() -> NodeConfig:
#     """Create quiz completion node - uses flow manager state"""
    
#     return {
#         "name": "quiz_complete",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Congratulations! The quiz is complete!

# Use the flow state to get:
# - score: {score}
# - total_questions: {total_questions}

# Calculate percentage = (score / total_questions) * 100

# If percentage >= 80:
#   Say: "Excellent work! You scored [score] out of [total_questions]! That's [percentage] percent!"
# If percentage >= 60:
#   Say: "Good job! You scored [score] out of [total_questions]. That's [percentage] percent."
# Else:
#   Say: "Thanks for playing! You scored [score] out of [total_questions]. That's [percentage] percent. Practice makes perfect!"

# Ask if they'd like to end the conversation, then use the end_quiz function."""
#             }
#         ],
#         "functions": [end_quiz_schema],
#     }


# def create_goodbye_node() -> NodeConfig:
#     """Create goodbye node"""
#     return {
#         "name": "goodbye",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": "Thank them warmly for playing the quiz and say goodbye!"
#             }
#         ],
#         "post_actions": [{"type": "end_conversation"}],
#     }


# # ============================================================================
# # Main Bot Function
# # ============================================================================

# async def run_bot(websocket_client, session_code: Optional[str] = None):
#     """Run the quiz bot with flow management"""
#     logger.info("🤖 Starting Quiz Bot")
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.5)),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create Gemini Multimodal Live LLM service
#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         config={
#             "system_instruction": """You are QuizMaster, a friendly, enthusiastic quiz host. 
#             You speak clearly and energetically at a moderate pace.
#             You always read questions and options aloud exactly as provided.
#             You provide encouraging feedback after each answer.
#             You maintain a positive and engaging tone throughout the quiz.
#             This is a voice conversation - avoid special characters and emojis."""
#         }
#     )

#     # Create conversation context
#     context = LLMContext()
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),
#             rtvi,
#             context_aggregator.user(),
#             llm,
#             ws_transport.output(),
#             context_aggregator.assistant(),
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#             allow_interruptions=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Initialize flow manager
#     flow_manager = FlowManager(
#         task=task,
#         llm=llm,
#         context_aggregator=context_aggregator,
#         transport=ws_transport,
#     )

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Initialize the flow with welcome node
#         await flow_manager.initialize(create_welcome_node())

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise

# import os
# import aiohttp
# import json
# from typing import Dict, Any, Optional
# from datetime import datetime

# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.audio.vad.vad_analyzer import VADParams
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# from pipecat_flows import (
#     FlowArgs,
#     FlowManager,
#     FlowResult,
#     FlowsFunctionSchema,
#     NodeConfig,
# )

# load_dotenv(override=True)

# # Node API configuration
# NODE_API_URL = os.getenv("NODE_API_URL", "http://localhost:3000")


# # ============================================================================
# # Type Definitions for Function Results
# # ============================================================================

# class SessionValidationResult(FlowResult):
#     """Result type for session validation"""
#     valid: bool
#     questions: list[Dict[str, Any]]
#     total_questions: int
#     roll_number: str = ""
#     session_code: str = ""


# class QuestionResult(FlowResult):
#     """Result type for question handling"""
#     question_index: int
#     question_text: str


# class AnswerResult(FlowResult):
#     """Result type for answer processing"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str
#     score: int


# class QuizCompleteResult(FlowResult):
#     """Result type for quiz completion"""
#     total_questions: int
#     correct_answers: int
#     score_percentage: float


# class MissingInfoResult(FlowResult):
#     """Result type for missing information collection"""
#     missing_fields: list[str]
#     collected_data: Dict[str, str]


# # ============================================================================
# # Helper Functions
# # ============================================================================

# async def get_questions(session_code: str, roll_number: str) -> Dict[str, Any]:
#     """Get questions for a session with roll number"""
#     try:
#         url = f"{NODE_API_URL}/api/sessions/{session_code}/questions"
#         params = {"rollNumber": roll_number} if roll_number else None
#         logger.info(f"🌐 Calling API: GET {url} with roll number: {roll_number}")
        
#         timeout = aiohttp.ClientTimeout(total=10)
#         async with aiohttp.ClientSession(timeout=timeout) as session:
#             async with session.get(url, params=params) as response:
#                 logger.info(f"📊 API Response Status: {response.status}")
                
#                 if response.status == 200:
#                     data = await response.json()
#                     logger.info(f"✅ Got questions for session {session_code}")
                    
#                     # Check response format
#                     if isinstance(data, dict) and "data" in data:
#                         return {"status": "ok", "data": data["data"]}
#                     elif isinstance(data, list):
#                         return {"status": "ok", "data": data}
#                     else:
#                         logger.error(f"❌ Unexpected response format: {data}")
#                         return {"status": "error", "error": "Unexpected format"}
#                 elif response.status == 404:
#                     return {"status": "error", "error": "Session not found or invalid roll number"}
#                 elif response.status == 403:
#                     return {"status": "error", "error": "Access denied - invalid credentials"}
#                 else:
#                     error_text = await response.text()
#                     logger.error(f"❌ API error {response.status}: {error_text}")
#                     return {"status": "error", "error": f"API error: {response.status}"}
#     except Exception as e:
#         logger.error(f"❌ Error getting questions: {e}")
#         return {"status": "error", "error": str(e)}


# def format_question_for_speech(question_data: Dict[str, Any]) -> str:
#     """Format question for natural speech"""
#     question_text = question_data.get("question_text", "No question text")
#     options = question_data.get("question_options", [])
    
#     # Format options with letters for speech
#     letters = ["A", "B", "C", "D", "E", "F"]
#     formatted_options = []
    
#     for i, option in enumerate(options[:6]):
#         option_text = option.get("option_text", f"Option {i+1}")
#         formatted_options.append(f"{letters[i]}: {option_text}")
    
#     options_text = ", ".join(formatted_options)
    
#     return f"{question_text}. Your options are: {options_text}"


# def get_correct_answer(question_data: Dict[str, Any]) -> str:
#     """Get the correct answer for a question"""
#     options = question_data.get("question_options", [])
#     for option in options:
#         if option.get("is_correct", False):
#             return option.get("option_text", "")
#     return ""


# # ============================================================================
# # Function Handlers
# # ============================================================================

# async def collect_missing_info(args: FlowArgs, flow_manager: FlowManager) -> tuple[MissingInfoResult, NodeConfig]:
#     """Collect missing session info (session code or roll number)"""
#     session_code = args.get("session_code", "").strip().upper()
#     roll_number = args.get("roll_number", "").strip()
    
#     logger.info(f"📝 Collecting info - Session: {session_code}, Roll: {roll_number}")
    
#     # Store what we have
#     if session_code:
#         flow_manager.state["session_code"] = session_code
#     if roll_number:
#         flow_manager.state["roll_number"] = roll_number
    
#     # Check what's missing
#     missing = []
#     if not session_code:
#         missing.append("session code")
#     if not roll_number:
#         missing.append("roll number")
    
#     result = MissingInfoResult(
#         missing_fields=missing,
#         collected_data={
#             "session_code": session_code,
#             "roll_number": roll_number
#         }
#     )
    
#     if not missing:
#         # Both provided, proceed to validation
#         logger.info("✅ Both session code and roll number provided, validating...")
#         return await validate_session(args, flow_manager)
    
#     # Determine which node to go to based on what's missing
#     if len(missing) == 2:
#         logger.info("❌ Missing both session code and roll number")
#         return result, create_welcome_node()
#     elif "session code" in missing:
#         logger.info("❌ Missing session code")
#         return result, create_ask_session_code_node()
#     else:  # missing roll number
#         logger.info("❌ Missing roll number")
#         return result, create_ask_roll_number_node()


# async def validate_session(args: FlowArgs, flow_manager: FlowManager) -> tuple[SessionValidationResult, NodeConfig]:
#     """Validate session code and load questions"""
#     # Get from args first, then fall back to state
#     session_code: str = args.get("session_code", "").strip().upper()
#     roll_number: str = args.get("roll_number", "").strip()
    
#     # If not in args, check state
#     if not session_code:
#         session_code = flow_manager.state.get("session_code", "")
#     if not roll_number:
#         roll_number = flow_manager.state.get("roll_number", "")
    
#     logger.info(f"🔍 Validating session: {session_code} with roll number: {roll_number}")
    
#     if not session_code or not roll_number:
#         logger.error("❌ Missing session code or roll number")
#         result = SessionValidationResult(
#             valid=False, 
#             total_questions=0, 
#             questions=[], 
#             roll_number=roll_number,
#             session_code=session_code
#         )
#         flow_manager.state["last_error"] = "Please provide both session code and roll number"
#         return result, create_invalid_session_node()
    
#     # Get questions from API with roll number
#     questions_result = await get_questions(session_code, roll_number)
    
#     if questions_result.get("status") == "ok" and "data" in questions_result:
#         questions = questions_result["data"]
        
#         if questions and len(questions) > 0:
#             logger.info(f"✅ Loaded {len(questions)} questions for roll number {roll_number}")
            
#             # Store in flow manager state
#             flow_manager.state["questions"] = questions
#             flow_manager.state["current_question_index"] = 0
#             flow_manager.state["score"] = 0
#             flow_manager.state["total_questions"] = len(questions)
#             flow_manager.state["roll_number"] = roll_number
#             flow_manager.state["session_code"] = session_code
            
#             result = SessionValidationResult(
#                 valid=True, 
#                 total_questions=len(questions), 
#                 questions=questions,
#                 roll_number=roll_number,
#                 session_code=session_code
#             )
#             next_node = create_ask_question_node()
#             return result, next_node
    
#     error_msg = questions_result.get("error", "Session validation failed")
#     logger.error(f"❌ Session validation failed: {error_msg}")
#     flow_manager.state["last_error"] = error_msg
#     result = SessionValidationResult(
#         valid=False, 
#         total_questions=0, 
#         questions=[],
#         roll_number=roll_number,
#         session_code=session_code
#     )
#     return result, create_invalid_session_node()


# async def load_and_speak_question(args: FlowArgs, flow_manager: FlowManager) -> tuple[QuestionResult, NodeConfig]:
#     """Load the current question and prepare to speak it"""
#     question_index = flow_manager.state.get("current_question_index", 0)
#     questions = flow_manager.state.get("questions", [])
#     total = flow_manager.state.get("total_questions", 0)
    
#     if question_index >= len(questions):
#         logger.info("🎉 No more questions")
#         return QuestionResult(
#             question_index=question_index,
#             question_text="Complete"
#         ), create_quiz_complete_node()
    
#     current_question = questions[question_index]
#     question_num = question_index + 1
    
#     # Format question for speech
#     formatted_question = format_question_for_speech(current_question)
    
#     # Store formatted question in state so LLM can access it
#     flow_manager.state["current_formatted_question"] = formatted_question
#     flow_manager.state["current_question_number"] = question_num
    
#     logger.info(f"📝 Loaded question {question_num}/{total}: {current_question.get('question_text', '')[:50]}...")
    
#     result = QuestionResult(
#         question_index=question_index,
#         question_text=formatted_question
#     )
    
#     # Move to speaking node
#     next_node = create_speak_question_node()
    
#     return result, next_node


# async def submit_answer(args: FlowArgs, flow_manager: FlowManager) -> tuple[AnswerResult, NodeConfig]:
#     """Process user's answer"""
#     user_answer: str = args["answer"].strip()
    
#     # Get data from flow manager state
#     question_index: int = flow_manager.state.get("current_question_index", 0)
#     questions: list = flow_manager.state.get("questions", [])
#     score: int = flow_manager.state.get("score", 0)
    
#     logger.info(f"📝 Processing answer: '{user_answer}' for question {question_index + 1}")
    
#     current_question = questions[question_index]
#     correct_answer = get_correct_answer(current_question)
    
#     # Check if answer is correct
#     user_answer_lower = user_answer.lower()
#     correct_answer_lower = correct_answer.lower()
    
#     is_correct = False
#     letters = ["a", "b", "c", "d", "e", "f"]
    
#     # Check letter answers
#     if user_answer_lower in letters:
#         index = letters.index(user_answer_lower)
#         options = current_question.get("question_options", [])
#         if index < len(options):
#             selected_option = options[index]
#             is_correct = selected_option.get("is_correct", False)
#     # Check text answers
#     elif user_answer_lower == correct_answer_lower:
#         is_correct = True
#     else:
#         # Partial match
#         is_correct = (user_answer_lower in correct_answer_lower or 
#                      correct_answer_lower in user_answer_lower)
    
#     # Update score
#     if is_correct:
#         score += 1
#         flow_manager.state["score"] = score
    
#     # Store feedback data
#     flow_manager.state["last_is_correct"] = is_correct
#     flow_manager.state["last_correct_answer"] = correct_answer
    
#     result = AnswerResult(
#         question_index=question_index,
#         user_answer=user_answer,
#         is_correct=is_correct,
#         correct_answer=correct_answer,
#         score=score
#     )
    
#     # Move to next question
#     next_index = question_index + 1
#     flow_manager.state["current_question_index"] = next_index
    
#     # Determine next node
#     if next_index < len(questions):
#         next_node = create_feedback_node()
#     else:
#         next_node = create_quiz_complete_node()
    
#     return result, next_node


# async def continue_to_next_question(args: FlowArgs, flow_manager: FlowManager) -> tuple[QuestionResult, NodeConfig]:
#     """Continue to next question"""
#     next_index = flow_manager.state.get("current_question_index", 0)
    
#     logger.info(f"➡️ Moving to question {next_index + 1}")
    
#     result = QuestionResult(
#         question_index=next_index,
#         question_text="Moving to next question"
#     )
    
#     next_node = create_ask_question_node()
    
#     return result, next_node


# async def end_quiz(args: FlowArgs, flow_manager: FlowManager) -> tuple[QuizCompleteResult, NodeConfig]:
#     """End the quiz"""
#     score = flow_manager.state.get("score", 0)
#     total = flow_manager.state.get("total_questions", 0)
    
#     logger.info(f"🏁 Quiz complete! Score: {score}/{total}")
    
#     result = QuizCompleteResult(
#         total_questions=total,
#         correct_answers=score,
#         score_percentage=(score / total * 100) if total > 0 else 0
#     )
    
#     return result, create_goodbye_node()


# # ============================================================================
# # Function Schemas
# # ============================================================================

# collect_missing_info_schema = FlowsFunctionSchema(
#     name="collect_missing_info",
#     description="Collect missing session information (session code or roll number)",
#     properties={
#         "session_code": {
#             "type": "string",
#             "description": "The session code provided by the user (e.g., H6TU)"
#         },
#         "roll_number": {
#             "type": "string",
#             "description": "The user's roll number (student ID)"
#         }
#     },
#     required=[],  # Not required since we might have partial info
#     handler=collect_missing_info,
# )

# validate_session_schema = FlowsFunctionSchema(
#     name="validate_session",
#     description="Validate the session code and roll number and load quiz questions",
#     properties={
#         "session_code": {
#             "type": "string",
#             "description": "The session code provided by the user (e.g., H6TU)"
#         },
#         "roll_number": {
#             "type": "string",
#             "description": "The user's roll number (student ID)"
#         }
#     },
#     required=["session_code", "roll_number"],
#     handler=validate_session,
# )

# load_and_speak_question_schema = FlowsFunctionSchema(
#     name="load_and_speak_question",
#     description="Load the current question and speak it to the user",
#     properties={},
#     required=[],
#     handler=load_and_speak_question,
# )

# submit_answer_schema = FlowsFunctionSchema(
#     name="submit_answer",
#     description="Submit the user's answer for the current question",
#     properties={
#         "answer": {
#             "type": "string",
#             "description": "The user's answer (letter A-F or full text)"
#         }
#     },
#     required=["answer"],
#     handler=submit_answer,
# )

# continue_schema = FlowsFunctionSchema(
#     name="continue_to_next_question",
#     description="Continue to the next question",
#     properties={},
#     required=[],
#     handler=continue_to_next_question,
# )

# end_quiz_schema = FlowsFunctionSchema(
#     name="end_quiz",
#     description="End the quiz and show final results",
#     properties={},
#     required=[],
#     handler=end_quiz,
# )


# # ============================================================================
# # Node Configurations
# # ============================================================================

# def create_welcome_node() -> NodeConfig:
#     """Create the welcome node"""
#     return {
#         "name": "welcome",
#         "role_messages": [
#             {
#                 "role": "system",
#                 "content": "You are QuizMaster, a friendly and enthusiastic quiz host. You speak clearly and energetically. Be encouraging and maintain positive energy throughout."
#             }
#         ],
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Welcome the user to the quiz! Introduce yourself as QuizMaster and explain you need two things to start:
# 1. Their session code (like H6TU)
# 2. Their roll number

# Start by asking for the session code first. You can say something like:
# "Welcome to QuizMaster! I'm excited to host your quiz today. To get started, I'll need two pieces of information. First, what's your session code?"

# Once they provide the session code, ask for their roll number. Then use the collect_missing_info function with both pieces of information."""
#             }
#         ],
#         "functions": [collect_missing_info_schema],
#     }


# def create_ask_session_code_node() -> NodeConfig:
#     """Create node to ask for session code"""
#     return {
#         "name": "ask_session_code",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Ask the user for their session code. It's usually a 4-character code like H6TU.
# Say something like: "Great, now I need your session code. What's your session code?"

# Once they provide it, use the collect_missing_info function with the session code."""
#             }
#         ],
#         "functions": [collect_missing_info_schema],
#     }


# def create_ask_roll_number_node() -> NodeConfig:
#     """Create node to ask for roll number"""
#     return {
#         "name": "ask_roll_number",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Ask the user for their roll number (student ID).
# Say something like: "Thank you! Now I need your roll number. What's your roll number?"

# Once they provide it, use the collect_missing_info function with the roll number."""
#             }
#         ],
#         "functions": [collect_missing_info_schema],
#     }


# def create_invalid_session_node() -> NodeConfig:
#     """Create node for invalid session"""
    
#     return {
#         "name": "invalid_session",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """The session validation failed. Possible reasons:
# 1. Incorrect session code
# 2. Incorrect roll number
# 3. Session doesn't exist
# 4. Roll number not authorized for this session

# Check flow state for error details: {last_error}

# Politely inform the user there was an issue. Say something like:
# "I'm sorry, but I couldn't validate your credentials. Let's try again."

# Ask them to provide both their session code and roll number again, then use the collect_missing_info function."""
#             }
#         ],
#         "functions": [collect_missing_info_schema],
#     }


# def create_ask_question_node() -> NodeConfig:
#     """Create node to prepare to ask a question"""
    
#     return {
#         "name": "ask_question",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """You're about to ask the user a quiz question.

# First, acknowledge their successful login. Say something like:
# "Perfect! Now let's start the quiz. Good luck!"

# Then use the load_and_speak_question function to load and prepare the next question."""
#             }
#         ],
#         "functions": [load_and_speak_question_schema],
#     }


# def create_speak_question_node() -> NodeConfig:
#     """Create node to actually speak the question"""
    
#     return {
#         "name": "speak_question",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Now speak the quiz question to the user. The question has been loaded into the state:

# Question number: {current_question_number}
# Total questions: {total_questions}
# Formatted question: {current_formatted_question}

# SPEAK THIS OUT LOUD:
# "Question {current_question_number} of {total_questions}. {current_formatted_question}. What's your answer?"

# Make sure to read ALL the options clearly. The user is LISTENING, not reading."""
#             }
#         ],
#         "functions": [submit_answer_schema],
#     }


# def create_feedback_node() -> NodeConfig:
#     """Create feedback node - uses flow manager state"""
    
#     return {
#         "name": "feedback",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Provide feedback on the user's answer using the flow state:
# - last_is_correct: {last_is_correct}
# - last_correct_answer: {last_correct_answer}
# - score: {score}
# - total_questions: {total_questions}

# If last_is_correct is True:
#   Say: "That's right! [last_correct_answer] is correct! Great job!"
# If last_is_correct is False:
#   Say: "Actually, the correct answer is [last_correct_answer]."

# Then say: "Your current score is [score] out of [total_questions]."

# Ask if they're ready for the next question, then use the continue_to_next_question function."""
#             }
#         ],
#         "functions": [continue_schema],
#     }


# def create_quiz_complete_node() -> NodeConfig:
#     """Create quiz completion node - uses flow manager state"""
    
#     return {
#         "name": "quiz_complete",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Congratulations! The quiz is complete!

# Use the flow state to get:
# - score: {score}
# - total_questions: {total_questions}

# Calculate percentage = (score / total_questions) * 100

# If percentage >= 80:
#   Say: "Excellent work! You scored [score] out of [total_questions]! That's [percentage] percent!"
# If percentage >= 60:
#   Say: "Good job! You scored [score] out of [total_questions]. That's [percentage] percent."
# Else:
#   Say: "Thanks for playing! You scored [score] out of [total_questions]. That's [percentage] percent. Practice makes perfect!"

# Ask if they'd like to end the conversation, then use the end_quiz function."""
#             }
#         ],
#         "functions": [end_quiz_schema],
#     }


# def create_goodbye_node() -> NodeConfig:
#     """Create goodbye node"""
#     return {
#         "name": "goodbye",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": "Thank them warmly for playing the quiz and say goodbye! You can say something like: 'Thank you for playing! Have a great day!'"
#             }
#         ],
#         "post_actions": [{"type": "end_conversation"}],
#     }


# # ============================================================================
# # Main Bot Function
# # ============================================================================

# async def run_bot(websocket_client, session_code: Optional[str] = None):
#     """Run the quiz bot with flow management"""
#     logger.info("🤖 Starting Quiz Bot")
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.5)),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create Gemini Multimodal Live LLM service
#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         config={
#             "system_instruction": """You are QuizMaster, a friendly, enthusiastic quiz host. 
#             You speak clearly and energetically at a moderate pace.
#             You always read questions and options aloud exactly as provided.
#             You provide encouraging feedback after each answer.
#             You maintain a positive and engaging tone throughout the quiz.
#             This is a voice conversation - avoid special characters and emojis."""
#         }
#     )

#     # Create conversation context
#     context = LLMContext()
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),
#             rtvi,
#             context_aggregator.user(),
#             llm,
#             ws_transport.output(),
#             context_aggregator.assistant(),
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#             allow_interruptions=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Initialize flow manager
#     flow_manager = FlowManager(
#         task=task,
#         llm=llm,
#         context_aggregator=context_aggregator,
#         transport=ws_transport,
#     )

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Initialize the flow with welcome node
#         await flow_manager.initialize(create_welcome_node())

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise

# import os
# import aiohttp
# import json
# from typing import Dict, Any, Optional
# from datetime import datetime

# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.audio.vad.vad_analyzer import VADParams
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# from pipecat_flows import (
#     FlowArgs,
#     FlowManager,
#     FlowResult,
#     FlowsFunctionSchema,
#     NodeConfig,
# )

# load_dotenv(override=True)

# # Node API configuration
# NODE_API_URL = os.getenv("NODE_API_URL", "http://localhost:3000")


# # ============================================================================
# # Type Definitions for Function Results
# # ============================================================================

# class SessionValidationResult(FlowResult):
#     """Result type for session validation"""
#     valid: bool
#     questions: list[Dict[str, Any]]
#     total_questions: int
#     roll_number: str = ""
#     session_code: str = ""


# class QuestionResult(FlowResult):
#     """Result type for question handling"""
#     question_index: int
#     question_text: str


# class AnswerResult(FlowResult):
#     """Result type for answer processing"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str
#     score: int


# class QuizCompleteResult(FlowResult):
#     """Result type for quiz completion"""
#     total_questions: int
#     correct_answers: int
#     score_percentage: float


# class MissingInfoResult(FlowResult):
#     """Result type for missing information collection"""
#     missing_fields: list[str]
#     collected_data: Dict[str, str]


# class ProceedResult(FlowResult):
#     """Result type for proceed confirmation"""
#     wants_to_proceed: bool
#     user_response: str


# # ============================================================================
# # Helper Functions
# # ============================================================================

# async def get_questions(session_code: str, roll_number: str) -> Dict[str, Any]:
#     """Get questions for a session with roll number"""
#     try:
#         url = f"{NODE_API_URL}/api/sessions/{session_code}/questions"
#         params = {"rollNumber": roll_number} if roll_number else None
#         logger.info(f"🌐 Calling API: GET {url} with roll number: {roll_number}")
        
#         timeout = aiohttp.ClientTimeout(total=10)
#         async with aiohttp.ClientSession(timeout=timeout) as session:
#             async with session.get(url, params=params) as response:
#                 logger.info(f"📊 API Response Status: {response.status}")
                
#                 if response.status == 200:
#                     data = await response.json()
#                     logger.info(f"✅ Got questions for session {session_code}")
                    
#                     # Check response format
#                     if isinstance(data, dict) and "data" in data:
#                         return {"status": "ok", "data": data["data"]}
#                     elif isinstance(data, list):
#                         return {"status": "ok", "data": data}
#                     else:
#                         logger.error(f"❌ Unexpected response format: {data}")
#                         return {"status": "error", "error": "Unexpected format"}
#                 elif response.status == 404:
#                     return {"status": "error", "error": "Session not found or invalid roll number"}
#                 elif response.status == 403:
#                     return {"status": "error", "error": "Access denied - invalid credentials"}
#                 else:
#                     error_text = await response.text()
#                     logger.error(f"❌ API error {response.status}: {error_text}")
#                     return {"status": "error", "error": f"API error: {response.status}"}
#     except Exception as e:
#         logger.error(f"❌ Error getting questions: {e}")
#         return {"status": "error", "error": str(e)}


# def format_question_for_speech(question_data: Dict[str, Any]) -> str:
#     """Format question for natural speech"""
#     question_text = question_data.get("question_text", "No question text")
#     options = question_data.get("question_options", [])
    
#     # Format options with letters for speech
#     letters = ["A", "B", "C", "D", "E", "F"]
#     formatted_options = []
    
#     for i, option in enumerate(options[:6]):
#         option_text = option.get("option_text", f"Option {i+1}")
#         formatted_options.append(f"{letters[i]}: {option_text}")
    
#     options_text = ", ".join(formatted_options)
    
#     return f"{question_text}. Your options are: {options_text}"


# def get_correct_answer(question_data: Dict[str, Any]) -> str:
#     """Get the correct answer for a question"""
#     options = question_data.get("question_options", [])
#     for option in options:
#         if option.get("is_correct", False):
#             return option.get("option_text", "")
#     return ""


# # ============================================================================
# # Function Handlers
# # ============================================================================

# async def collect_missing_info(args: FlowArgs, flow_manager: FlowManager) -> tuple[MissingInfoResult, NodeConfig]:
#     """Collect missing session info (session code or roll number)"""
#     session_code = args.get("session_code", "").strip().upper()
#     roll_number = args.get("roll_number", "").strip()
    
#     logger.info(f"📝 Collecting info - Session: {session_code}, Roll: {roll_number}")
    
#     # Store what we have
#     if session_code:
#         flow_manager.state["session_code"] = session_code
#     if roll_number:
#         flow_manager.state["roll_number"] = roll_number
    
#     # Check what's missing
#     missing = []
#     if not session_code:
#         missing.append("session code")
#     if not roll_number:
#         missing.append("roll number")
    
#     result = MissingInfoResult(
#         missing_fields=missing,
#         collected_data={
#             "session_code": session_code,
#             "roll_number": roll_number
#         }
#     )
    
#     if not missing:
#         # Both provided, proceed to validation
#         logger.info("✅ Both session code and roll number provided, validating...")
#         return await validate_session(args, flow_manager)
    
#     # Determine which node to go to based on what's missing
#     if len(missing) == 2:
#         logger.info("❌ Missing both session code and roll number")
#         return result, create_welcome_node()
#     elif "session code" in missing:
#         logger.info("❌ Missing session code")
#         return result, create_ask_session_code_node()
#     else:  # missing roll number
#         logger.info("❌ Missing roll number")
#         return result, create_ask_roll_number_node()


# async def validate_session(args: FlowArgs, flow_manager: FlowManager) -> tuple[SessionValidationResult, NodeConfig]:
#     """Validate session code and load questions"""
#     # Get from args first, then fall back to state
#     session_code: str = args.get("session_code", "").strip().upper()
#     roll_number: str = args.get("roll_number", "").strip()
    
#     # If not in args, check state
#     if not session_code:
#         session_code = flow_manager.state.get("session_code", "")
#     if not roll_number:
#         roll_number = flow_manager.state.get("roll_number", "")
    
#     logger.info(f"🔍 Validating session: {session_code} with roll number: {roll_number}")
    
#     if not session_code or not roll_number:
#         logger.error("❌ Missing session code or roll number")
#         result = SessionValidationResult(
#             valid=False, 
#             total_questions=0, 
#             questions=[], 
#             roll_number=roll_number,
#             session_code=session_code
#         )
#         flow_manager.state["last_error"] = "Please provide both session code and roll number"
#         return result, create_invalid_session_node()
    
#     # Get questions from API with roll number
#     questions_result = await get_questions(session_code, roll_number)
    
#     if questions_result.get("status") == "ok" and "data" in questions_result:
#         questions = questions_result["data"]
        
#         if questions and len(questions) > 0:
#             logger.info(f"✅ Loaded {len(questions)} questions for roll number {roll_number}")
            
#             # Store in flow manager state
#             flow_manager.state["questions"] = questions
#             flow_manager.state["current_question_index"] = 0
#             flow_manager.state["score"] = 0
#             flow_manager.state["total_questions"] = len(questions)
#             flow_manager.state["roll_number"] = roll_number
#             flow_manager.state["session_code"] = session_code
            
#             result = SessionValidationResult(
#                 valid=True, 
#                 total_questions=len(questions), 
#                 questions=questions,
#                 roll_number=roll_number,
#                 session_code=session_code
#             )
#             next_node = create_ask_question_node()
#             return result, next_node
    
#     error_msg = questions_result.get("error", "Session validation failed")
#     logger.error(f"❌ Session validation failed: {error_msg}")
#     flow_manager.state["last_error"] = error_msg
#     result = SessionValidationResult(
#         valid=False, 
#         total_questions=0, 
#         questions=[],
#         roll_number=roll_number,
#         session_code=session_code
#     )
#     return result, create_invalid_session_node()


# async def load_and_speak_question(args: FlowArgs, flow_manager: FlowManager) -> tuple[QuestionResult, NodeConfig]:
#     """Load the current question and prepare to speak it"""
#     question_index = flow_manager.state.get("current_question_index", 0)
#     questions = flow_manager.state.get("questions", [])
#     total = flow_manager.state.get("total_questions", 0)
    
#     if question_index >= len(questions):
#         logger.info("🎉 No more questions")
#         return QuestionResult(
#             question_index=question_index,
#             question_text="Complete"
#         ), create_quiz_complete_node()
    
#     current_question = questions[question_index]
#     question_num = question_index + 1
    
#     # Format question for speech
#     formatted_question = format_question_for_speech(current_question)
    
#     # Store formatted question in state so LLM can access it
#     flow_manager.state["current_formatted_question"] = formatted_question
#     flow_manager.state["current_question_number"] = question_num
    
#     logger.info(f"📝 Loaded question {question_num}/{total}: {current_question.get('question_text', '')[:50]}...")
    
#     result = QuestionResult(
#         question_index=question_index,
#         question_text=formatted_question
#     )
    
#     # Move to speaking node
#     next_node = create_speak_question_node()
    
#     return result, next_node


# async def submit_answer(args: FlowArgs, flow_manager: FlowManager) -> tuple[AnswerResult, NodeConfig]:
#     """Process user's answer"""
#     user_answer: str = args["answer"].strip()
    
#     # Get data from flow manager state
#     question_index: int = flow_manager.state.get("current_question_index", 0)
#     questions: list = flow_manager.state.get("questions", [])
#     score: int = flow_manager.state.get("score", 0)
    
#     logger.info(f"📝 Processing answer: '{user_answer}' for question {question_index + 1}")
    
#     current_question = questions[question_index]
#     correct_answer = get_correct_answer(current_question)
    
#     # Check if answer is correct
#     user_answer_lower = user_answer.lower()
#     correct_answer_lower = correct_answer.lower()
    
#     is_correct = False
#     letters = ["a", "b", "c", "d", "e", "f"]
    
#     # Check letter answers
#     if user_answer_lower in letters:
#         index = letters.index(user_answer_lower)
#         options = current_question.get("question_options", [])
#         if index < len(options):
#             selected_option = options[index]
#             is_correct = selected_option.get("is_correct", False)
#     # Check text answers
#     elif user_answer_lower == correct_answer_lower:
#         is_correct = True
#     else:
#         # Partial match
#         is_correct = (user_answer_lower in correct_answer_lower or 
#                      correct_answer_lower in user_answer_lower)
    
#     # Update score
#     if is_correct:
#         score += 1
#         flow_manager.state["score"] = score
    
#     # Store feedback data
#     flow_manager.state["last_is_correct"] = is_correct
#     flow_manager.state["last_correct_answer"] = correct_answer
    
#     result = AnswerResult(
#         question_index=question_index,
#         user_answer=user_answer,
#         is_correct=is_correct,
#         correct_answer=correct_answer,
#         score=score
#     )
    
#     # Move to next question
#     next_index = question_index + 1
#     flow_manager.state["current_question_index"] = next_index
    
#     # Determine next node
#     next_node = create_feedback_node()
    
#     return result, next_node


# async def proceed_to_next_question(args: FlowArgs, flow_manager: FlowManager) -> tuple[ProceedResult, NodeConfig]:
#     """Check if user wants to proceed to next question or end quiz"""
#     user_response: str = args.get("response", "").strip().lower()
    
#     proceed_keywords = ["yes", "yeah", "yep", "sure", "ready", "continue", "next", "go ahead", "proceed", "ok", "okay", "let's go", "go on", "please"]
#     stop_keywords = ["no", "nope", "stop", "end", "quit", "pause", "wait", "not ready", "not yet", "hold on", "later"]
    
#     logger.info(f"🤔 User response: '{user_response}'")
    
#     if any(keyword in user_response for keyword in proceed_keywords):
#         logger.info(f"✅ User wants to continue to next question")
#         # Check if there are more questions
#         next_index = flow_manager.state.get("current_question_index", 0)
#         total_questions = flow_manager.state.get("total_questions", 0)
        
#         if next_index < total_questions:
#             result = ProceedResult(
#                 wants_to_proceed=True,
#                 user_response=user_response
#             )
#             return result, create_ask_question_node()
#         else:
#             # No more questions, go to quiz complete
#             logger.info("🎉 No more questions, going to quiz complete")
#             result = ProceedResult(
#                 wants_to_proceed=True,
#                 user_response=user_response
#             )
#             return result, create_quiz_complete_node()
            
#     elif any(keyword in user_response for keyword in stop_keywords):
#         logger.info(f"❌ User wants to stop or pause")
#         # Ask if they want to end quiz completely
#         next_node = {
#             "name": "confirm_stop",
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user doesn't want to continue with the next question right now.
#                     Ask them if they want to end the quiz completely or just take a break.
#                     Say something like: "Would you like to end the quiz now, or would you like to take a break and continue later?"
                    
#                     If they say "end", "quit", "stop", "finish" or similar, use the confirm_end_quiz function.
#                     If they say "break", "pause", "later", "wait" etc., say: "Okay, I'll wait. Just say 'ready' when you want to continue." and wait for their response."""
#                 }
#             ],
#             "functions": [confirm_end_schema],
#         }
#         result = ProceedResult(
#             wants_to_proceed=False,
#             user_response=user_response
#         )
#         return result, next_node
#     else:
#         # Unclear response, ask again
#         logger.info(f"🤔 Unclear response: {user_response}")
#         next_node = {
#             "name": "clarify_proceed",
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user's response wasn't clear. Ask them again if they're ready for the next question.
#                     Say something like: "Sorry, I didn't catch that. Are you ready for the next question? Please say yes or no."
                    
#                     Wait for their response. If they say "yes" or similar, use the proceed_to_next_question function.
#                     If they say "no" or similar, ask if they want to end the quiz."""
#                 }
#             ],
#             "functions": [proceed_schema],
#         }
#         result = ProceedResult(
#             wants_to_proceed=False,
#             user_response=user_response
#         )
#         return result, next_node


# async def continue_to_next_question(args: FlowArgs, flow_manager: FlowManager) -> tuple[QuestionResult, NodeConfig]:
#     """Continue to next question after confirmation"""
#     next_index = flow_manager.state.get("current_question_index", 0)
    
#     logger.info(f"➡️ Moving to question {next_index + 1}")
    
#     result = QuestionResult(
#         question_index=next_index,
#         question_text="Moving to next question"
#     )
    
#     next_node = create_ask_question_node()
    
#     return result, next_node


# async def confirm_end_quiz(args: FlowArgs, flow_manager: FlowManager) -> tuple[QuizCompleteResult, NodeConfig]:
#     """Confirm user wants to end quiz"""
#     user_response: str = args.get("response", "").strip().lower()
    
#     end_keywords = ["end", "quit", "stop", "finish", "done", "yes end", "yes quit", "yes stop"]
#     continue_keywords = ["continue", "no", "go back", "resume", "keep going", "not end"]
    
#     if any(keyword in user_response for keyword in end_keywords):
#         logger.info("✅ User confirmed to end quiz")
#         return await end_quiz(args, flow_manager)
#     elif any(keyword in user_response for keyword in continue_keywords):
#         # User wants to continue, go back to current question
#         logger.info("🔄 User wants to continue with quiz")
#         # Go back to feedback node to ask about next question again
#         result = QuizCompleteResult(
#             total_questions=flow_manager.state.get("total_questions", 0),
#             correct_answers=flow_manager.state.get("score", 0),
#             score_percentage=0
#         )
#         return result, create_feedback_node()
#     else:
#         # Unclear, ask again
#         logger.info(f"🤔 Unclear end quiz response: {user_response}")
#         next_node = {
#             "name": "clarify_end",
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user's response wasn't clear. Ask them to clarify if they want to end the quiz or continue.
#                     Say something like: "Just to confirm, would you like to end the quiz now or continue with the next question? Please say 'end' or 'continue'."
                    
#                     If they say "end" or similar, use the confirm_end_quiz function.
#                     If they say "continue" or similar, go back to asking if they're ready for the next question."""
#                 }
#             ],
#             "functions": [confirm_end_schema],
#         }
#         result = QuizCompleteResult(
#             total_questions=flow_manager.state.get("total_questions", 0),
#             correct_answers=flow_manager.state.get("score", 0),
#             score_percentage=0
#         )
#         return result, next_node


# async def end_quiz(args: FlowArgs, flow_manager: FlowManager) -> tuple[QuizCompleteResult, NodeConfig]:
#     """End the quiz"""
#     score = flow_manager.state.get("score", 0)
#     total = flow_manager.state.get("total_questions", 0)
    
#     logger.info(f"🏁 Quiz complete! Score: {score}/{total}")
    
#     result = QuizCompleteResult(
#         total_questions=total,
#         correct_answers=score,
#         score_percentage=(score / total * 100) if total > 0 else 0
#     )
    
#     return result, create_goodbye_node()


# # ============================================================================
# # Function Schemas
# # ============================================================================

# collect_missing_info_schema = FlowsFunctionSchema(
#     name="collect_missing_info",
#     description="Collect missing session information (session code or roll number)",
#     properties={
#         "session_code": {
#             "type": "string",
#             "description": "The session code provided by the user (e.g., H6TU)"
#         },
#         "roll_number": {
#             "type": "string",
#             "description": "The user's roll number (student ID)"
#         }
#     },
#     required=[],  # Not required since we might have partial info
#     handler=collect_missing_info,
# )

# validate_session_schema = FlowsFunctionSchema(
#     name="validate_session",
#     description="Validate the session code and roll number and load quiz questions",
#     properties={
#         "session_code": {
#             "type": "string",
#             "description": "The session code provided by the user (e.g., H6TU)"
#         },
#         "roll_number": {
#             "type": "string",
#             "description": "The user's roll number (student ID)"
#         }
#     },
#     required=["session_code", "roll_number"],
#     handler=validate_session,
# )

# load_and_speak_question_schema = FlowsFunctionSchema(
#     name="load_and_speak_question",
#     description="Load the current question and speak it to the user",
#     properties={},
#     required=[],
#     handler=load_and_speak_question,
# )

# submit_answer_schema = FlowsFunctionSchema(
#     name="submit_answer",
#     description="Submit the user's answer for the current question",
#     properties={
#         "answer": {
#             "type": "string",
#             "description": "The user's answer (letter A-F or full text)"
#         }
#     },
#     required=["answer"],
#     handler=submit_answer,
# )

# proceed_schema = FlowsFunctionSchema(
#     name="proceed_to_next_question",
#     description="Check if user wants to proceed to next question or end quiz",
#     properties={
#         "response": {
#             "type": "string",
#             "description": "The user's response to whether they're ready for next question"
#         }
#     },
#     required=["response"],
#     handler=proceed_to_next_question,
# )

# continue_schema = FlowsFunctionSchema(
#     name="continue_to_next_question",
#     description="Continue to the next question",
#     properties={},
#     required=[],
#     handler=continue_to_next_question,
# )

# confirm_end_schema = FlowsFunctionSchema(
#     name="confirm_end_quiz",
#     description="Confirm if user wants to end the quiz",
#     properties={
#         "response": {
#             "type": "string",
#             "description": "User's response to ending the quiz"
#         }
#     },
#     required=["response"],
#     handler=confirm_end_quiz,
# )

# end_quiz_schema = FlowsFunctionSchema(
#     name="end_quiz",
#     description="End the quiz and show final results",
#     properties={},
#     required=[],
#     handler=end_quiz,
# )


# # ============================================================================
# # Node Configurations
# # ============================================================================

# def create_welcome_node() -> NodeConfig:
#     """Create the welcome node"""
#     return {
#         "name": "welcome",
#         "role_messages": [
#             {
#                 "role": "system",
#                 "content": "You are QuizMaster, a friendly and enthusiastic quiz host. You speak clearly and energetically. Be encouraging and maintain positive energy throughout."
#             }
#         ],
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Welcome the user to the quiz! Introduce yourself as QuizMaster and explain you need two things to start:
# 1. Their session code (like H6TU)
# 2. Their roll number

# Start by asking for the session code first. You can say something like:
# "Welcome to QuizMaster! I'm excited to host your quiz today. To get started, I'll need two pieces of information. First, what's your session code?"

# Once they provide the session code, ask for their roll number. Then use the collect_missing_info function with both pieces of information."""
#             }
#         ],
#         "functions": [collect_missing_info_schema],
#     }


# def create_ask_session_code_node() -> NodeConfig:
#     """Create node to ask for session code"""
#     return {
#         "name": "ask_session_code",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Ask the user for their session code. It's usually a 4-character code like H6TU.
# Say something like: "Great, now I need your session code. What's your session code?"

# Once they provide it, use the collect_missing_info function with the session code."""
#             }
#         ],
#         "functions": [collect_missing_info_schema],
#     }


# def create_ask_roll_number_node() -> NodeConfig:
#     """Create node to ask for roll number"""
#     return {
#         "name": "ask_roll_number",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Ask the user for their roll number (student ID).
# Say something like: "Thank you! Now I need your roll number. What's your roll number?"

# Once they provide it, use the collect_missing_info function with the roll number."""
#             }
#         ],
#         "functions": [collect_missing_info_schema],
#     }


# def create_invalid_session_node() -> NodeConfig:
#     """Create node for invalid session"""
    
#     return {
#         "name": "invalid_session",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """The session validation failed. Possible reasons:
# 1. Incorrect session code
# 2. Incorrect roll number
# 3. Session doesn't exist
# 4. Roll number not authorized for this session

# Check flow state for error details: {last_error}

# Politely inform the user there was an issue. Say something like:
# "I'm sorry, but I couldn't validate your credentials. Let's try again."

# Ask them to provide both their session code and roll number again, then use the collect_missing_info function."""
#             }
#         ],
#         "functions": [collect_missing_info_schema],
#     }


# def create_ask_question_node() -> NodeConfig:
#     """Create node to prepare to ask a question"""
    
#     return {
#         "name": "ask_question",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """You're about to ask the user a quiz question.

# First, acknowledge their successful login. Say something like:
# "Perfect! Now let's start the quiz. Good luck!"

# Then use the load_and_speak_question function to load and prepare the next question."""
#             }
#         ],
#         "functions": [load_and_speak_question_schema],
#     }


# def create_speak_question_node() -> NodeConfig:
#     """Create node to actually speak the question"""
    
#     return {
#         "name": "speak_question",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Now speak the quiz question to the user. The question has been loaded into the state:

# Question number: {current_question_number}
# Total questions: {total_questions}
# Formatted question: {current_formatted_question}

# SPEAK THIS OUT LOUD:
# "Question {current_question_number} of {total_questions}. {current_formatted_question}. What's your answer?"

# Make sure to read ALL the options clearly. The user is LISTENING, not reading."""
#             }
#         ],
#         "functions": [submit_answer_schema],
#     }


# def create_feedback_node() -> NodeConfig:
#     """Create feedback node - uses flow manager state"""
    
#     return {
#         "name": "feedback",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Provide feedback on the user's answer using the flow state:
# - last_is_correct: {last_is_correct}
# - last_correct_answer: {last_correct_answer}
# - score: {score}
# - total_questions: {total_questions}
# - current_question_index: {current_question_index}

# If last_is_correct is True:
#   Say: "That's right! {last_correct_answer} is correct! Great job!"
# If last_is_correct is False:
#   Say: "Actually, the correct answer is {last_correct_answer}."

# Then say: "Your current score is {score} out of {total_questions}."

# Now ask: "Are you ready for the next question?"

# Wait for their response. If they say anything affirmative (yes, yeah, ready, continue, next, etc.), 
# use the proceed_to_next_question function with their response."""
#             }
#         ],
#         "functions": [proceed_schema],
#     }


# def create_quiz_complete_node() -> NodeConfig:
#     """Create quiz completion node - uses flow manager state"""
    
#     return {
#         "name": "quiz_complete",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": """Congratulations! The quiz is complete!

# Use the flow state to get:
# - score: {score}
# - total_questions: {total_questions}

# Calculate percentage = (score / total_questions) * 100

# If percentage >= 80:
#   Say: "Excellent work! You scored {score} out of {total_questions}! That's {percentage} percent!"
# If percentage >= 60:
#   Say: "Good job! You scored {score} out of {total_questions}. That's {percentage} percent."
# Else:
#   Say: "Thanks for playing! You scored {score} out of {total_questions}. That's {percentage} percent. Practice makes perfect!"

# Now ask: "Would you like to end the quiz now?"
# Wait for their response. If they say yes or similar, use the confirm_end_quiz function."""
#             }
#         ],
#         "functions": [confirm_end_schema],
#     }


# def create_goodbye_node() -> NodeConfig:
#     """Create goodbye node"""
#     return {
#         "name": "goodbye",
#         "task_messages": [
#             {
#                 "role": "system",
#                 "content": "Thank them warmly for playing the quiz and say goodbye! You can say something like: 'Thank you for playing! Have a great day!'"
#             }
#         ],
#         "post_actions": [{"type": "end_conversation"}],
#     }


# # ============================================================================
# # Main Bot Function
# # ============================================================================

# async def run_bot(websocket_client, session_code: Optional[str] = None):
#     """Run the quiz bot with flow management"""
#     logger.info("🤖 Starting Quiz Bot")
    
#     # Create WebSocket transport
#     ws_transport = FastAPIWebsocketTransport(
#         websocket=websocket_client,
#         params=FastAPIWebsocketParams(
#             audio_in_enabled=True,
#             audio_out_enabled=True,
#             add_wav_header=False,
#             vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.5)),
#             serializer=ProtobufFrameSerializer(),
#         ),
#     )

#     # Create Gemini Multimodal Live LLM service
#     llm = GeminiLiveLLMService(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         config={
#             "system_instruction": """You are QuizMaster, a friendly, enthusiastic quiz host. 
#             You speak clearly and energetically at a moderate pace.
#             You always read questions and options aloud exactly as provided.
#             You provide encouraging feedback after each answer.
#             You maintain a positive and engaging tone throughout the quiz.
#             This is a voice conversation - avoid special characters and emojis."""
#         }
#     )

#     # Create conversation context
#     context = LLMContext()
#     context_aggregator = LLMContextAggregatorPair(context)

#     # RTVI for monitoring
#     rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#     # Build the pipeline
#     pipeline = Pipeline(
#         [
#             ws_transport.input(),
#             rtvi,
#             context_aggregator.user(),
#             llm,
#             ws_transport.output(),
#             context_aggregator.assistant(),
#         ]
#     )

#     # Create pipeline task
#     task = PipelineTask(
#         pipeline,
#         params=PipelineParams(
#             enable_metrics=True,
#             enable_usage_metrics=True,
#             allow_interruptions=True,
#         ),
#         observers=[RTVIObserver(rtvi)],
#     )

#     # Initialize flow manager
#     flow_manager = FlowManager(
#         task=task,
#         llm=llm,
#         context_aggregator=context_aggregator,
#         transport=ws_transport,
#     )

#     # Event handlers
#     @rtvi.event_handler("on_client_ready")
#     async def on_client_ready(rtvi):
#         logger.info("✅ Pipecat client ready.")
#         await rtvi.set_bot_ready()
#         # Initialize the flow with welcome node
#         await flow_manager.initialize(create_welcome_node())

#     @ws_transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         logger.info("✅ Client connected via WebSocket")

#     @ws_transport.event_handler("on_client_disconnected")
#     async def on_client_disconnected(transport, client):
#         logger.info("❌ Client disconnected")
#         await task.cancel()

#     # Create and run the pipeline runner
#     runner = PipelineRunner(handle_sigint=False)
    
#     try:
#         await runner.run(task)
#     except Exception as e:
#         logger.error(f"Error in pipeline: {e}")
#         raise

# import os
# import aiohttp
# import json
# from typing import Dict, Any, Optional, List, Tuple
# from datetime import datetime
# from enum import Enum

# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.audio.vad.vad_analyzer import VADParams
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# from pipecat_flows import (
#     FlowArgs,
#     FlowManager,
#     FlowResult,
#     FlowsFunctionSchema,
#     NodeConfig,
# )

# load_dotenv(override=True)

# # ============================================================================
# # Constants and Configuration
# # ============================================================================

# class FlowStateKeys:
#     """Keys used in flow manager state"""
#     SESSION_CODE = "session_code"
#     ROLL_NUMBER = "roll_number"
#     QUESTIONS = "questions"
#     CURRENT_QUESTION_INDEX = "current_question_index"
#     SCORE = "score"
#     TOTAL_QUESTIONS = "total_questions"
#     CURRENT_FORMATTED_QUESTION = "current_formatted_question"
#     CURRENT_QUESTION_NUMBER = "current_question_number"
#     LAST_IS_CORRECT = "last_is_correct"
#     LAST_CORRECT_ANSWER = "last_correct_answer"
#     LAST_ERROR = "last_error"
#     QUIZ_STARTED = "quiz_started"


# class NodeNames:
#     """Names for all flow nodes"""
#     WELCOME = "welcome"
#     ASK_SESSION_CODE = "ask_session_code"
#     ASK_ROLL_NUMBER = "ask_roll_number"
#     INVALID_SESSION = "invalid_session"
#     CONFIRM_START = "confirm_start"
#     ASK_QUESTION = "ask_question"
#     SPEAK_QUESTION = "speak_question"
#     FEEDBACK = "feedback"
#     CLARIFY_START = "clarify_start"
#     CLARIFY_PROCEED = "clarify_proceed"
#     CLARIFY_END = "clarify_end"
#     CONFIRM_STOP = "confirm_stop"
#     CONFIRM_DELAY = "confirm_delay"
#     QUIZ_COMPLETE = "quiz_complete"
#     GOODBYE = "goodbye"


# class ResponseKeywords:
#     """Keywords for user response analysis"""
#     POSITIVE = ["yes", "yeah", "yep", "sure", "ready", "start", "begin", 
#                 "go ahead", "proceed", "ok", "okay", "let's go", "go on", 
#                 "please", "continue", "next", "sure thing", "absolutely",
#                 "definitely", "of course", "certainly", "by all means"]
    
#     NEGATIVE = ["no", "nope", "stop", "wait", "pause", "not ready", 
#                 "not yet", "hold on", "later", "quit", "end", "exit",
#                 "finish", "done", "cancel", "abort", "terminate"]
    
#     CONTINUE = ["continue", "go back", "resume", "keep going", "not end",
#                 "carry on", "proceed", "move on", "advance"]
    
#     DELAY = ["break", "pause", "later", "wait", "rest", "take a break",
#              "need time", "moment please", "hold off"]


# # ============================================================================
# # API Service
# # ============================================================================

# class APIService:
#     """Service for handling API calls"""
    
#     def __init__(self, base_url: str = None):
#         self.base_url = base_url or os.getenv("NODE_API_URL", "http://localhost:3000")
#         self.timeout = aiohttp.ClientTimeout(total=10)
    
#     async def get_questions(self, session_code: str, roll_number: str) -> Dict[str, Any]:
#         """Get questions for a session with roll number"""
#         try:
#             url = f"{self.base_url}/api/sessions/{session_code}/questions"
#             params = {"rollNumber": roll_number} if roll_number else None
#             logger.info(f"🌐 Calling API: GET {url} with roll number: {roll_number}")
            
#             async with aiohttp.ClientSession(timeout=self.timeout) as session:
#                 async with session.get(url, params=params) as response:
#                     logger.info(f"📊 API Response Status: {response.status}")
                    
#                     if response.status == 200:
#                         data = await response.json()
#                         logger.info(f"✅ Got questions for session {session_code}")
                        
#                         # Check response format
#                         if isinstance(data, dict) and "data" in data:
#                             return {"status": "ok", "data": data["data"]}
#                         elif isinstance(data, list):
#                             return {"status": "ok", "data": data}
#                         else:
#                             logger.error(f"❌ Unexpected response format: {data}")
#                             return {"status": "error", "error": "Unexpected format"}
#                     elif response.status == 404:
#                         return {"status": "error", "error": "Session not found or invalid roll number"}
#                     elif response.status == 403:
#                         return {"status": "error", "error": "Access denied - invalid credentials"}
#                     else:
#                         error_text = await response.text()
#                         logger.error(f"❌ API error {response.status}: {error_text}")
#                         return {"status": "error", "error": f"API error: {response.status}"}
#         except Exception as e:
#             logger.error(f"❌ Error getting questions: {e}")
#             return {"status": "error", "error": str(e)}


# # ============================================================================
# # Type Definitions for Function Results
# # ============================================================================

# class SessionValidationResult(FlowResult):
#     """Result type for session validation"""
#     valid: bool
#     questions: list[Dict[str, Any]]
#     total_questions: int
#     roll_number: str = ""
#     session_code: str = ""


# class QuestionResult(FlowResult):
#     """Result type for question handling"""
#     question_index: int
#     question_text: str


# class AnswerResult(FlowResult):
#     """Result type for answer processing"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str
#     score: int


# class QuizCompleteResult(FlowResult):
#     """Result type for quiz completion"""
#     total_questions: int
#     correct_answers: int
#     score_percentage: float


# class MissingInfoResult(FlowResult):
#     """Result type for missing information collection"""
#     missing_fields: list[str]
#     collected_data: Dict[str, str]


# class ProceedResult(FlowResult):
#     """Result type for proceed confirmation"""
#     wants_to_proceed: bool
#     user_response: str


# # ============================================================================
# # Question Utilities
# # ============================================================================

# class QuestionFormatter:
#     """Utility for formatting quiz questions"""
    
#     @staticmethod
#     def format_for_speech(question_data: Dict[str, Any]) -> str:
#         """Format question for natural speech"""
#         question_text = question_data.get("question_text", "No question text")
#         options = question_data.get("question_options", [])
        
#         # Format options with letters for speech
#         letters = ["A", "B", "C", "D", "E", "F"]
#         formatted_options = []
        
#         for i, option in enumerate(options[:6]):
#             option_text = option.get("option_text", f"Option {i+1}")
#             formatted_options.append(f"{letters[i]}: {option_text}")
        
#         options_text = ", ".join(formatted_options)
        
#         return f"{question_text}. Your options are: {options_text}"
    
#     @staticmethod
#     def get_correct_answer(question_data: Dict[str, Any]) -> str:
#         """Get the correct answer for a question"""
#         options = question_data.get("question_options", [])
#         for option in options:
#             if option.get("is_correct", False):
#                 return option.get("option_text", "")
#         return ""
    
#     @staticmethod
#     def check_answer(user_answer: str, correct_answer: str, question_data: Dict[str, Any]) -> bool:
#         """Check if user's answer is correct"""
#         user_answer_lower = user_answer.lower().strip()
#         correct_answer_lower = correct_answer.lower()
        
#         # Check letter answers (A, B, C, etc.)
#         letters = ["a", "b", "c", "d", "e", "f"]
#         if user_answer_lower in letters:
#             index = letters.index(user_answer_lower)
#             options = question_data.get("question_options", [])
#             if index < len(options):
#                 selected_option = options[index]
#                 return selected_option.get("is_correct", False)
        
#         # Check exact text match
#         if user_answer_lower == correct_answer_lower:
#             return True
        
#         # Check partial match
#         if (user_answer_lower in correct_answer_lower or 
#             correct_answer_lower in user_answer_lower):
#             return True
        
#         return False


# class ResponseAnalyzer:
#     """Utility for analyzing user responses"""
    
#     @staticmethod
#     def contains_keywords(text: str, keyword_list: List[str]) -> bool:
#         """Check if text contains any of the keywords"""
#         text_lower = text.lower()
#         return any(keyword in text_lower for keyword in keyword_list)
    
#     @staticmethod
#     def is_positive_response(text: str) -> bool:
#         """Check if response is positive"""
#         return ResponseAnalyzer.contains_keywords(text, ResponseKeywords.POSITIVE)
    
#     @staticmethod
#     def is_negative_response(text: str) -> bool:
#         """Check if response is negative"""
#         return ResponseAnalyzer.contains_keywords(text, ResponseKeywords.NEGATIVE)
    
#     @staticmethod
#     def wants_to_continue(text: str) -> bool:
#         """Check if user wants to continue"""
#         return ResponseAnalyzer.contains_keywords(text, ResponseKeywords.CONTINUE)
    
#     @staticmethod
#     def wants_to_delay(text: str) -> bool:
#         """Check if user wants to delay"""
#         return ResponseAnalyzer.contains_keywords(text, ResponseKeywords.DELAY)


# # ============================================================================
# # Function Handlers
# # ============================================================================

# class FunctionHandlers:
#     """Collection of all function handlers"""
    
#     def __init__(self, api_service: APIService):
#         self.api_service = api_service
    
#     async def collect_missing_info(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[MissingInfoResult, NodeConfig]:
#         """Collect missing session info (session code or roll number)"""
#         session_code = args.get(FlowStateKeys.SESSION_CODE, "").strip().upper()
#         roll_number = args.get(FlowStateKeys.ROLL_NUMBER, "").strip()
        
#         logger.info(f"📝 Collecting info - Session: {session_code}, Roll: {roll_number}")
        
#         # Store what we have
#         if session_code:
#             flow_manager.state[FlowStateKeys.SESSION_CODE] = session_code
#         if roll_number:
#             flow_manager.state[FlowStateKeys.ROLL_NUMBER] = roll_number
        
#         # Check what's missing
#         missing = []
#         if not session_code:
#             missing.append("session code")
#         if not roll_number:
#             missing.append("roll number")
        
#         result = MissingInfoResult(
#             missing_fields=missing,
#             collected_data={
#                 FlowStateKeys.SESSION_CODE: session_code,
#                 FlowStateKeys.ROLL_NUMBER: roll_number
#             }
#         )
        
#         if not missing:
#             # Both provided, proceed to validation
#             logger.info("✅ Both session code and roll number provided, validating...")
#             return await self.validate_session(args, flow_manager)
        
#         # Determine which node to go to based on what's missing
#         if len(missing) == 2:
#             logger.info("❌ Missing both session code and roll number")
#             return result, NodeFactory.create_welcome_node()
#         elif "session code" in missing:
#             logger.info("❌ Missing session code")
#             return result, NodeFactory.create_ask_session_code_node()
#         else:  # missing roll number
#             logger.info("❌ Missing roll number")
#             return result, NodeFactory.create_ask_roll_number_node()
    
#     async def validate_session(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[SessionValidationResult, NodeConfig]:
#         """Validate session code and load questions"""
#         # Get from args first, then fall back to state
#         session_code: str = args.get(FlowStateKeys.SESSION_CODE, "").strip().upper()
#         roll_number: str = args.get(FlowStateKeys.ROLL_NUMBER, "").strip()
        
#         # If not in args, check state
#         if not session_code:
#             session_code = flow_manager.state.get(FlowStateKeys.SESSION_CODE, "")
#         if not roll_number:
#             roll_number = flow_manager.state.get(FlowStateKeys.ROLL_NUMBER, "")
        
#         logger.info(f"🔍 Validating session: {session_code} with roll number: {roll_number}")
        
#         if not session_code or not roll_number:
#             logger.error("❌ Missing session code or roll number")
#             result = SessionValidationResult(
#                 valid=False, 
#                 total_questions=0, 
#                 questions=[], 
#                 roll_number=roll_number,
#                 session_code=session_code
#             )
#             flow_manager.state[FlowStateKeys.LAST_ERROR] = "Please provide both session code and roll number"
#             return result, NodeFactory.create_invalid_session_node()
        
#         # Get questions from API with roll number
#         questions_result = await self.api_service.get_questions(session_code, roll_number)
        
#         if questions_result.get("status") == "ok" and "data" in questions_result:
#             questions = questions_result["data"]
            
#             if questions and len(questions) > 0:
#                 logger.info(f"✅ Loaded {len(questions)} questions for roll number {roll_number}")
                
#                 # Store in flow manager state
#                 flow_manager.state[FlowStateKeys.QUESTIONS] = questions
#                 flow_manager.state[FlowStateKeys.CURRENT_QUESTION_INDEX] = 0
#                 flow_manager.state[FlowStateKeys.SCORE] = 0
#                 flow_manager.state[FlowStateKeys.TOTAL_QUESTIONS] = len(questions)
#                 flow_manager.state[FlowStateKeys.ROLL_NUMBER] = roll_number
#                 flow_manager.state[FlowStateKeys.SESSION_CODE] = session_code
                
#                 result = SessionValidationResult(
#                     valid=True, 
#                     total_questions=len(questions), 
#                     questions=questions,
#                     roll_number=roll_number,
#                     session_code=session_code
#                 )
#                 # Go to confirmation node instead of directly to questions
#                 next_node = NodeFactory.create_confirm_start_node()
#                 return result, next_node
        
#         error_msg = questions_result.get("error", "Session validation failed")
#         logger.error(f"❌ Session validation failed: {error_msg}")
#         flow_manager.state[FlowStateKeys.LAST_ERROR] = error_msg
#         result = SessionValidationResult(
#             valid=False, 
#             total_questions=0, 
#             questions=[],
#             roll_number=roll_number,
#             session_code=session_code
#         )
#         return result, NodeFactory.create_invalid_session_node()
    
#     async def confirm_start_quiz(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[ProceedResult, NodeConfig]:
#         """Confirm user wants to start the quiz"""
#         user_response: str = args.get("response", "").strip().lower()
        
#         logger.info(f"🤔 User confirmation response: '{user_response}'")
        
#         if ResponseAnalyzer.is_positive_response(user_response):
#             logger.info("✅ User wants to start the quiz")
#             flow_manager.state[FlowStateKeys.QUIZ_STARTED] = True
#             result = ProceedResult(
#                 wants_to_proceed=True,
#                 user_response=user_response
#             )
#             return result, NodeFactory.create_ask_question_node()
#         elif ResponseAnalyzer.is_negative_response(user_response):
#             logger.info("❌ User doesn't want to start the quiz yet")
#             # Ask if they want to proceed later
#             next_node = NodeFactory.create_confirm_delay_node()
#             result = ProceedResult(
#                 wants_to_proceed=False,
#                 user_response=user_response
#             )
#             return result, next_node
#         else:
#             # Unclear response, ask again
#             logger.info(f"🤔 Unclear confirmation response: {user_response}")
#             next_node = NodeFactory.create_clarify_start_node()
#             result = ProceedResult(
#                 wants_to_proceed=False,
#                 user_response=user_response
#             )
#             return result, next_node
    
#     async def load_and_speak_question(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[QuestionResult, NodeConfig]:
#         """Load the current question and prepare to speak it"""
#         question_index = flow_manager.state.get(FlowStateKeys.CURRENT_QUESTION_INDEX, 0)
#         questions = flow_manager.state.get(FlowStateKeys.QUESTIONS, [])
#         total = flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0)
        
#         if question_index >= len(questions):
#             logger.info("🎉 No more questions")
#             return QuestionResult(
#                 question_index=question_index,
#                 question_text="Complete"
#             ), NodeFactory.create_quiz_complete_node()
        
#         current_question = questions[question_index]
#         question_num = question_index + 1
        
#         # Format question for speech
#         formatted_question = QuestionFormatter.format_for_speech(current_question)
        
#         # Store formatted question in state so LLM can access it
#         flow_manager.state[FlowStateKeys.CURRENT_FORMATTED_QUESTION] = formatted_question
#         flow_manager.state[FlowStateKeys.CURRENT_QUESTION_NUMBER] = question_num
        
#         logger.info(f"📝 Loaded question {question_num}/{total}: {current_question.get('question_text', '')[:50]}...")
        
#         result = QuestionResult(
#             question_index=question_index,
#             question_text=formatted_question
#         )
        
#         # Move to speaking node
#         next_node = NodeFactory.create_speak_question_node()
        
#         return result, next_node
    
#     async def submit_answer(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[AnswerResult, NodeConfig]:
#         """Process user's answer"""
#         user_answer: str = args["answer"].strip()
        
#         # Get data from flow manager state
#         question_index: int = flow_manager.state.get(FlowStateKeys.CURRENT_QUESTION_INDEX, 0)
#         questions: list = flow_manager.state.get(FlowStateKeys.QUESTIONS, [])
#         score: int = flow_manager.state.get(FlowStateKeys.SCORE, 0)
        
#         logger.info(f"📝 Processing answer: '{user_answer}' for question {question_index + 1}")
        
#         current_question = questions[question_index]
#         correct_answer = QuestionFormatter.get_correct_answer(current_question)
        
#         # Check if answer is correct
#         is_correct = QuestionFormatter.check_answer(user_answer, correct_answer, current_question)
        
#         # Update score
#         if is_correct:
#             score += 1
#             flow_manager.state[FlowStateKeys.SCORE] = score
        
#         # Store feedback data
#         flow_manager.state[FlowStateKeys.LAST_IS_CORRECT] = is_correct
#         flow_manager.state[FlowStateKeys.LAST_CORRECT_ANSWER] = correct_answer
        
#         result = AnswerResult(
#             question_index=question_index,
#             user_answer=user_answer,
#             is_correct=is_correct,
#             correct_answer=correct_answer,
#             score=score
#         )
        
#         # Move to next question
#         next_index = question_index + 1
#         flow_manager.state[FlowStateKeys.CURRENT_QUESTION_INDEX] = next_index
        
#         # Determine next node
#         next_node = NodeFactory.create_feedback_node()
        
#         return result, next_node
    
#     async def proceed_to_next_question(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[ProceedResult, NodeConfig]:
#         """Check if user wants to proceed to next question or end quiz"""
#         user_response: str = args.get("response", "").strip().lower()
        
#         logger.info(f"🤔 User response: '{user_response}'")
        
#         if ResponseAnalyzer.is_positive_response(user_response):
#             logger.info(f"✅ User wants to continue to next question")
#             # Check if there are more questions
#             next_index = flow_manager.state.get(FlowStateKeys.CURRENT_QUESTION_INDEX, 0)
#             total_questions = flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0)
            
#             if next_index < total_questions:
#                 result = ProceedResult(
#                     wants_to_proceed=True,
#                     user_response=user_response
#                 )
#                 return result, NodeFactory.create_ask_question_node()
#             else:
#                 # No more questions, go to quiz complete
#                 logger.info("🎉 No more questions, going to quiz complete")
#                 result = ProceedResult(
#                     wants_to_proceed=True,
#                     user_response=user_response
#                 )
#                 return result, NodeFactory.create_quiz_complete_node()
                
#         elif ResponseAnalyzer.is_negative_response(user_response):
#             logger.info(f"❌ User wants to stop or pause")
#             # Ask if they want to end quiz completely
#             next_node = NodeFactory.create_confirm_stop_node()
#             result = ProceedResult(
#                 wants_to_proceed=False,
#                 user_response=user_response
#             )
#             return result, next_node
#         else:
#             # Unclear response, ask again
#             logger.info(f"🤔 Unclear response: {user_response}")
#             next_node = NodeFactory.create_clarify_proceed_node()
#             result = ProceedResult(
#                 wants_to_proceed=False,
#                 user_response=user_response
#             )
#             return result, next_node
    
#     async def confirm_end_quiz(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[QuizCompleteResult, NodeConfig]:
#         """Confirm user wants to end quiz"""
#         user_response: str = args.get("response", "").strip().lower()
        
#         if ResponseAnalyzer.is_positive_response(user_response) or ResponseAnalyzer.is_negative_response(user_response):
#             logger.info("✅ User confirmed to end quiz")
#             return await self.end_quiz(args, flow_manager)
#         elif ResponseAnalyzer.wants_to_continue(user_response):
#             # User wants to continue, go back to current question
#             logger.info("🔄 User wants to continue with quiz")
#             # Go back to feedback node to ask about next question again
#             result = QuizCompleteResult(
#                 total_questions=flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0),
#                 correct_answers=flow_manager.state.get(FlowStateKeys.SCORE, 0),
#                 score_percentage=0
#             )
#             return result, NodeFactory.create_feedback_node()
#         else:
#             # Unclear, ask again
#             logger.info(f"🤔 Unclear end quiz response: {user_response}")
#             next_node = NodeFactory.create_clarify_end_node()
#             result = QuizCompleteResult(
#                 total_questions=flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0),
#                 correct_answers=flow_manager.state.get(FlowStateKeys.SCORE, 0),
#                 score_percentage=0
#             )
#             return result, next_node
    
#     async def end_quiz(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[QuizCompleteResult, NodeConfig]:
#         """End the quiz"""
#         score = flow_manager.state.get(FlowStateKeys.SCORE, 0)
#         total = flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0)
        
#         logger.info(f"🏁 Quiz complete! Score: {score}/{total}")
        
#         result = QuizCompleteResult(
#             total_questions=total,
#             correct_answers=score,
#             score_percentage=(score / total * 100) if total > 0 else 0
#         )
        
#         return result, NodeFactory.create_goodbye_node()


# # ============================================================================
# # Node Factory
# # ============================================================================

# class NodeFactory:
#     """Factory for creating node configurations"""
    
#     @staticmethod
#     def create_welcome_node() -> NodeConfig:
#         """Create the welcome node"""
#         return {
#             "name": NodeNames.WELCOME,
#             "role_messages": [
#                 {
#                     "role": "system",
#                     "content": "You are QuizMaster, a friendly and enthusiastic quiz host. You speak clearly and energetically. Be encouraging and maintain positive energy throughout."
#                 }
#             ],
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Welcome the user to the quiz! Introduce yourself as QuizMaster and explain you need two things to start:
# 1. Their session code (like H6TU)
# 2. Their roll number

# Start by asking for the session code first. You can say something like:
# "Welcome to QuizMaster! I'm excited to host your quiz today. To get started, I'll need two pieces of information. First, what's your session code?"

# Once they provide the session code, ask for their roll number. Then use the collect_missing_info function with both pieces of information.

# Once both are collected, I'll validate them and ask if you're ready to start."""
#                 }
#             ],
#             "functions": [FunctionSchemas.COLLECT_MISSING_INFO],
#         }
    
#     @staticmethod
#     def create_ask_session_code_node() -> NodeConfig:
#         """Create node to ask for session code"""
#         return {
#             "name": NodeNames.ASK_SESSION_CODE,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Ask the user for their session code. It's usually a 4-character code like H6TU.
# Say something like: "Great, now I need your session code. What's your session code?"

# Once they provide it, use the collect_missing_info function with the session code."""
#                 }
#             ],
#             "functions": [FunctionSchemas.COLLECT_MISSING_INFO],
#         }
    
#     @staticmethod
#     def create_ask_roll_number_node() -> NodeConfig:
#         """Create node to ask for roll number"""
#         return {
#             "name": NodeNames.ASK_ROLL_NUMBER,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Ask the user for their roll number (student ID).
# Say something like: "Thank you! Now I need your roll number. What's your roll number?"

# Once they provide it, use the collect_missing_info function with the roll number."""
#                 }
#             ],
#             "functions": [FunctionSchemas.COLLECT_MISSING_INFO],
#         }
    
#     @staticmethod
#     def create_invalid_session_node() -> NodeConfig:
#         """Create node for invalid session"""
#         return {
#             "name": NodeNames.INVALID_SESSION,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The session validation failed. Possible reasons:
# 1. Incorrect session code
# 2. Incorrect roll number
# 3. Session doesn't exist
# 4. Roll number not authorized for this session

# Check flow state for error details: {last_error}

# Politely inform the user there was an issue. Say something like:
# "I'm sorry, but I couldn't validate your credentials. Let's try again."

# Ask them to provide both their session code and roll number again, then use the collect_missing_info function."""
#                 }
#             ],
#             "functions": [FunctionSchemas.COLLECT_MISSING_INFO],
#         }
    
#     @staticmethod
#     def create_confirm_start_node() -> NodeConfig:
#         """Create node to confirm user wants to start the quiz"""
#         return {
#             "name": NodeNames.CONFIRM_START,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Perfect! Your session has been validated successfully.

# You have loaded: {total_questions} questions for roll number: {roll_number}

# Now ask the user if they're ready to start the quiz.
# Say something like: "Perfect! I've loaded {total_questions} questions for you. Are you ready to start the quiz now?"

# Wait for their response. If they say anything affirmative (yes, yeah, ready, start, begin, let's go, etc.), 
# use the confirm_start_quiz function with their response."""
#                 }
#             ],
#             "functions": [FunctionSchemas.CONFIRM_START_QUIZ],
#         }
    
#     @staticmethod
#     def create_clarify_start_node() -> NodeConfig:
#         """Create node to clarify start quiz response"""
#         return {
#             "name": NodeNames.CLARIFY_START,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user's response wasn't clear. Ask them again if they're ready to start the quiz.
#                     Say something like: "Sorry, I didn't catch that. Are you ready to start the quiz now? Please say yes or no."
                    
#                     Wait for their response. If they say "yes" or similar, use the confirm_start_quiz function again.
#                     If they say "no" or similar, ask if they want to delay or exit."""
#                 }
#             ],
#             "functions": [FunctionSchemas.CONFIRM_START_QUIZ],
#         }
    
#     @staticmethod
#     def create_ask_question_node() -> NodeConfig:
#         """Create node to prepare to ask a question"""
#         return {
#             "name": NodeNames.ASK_QUESTION,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Great! Let's begin the quiz. Say something encouraging like:
# "Excellent! Let's get started. Remember, speak clearly and choose your answers carefully. Good luck!"

# Then use the load_and_speak_question function to load and prepare the first question."""
#                 }
#             ],
#             "functions": [FunctionSchemas.LOAD_AND_SPEAK_QUESTION],
#         }
    
#     @staticmethod
#     def create_speak_question_node() -> NodeConfig:
#         """Create node to actually speak the question"""
#         return {
#             "name": NodeNames.SPEAK_QUESTION,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Now speak the quiz question to the user. The question has been loaded into the state:

# Question number: {current_question_number}
# Total questions: {total_questions}
# Formatted question: {current_formatted_question}

# SPEAK THIS OUT LOUD:
# "Question {current_question_number} of {total_questions}. {current_formatted_question}. What's your answer?"

# Make sure to read ALL the options clearly. The user is LISTENING, not reading."""
#                 }
#             ],
#             "functions": [FunctionSchemas.SUBMIT_ANSWER],
#         }
    
#     @staticmethod
#     def create_feedback_node() -> NodeConfig:
#         """Create feedback node - uses flow manager state"""
#         return {
#             "name": NodeNames.FEEDBACK,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Provide feedback on the user's answer using the flow state:
# - last_is_correct: {last_is_correct}
# - last_correct_answer: {last_correct_answer}
# - score: {score}
# - total_questions: {total_questions}
# - current_question_index: {current_question_index}

# If last_is_correct is True:
#   Say: "That's right! {last_correct_answer} is correct! Great job!"
# If last_is_correct is False:
#   Say: "Actually, the correct answer is {last_correct_answer}."

# Then say: "Your current score is {score} out of {total_questions}."

# Now ask: "Are you ready for the next question?"

# Wait for their response. If they say anything affirmative (yes, yeah, ready, continue, next, etc.), 
# use the proceed_to_next_question function with their response."""
#                 }
#             ],
#             "functions": [FunctionSchemas.PROCEED_TO_NEXT_QUESTION],
#         }
    
#     @staticmethod
#     def create_clarify_proceed_node() -> NodeConfig:
#         """Create node to clarify proceed response"""
#         return {
#             "name": NodeNames.CLARIFY_PROCEED,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user's response wasn't clear. Ask them again if they're ready for the next question.
#                     Say something like: "Sorry, I didn't catch that. Are you ready for the next question? Please say yes or no."
                    
#                     Wait for their response. If they say "yes" or similar, use the proceed_to_next_question function.
#                     If they say "no" or similar, ask if they want to end the quiz."""
#                 }
#             ],
#             "functions": [FunctionSchemas.PROCEED_TO_NEXT_QUESTION],
#         }
    
#     @staticmethod
#     def create_confirm_stop_node() -> NodeConfig:
#         """Create node to confirm stopping the quiz"""
#         return {
#             "name": NodeNames.CONFIRM_STOP,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user doesn't want to continue with the next question right now.
#                     Ask them if they want to end the quiz completely or just take a break.
#                     Say something like: "Would you like to end the quiz now, or would you like to take a break and continue later?"
                    
#                     If they say "end", "quit", "stop", "finish" or similar, use the confirm_end_quiz function.
#                     If they say "break", "pause", "later", "wait" etc., say: "Okay, I'll wait. Just say 'ready' when you want to continue." and wait for their response."""
#                 }
#             ],
#             "functions": [FunctionSchemas.CONFIRM_END_QUIZ],
#         }
    
#     @staticmethod
#     def create_confirm_delay_node() -> NodeConfig:
#         """Create node to confirm delaying the quiz"""
#         return {
#             "name": NodeNames.CONFIRM_DELAY,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user doesn't want to start the quiz right now.
#                     Ask them if they'd like to take a break and start later, or if they want to exit.
#                     Say something like: "Would you like to take a break and come back later, or would you prefer to exit the quiz?"
                    
#                     If they say "exit", "quit", "stop", "end" or similar, use the end_quiz function.
#                     If they say "break", "pause", "later", "wait" etc., say: "Okay, I'll wait. Just say 'ready' when you want to start the quiz." and wait for their response."""
#                 }
#             ],
#             "functions": [FunctionSchemas.END_QUIZ],
#         }
    
#     @staticmethod
#     def create_clarify_end_node() -> NodeConfig:
#         """Create node to clarify end quiz response"""
#         return {
#             "name": NodeNames.CLARIFY_END,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user's response wasn't clear. Ask them to clarify if they want to end the quiz or continue.
#                     Say something like: "Just to confirm, would you like to end the quiz now or continue with the next question? Please say 'end' or 'continue'."
                    
#                     If they say "end" or similar, use the confirm_end_quiz function.
#                     If they say "continue" or similar, go back to asking if they're ready for the next question."""
#                 }
#             ],
#             "functions": [FunctionSchemas.CONFIRM_END_QUIZ],
#         }
    
#     @staticmethod
#     def create_quiz_complete_node() -> NodeConfig:
#         """Create quiz completion node - uses flow manager state"""
#         return {
#             "name": NodeNames.QUIZ_COMPLETE,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Congratulations! The quiz is complete!

# Use the flow state to get:
# - score: {score}
# - total_questions: {total_questions}

# Calculate percentage = (score / total_questions) * 100

# If percentage >= 80:
#   Say: "Excellent work! You scored {score} out of {total_questions}! That's {percentage} percent!"
# If percentage >= 60:
#   Say: "Good job! You scored {score} out of {total_questions}. That's {percentage} percent."
# Else:
#   Say: "Thanks for playing! You scored {score} out of {total_questions}. That's {percentage} percent. Practice makes perfect!"

# Now ask: "Would you like to end the quiz now?"
# Wait for their response. If they say yes or similar, use the confirm_end_quiz function."""
#                 }
#             ],
#             "functions": [FunctionSchemas.CONFIRM_END_QUIZ],
#         }
    
#     @staticmethod
#     def create_goodbye_node() -> NodeConfig:
#         """Create goodbye node"""
#         return {
#             "name": NodeNames.GOODBYE,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": "Thank them warmly for playing the quiz and say goodbye! You can say something like: 'Thank you for playing! Have a great day!'"
#                 }
#             ],
#             "post_actions": [{"type": "end_conversation"}],
#         }


# # ============================================================================
# # Function Schemas
# # ============================================================================

# class FunctionSchemas:
#     """Collection of all function schemas"""
    
#     # Initialize API service
#     _api_service = APIService()
#     _handlers = FunctionHandlers(_api_service)
    
#     # Define all schemas
#     COLLECT_MISSING_INFO = FlowsFunctionSchema(
#         name="collect_missing_info",
#         description="Collect missing session information (session code or roll number)",
#         properties={
#             "session_code": {
#                 "type": "string",
#                 "description": "The session code provided by the user (e.g., H6TU)"
#             },
#             "roll_number": {
#                 "type": "string",
#                 "description": "The user's roll number (student ID)"
#             }
#         },
#         required=[],  # Not required since we might have partial info
#         handler=_handlers.collect_missing_info,
#     )
    
#     VALIDATE_SESSION = FlowsFunctionSchema(
#         name="validate_session",
#         description="Validate the session code and roll number and load quiz questions",
#         properties={
#             "session_code": {
#                 "type": "string",
#                 "description": "The session code provided by the user (e.g., H6TU)"
#             },
#             "roll_number": {
#                 "type": "string",
#                 "description": "The user's roll number (student ID)"
#             }
#         },
#         required=["session_code", "roll_number"],
#         handler=_handlers.validate_session,
#     )
    
#     CONFIRM_START_QUIZ = FlowsFunctionSchema(
#         name="confirm_start_quiz",
#         description="Confirm if user wants to start the quiz",
#         properties={
#             "response": {
#                 "type": "string",
#                 "description": "User's response to starting the quiz"
#             }
#         },
#         required=["response"],
#         handler=_handlers.confirm_start_quiz,
#     )
    
#     LOAD_AND_SPEAK_QUESTION = FlowsFunctionSchema(
#         name="load_and_speak_question",
#         description="Load the current question and speak it to the user",
#         properties={},
#         required=[],
#         handler=_handlers.load_and_speak_question,
#     )
    
#     SUBMIT_ANSWER = FlowsFunctionSchema(
#         name="submit_answer",
#         description="Submit the user's answer for the current question",
#         properties={
#             "answer": {
#                 "type": "string",
#                 "description": "The user's answer (letter A-F or full text)"
#             }
#         },
#         required=["answer"],
#         handler=_handlers.submit_answer,
#     )
    
#     PROCEED_TO_NEXT_QUESTION = FlowsFunctionSchema(
#         name="proceed_to_next_question",
#         description="Check if user wants to proceed to next question or end quiz",
#         properties={
#             "response": {
#                 "type": "string",
#                 "description": "The user's response to whether they're ready for next question"
#             }
#         },
#         required=["response"],
#         handler=_handlers.proceed_to_next_question,
#     )
    
#     CONFIRM_END_QUIZ = FlowsFunctionSchema(
#         name="confirm_end_quiz",
#         description="Confirm if user wants to end the quiz",
#         properties={
#             "response": {
#                 "type": "string",
#                 "description": "User's response to ending the quiz"
#             }
#         },
#         required=["response"],
#         handler=_handlers.confirm_end_quiz,
#     )
    
#     END_QUIZ = FlowsFunctionSchema(
#         name="end_quiz",
#         description="End the quiz and show final results",
#         properties={},
#         required=[],
#         handler=_handlers.end_quiz,
#     )
    
#     @classmethod
#     def get_all_schemas(cls) -> List[FlowsFunctionSchema]:
#         """Get all function schemas"""
#         return [
#             cls.COLLECT_MISSING_INFO,
#             cls.VALIDATE_SESSION,
#             cls.CONFIRM_START_QUIZ,
#             cls.LOAD_AND_SPEAK_QUESTION,
#             cls.SUBMIT_ANSWER,
#             cls.PROCEED_TO_NEXT_QUESTION,
#             cls.CONFIRM_END_QUIZ,
#             cls.END_QUIZ,
#         ]


# # ============================================================================
# # Quiz Bot
# # ============================================================================

# class QuizBot:
#     """Main quiz bot class"""
    
#     def __init__(self):
#         self.llm_config = {
#             "system_instruction": """You are QuizMaster, a friendly, enthusiastic quiz host. 
#             You speak clearly and energetically at a moderate pace.
#             You always read questions and options aloud exactly as provided.
#             You provide encouraging feedback after each answer.
#             You maintain a positive and engaging tone throughout the quiz.
#             This is a voice conversation - avoid special characters and emojis."""
#         }
    
#     async def run(self, websocket_client, session_code: Optional[str] = None):
#         """Run the quiz bot with flow management"""
#         logger.info("🤖 Starting Quiz Bot")
        
#         # Create WebSocket transport
#         ws_transport = FastAPIWebsocketTransport(
#             websocket=websocket_client,
#             params=FastAPIWebsocketParams(
#                 audio_in_enabled=True,
#                 audio_out_enabled=True,
#                 add_wav_header=False,
#                 vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.5)),
#                 serializer=ProtobufFrameSerializer(),
#             ),
#         )

#         # Create Gemini Multimodal Live LLM service
#         llm = GeminiLiveLLMService(
#             api_key=os.getenv("GOOGLE_API_KEY"),
#             config=self.llm_config
#         )

#         # Create conversation context
#         context = LLMContext()
#         context_aggregator = LLMContextAggregatorPair(context)

#         # RTVI for monitoring
#         rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#         # Build the pipeline
#         pipeline = Pipeline(
#             [
#                 ws_transport.input(),
#                 rtvi,
#                 context_aggregator.user(),
#                 llm,
#                 ws_transport.output(),
#                 context_aggregator.assistant(),
#             ]
#         )

#         # Create pipeline task
#         task = PipelineTask(
#             pipeline,
#             params=PipelineParams(
#                 enable_metrics=True,
#                 enable_usage_metrics=True,
#                 allow_interruptions=True,
#             ),
#             observers=[RTVIObserver(rtvi)],
#         )

#         # Initialize flow manager
#         flow_manager = FlowManager(
#             task=task,
#             llm=llm,
#             context_aggregator=context_aggregator,
#             transport=ws_transport,
#         )

#         # Event handlers
#         @rtvi.event_handler("on_client_ready")
#         async def on_client_ready(rtvi):
#             logger.info("✅ Pipecat client ready.")
#             await rtvi.set_bot_ready()
#             # Initialize the flow with welcome node
#             await flow_manager.initialize(NodeFactory.create_welcome_node())

#         @ws_transport.event_handler("on_client_connected")
#         async def on_client_connected(transport, client):
#             logger.info("✅ Client connected via WebSocket")

#         @ws_transport.event_handler("on_client_disconnected")
#         async def on_client_disconnected(transport, client):
#             logger.info("❌ Client disconnected")
#             await task.cancel()

#         # Create and run the pipeline runner
#         runner = PipelineRunner(handle_sigint=False)
        
#         try:
#             await runner.run(task)
#         except Exception as e:
#             logger.error(f"Error in pipeline: {e}")
#             raise


# # ============================================================================
# # Main Function
# # ============================================================================

# async def run_bot(websocket_client, session_code: Optional[str] = None):
#     """Main entry point for running the bot"""
#     bot = QuizBot()
#     await bot.run(websocket_client, session_code)

### - Incomplete loggin --
# import os
# import aiohttp
# import json
# from typing import Dict, Any, Optional, List, Tuple
# from datetime import datetime
# from enum import Enum
# from dataclasses import dataclass, asdict
# import uuid

# from dotenv import load_dotenv
# from loguru import logger
# from pipecat.audio.vad.silero import SileroVADAnalyzer
# from pipecat.audio.vad.vad_analyzer import VADParams
# from pipecat.pipeline.pipeline import Pipeline
# from pipecat.pipeline.runner import PipelineRunner
# from pipecat.pipeline.task import PipelineParams, PipelineTask
# from pipecat.processors.aggregators.llm_context import LLMContext
# from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
# from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
# from pipecat.serializers.protobuf import ProtobufFrameSerializer
# from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
# from pipecat.transports.websocket.fastapi import (
#     FastAPIWebsocketParams,
#     FastAPIWebsocketTransport,
# )

# from pipecat_flows import (
#     FlowArgs,
#     FlowManager,
#     FlowResult,
#     FlowsFunctionSchema,
#     NodeConfig,
# )

# load_dotenv(override=True)

# # ============================================================================
# # Data Models for Response Tracking
# # ============================================================================

# @dataclass
# class QuestionResponse:
#     """Track user response for a single question"""
#     question_id: str
#     question_text: str
#     question_index: int
#     options: List[Dict[str, Any]]
#     user_answer: str
#     correct_answer: str
#     is_correct: bool
#     timestamp: str
#     response_time_seconds: float = 0.0
#     confidence_score: float = 0.0  # Could be added later with VAD analysis


# @dataclass
# class QuizSessionData:
#     """Complete quiz session data"""
#     session_id: str
#     session_code: str
#     roll_number: str
#     start_time: str
#     end_time: str
#     total_questions: int
#     score: int
#     score_percentage: float
#     responses: List[QuestionResponse]
#     duration_seconds: float = 0.0


# # ============================================================================
# # Response Tracker
# # ============================================================================

# class ResponseTracker:
#     """Track and log user responses throughout the quiz"""
    
#     def __init__(self):
#         self.session_id = str(uuid.uuid4())[:8]
#         self.start_time = None
#         self.responses: List[QuestionResponse] = []
#         self.current_question_start = None
        
#     def start_session(self, session_code: str, roll_number: str):
#         """Start tracking a new quiz session"""
#         self.start_time = datetime.now()
#         self.session_code = session_code
#         self.roll_number = roll_number
#         logger.info(f"📊 Starting response tracking for session {session_code}, roll {roll_number}")
#         logger.info(f"📋 Session ID: {self.session_id}")
    
#     def start_question(self, question_index: int, question_data: Dict[str, Any]):
#         """Start tracking time for a question"""
#         self.current_question_start = datetime.now()
#         self.current_question = {
#             "index": question_index,
#             "data": question_data,
#             "id": question_data.get("id", f"q{question_index}")
#         }
    
#     def record_response(self, 
#                        user_answer: str, 
#                        correct_answer: str, 
#                        is_correct: bool,
#                        confidence_score: float = 0.0) -> QuestionResponse:
#         """Record user's response for the current question"""
#         if not self.current_question_start:
#             logger.warning("⚠️ No question started before recording response")
#             return None
        
#         response_time = (datetime.now() - self.current_question_start).total_seconds()
        
#         question_data = self.current_question["data"]
#         response = QuestionResponse(
#             question_id=self.current_question["id"],
#             question_text=question_data.get("question_text", ""),
#             question_index=self.current_question["index"],
#             options=question_data.get("question_options", []),
#             user_answer=user_answer,
#             correct_answer=correct_answer,
#             is_correct=is_correct,
#             timestamp=datetime.now().isoformat(),
#             response_time_seconds=response_time,
#             confidence_score=confidence_score
#         )
        
#         self.responses.append(response)
        
#         logger.info(f"📝 Recorded response for question {self.current_question['index'] + 1}: "
#                    f"Answer: '{user_answer}', Correct: {is_correct}, Time: {response_time:.2f}s")
        
#         return response
    
#     def get_session_summary(self) -> QuizSessionData:
#         """Get complete session summary"""
#         if not self.start_time:
#             return None
        
#         end_time = datetime.now()
#         duration = (end_time - self.start_time).total_seconds()
        
#         # Calculate score
#         correct_count = sum(1 for r in self.responses if r.is_correct)
#         total_questions = len(self.responses)
#         score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
#         summary = QuizSessionData(
#             session_id=self.session_id,
#             session_code=self.session_code,
#             roll_number=self.roll_number,
#             start_time=self.start_time.isoformat(),
#             end_time=end_time.isoformat(),
#             total_questions=total_questions,
#             score=correct_count,
#             score_percentage=score_percentage,
#             responses=self.responses,
#             duration_seconds=duration
#         )
        
#         return summary
    
#     def log_summary(self):
#         """Log the complete session summary as JSON"""
#         summary = self.get_session_summary()
#         if summary:
#             summary_dict = asdict(summary)
            
#             # Format the JSON nicely
#             summary_json = json.dumps(summary_dict, indent=2, default=str)
            
#             logger.info("=" * 60)
#             logger.info("🎯 QUIZ SESSION SUMMARY")
#             logger.info("=" * 60)
            
#             # Pretty print summary
#             logger.info(f"Session ID: {summary.session_id}")
#             logger.info(f"Session Code: {summary.session_code}")
#             logger.info(f"Roll Number: {summary.roll_number}")
#             logger.info(f"Start Time: {summary.start_time}")
#             logger.info(f"End Time: {summary.end_time}")
#             logger.info(f"Duration: {summary.duration_seconds:.2f} seconds")
#             logger.info(f"Total Questions: {summary.total_questions}")
#             logger.info(f"Score: {summary.score}/{summary.total_questions}")
#             logger.info(f"Percentage: {summary.score_percentage:.1f}%")
            
#             logger.info("\n📋 Detailed Responses:")
#             logger.info("-" * 40)
            
#             for i, response in enumerate(summary.responses, 1):
#                 status = "✅ CORRECT" if response.is_correct else "❌ INCORRECT"
#                 logger.info(f"Q{i}: {response.question_text[:50]}...")
#                 logger.info(f"   Answer: '{response.user_answer}'")
#                 logger.info(f"   Correct: '{response.correct_answer}'")
#                 logger.info(f"   Status: {status}")
#                 logger.info(f"   Time: {response.response_time_seconds:.2f}s")
#                 logger.info("-" * 40)
            
#             logger.info("\n📊 Complete JSON Data:")
#             logger.info("-" * 60)
#             print(summary_json)  # Print raw JSON to terminal
#             logger.info("-" * 60)
            
#             # Also save to file
#             self.save_to_file(summary_dict)
    
#     def save_to_file(self, summary_dict: Dict[str, Any]):
#         """Save session data to a JSON file"""
#         try:
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"quiz_session_{self.session_code}_{self.roll_number}_{timestamp}.json"
            
#             with open(filename, 'w') as f:
#                 json.dump(summary_dict, f, indent=2, default=str)
            
#             logger.info(f"💾 Session data saved to: {filename}")
#         except Exception as e:
#             logger.error(f"❌ Failed to save session data: {e}")


# # ============================================================================
# # Constants and Configuration
# # ============================================================================

# class FlowStateKeys:
#     """Keys used in flow manager state"""
#     SESSION_CODE = "session_code"
#     ROLL_NUMBER = "roll_number"
#     QUESTIONS = "questions"
#     CURRENT_QUESTION_INDEX = "current_question_index"
#     SCORE = "score"
#     TOTAL_QUESTIONS = "total_questions"
#     CURRENT_FORMATTED_QUESTION = "current_formatted_question"
#     CURRENT_QUESTION_NUMBER = "current_question_number"
#     LAST_IS_CORRECT = "last_is_correct"
#     LAST_CORRECT_ANSWER = "last_correct_answer"
#     LAST_ERROR = "last_error"
#     QUIZ_STARTED = "quiz_started"
#     RESPONSE_TRACKER = "response_tracker"  # New key for response tracker


# class NodeNames:
#     """Names for all flow nodes"""
#     WELCOME = "welcome"
#     ASK_SESSION_CODE = "ask_session_code"
#     ASK_ROLL_NUMBER = "ask_roll_number"
#     INVALID_SESSION = "invalid_session"
#     CONFIRM_START = "confirm_start"
#     ASK_QUESTION = "ask_question"
#     SPEAK_QUESTION = "speak_question"
#     FEEDBACK = "feedback"
#     CLARIFY_START = "clarify_start"
#     CLARIFY_PROCEED = "clarify_proceed"
#     CLARIFY_END = "clarify_end"
#     CONFIRM_STOP = "confirm_stop"
#     CONFIRM_DELAY = "confirm_delay"
#     QUIZ_COMPLETE = "quiz_complete"
#     GOODBYE = "goodbye"


# class ResponseKeywords:
#     """Keywords for user response analysis"""
#     POSITIVE = ["yes", "yeah", "yep", "sure", "ready", "start", "begin", 
#                 "go ahead", "proceed", "ok", "okay", "let's go", "go on", 
#                 "please", "continue", "next", "sure thing", "absolutely",
#                 "definitely", "of course", "certainly", "by all means"]
    
#     NEGATIVE = ["no", "nope", "stop", "wait", "pause", "not ready", 
#                 "not yet", "hold on", "later", "quit", "end", "exit",
#                 "finish", "done", "cancel", "abort", "terminate"]
    
#     CONTINUE = ["continue", "go back", "resume", "keep going", "not end",
#                 "carry on", "proceed", "move on", "advance"]
    
#     DELAY = ["break", "pause", "later", "wait", "rest", "take a break",
#              "need time", "moment please", "hold off"]


# # ============================================================================
# # API Service
# # ============================================================================

# class APIService:
#     """Service for handling API calls"""
    
#     def __init__(self, base_url: str = None):
#         self.base_url = base_url or os.getenv("NODE_API_URL", "http://localhost:3000")
#         self.timeout = aiohttp.ClientTimeout(total=10)
    
#     async def get_questions(self, session_code: str, roll_number: str) -> Dict[str, Any]:
#         """Get questions for a session with roll number"""
#         try:
#             url = f"{self.base_url}/api/sessions/{session_code}/questions"
#             params = {"rollNumber": roll_number} if roll_number else None
#             logger.info(f"🌐 Calling API: GET {url} with roll number: {roll_number}")
            
#             async with aiohttp.ClientSession(timeout=self.timeout) as session:
#                 async with session.get(url, params=params) as response:
#                     logger.info(f"📊 API Response Status: {response.status}")
                    
#                     if response.status == 200:
#                         data = await response.json()
#                         logger.info(f"✅ Got questions for session {session_code}")
                        
#                         # Check response format
#                         if isinstance(data, dict) and "data" in data:
#                             return {"status": "ok", "data": data["data"]}
#                         elif isinstance(data, list):
#                             return {"status": "ok", "data": data}
#                         else:
#                             logger.error(f"❌ Unexpected response format: {data}")
#                             return {"status": "error", "error": "Unexpected format"}
#                     elif response.status == 404:
#                         return {"status": "error", "error": "Session not found or invalid roll number"}
#                     elif response.status == 403:
#                         return {"status": "error", "error": "Access denied - invalid credentials"}
#                     else:
#                         error_text = await response.text()
#                         logger.error(f"❌ API error {response.status}: {error_text}")
#                         return {"status": "error", "error": f"API error: {response.status}"}
#         except Exception as e:
#             logger.error(f"❌ Error getting questions: {e}")
#             return {"status": "error", "error": str(e)}


# # ============================================================================
# # Type Definitions for Function Results
# # ============================================================================

# class SessionValidationResult(FlowResult):
#     """Result type for session validation"""
#     valid: bool
#     questions: list[Dict[str, Any]]
#     total_questions: int
#     roll_number: str = ""
#     session_code: str = ""


# class QuestionResult(FlowResult):
#     """Result type for question handling"""
#     question_index: int
#     question_text: str


# class AnswerResult(FlowResult):
#     """Result type for answer processing"""
#     question_index: int
#     user_answer: str
#     is_correct: bool
#     correct_answer: str
#     score: int


# class QuizCompleteResult(FlowResult):
#     """Result type for quiz completion"""
#     total_questions: int
#     correct_answers: int
#     score_percentage: float


# class MissingInfoResult(FlowResult):
#     """Result type for missing information collection"""
#     missing_fields: list[str]
#     collected_data: Dict[str, str]


# class ProceedResult(FlowResult):
#     """Result type for proceed confirmation"""
#     wants_to_proceed: bool
#     user_response: str


# # ============================================================================
# # Question Utilities
# # ============================================================================

# class QuestionFormatter:
#     """Utility for formatting quiz questions"""
    
#     @staticmethod
#     def format_for_speech(question_data: Dict[str, Any]) -> str:
#         """Format question for natural speech"""
#         question_text = question_data.get("question_text", "No question text")
#         options = question_data.get("question_options", [])
        
#         # Format options with letters for speech
#         letters = ["A", "B", "C", "D", "E", "F"]
#         formatted_options = []
        
#         for i, option in enumerate(options[:6]):
#             option_text = option.get("option_text", f"Option {i+1}")
#             formatted_options.append(f"{letters[i]}: {option_text}")
        
#         options_text = ", ".join(formatted_options)
        
#         return f"{question_text}. Your options are: {options_text}"
    
#     @staticmethod
#     def get_correct_answer(question_data: Dict[str, Any]) -> str:
#         """Get the correct answer for a question"""
#         options = question_data.get("question_options", [])
#         for option in options:
#             if option.get("is_correct", False):
#                 return option.get("option_text", "")
#         return ""
    
#     @staticmethod
#     def check_answer(user_answer: str, correct_answer: str, question_data: Dict[str, Any]) -> bool:
#         """Check if user's answer is correct"""
#         user_answer_lower = user_answer.lower().strip()
#         correct_answer_lower = correct_answer.lower()
        
#         # Check letter answers (A, B, C, etc.)
#         letters = ["a", "b", "c", "d", "e", "f"]
#         if user_answer_lower in letters:
#             index = letters.index(user_answer_lower)
#             options = question_data.get("question_options", [])
#             if index < len(options):
#                 selected_option = options[index]
#                 return selected_option.get("is_correct", False)
        
#         # Check exact text match
#         if user_answer_lower == correct_answer_lower:
#             return True
        
#         # Check partial match
#         if (user_answer_lower in correct_answer_lower or 
#             correct_answer_lower in user_answer_lower):
#             return True
        
#         return False


# class ResponseAnalyzer:
#     """Utility for analyzing user responses"""
    
#     @staticmethod
#     def contains_keywords(text: str, keyword_list: List[str]) -> bool:
#         """Check if text contains any of the keywords"""
#         text_lower = text.lower()
#         return any(keyword in text_lower for keyword in keyword_list)
    
#     @staticmethod
#     def is_positive_response(text: str) -> bool:
#         """Check if response is positive"""
#         return ResponseAnalyzer.contains_keywords(text, ResponseKeywords.POSITIVE)
    
#     @staticmethod
#     def is_negative_response(text: str) -> bool:
#         """Check if response is negative"""
#         return ResponseAnalyzer.contains_keywords(text, ResponseKeywords.NEGATIVE)
    
#     @staticmethod
#     def wants_to_continue(text: str) -> bool:
#         """Check if user wants to continue"""
#         return ResponseAnalyzer.contains_keywords(text, ResponseKeywords.CONTINUE)
    
#     @staticmethod
#     def wants_to_delay(text: str) -> bool:
#         """Check if user wants to delay"""
#         return ResponseAnalyzer.contains_keywords(text, ResponseKeywords.DELAY)


# # ============================================================================
# # Function Handlers (Updated with Response Tracking)
# # ============================================================================

# class FunctionHandlers:
#     """Collection of all function handlers"""
    
#     def __init__(self, api_service: APIService):
#         self.api_service = api_service
    
#     def _get_response_tracker(self, flow_manager: FlowManager) -> ResponseTracker:
#         """Get or create response tracker from flow state"""
#         tracker = flow_manager.state.get(FlowStateKeys.RESPONSE_TRACKER)
#         if not tracker:
#             tracker = ResponseTracker()
#             flow_manager.state[FlowStateKeys.RESPONSE_TRACKER] = tracker
#         return tracker
    
#     async def collect_missing_info(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[MissingInfoResult, NodeConfig]:
#         """Collect missing session info (session code or roll number)"""
#         session_code = args.get(FlowStateKeys.SESSION_CODE, "").strip().upper()
#         roll_number = args.get(FlowStateKeys.ROLL_NUMBER, "").strip()
        
#         logger.info(f"📝 Collecting info - Session: {session_code}, Roll: {roll_number}")
        
#         # Store what we have
#         if session_code:
#             flow_manager.state[FlowStateKeys.SESSION_CODE] = session_code
#         if roll_number:
#             flow_manager.state[FlowStateKeys.ROLL_NUMBER] = roll_number
        
#         # Check what's missing
#         missing = []
#         if not session_code:
#             missing.append("session code")
#         if not roll_number:
#             missing.append("roll number")
        
#         result = MissingInfoResult(
#             missing_fields=missing,
#             collected_data={
#                 FlowStateKeys.SESSION_CODE: session_code,
#                 FlowStateKeys.ROLL_NUMBER: roll_number
#             }
#         )
        
#         if not missing:
#             # Both provided, proceed to validation
#             logger.info("✅ Both session code and roll number provided, validating...")
#             return await self.validate_session(args, flow_manager)
        
#         # Determine which node to go to based on what's missing
#         if len(missing) == 2:
#             logger.info("❌ Missing both session code and roll number")
#             return result, NodeFactory.create_welcome_node()
#         elif "session code" in missing:
#             logger.info("❌ Missing session code")
#             return result, NodeFactory.create_ask_session_code_node()
#         else:  # missing roll number
#             logger.info("❌ Missing roll number")
#             return result, NodeFactory.create_ask_roll_number_node()
    
#     async def validate_session(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[SessionValidationResult, NodeConfig]:
#         """Validate session code and load questions"""
#         # Get from args first, then fall back to state
#         session_code: str = args.get(FlowStateKeys.SESSION_CODE, "").strip().upper()
#         roll_number: str = args.get(FlowStateKeys.ROLL_NUMBER, "").strip()
        
#         # If not in args, check state
#         if not session_code:
#             session_code = flow_manager.state.get(FlowStateKeys.SESSION_CODE, "")
#         if not roll_number:
#             roll_number = flow_manager.state.get(FlowStateKeys.ROLL_NUMBER, "")
        
#         logger.info(f"🔍 Validating session: {session_code} with roll number: {roll_number}")
        
#         if not session_code or not roll_number:
#             logger.error("❌ Missing session code or roll number")
#             result = SessionValidationResult(
#                 valid=False, 
#                 total_questions=0, 
#                 questions=[], 
#                 roll_number=roll_number,
#                 session_code=session_code
#             )
#             flow_manager.state[FlowStateKeys.LAST_ERROR] = "Please provide both session code and roll number"
#             return result, NodeFactory.create_invalid_session_node()
        
#         # Get questions from API with roll number
#         questions_result = await self.api_service.get_questions(session_code, roll_number)
        
#         if questions_result.get("status") == "ok" and "data" in questions_result:
#             questions = questions_result["data"]
            
#             if questions and len(questions) > 0:
#                 logger.info(f"✅ Loaded {len(questions)} questions for roll number {roll_number}")
                
#                 # Store in flow manager state
#                 flow_manager.state[FlowStateKeys.QUESTIONS] = questions
#                 flow_manager.state[FlowStateKeys.CURRENT_QUESTION_INDEX] = 0
#                 flow_manager.state[FlowStateKeys.SCORE] = 0
#                 flow_manager.state[FlowStateKeys.TOTAL_QUESTIONS] = len(questions)
#                 flow_manager.state[FlowStateKeys.ROLL_NUMBER] = roll_number
#                 flow_manager.state[FlowStateKeys.SESSION_CODE] = session_code
                
#                 # Initialize response tracker
#                 tracker = self._get_response_tracker(flow_manager)
#                 tracker.start_session(session_code, roll_number)
                
#                 result = SessionValidationResult(
#                     valid=True, 
#                     total_questions=len(questions), 
#                     questions=questions,
#                     roll_number=roll_number,
#                     session_code=session_code
#                 )
#                 # Go to confirmation node instead of directly to questions
#                 next_node = NodeFactory.create_confirm_start_node()
#                 return result, next_node
        
#         error_msg = questions_result.get("error", "Session validation failed")
#         logger.error(f"❌ Session validation failed: {error_msg}")
#         flow_manager.state[FlowStateKeys.LAST_ERROR] = error_msg
#         result = SessionValidationResult(
#             valid=False, 
#             total_questions=0, 
#             questions=[],
#             roll_number=roll_number,
#             session_code=session_code
#         )
#         return result, NodeFactory.create_invalid_session_node()
    
#     async def confirm_start_quiz(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[ProceedResult, NodeConfig]:
#         """Confirm user wants to start the quiz"""
#         user_response: str = args.get("response", "").strip().lower()
        
#         logger.info(f"🤔 User confirmation response: '{user_response}'")
        
#         if ResponseAnalyzer.is_positive_response(user_response):
#             logger.info("✅ User wants to start the quiz")
#             flow_manager.state[FlowStateKeys.QUIZ_STARTED] = True
#             result = ProceedResult(
#                 wants_to_proceed=True,
#                 user_response=user_response
#             )
#             return result, NodeFactory.create_ask_question_node()
#         elif ResponseAnalyzer.is_negative_response(user_response):
#             logger.info("❌ User doesn't want to start the quiz yet")
#             # Ask if they want to proceed later
#             next_node = NodeFactory.create_confirm_delay_node()
#             result = ProceedResult(
#                 wants_to_proceed=False,
#                 user_response=user_response
#             )
#             return result, next_node
#         else:
#             # Unclear response, ask again
#             logger.info(f"🤔 Unclear confirmation response: {user_response}")
#             next_node = NodeFactory.create_clarify_start_node()
#             result = ProceedResult(
#                 wants_to_proceed=False,
#                 user_response=user_response
#             )
#             return result, next_node
    
#     async def load_and_speak_question(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[QuestionResult, NodeConfig]:
#         """Load the current question and prepare to speak it"""
#         question_index = flow_manager.state.get(FlowStateKeys.CURRENT_QUESTION_INDEX, 0)
#         questions = flow_manager.state.get(FlowStateKeys.QUESTIONS, [])
#         total = flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0)
        
#         if question_index >= len(questions):
#             logger.info("🎉 No more questions")
#             return QuestionResult(
#                 question_index=question_index,
#                 question_text="Complete"
#             ), NodeFactory.create_quiz_complete_node()
        
#         current_question = questions[question_index]
#         question_num = question_index + 1
        
#         # Start tracking this question
#         tracker = self._get_response_tracker(flow_manager)
#         tracker.start_question(question_index, current_question)
        
#         # Format question for speech
#         formatted_question = QuestionFormatter.format_for_speech(current_question)
        
#         # Store formatted question in state so LLM can access it
#         flow_manager.state[FlowStateKeys.CURRENT_FORMATTED_QUESTION] = formatted_question
#         flow_manager.state[FlowStateKeys.CURRENT_QUESTION_NUMBER] = question_num
        
#         logger.info(f"📝 Loaded question {question_num}/{total}: {current_question.get('question_text', '')[:50]}...")
        
#         result = QuestionResult(
#             question_index=question_index,
#             question_text=formatted_question
#         )
        
#         # Move to speaking node
#         next_node = NodeFactory.create_speak_question_node()
        
#         return result, next_node
    
#     async def submit_answer(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[AnswerResult, NodeConfig]:
#         """Process user's answer"""
#         user_answer: str = args["answer"].strip()
        
#         # Get data from flow manager state
#         question_index: int = flow_manager.state.get(FlowStateKeys.CURRENT_QUESTION_INDEX, 0)
#         questions: list = flow_manager.state.get(FlowStateKeys.QUESTIONS, [])
#         score: int = flow_manager.state.get(FlowStateKeys.SCORE, 0)
        
#         logger.info(f"📝 Processing answer: '{user_answer}' for question {question_index + 1}")
        
#         current_question = questions[question_index]
#         correct_answer = QuestionFormatter.get_correct_answer(current_question)
        
#         # Check if answer is correct
#         is_correct = QuestionFormatter.check_answer(user_answer, correct_answer, current_question)
        
#         # Track the response
#         tracker = self._get_response_tracker(flow_manager)
#         response = tracker.record_response(user_answer, correct_answer, is_correct)
        
#         if response:
#             logger.info(f"⏱️ Response time: {response.response_time_seconds:.2f} seconds")
        
#         # Update score
#         if is_correct:
#             score += 1
#             flow_manager.state[FlowStateKeys.SCORE] = score
        
#         # Store feedback data
#         flow_manager.state[FlowStateKeys.LAST_IS_CORRECT] = is_correct
#         flow_manager.state[FlowStateKeys.LAST_CORRECT_ANSWER] = correct_answer
        
#         result = AnswerResult(
#             question_index=question_index,
#             user_answer=user_answer,
#             is_correct=is_correct,
#             correct_answer=correct_answer,
#             score=score
#         )
        
#         # Move to next question
#         next_index = question_index + 1
#         flow_manager.state[FlowStateKeys.CURRENT_QUESTION_INDEX] = next_index
        
#         # Determine next node
#         next_node = NodeFactory.create_feedback_node()
        
#         return result, next_node
    
#     async def proceed_to_next_question(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[ProceedResult, NodeConfig]:
#         """Check if user wants to proceed to next question or end quiz"""
#         user_response: str = args.get("response", "").strip().lower()
        
#         logger.info(f"🤔 User response: '{user_response}'")
        
#         if ResponseAnalyzer.is_positive_response(user_response):
#             logger.info(f"✅ User wants to continue to next question")
#             # Check if there are more questions
#             next_index = flow_manager.state.get(FlowStateKeys.CURRENT_QUESTION_INDEX, 0)
#             total_questions = flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0)
            
#             if next_index < total_questions:
#                 result = ProceedResult(
#                     wants_to_proceed=True,
#                     user_response=user_response
#                 )
#                 return result, NodeFactory.create_ask_question_node()
#             else:
#                 # No more questions, go to quiz complete
#                 logger.info("🎉 No more questions, going to quiz complete")
#                 result = ProceedResult(
#                     wants_to_proceed=True,
#                     user_response=user_response
#                 )
#                 return result, NodeFactory.create_quiz_complete_node()
                
#         elif ResponseAnalyzer.is_negative_response(user_response):
#             logger.info(f"❌ User wants to stop or pause")
#             # Ask if they want to end quiz completely
#             next_node = NodeFactory.create_confirm_stop_node()
#             result = ProceedResult(
#                 wants_to_proceed=False,
#                 user_response=user_response
#             )
#             return result, next_node
#         else:
#             # Unclear response, ask again
#             logger.info(f"🤔 Unclear response: {user_response}")
#             next_node = NodeFactory.create_clarify_proceed_node()
#             result = ProceedResult(
#                 wants_to_proceed=False,
#                 user_response=user_response
#             )
#             return result, next_node
    
#     async def confirm_end_quiz(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[QuizCompleteResult, NodeConfig]:
#         """Confirm user wants to end quiz"""
#         user_response: str = args.get("response", "").strip().lower()
        
#         if ResponseAnalyzer.is_positive_response(user_response) or ResponseAnalyzer.is_negative_response(user_response):
#             logger.info("✅ User confirmed to end quiz")
#             return await self.end_quiz(args, flow_manager)
#         elif ResponseAnalyzer.wants_to_continue(user_response):
#             # User wants to continue, go back to current question
#             logger.info("🔄 User wants to continue with quiz")
#             # Go back to feedback node to ask about next question again
#             result = QuizCompleteResult(
#                 total_questions=flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0),
#                 correct_answers=flow_manager.state.get(FlowStateKeys.SCORE, 0),
#                 score_percentage=0
#             )
#             return result, NodeFactory.create_feedback_node()
#         else:
#             # Unclear, ask again
#             logger.info(f"🤔 Unclear end quiz response: {user_response}")
#             next_node = NodeFactory.create_clarify_end_node()
#             result = QuizCompleteResult(
#                 total_questions=flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0),
#                 correct_answers=flow_manager.state.get(FlowStateKeys.SCORE, 0),
#                 score_percentage=0
#             )
#             return result, next_node
    
#     async def end_quiz(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[QuizCompleteResult, NodeConfig]:
#         """End the quiz"""
#         score = flow_manager.state.get(FlowStateKeys.SCORE, 0)
#         total = flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0)
        
#         logger.info(f"🏁 Quiz complete! Score: {score}/{total}")
        
#         # Log the complete session summary
#         tracker = self._get_response_tracker(flow_manager)
#         tracker.log_summary()
        
#         result = QuizCompleteResult(
#             total_questions=total,
#             correct_answers=score,
#             score_percentage=(score / total * 100) if total > 0 else 0
#         )
        
#         return result, NodeFactory.create_goodbye_node()


# # ============================================================================
# # Node Factory
# # ============================================================================

# class NodeFactory:
#     """Factory for creating node configurations"""
    
#     @staticmethod
#     def create_welcome_node() -> NodeConfig:
#         """Create the welcome node"""
#         return {
#             "name": NodeNames.WELCOME,
#             "role_messages": [
#                 {
#                     "role": "system",
#                     "content": "You are QuizMaster, a friendly and enthusiastic quiz host. You speak clearly and energetically. Be encouraging and maintain positive energy throughout."
#                 }
#             ],
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Welcome the user to the quiz! Introduce yourself as QuizMaster and explain you need two things to start:
# 1. Their session code (like H6TU)
# 2. Their roll number

# Start by asking for the session code first. You can say something like:
# "Welcome to QuizMaster! I'm excited to host your quiz today. To get started, I'll need two pieces of information. First, what's your session code?"

# Once they provide the session code, ask for their roll number. Then use the collect_missing_info function with both pieces of information.

# Once both are collected, I'll validate them and ask if you're ready to start."""
#                 }
#             ],
#             "functions": [FunctionSchemas.COLLECT_MISSING_INFO],
#         }
    
#     @staticmethod
#     def create_ask_session_code_node() -> NodeConfig:
#         """Create node to ask for session code"""
#         return {
#             "name": NodeNames.ASK_SESSION_CODE,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Ask the user for their session code. It's usually a 4-character code like H6TU.
# Say something like: "Great, now I need your session code. What's your session code?"

# Once they provide it, use the collect_missing_info function with the session code."""
#                 }
#             ],
#             "functions": [FunctionSchemas.COLLECT_MISSING_INFO],
#         }
    
#     @staticmethod
#     def create_ask_roll_number_node() -> NodeConfig:
#         """Create node to ask for roll number"""
#         return {
#             "name": NodeNames.ASK_ROLL_NUMBER,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Ask the user for their roll number (student ID).
# Say something like: "Thank you! Now I need your roll number. What's your roll number?"

# Once they provide it, use the collect_missing_info function with the roll number."""
#                 }
#             ],
#             "functions": [FunctionSchemas.COLLECT_MISSING_INFO],
#         }
    
#     @staticmethod
#     def create_invalid_session_node() -> NodeConfig:
#         """Create node for invalid session"""
#         return {
#             "name": NodeNames.INVALID_SESSION,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The session validation failed. Possible reasons:
# 1. Incorrect session code
# 2. Incorrect roll number
# 3. Session doesn't exist
# 4. Roll number not authorized for this session

# Check flow state for error details: {last_error}

# Politely inform the user there was an issue. Say something like:
# "I'm sorry, but I couldn't validate your credentials. Let's try again."

# Ask them to provide both their session code and roll number again, then use the collect_missing_info function."""
#                 }
#             ],
#             "functions": [FunctionSchemas.COLLECT_MISSING_INFO],
#         }
    
#     @staticmethod
#     def create_confirm_start_node() -> NodeConfig:
#         """Create node to confirm user wants to start the quiz"""
#         return {
#             "name": NodeNames.CONFIRM_START,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Perfect! Your session has been validated successfully.

# You have loaded: {total_questions} questions for roll number: {roll_number}

# Now ask the user if they're ready to start the quiz.
# Say something like: "Perfect! I've loaded {total_questions} questions for you. Are you ready to start the quiz now?"

# Wait for their response. If they say anything affirmative (yes, yeah, ready, start, begin, let's go, etc.), 
# use the confirm_start_quiz function with their response."""
#                 }
#             ],
#             "functions": [FunctionSchemas.CONFIRM_START_QUIZ],
#         }
    
#     @staticmethod
#     def create_clarify_start_node() -> NodeConfig:
#         """Create node to clarify start quiz response"""
#         return {
#             "name": NodeNames.CLARIFY_START,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user's response wasn't clear. Ask them again if they're ready to start the quiz.
#                     Say something like: "Sorry, I didn't catch that. Are you ready to start the quiz now? Please say yes or no."
                    
#                     Wait for their response. If they say "yes" or similar, use the confirm_start_quiz function again.
#                     If they say "no" or similar, ask if they want to delay or exit."""
#                 }
#             ],
#             "functions": [FunctionSchemas.CONFIRM_START_QUIZ],
#         }
    
#     @staticmethod
#     def create_ask_question_node() -> NodeConfig:
#         """Create node to prepare to ask a question"""
#         return {
#             "name": NodeNames.ASK_QUESTION,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Great! Let's begin the quiz. Say something encouraging like:
# "Excellent! Let's get started. Remember, speak clearly and choose your answers carefully. Good luck!"

# Then use the load_and_speak_question function to load and prepare the first question."""
#                 }
#             ],
#             "functions": [FunctionSchemas.LOAD_AND_SPEAK_QUESTION],
#         }
    
#     @staticmethod
#     def create_speak_question_node() -> NodeConfig:
#         """Create node to actually speak the question"""
#         return {
#             "name": NodeNames.SPEAK_QUESTION,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Now speak the quiz question to the user. The question has been loaded into the state:

# Question number: {current_question_number}
# Total questions: {total_questions}
# Formatted question: {current_formatted_question}

# SPEAK THIS OUT LOUD:
# "Question {current_question_number} of {total_questions}. {current_formatted_question}. What's your answer?"

# Make sure to read ALL the options clearly. The user is LISTENING, not reading."""
#                 }
#             ],
#             "functions": [FunctionSchemas.SUBMIT_ANSWER],
#         }
    
#     @staticmethod
#     def create_feedback_node() -> NodeConfig:
#         """Create feedback node - uses flow manager state"""
#         return {
#             "name": NodeNames.FEEDBACK,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Provide feedback on the user's answer using the flow state:
# - last_is_correct: {last_is_correct}
# - last_correct_answer: {last_correct_answer}
# - score: {score}
# - total_questions: {total_questions}
# - current_question_index: {current_question_index}

# If last_is_correct is True:
#   Say: "That's right! {last_correct_answer} is correct! Great job!"
# If last_is_correct is False:
#   Say: "Actually, the correct answer is {last_correct_answer}."

# Then say: "Your current score is {score} out of {total_questions}."

# Now ask: "Are you ready for the next question?"

# Wait for their response. If they say anything affirmative (yes, yeah, ready, continue, next, etc.), 
# use the proceed_to_next_question function with their response."""
#                 }
#             ],
#             "functions": [FunctionSchemas.PROCEED_TO_NEXT_QUESTION],
#         }
    
#     @staticmethod
#     def create_clarify_proceed_node() -> NodeConfig:
#         """Create node to clarify proceed response"""
#         return {
#             "name": NodeNames.CLARIFY_PROCEED,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user's response wasn't clear. Ask them again if they're ready for the next question.
#                     Say something like: "Sorry, I didn't catch that. Are you ready for the next question? Please say yes or no."
                    
#                     Wait for their response. If they say "yes" or similar, use the proceed_to_next_question function.
#                     If they say "no" or similar, ask if they want to end the quiz."""
#                 }
#             ],
#             "functions": [FunctionSchemas.PROCEED_TO_NEXT_QUESTION],
#         }
    
#     @staticmethod
#     def create_confirm_stop_node() -> NodeConfig:
#         """Create node to confirm stopping the quiz"""
#         return {
#             "name": NodeNames.CONFIRM_STOP,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user doesn't want to continue with the next question right now.
#                     Ask them if they want to end the quiz completely or just take a break.
#                     Say something like: "Would you like to end the quiz now, or would you like to take a break and continue later?"
                    
#                     If they say "end", "quit", "stop", "finish" or similar, use the confirm_end_quiz function.
#                     If they say "break", "pause", "later", "wait" etc., say: "Okay, I'll wait. Just say 'ready' when you want to continue." and wait for their response."""
#                 }
#             ],
#             "functions": [FunctionSchemas.CONFIRM_END_QUIZ],
#         }
    
#     @staticmethod
#     def create_confirm_delay_node() -> NodeConfig:
#         """Create node to confirm delaying the quiz"""
#         return {
#             "name": NodeNames.CONFIRM_DELAY,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user doesn't want to start the quiz right now.
#                     Ask them if they'd like to take a break and start later, or if they want to exit.
#                     Say something like: "Would you like to take a break and come back later, or would you prefer to exit the quiz?"
                    
#                     If they say "exit", "quit", "stop", "end" or similar, use the end_quiz function.
#                     If they say "break", "pause", "later", "wait" etc., say: "Okay, I'll wait. Just say 'ready' when you want to start the quiz." and wait for their response."""
#                 }
#             ],
#             "functions": [FunctionSchemas.END_QUIZ],
#         }
    
#     @staticmethod
#     def create_clarify_end_node() -> NodeConfig:
#         """Create node to clarify end quiz response"""
#         return {
#             "name": NodeNames.CLARIFY_END,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """The user's response wasn't clear. Ask them to clarify if they want to end the quiz or continue.
#                     Say something like: "Just to confirm, would you like to end the quiz now or continue with the next question? Please say 'end' or 'continue'."
                    
#                     If they say "end" or similar, use the confirm_end_quiz function.
#                     If they say "continue" or similar, go back to asking if they're ready for the next question."""
#                 }
#             ],
#             "functions": [FunctionSchemas.CONFIRM_END_QUIZ],
#         }
    
#     @staticmethod
#     def create_quiz_complete_node() -> NodeConfig:
#         """Create quiz completion node - uses flow manager state"""
#         return {
#             "name": NodeNames.QUIZ_COMPLETE,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": """Congratulations! The quiz is complete!

# Use the flow state to get:
# - score: {score}
# - total_questions: {total_questions}

# Calculate percentage = (score / total_questions) * 100

# If percentage >= 80:
#   Say: "Excellent work! You scored {score} out of {total_questions}! That's {percentage} percent!"
# If percentage >= 60:
#   Say: "Good job! You scored {score} out of {total_questions}. That's {percentage} percent."
# Else:
#   Say: "Thanks for playing! You scored {score} out of {total_questions}. That's {percentage} percent. Practice makes perfect!"

# Now ask: "Would you like to end the quiz now?"
# Wait for their response. If they say yes or similar, use the confirm_end_quiz function."""
#                 }
#             ],
#             "functions": [FunctionSchemas.CONFIRM_END_QUIZ],
#         }
    
#     @staticmethod
#     def create_goodbye_node() -> NodeConfig:
#         """Create goodbye node"""
#         return {
#             "name": NodeNames.GOODBYE,
#             "task_messages": [
#                 {
#                     "role": "system",
#                     "content": "Thank them warmly for playing the quiz and say goodbye! You can say something like: 'Thank you for playing! Have a great day!'"
#                 }
#             ],
#             "post_actions": [{"type": "end_conversation"}],
#         }


# # ============================================================================
# # Function Schemas
# # ============================================================================

# class FunctionSchemas:
#     """Collection of all function schemas"""
    
#     # Initialize API service
#     _api_service = APIService()
#     _handlers = FunctionHandlers(_api_service)
    
#     # Define all schemas
#     COLLECT_MISSING_INFO = FlowsFunctionSchema(
#         name="collect_missing_info",
#         description="Collect missing session information (session code or roll number)",
#         properties={
#             "session_code": {
#                 "type": "string",
#                 "description": "The session code provided by the user (e.g., H6TU)"
#             },
#             "roll_number": {
#                 "type": "string",
#                 "description": "The user's roll number (student ID)"
#             }
#         },
#         required=[],  # Not required since we might have partial info
#         handler=_handlers.collect_missing_info,
#     )
    
#     VALIDATE_SESSION = FlowsFunctionSchema(
#         name="validate_session",
#         description="Validate the session code and roll number and load quiz questions",
#         properties={
#             "session_code": {
#                 "type": "string",
#                 "description": "The session code provided by the user (e.g., H6TU)"
#             },
#             "roll_number": {
#                 "type": "string",
#                 "description": "The user's roll number (student ID)"
#             }
#         },
#         required=["session_code", "roll_number"],
#         handler=_handlers.validate_session,
#     )
    
#     CONFIRM_START_QUIZ = FlowsFunctionSchema(
#         name="confirm_start_quiz",
#         description="Confirm if user wants to start the quiz",
#         properties={
#             "response": {
#                 "type": "string",
#                 "description": "User's response to starting the quiz"
#             }
#         },
#         required=["response"],
#         handler=_handlers.confirm_start_quiz,
#     )
    
#     LOAD_AND_SPEAK_QUESTION = FlowsFunctionSchema(
#         name="load_and_speak_question",
#         description="Load the current question and speak it to the user",
#         properties={},
#         required=[],
#         handler=_handlers.load_and_speak_question,
#     )
    
#     SUBMIT_ANSWER = FlowsFunctionSchema(
#         name="submit_answer",
#         description="Submit the user's answer for the current question",
#         properties={
#             "answer": {
#                 "type": "string",
#                 "description": "The user's answer (letter A-F or full text)"
#             }
#         },
#         required=["answer"],
#         handler=_handlers.submit_answer,
#     )
    
#     PROCEED_TO_NEXT_QUESTION = FlowsFunctionSchema(
#         name="proceed_to_next_question",
#         description="Check if user wants to proceed to next question or end quiz",
#         properties={
#             "response": {
#                 "type": "string",
#                 "description": "The user's response to whether they're ready for next question"
#             }
#         },
#         required=["response"],
#         handler=_handlers.proceed_to_next_question,
#     )
    
#     CONFIRM_END_QUIZ = FlowsFunctionSchema(
#         name="confirm_end_quiz",
#         description="Confirm if user wants to end the quiz",
#         properties={
#             "response": {
#                 "type": "string",
#                 "description": "User's response to ending the quiz"
#             }
#         },
#         required=["response"],
#         handler=_handlers.confirm_end_quiz,
#     )
    
#     END_QUIZ = FlowsFunctionSchema(
#         name="end_quiz",
#         description="End the quiz and show final results",
#         properties={},
#         required=[],
#         handler=_handlers.end_quiz,
#     )
    
#     @classmethod
#     def get_all_schemas(cls) -> List[FlowsFunctionSchema]:
#         """Get all function schemas"""
#         return [
#             cls.COLLECT_MISSING_INFO,
#             cls.VALIDATE_SESSION,
#             cls.CONFIRM_START_QUIZ,
#             cls.LOAD_AND_SPEAK_QUESTION,
#             cls.SUBMIT_ANSWER,
#             cls.PROCEED_TO_NEXT_QUESTION,
#             cls.CONFIRM_END_QUIZ,
#             cls.END_QUIZ,
#         ]


# # ============================================================================
# # Quiz Bot
# # ============================================================================

# class QuizBot:
#     """Main quiz bot class"""
    
#     def __init__(self):
#         self.llm_config = {
#             "system_instruction": """You are QuizMaster, a friendly, enthusiastic quiz host. 
#             You speak clearly and energetically at a moderate pace.
#             You always read questions and options aloud exactly as provided.
#             You provide encouraging feedback after each answer.
#             You maintain a positive and engaging tone throughout the quiz.
#             This is a voice conversation - avoid special characters and emojis."""
#         }
    
#     async def run(self, websocket_client, session_code: Optional[str] = None):
#         """Run the quiz bot with flow management"""
#         logger.info("🤖 Starting Quiz Bot")
        
#         # Create WebSocket transport
#         ws_transport = FastAPIWebsocketTransport(
#             websocket=websocket_client,
#             params=FastAPIWebsocketParams(
#                 audio_in_enabled=True,
#                 audio_out_enabled=True,
#                 add_wav_header=False,
#                 vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.5)),
#                 serializer=ProtobufFrameSerializer(),
#             ),
#         )

#         # Create Gemini Multimodal Live LLM service
#         llm = GeminiLiveLLMService(
#             api_key=os.getenv("GOOGLE_API_KEY"),
#             config=self.llm_config
#         )

#         # Create conversation context
#         context = LLMContext()
#         context_aggregator = LLMContextAggregatorPair(context)

#         # RTVI for monitoring
#         rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

#         # Build the pipeline
#         pipeline = Pipeline(
#             [
#                 ws_transport.input(),
#                 rtvi,
#                 context_aggregator.user(),
#                 llm,
#                 ws_transport.output(),
#                 context_aggregator.assistant(),
#             ]
#         )

#         # Create pipeline task
#         task = PipelineTask(
#             pipeline,
#             params=PipelineParams(
#                 enable_metrics=True,
#                 enable_usage_metrics=True,
#                 allow_interruptions=True,
#             ),
#             observers=[RTVIObserver(rtvi)],
#         )

#         # Initialize flow manager
#         flow_manager = FlowManager(
#             task=task,
#             llm=llm,
#             context_aggregator=context_aggregator,
#             transport=ws_transport,
#         )

#         # Event handlers
#         @rtvi.event_handler("on_client_ready")
#         async def on_client_ready(rtvi):
#             logger.info("✅ Pipecat client ready.")
#             await rtvi.set_bot_ready()
#             # Initialize the flow with welcome node
#             await flow_manager.initialize(NodeFactory.create_welcome_node())

#         @ws_transport.event_handler("on_client_connected")
#         async def on_client_connected(transport, client):
#             logger.info("✅ Client connected via WebSocket")

#         @ws_transport.event_handler("on_client_disconnected")
#         async def on_client_disconnected(transport, client):
#             logger.info("❌ Client disconnected")
#             # Log session summary if quiz was started
#             tracker = flow_manager.state.get(FlowStateKeys.RESPONSE_TRACKER)
#             if tracker:
#                 logger.info("📊 Logging incomplete session data due to disconnection")
#                 tracker.log_summary()
#             await task.cancel()

#         # Create and run the pipeline runner
#         runner = PipelineRunner(handle_sigint=False)
        
#         try:
#             await runner.run(task)
#         except Exception as e:
#             logger.error(f"Error in pipeline: {e}")
#             # Log session summary on error
#             tracker = flow_manager.state.get(FlowStateKeys.RESPONSE_TRACKER)
#             if tracker:
#                 logger.info("📊 Logging session data due to error")
#                 tracker.log_summary()
#             raise


# # ============================================================================
# # Main Function
# # ============================================================================

# async def run_bot(websocket_client, session_code: Optional[str] = None):
#     """Main entry point for running the bot"""
#     bot = QuizBot()
#     await bot.run(websocket_client, session_code)

import os
import aiohttp
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime

from dotenv import load_dotenv
from loguru import logger
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
from pipecat.serializers.protobuf import ProtobufFrameSerializer
from pipecat.services.google.gemini_live.llm import GeminiLiveLLMService
from pipecat.transports.websocket.fastapi import (
    FastAPIWebsocketParams,
    FastAPIWebsocketTransport,
)

from pipecat_flows import (
    FlowArgs,
    FlowManager,
    FlowResult,
    FlowsFunctionSchema,
    NodeConfig,
)

load_dotenv(override=True)

# ============================================================================
# Simple Response Tracker
# ============================================================================

class ResponseTracker:
    """Simple tracker for user responses"""
    
    def __init__(self):
        self.responses = {}
        self.total_questions = 0
    
    def start_session(self, session_code: str, roll_number: str, total_questions: int):
        """Start tracking a new quiz session"""
        self.session_code = session_code
        self.roll_number = roll_number
        self.total_questions = total_questions
        self.responses = {}
        logger.info(f"📊 Starting response tracking for {session_code} - {roll_number}")
    
    def record_response(self, question_number: int, user_answer: str, correct_answer: str, is_correct: bool):
        """Record user's response for a question"""
        question_key = f"Q{question_number}"
        
        self.responses[question_key] = {
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        
        # Print current state of responses dictionary
        logger.info("=" * 50)
        logger.info("📝 CURRENT RESPONSES DICTIONARY:")
        logger.info("=" * 50)
        for key, value in self.responses.items():
            status = "✅" if value["is_correct"] else "❌"
            logger.info(f"{key}: {value['user_answer']} (Correct: {value['correct_answer']}) {status}")
        logger.info("-" * 50)
        logger.info(f"Total responses: {len(self.responses)}/{self.total_questions}")
        logger.info("=" * 50)
    
    def print_final_responses(self):
        """Print final responses dictionary"""
        logger.info("🎯 FINAL RESPONSES SUMMARY:")
        logger.info("=" * 60)
        logger.info(f"Session: {self.session_code}")
        logger.info(f"Roll Number: {self.roll_number}")
        logger.info(f"Total Questions: {self.total_questions}")
        logger.info(f"Questions Answered: {len(self.responses)}")
        logger.info("=" * 60)
        
        # Print the dictionary in a readable format
        logger.info("\n📋 Responses Dictionary:")
        for key, value in self.responses.items():
            status = "CORRECT" if value["is_correct"] else "INCORRECT"
            logger.info(f"{key}: {{")
            logger.info(f"  'user_answer': '{value['user_answer']}',")
            logger.info(f"  'correct_answer': '{value['correct_answer']}',")
            logger.info(f"  'is_correct': {value['is_correct']},")
            logger.info(f"  'timestamp': '{value['timestamp']}',")
            logger.info(f"  'status': '{status}'")
            logger.info("}")
        
        # Also print as JSON
        logger.info("\n📄 JSON Format:")
        print(json.dumps(self.responses, indent=2))
        logger.info("=" * 60)


# ============================================================================
# Constants and Configuration
# ============================================================================

class FlowStateKeys:
    """Keys used in flow manager state"""
    SESSION_CODE = "session_code"
    ROLL_NUMBER = "roll_number"
    QUESTIONS = "questions"
    CURRENT_QUESTION_INDEX = "current_question_index"
    TOTAL_QUESTIONS = "total_questions"
    CURRENT_FORMATTED_QUESTION = "current_formatted_question"
    CURRENT_QUESTION_NUMBER = "current_question_number"
    LAST_IS_CORRECT = "last_is_correct"
    LAST_CORRECT_ANSWER = "last_correct_answer"
    LAST_ERROR = "last_error"
    QUIZ_STARTED = "quiz_started"
    RESPONSE_TRACKER = "response_tracker"


class NodeNames:
    """Names for all flow nodes"""
    WELCOME = "welcome"
    ASK_SESSION_CODE = "ask_session_code"
    ASK_ROLL_NUMBER = "ask_roll_number"
    INVALID_SESSION = "invalid_session"
    CONFIRM_START = "confirm_start"
    ASK_QUESTION = "ask_question"
    SPEAK_QUESTION = "speak_question"
    FEEDBACK = "feedback"
    CLARIFY_START = "clarify_start"
    CLARIFY_PROCEED = "clarify_proceed"
    CLARIFY_END = "clarify_end"
    CONFIRM_STOP = "confirm_stop"
    CONFIRM_DELAY = "confirm_delay"
    QUIZ_COMPLETE = "quiz_complete"
    GOODBYE = "goodbye"


class ResponseKeywords:
    """Keywords for user response analysis"""
    POSITIVE = ["yes", "yeah", "yep", "sure", "ready", "start", "begin", 
                "go ahead", "proceed", "ok", "okay", "let's go", "go on", 
                "please", "continue", "next", "sure thing", "absolutely",
                "definitely", "of course", "certainly", "by all means"]
    
    NEGATIVE = ["no", "nope", "stop", "wait", "pause", "not ready", 
                "not yet", "hold on", "later", "quit", "end", "exit",
                "finish", "done", "cancel", "abort", "terminate"]
    
    CONTINUE = ["continue", "go back", "resume", "keep going", "not end",
                "carry on", "proceed", "move on", "advance"]
    
    DELAY = ["break", "pause", "later", "wait", "rest", "take a break",
             "need time", "moment please", "hold off"]


# ============================================================================
# API Service
# ============================================================================

class APIService:
    """Service for handling API calls"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("NODE_API_URL", "http://localhost:3000")
        self.timeout = aiohttp.ClientTimeout(total=10)
    
    async def get_questions(self, session_code: str, roll_number: str) -> Dict[str, Any]:
        """Get questions for a session with roll number"""
        try:
            url = f"{self.base_url}/api/sessions/{session_code}/questions"
            params = {"rollNumber": roll_number} if roll_number else None
            logger.info(f"🌐 Calling API: GET {url} with roll number: {roll_number}")
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params) as response:
                    logger.info(f"📊 API Response Status: {response.status}")
                    
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"✅ Got questions for session {session_code}")
                        
                        # Check response format
                        if isinstance(data, dict) and "data" in data:
                            return {"status": "ok", "data": data["data"]}
                        elif isinstance(data, list):
                            return {"status": "ok", "data": data}
                        else:
                            logger.error(f"❌ Unexpected response format: {data}")
                            return {"status": "error", "error": "Unexpected format"}
                    elif response.status == 404:
                        return {"status": "error", "error": "Session not found or invalid roll number"}
                    elif response.status == 403:
                        return {"status": "error", "error": "Access denied - invalid credentials"}
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ API error {response.status}: {error_text}")
                        return {"status": "error", "error": f"API error: {response.status}"}
        except Exception as e:
            logger.error(f"❌ Error getting questions: {e}")
            return {"status": "error", "error": str(e)}


# ============================================================================
# Type Definitions for Function Results
# ============================================================================

class SessionValidationResult(FlowResult):
    """Result type for session validation"""
    valid: bool
    questions: list[Dict[str, Any]]
    total_questions: int
    roll_number: str = ""
    session_code: str = ""


class QuestionResult(FlowResult):
    """Result type for question handling"""
    question_index: int
    question_text: str


class AnswerResult(FlowResult):
    """Result type for answer processing"""
    question_index: int
    user_answer: str
    is_correct: bool
    correct_answer: str


class QuizCompleteResult(FlowResult):
    """Result type for quiz completion"""
    total_questions: int


class MissingInfoResult(FlowResult):
    """Result type for missing information collection"""
    missing_fields: list[str]
    collected_data: Dict[str, str]


class ProceedResult(FlowResult):
    """Result type for proceed confirmation"""
    wants_to_proceed: bool
    user_response: str


# ============================================================================
# Question Utilities
# ============================================================================

class QuestionFormatter:
    """Utility for formatting quiz questions"""
    
    @staticmethod
    def format_for_speech(question_data: Dict[str, Any]) -> str:
        """Format question for natural speech"""
        question_text = question_data.get("question_text", "No question text")
        options = question_data.get("question_options", [])
        
        # Format options with letters for speech
        letters = ["A", "B", "C", "D", "E", "F"]
        formatted_options = []
        
        for i, option in enumerate(options[:6]):
            option_text = option.get("option_text", f"Option {i+1}")
            formatted_options.append(f"{letters[i]}: {option_text}")
        
        options_text = ", ".join(formatted_options)
        
        return f"{question_text}. Your options are: {options_text}"
    
    @staticmethod
    def get_correct_answer(question_data: Dict[str, Any]) -> str:
        """Get the correct answer for a question"""
        options = question_data.get("question_options", [])
        for option in options:
            if option.get("is_correct", False):
                return option.get("option_text", "")
        return ""
    
    @staticmethod
    def check_answer(user_answer: str, correct_answer: str, question_data: Dict[str, Any]) -> bool:
        """Check if user's answer is correct"""
        user_answer_lower = user_answer.lower().strip()
        correct_answer_lower = correct_answer.lower()
        
        # Check letter answers (A, B, C, etc.)
        letters = ["a", "b", "c", "d", "e", "f"]
        if user_answer_lower in letters:
            index = letters.index(user_answer_lower)
            options = question_data.get("question_options", [])
            if index < len(options):
                selected_option = options[index]
                return selected_option.get("is_correct", False)
        
        # Check exact text match
        if user_answer_lower == correct_answer_lower:
            return True
        
        # Check partial match
        if (user_answer_lower in correct_answer_lower or 
            correct_answer_lower in user_answer_lower):
            return True
        
        return False


class ResponseAnalyzer:
    """Utility for analyzing user responses"""
    
    @staticmethod
    def contains_keywords(text: str, keyword_list: List[str]) -> bool:
        """Check if text contains any of the keywords"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keyword_list)
    
    @staticmethod
    def is_positive_response(text: str) -> bool:
        """Check if response is positive"""
        return ResponseAnalyzer.contains_keywords(text, ResponseKeywords.POSITIVE)
    
    @staticmethod
    def is_negative_response(text: str) -> bool:
        """Check if response is negative"""
        return ResponseAnalyzer.contains_keywords(text, ResponseKeywords.NEGATIVE)
    
    @staticmethod
    def wants_to_continue(text: str) -> bool:
        """Check if user wants to continue"""
        return ResponseAnalyzer.contains_keywords(text, ResponseKeywords.CONTINUE)
    
    @staticmethod
    def wants_to_delay(text: str) -> bool:
        """Check if user wants to delay"""
        return ResponseAnalyzer.contains_keywords(text, ResponseKeywords.DELAY)


# ============================================================================
# Function Handlers
# ============================================================================

class FunctionHandlers:
    """Collection of all function handlers"""
    
    def __init__(self, api_service: APIService):
        self.api_service = api_service
    
    def _get_response_tracker(self, flow_manager: FlowManager) -> ResponseTracker:
        """Get or create response tracker from flow state"""
        tracker = flow_manager.state.get(FlowStateKeys.RESPONSE_TRACKER)
        if not tracker:
            tracker = ResponseTracker()
            flow_manager.state[FlowStateKeys.RESPONSE_TRACKER] = tracker
        return tracker
    
    async def collect_missing_info(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[MissingInfoResult, NodeConfig]:
        """Collect missing session info (session code or roll number)"""
        session_code = args.get(FlowStateKeys.SESSION_CODE, "").strip().upper()
        roll_number = args.get(FlowStateKeys.ROLL_NUMBER, "").strip()
        
        logger.info(f"📝 Collecting info - Session: {session_code}, Roll: {roll_number}")
        
        # Store what we have
        if session_code:
            flow_manager.state[FlowStateKeys.SESSION_CODE] = session_code
        if roll_number:
            flow_manager.state[FlowStateKeys.ROLL_NUMBER] = roll_number
        
        # Check what's missing
        missing = []
        if not session_code:
            missing.append("session code")
        if not roll_number:
            missing.append("roll number")
        
        result = MissingInfoResult(
            missing_fields=missing,
            collected_data={
                FlowStateKeys.SESSION_CODE: session_code,
                FlowStateKeys.ROLL_NUMBER: roll_number
            }
        )
        
        if not missing:
            # Both provided, proceed to validation
            logger.info("✅ Both session code and roll number provided, validating...")
            return await self.validate_session(args, flow_manager)
        
        # Determine which node to go to based on what's missing
        if len(missing) == 2:
            logger.info("❌ Missing both session code and roll number")
            return result, NodeFactory.create_welcome_node()
        elif "session code" in missing:
            logger.info("❌ Missing session code")
            return result, NodeFactory.create_ask_session_code_node()
        else:  # missing roll number
            logger.info("❌ Missing roll number")
            return result, NodeFactory.create_ask_roll_number_node()
    
    async def validate_session(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[SessionValidationResult, NodeConfig]:
        """Validate session code and load questions"""
        # Get from args first, then fall back to state
        session_code: str = args.get(FlowStateKeys.SESSION_CODE, "").strip().upper()
        roll_number: str = args.get(FlowStateKeys.ROLL_NUMBER, "").strip()
        
        # If not in args, check state
        if not session_code:
            session_code = flow_manager.state.get(FlowStateKeys.SESSION_CODE, "")
        if not roll_number:
            roll_number = flow_manager.state.get(FlowStateKeys.ROLL_NUMBER, "")
        
        logger.info(f"🔍 Validating session: {session_code} with roll number: {roll_number}")
        
        if not session_code or not roll_number:
            logger.error("❌ Missing session code or roll number")
            result = SessionValidationResult(
                valid=False, 
                total_questions=0, 
                questions=[], 
                roll_number=roll_number,
                session_code=session_code
            )
            flow_manager.state[FlowStateKeys.LAST_ERROR] = "Please provide both session code and roll number"
            return result, NodeFactory.create_invalid_session_node()
        
        # Get questions from API with roll number
        questions_result = await self.api_service.get_questions(session_code, roll_number)
        
        if questions_result.get("status") == "ok" and "data" in questions_result:
            questions = questions_result["data"]
            
            if questions and len(questions) > 0:
                logger.info(f"✅ Loaded {len(questions)} questions for roll number {roll_number}")
                
                # Store in flow manager state
                flow_manager.state[FlowStateKeys.QUESTIONS] = questions
                flow_manager.state[FlowStateKeys.CURRENT_QUESTION_INDEX] = 0
                flow_manager.state[FlowStateKeys.TOTAL_QUESTIONS] = len(questions)
                flow_manager.state[FlowStateKeys.ROLL_NUMBER] = roll_number
                flow_manager.state[FlowStateKeys.SESSION_CODE] = session_code
                
                # Initialize response tracker
                tracker = self._get_response_tracker(flow_manager)
                tracker.start_session(session_code, roll_number, len(questions))
                
                result = SessionValidationResult(
                    valid=True, 
                    total_questions=len(questions), 
                    questions=questions,
                    roll_number=roll_number,
                    session_code=session_code
                )
                # Go to confirmation node instead of directly to questions
                next_node = NodeFactory.create_confirm_start_node()
                return result, next_node
        
        error_msg = questions_result.get("error", "Session validation failed")
        logger.error(f"❌ Session validation failed: {error_msg}")
        flow_manager.state[FlowStateKeys.LAST_ERROR] = error_msg
        result = SessionValidationResult(
            valid=False, 
            total_questions=0, 
            questions=[],
            roll_number=roll_number,
            session_code=session_code
        )
        return result, NodeFactory.create_invalid_session_node()
    
    async def confirm_start_quiz(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[ProceedResult, NodeConfig]:
        """Confirm user wants to start the quiz"""
        user_response: str = args.get("response", "").strip().lower()
        
        logger.info(f"🤔 User confirmation response: '{user_response}'")
        
        if ResponseAnalyzer.is_positive_response(user_response):
            logger.info("✅ User wants to start the quiz")
            flow_manager.state[FlowStateKeys.QUIZ_STARTED] = True
            result = ProceedResult(
                wants_to_proceed=True,
                user_response=user_response
            )
            return result, NodeFactory.create_ask_question_node()
        elif ResponseAnalyzer.is_negative_response(user_response):
            logger.info("❌ User doesn't want to start the quiz yet")
            # Ask if they want to proceed later
            next_node = NodeFactory.create_confirm_delay_node()
            result = ProceedResult(
                wants_to_proceed=False,
                user_response=user_response
            )
            return result, next_node
        else:
            # Unclear response, ask again
            logger.info(f"🤔 Unclear confirmation response: {user_response}")
            next_node = NodeFactory.create_clarify_start_node()
            result = ProceedResult(
                wants_to_proceed=False,
                user_response=user_response
            )
            return result, next_node
    
    async def load_and_speak_question(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[QuestionResult, NodeConfig]:
        """Load the current question and prepare to speak it"""
        question_index = flow_manager.state.get(FlowStateKeys.CURRENT_QUESTION_INDEX, 0)
        questions = flow_manager.state.get(FlowStateKeys.QUESTIONS, [])
        total = flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0)
        
        if question_index >= len(questions):
            logger.info("🎉 No more questions")
            return QuestionResult(
                question_index=question_index,
                question_text="Complete"
            ), NodeFactory.create_quiz_complete_node()
        
        current_question = questions[question_index]
        question_num = question_index + 1
        
        # Format question for speech
        formatted_question = QuestionFormatter.format_for_speech(current_question)
        
        # Store formatted question in state so LLM can access it
        flow_manager.state[FlowStateKeys.CURRENT_FORMATTED_QUESTION] = formatted_question
        flow_manager.state[FlowStateKeys.CURRENT_QUESTION_NUMBER] = question_num
        
        logger.info(f"📝 Loaded question {question_num}/{total}: {current_question.get('question_text', '')[:50]}...")
        
        result = QuestionResult(
            question_index=question_index,
            question_text=formatted_question
        )
        
        # Move to speaking node
        next_node = NodeFactory.create_speak_question_node()
        
        return result, next_node
    
    async def submit_answer(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[AnswerResult, NodeConfig]:
        """Process user's answer"""
        user_answer: str = args["answer"].strip()
        
        # Get data from flow manager state
        question_index: int = flow_manager.state.get(FlowStateKeys.CURRENT_QUESTION_INDEX, 0)
        questions: list = flow_manager.state.get(FlowStateKeys.QUESTIONS, [])
        
        logger.info(f"📝 Processing answer: '{user_answer}' for question {question_index + 1}")
        
        current_question = questions[question_index]
        correct_answer = QuestionFormatter.get_correct_answer(current_question)
        
        # Check if answer is correct
        is_correct = QuestionFormatter.check_answer(user_answer, correct_answer, current_question)
        
        # Track the response in dictionary
        tracker = self._get_response_tracker(flow_manager)
        question_number = question_index + 1
        tracker.record_response(question_number, user_answer, correct_answer, is_correct)
        
        # Store feedback data
        flow_manager.state[FlowStateKeys.LAST_IS_CORRECT] = is_correct
        flow_manager.state[FlowStateKeys.LAST_CORRECT_ANSWER] = correct_answer
        
        result = AnswerResult(
            question_index=question_index,
            user_answer=user_answer,
            is_correct=is_correct,
            correct_answer=correct_answer
        )
        
        # Move to next question
        next_index = question_index + 1
        flow_manager.state[FlowStateKeys.CURRENT_QUESTION_INDEX] = next_index
        
        # Determine next node
        next_node = NodeFactory.create_feedback_node()
        
        return result, next_node
    
    async def proceed_to_next_question(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[ProceedResult, NodeConfig]:
        """Check if user wants to proceed to next question or end quiz"""
        user_response: str = args.get("response", "").strip().lower()
        
        logger.info(f"🤔 User response: '{user_response}'")
        
        if ResponseAnalyzer.is_positive_response(user_response):
            logger.info(f"✅ User wants to continue to next question")
            # Check if there are more questions
            next_index = flow_manager.state.get(FlowStateKeys.CURRENT_QUESTION_INDEX, 0)
            total_questions = flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0)
            
            if next_index < total_questions:
                result = ProceedResult(
                    wants_to_proceed=True,
                    user_response=user_response
                )
                return result, NodeFactory.create_ask_question_node()
            else:
                # No more questions, go to quiz complete
                logger.info("🎉 No more questions, going to quiz complete")
                result = ProceedResult(
                    wants_to_proceed=True,
                    user_response=user_response
                )
                return result, NodeFactory.create_quiz_complete_node()
                
        elif ResponseAnalyzer.is_negative_response(user_response):
            logger.info(f"❌ User wants to stop or pause")
            # Ask if they want to end quiz completely
            next_node = NodeFactory.create_confirm_stop_node()
            result = ProceedResult(
                wants_to_proceed=False,
                user_response=user_response
            )
            return result, next_node
        else:
            # Unclear response, ask again
            logger.info(f"🤔 Unclear response: {user_response}")
            next_node = NodeFactory.create_clarify_proceed_node()
            result = ProceedResult(
                wants_to_proceed=False,
                user_response=user_response
            )
            return result, next_node
    
    async def confirm_end_quiz(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[QuizCompleteResult, NodeConfig]:
        """Confirm user wants to end quiz"""
        user_response: str = args.get("response", "").strip().lower()
        
        if ResponseAnalyzer.is_positive_response(user_response) or ResponseAnalyzer.is_negative_response(user_response):
            logger.info("✅ User confirmed to end quiz")
            return await self.end_quiz(args, flow_manager)
        elif ResponseAnalyzer.wants_to_continue(user_response):
            # User wants to continue, go back to current question
            logger.info("🔄 User wants to continue with quiz")
            # Go back to feedback node to ask about next question again
            result = QuizCompleteResult(
                total_questions=flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0)
            )
            return result, NodeFactory.create_feedback_node()
        else:
            # Unclear, ask again
            logger.info(f"🤔 Unclear end quiz response: {user_response}")
            next_node = NodeFactory.create_clarify_end_node()
            result = QuizCompleteResult(
                total_questions=flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0)
            )
            return result, next_node
    
    async def end_quiz(self, args: FlowArgs, flow_manager: FlowManager) -> tuple[QuizCompleteResult, NodeConfig]:
        """End the quiz"""
        total = flow_manager.state.get(FlowStateKeys.TOTAL_QUESTIONS, 0)
        
        logger.info("🏁 Quiz complete!")
        
        # Print final responses dictionary
        tracker = self._get_response_tracker(flow_manager)
        tracker.print_final_responses()
        
        result = QuizCompleteResult(
            total_questions=total
        )
        
        return result, NodeFactory.create_goodbye_node()


# ============================================================================
# Node Factory
# ============================================================================

class NodeFactory:
    """Factory for creating node configurations"""
    
    @staticmethod
    def create_welcome_node() -> NodeConfig:
        """Create the welcome node"""
        return {
            "name": NodeNames.WELCOME,
            "role_messages": [
                {
                    "role": "system",
                    "content": "You are QuizMaster, a friendly and enthusiastic quiz host. You speak clearly and energetically. Be encouraging and maintain positive energy throughout."
                }
            ],
            "task_messages": [
                {
                    "role": "system",
                    "content": """Welcome the user to the quiz! Introduce yourself as QuizMaster and explain you need two things to start:
1. Their session code (like H6TU)
2. Their roll number

Start by asking for the session code first. You can say something like:
"Welcome to QuizMaster! I'm excited to host your quiz today. To get started, I'll need two pieces of information. First, what's your session code?"

Once they provide the session code, ask for their roll number. Then use the collect_missing_info function with both pieces of information.

Once both are collected, I'll validate them and ask if you're ready to start."""
                }
            ],
            "functions": [FunctionSchemas.COLLECT_MISSING_INFO],
        }
    
    @staticmethod
    def create_ask_session_code_node() -> NodeConfig:
        """Create node to ask for session code"""
        return {
            "name": NodeNames.ASK_SESSION_CODE,
            "task_messages": [
                {
                    "role": "system",
                    "content": """Ask the user for their session code. It's usually a 4-character code like H6TU.
Say something like: "Great, now I need your session code. What's your session code?"

Once they provide it, use the collect_missing_info function with the session code."""
                }
            ],
            "functions": [FunctionSchemas.COLLECT_MISSING_INFO],
        }
    
    @staticmethod
    def create_ask_roll_number_node() -> NodeConfig:
        """Create node to ask for roll number"""
        return {
            "name": NodeNames.ASK_ROLL_NUMBER,
            "task_messages": [
                {
                    "role": "system",
                    "content": """Ask the user for their roll number (student ID).
Say something like: "Thank you! Now I need your roll number. What's your roll number?"

Once they provide it, use the collect_missing_info function with the roll number."""
                }
            ],
            "functions": [FunctionSchemas.COLLECT_MISSING_INFO],
        }
    
    @staticmethod
    def create_invalid_session_node() -> NodeConfig:
        """Create node for invalid session"""
        return {
            "name": NodeNames.INVALID_SESSION,
            "task_messages": [
                {
                    "role": "system",
                    "content": """The session validation failed. Possible reasons:
1. Incorrect session code
2. Incorrect roll number
3. Session doesn't exist
4. Roll number not authorized for this session

Check flow state for error details: {last_error}

Politely inform the user there was an issue. Say something like:
"I'm sorry, but I couldn't validate your credentials. Let's try again."

Ask them to provide both their session code and roll number again, then use the collect_missing_info function."""
                }
            ],
            "functions": [FunctionSchemas.COLLECT_MISSING_INFO],
        }
    
    @staticmethod
    def create_confirm_start_node() -> NodeConfig:
        """Create node to confirm user wants to start the quiz"""
        return {
            "name": NodeNames.CONFIRM_START,
            "task_messages": [
                {
                    "role": "system",
                    "content": """Perfect! Your session has been validated successfully.

You have loaded: {total_questions} questions for roll number: {roll_number}

Now ask the user if they're ready to start the quiz.
Say something like: "Perfect! I've loaded {total_questions} questions for you. Are you ready to start the quiz now?"

Wait for their response. If they say anything affirmative (yes, yeah, ready, start, begin, let's go, etc.), 
use the confirm_start_quiz function with their response."""
                }
            ],
            "functions": [FunctionSchemas.CONFIRM_START_QUIZ],
        }
    
    @staticmethod
    def create_clarify_start_node() -> NodeConfig:
        """Create node to clarify start quiz response"""
        return {
            "name": NodeNames.CLARIFY_START,
            "task_messages": [
                {
                    "role": "system",
                    "content": """The user's response wasn't clear. Ask them again if they're ready to start the quiz.
                    Say something like: "Sorry, I didn't catch that. Are you ready to start the quiz now? Please say yes or no."
                    
                    Wait for their response. If they say "yes" or similar, use the confirm_start_quiz function again.
                    If they say "no" or similar, ask if they want to delay or exit."""
                }
            ],
            "functions": [FunctionSchemas.CONFIRM_START_QUIZ],
        }
    
    @staticmethod
    def create_ask_question_node() -> NodeConfig:
        """Create node to prepare to ask a question"""
        return {
            "name": NodeNames.ASK_QUESTION,
            "task_messages": [
                {
                    "role": "system",
                    "content": """Great! Let's begin the quiz. Say something encouraging like:
"Excellent! Let's get started. Remember, speak clearly and choose your answers carefully. Good luck!"

Then use the load_and_speak_question function to load and prepare the first question."""
                }
            ],
            "functions": [FunctionSchemas.LOAD_AND_SPEAK_QUESTION],
        }
    
    @staticmethod
    def create_speak_question_node() -> NodeConfig:
        """Create node to actually speak the question"""
        return {
            "name": NodeNames.SPEAK_QUESTION,
            "task_messages": [
                {
                    "role": "system",
                    "content": """Now speak the quiz question to the user. The question has been loaded into the state:

Question number: {current_question_number}
Total questions: {total_questions}
Formatted question: {current_formatted_question}

SPEAK THIS OUT LOUD:
"Question {current_question_number} of {total_questions}. {current_formatted_question}. What's your answer?"

Make sure to read ALL the options clearly. The user is LISTENING, not reading."""
                }
            ],
            "functions": [FunctionSchemas.SUBMIT_ANSWER],
        }
    
    @staticmethod
    def create_feedback_node() -> NodeConfig:
        """Create feedback node"""
        return {
            "name": NodeNames.FEEDBACK,
            "task_messages": [
                {
                    "role": "system",
                    "content": """Provide feedback on the user's answer using the flow state:
- last_is_correct: {last_is_correct}
- last_correct_answer: {last_correct_answer}

If last_is_correct is True:
  Say: "That's right! {last_correct_answer} is correct! Great job!"
If last_is_correct is False:
  Say: "Actually, the correct answer is {last_correct_answer}."

Now ask: "Are you ready for the next question?"

Wait for their response. If they say anything affirmative (yes, yeah, ready, continue, next, etc.), 
use the proceed_to_next_question function with their response."""
                }
            ],
            "functions": [FunctionSchemas.PROCEED_TO_NEXT_QUESTION],
        }
    
    @staticmethod
    def create_clarify_proceed_node() -> NodeConfig:
        """Create node to clarify proceed response"""
        return {
            "name": NodeNames.CLARIFY_PROCEED,
            "task_messages": [
                {
                    "role": "system",
                    "content": """The user's response wasn't clear. Ask them again if they're ready for the next question.
                    Say something like: "Sorry, I didn't catch that. Are you ready for the next question? Please say yes or no."
                    
                    Wait for their response. If they say "yes" or similar, use the proceed_to_next_question function.
                    If they say "no" or similar, ask if they want to end the quiz."""
                }
            ],
            "functions": [FunctionSchemas.PROCEED_TO_NEXT_QUESTION],
        }
    
    @staticmethod
    def create_confirm_stop_node() -> NodeConfig:
        """Create node to confirm stopping the quiz"""
        return {
            "name": NodeNames.CONFIRM_STOP,
            "task_messages": [
                {
                    "role": "system",
                    "content": """The user doesn't want to continue with the next question right now.
                    Ask them if they want to end the quiz completely or just take a break.
                    Say something like: "Would you like to end the quiz now, or would you like to take a break and continue later?"
                    
                    If they say "end", "quit", "stop", "finish" or similar, use the confirm_end_quiz function.
                    If they say "break", "pause", "later", "wait" etc., say: "Okay, I'll wait. Just say 'ready' when you want to continue." and wait for their response."""
                }
            ],
            "functions": [FunctionSchemas.CONFIRM_END_QUIZ],
        }
    
    @staticmethod
    def create_confirm_delay_node() -> NodeConfig:
        """Create node to confirm delaying the quiz"""
        return {
            "name": NodeNames.CONFIRM_DELAY,
            "task_messages": [
                {
                    "role": "system",
                    "content": """The user doesn't want to start the quiz right now.
                    Ask them if they'd like to take a break and start later, or if they want to exit.
                    Say something like: "Would you like to take a break and come back later, or would you prefer to exit the quiz?"
                    
                    If they say "exit", "quit", "stop", "end" or similar, use the end_quiz function.
                    If they say "break", "pause", "later", "wait" etc., say: "Okay, I'll wait. Just say 'ready' when you want to start the quiz." and wait for their response."""
                }
            ],
            "functions": [FunctionSchemas.END_QUIZ],
        }
    
    @staticmethod
    def create_clarify_end_node() -> NodeConfig:
        """Create node to clarify end quiz response"""
        return {
            "name": NodeNames.CLARIFY_END,
            "task_messages": [
                {
                    "role": "system",
                    "content": """The user's response wasn't clear. Ask them to clarify if they want to end the quiz or continue.
                    Say something like: "Just to confirm, would you like to end the quiz now or continue with the next question? Please say 'end' or 'continue'."
                    
                    If they say "end" or similar, use the confirm_end_quiz function.
                    If they say "continue" or similar, go back to asking if they're ready for the next question."""
                }
            ],
            "functions": [FunctionSchemas.CONFIRM_END_QUIZ],
        }
    
    @staticmethod
    def create_quiz_complete_node() -> NodeConfig:
        """Create quiz completion node"""
        return {
            "name": NodeNames.QUIZ_COMPLETE,
            "task_messages": [
                {
                    "role": "system",
                    "content": """Congratulations! The quiz is complete!

Say something like: "Well done! You've completed all the questions."

Now ask: "Would you like to end the quiz now?"
Wait for their response. If they say yes or similar, use the confirm_end_quiz function."""
                }
            ],
            "functions": [FunctionSchemas.CONFIRM_END_QUIZ],
        }
    
    @staticmethod
    def create_goodbye_node() -> NodeConfig:
        """Create goodbye node"""
        return {
            "name": NodeNames.GOODBYE,
            "task_messages": [
                {
                    "role": "system",
                    "content": "Thank them warmly for playing the quiz and say goodbye! You can say something like: 'Thank you for playing! Have a great day!'"
                }
            ],
            "post_actions": [{"type": "end_conversation"}],
        }


# ============================================================================
# Function Schemas
# ============================================================================

class FunctionSchemas:
    """Collection of all function schemas"""
    
    # Initialize API service
    _api_service = APIService()
    _handlers = FunctionHandlers(_api_service)
    
    # Define all schemas
    COLLECT_MISSING_INFO = FlowsFunctionSchema(
        name="collect_missing_info",
        description="Collect missing session information (session code or roll number)",
        properties={
            "session_code": {
                "type": "string",
                "description": "The session code provided by the user (e.g., H6TU)"
            },
            "roll_number": {
                "type": "string",
                "description": "The user's roll number (student ID)"
            }
        },
        required=[],  # Not required since we might have partial info
        handler=_handlers.collect_missing_info,
    )
    
    VALIDATE_SESSION = FlowsFunctionSchema(
        name="validate_session",
        description="Validate the session code and roll number and load quiz questions",
        properties={
            "session_code": {
                "type": "string",
                "description": "The session code provided by the user (e.g., H6TU)"
            },
            "roll_number": {
                "type": "string",
                "description": "The user's roll number (student ID)"
            }
        },
        required=["session_code", "roll_number"],
        handler=_handlers.validate_session,
    )
    
    CONFIRM_START_QUIZ = FlowsFunctionSchema(
        name="confirm_start_quiz",
        description="Confirm if user wants to start the quiz",
        properties={
            "response": {
                "type": "string",
                "description": "User's response to starting the quiz"
            }
        },
        required=["response"],
        handler=_handlers.confirm_start_quiz,
    )
    
    LOAD_AND_SPEAK_QUESTION = FlowsFunctionSchema(
        name="load_and_speak_question",
        description="Load the current question and speak it to the user",
        properties={},
        required=[],
        handler=_handlers.load_and_speak_question,
    )
    
    SUBMIT_ANSWER = FlowsFunctionSchema(
        name="submit_answer",
        description="Submit the user's answer for the current question",
        properties={
            "answer": {
                "type": "string",
                "description": "The user's answer (letter A-F or full text)"
            }
        },
        required=["answer"],
        handler=_handlers.submit_answer,
    )
    
    PROCEED_TO_NEXT_QUESTION = FlowsFunctionSchema(
        name="proceed_to_next_question",
        description="Check if user wants to proceed to next question or end quiz",
        properties={
            "response": {
                "type": "string",
                "description": "The user's response to whether they're ready for next question"
            }
        },
        required=["response"],
        handler=_handlers.proceed_to_next_question,
    )
    
    CONFIRM_END_QUIZ = FlowsFunctionSchema(
        name="confirm_end_quiz",
        description="Confirm if user wants to end the quiz",
        properties={
            "response": {
                "type": "string",
                "description": "User's response to ending the quiz"
            }
        },
        required=["response"],
        handler=_handlers.confirm_end_quiz,
    )
    
    END_QUIZ = FlowsFunctionSchema(
        name="end_quiz",
        description="End the quiz and log all responses",
        properties={},
        required=[],
        handler=_handlers.end_quiz,
    )
    
    @classmethod
    def get_all_schemas(cls) -> List[FlowsFunctionSchema]:
        """Get all function schemas"""
        return [
            cls.COLLECT_MISSING_INFO,
            cls.VALIDATE_SESSION,
            cls.CONFIRM_START_QUIZ,
            cls.LOAD_AND_SPEAK_QUESTION,
            cls.SUBMIT_ANSWER,
            cls.PROCEED_TO_NEXT_QUESTION,
            cls.CONFIRM_END_QUIZ,
            cls.END_QUIZ,
        ]


# ============================================================================
# Quiz Bot
# ============================================================================

class QuizBot:
    """Main quiz bot class"""
    
    def __init__(self):
        self.llm_config = {
            "system_instruction": """You are QuizMaster, a friendly, enthusiastic quiz host. 
            You speak clearly and energetically at a moderate pace.
            You always read questions and options aloud exactly as provided.
            You provide encouraging feedback after each answer.
            You maintain a positive and engaging tone throughout the quiz.
            This is a voice conversation - avoid special characters and emojis."""
        }
    
    async def run(self, websocket_client, session_code: Optional[str] = None):
        """Run the quiz bot with flow management"""
        logger.info("🤖 Starting Quiz Bot")
        
        # Create WebSocket transport
        ws_transport = FastAPIWebsocketTransport(
            websocket=websocket_client,
            params=FastAPIWebsocketParams(
                audio_in_enabled=True,
                audio_out_enabled=True,
                add_wav_header=False,
                vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.5)),
                serializer=ProtobufFrameSerializer(),
            ),
        )

        # Create Gemini Multimodal Live LLM service
        llm = GeminiLiveLLMService(
            api_key=os.getenv("GOOGLE_API_KEY"),
            config=self.llm_config
        )

        # Create conversation context
        context = LLMContext()
        context_aggregator = LLMContextAggregatorPair(context)

        # RTVI for monitoring
        rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

        # Build the pipeline
        pipeline = Pipeline(
            [
                ws_transport.input(),
                rtvi,
                context_aggregator.user(),
                llm,
                ws_transport.output(),
                context_aggregator.assistant(),
            ]
        )

        # Create pipeline task
        task = PipelineTask(
            pipeline,
            params=PipelineParams(
                enable_metrics=True,
                enable_usage_metrics=True,
                allow_interruptions=True,
            ),
            observers=[RTVIObserver(rtvi)],
        )

        # Initialize flow manager
        flow_manager = FlowManager(
            task=task,
            llm=llm,
            context_aggregator=context_aggregator,
            transport=ws_transport,
        )

        # Event handlers
        @rtvi.event_handler("on_client_ready")
        async def on_client_ready(rtvi):
            logger.info("✅ Pipecat client ready.")
            await rtvi.set_bot_ready()
            # Initialize the flow with welcome node
            await flow_manager.initialize(NodeFactory.create_welcome_node())

        @ws_transport.event_handler("on_client_connected")
        async def on_client_connected(transport, client):
            logger.info("✅ Client connected via WebSocket")

        @ws_transport.event_handler("on_client_disconnected")
        async def on_client_disconnected(transport, client):
            logger.info("❌ Client disconnected")
            # Print responses if quiz was started
            tracker = flow_manager.state.get(FlowStateKeys.RESPONSE_TRACKER)
            if tracker and tracker.responses:
                logger.info("📊 Printing responses due to disconnection")
                tracker.print_final_responses()
            await task.cancel()

        # Create and run the pipeline runner
        runner = PipelineRunner(handle_sigint=False)
        
        try:
            await runner.run(task)
        except Exception as e:
            logger.error(f"Error in pipeline: {e}")
            # Print responses on error
            tracker = flow_manager.state.get(FlowStateKeys.RESPONSE_TRACKER)
            if tracker and tracker.responses:
                logger.info("📊 Printing responses due to error")
                tracker.print_final_responses()
            raise


# ============================================================================
# Main Function
# ============================================================================

async def run_bot(websocket_client, session_code: Optional[str] = None):
    """Main entry point for running the bot"""
    bot = QuizBot()
    await bot.run(websocket_client, session_code)