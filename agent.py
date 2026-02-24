import os
import asyncio
from dotenv import load_dotenv

from livekit.agents import AutoSubscribe, JobContext, JobProcess, WorkerOptions, cli, llm
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import deepgram, groq, sarvam, silero

load_dotenv()

async def entrypoint(ctx: JobContext):
    # Connect to the LiveKit room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Initializing the voice pipeline agent session
    # We use Silero for Voice Activity Detection (VAD)
    # Deepgram for Speech-to-Text (STT)
    # Groq for the Language Model (LLM)
    # Sarvam AI for Text-to-Speech (TTS)
    
    # 1. Provide instructions to the Agent
    agent = Agent(
        instructions=(
            "You are a helpful and friendly AI assistant. "
            "You are speaking to a human over the phone. "
            "Keep your responses concise, conversational, and natural. "
            "Avoid outputting markdown, lists, or long monologues."
        )
    )

    # 2. Setup the AgentSession with pipeline plugins
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=groq.LLM(model="llama-3.1-8b-instant"), # Groq's fast Llama model
        tts=sarvam.TTS(target_language_code="en-IN"),
    )

    # Start the agent session in the connected room
    await session.start(agent, room=ctx.room)

    # Optional: Have the agent proactively greet the user when they join
    await session.say("Hello! How can I help you today?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            # We only want this worker to handle incoming connections
            # generated from our specific Vobiz SIP Trunk
        )
    )
