import reflex as rx
from .auth import AuthState
from ..models import Project


class MyProjectState(AuthState):
    """State for my projects page."""

    project_title: str = ""
    project_description: str = ""

    project_id: str = ""

    show: bool = False

    def change(self):
        self.show = not (self.show)

    @rx.var
    def projects(self) -> list[Project]:
        """List of projects."""
        with rx.session() as session:
            projects = session.query(Project).all()
            if self.is_admin or self.is_assigned_admin:
                return projects
            return [project for project in projects if self.user in project.members]

    def set_project_id(self, project_id: str):
        """Set project id."""
        self.project_id = project_id

    def handle_create_project(self):
        """Handle creation of project"""

        with rx.session() as session:
            project = Project(
                title=self.project_title, description=self.project_description
            )
            session.add(project)
            session.commit()
        self.project_title = self.project_description = ""
        self.change()

    def delete_project(self, project_id: str):
        """Delete project by id"""

        with rx.session() as session:
            project = session.query(Project).where(Project.id == project_id).delete()
            session.commit()
        self.projects = self.projects
