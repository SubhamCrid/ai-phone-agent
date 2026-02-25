# AI Phone Agent Cost Analysis

Based on your current infrastructure established in `agent.py`, here is a detailed breakdown of the running costs for **100 calls per day** at an average of **2 minutes per call**.

## Assumptions

- **Total Minutes/Day:** 200 minutes
- **Total Minutes/Month:** 6,000 minutes (assuming 30 days)
- **Speech Speed:** ~150 words per minute (wpm) each for Human and AI.
- **Conversion Rate:** 1 USD ≈ 84 INR (for Vobiz and Sarvam pricing conversions).

---

## 1. Provider Cost Breakdown

### **1. Vobiz (SIP Trunk)**

Vobiz handles your inbound/outbound telephony.

- **Per-minute Cost:** ₹0.45 INR (~$0.0054 USD)
- **Monthly Virtual Number (DID) Cost:** ₹500 INR (~$6.00 USD)
- **Calculation (Monthly):** (6,000 mins × ₹0.45) = ₹2,700 + ₹500 DID = ₹3,200 INR
- **Cost / Month:** **~$38.10 USD**

### **2. LiveKit Cloud (SIP Ingest + Agent Session)**

LiveKit handles WebRTC endpoints, Agent logic execution, and SIP bridging.

- **SIP Minutes (Inbound):** The Ship plan provides 5,000 SIP minutes for $50/mo. Overage is $0.004/min. Let's assume you're on the Ship plan ($50 base + 1,000 mins at $0.004). Total: $54.00.
- **Agent Session Minutes:** $0.01 per minute when an agent is active in a room. 6,000 mins × $0.01 = $60.00.
- **Calculation (Monthly):** $54.00 (SIP) + $60.00 (Agent Session)
- **Cost / Month:** **~$114.00 USD**
  _(Note: If self-hosting LiveKit, your cost would be a flat VPS cost of ~$20-$40/mo)._

### **3. Deepgram (Speech-to-Text)**

Deepgram transcribes the user's voice using the Nova-2 model natively via LiveKit's deepgram plugin.

- **Per-minute Cost:** ~$0.0058 USD (Pay-as-you-go Plan for Nova-2).
- **Calculation (Monthly):** 6,000 mins × $0.0058
- **Cost / Month:** **~$34.80 USD**

### **4. Groq (LLM - Llama 3.1 8b Instant)**

Groq processes transcribed text and generates completions.

- **Pricing:** $0.05 per 1M Input Tokens | $0.08 per 1M Output Tokens.
- **Usage Estimate:** At a combined 300 words/min (roughly 400 tokens/min combined), 6,000 mins generates ~2.4 million tokens/month. Even with a highly inflated context window (e.g., 5M tokens input, 1M tokens output).
- **Calculation (Monthly):** (5M input × $0.05) + (1M output × $0.08)
- **Cost / Month:** **~$0.33 USD** _(Practically free)_

### **5. Sarvam AI (Text-to-Speech)**

Sarvam synthesizes the Indian-accented English audio (`en-IN`).

- **Pricing:** ₹15 INR per 10,000 characters (Bulbul model).
- **Usage Estimate:** An AI speaking 150 words/min produces roughly ~750 characters/min.
- **Characters per month:** 6,000 mins × 750 chars = 4,500,000 characters.
- **Calculation (Monthly):** (4,500,000 / 10,000) × ₹15 = ₹6,750 INR
- **Cost / Month:** **~$80.35 USD**

---

## 2. Total Cost Summary

| Service                    | Estimated Monthly Cost | Average Cost Per Minute       |
| :------------------------- | :--------------------- | :---------------------------- |
| **Vobiz (SIP + DID)**      | $38.10                 | $0.0063                       |
| **LiveKit Cloud (Hosted)** | $114.00                | $0.0190                       |
| **Deepgram (STT)**         | $34.80                 | $0.0058                       |
| **Groq (Llama 3.1 8b)**    | $0.33                  | < $0.0001                     |
| **Sarvam AI (TTS)**        | $80.35                 | $0.0134                       |
| **TOTAL**                  | **~$267.58 USD**       | **~$0.0446 USD (~4.5 cents)** |

### Final Breakdown:

- **Cost Per Minute:** **~$0.045 USD** (~4.5 cents per minute)
- **Cost Per Call (2 mins):** **~$0.09 USD** (~9 cents per call)
- **Cost Per Day (100 calls):** **~$8.90 USD**
- **Cost Per Month (6,000 mins):** **~$267.58 USD**

## Optimization Tips

1. **Self-host LiveKit:** If you move off LiveKit Cloud to self-hosted OSS LiveKit, you drop the $114/month bill to a flat $20-$40/month VPS fee.
2. **Deepgram Growth Plan:** Upgrading Deepgram packages down the line can lower STT costs slightly.
3. **Sarvam Character Efficiency:** Keep the agent's prompts naturally concise. Less output chatter = less text for Sarvam to synthesis = cheaper TTS costs.
