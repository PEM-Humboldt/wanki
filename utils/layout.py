"""
"""
import base64
import pathlib

import dash.dcc as dcc
import dash.html as html
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable


logo_path = pathlib.Path(__file__).parents[1].joinpath("assets/logo.png").as_posix()
encoded_image = base64.b64encode(open(logo_path, "rb").read())
header = html.Div(
    [
        html.Div(
            html.Img(
                src=f"data:image/png;base64,{encoded_image.decode()}", id="app-logo",
            )
        ),
        html.P(
            """
            Una aplicación para explorar y transformar datos provenientes de Wildlife 
            Insights.
            """
        ),
    ],
    className="h-100",
    id="header",
)

humboldt_logo_path = (
    pathlib.Path(__file__).parents[1].joinpath("assets/humboldt_logo.png").as_posix()
)
encoded_image = base64.b64encode(open(humboldt_logo_path, "rb").read())
logo = html.Div(
    [
        html.Img(
            src=f"data:image/png;base64,{encoded_image.decode()}",
            className="mh-100",
            id="logo",
        )
    ],
    className="h-100",
    id="logo-container",
)

data_box = dbc.Card(
    [
        dbc.CardHeader(
            [
                html.P("Carga de datos", className="title"),
                html.Div(
                    [
                        html.I(id="data-check", className="mx-1"),
                        html.I(className="fas fa-info-circle mx-1", id="data-info"),
                    ]
                ),
                dbc.Tooltip(
                    """
                    Carga de archivo .zip con el proyecto descargado de Wildlife Insights
                    con toda la información correspondiente. El archivo .zip debe contener
                    cuatro tablas en formato .csv (i.e. cameras.csv, 
                    deployments.csv, images.csv y project.csv). Aquellas imágenes que
                    no tengan alguna identificación hasta por lo menos género serán removidas.
                    También es posible eliminar registros duplicados dado un intervalo de
                    tiempo en minutos.
                """,
                    target="data-info",
                ),
                dbc.Tooltip(
                    """
                    Los datos cargados no son válidos. Asegurese que es un archivo .zip
                    y contiene todas las tablas asociadas al proyecto.
                """,
                    target="data-check",
                    id="data-check-tooltip",
                ),
            ],
            class_name="card-header",
        ),
        dbc.CardBody(
            dcc.Loading(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Upload(
                                    dbc.Button("Cargar", size="sm"),
                                    id="upload",
                                    accept=".zip",
                                ),
                                dcc.Checklist(
                                    options=[
                                        {"label": "Remover duplicados", "value": 1}
                                    ],
                                    id="remove-duplicates",
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            "Intervalo (minutos)",
                                            className="input-description",
                                        ),
                                        dbc.Input(
                                            type="number",
                                            min=0,
                                            max=3600,
                                            step=1,
                                            id="remove-duplicates-interval",
                                            value=30,
                                        ),
                                    ],
                                    className="input-group",
                                ),
                            ],
                            className="data-box-container",
                            width=7,
                        ),
                        dbc.Col(
                            [
                                html.P(
                                    [
                                        html.Span("Nombre:", className="item"),
                                        html.Span(id="project-name"),
                                    ]
                                ),
                                html.P(
                                    [
                                        html.Span("Sitios:", className="item"),
                                        html.Span(id="project-sites"),
                                    ]
                                ),
                                html.P(
                                    [
                                        html.Span("Imágenes totales:", className="item"),
                                        html.Span(id="project-images-all"),
                                    ]
                                ),
                                html.P(
                                    [
                                        html.Span("Imágenes identificadas:", className="item"),
                                        html.Span(id="project-images"),
                                    ]
                                ),
                            ],
                            className="data-box-container",
                            width=5,
                        ),
                    ]
                )
            )
        ),
    ],
    class_name="w-100",
    id="data-box",
)

video_box = dbc.Card(
    [
        dbc.CardHeader(
            [
                html.P("Carga de Videos", className="title"),
                html.Div(
                    [
                        html.I(id="data-check", className="mx-1"),
                        html.I(className="fas fa-info-circle mx-1", id="data-info"),
                    ]
                ),
                dbc.Tooltip(
                    """
                    TODO
                    Carga de archivo .zip con el proyecto descargado de Wildlife Insights
                    con toda la información correspondiente. El archivo .zip debe contener
                    cuatro tablas en formato .csv (i.e. cameras.csv, 
                    deployments.csv, images.csv y project.csv). Aquellas imágenes que
                    no tengan alguna identificación hasta por lo menos género serán removidas.
                    También es posible eliminar registros duplicados dado un intervalo de
                    tiempo en minutos.
                """,
                    target="data-info",
                ),
                dbc.Tooltip(
                    """
                    TODO
                    Los datos cargados no son válidos. Asegurese que es un archivo .zip
                    y contiene todas las tablas asociadas al proyecto.
                """,
                    target="data-check",
                    id="data-check-tooltip",
                ),
            ],
            class_name="card-header",
        ),
        dbc.CardBody(
            dcc.Loading(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Upload(
                                    dbc.Button("Cargar", size="sm"),
                                    id="upload",
                                    accept=".mp4",
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            "Offset ?",
                                            className="input-description",
                                        ),
                                        dbc.Input(
                                            type="number",
                                            min=0,
                                            max=3600,
                                            step=1,
                                            id="remove-duplicates-interval",
                                            value=30,
                                        ),
                                    ],
                                    className="input-group",
                                ),
                            ],
                            className="data-box-container",
                            width=7,
                        ),
                    
                    ]
                )
            )
        ),
    ],
    class_name="w-100",
    id="data-box",
)

tables = dbc.Accordion(
    [
        dbc.AccordionItem(
            [
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Listado de especies"),
                        dbc.PopoverBody(
                            """
                        Listado de especies con número de imágenes y eventos de muestreo 
                        asociados. Se puede incluir el estado de amenaza y endemismo de 
                        cada especie.
                    """
                        ),
                    ],
                    target="general-count-item",
                    trigger="hover",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P("Opciones", className="input-description"),
                                dcc.Checklist(
                                    options=[
                                        {
                                            "label": "Agregar taxonomía superior",
                                            "value": 1,
                                        }
                                    ],
                                    id="general-count-add-taxonomy",
                                ),
                                dcc.Checklist(
                                    options=[
                                        {
                                            "label": "Agregar categoría de Amenaza",
                                            "value": 1,
                                        }
                                    ],
                                    id="general-count-threat-status",
                                ),
                                dcc.Checklist(
                                    options=[{"label": "Agregar endemismo", "value": 1}],
                                    id="general-count-endemic",
                                ),
                            ],
                            className="input-group",
                        ),
                    ],
                    className="args",
                ),
                dbc.Button("Ejecutar", size="sm", id="general-count", n_clicks=0),
            ],
            title="Listado de especies",
            id="general-count-item",
        ),
        dbc.AccordionItem(
            [
                dbc.Popover(
                    [
                        dbc.PopoverHeader("DarwinCore"),
                        dbc.PopoverBody(
                            """
                    Tablas de eventos y registros organizadas bajo el estándar Darwin Core
                    (DwC) para publicación en sistemas de información de biodiversidad 
                    (e.g. SiB Colombia y GBIF). Algunos requerimientos quedan vacíos 
                    para el diligenciamiento por parte del usuario.
                    """
                        ),
                    ],
                    target="darwin-core-item",
                    trigger="hover",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P("Idioma", className="input-description"),
                                dcc.Dropdown(
                                    options=[
                                        {"label": "Español", "value": "es"},
                                        {"label": "Inglés", "value": "en"},
                                    ],
                                    id="dwc-lang",
                                    value="es",
                                ),
                            ],
                            className="input-group",
                        ),
                    ],
                    className="args",
                ),
                dbc.Button("Eventos", size="sm", id="dwc-events", n_clicks=0),
                dbc.Button("Registros", size="sm", id="dwc-records", n_clicks=0),
            ],
            title="DarwinCore",
            id="darwin-core-item",
        ),
        dbc.AccordionItem(
            [
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Detección por sitio"),
                        dbc.PopoverBody(
                            """
                    Listado de especies con frecuencia/presencia por evento de muestreo.
                    """
                        ),
                    ],
                    target="deployment-detection-id",
                    trigger="hover",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P("Cálculo", className="input-description"),
                                dcc.RadioItems(
                                    options=[
                                        {"label": "Frecuencia", "value": 1},
                                        {"label": "Presencia", "value": 0},
                                    ],
                                    value=1,
                                    id="deployment-detection-compute-abundance",
                                ),
                            ],
                            className="input-group",
                        ),
                        html.Div(
                            [
                                html.P("Formato", className="input-description"),
                                dcc.RadioItems(
                                    options=[
                                        {"label": "Horizontal", "value": 1},
                                        {"label": "Vertical", "value": 0},
                                    ],
                                    value=1,
                                    id="deployment-detection-pivot",
                                ),
                            ],
                            className="input-group",
                        ),
                    ],
                    className="args",
                ),
                dbc.Button("Ejecutar", size="sm", id="deployment-detection", n_clicks=0),
            ],
            title="Detección por sitio",
            id="deployment-detection-id",
        ),
        dbc.AccordionItem(
            [
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Historias de detección"),
                        dbc.PopoverBody(
                            """
                        Para cada especie, frecuencia/presencia agrupada por intervalo de
                         días.
                        """
                        ),
                    ],
                    target="detection-history-item",
                    trigger="hover",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    "Intervalo (días)", className="input-description"
                                ),
                                dbc.Input(
                                    type="number",
                                    min=1,
                                    max=60,
                                    step=1,
                                    id="detection-history-days",
                                    value=1,
                                ),
                            ],
                            className="input-group",
                        ),
                        html.Div(
                            [
                                html.P("Rango de fechas", className="input-description"),
                                dcc.RadioItems(
                                    options=[
                                        {"label": "Eventos", "value": "deployments"},
                                        {"label": "Imágenes", "value": "images"},
                                    ],
                                    value="deployments",
                                    id="detection-history-date-range",
                                ),
                            ],
                            className="input-group",
                        ),
                        html.Div(
                            [
                                html.P("Cálculo", className="input-description"),
                                dcc.RadioItems(
                                    options=[
                                        {"label": "Frecuencia", "value": 1},
                                        {"label": "Presencia", "value": 0},
                                    ],
                                    value=1,
                                    id="detection-history-compute-abundance",
                                ),
                            ],
                            className="input-group",
                        ),
                        html.Div(
                            [
                                html.P("Formato", className="input-description"),
                                dcc.RadioItems(
                                    options=[
                                        {"label": "Horizontal", "value": 1},
                                        {"label": "Vertical", "value": 0},
                                    ],
                                    value=1,
                                    id="detection-history-pivot",
                                ),
                            ],
                            className="input-group",
                        ),
                    ],
                    className="args",
                ),
                dbc.Button("Ejecutar", size="sm", id="detection-history", n_clicks=0),
            ],
            title="Historias de detección",
            id="detection-history-item",
        ),
        dbc.AccordionItem(
            [
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Números de Hill"),
                        dbc.PopoverBody(
                            """
                        Índices de diversidad de orden q (0: riqueza absoluta, 1: Shannon-Wiener, 2: Simpson).
                    """
                        ),
                    ],
                    target="hill-numbers-item",
                    trigger="hover",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P("Valores de q", className="input-description"),
                                dbc.Input(
                                    type="text",
                                    id="hill-numbers-q",
                                    placeholder="e.g. 1,2,3",
                                ),
                            ],
                            className="input-group",
                        ),
                        html.Div(
                            [
                                html.P("Formato", className="input-description"),
                                dcc.RadioItems(
                                    options=[
                                        {"label": "Horizontal", "value": 1},
                                        {"label": "Vertical", "value": 0},
                                    ],
                                    value=1,
                                    id="hill-numbers-pivot",
                                ),
                            ],
                            className="input-group",
                        ),
                    ],
                    className="args",
                ),
                dbc.Button("Ejecutar", size="sm", id="hill-numbers", n_clicks=0),
            ],
            title="Números de Hill",
            id="hill-numbers-item",
        ),
        dbc.AccordionItem(
            [
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Resumen por sitio"),
                        dbc.PopoverBody(
                            """
                        Número de imágenes y especies por evento de muestreo.
                    """
                        ),
                    ],
                    target="deployment-summary-item",
                    trigger="hover",
                ),
                dbc.Button("Ejecutar", size="sm", id="deployment-summary", n_clicks=0),
            ],
            title="Resumen por sitio",
            id="deployment-summary-item",
        ),
    ]
)

figures = dbc.Accordion(
    [
        dbc.AccordionItem(
            [
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Curva de acumulación"),
                        dbc.PopoverBody(
                            """
                        Especies registradas por días de muestreo.
                    """
                        ),
                    ],
                    target="accumulation-curve-item",
                    trigger="hover",
                ),
                dbc.Button("Ejecutar", size="sm", id="accumulation-curve", n_clicks=0),
            ],
            title="Curva de acumulación",
            id="accumulation-curve-item",
        ),
        dbc.AccordionItem(
            [
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Fechas por sitio"),
                        dbc.PopoverBody(
                            """
                                Intervalo de muestreo por evento.
                            """
                        ),
                    ],
                    target="site-dates-item",
                    trigger="hover",
                ),
                dbc.Button("Ejecutar", size="sm", id="site-dates", n_clicks=0),
            ],
            title="Fechas de muestreo",
            id="site-dates-item",
        ),
        dbc.AccordionItem(
            [
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Horario de actividad"),
                        dbc.PopoverBody(
                            """
                                Horario de actividad para una o múltiples especies.
                            """
                        ),
                    ],
                    target="activity-hours-item",
                    trigger="hover",
                ),
                html.Div(
                    [
                        html.P("Especies", className="input-description"),
                        dcc.Dropdown(id="fig-species-list-1", multi=True),
                    ],
                    className="input-group",
                ),
                dbc.Button("Ejecutar", size="sm", id="activity-hours", n_clicks=0),
            ],
            title="Horario de actividad",
            id="activity-hours-item",
        ),
        dbc.AccordionItem(
            [
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Presencia/Ausencia"),
                        dbc.PopoverBody(
                            """
                            Registro en eventos por días de muestreo.
                            """
                        ),
                    ],
                    target="presence-absence-item",
                    trigger="hover",
                ),
                html.Div(
                    [
                        html.P("Especie", className="input-description"),
                        dcc.Dropdown(id="fig-species-list-2", multi=False),
                    ],
                    className="input-group",
                ),
                dbc.Button("Ejecutar", size="sm", id="presence-absence", n_clicks=0),
            ],
            title="Presencia/Ausencia",
            id="presence-absence-item",
        ),
    ]
)

functions_box = dbc.Card(
    [
        dbc.CardHeader(
            [
                html.P("Funciones", className="title"),
                html.I(className="fas fa-info-circle", id="functions-info"),
                dbc.Tooltip(
                    """
                    Funciones para generar figuras o tablas a partir de la información
                    del proyecto cargado.
                """,
                    target="functions-info",
                ),
            ],
            class_name="card-header",
        ),
        dbc.CardBody(
            [
                dbc.Tabs(
                    [dbc.Tab(figures, label="Figuras"), dbc.Tab(tables, label="Tablas")]
                )
            ],
        ),
    ],
    class_name="w-100",
    id="function-box",
)

preview = dbc.Card(
    [
        dbc.CardHeader(
            [
                html.P("Resultados", className="title"),
                html.Div(
                    [
                        html.I(className="fas fa-info-circle", id="results-info"),
                        dbc.Tooltip(
                            """
                            Aparecen las figuras o tablas generadas con la posibilidad 
                            de descarga.
                        """,
                            target="results-info",
                        ),
                    ]
                ),
            ],
            class_name="card-header",
        ),
        dbc.CardBody(
            [
                dcc.Loading(
                    html.Div(
                        [
                            html.Div(
                                DataTable(id="data-table", export_format="xlsx"),
                                id="data-table-wrapper",
                            ),
                            html.Div(dcc.Graph(id="graph"), id="graph-wrapper",),
                        ],
                        id="preview-container",
                    )
                )
            ]
        ),
    ],
    class_name="h-100 w-100",
)

footer = html.Div(
    [
        html.P(
            """
            Desarrollado por el Programa de Evaluación y Monitoreo de la Biodiversidad - 
            Instituto de Investigación de Recursos Biológicos Alexander von Humboldt.
            """
        )
    ],
    className="text-muted h-100",
    id="footer",
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col([header], width=10, class_name="mh-100"),
                dbc.Col([logo], width=2, class_name="mh-100"),
            ],
            style={"height": "15vh"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    [data_box,
                    #video_box, 
                    functions_box],
                    width=4,
                    class_name="mh-100",
                    id="controls",
                ),
                dbc.Col([preview], width=8, class_name="mh-100"),
            ],
            style={"height": "95vh"},
        ),
        dbc.Row([dbc.Col([footer])], style={"height": "5vh"}),
        dcc.Store(id="store", storage_type="memory"),
    ]
)