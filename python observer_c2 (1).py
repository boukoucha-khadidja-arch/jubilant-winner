# =========================================
# C2 - Observer Pattern for Notifications
# =========================================


# -------- Observer Interface --------
class Observer:
    def update(self, message):
        raise NotImplementedError


# -------- Concrete Observers --------
class EmailObserver(Observer):
    def update(self, message):
        print(f"[EMAIL] {message}")


class DashboardObserver(Observer):
    def update(self, message):
        print(f"[DASHBOARD] {message}")


# -------- Subject --------
class NotificationSubject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, message):
        for obs in self.observers:
            obs.update(message)


# -------- Project (uses Subject) --------
class Project(NotificationSubject):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.submissions = []

        # notify when project is created
        self.notify(f"Project '{self.title}' created")

    def add_submission(self, submission):
        self.submissions.append(submission)
        self.notify(f"Submission '{submission.title}' added to project '{self.title}'")

    def approve_submission(self, submission):
        submission.status = "approved"
        self.notify(f"Submission '{submission.title}' approved")

    def reject_submission(self, submission):
        submission.status = "rejected"
        self.notify(f"Submission '{submission.title}' rejected")


# -------- Submission --------
class Submission:
    def __init__(self, title):
        self.title = title
        self.status = "pending"


# -------- Test --------
if __name__ == "__main__":

    # Create observers
    email = EmailObserver()
    dashboard = DashboardObserver()

    # Create project (Subject)
    project = Project("SURMS")

    # Attach observers
    project.attach(email)
    project.attach(dashboard)

    # Add submission
    s1 = Submission("Paper 1")
    project.add_submission(s1)

    # Approve submission
    project.approve_submission(s1)

    # Reject another submission
    s2 = Submission("Dataset 1")
    project.add_submission(s2)
    project.reject_submission(s2)

