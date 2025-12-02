import reflex as rx
from reflex_google_auth import GoogleAuthState
from typing import TypedDict, Any
from datetime import datetime, timedelta
from collections import defaultdict
import os
import logging
from sqlalchemy import text


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


class EmployeeOption(TypedDict):
    label: str
    value: str


class CategoryOption(TypedDict):
    label: str
    value: str


class ExpenseState(GoogleAuthState):
    expenses: list[ExpenseReport] = []
    start_date: str = "2024-03-01"
    end_date: str = datetime.now().strftime("%Y-%m-%d")

    @rx.event
    async def load_expenses(self):
        """Fetch expenses from the database."""
        async with rx.asession() as session:
            try:
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
                result = await session.execute(query)
                rows = result.all()
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
                    for row in rows
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

    is_create_modal_open: bool = False
    employee_options: list[EmployeeOption] = []
    category_options: list[CategoryOption] = []
    new_expense_employee_id: str = ""
    new_expense_date: str = datetime.now().strftime("%Y-%m-%d")
    new_expense_category_id: str = ""
    new_expense_amount: str = ""
    new_expense_description: str = ""
    new_expense_receipt_url: str = ""

    @rx.event
    def set_new_expense_employee_id(self, value: str):
        self.new_expense_employee_id = value

    @rx.event
    def set_new_expense_date(self, value: str):
        self.new_expense_date = value

    @rx.event
    def set_new_expense_category_id(self, value: str):
        self.new_expense_category_id = value

    @rx.event
    def set_new_expense_amount(self, value: str):
        self.new_expense_amount = value

    @rx.event
    def set_new_expense_description(self, value: str):
        self.new_expense_description = value

    @rx.event
    def set_new_expense_receipt_url(self, value: str):
        self.new_expense_receipt_url = value

    @rx.event
    async def load_form_data(self):
        """Fetch employees and categories for the dropdowns."""
        async with rx.asession() as session:
            try:
                emp_query = text(
                    "SELECT employee_id, first_name, last_name FROM employees ORDER BY last_name"
                )
                emp_result = await session.execute(emp_query)
                self.employee_options = [
                    {"label": f"{row[1]} {row[2]}", "value": str(row[0])}
                    for row in emp_result
                ]
                cat_query = text(
                    "SELECT category_id, category_name FROM expense_categories ORDER BY category_name"
                )
                cat_result = await session.execute(cat_query)
                self.category_options = [
                    {"label": row[1], "value": str(row[0])} for row in cat_result
                ]
            except Exception as e:
                logging.exception(f"Error loading form data: {e}")

    @rx.event
    async def open_create_modal(self):
        """Opens the create modal and loads data."""
        self.is_create_modal_open = True
        self.new_expense_date = datetime.now().strftime("%Y-%m-%d")
        return ExpenseState.load_form_data

    @rx.event
    def close_create_modal(self):
        """Closes the create modal and resets form."""
        self.is_create_modal_open = False
        self.new_expense_employee_id = ""
        self.new_expense_category_id = ""
        self.new_expense_amount = ""
        self.new_expense_description = ""
        self.new_expense_receipt_url = ""

    @rx.event
    async def create_expense(self):
        """Creates a new expense and expense report in the database."""
        if (
            not self.new_expense_employee_id
            or not self.new_expense_category_id
            or (not self.new_expense_amount)
        ):
            return rx.toast.error("Please fill in all required fields.")
        async with rx.asession() as session:
            try:
                report_query = text("""
                    INSERT INTO expense_reports (employee_id, report_month, total_amount, submission_date, approval_status)
                    VALUES (:emp_id, :date, :amount, NOW(), 'Pending')
                    RETURNING report_id
                """)
                result = await session.execute(
                    report_query,
                    {
                        "emp_id": int(self.new_expense_employee_id),
                        "date": self.new_expense_date,
                        "amount": float(self.new_expense_amount),
                    },
                )
                report_id = result.scalar()
                expense_query = text("""
                    INSERT INTO expenses (report_id, expense_date, category_id, amount, description, receipt_url)
                    VALUES (:report_id, :date, :cat_id, :amount, :desc, :url)
                """)
                await session.execute(
                    expense_query,
                    {
                        "report_id": report_id,
                        "date": self.new_expense_date,
                        "cat_id": int(self.new_expense_category_id),
                        "amount": float(self.new_expense_amount),
                        "desc": self.new_expense_description,
                        "url": self.new_expense_receipt_url,
                    },
                )
                await session.commit()
            except Exception as e:
                logging.exception(f"Error creating expense: {e}")
                return rx.toast.error("Failed to create expense.")
        self.close_create_modal()
        return [
            rx.toast.success("Expense created successfully"),
            ExpenseState.load_expenses,
        ]

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