from argparse import ArgumentParser
from _thread import start_new_thread
import requests
import time, json, os

def get_tools_from_config(cfg: dict):
    from langchain.agents import load_tools
    from PluginLoader import PluginLoader # PluginLoader.py
    tools = []
    for url in cfg['tools']['openai']:
        tools.append(PluginLoader(url).get_tool())
    if (l_tools := cfg['tools']['langchain']):
        tools += load_tools(l_tools)
    return tools

def shutdown_server(agent_url: str):
    requests.get(f'{agent_url}/shutdown')

def chat(args):
    os.environ['TERMUX_AGENT_URL'] = f'http://{args.host}:{args.port}'
    from chatbot import Chatbot
    config = json.load(open(args.config, 'r'))
    tools = get_tools_from_config(config)
    bot = Chatbot(verbose=args.verbose, tools=tools)
    if args.voice:
        from termux_agent import sh
        get_voice = lambda: sh('termux-speech-to-text').strip()
        say_voice = lambda text: sh(f'termux-tts-speak "{text}"')
        while True:
            say_voice("Listening!")
            time.sleep(0.5)
            print('You: ', end='')
            msg = get_voice()
            while not msg:
                print('... ', end='')
                time.sleep(0.5)
                msg = get_voice()
            print(msg)

            resp = bot.ask(msg)
            say_voice(resp)
            print('Bot: ', resp, '\n\n')
            if args.once:
                break
    else:
        while True:
            message = input('You: ')
            print('Bot: ', bot.ask(message))
            if args.once:
                break
def agent(args):
    from termux_agent import main
    main(host=args.host, port=args.port)

p = ArgumentParser()
p.add_argument(
    '-c', '--chat', 
    action='store_true', 
    help=(
        "Start the chatbot interface."
    )
)
p.add_argument(
    '--voice',
    action='store_true',
    help=(
        "Start the chatbot interface with voice input and output."
    )
)
p.add_argument(
    '-a', '--agent',
    action='store_true',
    help=(
        "Start the agent server."
        "Must be run from inside Termux."
    )
)
p.add_argument(
    "-b", "--both",
    action='store_true',
    help=(
        "Starts the agent server, and then starts the chatbot interface."
        "Must be run from inside Termux."
    )
)
p.add_argument(
    "--host",
    default='127.0.0.1',
    type=str,
    help=(
        "For running the Termux agent server."
        "Defaults to localhost."
    )
)
p.add_argument(
    "--port",
    default=8080,
    type=int,
    help=(
        "For running the Termux agent server."
        "Defaults to 8080."
    )
)
p.add_argument(
    '-v', '--verbose',
    action='store_true',
    default=True,
    help=(
        "Prints verbose output."
        "Defaults to True (until v2 release)."
    )
)
p.add_argument(
    '--once',
    action='store_true',
    help=(
        "For chat mode, exit after one interaction."
    )
)
p.add_argument(
    '--config',
    default='config.json',
    type=str,
    help=(
        "Path to the config file containing additional tools to load."
        "Defaults to config.json."
    )
)

args = p.parse_args()
if args.agent:
    agent(args)
elif args.chat:
    chat(args)
elif args.both:
    start_new_thread(agent, (args,))
    time.sleep(1.3)
    chat(args)
    shutdown_server(f'http://{args.host}:{args.port}')
    exit(0)
