import reflex as rx
from reflex_google_auth import google_oauth_provider
from app.states.expense_state import ExpenseState, EmployeeSpending
from app.components.charts import cash_flow_chart, category_pie_chart
from app.components.tables import employee_table, expense_table
from app.components.modal import expense_detail_modal, create_expense_modal
from app.components.landing import landing_page


def user_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src=ExpenseState.tokeninfo["picture"],
                class_name="h-10 w-10 rounded-full border border-gray-200 shadow-sm",
                alt="User profile",
            ),
            rx.el.div(
                rx.el.p(
                    ExpenseState.tokeninfo["name"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    ExpenseState.tokeninfo["email"],
                    class_name="text-xs text-gray-500 font-medium",
                ),
                class_name="ml-3",
            ),
            class_name="flex items-center",
        ),
        rx.el.button(
            rx.el.span("Sign out", class_name="mr-2"),
            rx.icon("log-out", class_name="h-4 w-4"),
            on_click=ExpenseState.logout,
            class_name="flex items-center text-sm font-medium text-gray-600 hover:text-red-600 hover:bg-red-50 px-4 py-2 rounded-lg transition-all duration-200",
        ),
        class_name="flex items-center justify-between w-full bg-white p-4 rounded-xl border border-gray-100 shadow-sm mb-6",
    )


def stats_card(
    title: str, value: str, subtext: str, icon_name: str, color_class: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon_name, class_name=f"h-6 w-6 {color_class}"),
                class_name=f"p-3 rounded-lg bg-opacity-10 {color_class.replace('text-', 'bg-')}",
            ),
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
                rx.el.p(value, class_name="text-2xl font-semibold text-gray-900"),
                class_name="ml-4",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.span(subtext, class_name="text-sm text-gray-500"),
            class_name="mt-3 border-t border-gray-100 pt-3",
        ),
        class_name="bg-white rounded-xl p-6 shadow-sm border border-gray-100",
    )


def employee_summary_card(employee: EmployeeSpending) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("user", class_name="h-5 w-5 text-gray-600"),
                    class_name="h-10 w-10 rounded-full bg-gray-100 flex items-center justify-center",
                ),
                rx.el.div(
                    rx.el.p(
                        employee["name"], class_name="text-sm font-medium text-gray-900"
                    ),
                    rx.el.p(
                        f"{employee['count']} reports",
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            rx.el.p(
                f"${employee['total']}",
                class_name="text-sm font-semibold text-indigo-600",
            ),
            class_name="flex items-center justify-between",
        ),
        class_name="bg-white p-4 rounded-lg border border-gray-100 hover:border-indigo-100 transition-colors",
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        user_header(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Expense Dashboard", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Overview of company spending and efficiency metrics",
                    class_name="text-sm text-gray-500 mt-1",
                ),
                class_name="mb-4 sm:mb-0",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "calendar",
                            class_name="h-4 w-4 text-gray-500 absolute left-3 top-1/2 transform -translate-y-1/2",
                        ),
                        rx.el.input(
                            type="date",
                            on_change=ExpenseState.set_start_date,
                            default_value=ExpenseState.start_date,
                            class_name="pl-9 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none",
                        ),
                        class_name="relative",
                    ),
                    rx.el.span("to", class_name="text-sm text-gray-500"),
                    rx.el.div(
                        rx.icon(
                            "calendar",
                            class_name="h-4 w-4 text-gray-500 absolute left-3 top-1/2 transform -translate-y-1/2",
                        ),
                        rx.el.input(
                            type="date",
                            on_change=ExpenseState.set_end_date,
                            default_value=ExpenseState.end_date,
                            class_name="pl-9 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none",
                        ),
                        class_name="relative",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="h-4 w-4 mr-2"),
                    "Create New Expense",
                    on_click=ExpenseState.open_create_modal,
                    class_name="ml-4 flex items-center px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition-colors shadow-sm",
                ),
                class_name="flex items-center",
            ),
            class_name="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8",
        ),
        rx.el.div(
            stats_card(
                "Total Spending",
                f"${ExpenseState.total_filtered_amount}",
                "In selected period",
                "dollar-sign",
                "text-indigo-600",
            ),
            stats_card(
                "Total Reports",
                ExpenseState.filtered_count.to_string(),
                "Processed reports",
                "file-text",
                "text-emerald-600",
            ),
            stats_card(
                "Average Report",
                f"${(ExpenseState.total_filtered_amount / rx.cond(ExpenseState.filtered_count > 0, ExpenseState.filtered_count, 1)).to_string()[:5]}",
                "Per expense report",
                "bar-chart-2",
                "text-amber-600",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(cash_flow_chart(), class_name="col-span-1 lg:col-span-2"),
            rx.el.div(category_pie_chart(), class_name="col-span-1"),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Top Spenders Overview",
                    class_name="text-lg font-semibold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.foreach(ExpenseState.top_employees, employee_summary_card),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4",
                ),
                class_name="mb-8",
            )
        ),
        rx.el.div(
            rx.el.div(employee_table(), class_name="col-span-1 lg:col-span-1"),
            rx.el.div(expense_table(), class_name="col-span-1 lg:col-span-2"),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8",
        ),
        expense_detail_modal(),
        create_expense_modal(),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
    )


def index() -> rx.Component:
    return rx.el.div(
        google_oauth_provider(
            rx.cond(ExpenseState.token_is_valid, dashboard_content(), landing_page())
        ),
        class_name="min-h-screen bg-gray-50 font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=ExpenseState.load_expenses)