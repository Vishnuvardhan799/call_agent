✅ **1. Prerequisites**


Before doing anything:

- Python 3.9+ should be installed.
- pip should be available.


Make sure your working directory contains:
- inbound_trunk.py
- dispatch_rule.py
- agent.py
- requirements.txt
- .env file (with the needed API keys and config values)

<br><br>
✅ **2. Set Up Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
<br><br>
✅ **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

💡 _This includes LiveKit, OpenAI plugins, Silero VAD, Twilio, and dotenv._

<br><br>

✅ **4. Configure .env File**

Make sure your .env contains:

```bash
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_SECRET_KEY=your_livekit_secret
TWIML_USERNAME=your_twiml_username
TWIML_PASSWORD=your_twiml_password
OPENAI_API_KEY=your_openai_key
```
<br><br>
✅ **5. Register the SIP Inbound Trunk**

Run this only **once** to create the trunk in LiveKit.

```bash
python3 inbound_trunk.py
```

_This sets up the SIP trunk inside your LiveKit environment using your .env credentials._

<br><br>
✅ **6. Register the SIP Dispatch Rule**

Run this **after** the trunk is created.

```bash
python3 dispatch_rule.py
```

_This configures how inbound calls get routed (e.g., to inbound_agent)._

<br><br>
✅ **7. Repeat steps 2 to 6 for agent folder**

<br><br>
✅ **8. Start the Voice Agent**

This is the AI voice assistant that will handle the call.

```bash
python3 agent.py dev
```

_This file loads the instructions.txt, joins the room, listens using STT, processes using OpenAI, and replies via TTS._

<br><br>
🙏 **Credits**
[LiveKit](https://livekit.io/)
[Twilio](https://www.twilio.com/en-us)
[OpenAI](https://platform.openai.com/)
