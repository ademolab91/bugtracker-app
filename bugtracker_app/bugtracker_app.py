"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from .styles import styles
from .pages import (
    login_page,
    dashboard,
    manage_project_users,
    my_projects,
    project_details,
    ticket_details,
    tickets,
    manage_role_assignment,
    edit_project,
    edit_project_ticket,
)
from .states import (
    State,
    DashBoardState,
    ProjectDetailsState,
    ProjectTicketState,
    TicketsState,
    ManageProjectUsersState,
)
from .pages.manage_role_assignment import ManageRoleAssignmentState
from .components.components import home_header

import reflex as rx


def index() -> rx.Component:
    return rx.box(
        home_header(),
        rx.vstack(
            rx.heading("Keep track of bugs"),
            rx.text("Try Bug tracker now"),
            rx.link(
                "Dashboard",
                href="/dashboard",
                padding=".7em",
                width="200px",
                border="1px solid black",
                _hover={
                    "color": "white",
                    "background-color": "black",
                    "text_decoration": "none",
                },
                margin_y=".2em",
                text_align="center",
            ),
        ),
        display="flex",
        justify_content="center",
        align_items="center",
        flex_direction="column",
        height="100vh",
        width="100vw",
        background_color="#0093E9",
        background_image="linear-gradient(160deg, #0093E9 0%, #80D0C7 100%)",
    )


# Add state and page to the app.
app = rx.App(state=State, style=styles, stylesheets=["fonts/tenor_sans.css"])
app.add_page(index)
app.add_page(login_page, route="/login")
app.add_page(dashboard, route="/dashboard", on_load=DashBoardState.prepare_dashboard())
app.add_page(
    manage_project_users,
    route="/manage-project-users",
    on_load=ManageProjectUsersState.check_login(),
)
app.add_page(my_projects, route="/projects", on_load=State.check_login())
app.add_page(
    project_details,
    route="/projects/details",
    on_load=ProjectDetailsState.get_project_details(),
)
app.add_page(
    ticket_details,
    route="/projects/details/ticket",
    on_load=ProjectTicketState.get_ticket_details(),
)
app.add_page(tickets, route="/tickets", on_load=TicketsState.get_all_tickets())
app.add_page(
    manage_role_assignment,
    route="/manage-role-assignments",
    on_load=ManageRoleAssignmentState.check_login(),
)
app.add_page(edit_project, route="/projects/details/edit", on_load=State.check_login())
app.add_page(
    edit_project_ticket,
    route="/projects/details/ticket/edit",
    on_load=State.check_login(),
)
app.compile()
