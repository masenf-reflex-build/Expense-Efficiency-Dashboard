import reflex as rx
from app.states.expense_state import ExpenseState, CategoryData

TOOLTIP_PROPS = {
    "content_style": {
        "backgroundColor": "white",
        "borderRadius": "8px",
        "border": "1px solid #E5E7EB",
        "boxShadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "padding": "8px 12px",
    },
    "item_style": {
        "color": "#374151",
        "fontSize": "14px",
        "fontWeight": "500",
        "padding": "0",
    },
    "label_style": {"color": "#6B7280", "fontSize": "12px", "marginBottom": "4px"},
    "separator": "",
}


def cash_flow_chart() -> rx.Component:
    """Area chart showing spending trends over time."""
    return rx.el.div(
        rx.el.h3(
            "Cash Flow Trend", class_name="text-lg font-semibold text-gray-900 mb-4"
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", vertical=False, stroke="#E5E7EB"
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="date",
                axis_line=False,
                tick_line=False,
                tick={"fill": "#6B7280", "fontSize": 12},
                tick_margin=10,
                min_tick_gap=30,
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                tick={"fill": "#6B7280", "fontSize": 12},
                tick_margin=10,
            ),
            rx.recharts.area(
                data_key="amount",
                name="Daily Spending",
                stroke="#4F46E5",
                fill="#4F46E5",
                fill_opacity=0.1,
                stroke_width=2,
                active_dot={"r": 6, "strokeWidth": 0},
            ),
            data=ExpenseState.daily_spending,
            width="100%",
            height=300,
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full",
    )


def category_legend_item(item: CategoryData) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="w-3 h-3 rounded-full mr-2",
            style={"backgroundColor": item["fill"]},
        ),
        rx.el.span(item["name"], class_name="text-sm text-gray-600 flex-1"),
        rx.el.span(f"${item['value']}", class_name="text-sm font-medium text-gray-900"),
        class_name="flex items-center mb-2",
    )


def category_pie_chart() -> rx.Component:
    """Pie chart showing spending by category."""
    return rx.el.div(
        rx.el.h3(
            "Spending by Category",
            class_name="text-lg font-semibold text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.recharts.pie_chart(
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.pie(
                    data=ExpenseState.category_breakdown,
                    data_key="value",
                    name_key="name",
                    cx="50%",
                    cy="50%",
                    inner_radius="60%",
                    outer_radius="100%",
                    padding_angle=2,
                    stroke="white",
                    stroke_width=2,
                ),
                width="100%",
                height=200,
            ),
            class_name="h-[200px] w-full mb-6",
        ),
        rx.el.div(
            rx.foreach(ExpenseState.category_breakdown, category_legend_item),
            class_name="flex flex-col max-h-[200px] overflow-y-auto pr-2 custom-scrollbar",
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full flex flex-col",
    )