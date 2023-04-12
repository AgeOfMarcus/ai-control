from langchain.tools import BaseTool
from langchain.llms import OpenAI
from langchain.llms.base import BaseLLM
from pydantic import Field
import asyncio, time, json
# RemoteTools.py
from RemoteTools import REMOTE_TOOLS

class PlanTool(BaseTool):
    name = "Planning Tool"
    description = (
        "Useful for determining a plan of steps to take to achieve a goal."
        "Use this when asked to preform a series of actions."
        "Accepts a single argument, which is a string representing the goal."
        "Returns a list of dictionaries, each containing a 'name' and 'argument' key."
    )
    llm: BaseLLM = Field(default_factory=lambda: OpenAI(temperature=0))

    def _run(self, goal):
        resp = self.llm.run(f"""
        You are given a goal: {goal}.
        You must plan out a series of steps to achieve this goal.
        Here is a list of tools you have available to accomplish this goal:
        {', '.join([(tool.name, tool.description) for tool in REMOTE_TOOLS])}

        Return a list of dictionaries, each containing a 'name' and 'argument' key.
        """)
        return json.loads(resp)

    async def _arun(self, goal):
        return self._run(goal)

class SleepTool(BaseTool):
    name = 'Sleep'
    description = (
        'Useful for waiting for a certain amount of time before continuing.'
        'Use this when asked to wait between commands.'
        'Accepts a single argument, which is an integer representing the number of seconds to wait.'
    )

    def _run(self, seconds):
        time.sleep(int(seconds))
        return 'done'

    async def _arun(self, seconds):
        await asyncio.sleep(int(seconds))
        return 'done'

UTIL_TOOLS = [
    SleepTool(),
]