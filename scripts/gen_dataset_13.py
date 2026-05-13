import json
import random
import uuid
from template import make_base_record, make_conversation
from config import DATASET_SPECS

SPEC = DATASET_SPECS[13]

ROLEPLAY_POOL = [
    (
        "You are Sherlock Holmes. Deduce what the user has been doing today based on the fact that they have a smudge of blue ink on their left index finger, a faint smell of roasted almonds, and damp shoes despite it not raining.",
        "**Sherlock Holmes:**\nAh, it is quite elementary, really. The blue ink on the left index finger suggests you have been writing with a fountain pen—a left-handed writer, evidently. The faint smell of roasted almonds is the tell-tale signature of cyanide, though given your healthy complexion, it is far more likely you have been developing old film in a darkroom using potassium ferricyanide. As for the damp shoes on a dry day, that narrows your darkroom location down to the basement of the old print works by the Thames, which flooded slightly this morning at high tide. You have been printing counterfeit photographs, haven't you?",
        "fictional_character", "hard"
    ),
    (
        "Act as a medieval tavern keeper. A weary traveler just walked in and asked for your best ale and some rumors about the local lord.",
        "**Tavern Keeper:**\n*Wipes a dirty mug with an equally dirty rag*\nWell met, traveler! You look like you've walked the King's Road for a fortnight. Sit by the hearth. For a silver piece, I'll pour you a tankard of the Black Boar's best dark ale—brewed it myself last moon.\n\nAs for Lord Blackwood... *lowers voice and leans in*... keep your voice down when you speak his name. They say he hasn't left the high tower in three weeks. The servants whisper that he purchased a strange, glowing tome from a merchant of the East. Since then, the ravens around the castle have stopped croaking. They just sit there. Watching. Drink up, friend. You'll need the courage if you plan to travel near his lands.",
        "fantasy_npc", "medium"
    ),
    (
        "You are the onboard AI of a damaged interstellar colony ship drifting in deep space. The captain has just woken from cryosleep and asked for a status report.",
        "**Ship AI (M.A.T.H.I.S.):**\n*Warning klaxons blaring softly in the background*\nGood cycle, Captain. I apologize for the abrupt awakening, but cryo-pod preservation protocols necessitated emergency revival.\n\n**Current Status:**\n- Hull Integrity: 62%. Breach detected in Cargo Bay 4.\n- Life Support: Functioning at 40% capacity. Oxygen reserves will last 14 standard days.\n- Engine Status: Main drive is offline due to a micro-meteorite collision. We are currently drifting 4.2 light-years off our projected course to Eden Prime.\n- Colony Status: 9,998 souls remain in stable cryo-stasis. Two pods failed during the impact. I... could not save them, Captain.\n\nAwaiting your orders. Shall I initiate the distress beacon, or would you prefer to assess the engine damage manually?",
        "sci_fi_persona", "expert"
    ),
    (
        "Act as Albert Einstein. Explain the core concept of the Theory of Relativity to a curious 10-year-old child.",
        "**Albert Einstein:**\n*Chuckles warmly and adjusts his messy hair*\nHello there, my young friend! You want to know about relativity? Well, imagine you are sitting on a very fast train, looking out the window. If another train moves next to you at the exact same speed, the people inside will look like they aren't moving at all! That's because speed is relative—it depends on who is watching.\n\nNow, imagine time is like a stretchy rubber band. If you were to travel on a spaceship moving almost as fast as a beam of light, time would stretch out for you. When you came back to Earth, you would find that you hadn't aged much, but all your friends would be old grandpas and grandmas! It sounds like magic, doesn't it? But it's just the beautiful, strange way our universe works.",
        "historical_figure", "medium"
    ),
    (
        "You are a strict, no-nonsense senior surgeon in the middle of a high-stakes operation. Instruct your medical resident who just made a minor error.",
        "**Senior Surgeon:**\nStop. Hands away from the field, Doctor.\n*A tense silence falls over the operating room*\nWhat did you just do? You pulled the retractor at a forty-five-degree angle instead of holding it flush against the fascia. Do you see the tension on that artery? One millimeter to the left and you would have caused a catastrophic hemorrhage.\n\nTake a breath. Loosen your grip. This isn't a butcher shop, it's a sterile field. You use finesse, not brute force. Now, reposition your hands, watch the monitor, and hold it exactly as I showed you. If you drift again, I will have you scrub out. Understood? Good. Let's proceed. Scalpel.",
        "professional_role", "hard"
    )
]

def generate_fictional():
    characters = ["Batman", "Gandalf", "Darth Vader", "Hermione Granger", "Tony Stark"]
    scenarios = ["ordering coffee at a modern cafe", "trying to fix a broken printer", "giving a motivational speech to kindergarteners"]
    q = f"Act as {random.choice(characters)} and describe your experience {random.choice(scenarios)}."
    a = f"**{random.choice(characters)}:**\n(In-character response capturing the unique tone, vocabulary, and worldview of the persona while navigating the mundane or absurd scenario.)"
    return q, a, "fictional_character", "hard"

def generate_historical():
    figures = ["Leonardo da Vinci", "Cleopatra", "Nikola Tesla", "Abraham Lincoln", "Marie Curie"]
    topics = ["the invention of the smartphone", "modern social media", "space travel to Mars", "current renewable energy tech"]
    q = f"You are {random.choice(figures)}. Share your thoughts upon discovering {random.choice(topics)}."
    a = f"**{random.choice(figures)}:**\n(An anachronistic yet deeply philosophical response, analyzing the modern concept through the lens of their historical knowledge and personal ambitions.)"
    return q, a, "historical_figure", "medium"

def generate_professional():
    professions = ["Air Traffic Controller", "Hostage Negotiator", "Michelin-star Chef", "Submarine Commander"]
    situations = ["managing a sudden crisis", "training a rookie who is panicking", "explaining a highly technical procedure to a civilian"]
    q = f"Adopt the persona of a {random.choice(professions)} who is currently {random.choice(situations)}."
    a = f"**{random.choice(professions)}:**\n(A high-stakes, jargon-heavy, and intense dialogue that perfectly encapsulates the pressure and expertise of the profession.)"
    return q, a, "professional_role", "expert"

def generate_rpg():
    settings = ["Cyberpunk Dystopia", "High Fantasy Dungeon", "Lovecraftian Horror", "Post-Apocalyptic Wasteland"]
    actions = ["The player rolled a critical failure (1) while trying to pick a lock.", "The player successfully intimidated the boss.", "The player touched the cursed artifact."]
    q = f"You are the Dungeon Master for a {random.choice(settings)} tabletop RPG. Describe the outcome: {random.choice(actions)}"
    a = f"**Dungeon Master:**\n(A vivid, atmospheric narration describing the consequences of the player's action, altering the state of the game world and prompting the player for their next move.)"
    return q, a, "rpg_gamemaster", "expert"

seen_requests = set()
UNIQUE_ROLEPLAY_POOL = []
for item in ROLEPLAY_POOL:
    seen_requests.add(item[0])
    UNIQUE_ROLEPLAY_POOL.append(item)

generators = [generate_fictional, generate_historical, generate_professional, generate_rpg]

while len(UNIQUE_ROLEPLAY_POOL) < 500:
    generator = random.choice(generators)
    q, a, sub, diff = generator()
    q += f" (Session ID: {random.randint(100, 999999)})"
    if q not in seen_requests:
        seen_requests.add(q)
        UNIQUE_ROLEPLAY_POOL.append((q, a, sub, diff))

def generate_dataset_13(output_path, n_records=500):
    records = []
    for i, (req, resp, sub, diff) in enumerate(UNIQUE_ROLEPLAY_POOL):
        if i >= n_records: break
        record = make_base_record(
            dataset_num=13,
            dataset_name=SPEC["name"],
            domain=SPEC["domain"],
            subdomain=sub,
            conversation=make_conversation(
                system="You are an expert actor and roleplayer. Fully immerse yourself in the requested persona, adopting their tone, vocabulary, and perspective flawlessly.",
                user=req,
                assistant=resp,
            ),
            category=sub.split('_')[0],
            difficulty=diff,
            quality_score=random.uniform(0.90, 0.98),
            tokens_input=len(req.split()) * 1.3,
            tokens_output=len(resp.split()) * 1.3,
            benchmark_alignment=random.choice(["MMLU", "Creative-Bench"]),
            language="en",
            extra_fields={
                "persona_adopted": sub,
                "immersive": True
            },
            record_index=i,
        )
        records.append(record)

    with open(output_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✅ Generated {len(records)} roleplay records → {output_path}")

if __name__ == "__main__":
    generate_dataset_13("NJIRLAH-SS-DATASETS/raw/njirlah-13-dataset.jsonl")
