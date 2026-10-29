"""
5022CMD Advanced Algorithms - Question 2 (UPGRADED)
Unweighted Directed Graph + Course-Prerequisite System
"""

# ============================================================
# GENERIC GRAPH (no domain-specific code)
# ============================================================
class Graph:
    """
    Unweighted directed graph using adjacency lists.
    Vertices are generic (any hashable type).
    """
    def __init__(self):
        self.adjacency = {}  # vertex -> list of outgoing neighbours

    def addVertex(self, vertex):
        """Add a new vertex to the graph."""
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []

    def addEdge(self, from_vertex, to_vertex):
        """Add a directed edge from_vertex -> to_vertex."""
        self.addVertex(from_vertex)
        self.addVertex(to_vertex)
        if to_vertex not in self.adjacency[from_vertex]:
            self.adjacency[from_vertex].append(to_vertex)

    def removeEdge(self, from_vertex, to_vertex):
        """Remove a directed edge from_vertex -> to_vertex."""
        if from_vertex in self.adjacency and to_vertex in self.adjacency[from_vertex]:
            self.adjacency[from_vertex].remove(to_vertex)
            return True
        return False

    def listIncomingAdjacentVertex(self, vertex):
        """List all vertices with an edge incoming to the given vertex."""
        incoming = []
        for v, neighbours in self.adjacency.items():
            if vertex in neighbours:
                incoming.append(v)
        return incoming

    def listOutgoingAdjacentVertex(self, vertex):
        """List all vertices that the given vertex points to."""
        return self.adjacency.get(vertex, [])

    def getVertices(self):
        """Return all vertices in the graph."""
        return list(self.adjacency.keys())

    def hasVertex(self, vertex):
        """Check if a vertex exists."""
        return vertex in self.adjacency

    def display(self):
        """Display adjacency list for debugging."""
        print("\n--- Graph Adjacency List ---")
        for v, neighbours in self.adjacency.items():
            print(f"  {v: <6} -> {neighbours}")


# ============================================================
# COURSE ENTITY
# ============================================================
class Course:
    """
    Entity class representing a university course.
    """
    def __init__(self, course_code, course_name, credit_hours, level):
        self.course_code = course_code
        self.course_name = course_name
        self.credit_hours = credit_hours
        self.level = level

    def __str__(self):
        return (f"{self.course_code} - {self.course_name} "
                f"({self.credit_hours} credits, {self.level})")

    def __repr__(self):
        return self.__str__()


# ============================================================
# VALIDATION HELPERS
# ============================================================
def get_nonempty_string(prompt):
    """Prompt until a non-empty string is entered."""
    while True:
        value = input(prompt).strip().upper()  # Course codes are usually uppercase
        if value:
            return value
        print("  ⚠ Input cannot be empty. Try again.")


def get_int(prompt, min_value=None):
    """Prompt until a valid integer is entered."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"  ⚠ Value must be at least {min_value}. Try again.")
                continue
            return value
        except ValueError:
            print("  ⚠ Invalid input. Please enter a whole number.")


def confirm(prompt):
    """Ask for yes/no confirmation."""
    while True:
        ans = input(prompt + " (y/n): ").strip().lower()
        if ans in ('y', 'yes'):
            return True
        if ans in ('n', 'no'):
            return False
        print("  ⚠ Please enter 'y' or 'n'.")


# ============================================================
# SYSTEM
# ============================================================
class CourseSystem:
    def __init__(self):
        self.courses = []
        self.graph = Graph()

    def find_course(self, course_code):
        for c in self.courses:
            if c.course_code == course_code:
                return c
        return None

    def add_course(self, course):
        self.courses.append(course)
        self.graph.addVertex(course.course_code)

    def add_prerequisite(self, prereq_code, course_code):
        self.graph.addEdge(prereq_code, course_code)

    def remove_prerequisite(self, prereq_code, course_code):
        return self.graph.removeEdge(prereq_code, course_code)

    def view_all_courses(self):
        print("\n--- AVAILABLE COURSES ---")
        for i, c in enumerate(self.courses, 1):
            print(f"  {i}. {c.course_code:<6} - {c.course_name}")

    def view_course_details(self, code):
        course = self.find_course(code)
        if not course:
            print(f"  ✗ Course '{code}' not found.")
            return

        # Advanced feature: elective visibility
        if course.level.lower() == "elective":
            print(f"\n  Course Name: {course.course_name}")
            print("  (Details hidden - this is an Elective course)")
        else:
            print(f"\n--- COURSE DETAILS ---")
            print(f"  Code:     {course.course_code}")
            print(f"  Name:     {course.course_name}")
            print(f"  Credits:  {course.credit_hours}")
            print(f"  Level:    {course.level}")

    def view_prerequisites(self, code):
        course = self.find_course(code)
        if not course:
            print(f"  ✗ Course '{code}' not found.")
            return
        prereqs = self.graph.listIncomingAdjacentVertex(code)
        print(f"\n--- PREREQUISITES FOR {code} ---")
        if not prereqs:
            print("  None")
        for p in prereqs:
            pc = self.find_course(p)
            print(f"  - {p} ({pc.course_name})")

    def view_unlocked(self, code):
        course = self.find_course(code)
        if not course:
            print(f"  ✗ Course '{code}' not found.")
            return
        unlocked = self.graph.listOutgoingAdjacentVertex(code)
        print(f"\n--- COURSES UNLOCKED BY {code} ---")
        if not unlocked:
            print("  None")
        for u in unlocked:
            uc = self.find_course(u)
            print(f"  - {u} ({uc.course_name})")


# ============================================================
# MENU
# ============================================================
def main():
    system = CourseSystem()

    # Create 7 courses
    system.add_course(Course("CS101", "Introduction to Programming", 3, "Core"))
    system.add_course(Course("CS201", "Data Structures", 3, "Core"))
    system.add_course(Course("CS301", "Algorithms", 3, "Core"))
    system.add_course(Course("CS302", "Database Systems", 3, "Core"))
    system.add_course(Course("CS401", "Software Engineering", 3, "Core"))
    system.add_course(Course("CS402", "Artificial Intelligence", 3, "Elective"))
    system.add_course(Course("CS403", "Machine Learning", 3, "Elective"))

    # Define prerequisites
    system.add_prerequisite("CS101", "CS201")
    system.add_prerequisite("CS201", "CS301")
    system.add_prerequisite("CS201", "CS302")
    system.add_prerequisite("CS301", "CS401")
    system.add_prerequisite("CS302", "CS401")
    system.add_prerequisite("CS301", "CS402")
    system.add_prerequisite("CS402", "CS403")

    print("=" * 60)
    print("  WELCOME TO COURSE PREREQUISITE SYSTEM")
    print("  (Generic Directed Graph Implementation)")
    print("=" * 60)
    print(f"  {len(system.courses)} pre-defined courses loaded.")
    print("=" * 60)

    while True:
        print("\n┌──────────────────────────────────────────┐")
        print("│                MAIN MENU                 │")
        print("├──────────────────────────────────────────┤")
        print("│  1. View All Courses                     │")
        print("│  2. View Course Details                  │")
        print("│  3. View Prerequisites of a Course       │")
        print("│  4. View Courses Unlocked by a Course    │")
        print("│  5. Add a Course                         │")
        print("│  6. Add a Prerequisite                   │")
        print("│  7. Remove a Prerequisite                │")
        print("│  8. Display Graph Adjacency List         │")
        print("│  9. Exit                                 │")
        print("└──────────────────────────────────────────┘")

        choice = input("Enter choice (1-9): ").strip()

        if choice == '1':
            system.view_all_courses()

        elif choice == '2':
            code = get_nonempty_string("Enter Course Code: ")
            system.view_course_details(code)

        elif choice == '3':
            code = get_nonempty_string("Enter Course Code: ")
            system.view_prerequisites(code)

        elif choice == '4':
            code = get_nonempty_string("Enter Course Code: ")
            system.view_unlocked(code)

        elif choice == '5':
            print("\n--- ADD NEW COURSE ---")
            code = get_nonempty_string("Enter new course code: ")
            if system.find_course(code):
                print(f"  ⚠ Course {code} already exists!")
                continue
            name = input("Enter course name: ").strip()
            credits = get_int("Enter credit hours: ", min_value=1)
            level = input("Enter level (Core/Elective): ").strip().capitalize()
            if level not in ["Core", "Elective"]:
                print("  ⚠ Invalid level. Defaulting to 'Elective'.")
                level = "Elective"

            system.add_course(Course(code, name, credits, level))
            print(f"\n  ✓ Course {code} added successfully.")

        elif choice == '6':
            print("\n--- ADD PREREQUISITE ---")
            prereq = get_nonempty_string("Enter prerequisite course code: ")
            course = get_nonempty_string("Enter target course code: ")
            if not system.find_course(prereq) or not system.find_course(course):
                print("  ✗ One or both course codes do not exist.")
                continue

            system.add_prerequisite(prereq, course)
            print(f"\n  ✓ Prerequisite {prereq} added for {course}.")

        elif choice == '7':
            print("\n--- REMOVE PREREQUISITE ---")
            prereq = get_nonempty_string("Enter prerequisite course code: ")
            course = get_nonempty_string("Enter target course code: ")

            if system.remove_prerequisite(prereq, course):
                print(f"\n  ✓ Prerequisite {prereq} removed from {course}.")
            else:
                print(f"  ✗ Edge from {prereq} to {course} not found.")

        elif choice == '8':
            system.graph.display()

        elif choice == '9':
            print("\nThank you for using the Course System. Goodbye!")
            break
        else:
            print("  ⚠ Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()