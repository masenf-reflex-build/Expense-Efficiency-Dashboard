import reflex as rx
from app.states.expense_state import ExpenseState, EmployeeSpending, ExpenseReport


def sort_icon(column: str) -> rx.Component:
    return rx.cond(
        ExpenseState.sort_column == column,
        rx.cond(
            ExpenseState.sort_reverse,
            rx.icon("chevron-down", class_name="h-4 w-4 ml-1 inline"),
            rx.icon("chevron-up", class_name="h-4 w-4 ml-1 inline"),
        ),
        rx.icon("chevrons-up-down", class_name="h-4 w-4 ml-1 inline text-gray-300"),
    )


def th_sortable(label: str, column_key: str) -> rx.Component:
    return rx.el.th(
        rx.el.button(
            rx.el.span(label),
            sort_icon(column_key),
            on_click=lambda: ExpenseState.sort_employees_by(column_key),
            class_name="flex items-center font-semibold hover:text-indigo-600 transition-colors",
        ),
        class_name="px-6 py-3 text-left text-xs text-gray-500 uppercase tracking-wider cursor-pointer",
    )


def employee_row(employee: EmployeeSpending) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.icon("user", class_name="h-5 w-5 text-gray-500"),
                    class_name="h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center mr-3",
                ),
                rx.el.span(employee["name"], class_name="font-medium text-gray-900"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            f"${employee['total']:.2f}",
            class_name="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900",
        ),
        rx.el.td(
            employee["count"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            f"${employee['avg']:.2f}",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
    )


def employee_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Employee Spending Overview",
                class_name="text-lg font-semibold text-gray-900 mb-4",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            th_sortable("Employee", "tag"),
                            th_sortable("Total Spent", "percent"),
                            th_sortable("Reports", "clock"),
                            th_sortable("Avg / Report", "clock_alert"),
                            class_name="bg-gray-50",
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(ExpenseState.all_employee_spending, employee_row),
                        class_name="bg-white divide-y divide-gray-100",
                    ),
                    class_name="min-w-full",
                ),
                class_name="overflow-x-auto rounded-lg border border-gray-200",
            ),
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full",
    )


def status_badge_small(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Approved",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
            ),
            (
                "Pending",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
            ),
            (
                "Rejected",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
            ),
            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
        ),
    )


def expense_row(expense: ExpenseReport) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            expense["date"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            expense["employee"],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            expense["category"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            f"${expense['amount']}",
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            status_badge_small(expense["status"]),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                "View",
                class_name="text-indigo-600 hover:text-indigo-900 text-sm font-medium",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
        on_click=lambda: ExpenseState.select_expense(expense),
        class_name="cursor-pointer hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
    )


def expense_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Detailed Expense Reports",
                class_name="text-lg font-semibold text-gray-900 mb-4",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Date",
                                class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Employee",
                                class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Category",
                                class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Amount",
                                class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "",
                                class_name="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            class_name="bg-gray-50",
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(ExpenseState.filtered_expenses, expense_row),
                        class_name="bg-white divide-y divide-gray-100",
                    ),
                    class_name="min-w-full",
                ),
                class_name="overflow-x-auto rounded-lg border border-gray-200 max-h-[500px]",
            ),
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full",
    )