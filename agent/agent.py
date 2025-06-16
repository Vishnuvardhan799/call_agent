from __future__ import annotations
import os 
import logging
from livekit import rtc
from livekit.agents import ( AutoSubscribe, JobContext, WorkerOptions, cli, llm, )
from livekit.agents import AgentSession, Agent
from livekit.plugins import openai, silero
from dotenv import load_dotenv

load_dotenv()

# Initialize the logger for the agent
log = logging.getLogger("voice_agent")
log.setLevel(logging.INFO)

# Load the instructions for the AI model
instructions_doc = open("instructions.txt", "r").read()
log.info(f"Instructions: {instructions_doc}")

async def main_entry(ctx: JobContext):
    log.info("Initiating the entry point")

    openai_api_key = os.getenv("OPENAI_API_KEY")
    api_key = os.getenv("LIVEKIT_API_KEY")

    # Connect to the room (audio only)
    await ctx.connect()
    #log.info(f"Agent joined room: {ctx.room} with identity: {ctx.identity}")

    # Create session with components
    session = AgentSession(
        stt=openai.stt.STT(
            model="whisper-1",
            language="en",
            api_key=openai_api_key
        ),
        llm=openai.realtime.RealtimeModel(
            voice = "shimmer",
            temperature=0.8,
            api_key=openai_api_key,
        ),
        tts=openai.TTS(api_key=openai_api_key, voice="shimmer"),
        vad=silero.VAD.load()
    )

    # Run the agent inside the room
    await session.start(room=ctx.room, agent=Agent(instructions=instructions_doc))
    await session.say(
        "Hello, this is Clearpath Medical. How may I help you today?",
        allow_interruptions=False,
    )

if __name__ == "__main__":
    log.info("About to run main")
    #Run the agent, giving it the name "inbound-agent"
    cli.run_app(WorkerOptions(entrypoint_fnc=main_entry, agent_name="inbound_agent"))