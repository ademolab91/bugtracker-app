from ..states import TicketsState
from ..components.components import base_layout
import reflex as rx


def tickets():
    """Tickets page"""

    return base_layout(
        rx.box(
            rx.heading("Your tickets"),
            rx.text("This is where you can see all your tickets."),
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("Title"),
                        rx.th("Project Name"),
                        rx.th("Developer"),
                        rx.th("Ticket Priority"),
                        rx.th("Ticket Status"),
                        rx.th("Ticket Type"),
                        rx.th("Created On"),
                        rx.th(""),
                    ),
                ),
                rx.tbody(
                    rx.foreach(
                        TicketsState.tickets,
                        lambda ticket: rx.tr(
                            rx.td(ticket.title),
                            rx.td(ticket.project_name),
                            rx.td(ticket.assigned_developer_name),
                            rx.td(ticket.priority),
                            rx.td(ticket.status),
                            rx.td(ticket.ticket_type),
                            rx.td(ticket.created_at),
                            rx.td(
                                rx.list(
                                    rx.list_item(
                                        rx.link("Edit / Assign", href="/tickets/edit")
                                    ),
                                    rx.list_item(
                                        rx.link("Details", href="/tickets/details")
                                    ),
                                )
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
