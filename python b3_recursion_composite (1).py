# =================================================
# B3 - Recursive Submission Counter using Composite
# =================================================


# -------- Component --------
class ResearchComponent:
    def count_submissions(self):
        raise NotImplementedError


# -------- Submission --------
class Submission:
    def __init__(self, title):
        self.title = title


# -------- Leaf --------
class Researcher(ResearchComponent):
    def __init__(self, name):
        self.name = name
        self.submissions = []

    def add_submission(self, submission):
        self.submissions.append(submission)

    # Base case
    def count_submissions(self):
        return len(self.submissions)


# -------- Composite --------
class ResearchGroup(ResearchComponent):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def get_children(self):
        return self.children

    # Recursive step
    def count_submissions(self):
        total = 0
        for child in self.children:
            total += child.count_submissions()
        return total


# -------- Main Test --------
if __name__ == "__main__":

    # Researchers
    r1 = Researcher("Aziza")
    r2 = Researcher("Sara")

    r1.add_submission(Submission("Paper 1"))
    r1.add_submission(Submission("Paper 2"))
    r2.add_submission(Submission("Dataset 1"))

    # Groups
    group1 = ResearchGroup("AI Group")
    group2 = ResearchGroup("Data Group")

    group1.add(r1)
    group2.add(r2)

    # Department (top composite)
    department = ResearchGroup("Computer Science Department")
    department.add(group1)
    department.add(group2)

    # Recursive counting
    print("Total submissions:", department.count_submissions())
