from pydantic import Field
from typing import Optional, List
from openenv.core.env_server.types import Action, Observation


class EmailTriageAction(Action):
    label: Optional[str] = Field(None)
    reply: Optional[str] = Field(None)
    priority_order: Optional[List[str]] = Field(None)


class EmailTriageObservation(Observation):
    task: str
    email_id: str
    subject: str
    body: str
    emails: Optional[List[dict]] = None

    done: bool = False
    reward: float = 0.0
    success: bool = True