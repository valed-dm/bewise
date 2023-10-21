"""Post request model"""

from pydantic import BaseModel


class Qnum(BaseModel):
    """Post request questions number"""

    qnum: int
