# ai-control v2.1
Using GPT-4 to remotely execute code on my smartphone is a smart idea, surely. Supports voice control, and loading OpenAI Plugins. Comes with Termux shortcuts.

### What's new?

The assistant is now able to effectively execute multiple actions in a row. It does this by calling another LLM, which comes up with a plan. It also has access to a bunch more Termux API tools.

#### Just added: voice chat mode & OpenAI Plugin Loader!

## [Video Demo (*YouTube*)](https://www.youtube.com/watch?v=nWdNP0BInNo)

# features
 **Not all of these have been tested, so please open an issue if you find something not working.**

## Tools using Termux API:

* BatteryStatusTool
* BrightnessTool
* PhotoTool
* ClipboardGetTool
* ClipboardSetTool
* FingerprintTool
* LocationTool
* MediaPauseTool
* RecordMicTool
* NotificationTool
* ListNotificationsTool
* RemoveNotificationTool
* URLOpenerTool
* TorchTool
* SpeakTool
* GetVolumeTool
* SetVolumeTool
* WiFiInfoTool
* WiFiScanTool
* VibratorTool
* MediaPlayTool
* SearchContactsTool
    * This lists all contacts, but filters by name to avoid a prompt too large for OpenAIs limits.
* ListSMSTool
* SendSMSTool
* GetCellInfoTool
* StartCallTool
* ListSensorsTool
* ReadSensorTool

## Utility Tools

* Sleep
* PlanTool *(this is the second LLM that lets the assistant perforn complex series of commands)*
* GoogleSearchTool - no API key needed

## OpenAI Plugins

Langchain built their own plugin loader, but I found it didn't work how I wanted it to, so I built on top of that. You can see my work in `PluginLoader.py`. Plugins will be loaded by URL, from the list defined in your config which I will go over.

# `config.json`

This file is where you can define additional tools you want your Assistant to have. In the `langchain` section, include [tools built-in to langchain](https://python.langchain.com/en/latest/modules/agents/tools.html). If any of those tools require an API key, set it in your `.env` file. 

In the `openai` section, include any URLs of OpenAI Plugins you'd like to load (e.g., `https://www.klarna.com/.well-known/ai-plugin.json`). **This feature is highly experimental!** Also, this requires you include the `requests_all` tool in the `langchain` section of your `config.json`. 

You can use mutliple configuration files, if you want. You can specify which to load with the `--config <filename>` argument.

# Future ideas

Ngl I'm writing this for myself. Sorry if I get too verbose with it.

* executing shell commands
* scheduling events for the future
* add an option, for when running chat from a Termux environment (or when running both - as it must be a Termux environment), to **use Termux speech to text and vice versa** instead of typing to the bot

# setup/installation
Make a copy of `.env.example` named `.env` and set the following keys:

* `OPENAI_API_KEY` - from [OpenAI](https://platform.openai.com)
* `TERMUX_AGENT_URL` - the URL of where the termux agent is running
    * If you're running the termux agent and the controller on the same device, you can skip this step as it defaults to `http://localhost:8080`
    * Otherwise, it's just `http://` + your phone's IP address + `:8080` for the port

For the agent device, make sure you have the Termux-API app installed along with the interface. To install the interface, run `pkg install termux-*` from within a termux session. **Be sure to enable all permissions you want to use for Termux-API - for Android 13+ you might need to [allow restricted settings](https://support.google.com/android/answer/12623953?hl=en).**

# usage

Verbose mode will be set on as default so you can see what actions are performed.

1. Run `main.py` for the CLI interface

![Usage (old)](/media/cli_usage.png)

## termux shortcuts

*Requires the Termux-Widgets app*

* Copy the `.shortcuts` folder to your home directory (or move the scripts inside, if you already have a `.shortcuts` folder in your home dir)
