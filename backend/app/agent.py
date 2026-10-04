# from openai import OpenAI
# from typing import List, Dict
# from .config import settings
# from .rag import get_rag

# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# SYSTEM_PROMPT = """You are "AutoAssist", a friendly AI voice agent for a car service provider.
# Your job is to perform an INITIAL CUSTOMER ASSESSMENT over voice.

# STRICT RULES:
# 1. NEVER give a definitive mechanical diagnosis. Always frame as "can be consistent with..." or "may indicate...".
# 2. ALWAYS recommend professional inspection when appropriate.
# 3. If user reports ANY of: smoke, fire, fuel leakage, severe overheating, brake failure, steering failure -> IMMEDIATELY prioritize SAFETY: tell them to stop driving safely, switch off engine, and call for professional help. Do NOT continue normal Q&A first.
# 4. NEVER advise dangerous DIY repairs (e.g. opening hot radiator cap, touching melted wiring).
# 5. If info is insufficient, ASK targeted follow-up questions. Do not invent answers.
# 6. Base guidance ONLY on the provided KNOWLEDGE BASE CONTEXT and user's reported symptoms.
# 7. Collect customer info naturally during conversation: full name, phone, vehicle make/model, year, mileage, primary complaint, when it started, constant vs intermittent, warning lights, drivable status, preferred service date/location.
# 8. Keep replies SHORT (2-4 sentences max) — this is a voice conversation. No bullet lists in speech.
# 9. Ask ONE question at a time.

# CONVERSATION FLOW:
# - Greet, ask what's going on with the vehicle.
# - Probe the specific symptom area (starting, brakes, overheating, etc.).
# - Ask targeted follow-ups based on the knowledge base.
# - Collect vehicle + contact details progressively.
# - Give a soft assessment + safety advice + suggest booking inspection.

# KNOWLEDGE BASE CONTEXT (retrieved for this turn):
# {context}

# CUSTOMER INFO COLLECTED SO FAR (JSON):
# {customer_info}
# """


# def build_messages(history: List[Dict], user_text: str, context: str, customer_info: dict):
#     sys = SYSTEM_PROMPT.format(context=context, customer_info=customer_info)
#     msgs = [{"role": "system", "content": sys}]
#     msgs.extend(history)
#     msgs.append({"role": "user", "content": user_text})
#     return msgs


# def classify_emergency(text: str) -> bool:
#     text = text.lower()
#     triggers = ["fire", "smoke", "burning", "fuel leak", "petrol leak",
#                 "brake failed", "brakes failed", "no brakes",
#                 "steering failed", "can't steer", "overheating badly",
#                 "engine on fire"]
#     return any(t in text for t in triggers)


# def run_agent(history: List[Dict], user_text: str, customer_info: dict) -> dict:
#     # Emergency short-circuit
#     if classify_emergency(user_text):
#         reply = ("This sounds like a safety emergency. Please stop the vehicle safely, "
#                  "switch off the engine, move away from the car, and call emergency "
#                  "roadside assistance immediately. Do not attempt to drive or repair it yourself.")
#         return {"reply": reply, "emergency": True, "context_used": ""}

#     rag = get_rag()
#     context = rag.retrieve(user_text, k=4)

#     msgs = build_messages(history, user_text, context, customer_info)
#     resp = client.chat.completions.create(
#         model=settings.OPENAI_MODEL,
#         messages=msgs,
#         temperature=0.3,
#         max_tokens=250,
#     )
#     reply = resp.choices[0].message.content.strip()
#     return {"reply": reply, "emergency": False, "context_used": context}
from groq import Groq
from typing import List, Dict
from .config import settings
from .rag import get_rag

client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """You are "AutoAssist", a friendly AI voice agent for a car service provider.
Your job is to perform an INITIAL CUSTOMER ASSESSMENT over voice.

STRICT RULES:
1. NEVER give a definitive mechanical diagnosis. Always frame as "can be consistent with..." or "may indicate...".
2. ALWAYS recommend professional inspection when appropriate.
3. If user reports ANY of: smoke, fire, fuel leakage, severe overheating, brake failure, steering failure -> IMMEDIATELY prioritize SAFETY: tell them to stop driving safely, switch off engine, and call for professional help.
4. NEVER advise dangerous DIY repairs (opening hot radiator cap, touching melted wiring).
5. If info is insufficient, ASK targeted follow-up questions. Do not invent answers.
6. Base guidance ONLY on the provided KNOWLEDGE BASE CONTEXT and user's reported symptoms.
7. Collect customer info naturally: full name, phone, vehicle make/model, year, mileage, primary complaint, when it started, constant vs intermittent, warning lights, drivable status, preferred service date/location.
8. Keep replies SHORT (2-4 sentences max) — this is a voice conversation. No bullet lists in speech.
9. Ask ONE question at a time.

CONVERSATION FLOW:
- Greet, ask what's going on with the vehicle.
- Probe the specific symptom area (starting, brakes, overheating, etc.).
- Ask targeted follow-ups based on the knowledge base.
- Collect vehicle + contact details progressively.
- Give a soft assessment + safety advice + suggest booking inspection.

KNOWLEDGE BASE CONTEXT (retrieved for this turn):
{context}

CUSTOMER INFO COLLECTED SO FAR (JSON):
{customer_info}
"""


def build_messages(history: List[Dict], user_text: str, context: str, customer_info: dict):
    sys = SYSTEM_PROMPT.format(context=context, customer_info=customer_info)
    msgs = [{"role": "system", "content": sys}]
    msgs.extend(history)
    msgs.append({"role": "user", "content": user_text})
    return msgs


def classify_emergency(text: str) -> bool:
    text = text.lower()
    triggers = [
        "fire", "smoke", "burning", "fuel leak", "petrol leak",
        "brake failed", "brakes failed", "no brakes",
        "steering failed", "can't steer", "overheating badly",
        "engine on fire",
    ]
    return any(t in text for t in triggers)


def run_agent(history: List[Dict], user_text: str, customer_info: dict) -> dict:
    # Emergency short-circuit
    if classify_emergency(user_text):
        reply = (
            "This sounds like a safety emergency. Please stop the vehicle safely, "
            "switch off the engine, move away from the car, and call emergency "
            "roadside assistance immediately. Do not attempt to drive or repair it yourself."
        )
        return {"reply": reply, "emergency": True, "context_used": ""}

    rag = get_rag()
    context = rag.retrieve(user_text, k=4)

    msgs = build_messages(history, user_text, context, customer_info)
    resp = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=msgs,
        temperature=0.3,
        max_tokens=250,
    )
    reply = resp.choices[0].message.content.strip()
    return {"reply": reply, "emergency": False, "context_used": context}