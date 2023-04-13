from dotenv import load_dotenv
load_dotenv()
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.agents import AgentType
# RemoteTools.py
from RemoteTools import REMOTE_TOOLS
# UtilTools.py
from UtilTools import UTIL_TOOLS
# prompt.py
from prompt import (
    ASSISTANT_PREFIX,
    ASSISTANT_FORMAT_INSTRUCTIONS,
    ASSISTANT_SUFFIX
)

class Chatbot(object):
    def __init__(self, verbose=True, tools: list = []):
        self.llm = ChatOpenAI(temperature=0, model_name='gpt-4')
        self.tools = UTIL_TOOLS + REMOTE_TOOLS + tools
        self.memory = ConversationBufferMemory(memory_key='chat_history', output_key='output', return_messages=True)
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            agent_kwargs={
                'prefix': ASSISTANT_PREFIX,
                'format_instructions': ASSISTANT_FORMAT_INSTRUCTIONS,
                'suffix': ASSISTANT_SUFFIX
            },
            verbose=verbose
        )
        self.last_tool = {
            'name': '',
            'argument': '',
            'result': ''
        }
        self.agent.callback_manager.on_tool_start = self._on_tool_start
        self.agent.callback_manager.on_tool_end = self._on_tool_end
    
    def _on_tool_start(self, tool: dict, argument: str, **kwargs):
        self.last_tool = {
            'name': tool['name'],
            'argument': argument,
            'result': ''
        }
    def _on_tool_end(self, output: str, **kwargs):
        self.last_tool['result'] = output

    def ask(self, message: str) -> str:
        return self.agent.run(message)
