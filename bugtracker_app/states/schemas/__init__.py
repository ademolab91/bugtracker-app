import reflex as rx
from ...enumerations import Action
from ..manage_project_users_state import Member


class AttachmentOut(rx.Base):
    """Attachment out"""

    id: str
    file_name: str
    description: str
    file_path: str
    created_at: str


class TicketHistoryOut(rx.Base):
    """Ticket history out"""

    action: Action
    previous_value: str
    present_value: str
    created_at: str


class CommentOut(rx.Base):
    """Comment out"""

    id: str
    content: str
    commenter: Member
    created_at: str


class TicketOut(rx.Base):
    """Ticket out"""

    id: str
    title: str
    assigned_developer_name: str
    project_name: str
    ticket_type: str
    priority: str
    status: str
    created_at: str
