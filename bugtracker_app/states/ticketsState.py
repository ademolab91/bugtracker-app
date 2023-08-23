from .auth import AuthState
import reflex as rx
from ..models import Ticket, User, Project, UserProject
from .schemas import TicketOut


class TicketsState(AuthState):
    """All ticket state"""

    tickets: list[TicketOut] = []

    def get_all_tickets(self) -> list[TicketOut]:
        """Get all tickets"""

        if not self.logged_in:
            return rx.redirect("/login")

        with rx.session() as session:
            tkts = []
            if self.is_admin or self.is_assigned_admin:
                tkts = session.query(Ticket).all()

            elif self.is_project_manager:
                tkts = (
                    session.query(Ticket)
                    .join(Project, Project.id == Ticket.project_id)
                    .join(UserProject, UserProject.project_id == Project.id)
                    .filter(UserProject.user_id == self.user.id)
                    .all()
                )
                print(tkts)

            elif self.is_developer:
                tkts = (
                    session.query(Ticket)
                    .filter(Ticket.assigned_developer_id == self.user.id)
                    .all()
                )

            elif self.is_submitter:
                tkts = (
                    session.query(Ticket)
                    .filter(Ticket.submitter_id == self.user.id)
                    .all()
                )

            else:
                tkts = []

            if tkts:
                for tkt in tkts:
                    tkt.project_name = (
                        session.query(Project)
                        .where(Project.id == tkt.project_id)
                        .first()
                        .title
                    )
                    tkt.assigned_developer_name = (
                        session.query(User)
                        .where(User.id == tkt.assigned_developer_id)
                        .first()
                        .full_name
                    )

            self.tickets = tkts
