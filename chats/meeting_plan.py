from jumpscale.loader import j
from jumpscale.sals.chatflows.chatflows import GedisChatBot, chatflow_step


class MeetingPlan(GedisChatBot):

    # Chatflow steps
    steps = ["description_step", "scheduling_step", "documents_step", "confirmation"]

    # Chatflow title
    title = "Meeting Plan"

    @chatflow_step("Welcome")
    def description_step(self):
        self.logged_in_user = self.user_info()
        self.username = self.logged_in_user["username"].split(".3bot")[0]
        email = self.logged_in_user["email"]
        self.md_show(
            f"Welcome {self.username} to the meeting planner! This platform will be used to plan and gather required information for the next meeting.",
            required=True,
        )

    @chatflow_step("Meeting Scheduling")
    def scheduling_step(self):
        form = self.new_form()
        chosen_time = form.datetime_picker(
            "When do you prefer the meeting to take place?", default=j.data.time.get().timestamp, required=True
        )
        place = form.drop_down_choice(
            "Where do you prefer the meeting to be held?", ["Belgium", "Spain", "Egypt"], required=True
        )
        form.ask()
        self.meeting_time = int(chosen_time.value)
        self.meeting_place = place.value

    @chatflow_step("Relevant Document")
    def documents_step(self):
        self.documents = self.upload_file(
            """Please add any relevant document or notes that will be used in the meeting
                    Just upload the file with the key""",
            required=True,
        )

    @chatflow_step(title="Confirmation", disable_previous=True, final_step=True)
    def confirmation(self):
        report = f"""# Hello {self.username}
## You have successfully submitted a response \n\n<br>\n
### You prefer the meeting to be held on {j.data.time.get(self.meeting_time).format()} in {self.meeting_place}
### You have attached the following to be used as meeting notes:
### {self.documents}
        """

        self.md_show(report, md=True)


chat = MeetingPlan
