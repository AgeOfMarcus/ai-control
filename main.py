from argparse import ArgumentParser
from _thread import start_new_thread
import time
import os

def chat(args):
    os.environ['TERMUX_AGENT_URL'] = f'http://{args.host}:{args.port}'
    from chatbot import Chatbot
    bot = Chatbot(verbose=args.verbose)
    if args.voice:
        from termux_agent import sh
        get_voice = lambda: sh('termux-speech-to-text').strip()
        say_voice = lambda text: sh(f'termux-tts-speak "{text}"')
        while True:
            print('You: ', end='')
            msg = get_voice()
            while not msg:
                print('... ', end='')
                msg = get_voice()
            print(msg)

            resp = bot.ask(msg)
            print('Bot: ', resp, '\n\n')
            say_voice(resp)
    else:
        while True:
            message = input('You: ')
            print('Bot: ', bot.ask(message))
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

args = p.parse_args()
if args.agent:
    agent(args)
elif args.chat:
    chat(args)
elif args.both:
    start_new_thread(agent, (args,))
    time.sleep(2)
    chat(args)