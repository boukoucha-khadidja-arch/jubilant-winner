# =====================================================
# SURMS - Section B2 OOP Implementation (Full Example)
# =====================================================


# ---------------- Submission (for Composition) ----------------
class Submission:
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return self.title


# ---------------- Professor (for Association) ----------------
class Professor:
    def __init__(self, name):
        self.name = name

    def supervise(self, researcher):
        print(f"Professor {self.name} supervises {researcher.name}")


# ---------------- Researcher ----------------
class Researcher:
    # Static counter (class variable)
    counter = 0

    def __init__(self, name):
        self.name = name
        self.supervisor = None   # Association

        Researcher.counter += 1

    def set_supervisor(self, professor):
        self.supervisor = professor
        professor.supervise(self)


# ---------------- Department (Aggregation) ----------------
class Department:
    def __init__(self, name):
        self.name = name
        self.researchers = []   # Aggregation

    def add_researcher(self, researcher):
        self.researchers.append(researcher)

    def list_researchers(self):
        for r in self.researchers:
            print("-", r.name)


# ---------------- Project (Private + Protected + Composition) ----------------
class Project:
    def __init__(self, title, budget):
        self.title = title
        self.__budget = budget        # Private attribute
        self._status = "created"     # Protected attribute

        # Composition: Project owns submissions
        self.submissions = []

    def add_submission(self, submission):
        self.submissions.append(submission)

    # Getter for private budget
    def get_budget(self):
        return self.__budget

    def set_status(self, status):
        self._status = status

    def show_info(self):
        print("\nProject:", self.title)
        print("Budget:", self.__budget)
        print("Status:", self._status)
        print("Submissions:")
        for s in self.submissions:
            print("  *", s)


# ---------------- MAIN TEST ----------------
if __name__ == "__main__":

    print("=== SURMS B2 OOP DEMO ===\n")

    # Professor
    prof = Professor("Dr Ahmed")

    # Researchers (Static Counter)
    r1 = Researcher("Aziza")
    r2 = Researcher("Sara")

    print("Number of Researchers:", Researcher.counter)

    # Association
    r1.set_supervisor(prof)

    # Aggregation
    dept = Department("Computer Science")
    dept.add_researcher(r1)
    dept.add_researcher(r2)

    print("\nDepartment Researchers:")
    dept.list_researchers()

    # Project
    project = Project("SURMS", 5000)

    # Composition
    s1 = Submission("Paper Submission")
    s2 = Submission("Dataset Submission")

    project.add_submission(s1)
    project.add_submission(s2)

    project.set_status("running")

    # Display project info
    project.show_info()

    print("\nAccessing private budget via getter:", project.get_budget())

    print("\n=== END ===")
