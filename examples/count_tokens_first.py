"""Count input tokens before sending, and optionally estimate input cost.

Env: ANTHROPIC_API_KEY, CLAUDE_MODEL, optional INPUT_USD_PER_MTOK (from the pricing page).
"""
import os
import sys

import anthropic

model = os.environ.get('CLAUDE_MODEL')
if not model:
    sys.exit('set CLAUDE_MODEL to a model id from https://claude.com/pricing#api')

client = anthropic.Anthropic()

system = 'You summarize documents in three bullet points.'
document = sys.stdin.read() if not sys.stdin.isatty() else 'Paste a document on stdin to count it.'
messages = [{'role': 'user', 'content': document}]

count = client.messages.count_tokens(model=model, system=system, messages=messages)
print('input_tokens:', count.input_tokens)

# Guard: refuse prompts above a threshold instead of paying for them.
LIMIT = int(os.environ.get('INPUT_TOKEN_LIMIT', '50000'))
if count.input_tokens > LIMIT:
    sys.exit(f'prompt is over the {LIMIT} token limit; not sending')

rate = os.environ.get('INPUT_USD_PER_MTOK')
if rate:
    est = count.input_tokens / 1_000_000 * float(rate)
    print(f'estimated input cost: ${est:.6f} at ${rate} per million input tokens')
else:
    print('set INPUT_USD_PER_MTOK to the rate on the pricing page for a cost estimate')
