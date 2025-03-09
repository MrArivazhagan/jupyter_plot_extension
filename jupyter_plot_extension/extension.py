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
            response.stream(
                MarkdownData("""\n```text\n@data /plot <url>"\n```\n""")
            )
            response.stream(
                MarkdownData(
                    "Here is a Python method I generated. "
                    "\n```python\ndef show_message():\n  print('Hello world!')"
                    "\n```\n"
                )
            )
            response.finish()
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
