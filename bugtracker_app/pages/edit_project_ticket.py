import reflex as rx
from ..states import ProjectTicketState
from ..components.components import base_layout
from ..enumerations import TicketType, Priority, Status, Role, Action
from ..models import User, Ticket, TicketHistory
from datetime import datetime


ticket_types: list = [
    TicketType.BUG_ERROR,
    TicketType.CHANGE_REQUEST,
    TicketType.DOCUMENTATION,
    TicketType.FEATURE_REQUEST,
    TicketType.FEEDBACK,
    TicketType.INCIDENT,
    TicketType.SECURITY,
    TicketType.SUPPORT_HELPDESK,
    TicketType.TASK,
    TicketType.OTHER,
]

priorities: list = [Priority.HIGH, Priority.LOW, Priority.MEDIUM, Priority.NONE]

statuses: list = [
    Status.CLOSED,
    Status.DUPLICATE,
    Status.IN_PROGRESS,
    Status.OPEN,
    Status.PENDING,
    Status.REOPENED,
    Status.RESOLVED,
]


class EditTicket(ProjectTicketState):
    new_description: str = ""
    developer_option: str = ""

    ticket_type_option: TicketType = ""
    priority_option: Priority = ""
    status_option: Status = ""

    form_data: dict = {}

    @rx.var
    def developers(self) -> list[User]:
        """Get project developers"""
        return [user.email for user in self.members if user.role == Role.DEVELOPER]

    def handle_edit(self, form_data: dict):
        """Handle ticket edit"""

        self.form_data = form_data

        current_time = datetime.utcnow()

        with rx.session() as session:
            ticket = session.query(Ticket).where(Ticket.id == self.ticket_id).first()

            if self.form_data["title"] and self.ticket_title != self.form_data["title"]:
                ticket.title = self.form_data["title"]
                ticket_history = TicketHistory(
                    created_at=current_time,
                    updated_at=current_time,
                    action=Action.TITLE_CHANGE,
                    previous_value=self.ticket_title,
                    present_value=self.form_data["title"],
                    ticket_id=ticket.id,
                )
                session.add(ticket)
                session.add(ticket_history)

            if (
                self.ticket_description != self.new_description
                and self.new_description != ""
            ):
                ticket.description = self.new_description
                ticket_history = TicketHistory(
                    created_at=current_time,
                    updated_at=current_time,
                    action=Action.DESCRIPTION_CHANGE,
                    previous_value=self.ticket_description,
                    present_value=self.new_description,
                    ticket_id=ticket.id,
                )
                session.add(ticket)
                session.add(ticket_history)

            if (
                self.ticket_ticket_type != self.ticket_type_option
                and self.ticket_type_option != ""
            ):
                ticket.ticket_type = self.ticket_type_option
                ticket_history = TicketHistory(
                    created_at=current_time,
                    updated_at=current_time,
                    action=Action.TICKET_TYPE_CHANGE,
                    previous_value=self.ticket_ticket_type,
                    present_value=self.ticket_type_option,
                    ticket_id=ticket.id,
                )
                session.add(ticket)
                session.add(ticket_history)

            if (
                self.ticket_priority != self.priority_option
                and self.priority_option != ""
            ):
                ticket.priority = self.priority_option
                ticket_history = TicketHistory(
                    created_at=current_time,
                    updated_at=current_time,
                    action=Action.PRIORITY_CHANGE,
                    previous_value=self.ticket_priority,
                    present_value=self.priority_option,
                    ticket_id=ticket.id,
                )
                session.add(ticket)
                session.add(ticket_history)

            if self.ticket_status != self.status_option and self.status_option != "":
                ticket.status = self.status_option
                ticket_history = TicketHistory(
                    created_at=current_time,
                    updated_at=current_time,
                    action=Action.PRIORITY_CHANGE,
                    previous_value=self.ticket_status,
                    present_value=self.status_option,
                    ticket_id=ticket.id,
                )
                session.add(ticket)
                session.add(ticket_history)

            if self.developer_option != "":
                user = (
                    session.query(User)
                    .where(User.email == self.developer_option)
                    .first()
                )
                ticket.assigned_developer_id = user.id
                ticket_history = TicketHistory(
                    created_at=current_time,
                    updated_at=current_time,
                    action=Action.ASSIGNED_DEVELOPER_CHANGE,
                    previous_value=self.ticket_assigned_developer,
                    present_value=user.email,
                    ticket_id=ticket.id,
                )
                session.add(ticket)
                session.add(ticket_history)

            session.commit()
            session.refresh(ticket)
            print(ticket)

        # print(
        #     self.form_data,
        #     "\n",
        #     self.new_description,
        #     "\n",
        #     self.ticket_type_option,
        #     "\n",
        #     self.priority_option,
        #     "\n",
        #     self.status_option,
        #     "\n",
        #     self.developer_option,
        # )


def edit_project_ticket():
    """Edit a ticket"""

    return base_layout(
        rx.container(
            rx.form(
                rx.input(id="title", default_value=EditTicket.ticket_title),
                rx.text_area(
                    default_value=EditTicket.ticket_description,
                    on_blur=EditTicket.set_new_description,
                ),
                rx.select(
                    ticket_types,
                    default_value=EditTicket.ticket_ticket_type,
                    on_change=EditTicket.set_ticket_type_option,
                ),
                rx.select(
                    priorities,
                    default_value=EditTicket.ticket_priority,
                    on_change=EditTicket.set_priority_option,
                ),
                rx.select(
                    statuses,
                    default_value=EditTicket.ticket_status,
                    on_change=EditTicket.set_status_option,
                ),
                rx.select(
                    EditTicket.developers,
                    default_value=EditTicket.ticket_assigned_developer,
                    on_change=EditTicket.set_developer_option,
                ),
                rx.button("Edit", type_="submit"),
                on_submit=EditTicket.handle_edit,
            )
        )
    )
