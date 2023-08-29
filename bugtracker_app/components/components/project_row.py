import reflex as rx
from ...states import MyProjectState


def project_row(project, **props):
    """View project"""

    return rx.tr(
        rx.td(project.title),
        rx.td(project.description),
        rx.td(
            rx.list(
                rx.cond(
                    MyProjectState.is_admin,
                    rx.list_item(
                        rx.hstack(
                            rx.link(
                                "Manage users",
                                href="/manage-project-users",
                            ),
                            rx.text(" | "),
                            rx.button(
                                rx.icon(tag="delete"),
                                on_click=lambda: MyProjectState.delete_project(
                                    project.id
                                ),
                            ),
                        )
                    ),
                    rx.cond(
                        MyProjectState.is_assigned_admin,
                        rx.list_item(
                            rx.hstack(
                                rx.link(
                                    "Manage users",
                                    href="/manage-project-users",
                                ),
                                rx.text(" | "),
                                rx.button(
                                    rx.icon(tag="delete"),
                                    on_click=lambda: MyProjectState.delete_project(
                                        project.id
                                    ),
                                ),
                            )
                        ),
                    ),
                ),
                rx.list_item(
                    rx.link(
                        "Details",
                        href="/projects/details",
                        on_click=MyProjectState.set_project_id(project.id),
                    )
                ),
            )
        ),
    )
