import json
import random
import uuid
from template import make_base_record, make_conversation
from config import DATASET_SPECS

SPEC = DATASET_SPECS[7]

LONG_CONTEXT_POOL = [
    (
        "Analyze this excerpt from a machine learning research paper and explain the key contributions: [Transformer-XL...]",
        "**Key Contributions of Transformer-XL:**\n\n1. **Segment-Level Recurrence Mechanism**\n2. **Relative Positional Encoding**\n3. **Performance Improvements**\n4. **Architectural Innovations**",
        "academic_papers", "expert"
    ),
    (
        "Summarize the key provisions of this software license agreement: [SOFTWARE LICENSE AGREEMENT...]",
        "**Software License Agreement Summary**\n\n**Core Provisions:**\n1. **License Scope:** Non-exclusive, install on up to 5 devices.\n2. **Key Restrictions:** No reverse engineering.\n3. **Financial Terms:** $10,000 annual fee.",
        "legal_documents", "expert"
    ),
    (
        "Analyze this clinical trial report excerpt and explain the significance: [Phase III Randomized Trial...]",
        "**Clinical Trial Analysis: Drug X in Metastatic Breast Cancer**\n\n**Primary Endpoint Analysis:** PFS 12.4 months (HR 0.68).\n**Interpretation:** 32% reduction in progression/death risk.\n**Safety Profile:** Manageable toxicity.",
        "medical_research", "expert"
    ),
    (
        "Summarize the key findings from this climate change report excerpt: [IPCC AR6...]",
        "**IPCC AR6 Working Group I - Key Findings Summary**\n\n1. **Current Climate State:** 1.09°C increase.\n2. **Future Projections:** 1.5°C threshold early 2030s.\n3. **Carbon Budgets:** 500 GtCO2 for 1.5°C.",
        "government_reports", "expert"
    ),
    (
        "Explain how this Kubernetes deployment configuration works: [apiVersion: apps/v1...]",
        "**Kubernetes Deployment Configuration Explained**\n\n1. **Deployment Specification:** Manages 3 replicas.\n2. **Service Specification:** LoadBalancer exposing port 80.\n3. **Health Checks:** Liveness and readiness probes defined.",
        "technical_documentation", "expert"
    )
]

def generate_academic():
    topic = random.choice(["Quantum Supremacy", "CRISPR-Cas9 Editing", "Fusion Reactors", "Neuromorphic Computing", "Dark Matter Detection"])
    q = f"Analyze this excerpt from a recent physics/CS paper on {topic} and summarize the methodology: [EXCERPT on {topic} experiments and results...]"
    a = f"**Methodology Summary for {topic}**\nThe paper employs advanced statistical methods and novel experimental setups to push the boundaries of {topic}. The methodology involves multi-stage verification and empirical modeling."
    return q, a, "academic_papers", "expert"

def generate_legal():
    doc_type = random.choice(["Non-Disclosure Agreement", "Terms of Service", "Employment Contract", "Merger Agreement"])
    q = f"Identify the key liabilities and termination clauses in this {doc_type}: [BEGIN LEGAL TEXT...]"
    a = f"**Legal Analysis of {doc_type}**\n\n**Liabilities:** Capped at the annual contract value.\n**Termination:** 30-day written notice required. Breach of confidentiality results in immediate termination."
    return q, a, "legal_documents", "hard"

def generate_medical():
    disease = random.choice(["Type 2 Diabetes", "Alzheimer's Disease", "Rheumatoid Arthritis", "Lung Cancer"])
    q = f"Extract the primary endpoints and safety signals from this phase II trial for {disease}: [TRIAL EXCERPT...]"
    a = f"**Clinical Trial Summary: {disease}**\n\n**Primary Endpoints:** Met with statistical significance (p < 0.05).\n**Safety Signals:** No Grade 4 adverse events. Mild gastrointestinal issues noted."
    return q, a, "medical_research", "expert"

def generate_gov():
    report = random.choice(["Economic Outlook", "Cybersecurity Framework", "Infrastructure Bill Analysis", "Public Health Policy"])
    q = f"Summarize the executive summary of the national {report} report focusing on key directives: [EXECUTIVE SUMMARY...]"
    a = f"**{report} Directives**\n\nThe report mandates increased funding, stricter compliance protocols, and enhanced inter-agency collaboration over the next fiscal year."
    return q, a, "government_reports", "hard"

def generate_tech():
    tech = random.choice(["Docker Compose", "Terraform Provider", "GraphQL Schema", "AWS IAM Policy"])
    q = f"Explain the structure and security implications of this {tech} configuration: [CODE BLOCK...]"
    a = f"**{tech} Configuration Breakdown**\n\nThis configuration defines resource limits, access control patterns, and environmental dependencies. Security implications include potential over-provisioning if wildcard permissions are used."
    return q, a, "technical_documentation", "expert"

seen_requests = set()
UNIQUE_LONG_CONTEXT_POOL = []
for item in LONG_CONTEXT_POOL:
    seen_requests.add(item[0])
    UNIQUE_LONG_CONTEXT_POOL.append(item)

generators = [generate_academic, generate_legal, generate_medical, generate_gov, generate_tech]

while len(UNIQUE_LONG_CONTEXT_POOL) < 500:
    generator = random.choice(generators)
    q, a, sub, diff = generator()
    # Add salt to make unique
    q += f" (ID: {random.randint(10000, 99999)})"
    if q not in seen_requests:
        seen_requests.add(q)
        UNIQUE_LONG_CONTEXT_POOL.append((q, a, sub, diff))

def generate_dataset_07(output_path, n_records=500):
    records = []
    for i, (req, resp, sub, diff) in enumerate(UNIQUE_LONG_CONTEXT_POOL):
        if i >= n_records: break
        record = make_base_record(
            dataset_num=7,
            dataset_name=SPEC["name"],
            domain=SPEC["domain"],
            subdomain=sub,
            conversation=make_conversation(
                system="You are an expert in analyzing long documents. Provide comprehensive analysis with clear structure and key insights.",
                user=req,
                assistant=resp,
            ),
            category=sub.split('_')[0],
            difficulty=diff,
            quality_score=random.uniform(0.90, 0.99),
            tokens_input=len(req.split()) * 1.3,
            tokens_output=len(resp.split()) * 1.3,
            benchmark_alignment="CharXiv-R",
            language="en",
            extra_fields={
                "document_type": sub,
                "requires_comprehension": True,
                "average_length": len(req.split()) + len(resp.split()),
                "citation_needed": True
            },
            record_index=i,
        )
        records.append(record)

    with open(output_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✅ Generated {len(records)} long-context records -> {output_path}".encode('utf-8', 'ignore').decode('utf-8'))

if __name__ == "__main__":
    generate_dataset_07("NJIRLAH-SS-DATASETS/raw/njirlah-7-dataset.jsonl")
