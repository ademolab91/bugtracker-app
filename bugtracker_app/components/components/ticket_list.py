import reflex as rx
from ...states import ProjectDetailsState
from ...enumerations import TicketType


def ticket_list(**props) -> rx.Component:
    """Ticket list"""

    return rx.box(
        rx.heading("Tickets", size="lg"),
        rx.text("Tickets for this project."),
        rx.table(
            rx.thead(
                rx.tr(
                    rx.th("Title"),
                    rx.th("Submitter"),
                    rx.th("Status"),
                    rx.th("Assigned To"),
                    rx.th("Submitted on"),
                )
            ),
            rx.tbody(
                rx.foreach(
                    ProjectDetailsState.tickets,
                    lambda ticket: rx.tr(
                        rx.td(ticket.title),
                        rx.td(ticket.submitter.full_name),
                        rx.td(ticket.status),
                        rx.td(ticket.assigned_developer.full_name),
                        rx.td(ticket.created_at),
                        rx.td(
                            rx.link(
                                "More details",
                                href="/projects/details/ticket",
                                on_click=lambda: ProjectDetailsState.set_ticket_id(
                                    ticket.id
                                ),
                            )
                        ),
                    ),
                ),
            ),
        ),
        rx.button(
            "Submit ticket", on_click=ProjectDetailsState.change_add_ticket_modal_state
        ),
        rx.modal(
            rx.modal_overlay(
                rx.modal_content(
                    rx.modal_header("Submit ticket"),
                    rx.modal_body(
                        rx.form(
                            rx.input(
                                placeholder="Title",
                                on_change=ProjectDetailsState.set_new_ticket_title,
                                is_required=True,
                            ),
                            rx.text_area(
                                placeholder="Description",
                                on_change=ProjectDetailsState.set_new_ticket_description,
                                is_required=True,
                            ),
                            rx.select(
                                [
                                    TicketType.BUG_ERROR,
                                    TicketType.FEATURE_REQUEST,
                                    TicketType.OTHER,
                                    TicketType.CHANGE_REQUEST,
                                    TicketType.DOCUMENTATION,
                                    TicketType.FEEDBACK,
                                    TicketType.INCIDENT,
                                    TicketType.SECURITY,
                                    TicketType.TASK,
                                    TicketType.SUPPORT_HELPDESK,
                                ],
                                placeholder="Select Ticket type",
                                on_change=ProjectDetailsState.set_ticket_type_for_new_ticket,
                                is_required=True,
                            ),
                            rx.button("Submit", type_="submit"),
                            on_submit=ProjectDetailsState.handle_add_ticket_submit,
                        )
                    ),
                    rx.modal_footer(
                        rx.button(
                            "Close",
                            on_click=ProjectDetailsState.change_add_ticket_modal_state,
                        )
                    ),
                )
            ),
            is_open=ProjectDetailsState.show_add_ticket_modal,
        ),
        **props,
    )
