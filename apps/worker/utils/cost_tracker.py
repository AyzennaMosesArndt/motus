import json
import os
from datetime import datetime, timezone
from pathlib import Path

from utils.logger import get_logger

logger = get_logger(__name__)

LOGS_DIR = Path(__file__).parent.parent / 'logs'
COST_LOG = LOGS_DIR / 'pipeline_costs.jsonl'

PRICING = {
    'claude-haiku-4-5-20251001': {'input': 0.80, 'output': 4.00},
    'claude-sonnet-4-6': {'input': 3.00, 'output': 15.00},
}


def _calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    prices = PRICING.get(model, {'input': 1.0, 'output': 5.0})
    return (input_tokens * prices['input'] + output_tokens * prices['output']) / 1_000_000


def log_call(
    stage: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    paper_id: str,
) -> None:
    LOGS_DIR.mkdir(exist_ok=True)
    cost = _calculate_cost(model, input_tokens, output_tokens)
    entry = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'stage': stage,
        'model': model,
        'input_tokens': input_tokens,
        'output_tokens': output_tokens,
        'estimated_cost_usd': round(cost, 8),
        'paper_id': paper_id,
    }
    with open(COST_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')
    logger.info(f'Cost logged: stage={stage} cost=${cost:.6f}')


def get_session_total() -> dict:
    if not COST_LOG.exists():
        return {'calls': 0, 'input_tokens': 0, 'output_tokens': 0, 'total_cost_usd': 0.0}

    process_start = datetime.fromtimestamp(
        os.path.getmtime(COST_LOG), tz=timezone.utc
    )
    calls, inp, out, cost = 0, 0, 0, 0.0
    with open(COST_LOG, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            ts = datetime.fromisoformat(entry['timestamp'])
            if ts >= process_start:
                calls += 1
                inp += entry['input_tokens']
                out += entry['output_tokens']
                cost += entry['estimated_cost_usd']
    return {'calls': calls, 'input_tokens': inp, 'output_tokens': out, 'total_cost_usd': round(cost, 6)}


def get_monthly_total() -> dict:
    if not COST_LOG.exists():
        return {'calls': 0, 'input_tokens': 0, 'output_tokens': 0, 'total_cost_usd': 0.0}

    cutoff = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    calls, inp, out, cost = 0, 0, 0, 0.0
    with open(COST_LOG, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            ts = datetime.fromisoformat(entry['timestamp'])
            if ts >= cutoff:
                calls += 1
                inp += entry['input_tokens']
                out += entry['output_tokens']
                cost += entry['estimated_cost_usd']
    return {'calls': calls, 'input_tokens': inp, 'output_tokens': out, 'total_cost_usd': round(cost, 6)}
