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