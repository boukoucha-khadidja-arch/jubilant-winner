# patterns/access_proxy.py

from abc import ABC, abstractmethod
from enum import Enum
from typing import List

class UserRole(Enum):
    RESEARCHER = "Researcher"
    SUPERVISOR = "Supervisor"
    ADMIN = "Administrator"
    DEPARTMENT_HEAD = "Department Head"

class User:
    def __init__(self, user_id: str, name: str, role: UserRole):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.permissions = self._get_default_permissions(role)
    
    def _get_default_permissions(self, role: UserRole) -> List[str]:
        """Define permissions based on user role"""
        permissions_map = {
            UserRole.RESEARCHER: ["view_submissions", "create_submission"],
            UserRole.SUPERVISOR: ["view_submissions", "create_submission", "evaluate_submission"],
            UserRole.DEPARTMENT_HEAD: ["view_submissions", "create_submission", "evaluate_submission", "modify_budget"],
            UserRole.ADMIN: ["view_submissions", "create_submission", "delete_submission", "modify_budget"]
        }
        return permissions_map.get(role, [])

class Project:
    def __init__(self, project_id: str, title: str, budget: float):
        self.project_id = project_id
        self.title = title
        self._budget = budget
        self.submissions = []
    
    def get_budget(self) -> float:
        return self._budget
    
    def set_budget(self, new_budget: float):
        self._budget = new_budget
        print(f"Project budget updated to: ${new_budget:.2f}")
    
    def add_submission(self, submission):
        self.submissions.append(submission)
    
    def delete_submission(self, submission_id: str):
        for i, sub in enumerate(self.submissions):
            if sub.submission_id == submission_id:
                del self.submissions[i]
                print(f"Submission {submission_id} deleted")
                return True
        print(f"Submission {submission_id} not found")
        return False

class Submission:
    def __init__(self, submission_id: str, title: str, author: User):
        self.submission_id = submission_id
        self.title = title
        self.author = author
        self.status = "Pending"

# Abstract interface for Project operations
class IProjectService(ABC):
    @abstractmethod
    def get_budget(self) -> float:
        pass
    
    @abstractmethod
    def set_budget(self, user: User, new_budget: float) -> bool:
        pass
    
    @abstractmethod
    def delete_submission(self, user: User, submission_id: str) -> bool:
        pass
    
    @abstractmethod
    def add_submission(self, submission: Submission) -> bool:
        pass

# Real Subject - The actual project service
class RealProjectService(IProjectService):
    def __init__(self, project: Project):
        self._project = project
    
    def get_budget(self) -> float:
        return self._project.get_budget()
    
    def set_budget(self, user: User, new_budget: float) -> bool:
        self._project.set_budget(new_budget)
        return True
    
    def delete_submission(self, user: User, submission_id: str) -> bool:
        return self._project.delete_submission(submission_id)
    
    def add_submission(self, submission: Submission) -> bool:
        self._project.add_submission(submission)
        print(f"Submission '{submission.title}' added to project")
        return True

# Proxy - Access Control Proxy
class AccessControlProxy(IProjectService):
    def __init__(self, real_service: RealProjectService):
        self._real_service = real_service
        self._access_log = []
    
    def _log_access(self, user: User, action: str, success: bool):
        """Log all access attempts"""
        log_entry = {
            "user": user.name,
            "role": user.role.value,
            "action": action,
            "success": success,
            "timestamp": "2024-01-26 10:00:00"  # In real app, use datetime.now()
        }
        self._access_log.append(log_entry)
        print(f"LOG: {user.name} ({user.role.value}) attempted {action}: {'SUCCESS' if success else 'DENIED'}")
    
    def _check_permission(self, user: User, permission: str) -> bool:
        """Check if user has specific permission"""
        has_permission = permission in user.permissions
        if not has_permission:
            print(f"ACCESS DENIED: {user.name} lacks '{permission}' permission")
        return has_permission
    
    def get_budget(self) -> float:
        """No access control needed for viewing"""
        return self._real_service.get_budget()
    
    def set_budget(self, user: User, new_budget: float) -> bool:
        """Check permission before modifying budget"""
        if not self._check_permission(user, "modify_budget"):
            self._log_access(user, "modify_budget", False)
            return False
        
        # Additional business logic: Budget cannot be negative
        if new_budget < 0:
            print("ERROR: Budget cannot be negative")
            self._log_access(user, "modify_budget", False)
            return False
        
        success = self._real_service.set_budget(user, new_budget)
        self._log_access(user, "modify_budget", success)
        return success
    
    def delete_submission(self, user: User, submission_id: str) -> bool:
        """Check permission before deleting submission"""
        if not self._check_permission(user, "delete_submission"):
            self._log_access(user, "delete_submission", False)
            return False
        
        # Additional business logic: User cannot delete others' submissions
        project = self._real_service._project
        for submission in project.submissions:
            if submission.submission_id == submission_id:
                if submission.author.user_id != user.user_id and user.role != UserRole.ADMIN:
                    print(f"ERROR: {user.name} cannot delete others' submissions")
                    self._log_access(user, "delete_submission", False)
                    return False
                break
        
        success = self._real_service.delete_submission(user, submission_id)
        self._log_access(user, "delete_submission", success)
        return success
    
    def add_submission(self, submission: Submission) -> bool:
        """Check permission before adding submission"""
        if not self._check_permission(submission.author, "create_submission"):
            self._log_access(submission.author, "create_submission", False)
            return False
        
        success = self._real_service.add_submission(submission)
        self._log_access(submission.author, "create_submission", success)
        return success
    
    def get_access_log(self):
        """Return access log for auditing"""
        return self._access_log

# Example Usage
if __name__ == "__main__":
    print("=== SURMS Access Control Proxy Demo ===\n")
    
    # Create users with different roles
    researcher = User("R001", "Alice Smith", UserRole.RESEARCHER)
    supervisor = User("S001", "Bob Johnson", UserRole.SUPERVISOR)
    admin = User("A001", "Carol Williams", UserRole.ADMIN)
    dept_head = User("D001", "David Brown", UserRole.DEPARTMENT_HEAD)
    
    # Create a project
    project = Project("P001", "AI Research Project", 50000.00)
    
    # Create real service and proxy
    real_service = RealProjectService(project)
    proxy_service = AccessControlProxy(real_service)
    
    # Test 1: Researcher tries to modify budget (Should fail)
    print("\n1. Researcher attempting to modify budget:")
    proxy_service.set_budget(researcher, 60000.00)
    
    # Test 2: Admin modifies budget (Should succeed)
    print("\n2. Admin modifying budget:")
    proxy_service.set_budget(admin, 60000.00)
    
    # Test 3: Add submissions
    print("\n3. Adding submissions:")
    submission1 = Submission("S001", "Research Paper", researcher)
    submission2 = Submission("S002", "Dataset Analysis", supervisor)
    proxy_service.add_submission(submission1)
    proxy_service.add_submission(submission2)
    
    # Test 4: Researcher tries to delete supervisor's submission (Should fail)
    print("\n4. Researcher trying to delete supervisor's submission:")
    proxy_service.delete_submission(researcher, "S002")
    
    # Test 5: Admin deletes submission (Should succeed)
    print("\n5. Admin deleting submission:")
    proxy_service.delete_submission(admin, "S001")
    
    # Test 6: Department Head modifies budget (Should succeed)
    print("\n6. Department Head modifying budget:")
    proxy_service.set_budget(dept_head, 55000.00)
    
    # Test 7: Try negative budget (Should fail even with permission)
    print("\n7. Admin trying to set negative budget:")
    proxy_service.set_budget(admin, -1000.00)
    
    # Display access log
    print("\n=== Access Log ===")
    for entry in proxy_service.get_access_log():
        print(f"{entry['timestamp']} - {entry['user']} ({entry['role']}): {entry['action']} - {entry['success']}")
    
    print("\n=== Current Project State ===")
    print(f"Project: {project.title}")
    print(f"Budget: ${project.get_budget():.2f}")
    print(f"Submissions: {len(project.submissions)}")