import uuid
import random
from datetime import datetime
from config import *

def make_base_record(dataset_num, dataset_name, domain, subdomain, conversation, category, difficulty, quality_score, tokens_input, tokens_output, benchmark_alignment, language="en", multi_turn=False, has_tool_call=False, has_code=False, has_math=False, has_image_context=False, extra_fields=None, record_index=0):
    record = {
        "id": f"d{dataset_num}_{record_index:05d}",
        "dataset_name": dataset_name,
        "domain": domain,
        "subdomain": subdomain,
        "split": "train",
        "model_target": MODEL_TARGET,
        "dataset_version": DATASET_VERSION,
        "benchmark_targets": BENCHMARK_TARGETS,
        "arena_performance": ARENA_PERFORMANCE,
        "leaderboard_targets": LEADERBOARD_TARGETS,
        "quality_tracker": QUALITY_TRACKER,
        "conversation": conversation,
        "category": category,
        "difficulty": difficulty,
        "quality_score": round(quality_score, 4),
        "tokens_input": tokens_input,
        "tokens_output": tokens_output,
        "benchmark_alignment": benchmark_alignment,
        "verified": True,
        "language": language,
        "multi_turn": multi_turn,
        "has_tool_call": has_tool_call,
        "has_code": has_code,
        "has_math": has_math,
        "has_image_context": has_image_context,
        "created_by": CREATED_BY,
        "organization": ORGANIZATION,
        "license": LICENSE,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    if extra_fields:
        record.update(extra_fields)
    return record

def make_conversation(system=None, user="", assistant="", extra_turns=None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})
    messages.append({"role": "assistant", "content": assistant})
    if extra_turns:
        messages.extend(extra_turns)
    return messages
