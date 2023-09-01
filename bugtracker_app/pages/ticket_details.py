import reflex as rx
from ..components.components import base_layout
from ..states import ProjectTicketState


def ticket_core_details(**props) -> rx.Component:
    """Ticket core details"""

    return rx.box(
        rx.heading("Details for ", ProjectTicketState.ticket_title),
        rx.hstack(
            rx.link("Back to project", href="/projects/details"),
            rx.text(" | "),
            rx.cond(
                ProjectTicketState.is_admin,
                rx.hstack(
                    rx.link("Edit ticket", href="/projects/details/ticket/edit"),
                    rx.text(" | "),
                    rx.button(
                        rx.icon(tag="delete"),
                        padding=".1em",
                        on_click=lambda: ProjectTicketState.delete_ticket(),
                    ),
                ),
                rx.cond(
                    ProjectTicketState.is_assigned_admin,
                    rx.link("Edit ticket", href="/projects/details/ticket/edit"),
                ),
            ),
        ),
        rx.box(
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("TICKET TITLE"),
                        rx.th("DESCRIPTION"),
                    )
                ),
                rx.tbody(
                    rx.tr(
                        rx.td(ProjectTicketState.ticket_title),
                        rx.td(ProjectTicketState.ticket_description),
                    )
                ),
            ),
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("ASSIGNED DEVELOPER"),
                        rx.th("SUBMITTER"),
                    )
                ),
                rx.tbody(
                    rx.tr(
                        rx.td(""),
                        rx.td(""),
                    )
                ),
            ),
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("PROJECT"),
                        rx.th("TICKET PRIORITY"),
                    )
                ),
                rx.tbody(
                    rx.tr(
                        rx.td(ProjectTicketState.ticket_project),
                        rx.td(ProjectTicketState.ticket_priority),
                    )
                ),
            ),
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("TICKET STATUS"),
                        rx.th("TICKET TYPE"),
                    )
                ),
                rx.tbody(
                    rx.tr(
                        rx.td(ProjectTicketState.ticket_status),
                        rx.td(ProjectTicketState.ticket_ticket_type),
                    )
                ),
            ),
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("CREATED ON"),
                        rx.th("UPDATED ON"),
                    )
                ),
                rx.tbody(
                    rx.tr(
                        rx.td(ProjectTicketState.ticket_created_at),
                        rx.td(ProjectTicketState.ticket_updated_at),
                    )
                ),
            ),
            margin_y="2em",
        ),
        **props,
        padding_x="2em",
        border_right="1px solid gray",
    )


def comment_section(**props) -> rx.Component:
    """Add and read comments"""

    return rx.box(
        rx.heading("Add a comment"),
        rx.form(
            rx.text_area(
                placeholder="Add a comment",
                on_blur=ProjectTicketState.set_new_comment,
                rows=5,
                cols=50,
            ),
            rx.button("Add", type_="submit"),
            on_submit=ProjectTicketState.handle_add_comment_click,
            display="flex",
            align_items="baseline",
        ),
        rx.heading("Comments", size="md"),
        rx.text("All comments from this ticket"),
        rx.table(
            rx.thead(
                rx.tr(
                    rx.th("Commenter"),
                    rx.th("Message"),
                    rx.th("Commented on"),
                    rx.th(""),
                ),
            ),
            rx.tbody(
                rx.foreach(
                    ProjectTicketState.comments,
                    lambda comment: rx.tr(
                        rx.td(comment.commenter.full_name),
                        rx.td(comment.content),
                        rx.td(comment.created_at),
                        rx.cond(
                            ProjectTicketState.is_admin_or_assigned_admin,
                            rx.td(
                                rx.button(
                                    rx.icon(tag="delete"),
                                    on_click=lambda: ProjectTicketState.delete_comment(
                                        comment.id
                                    ),
                                )
                            ),
                        ),
                    ),
                ),
            ),
        ),
        **props,
        padding_x="2em",
    )


def ticket_history(**props) -> rx.Component:
    """Ticket history"""
    return rx.box(
        rx.heading("Ticket History"),
        rx.text("All history information for the ticket"),
        rx.table(
            rx.thead(
                rx.tr(
                    rx.th("Action"),
                    rx.th("Previous Value"),
                    rx.th("Present Value"),
                    rx.th("Date Changed"),
                )
            ),
            rx.tbody(
                rx.foreach(
                    ProjectTicketState.get_history,
                    lambda history: rx.tr(
                        rx.td(history.action),
                        rx.td(history.previous_value),
                        rx.td(history.present_value),
                        rx.td(history.created_at),
                    ),
                )
            ),
        ),
    )


color = "rgb(107,99,246)"


def attachment_section(**props) -> rx.Component:
    """Ticket attachments"""
    return rx.box(
        rx.box(
            rx.heading("Add an Attachment?"),
            rx.hstack(
                rx.upload(
                    rx.vstack(
                        rx.text("Select files"),
                        rx.button(
                            "Select File",
                            color=color,
                            bg="white",
                            border=f"1px solid {color}",
                        ),
                    ),
                    border=f"1px dotted {color}",
                    padding=".2em",
                ),
                rx.vstack(
                    rx.button(
                        "Upload",
                        on_click=lambda: ProjectTicketState.handle_upload(
                            rx.upload_files()
                        ),
                    ),
                    rx.foreach(ProjectTicketState.fls, lambda fl: rx.text(fl)),
                ),
                rx.hstack(
                    rx.form(
                        rx.vstack(
                            rx.text("Add a description"),
                            rx.input(id="description"),
                        ),
                        rx.button(
                            "Add",
                            type_="submit",
                        ),
                        on_submit=ProjectTicketState.handle_add_attachment_click,
                    ),
                ),
            ),
        ),
        rx.box(
            rx.heading("Ticket Attachments"),
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("File"),
                        rx.th("Uploader"),
                        rx.th("Notes"),
                        rx.th("Uploaded on"),
                        rx.th(""),
                    )
                ),
                rx.tbody(
                    rx.foreach(
                        ProjectTicketState.attachments,
                        lambda atmnt: rx.tr(
                            rx.td(
                                rx.link(
                                    atmnt.file_name,
                                    href=atmnt.file_path,
                                    download=atmnt.file_name,
                                )
                            ),
                            rx.td(),
                            rx.td(atmnt.description),
                            rx.td(atmnt.created_at),
                            rx.cond(
                                ProjectTicketState.is_admin_or_assigned_admin,
                                rx.td(
                                    rx.button(
                                        rx.icon(tag="delete"),
                                        on_click=lambda: ProjectTicketState.delete_attachment(
                                            atmnt.id
                                        ),
                                    )
                                ),
                            ),
                        ),
                    )
                ),
            ),
        ),
    )


def ticket_details():
    """Ticket details"""

    return base_layout(
        rx.box(
            ticket_core_details(),
            comment_section(),
            ticket_history(),
            attachment_section(),
            padding="3em",
            display="grid",
            grid_template_columns="1fr 1fr",
            grid_template_rows="1fr 1fr",
            gap="2em",
        )
    )
