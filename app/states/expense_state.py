import reflex as rx
from reflex_google_auth import GoogleAuthState
from typing import TypedDict, Any
from datetime import datetime, timedelta
from collections import defaultdict
import os
import logging
from sqlalchemy import create_engine, text


class ExpenseReport(TypedDict):
    id: str
    employee: str
    amount: float
    category: str
    date: str
    description: str
    status: str


class DailySpending(TypedDict):
    date: str
    amount: float


class CategoryData(TypedDict):
    name: str
    value: float
    fill: str


class EmployeeSpending(TypedDict):
    name: str
    total: float
    count: int
    avg: float


class ExpenseState(GoogleAuthState):
    expenses: list[ExpenseReport] = []
    start_date: str = "2024-03-01"
    end_date: str = datetime.now().strftime("%Y-%m-%d")

    @rx.event
    def load_expenses(self):
        """Fetch expenses from the database."""
        db_url = os.getenv("REFLEX_DB_URL")
        if not db_url:
            print("Warning: REFLEX_DB_URL environment variable not set.")
            return
        try:
            engine = create_engine(db_url)
            with engine.connect() as conn:
                query = text("""
                    SELECT 
                        e.expense_id,
                        emp.first_name,
                        emp.last_name,
                        e.amount,
                        ec.category_name,
                        e.expense_date,
                        e.description,
                        er.approval_status
                    FROM expenses e
                    JOIN expense_reports er ON e.report_id = er.report_id
                    JOIN employees emp ON er.employee_id = emp.employee_id
                    JOIN expense_categories ec ON e.category_id = ec.category_id
                    ORDER BY e.expense_date DESC
                """)
                result = conn.execute(query)
                self.expenses = [
                    {
                        "id": str(row[0]),
                        "employee": f"{row[1]} {row[2]}",
                        "amount": float(row[3]),
                        "category": row[4],
                        "date": str(row[5]),
                        "description": row[6] or "",
                        "status": row[7],
                    }
                    for row in result
                ]
        except Exception as e:
            logging.exception(f"Error loading expenses: {e}")

    @rx.var
    def filtered_expenses(self) -> list[ExpenseReport]:
        """
        Filters expenses based on the selected date range.
        Date strings in ISO format (YYYY-MM-DD) can be compared directly.
        """
        filtered = []
        for expense in self.expenses:
            if (self.start_date == "" or expense["date"] >= self.start_date) and (
                self.end_date == "" or expense["date"] <= self.end_date
            ):
                filtered.append(expense)
        return filtered

    @rx.var
    def total_filtered_amount(self) -> float:
        """Calculates the total amount of the filtered expenses."""
        return sum((expense["amount"] for expense in self.filtered_expenses))

    @rx.var
    def filtered_count(self) -> int:
        """Returns the number of expenses in the filtered set."""
        return len(self.filtered_expenses)

    @rx.event
    def set_start_date(self, date: str):
        self.start_date = date

    @rx.event
    def set_end_date(self, date: str):
        self.end_date = date

    @rx.var
    def daily_spending(self) -> list[DailySpending]:
        """Aggregates spending by date for the area chart."""
        data = defaultdict(float)
        for expense in self.filtered_expenses:
            data[expense["date"]] += expense["amount"]
        sorted_dates = sorted(data.keys())
        return [{"date": d, "amount": data[d]} for d in sorted_dates]

    @rx.var
    def category_breakdown(self) -> list[CategoryData]:
        """Aggregates spending by category for the pie chart."""
        data = defaultdict(float)
        for expense in self.filtered_expenses:
            data[expense["category"]] += expense["amount"]
        colors = [
            "#4F46E5",
            "#10B981",
            "#F59E0B",
            "#EF4444",
            "#8B5CF6",
            "#EC4899",
            "#3B82F6",
            "#6366F1",
        ]
        result = []
        for i, (cat, amount) in enumerate(data.items()):
            result.append(
                {"name": cat, "value": amount, "fill": colors[i % len(colors)]}
            )
        return sorted(result, key=lambda x: x["value"], reverse=True)

    @rx.var
    def top_employees(self) -> list[EmployeeSpending]:
        """Identifies top spenders for summary cards (first 4)."""
        return self.all_employee_spending[:4]

    sort_column: str = "total"
    sort_reverse: bool = True
    selected_expense: ExpenseReport | None = None
    is_modal_open: bool = False

    @rx.event
    def sort_employees_by(self, column: str):
        """Sorts the employee list by the given column."""
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = True

    @rx.event
    def select_expense(self, expense: ExpenseReport):
        """Selects an expense and opens the modal."""
        self.selected_expense = expense
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        """Closes the modal."""
        self.is_modal_open = False

    @rx.var
    def all_employee_spending(self) -> list[EmployeeSpending]:
        """Aggregates spending for all employees with sorting."""
        data = defaultdict(float)
        counts = defaultdict(int)
        for expense in self.filtered_expenses:
            emp = expense["employee"]
            data[emp] += expense["amount"]
            counts[emp] += 1
        result = []
        for name, total in data.items():
            count = counts[name]
            result.append(
                {
                    "name": name,
                    "total": total,
                    "count": count,
                    "avg": total / count if count > 0 else 0,
                }
            )
        key = self.sort_column
        return sorted(
            result,
            key=lambda x: x.get(key, 0) if key != "name" else x.get(key, ""),
            reverse=self.sort_reverse,
        )