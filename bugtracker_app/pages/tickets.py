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
                        TicketsState.tkts,
                        lambda ticket: rx.tr(
                            rx.td(ticket.title),
                            rx.td(ticket.project_name),
                            rx.td(ticket.assigned_developer_name),
                            rx.td(ticket.priority),
                            rx.td(ticket.status),
                            rx.td(ticket.ticket_type),
                            rx.td(ticket.created_at),
                            rx.td(
                                rx.hstack(
                                    rx.link(
                                        "Details",
                                        href="/projects/details/ticket",
                                        on_click=lambda: TicketsState.set_ticket_id(
                                            ticket.id
                                        ),
                                    ),
                                    rx.text(" | "),
                                    rx.button(rx.icon(tag="delete"), on_click=lambda: TicketsState.delete_ticket(ticket.id))
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
