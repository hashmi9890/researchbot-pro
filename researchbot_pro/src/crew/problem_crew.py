"""
Problem Solving Crew — Clarifier + Solver + Risk Analyst
"""

from crewai import Crew, Task, Process
from src.agents.problem_solver_agent import (
    create_clarifier,
    create_problem_solver,
    create_risk_analyst,
)


class ProblemSolvingCrew:

    def __init__(self, problem_data: dict) -> None:
        self.problem_data = problem_data
        self.clarifier = create_clarifier()
        self.solver = create_problem_solver()
        self.risk_analyst = create_risk_analyst()
        self._tasks = self._build_tasks()
        self._crew = Crew(
            agents=[self.clarifier, self.solver, self.risk_analyst],
            tasks=self._tasks,
            process=Process.sequential,
            verbose=True,
        )

    def _build_tasks(self) -> list:
        p = self.problem_data

        clarify_task = Task(
            description=(
                f"Clarify and structure this business problem:\n\n"
                f"Problem: {p.get('problem', 'N/A')}\n"
                f"Industry: {p.get('industry', 'N/A')}\n"
                f"Goal: {p.get('goal', 'N/A')}\n"
                f"Constraints: {p.get('constraints', 'N/A')}\n"
                f"Budget: {p.get('budget', 'N/A')}\n"
                f"Timeline: {p.get('timeline', 'N/A')}\n\n"
                "DELIVERABLES:\n"
                "1. Restated problem (clear, specific)\n"
                "2. Root problem vs symptoms\n"
                "3. Key stakeholders affected\n"
                "4. Success criteria\n"
                "5. Scope boundaries"
            ),
            expected_output="Structured problem definition with clear scope",
            agent=self.clarifier,
        )

        solve_task = Task(
            description=(
                "Based on the clarified problem, provide:\n\n"
                "1. Root Cause Analysis (5-Why method)\n"
                "2. Key Blockers & Dependencies\n"
                "3. Solution Option A (Low cost)\n"
                "4. Solution Option B (Medium cost)\n"
                "5. Solution Option C (High investment)\n"
                "6. Recommended Solution with justification\n"
                "7. 30-Day Action Plan\n"
                "8. 60-Day Milestones\n"
                "9. 90-Day Target State\n"
                "10. KPIs to track success"
            ),
            expected_output="Complete problem solving report with 30/60/90 plan",
            agent=self.solver,
            context=[clarify_task],
        )

        risk_task = Task(
            description=(
                "Analyze the recommended solution and provide:\n\n"
                "1. Top 5 Risks (probability + impact)\n"
                "2. Risk Mitigation Strategies\n"
                "3. Best Case Scenario\n"
                "4. Base Case Scenario\n"
                "5. Worst Case Scenario\n"
                "6. Contingency Plans\n"
                "7. SWOT Analysis"
            ),
            expected_output="Risk and scenario analysis with SWOT",
            agent=self.risk_analyst,
            context=[clarify_task, solve_task],
        )

        return [clarify_task, solve_task, risk_task]

    def run(self) -> str:
        result = self._crew.kickoff(inputs=self.problem_data)
        return str(result)
