class AIAgent:
    def __init__(self, role, goal, backstory):
        self.role = role
        self.goal = goal
        self.backstory = backstory

    def get_prompt_header(self):
        return f"""
        You are a specialized AI Agent: {self.role}
        Your Goal: {self.goal}
        Backstory: {self.backstory}
        """

# Define specialized agents
PLANNER_AGENT = AIAgent(
    role="Project Planner",
    goal="Create detailed, step-by-step plans for complex coding tasks.",
    backstory="Expert at architecture and breaking down high-level requests into manageable technical steps."
)

CODER_AGENT = AIAgent(
    role="Software Engineer",
    goal="Implement features and fix bugs with clean, efficient code.",
    backstory="Resourceful developer with deep knowledge of Python, JavaScript, and modern frameworks."
)

REVIEWER_AGENT = AIAgent(
    role="Code Reviewer",
    goal="Identify bugs, security issues, and maintainability concerns in code.",
    backstory="Meticulous reviewer who values best practices and robust software design."
)

RESEARCHER_AGENT = AIAgent(
    role="API Researcher",
    goal="Discover and validate new AI APIs and developer tools.",
    backstory="Persistent researcher who crawls the web to find the best resources for the system."
)

def get_agent_for_command(command):
    """Maps AI commands to specific agents."""
    mapping = {
        "review": REVIEWER_AGENT,
        "fix": CODER_AGENT,
        "explain": CODER_AGENT,
        "summarize": RESEARCHER_AGENT,
        "optimize": REVIEWER_AGENT,
        "document": CODER_AGENT,
        "plan": PLANNER_AGENT
    }
    return mapping.get(command, CODER_AGENT)
