import requests
import vertexai
from vertexai import agent_engines

vertexai.init(
    project="genibuilder",               # Your project ID.
    location="asia-east1",                # Your cloud region.
    staging_bucket="gs://vertex-wiwi"
)


def get_exchange_rate(
    currency_from: str = "USD",
    currency_to: str = "EUR",
    currency_date: str = "latest",
):
    """Retrieves the exchange rate between two currencies on a specified date."""
    response = requests.get(
        f"https://api.frankfurter.app/{currency_date}",
        params={"from": currency_from, "to": currency_to},
    )
    return response.json()


agent = agent_engines.LangchainAgent(
    model="gemini-2.0-flash",
    tools=[get_exchange_rate],
    model_kwargs={
        "temperature": 0.28,
        "max_output_tokens": 1000,
        "top_p": 0.95,
    },
)
