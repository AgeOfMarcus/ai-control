# ai-control v2
Using GPT-4 to remotely execute code on my smartphone is a smart idea, surely. 

### What's new?

The assistant is now able to effectively execute multiple actions in a row. It does this by calling another LLM, which comes up with a plan.

## [Video Demo (*YouTube*) - somewhat outdated](https://youtu.be/0evGdb2RLDY)

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
* ListContactsTool
* ListSMSTool
* SendSMSTool
* GetCellInfoTool
* StartCallTool
* ListSensorsTool
* ReadSensorTool

## Utility Tools

* Sleep
* PlanTool *(this is the second LLM that lets the assistant perforn complex series of commands)*

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

![Usage](/media/cli_usage.png)
