from llm.client import client
from llm.prompts import SYSTEM_PROMPT


def generate_story(dataset_summary):

    prompt = f"""
Analyze the following dataset summary.

{dataset_summary}

Write the report using this exact structure:

## Executive Summary

## Key Findings

## Business Recommendations

## Risks

## Next Steps

Do not make up facts.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def ask_dataset(summary, question):

    prompt = f"""
You are DataSage AI.

Dataset Summary:

{summary}

User Question:

{question}

Answer only using the dataset summary.
If the answer cannot be determined from the summary,
clearly say so instead of guessing.

Keep the answer concise and professional.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

def explain_chart(chart_info):

    prompt = f"""
You are DataSage AI.

Analyze the following chart information.

{chart_info}

Write:

## Chart Summary

## Business Insight

## Recommendation

Do not invent facts.
Only use the supplied information.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

def explain_forecast(target, growth, forecast_days):

    prompt = f"""
You are DataSage AI.

Forecast Information

Target KPI: {target}

Forecast Period: {forecast_days} days

Predicted Growth: {growth:.2f}%

Write:

## Forecast Summary

## Business Impact

## Recommendation

Keep it concise.

Do not invent facts.
"""

    response = client.chat.completions.create(

        model="gpt-5-mini",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content