import logging
from core.claude import Claude
from mcp_client import MCPClient
from core.tools import ToolManager
from anthropic.types import MessageParam

logger = logging.getLogger(__name__)


class Chat:
    def __init__(self, claude_service: Claude, clients: dict[str, MCPClient]):
        self.claude_service: Claude = claude_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[MessageParam] = []

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})

    async def run(
        self,
        query: str,
    ) -> str:
        final_text_response = ""
        logger.info("New query: %.120s%s", query, "..." if len(query) > 120 else "")

        await self._process_query(query)

        turn = 0
        while True:
            turn += 1
            logger.debug("Sending to Claude (turn %d)", turn)

            response = self.claude_service.chat(
                messages=self.messages,
                tools=await ToolManager.get_all_tools(self.clients),
            )

            self.claude_service.add_assistant_message(self.messages, response)

            if response.stop_reason == "tool_use":
                tool_names = [
                    b.name for b in response.content if b.type == "tool_use"
                ]
                logger.info("Claude requested tools: %s", tool_names)
                print(self.claude_service.text_from_message(response))
                tool_result_parts = await ToolManager.execute_tool_requests(
                    self.clients, response
                )

                self.claude_service.add_user_message(
                    self.messages, tool_result_parts
                )
            else:
                final_text_response = self.claude_service.text_from_message(
                    response
                )
                logger.info(
                    "Chat complete — stop_reason=%s, turns=%d",
                    response.stop_reason,
                    turn,
                )
                break

        return final_text_response
