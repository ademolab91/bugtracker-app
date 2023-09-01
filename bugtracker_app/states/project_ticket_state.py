import reflex as rx

# from .ticketsState import TicketsState
from .project_details_state import ProjectDetailsState
from ..models import Ticket, Project
from .schemas import AttachmentOut, TicketHistoryOut, CommentOut
from ..enumerations import TicketType, Priority, Status, Action
from .manage_project_users_state import Member
from ..models import User, TicketHistory, Attachment, Comment


class ProjectTicketState(ProjectDetailsState):
    """Project ticket state"""

    ticket_title: str = ""
    ticket_description: str = ""
    ticket_submitter: str = ""
    ticket_assigned_developer: str = ""
    ticket_ticket_type: TicketType
    ticket_priority: Priority
    ticket_status: Status
    ticket_project: str = ""
    attachments: list[AttachmentOut]
    history: list[TicketHistoryOut]
    comments: list[CommentOut]
    ticket_created_at: str = ""
    ticket_updated_at: str = ""

    new_comment: str = ""
    attachment_form_data: dict = {}
    fls: list[str]
    outfiles: list[str]

    def get_ticket_details(self):
        """Get ticket"""

        if not self.logged_in:
            return rx.redirect("/login")

        with rx.session() as session:
            ticket = session.query(Ticket).get(self.ticket_id)
            self.ticket_title = ticket.title
            self.ticket_description = ticket.description
            self.ticket_priority = ticket.priority
            self.ticket_ticket_type = ticket.ticket_type
            self.ticket_status = ticket.status
            if ticket.assigned_developer_id != None:
                self.ticket_assigned_developer = (
                    session.query(User).get(ticket.assigned_developer_id).full_name
                )
            self.ticket_submitter = (
                session.query(User).get(ticket.submitter_id).full_name
            )
            self.attachments = ticket.attachments
            self.history = ticket.history
            comments = ticket.comments
            for comment in comments:
                comment.commenter = (
                    session.query(User).where(User.id == comment.commenter_id).first()
                )
            self.comments = comments
            self.ticket_created_at = ticket.created_at
            self.ticket_project = session.query(Project).get(ticket.project_id).title
            if ticket.created_at != ticket.updated_at:
                self.ticket_updated_at = ticket.updated_at

    @rx.var
    def get_history(self) -> list[TicketHistoryOut]:
        """Get ticket history"""

        with rx.session() as session:
            history = (
                session.query(TicketHistory)
                .where(TicketHistory.ticket_id == self.ticket_id)
                .all()
            )
            # for item in history:
            #     if item.action == Action.ASSIGNED_DEVELOPER_CHANGE:
            #         if item.previous_value:
            #             item.previous_value = (
            #                 session.query(User).where(User.email == item.previous_value).full_name
            #             )
            #         if item.present_value:
            #             item.present_value = (
            #                 session.query(User).get(item.present_value).full_name
            #             )
        return history

    def handle_add_comment_click(self):
        """Handle add comment button click"""

        from ..models import Comment

        with rx.session() as session:
            session.add(
                Comment(
                    content=self.new_comment,
                    ticket_id=self.ticket_id,
                    commenter_id=self.user.id,
                )
            )
            session.commit()
            self.comments = (
                session.query(Comment).where(Comment.ticket_id == self.ticket_id).all()
            )

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle file upload"""

        if not files:
            return rx.window_alert("Please select a file to upload")

        for file in files:
            upload_data = await file.read()
            outfile = rx.get_asset_path(file.filename)

            with open(outfile, "wb") as f:
                f.write(upload_data)

            self.fls.append(file.filename)
            self.outfiles.append(outfile)
        return rx.window_alert("File uploaded successfully, Add description")

    def handle_add_attachment_click(self, form_data: dict):
        """Handle add attachment button click"""

        self.attachment_form_data = form_data
        if (
            not self.fls
            or not self.outfiles
            or self.attachment_form_data["description"] == ""
        ):
            return rx.window_alert("Please select a file to upload and a description")

        for filename, outfile in zip(self.fls, self.outfiles):
            with rx.session() as session:
                session.add(
                    Attachment(
                        file_name=filename,
                        description=self.attachment_form_data["description"],
                        file_path=outfile,
                        ticket_id=self.ticket_id,
                    )
                )
                session.commit()
        with rx.session() as session:
            self.attachments = (
                session.query(Attachment)
                .where(Attachment.ticket_id == self.ticket_id)
                .all()
            )
        self.fls = self.outfiles = []

    def delete_ticket(self):
        """Delete ticket"""

        with rx.session() as session:
            session.query(Ticket).where(Ticket.id == self.ticket_id).delete()
            session.commit()
        return rx.redirect("/projects/details")

    def delete_attachment(self, atmnt_id: str):
        """Delete attachment"""

        with rx.session() as session:
            session.query(Attachment).where(Attachment.id == atmnt_id).delete()
            session.commit()
            self.attachments = (
                session.query(Attachment)
                .where(Attachment.ticket_id == self.ticket_id)
                .all()
            )

    def delete_comment(self, comment_id: str):
        with rx.session() as session:
            comment = session.query(Comment).get(comment_id)
            session.delete(comment)
            session.commit()
            self.comments = (
                session.query(Comment).where(Comment.ticket_id == self.ticket_id).all()
            )
