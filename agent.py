from __future__ import annotations
import os 
import logging
from livekit import rtc
from livekit.agents import (
    AutoSubscribe, JobContext, WorkerOptions, cli, function_tool, Agent, RunContext
)
from livekit.agents import AgentSession
from livekit.plugins import google, silero, deepgram
from dotenv import load_dotenv
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from db import DatabaseDriver
from typing import List, Dict, Any

load_dotenv()

db_driver = DatabaseDriver()

class OrderAgent(Agent):
    def __init__(self):
        super().__init__(instructions=AGENT_INSTRUCTION)

    @function_tool()
    async def create_order(self, context: RunContext, name: str, phone: str, address: str, items: List[Dict[str, Any]]):
        """
        Saves a customer's order to the database.

        Args:
            name: The customer's full name.
            phone: The customer's phone number.
            address: The customer's full delivery address.
            items: A list of items being ordered. Each item should be a dictionary
                   with "name", "quantity", and "price".
                   Example: [{{"name": "Chicken Biryani", "quantity": 1, "price": 280}}]
        """
        logging.info(f"Creating order for {name} with items: {items}")
        db_driver.create_order(name=name, phone=phone, address=address, items=items)
        return "Order has been successfully created in the database."

# Initialize the logger for the agent
log = logging.getLogger("voice_agent")
log.setLevel(logging.INFO)

async def main_entry(ctx: JobContext):
    log.info("Initiating the entry point")

    google_api_key = os.getenv("GOOGLE_API_KEY")
    deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")

    if not deepgram_api_key:
        log.error("DEEPGRAM_API_KEY is not set. Deepgram STT/TTS will fail to connect. Exiting early.")
        return
    if not google_api_key:
        log.warning("GOOGLE_API_KEY is not set. Google LLM may fail to initialize.")

    # Connect to the room (audio only)
    await ctx.connect()

    agent = OrderAgent()

    # Create session with components
    session = AgentSession(
        stt=deepgram.STT(api_key=deepgram_api_key) if deepgram_api_key else deepgram.STT(),
        llm=google.LLM(
            model="gemini-2.0-flash-exp",
            api_key=google_api_key,
        ),
        tts=deepgram.TTS(api_key=deepgram_api_key) if deepgram_api_key else deepgram.TTS(),
        vad=silero.VAD.load(),
    )

    # Run the agent inside the room
    await session.start(room=ctx.room, agent=agent)
    await session.say(
        "Hello, welcome to Bawarchi Restaurant. How may I help you today?",
        allow_interruptions=True,
    )

if __name__ == "__main__":
    log.info("About to run main")
    #Run the agent, giving it the name "inbound-agent"
    cli.run_app(WorkerOptions(entrypoint_fnc=main_entry, agent_name="inbound_agent"))