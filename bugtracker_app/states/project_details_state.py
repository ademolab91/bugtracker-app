import reflex as rx
from .my_projects_state import MyProjectState
from ..models import Project, Ticket, User
from .manage_project_users_state import Member
from ..enumerations import TicketType, Priority, Status


class TicketOut(rx.Base):
    """Ticket out."""

    id: str
    title: str
    submitter: Member
    assigned_developer: Member | None
    ticket_type: TicketType
    priority: Priority
    status: Status
    created_at: str


class ProjectDetailsState(MyProjectState):
    """State for project details page."""

    title: str = ""
    description: str = ""
    members: list[User] = []

    ticket_id: str = ""

    show_add_ticket_modal: bool = False

    ticket_type_for_new_ticket: TicketType = TicketType.BUG_ERROR
    new_ticket_description: str = ""
    new_ticket_title: str = ""

    def change_add_ticket_modal_state(self):
        self.show_add_ticket_modal = not (self.show_add_ticket_modal)

    def handle_add_ticket_submit(self):
        with rx.session() as session:
            ticket = Ticket(
                title=self.new_ticket_title,
                description=self.new_ticket_description,
                ticket_type=self.ticket_type_for_new_ticket,
                project_id=self.project_id,
                submitter_id=self.user.id,
                priority=Priority.NONE,
                status=Status.OPEN,
            )
            session.add(ticket)
            session.commit()
        self.ticket_type_for_new_ticket = TicketType.BUG_ERROR
        self.new_ticket_description = ""
        self.new_ticket_title = ""
        self.change_add_ticket_modal_state()

    def get_project_details(self) -> Project:
        """Project."""
        if not self.logged_in:
            return rx.redirect("/login")
        with rx.session() as session:
            project = session.query(Project).get(self.project_id)
            self.title = project.title
            self.description = project.description
            self.members = project.members

    @rx.var
    def tickets(self) -> list[TicketOut]:
        """List of tickets."""
        with rx.session() as session:
            tickets = session.query(Ticket).filter_by(project_id=self.project_id).all()
            for ticket in tickets:
                ticket.submitter = session.query(User).get(ticket.submitter_id)
                if ticket.assigned_developer_id != None:
                    ticket.assigned_developer = session.query(User).get(
                        ticket.assigned_developer_id
                    )
            return tickets

    def set_ticket_id(self, ticket_id: str):
        """Set ticket in view"""
        self.ticket_id = ticket_id
