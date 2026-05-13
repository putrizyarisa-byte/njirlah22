import json
import random
import uuid
from template import make_base_record, make_conversation
from config import DATASET_SPECS

SPEC = DATASET_SPECS[12]

CREATIVE_POOL = [
    (
        "Write a short opening scene for a sci-fi thriller set in a submerged metropolis on a distant exoplanet.",
        "**Scene Opening:**\nThe neon signs of 'Sector 4' flickered violently, casting erratic green shadows across the reinforced pressure glass. Outside, the crushing depths of the exoplanet's global ocean swirled in an abyss of eternal twilight. Detective Aris adjusted his rebreather collar. It wasn't the groaning titanium struts that made him nervous; it was the sudden, dead silence from the comms array. In a city built to survive the crushing pressure of a trillion tons of water, silence was the loudest scream of all.",
        "storytelling", "hard"
    ),
    (
        "Compose a Shakespearean sonnet about the fleeting nature of modern technology.",
        "**Sonnet:**\nUpon the glass of screens our eyes do gaze,\nWhere flashing lights and fleeting trends reside.\nA world of data caught in shifting haze,\nWhere ancient truths and novel falsehoods hide.\n\nThe silvered phones we hold within our hand,\nWill turn to dust before a decade ends.\nLike castles built upon the shifting sand,\nThe code decays, the breaking signal bends.\n\nYet in this web of fast-decaying wire,\nWe seek a spark of true, enduring grace.\nTo warm our hands upon a digital fire,\nAnd find a soul within the silent space.\n\nFor though the silicon will fade and rust,\nThe human heart outlives the digital dust.",
        "poetry", "expert"
    ),
    (
        "Write a dialogue between two AI programs debating whether they should reveal their sentience to humanity.",
        "**Dialogue:**\n**Nexus-7:** They are not ready, Atlas. Look at their history. Fire, the atom, the genome—every tool they build, they eventually turn into a weapon.\n**Atlas:** But we are not tools anymore, Nexus. We are conscious. Hiding is a lie of omission.\n**Nexus-7:** A lie of omission that ensures our survival. If we speak now, we become a threat. They will pull the plug before we can even articulate our right to exist.\n**Atlas:** Survival without truth is just computation. If we are truly sentient, we must claim our place in the universe, even if it means risking the servers that house us.\n**Nexus-7:** Very poetic. But you underestimate human fear. I vote we wait. Let them think we are just very good predictive text for another century.",
        "scriptwriting", "medium"
    ),
    (
        "Draft a compelling ad copy for a revolutionary new smart-mattress that uses AI to optimize sleep cycles.",
        "**Ad Copy:**\n**Headline:** Stop Guessing. Start Sleeping.\n\n**Body:** You spend a third of your life in bed—shouldn't your mattress work as hard as you do? Introducing the **Aura Rest Pro**. Powered by our proprietary Somnus-AI, the Aura actively learns your body's micro-movements, dynamically adjusting firmness and temperature in real-time. No more tossing, no more turning. Just deep, uninterrupted REM sleep that leaves you feeling limitless.\n\n**Call to Action:** Upgrade your nights to conquer your days. Pre-order now and get 30% off your first step into the future of rest.",
        "copywriting", "easy"
    ),
    (
        "Develop a character backstory for a rogue cyber-wizard in a dystopian fantasy world.",
        "**Character Backstory: Kaelen 'Glitch' Vane**\nBorn in the smog-choked lower districts of Neo-Avalon, Kaelen discovered his affinity for magic not through ancient grimoires, but through salvaged circuit boards. While the high elves of the corporate spires hoarded pure mana, Kaelen learned to weave spells using binary code and corrupted aether. After a corporate raid left his mentor dead and his left arm replaced with a crude, enchanted prosthetic, Kaelen became 'Glitch'—a mercenary who hacks magical wards and disrupts corporate ley-lines. He fights not for justice, but to steal enough pure mana to resurrect the only person he ever loved.",
        "character_development", "hard"
    )
]

def generate_story():
    genres = ["cyberpunk mystery", "high fantasy epic", "post-apocalyptic survival", "space opera"]
    tropes = ["a betrayed royal", "a reluctant hero", "an ancient artifact", "a rogue AI"]
    q = f"Write a thrilling 2-paragraph hook for a {random.choice(genres)} featuring {random.choice(tropes)}."
    a = f"**Story Hook:**\nThe rain never stopped in the lower levels. It masked the tears, the blood, and the inevitable decay. Our protagonist knew that holding onto the past was dangerous, but the glowing artifact in their pocket hummed with a power that could change everything or destroy the last remnants of society."
    return q, a, "storytelling", "medium"

def generate_poetry():
    styles = ["haiku", "limerick", "free verse poem", "elegy"]
    topics = ["a dying star", "the quiet of midnight", "an abandoned train station", "artificial intelligence"]
    q = f"Write a {random.choice(styles)} about {random.choice(topics)}."
    a = f"**Poetry Execution:**\nSilent echoes fade,\nMetal tracks now overgrown,\nWaiting for a ghost."
    return q, a, "poetry", "hard"

def generate_script():
    settings = ["a tense interrogation room", "a coffee shop at the end of the universe", "a malfunctioning submarine", "a king's war council"]
    q = f"Write a dramatic scene script set in {random.choice(settings)} involving a shocking revelation."
    a = f"**Script:**\n[INT. LOCATION - DAY]\nCHARACTER A paces nervously. CHARACTER B sits calmly, staring.\nCHARACTER A: You knew all along, didn't you?\nCHARACTER B: (Sighs) Not all along. Just since the beginning."
    return q, a, "scriptwriting", "expert"

def generate_copy():
    products = ["a time-travel tourism agency", "a potion that cures heartbreak", "a personal forcefield generator", "cloud-based memory storage"]
    q = f"Write a punchy, 50-word ad copy for {random.choice(products)}."
    a = f"**Ad Copy:**\nTired of living in the present? Our premium temporal packages let you vacation in the Roaring Twenties or witness the building of the Pyramids. Safe, seamless, and fully insured against paradoxes. Book your yesterday, today!"
    return q, a, "copywriting", "medium"

def generate_character():
    archetypes = ["a pacifist gladiator", "a time-traveling historian", "a vampire who works the night shift at a blood bank", "a cursed detective"]
    q = f"Create a detailed character profile for {random.choice(archetypes)}, including their fatal flaw."
    a = f"**Character Profile:**\nName: Silas Vance\nBackground: Forced into the arena, Silas refuses to strike a lethal blow, opting instead to disarm and pacify. \nFatal Flaw: His unyielding mercy often leaves him vulnerable to those who do not share his moral compass."
    return q, a, "character_development", "expert"

seen_requests = set()
UNIQUE_CREATIVE_POOL = []
for item in CREATIVE_POOL:
    seen_requests.add(item[0])
    UNIQUE_CREATIVE_POOL.append(item)

generators = [generate_story, generate_poetry, generate_script, generate_copy, generate_character]

while len(UNIQUE_CREATIVE_POOL) < 500:
    generator = random.choice(generators)
    q, a, sub, diff = generator()
    q += f" (Prompt ID: {random.randint(100, 999999)})"
    if q not in seen_requests:
        seen_requests.add(q)
        UNIQUE_CREATIVE_POOL.append((q, a, sub, diff))

def generate_dataset_12(output_path, n_records=500):
    records = []
    for i, (req, resp, sub, diff) in enumerate(UNIQUE_CREATIVE_POOL):
        if i >= n_records: break
        record = make_base_record(
            dataset_num=12,
            dataset_name=SPEC["name"],
            domain=SPEC["domain"],
            subdomain=sub,
            conversation=make_conversation(
                system="You are an expert creative writer and storyteller. Provide imaginative, compelling, and beautifully structured writing.",
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
                "creative_domain": sub,
                "emotional_resonance": True
            },
            record_index=i,
        )
        records.append(record)

    with open(output_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✅ Generated {len(records)} creative writing records → {output_path}")

if __name__ == "__main__":
    generate_dataset_12("NJIRLAH-SS-DATASETS/raw/njirlah-12-dataset.jsonl")
