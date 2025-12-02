import reflex as rx
from app.states.expense_state import ExpenseState


def detail_row(label: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
        rx.el.p(value, class_name="text-base text-gray-900 font-medium"),
        class_name="py-3 border-b border-gray-100 last:border-0",
    )


def status_badge_large(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Approved",
                "px-3 py-1 rounded-full bg-emerald-100 text-emerald-700 text-sm font-semibold border border-emerald-200",
            ),
            (
                "Pending",
                "px-3 py-1 rounded-full bg-amber-100 text-amber-700 text-sm font-semibold border border-amber-200",
            ),
            (
                "Rejected",
                "px-3 py-1 rounded-full bg-red-100 text-red-700 text-sm font-semibold border border-red-200",
            ),
            "px-3 py-1 rounded-full bg-gray-100 text-gray-700 text-sm font-semibold border border-gray-200",
        ),
    )


def expense_detail_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 animate-fade-in"
            ),
            rx.radix.primitives.dialog.content(
                rx.cond(
                    ExpenseState.selected_expense,
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.radix.primitives.dialog.title(
                                    "Expense Details",
                                    class_name="text-xl font-bold text-gray-900",
                                ),
                                rx.radix.primitives.dialog.description(
                                    "Full report information",
                                    class_name="text-sm text-gray-500 mt-1",
                                ),
                            ),
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    rx.icon("x", class_name="h-5 w-5 text-gray-500"),
                                    class_name="p-2 rounded-full hover:bg-gray-100 transition-colors",
                                )
                            ),
                            class_name="flex justify-between items-start mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.p(
                                        "Amount", class_name="text-sm text-gray-500"
                                    ),
                                    rx.el.h2(
                                        f"${ExpenseState.selected_expense['amount']}",
                                        class_name="text-3xl font-bold text-gray-900 mt-1",
                                    ),
                                    class_name="bg-gray-50 rounded-lg p-4 text-center mb-6",
                                ),
                                detail_row(
                                    "Employee",
                                    ExpenseState.selected_expense["employee"],
                                ),
                                detail_row(
                                    "Category",
                                    ExpenseState.selected_expense["category"],
                                ),
                                detail_row(
                                    "Date", ExpenseState.selected_expense["date"]
                                ),
                                detail_row(
                                    "Description",
                                    ExpenseState.selected_expense["description"],
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Status",
                                        class_name="text-sm font-medium text-gray-500 mb-2",
                                    ),
                                    status_badge_large(
                                        ExpenseState.selected_expense["status"]
                                    ),
                                    class_name="py-3",
                                ),
                            )
                        ),
                        class_name="p-6",
                    ),
                    rx.el.div("No expense selected", class_name="p-6"),
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-2xl shadow-2xl w-full max-w-md z-50 outline-none focus:outline-none",
            ),
        ),
        open=ExpenseState.is_modal_open,
        on_open_change=ExpenseState.close_modal,
    )


def create_expense_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 animate-fade-in"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.radix.primitives.dialog.title(
                                "Create New Expense",
                                class_name="text-xl font-bold text-gray-900",
                            ),
                            rx.radix.primitives.dialog.description(
                                "Enter the details for the new expense.",
                                class_name="text-sm text-gray-500 mt-1",
                            ),
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="h-5 w-5 text-gray-500"),
                                class_name="p-2 rounded-full hover:bg-gray-100 transition-colors",
                            )
                        ),
                        class_name="flex justify-between items-start mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Employee",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.select(
                                rx.el.option(
                                    "Select Employee", value="", disabled=True
                                ),
                                rx.foreach(
                                    ExpenseState.employee_options,
                                    lambda opt: rx.el.option(
                                        opt["label"], value=opt["value"]
                                    ),
                                ),
                                value=ExpenseState.new_expense_employee_id,
                                on_change=ExpenseState.set_new_expense_employee_id,
                                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 border",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Date",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="date",
                                on_change=ExpenseState.set_new_expense_date,
                                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 border",
                                default_value=ExpenseState.new_expense_date,
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Category",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.select(
                                rx.el.option(
                                    "Select Category", value="", disabled=True
                                ),
                                rx.foreach(
                                    ExpenseState.category_options,
                                    lambda opt: rx.el.option(
                                        opt["label"], value=opt["value"]
                                    ),
                                ),
                                value=ExpenseState.new_expense_category_id,
                                on_change=ExpenseState.set_new_expense_category_id,
                                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 border",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Amount",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "$",
                                    class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500",
                                ),
                                rx.el.input(
                                    type="number",
                                    placeholder="0.00",
                                    step="0.01",
                                    on_change=ExpenseState.set_new_expense_amount,
                                    class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 pl-7 pr-3 border",
                                    default_value=ExpenseState.new_expense_amount,
                                ),
                                class_name="relative",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Description",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.textarea(
                                placeholder="Enter expense details...",
                                on_change=ExpenseState.set_new_expense_description,
                                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 border",
                                rows="3",
                                default_value=ExpenseState.new_expense_description,
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Receipt URL (Optional)",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="text",
                                placeholder="https://...",
                                on_change=ExpenseState.set_new_expense_receipt_url,
                                class_name="w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 border",
                                default_value=ExpenseState.new_expense_receipt_url,
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Cancel",
                                    class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 mr-3",
                                )
                            ),
                            rx.el.button(
                                "Create Expense",
                                on_click=ExpenseState.create_expense,
                                class_name="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700",
                            ),
                            class_name="flex justify-end",
                        ),
                    ),
                    class_name="p-6",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-2xl shadow-2xl w-full max-w-lg z-50 outline-none focus:outline-none max-h-[90vh] overflow-y-auto",
            ),
        ),
        open=ExpenseState.is_create_modal_open,
        on_open_change=ExpenseState.close_create_modal,
    )