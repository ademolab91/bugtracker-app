import reflex as rx
from ..enumerations import Role
from ..states import AuthState
from ..components.components import base_layout
from ..models import User


roles = [Role.ASSIGNED_ADMIN, Role.DEVELOPER, Role.PROJECT_MANAGER, Role.SUBMITTER]


class ManageRoleAssignmentState(AuthState):
    """Manage role assignment State"""

    option: str = "No selection yet"

    @rx.var
    def users(self) -> list[User]:
        """Get users"""

        with rx.session() as session:
            db_users = session.query(User).all()
        return db_users

    def handle_role_assignment(self, id: str):
        """Handle role assignment"""

        with rx.session() as session:
            user = session.query(User).where(User.id == id).first()
            if self.disable(user):
                self.option = ""
                return rx.window_alert("Cannot assign ADMIN")
            if self.option == "":
                return rx.window_alert("Please select a valid role")
            user.role = self.option
            session.add(user)
            session.commit()
            session.refresh(user)
        self.option = ""
        # self.users()

    def disable(self, user) -> bool:
        """Return True if user is admin

        Return True if user
        is assigned_admin and self.user is assigned_admin

        Else: return False
        """
        if user.role == Role.ADMIN:
            return True
        elif user.role == Role.ASSIGNED_ADMIN and self.user.role == Role.ASSIGNED_ADMIN:
            return True
        return False


def manage_role_assignment():
    """Manage role assignment page"""

    return base_layout(
        rx.box(
            rx.heading("Manage user roles", size="lg"),
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("User"),
                        rx.th("Role"),
                        rx.th("Action"),
                    )
                ),
                rx.tbody(
                    rx.foreach(
                        ManageRoleAssignmentState.users,
                        lambda user: rx.tr(
                            rx.td(
                                user.email,
                                rx.td(user.role),
                                rx.td(
                                    rx.form(
                                        rx.select(
                                            roles,
                                            placeholder="Select role",
                                            on_change=ManageRoleAssignmentState.set_option,
                                        ),
                                        rx.button(
                                            "Assign",
                                            type_="submit",
                                        ),
                                        on_submit=lambda: ManageRoleAssignmentState.handle_role_assignment(
                                            user.id
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        )
    )
