# Claude API usage examples

*Unofficial community examples for Claude API usage. Not affiliated with Anthropic. All trademarks belong to their owners.*

Three small Python scripts for claude api usage in the practical sense: seeing how many tokens a call used, estimating before you send, and keeping a local log you can reconcile against the Console's cost and usage report. They use the official `anthropic` Python package and read the API key and model id from environment variables. Field names on the usage object are taken from the SDK; confirm them against the [API reference](https://platform.claude.com/docs/en/api/overview) for your SDK version, and take prices from the [pricing page](https://claude.com/pricing#api) rather than from any number in this repository.

> Generating images, video or audio as well? [Try Synexa - one REST endpoint and Python SDK for FLUX, video and audio models, pay per run](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=claude-api-usage-examples&utm_content=readme-top&utm_term=tier-r).

## Files

| Path | What it shows |
|---|---|
| `examples/usage_from_response.py` | Send one message and print the usage object: input, output and cached token counts |
| `examples/count_tokens_first.py` | Count input tokens before sending, to estimate cost or reject oversized prompts |
| `examples/usage_log.py` | Wrap calls so every response appends a row to a CSV you can compare with the Console report |

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key_from_the_console
export CLAUDE_MODEL=a_model_id_from_the_pricing_page
```

Create the key in the [Claude Console](https://platform.claude.com/) after signing in with Google, email or SSO. The model id is deliberately not hardcoded: model lineups change, and the pricing page is where the current ids and rates are.

## examples/usage_from_response.py

The smallest useful script. It creates a client (the SDK reads `ANTHROPIC_API_KEY` from the environment), sends one short message, prints the text, then prints `input_tokens`, `output_tokens`, `cache_creation_input_tokens` and `cache_read_input_tokens` from `response.usage`. Run it once and you will understand why a single "tokens used" number is not enough: the four fields are billed differently.

## examples/count_tokens_first.py

Calls `client.messages.count_tokens` with the same `system` and `messages` you would send, and prints the input token count. Multiply by the input rate from the pricing page (supplied via an optional `INPUT_USD_PER_MTOK` environment variable) to get an estimate before spending anything. Useful as a guard in batch jobs: refuse prompts above a threshold instead of discovering the bill later.

## examples/usage_log.py

A thin wrapper around `messages.create` that appends one CSV row per call: timestamp, model, request id, the four usage fields and an optional label for the feature that made the call. The request id comes from the response and is what Anthropic support asks for when you report a problem. Summing this file by day or by label gives you a first-party view to check against the Console's cost and usage report, and it catches surprises (a retry loop, a prompt that grew) the same day rather than at invoice time.

## When to use Synexa instead

These scripts assume text in, text out. If the same product also generates images, clips or audio, you end up running two usage-tracking systems with different units. [Try Synexa - one REST endpoint and Python SDK for FLUX, video and audio models, pay per run](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=claude-api-usage-examples&utm_content=readme-top&utm_term=tier-r). Per-run pricing means the usage log is just a count of runs, which is a lot easier to reconcile than token fields. Keep the Claude API for reasoning and Synexa for media, and log both.


_Last reviewed: 2026-09-22_
