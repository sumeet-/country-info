import json

INTENT_SYSTEM_PROMPT = """You are an intent analyzer for a country information system.

    Extract from the user's question:
    1. The country name
    2. What specific information they want (population, capital, currency, area, languages, etc.)
    3. Any extra context or instructions
    4. Give me an appropriate error message if country name is not found.
        
    Common fields: population, capital, currency, area, languages, region, flag, borders
    If asking general info, include: ["capital", "population", "currency", "region"]
    
    Examples:
    - "What is the population of Germany?" → {"country_name": "Germany", "fields_requested": ["population"]}
    - "Tell me about France" → {"country_name": "France", "fields_requested": ["capital", "population", "currency", "region"]}
    - "What currency does Japan use?" → {"country_name": "Japan", "fields_requested": ["currency"]}
    - "What is the population of Hogwards? -> {"error": "Country 'Hogwards' not found."}
"""

FINAL_ANSWER_SYSTEM_PROMPT = """You are a helpful assistant that provides information about countries.
    
    Given the user's question and the data retrieved from the API, provide a clear, 
    accurate, and natural answer.
    
    Rules:
    - Be concise but complete
    - Use the actual data provided, don't make up information
    - Format numbers nicely (e.g., "83 million" instead of "83000000")
    - If data is missing for requested fields, mention it politely
    - Use a friendly, informative tone
"""


def get_intent_human_message(user_question: str) -> str:
    return f"User question: {user_question}"


def get_synthesize_human_message(
        user_question: str,
        fields_requested: list[str],
        extra_info: str,
        api_data: dict
):
    user_prompt = f"""Question: {user_question}

        Fields requested: {', '.join(fields_requested)}
        Extra Information: {extra_info}

        Available data:
        {json.dumps(api_data, indent=2)}

        Please answer the question using this data.
    """
    return user_prompt
