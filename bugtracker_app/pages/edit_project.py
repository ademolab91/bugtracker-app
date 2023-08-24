import reflex as rx
from ..states import ProjectDetailsState
from ..components.components import base_layout
from ..models import Project
from datetime import datetime


class EditProjectState(ProjectDetailsState):
    new_description: str = ""
    form_data: dict = {}

    def handle_edit(self, form_data: dict):
        """Handle edit"""

        self.form_data = form_data

        with rx.session() as session:
            project = (
                session.query(Project).where(Project.id == self.project_id).first()
            )
            project.title = self.form_data.get("title", self.title)
            if self.new_description != "":
                project.description = self.new_description
            project.updated_at = datetime.utcnow()
            session.add(project)
            session.commit()
            session.refresh(project)
        return rx.window_alert("Project has been successfully edited")


def edit_project():
    """Project editing page"""

    return base_layout(
        rx.container(
            rx.form(
                rx.input(default_value=EditProjectState.title, id="title"),
                rx.text_area(
                    default_value=EditProjectState.description,
                    on_blur=EditProjectState.set_new_description,
                ),
                rx.button("Edit", type_="submit"),
                on_submit=EditProjectState.handle_edit,
            )
        )
    )
