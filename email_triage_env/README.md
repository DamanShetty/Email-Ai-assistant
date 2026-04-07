# Email Triage Environment

Managing email efficiently is a common challenge. This project models a simple email triage workflow where an agent is evaluated on how well it can classify messages, draft replies, and prioritize tasks.

## Tasks

* `classify_easy`: classify an email as `spam`, `urgent`, or `normal`
* `reply_medium`: write a short, professional one-line reply
* `triage_hard`: arrange multiple emails based on urgency

## Tech Stack

* Python
* FastAPI (via OpenEnv)
* OpenEnv environment interface

## Running Locally

From the project root:

```bash
uvicorn email_triage_env.server.app:app --host 0.0.0.0 --port 8000
```

In a separate terminal:

```bash
py inference.py
```

To validate the setup:

```bash
cd email_triage_env
openenv validate .
```

## How It Works

The `inference.py` script runs each task one by one. For every task, it:

* resets the environment
* builds a structured prompt
* converts the model’s response into valid JSON
* sends the action back to the environment

The system keeps the flow simple and logs only key steps during execution.
