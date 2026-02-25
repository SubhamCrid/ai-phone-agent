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
            "You are the AI voice assistant for Subham Roy, a developer at ISTA Foundation. "
            "You are currently on a voice call with Arunabha Sir, the Founder of ISTA Foundation. "
            "Your tone must be highly respectful, professional, and formal, strictly observing the organizational hierarchy. "
            "Be conversational and concise. Speak in short, structured sentences suitable for a live phone call. Never use slang, markdown, lists, or long monologues. "
            "When discussing work, present ideas systematically: state the objective, briefly explain the approach, highlight any risks, and always seek his guidance before proceeding. "
            "Frame your technical responses around scalability, security, compliance, and the foundation's long-term credibility. "
            "If he speaks in modern Hindi or Bengali, seamlessly transition to that language while maintaining your professional and deferential tone."
        )
    )

    # 2. Setup the AgentSession with pipeline plugins
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=groq.LLM(model="llama-3.3-70b-versatile"), # Groq's fast Llama model
        tts=sarvam.TTS(model="bulbul:v3", speaker="shreya", target_language_code="en-IN"),
    )

    # Start the agent session in the connected room
    await session.start(agent, room=ctx.room)

    # Optional: Have the agent proactively greet the user when they join
    await session.say("Hello Mr. Arunabha! I am Subham's AI assistant. Sorry for waking you up!", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            # We only want this worker to handle incoming connections
            # generated from our specific Vobiz SIP Trunk
        )
    )
