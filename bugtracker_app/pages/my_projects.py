import reflex as rx
from ..components.components import base_layout, project_row
from ..states import MyProjectState


def my_projects():
    return base_layout(
        rx.box(
            rx.cond(
                MyProjectState.is_admin_or_assigned_admin,
                rx.button(
                    "Create a new project",
                    width="20em",
                    padding="1em",
                    on_click=MyProjectState.change,
                ),
            ),
            rx.modal(
                rx.modal_overlay(
                    rx.modal_content(
                        rx.modal_header("Create a new project"),
                        rx.modal_body(
                            rx.form(
                                rx.vstack(
                                    rx.input(
                                        id="title",
                                        on_change=MyProjectState.set_project_title,
                                        placeholder="Project's title",
                                        is_required=True,
                                    ),
                                    rx.text_area(
                                        id="description",
                                        on_blur=MyProjectState.set_project_description,
                                        placeholder="Project's description",
                                        is_required=True,
                                    ),
                                    rx.button("Create", type_="submit"),
                                ),
                                on_submit=MyProjectState.handle_create_project,
                            ),
                        ),
                        rx.modal_footer(
                            rx.button("Close", on_click=MyProjectState.change)
                        ),
                    )
                ),
                is_open=MyProjectState.show,
            ),
            rx.heading("My Projects"),
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("Project Name"),
                        rx.th("Description"),
                        rx.th("Actions"),
                    )
                ),
                rx.tbody(
                    rx.foreach(MyProjectState.projects, project_row),
                ),
            ),
            width="100%",
            padding="3em",
        ),
    )
