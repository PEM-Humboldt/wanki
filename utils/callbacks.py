"""
"""
import base64
import io
import pathlib
from zipfile import ZipFile

import dash
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import wiutils
from dash.dependencies import Output, Input, State
from scipy.stats.kde import gaussian_kde


def _plot_accumulation_curve(images, deployments):
    images = images.copy()
    images["timestamp"] = pd.to_datetime(images["timestamp"])
    images["date"] = pd.to_datetime(images["timestamp"].dt.date)
    start = pd.to_datetime(deployments["start_date"]).min()
    end = pd.to_datetime(deployments["end_date"]).max()
    date_range = pd.date_range(start, end, freq="D")
    df = pd.DataFrame(
        {"date": date_range, "day": np.arange(date_range.size), "richness": 0}
    )
    for i, row in df.iterrows():
        date = row["date"]
        subdf = images[images["date"] <= date]
        richness = subdf["scientific_name"].unique().size
        row["richness"] = richness
        df.loc[i] = row

    fig = px.line(
        df, x="day", y="richness", labels={"day": "Día", "richness": "Riqueza"}
    )

    return fig


def _plot_site_dates(deployments):
    deployments = deployments.copy()
    deployments["start_date"] = pd.to_datetime(deployments["start_date"])
    deployments["end_date"] = pd.to_datetime(deployments["end_date"])

    df = pd.melt(
        deployments, id_vars="deployment_id", value_vars=["start_date", "end_date"]
    )

    df = df.sort_values(["value"], ascending=True)

    fig = px.line(
        df,
        x="value",
        y="deployment_id",
        color="deployment_id",
        color_discrete_sequence=["#636EFA"],
        labels={"value": "Fecha", "deployment_id": "Evento"},
    )

    fig.update_layout(showlegend=False)

    return fig


def _plot_activity_hours(images, names):

    images = images.copy()
    images["hour"] = pd.to_datetime(images["timestamp"]).dt.round("H").dt.hour
    df = pd.DataFrame(columns=["x", "y", "name"])
    x_range = np.linspace(0, 24, 1000)
    for name in names:
        hours = images[images["scientific_name"] == name]["hour"].to_numpy()
        if np.unique(hours).size > 1:
            kde = gaussian_kde(hours)       
            df = pd.concat([df, 
                            pd.DataFrame(
                    {"x": x_range, "y": kde(x_range), "name": [name] * x_range.size}
                )
                            ], 
                            ignore_index=True)
    if not df.empty:
        fig = px.line(
            df, x="x", y="y", color="name", labels={"x": "Hora", "y": "Densidad"}
        )
        ticks = [i for i in range(0, 25) if i % 2 == 0]
        fig.update_layout(
            xaxis=dict(
                tickmode="array",
                tickvals=ticks,
                ticktext=list(map(lambda x: f"{str(x).zfill(2)}:00", ticks)),
            ),
            legend_title_text="",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
    else:
        fig = go.Figure()
    return fig


def _plot_presence_absence(images, deployments, name):
    images = images.copy()
    images = images[images["scientific_name"] == name]
    images["timestamp"] = pd.to_datetime(images["timestamp"])
    images["date"] = pd.to_datetime(images["timestamp"].dt.date)
    start = pd.to_datetime(deployments["start_date"]).min()
    end = pd.to_datetime(deployments["end_date"]).max()
    date_range = pd.date_range(start, end, freq="D")
    deployment_ids = sorted(deployments["deployment_id"].unique())
    df = pd.DataFrame(index=deployment_ids, columns=np.arange(date_range.size))
    for id_ in deployment_ids:
        subdf = images[images["deployment_id"] == id_]
        if subdf.empty:
            df.loc[id_] = 0
        df.loc[id_] = date_range.isin(subdf["date"]).astype(int)

    fig = px.imshow(df, labels={"x": "Día", "y": "Evento", "color": "Presencia"})

    return fig


def generate_callbacks(app):
    """
    """

    @app.callback(
        Output("store", "data"),
        Output("project-name", "children"),
        Output("project-sites", "children"),
        Output("project-images", "children"),
        Output("fig-species-list-1", "options"),
        Output("fig-species-list-2", "options"),
        Output("data-check", "className"),
        Output("data-check-tooltip", "style"),
        Input("upload", "contents"),
        State("upload", "filename"),
        State("remove-duplicates", "value"),
        State("remove-duplicates-interval", "value"),
    )
    def store_project(content, name, remove_duplicates, remove_duplicates_interval):
        if content is not None:
            string = content.split(",")[1]
            decoded = base64.b64decode(string)
            z = ZipFile(io.BytesIO(decoded))
            stem = pathlib.Path(name).stem
            try:
                images = pd.read_csv(io.BytesIO(z.read(f"{stem}/images.csv")))
                images = wiutils.remove_unidentified(images, rank="genus")
                images["scientific_name"] = wiutils.get_scientific_name(
                    images, keep_genus=True, add_qualifier=True
                )
                if remove_duplicates and remove_duplicates_interval:
                    images = wiutils.remove_duplicates(
                        images, interval=remove_duplicates_interval, unit="minutes"
                    )
                deployments = pd.read_csv(io.BytesIO(z.read(f"{stem}/deployments.csv")))
                projects = pd.read_csv(io.BytesIO(z.read(f"{stem}/projects.csv")))
            except KeyError:
                return None, "", "", "", [], [], "fas fa-times-circle", {"display": "float"}
            reference = pd.read_csv(
                pathlib.Path(__file__)
                .parents[1]
                .joinpath("assets/reference.csv")
                .as_posix()
            )
            data = {
                "images": images.to_json(orient="split"),
                "deployments": deployments.to_json(orient="split"),
                "projects": projects.to_json(orient="split"),
                "reference": reference.to_json(orient="split"),
            }
            name = projects.loc[0, "project_name"]
            sites = pd.read_json(data["deployments"], orient="split").shape[0]
            nimages = images.shape[0]
            options = [
                {"label": name, "value": name}
                for name in images["scientific_name"].dropna().sort_values().unique()
            ]

            return data, name, sites, nimages, options, options, "fas fa-check-circle", {"display": "none"}
        else:
            return None, "", "", "", [], [], "", {}

    @app.callback(
        Output("data-table", "columns"),
        Output("data-table", "data"),
        Output("data-table-wrapper", "style"),
        Output("graph", "figure"),
        Output("graph-wrapper", "style"),
        Input("general-count", "n_clicks"),
        Input("dwc-events", "n_clicks"),
        Input("dwc-records", "n_clicks"),
        Input("deployment-detection", "n_clicks"),
        Input("detection-history", "n_clicks"),
        Input("hill-numbers", "n_clicks"),
        Input("deployment-summary", "n_clicks"),
        Input("accumulation-curve", "n_clicks"),
        Input("site-dates", "n_clicks"),
        Input("activity-hours", "n_clicks"),
        Input("presence-absence", "n_clicks"),
        State("store", "data"),
        State("general-count-add-taxonomy", "value"),
        State("general-count-threat-status", "value"),
        State("general-count-endemic", "value"),
        State("dwc-lang", "value"),
        State("deployment-detection-compute-abundance", "value"),
        State("deployment-detection-pivot", "value"),
        State("detection-history-days", "value"),
        State("detection-history-date-range", "value"),
        State("detection-history-compute-abundance", "value"),
        State("detection-history-pivot", "value"),
        State("hill-numbers-q", "value"),
        State("hill-numbers-pivot", "value"),
        State("fig-species-list-1", "value"),
        State("fig-species-list-2", "value"),
    )
    def execute(
        btn1,
        btn2,
        btn3,
        btn4,
        btn5,
        btn6,
        btn7,
        btn8,
        btn9,
        btn10,
        btn11,
        data,
        general_count_add_taxonomy,
        general_count_threat_status,
        general_count_endemic,
        dwc_lang,
        deployment_detection_compute_abundance,
        deployment_detection_pivot,
        detection_history_days,
        detection_history_date_range,
        detection_history_compute_abundance,
        detection_history_pivot,
        hill_numbers_q,
        hill_numbers_pivot,
        names,
        name,
    ):
        ctx = dash.callback_context
        if not ctx.triggered:
            return None, None, {}, {}, {}
        else:
            id_ = ctx.triggered[0]["prop_id"].split(".")[0]
            images = pd.read_json(data["images"], orient="split")
            deployments = pd.read_json(data["deployments"], orient="split")
            projects = pd.read_json(data["projects"], orient="split")
            status = None
            if id_ == "general-count":
                status = "table"
                reference = pd.read_json(data["reference"], orient="split")
                reference = reference.rename(
                    columns={
                        "scientificName": "scientific_name",
                        "threatStatus": "threat_status",
                        "establishmentMeans": "establishment_means",
                    }
                )
                result = wiutils.compute_general_count(
                    images, add_taxonomy=True#bool(general_count_add_taxonomy)
                )
                result['scientific_name'] = wiutils.get_scientific_name(result)
                if bool(general_count_threat_status):
                    result = pd.merge(
                        result,
                        reference[["scientific_name", "threat_status"]],
                        how="left",
                        on="scientific_name",
                    )
                if bool(general_count_endemic):
                    result = pd.merge(
                        result,
                        reference[["scientific_name", "establishment_means"]],
                        how="left",
                        on="scientific_name",
                    )
            elif id_ == "dwc-events":
                status = "table"
                result = wiutils.create_dwc_event(
                    deployments, projects,#language=dwc_lang
                    )
            elif id_ == "dwc-records":
                status = "table"
                result = wiutils.create_dwc_occurrence(
                    images, deployments, projects,
                    #remove_duplicate_kws={"interval": 1, "unit": "hours"}, 
                    #language=dwc_lang
                    )
            elif id_ == "deployment-detection":
                status = "table"
                result = wiutils.compute_detection(
                    images,
                    compute_abundance=deployment_detection_compute_abundance,
                    pivot=deployment_detection_pivot,
                )
            elif id_ == "detection-history":
                status = "table"
                result = wiutils.compute_detection_history(
                    images,
                    deployments,
                    date_range=detection_history_date_range,
                    days=detection_history_days,
                    compute_abundance=detection_history_compute_abundance,
                    pivot=detection_history_pivot,
                )
            elif id_ == "hill-numbers":
                status = "table"
                q_values = list(map(lambda x: int(x), hill_numbers_q.split(",")))
                result = wiutils.compute_hill_numbers(
                    images, q_values=q_values, pivot=hill_numbers_pivot
                )
            elif id_ == "deployment-summary":
                status = "table"
                result = wiutils.compute_count_summary(images)
            elif id_ == "accumulation-curve":
                status = "figure"
                fig = _plot_accumulation_curve(images, deployments)
            elif id_ == "site-dates":
                status = "figure"
                fig = _plot_site_dates(deployments)
            elif id_ == "activity-hours":
                status = "figure"
                fig = _plot_activity_hours(images, names)
            elif id_ == "presence-absence":
                status = "figure"
                fig = _plot_presence_absence(images, deployments, name)
            else:
                return None, None, {}, {}, {}

            if status == "table":
                table_style = {"display": "block"}
                figure_style = {"display": "none"}
                columns = [{"name": i, "id": i} for i in result.columns]
                data = result.to_dict("records")
                fig = {}
            elif status == "figure":
                table_style = {"display": "none"}
                figure_style = {"display": "block"}
                columns = []
                data = []

            return columns, data, table_style, fig, figure_style