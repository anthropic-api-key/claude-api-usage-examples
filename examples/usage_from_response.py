"""Send one message to the Claude API and print the usage object.

Env: ANTHROPIC_API_KEY (read by the SDK), CLAUDE_MODEL (a model id from the pricing page).
"""
import os
import sys

import anthropic

model = os.environ.get('CLAUDE_MODEL')
if not model:
    sys.exit('set CLAUDE_MODEL to a model id from https://claude.com/pricing#api')

client = anthropic.Anthropic()  # picks up ANTHROPIC_API_KEY from the environment

response = client.messages.create(
    model=model,
    max_tokens=512,
    messages=[{'role': 'user', 'content': 'In one sentence, what is a token?'}],
)

for block in response.content:
    if block.type == 'text':
        print(block.text)

u = response.usage
print('--- usage ---')
print('input_tokens:               ', u.input_tokens)
print('output_tokens:              ', u.output_tokens)
print('cache_creation_input_tokens:', getattr(u, 'cache_creation_input_tokens', None))
print('cache_read_input_tokens:    ', getattr(u, 'cache_read_input_tokens', None))
print('request id:', response._request_id)
