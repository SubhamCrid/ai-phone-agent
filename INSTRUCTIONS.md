# Instructions: Configuring Vobiz and LiveKit

To connect your Vobiz phone number to your LiveKit agent, you need to set up a SIP trunk. Since your current Vobiz number is a trial number that only supports **outbound calls**, the instructions below focus on setting up LiveKit to handle the audio routing, and how you will initiate an outbound call.

## Step 1: Create a LiveKit Cloud Project

1. Go to [LiveKit Cloud](https://cloud.livekit.io/) and sign up for a free account.
2. Create a new "Project".
3. In your project settings, generate your API Keys.
4. Copy the `LIVEKIT_URL`, `API Key`, and `API Secret` into the `.env` file in this project folder.

## Step 2: Configure LiveKit SIP Inbound (For when you upgrade Vobiz)

_Note: This is required if you want people to call YOU._

1. In your LiveKit Cloud dashboard, navigate to **SIP**.
2. Create a new **SIP Inbound Trunk**.
3. LiveKit will give you a list of SIP URIs (e.g., `sip:xyz@sip.livekit.cloud`).
4. Go to your Vobiz Dashboard. Under "SIP Trunks" or "Forwarding", enter the LiveKit SIP URI.
5. In LiveKit, create a **SIP Dispatch Rule** that sends incoming SIP traffic to a Specific Room (e.g., "demo-room").

## Step 3: Getting Your API Keys (Detailed Steps)

You will need 4 free accounts to make this work. Here is exactly how to get each key:

### A. LiveKit API Key (The Orchestrator)

1. Go to [LiveKit Cloud](https://cloud.livekit.io/) and click "Sign Up" via Github or Google.
2. Once logged in, click **Create Project** (name it whatever you want).
3. On the left sidebar of your new project, click **Settings**, then click **Keys**.
4. Click **Add New Key**.
5. It will reveal two strings: an **API Key** (e.g., `APIxxxxx`) and an **API Secret**.
6. In your `ai-phone-agent` folder, rename the file `.env.example` to just `.env`.
7. Paste the API Key and API Secret into the `.env` file where it says `<your-api-key>` and `<your-api-secret>`.
8. Also on the dashboard home screen, find your **WebSocket URL** (looks like `wss://project-name.livekit.cloud`) and paste it into `LIVEKIT_URL` in the `.env` file.

### B. Deepgram API Key (Speech-to-Text)

1. Go to [Deepgram Console](https://console.deepgram.com/) and sign up. You will instantly get $200 in free credit.
2. Once logged in, look at the left sidebar and click **API Keys**.
3. Click the **Create a New API Key** button in the top right.
4. Name it "Phone Agent" and assign it the "Member" role.
5. Copy the long string it gives you and paste it into the `DEEPGRAM_API_KEY` slot in your `.env` file. _(Note: You can only see this key once!)_

### C. Groq API Key (The Brain / LLM)

1. Go to [GroqCloud Console](https://console.groq.com/) and log in or sign up.
2. On the left sidebar, click on **API Keys**.
3. Click the **Create API Key** button.
4. Give it a name like "Phone Agent" and click Submit.
5. Copy the key (starts with `gsk_...`) and paste it into the `GROQ_API_KEY` slot in your `.env` file.

### D. Sarvam AI API Key (Text-to-Speech)

1. Go to [Sarvam AI Dashboard](https://dashboard.sarvam.ai/) and sign up or log in.
2. On the left side navigation menu, click on **API Keys**.
3. Click **Generate New API Key**.
4. Copy the generated key and paste it into the `SARVAM_API_KEY` slot in your `.env` file.

## Step 4: Running the Agent

1. Open your terminal in the `ai-phone-agent` folder.
2. Make sure your virtual environment is activated: `.\venv\Scripts\activate`
3. Run the agent: `python agent.py start`
4. This will start your agent and tell it to listen for someone joining a LiveKit room.

## Next Steps for Outbound Calling

Because you are on a Vobiz trial, you cannot receive calls. You must use LiveKit's **CreateSIPParticipant** API endpoint to tell LiveKit to dial _out_ through Vobiz to your personal phone number.
We will write a small script to trigger this outbound call once the agent is running.
