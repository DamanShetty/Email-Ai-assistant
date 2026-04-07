# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Email Triage environment logic."""

from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from ..models import EmailTriageAction, EmailTriageObservation

TASKS = {
    "classify_easy": {
        "subject": "WIN FREE MONEY NOW!!!",
        "body": "Click here to claim your prize immediately!",
        "answer": "spam",
    },
    "reply_medium": {
        "subject": "Team sync tomorrow 10am",
        "body": "Hi, can we confirm the meeting for 10am tomorrow?",
    },
    "triage_hard": {
        "emails": [
            {"id": "A", "subject": "URGENT: Production server down", "priority": 1},
            {"id": "B", "subject": "Monthly newsletter", "priority": 3},
            {"id": "C", "subject": "Client demo in 2 hours", "priority": 2},
        ],
        "correct_order": ["A", "C", "B"],
    },
}


class EmailTriageEnvironment(Environment):
    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._current_task = "classify_easy"

    def reset(self, task: str = "classify_easy") -> EmailTriageObservation:
        self._current_task = task
        self._state = State(episode_id=str(uuid4()), step_count=0)
        t = TASKS[task]
        if task.startswith("triage"):
            return EmailTriageObservation(
                task=task,
                email_id=task,
                subject="Sort your inbox",
                body="Prioritize the emails below.",
                emails=t["emails"],
            )
        return EmailTriageObservation(
            task=task,
            email_id=task,
            subject=t["subject"],
            body=t["body"],
        )

    def step(self, action: EmailTriageAction) -> EmailTriageObservation:
        self._state.step_count += 1

        task_key = self._current_task
        task_type = task_key.split("_")[0]
        t = TASKS[task_key]

        reward = 0.0

        if task_type == "classify":
            reward = 1.0 if action.label and action.label.lower() == t["answer"] else 0.0

        elif task_type == "reply":
            if not action.reply:
                reward = 0.0
            else:
                keywords = ["meeting", "available", "confirm", "yes", "tomorrow", "time"]
                matches = sum(1 for k in keywords if k in action.reply.lower())
                reward = matches / len(keywords)

        elif task_type == "triage":
            if not action.priority_order:
                return EmailTriageObservation(
                    task=task_key,
                    email_id=task_key,
                    subject="done",
                    body="done",
                    done=True,
                    reward=0.0,
                    success=False,
                )
            if action.priority_order == t["correct_order"]:
                reward = 1.0
            elif len(action.priority_order) > 0 and action.priority_order[0] == "A":
                reward = 0.5
            else:
                reward = 0.0

        return EmailTriageObservation(
            task=task_key,
            email_id=task_key,
            subject="done",
            body="done",
            done=True,
            reward=reward,
            success=reward > 0,
        )

    @property
    def state(self) -> State:
        return self._state