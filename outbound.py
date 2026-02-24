import os
import asyncio
from dotenv import load_dotenv
from livekit.api import LiveKitAPI, CreateSIPParticipantRequest

load_dotenv()

async def create_outbound_call():
    print("Initiating outbound call via Vobiz...")
    
    # 1. Provide your recipient number (your cell phone)
    to_number = os.getenv("SIP_TO_NUMBER")
    
    # 2. Your Vobiz SIP Trunk Outbound URI (You will get this from the Vobiz dashboard)
    # It usually looks like 'sip:<number>@vobiz.sip.trunk.domain'
    sip_trunk_id = os.getenv("SIP_TRUNK_ID") # The ID of the SIP Trunk in your LiveKit Dashboard

    api = LiveKitAPI(
        url=os.environ.get("LIVEKIT_URL"),
        api_key=os.environ.get("LIVEKIT_API_KEY"),
        api_secret=os.environ.get("LIVEKIT_API_SECRET"),
    )

    try:
        req = CreateSIPParticipantRequest(
            sip_trunk_id=sip_trunk_id,
            sip_call_to=to_number,
            room_name="demo-room",
            participant_identity=to_number,
            participant_name="Human Caller"
        )
        participant = await api.sip.create_sip_participant(req)
        print(f"✅ Call Initiated. Participant ID: {participant.participant_id}")
        
    except Exception as e:
         print(f"❌ Error initiating call: {e}")
    finally:
         await api.aclose()

if __name__ == "__main__":
    asyncio.run(create_outbound_call())
