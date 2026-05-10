import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
from dotenv import load_dotenv
import logging
import time

load_dotenv()
client = anthropic.Anthropic()

# Set up logging so you can SEE tenacity retrying in the terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── PART 1: Simulate a 429 to PROVE tenacity works ──────────────

attempt_count = 0  # track how many times the function is called

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=2, max=16),
    before_sleep=before_sleep_log(logger, logging.INFO)  # logs each retry
)
def call_claude_with_retry(messages):
    global attempt_count
    attempt_count += 1

    print(f"\n>>> Attempt #{attempt_count}")

    # Simulate a 429 on the first 2 attempts, succeed on 3rd
    if attempt_count < 3:
        print(f"    Simulating 429 RateLimitError on attempt #{attempt_count}...")
        raise anthropic.RateLimitError(
            message="Rate limit exceeded (simulated)",
            response=None,
            body={}
        )

    print(f"    Attempt #{attempt_count} succeeded!")
    return client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=messages
    )


print("=" * 60)
print("PART 1: Simulated 429 — watch tenacity retry")
print("=" * 60)

start = time.time()
response = call_claude_with_retry([
    {"role": "user", "content": "In one sentence, what is prompt caching?"}
])
elapsed = time.time() - start

print(f"\nFinal answer: {response.content[0].text}")
print(f"Total time (including retries): {elapsed:.1f}s")
print(f"Total attempts made: {attempt_count}")


# ── PART 2: Real call with retry protection (production pattern) ─

print("\n" + "=" * 60)
print("PART 2: Real call with tenacity protection (production pattern)")
print("=" * 60)

attempt_count = 0  # reset counter

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=2, max=16),
    before_sleep=before_sleep_log(logger, logging.INFO)
)
def call_claude_production(messages):
    return client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=messages
    )

response2 = call_claude_production([
    {"role": "user", "content": "What is the token bucket algorithm in one sentence?"}
])

print(f"\nAnswer: {response2.content[0].text}")


# ── PART 3: Check rate limit headers ────────────────────────────

print("\n" + "=" * 60)
print("PART 3: Rate limit headers from API response")
print("=" * 60)

# Make a raw call to inspect headers
raw_response = client.messages.with_raw_response.create(
    model="claude-sonnet-4-6",
    max_tokens=50,
    messages=[{"role": "user", "content": "Say hello"}]
)

headers = raw_response.headers
print(f"Requests remaining:      {headers.get('anthropic-ratelimit-requests-remaining', 'N/A')}")
print(f"Requests limit:          {headers.get('anthropic-ratelimit-requests-limit', 'N/A')}")
print(f"Input tokens remaining:  {headers.get('anthropic-ratelimit-input-tokens-remaining', 'N/A')}")
print(f"Output tokens remaining: {headers.get('anthropic-ratelimit-output-tokens-remaining', 'N/A')}")
print(f"Tokens reset at:         {headers.get('anthropic-ratelimit-tokens-reset', 'N/A')}")


print("\n" + "=" * 60)
print("KEY LEARNINGS:")
print("1. Tenacity retries automatically on RateLimitError")
print("2. Exponential backoff = wait 2s, 4s, 8s before retrying")
print("3. before_sleep logs each retry — essential for debugging")
print("4. Response headers tell you how many requests/tokens remain")
print("5. Production pattern: ALWAYS wrap API calls with retry logic")
print("=" * 60)