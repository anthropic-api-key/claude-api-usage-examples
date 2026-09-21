"""Wrap messages.create so every call appends a usage row to a CSV.

Sum the CSV by day or label and compare with the Console's cost and usage report.
Env: ANTHROPIC_API_KEY, CLAUDE_MODEL, optional USAGE_LOG (path, default usage_log.csv).
"""
import csv
import os
import sys
from datetime import datetime, timezone

import anthropic

LOG_PATH = os.environ.get('USAGE_LOG', 'usage_log.csv')
FIELDS = ['ts', 'label', 'model', 'request_id', 'input_tokens', 'output_tokens',
          'cache_creation_input_tokens', 'cache_read_input_tokens', 'stop_reason']

client = anthropic.Anthropic()


def logged_create(label: str, **kwargs):
    """Call messages.create and append one row describing what it used."""
    response = client.messages.create(**kwargs)
    u = response.usage
    row = {
        'ts': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'label': label,
        'model': response.model,
        'request_id': response._request_id,
        'input_tokens': u.input_tokens,
        'output_tokens': u.output_tokens,
        'cache_creation_input_tokens': getattr(u, 'cache_creation_input_tokens', None),
        'cache_read_input_tokens': getattr(u, 'cache_read_input_tokens', None),
        'stop_reason': response.stop_reason,
    }
    new_file = not os.path.exists(LOG_PATH)
    with open(LOG_PATH, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            w.writeheader()
        w.writerow(row)
    return response


if __name__ == '__main__':
    model = os.environ.get('CLAUDE_MODEL')
    if not model:
        sys.exit('set CLAUDE_MODEL to a model id from https://claude.com/pricing#api')
    prompt = ' '.join(sys.argv[1:]) or 'Say hello in five words.'
    resp = logged_create(
        'demo',
        model=model,
        max_tokens=256,
        messages=[{'role': 'user', 'content': prompt}],
    )
    print(next((b.text for b in resp.content if b.type == 'text'), ''))
    print(f'logged to {LOG_PATH}')
