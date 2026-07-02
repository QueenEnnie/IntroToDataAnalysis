from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dash_table, dcc, html

DATA_PATH = Path(__file__).with_name("Sleep_Health_and_Lifestyle_Dataset.csv")


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Файл Sleep_Health_and_Lifestyle_Dataset.csv не найден. "
            "Положите CSV из ЛР4 в одну папку с этим app.py."
        )

    df = pd.read_csv(DATA_PATH)
    df = df.copy()

    # Подготовка признаков так же, как в ЛР4.
    if "BMI Category" in df.columns:
        df["BMI Category"] = df["BMI Category"].replace({"Normal Weight": "Normal"})

    if "Sleep Disorder" in df.columns:
        df["Sleep Disorder"] = df["Sleep Disorder"].fillna("None")

    if "Blood Pressure" in df.columns and "Systolic_BP" not in df.columns:
        df["Systolic_BP"] = df["Blood Pressure"].astype(str).str.split("/").str[0].astype(int)

    numeric_cols = [
        "Age",
        "Sleep Duration",
        "Quality of Sleep",
        "Physical Activity Level",
        "Stress Level",
        "Heart Rate",
        "Daily Steps",
        "Systolic_BP",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data()

app = Dash(__name__)
app.title = "ЛР5 — Sleep Health Dashboard"
server = app.server

FILTER_STYLE = {
    "backgroundColor": "white",
    "border": "1px solid #e6edf5",
    "borderRadius": "14px",
    "padding": "14px",
    "boxShadow": "0 6px 18px rgba(20, 40, 80, 0.05)",
}
CARD_STYLE = {
    "backgroundColor": "white",
    "border": "1px solid #e6edf5",
    "borderRadius": "18px",
    "padding": "18px",
    "boxShadow": "0 8px 22px rgba(20, 40, 80, 0.06)",
}


def card(title: str, value_id: str, subtitle: str) -> html.Div:
    return html.Div(
        [
            html.Div(title, style={"fontSize": "14px", "color": "#64748b", "marginBottom": "8px"}),
            html.Div(id=value_id, style={"fontSize": "34px", "fontWeight": "700", "color": "#0f172a"}),
            html.Div(subtitle, style={"fontSize": "12px", "color": "#94a3b8", "marginTop": "8px"}),
        ],
        style=CARD_STYLE,
    )


def dropdown_options(col: str):
    return [{"label": str(x), "value": x} for x in sorted(df[col].dropna().unique())]


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Дашборд: здоровье сна и образ жизни", style={"margin": "0", "color": "#0f172a"}),
                html.P(
                    "Интерактивный анализ датасета Sleep Health and Lifestyle",
                    style={"marginTop": "8px", "color": "#475569"},
                ),
            ],
            style={"marginBottom": "18px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Пол", style={"fontWeight": "600"}),
                        dcc.Dropdown(
                            id="gender-filter",
                            options=dropdown_options("Gender") if "Gender" in df.columns else [],
                            multi=True,
                            placeholder="Все значения",
                        ),
                    ],
                    style=FILTER_STYLE,
                ),
                html.Div(
                    [
                        html.Label("Категория BMI", style={"fontWeight": "600"}),
                        dcc.Dropdown(
                            id="bmi-filter",
                            options=dropdown_options("BMI Category") if "BMI Category" in df.columns else [],
                            multi=True,
                            placeholder="Все категории",
                        ),
                    ],
                    style=FILTER_STYLE,
                ),
                html.Div(
                    [
                        html.Label("Нарушение сна", style={"fontWeight": "600"}),
                        dcc.Dropdown(
                            id="disorder-filter",
                            options=dropdown_options("Sleep Disorder") if "Sleep Disorder" in df.columns else [],
                            multi=True,
                            placeholder="Все типы",
                        ),
                    ],
                    style=FILTER_STYLE,
                ),
            ],
            style={"display": "grid", "gridTemplateColumns": "repeat(3, minmax(220px, 1fr))", "gap": "14px", "marginBottom": "16px"},
        ),
        html.Div(
            [
                card("Средняя длительность сна", "avg-sleep", "Sleep Duration, часы"),
                card("Среднее качество сна", "avg-quality", "Quality of Sleep, 1–10"),
            ],
            style={"display": "grid", "gridTemplateColumns": "repeat(2, minmax(220px, 1fr))", "gap": "14px", "marginBottom": "16px"},
        ),
        html.Div(
            [
                html.Div(dcc.Graph(id="age-quality"), style=CARD_STYLE),
                html.Div(dcc.Graph(id="bmi-quality"), style=CARD_STYLE),
            ],
            style={"display": "grid", "gridTemplateColumns": "repeat(2, minmax(320px, 1fr))", "gap": "14px", "marginBottom": "16px"},
        ),
        html.Div(
            [
                html.Div(dcc.Graph(id="occupation-stress"), style=CARD_STYLE),
                html.Div(dcc.Graph(id="corr-heatmap"), style=CARD_STYLE),
            ],
            style={"display": "grid", "gridTemplateColumns": "repeat(2, minmax(320px, 1fr))", "gap": "14px", "marginBottom": "16px"},
        ),
        html.Div(
            [
                html.H3("Сводная таблица по профессиям", style={"marginTop": "0", "color": "#0f172a"}),
                dash_table.DataTable(
                    id="summary-table",
                    page_size=10,
                    sort_action="native",
                    style_table={"overflowX": "auto"},
                    style_cell={"fontFamily": "Arial", "fontSize": 13, "padding": "8px", "textAlign": "left"},
                    style_header={"fontWeight": "700", "backgroundColor": "#f8fafc"},
                    style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#fbfdff"}],
                ),
            ],
            style=CARD_STYLE,
        ),
    ],
    style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f6f8fb", "minHeight": "100vh", "padding": "28px"},
)


def filter_df(genders, bmi_categories, disorders):
    dff = df.copy()
    if genders:
        dff = dff[dff["Gender"].isin(genders)]
    if bmi_categories:
        dff = dff[dff["BMI Category"].isin(bmi_categories)]
    if disorders:
        dff = dff[dff["Sleep Disorder"].isin(disorders)]
    return dff


@app.callback(
    Output("avg-sleep", "children"),
    Output("avg-quality", "children"),
    Output("age-quality", "figure"),
    Output("bmi-quality", "figure"),
    Output("occupation-stress", "figure"),
    Output("corr-heatmap", "figure"),
    Output("summary-table", "data"),
    Output("summary-table", "columns"),
    Input("gender-filter", "value"),
    Input("bmi-filter", "value"),
    Input("disorder-filter", "value"),
)
def update_dashboard(genders, bmi_categories, disorders):
    dff = filter_df(genders, bmi_categories, disorders)

    avg_sleep = "—" if dff.empty else f"{dff['Sleep Duration'].mean():.2f}"
    avg_quality = "—" if dff.empty else f"{dff['Quality of Sleep'].mean():.2f}"

    if dff.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Нет данных для выбранных фильтров", template="plotly_white")
        return avg_sleep, avg_quality, empty_fig, empty_fig, empty_fig, empty_fig, [], []

    fig_age = px.scatter(
        dff,
        x="Age",
        y="Quality of Sleep",
        color="Sleep Disorder" if "Sleep Disorder" in dff.columns else None,
        trendline="ols",
        title="Возраст и качество сна",
        labels={"Age": "Возраст", "Quality of Sleep": "Качество сна", "Sleep Disorder": "Нарушение сна"},
    )
    fig_age.update_layout(template="plotly_white", legend_title_text="Нарушение сна")

    fig_bmi = px.box(
        dff,
        x="BMI Category",
        y="Quality of Sleep",
        points="all",
        title="Качество сна по категориям BMI",
        labels={"BMI Category": "Категория BMI", "Quality of Sleep": "Качество сна"},
    )
    fig_bmi.update_layout(template="plotly_white")

    occ = (
        dff.groupby("Occupation", as_index=False)["Stress Level"]
        .mean()
        .sort_values("Stress Level", ascending=False)
        .head(10)
    )
    fig_occ = px.bar(
        occ,
        x="Stress Level",
        y="Occupation",
        orientation="h",
        title="Топ-10 профессий по среднему уровню стресса",
        labels={"Stress Level": "Средний стресс", "Occupation": "Профессия"},
    )
    fig_occ.update_layout(template="plotly_white", yaxis={"categoryorder": "total ascending"})

    corr_cols = [
        "Age",
        "Sleep Duration",
        "Quality of Sleep",
        "Physical Activity Level",
        "Stress Level",
        "Heart Rate",
        "Daily Steps",
        "Systolic_BP",
    ]
    corr_cols = [c for c in corr_cols if c in dff.columns]
    corr = dff[corr_cols].corr(numeric_only=True).round(2)
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Корреляции числовых показателей",
        labels={"color": "r"},
    )
    fig_corr.update_layout(template="plotly_white")

    summary = (
        dff.groupby("Occupation")
        .agg(
            Count=("Person ID", "count"),
            Avg_Sleep=("Sleep Duration", "mean"),
            Avg_Quality=("Quality of Sleep", "mean"),
            Avg_Stress=("Stress Level", "mean"),
            Avg_Activity=("Physical Activity Level", "mean"),
        )
        .reset_index()
        .sort_values("Count", ascending=False)
    )
    summary = summary.round({"Avg_Sleep": 2, "Avg_Quality": 2, "Avg_Stress": 2, "Avg_Activity": 2})
    columns = [
        {"name": "Профессия", "id": "Occupation"},
        {"name": "Кол-во", "id": "Count"},
        {"name": "Сон, ч", "id": "Avg_Sleep"},
        {"name": "Качество сна", "id": "Avg_Quality"},
        {"name": "Стресс", "id": "Avg_Stress"},
        {"name": "Активность", "id": "Avg_Activity"},
    ]

    return avg_sleep, avg_quality, fig_age, fig_bmi, fig_occ, fig_corr, summary.to_dict("records"), columns


if __name__ == "__main__":
    app.run(debug=True)
