from langchain.tools import BaseTool
import asyncio, time

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