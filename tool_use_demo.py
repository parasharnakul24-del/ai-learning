import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

MODEL = "claude-sonnet-4-6"

# ── TOOL DEFINITIONS ────────────────────────────────────────────
# The description is NOT just documentation.
# Claude reads it to decide WHEN and WHETHER to call the tool.

tools = [
    {
        "name": "get_weather",
        "description": (
            "Get the current weather conditions for a specific city. "
            "Use this when the user asks about weather, temperature, "
            "climate conditions, or whether to carry an umbrella."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city, e.g. Mumbai, Delhi, London"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit. Default to celsius."
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_population",
        "description": (
            "Get the current population of a city or country. "
            "Use this when the user asks about population size, "
            "how many people live somewhere, or city/country demographics."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City or country name"
                }
            },
            "required": ["location"]
        }
    }
]


# ── MOCK EXECUTION FUNCTIONS ─────────────────────────────────────
# In production these would call real APIs.
# Here we return hardcoded data to focus on the tool use CYCLE.

def get_weather(city, unit="celsius"):
    data = {
        "mumbai":  {"temp": 32, "condition": "Humid and partly cloudy"},
        "delhi":   {"temp": 38, "condition": "Hot and hazy"},
        "london":  {"temp": 15, "condition": "Overcast with light drizzle"},
        "gurgaon": {"temp": 37, "condition": "Hot and sunny"},
    }
    result = data.get(city.lower(), {"temp": 25, "condition": "Clear skies"})
    return f"{result['temp']}°{'C' if unit == 'celsius' else 'F'}, {result['condition']} in {city}"


def get_population(location):
    data = {
        "mumbai":  "20.7 million",
        "delhi":   "32.9 million",
        "london":  "9.0 million",
        "india":   "1.44 billion",
        "gurgaon": "1.1 million",
    }
    return data.get(location.lower(), "Population data not available")


# ── TOOL DISPATCHER ──────────────────────────────────────────────
def execute_tool(tool_name, tool_input):
    if tool_name == "get_weather":
        return get_weather(
            tool_input["city"],
            tool_input.get("unit", "celsius")
        )
    elif tool_name == "get_population":
        return get_population(tool_input["location"])
    else:
        return f"Unknown tool: {tool_name}"


# ── FULL TOOL USE CYCLE ──────────────────────────────────────────
def run_with_tools(user_message):
    print(f"\n{'=' * 60}")
    print(f"USER: {user_message}")
    print("=" * 60)

    messages = [{"role": "user", "content": user_message}]

    # ── TURN 1: Send user message + tools to Claude ──────────────
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    print(f"\nSTOP REASON: {response.stop_reason}")

    # ── Check if Claude wants to use a tool ─────────────────────
    if response.stop_reason == "tool_use":

        # Extract tool use block(s)
        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                print(f"\nCLAUDE CALLS TOOL: {block.name}")
                print(f"WITH INPUTS: {block.input}")

                # Execute the tool
                result = execute_tool(block.name, block.input)
                print(f"TOOL RESULT: {result}")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        # ── TURN 2: Send tool results back to Claude ─────────────
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

        final_response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        print(f"\nCLAUDE FINAL ANSWER:\n{final_response.content[0].text}")

    else:
        # Claude answered directly — no tool needed
        print(f"\nCLAUDE ANSWERED DIRECTLY (no tool used):")
        print(response.content[0].text)


# ── TEST CASES ───────────────────────────────────────────────────

# Should trigger get_weather
run_with_tools("What is the weather like in Mumbai right now?")

# Should trigger get_population
run_with_tools("How many people live in Delhi?")

# Should trigger BOTH tools
run_with_tools("Tell me the weather and population of London.")

# Should NOT trigger any tool — Claude answers from knowledge
run_with_tools("What is the capital of France?")

print("\n" + "=" * 60)
print("KEY LEARNING:")
print("1. stop_reason='tool_use' means Claude wants to call a tool")
print("2. stop_reason='end_turn' means Claude answered directly")
print("3. Tool description = the prompt Claude uses to decide WHEN to call it")
print("4. You always execute the tool — Claude never runs code itself")
print("5. This 4-step cycle is the foundation of every AI agent")
print("=" * 60)