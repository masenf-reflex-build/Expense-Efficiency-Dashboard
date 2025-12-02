import reflex as rx
from reflex_google_auth import google_login


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-white"),
            class_name="h-12 w-12 rounded-lg bg-indigo-600 flex items-center justify-center mb-4 shadow-lg shadow-indigo-500/20",
        ),
        rx.el.h3(title, class_name="text-lg font-semibold text-gray-900 mb-2"),
        rx.el.p(description, class_name="text-gray-600 leading-relaxed"),
        class_name="p-6 bg-white rounded-2xl border border-gray-100 hover:shadow-xl transition-all duration-300 hover:-translate-y-1",
    )


def benefit_row(text: str) -> rx.Component:
    return rx.el.div(
        rx.icon(
            "circle-check", class_name="h-5 w-5 text-emerald-500 mr-3 flex-shrink-0"
        ),
        rx.el.span(text, class_name="text-gray-700"),
        class_name="flex items-center mb-4 last:mb-0",
    )


def landing_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Smart Expense Management",
                        class_name="inline-block px-4 py-1.5 rounded-full bg-indigo-50 text-indigo-600 text-sm font-semibold mb-6 border border-indigo-100",
                    ),
                    rx.el.h1(
                        "Control Your Spend,",
                        rx.el.br(),
                        rx.el.span(
                            "Maximize Your Growth", class_name="text-indigo-600"
                        ),
                        class_name="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 tracking-tight mb-6 leading-tight",
                    ),
                    rx.el.p(
                        "The modern expense tracking dashboard that gives you full visibility into your organization's spending. Real-time analytics, detailed reports, and actionable insights.",
                        class_name="text-lg sm:text-xl text-gray-600 mb-8 max-w-2xl mx-auto",
                    ),
                    rx.el.div(
                        google_login(),
                        class_name="transform hover:scale-105 transition-transform duration-200 inline-block shadow-lg shadow-indigo-500/20 rounded-full overflow-hidden",
                    ),
                    class_name="text-center max-w-4xl mx-auto pt-20 pb-16 sm:pt-32 sm:pb-24",
                ),
                class_name="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10",
            ),
            rx.el.div(
                class_name="absolute top-0 left-0 right-0 h-[500px] bg-gradient-to-b from-indigo-50/50 to-white -z-10"
            ),
            rx.el.div(
                class_name="absolute top-20 left-10 w-64 h-64 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"
            ),
            rx.el.div(
                class_name="absolute top-20 right-10 w-64 h-64 bg-indigo-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"
            ),
            class_name="relative overflow-hidden",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Everything you need to manage expenses",
                        class_name="text-3xl font-bold text-gray-900 text-center mb-4",
                    ),
                    rx.el.p(
                        "Powerful features to help you keep track of every penny.",
                        class_name="text-gray-600 text-center mb-12 max-w-2xl mx-auto",
                    ),
                    class_name="container mx-auto px-4 sm:px-6 lg:px-8",
                ),
                rx.el.div(
                    feature_card(
                        "bar-chart-3",
                        "Real-time Analytics",
                        "Visualize spending trends instantly with interactive charts and graphs.",
                    ),
                    feature_card(
                        "pie-chart",
                        "Category Insights",
                        "Break down expenses by category to identify high-spending areas.",
                    ),
                    feature_card(
                        "users",
                        "Team Tracking",
                        "Monitor spending across different employees and departments.",
                    ),
                    feature_card(
                        "file-spreadsheet",
                        "Detailed Reports",
                        "Drill down into individual expense reports with full context.",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 container mx-auto px-4 sm:px-6 lg:px-8",
                ),
                class_name="py-20 bg-white",
            )
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Why choose our dashboard?",
                        class_name="text-3xl font-bold text-gray-900 mb-6",
                    ),
                    rx.el.p(
                        "Stop wrestling with spreadsheets. Our platform provides a centralized hub for all your expense data, making it easy to audit, analyze, and optimize.",
                        class_name="text-lg text-gray-600 mb-8",
                    ),
                    benefit_row("Instant visibility into company cash flow"),
                    benefit_row("Identify top spenders and trends automatically"),
                    benefit_row("Secure, Google-integrated authentication"),
                    benefit_row("Mobile-friendly design for on-the-go access"),
                    class_name="max-w-xl",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            class_name="absolute inset-0 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-2xl transform rotate-3 opacity-10"
                        ),
                        rx.el.div(
                            rx.icon(
                                "layout-dashboard",
                                class_name="w-32 h-32 text-indigo-600 opacity-50 mx-auto mt-20",
                            ),
                            class_name="relative bg-white border border-gray-200 rounded-2xl shadow-2xl h-80 w-full flex items-center justify-center overflow-hidden",
                        ),
                        class_name="relative",
                    ),
                    class_name="relative lg:ml-10 mt-12 lg:mt-0",
                ),
                class_name="container mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 lg:grid-cols-2 items-center",
            ),
            class_name="py-20 bg-gray-50",
        ),
        rx.el.div(
            rx.el.h2(
                "Ready to take control?",
                class_name="text-3xl font-bold text-white mb-6",
            ),
            rx.el.p(
                "Join thousands of teams managing their expenses smarter.",
                class_name="text-indigo-100 mb-8 max-w-xl mx-auto",
            ),
            rx.el.div(
                google_login(),
                class_name="inline-block bg-white rounded-full p-1 hover:shadow-lg transition-all overflow-hidden",
            ),
            class_name="bg-indigo-600 py-20 text-center px-4",
        ),
        class_name="min-h-screen bg-white font-['Inter']",
    )