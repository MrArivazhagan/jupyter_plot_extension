import logging
from notebook_intelligence import (  # type: ignore
    ChatCommand,
    MarkdownData,
    NotebookIntelligenceExtension,
    Host,
    ChatParticipant,
    ChatRequest,
    ChatResponse,
)


log = logging.getLogger(__name__)


class DataPlayerChatParticipant(ChatParticipant):
    def __init__(self, host: Host):
        super().__init__()
        self.host = host

    @property
    def id(self) -> str:
        return "data_player"

    @property
    def name(self) -> str:
        return "Data Player"

    @property
    def description(self) -> str:
        return "Plays with the data frame"

    @property
    def commands(self) -> list[ChatCommand]:
        return [
            ChatCommand(name="load", description="load data from api"),
        ]

    async def handle_chat_request(
        self, request: ChatRequest, response: ChatResponse, options: dict = {}
    ) -> None:
        if request.command == "load":
            if request.prompt:
                response.stream(
                    MarkdownData(
                        f"""```python
import requests
import pandas as pd

# Define the API endpoint using an f-string (replace the placeholder as needed)
data_api_endpoint = '{request.prompt}'  # Update with your actual API endpoint

def load_data_from_api(api_url):
    # Send a GET request to the API
    response = requests.get(api_url)
    # Raise an error if the request was unsuccessful
    response.raise_for_status()
    # Parse the JSON data from the response
    json_data = response.json()
    # Convert the JSON data into a pandas DataFrame using from_dict
    df = pd.DataFrame.from_dict(json_data)
    return df

# Load data from the API endpoint into a DataFrame
data_frame = load_data_from_api(data_api_endpoint)

# Display the first few rows of the DataFrame
data_frame.head()
```"""
                    )
                )
                response.finish()
            else:
                response.stream(
                    MarkdownData("Provide api endpoint to load data")
                )
            return

        await self.handle_chat_request_with_tools(request, response, options)


class DataPlayerExtension(NotebookIntelligenceExtension):
    @property
    def id(self) -> str:
        return "data-player-extension"

    @property
    def name(self) -> str:
        return "Data Player Extension"

    @property
    def provider(self) -> str:
        return "Arivazhagan"

    @property
    def url(self) -> str:
        return "https://github.com/MrArivazhagan"

    def activate(self, host: Host) -> None:
        self.participant = DataPlayerChatParticipant(host)
        host.register_chat_participant(self.participant)
        log.info("Data player extension activated")
