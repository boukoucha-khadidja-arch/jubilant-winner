# patterns/approval_chain.py

from abc import ABC, abstractmethod
from enum import Enum

class SubmissionStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class Submission:
    def __init__(self, title: str, researcher: str):
        self.title = title
        self.researcher = researcher
        self.status = SubmissionStatus.PENDING
        self.approved_by = []
        self.rejected_by = None
        self.comments = ""

class Approver(ABC):
    def __init__(self, name: str):
        self.name = name
        self._next_approver = None

    def set_next(self, approver):
        self._next_approver = approver
        return approver

    @abstractmethod
    def approve(self, submission: Submission) -> bool:
        pass

    def _process_next(self, submission: Submission):
        if self._next_approver:
            return self._next_approver.approve(submission)
        return True  # If no next approver, process ends successfully

class Supervisor(Approver):
    def approve(self, submission: Submission) -> bool:
        print(f"Supervisor {self.name} reviewing submission: {submission.title}")
        # Simulate approval logic
        if "urgent" in submission.title.lower():
            submission.status = SubmissionStatus.REJECTED
            submission.rejected_by = self.name
            submission.comments = "Urgent submissions must go directly to Department Head."
            print(f"  -> REJECTED by {self.name}: {submission.comments}")
            return False
        else:
            submission.status = SubmissionStatus.APPROVED
            submission.approved_by.append(self.name)
            print(f"  -> APPROVED by {self.name}")
            return self._process_next(submission)

class DepartmentHead(Approver):
    def approve(self, submission: Submission) -> bool:
        print(f"Department Head {self.name} reviewing submission: {submission.title}")
        if "experimental" in submission.title.lower():
            submission.status = SubmissionStatus.REJECTED
            submission.rejected_by = self.name
            submission.comments = "Experimental projects require additional funding review."
            print(f"  -> REJECTED by {self.name}: {submission.comments}")
            return False
        else:
            submission.status = SubmissionStatus.APPROVED
            submission.approved_by.append(self.name)
            print(f"  -> APPROVED by {self.name}")
            return self._process_next(submission)

class Dean(Approver):
    def approve(self, submission: Submission) -> bool:
        print(f"Dean {self.name} reviewing submission: {submission.title}")
        if len(submission.approved_by) < 2:
            submission.status = SubmissionStatus.REJECTED
            submission.rejected_by = self.name
            submission.comments = "Submission must be approved by both Supervisor and Department Head first."
            print(f"  -> REJECTED by {self.name}: {submission.comments}")
            return False
        else:
            submission.status = SubmissionStatus.APPROVED
            submission.approved_by.append(self.name)
            print(f"  -> FINAL APPROVAL by {self.name}")
            return True

# Example usage
if __name__ == "__main__":
    # Create approvers
    supervisor = Supervisor("Dr. Alice")
    dept_head = DepartmentHead("Prof. Bob")
    dean = Dean("Dr. Carol")

    # Set up the chain: Supervisor -> Department Head -> Dean
    supervisor.set_next(dept_head).set_next(dean)

    # Create a submission
    submission = Submission("AI Research Proposal", "John Doe")

    # Start the approval chain
    print("\n=== Starting Approval Chain ===\n")
    result = supervisor.approve(submission)

    print("\n=== Final Submission Status ===")
    print(f"Title: {submission.title}")
    print(f"Status: {submission.status.value}")
    print(f"Approved by: {', '.join(submission.approved_by) if submission.approved_by else 'None'}")
    if submission.rejected_by:
        print(f"Rejected by: {submission.rejected_by}")
        print(f"Comments: {submission.comments}")