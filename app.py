#!/usr/bin/env python

# -*- coding: utf-8 -*-

import base64 as _base64
import functools as _functools
import io as _io

import numpy as _np
import pandas as _pd

import plotly as _py
import plotly.express as _px

import dash as _dash
import dash.dcc as _dcc
import dash.dependencies as _dep
import dash.exceptions as _exc
import dash.html as _html
import dash_bootstrap_components as _dbc

_app = _dash.Dash(
    __name__,
    title = 'New Testing App',
    external_stylesheets = [
        r"https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.css"
    ],
    external_scripts = [
        r"https://polyfill.io/v3/polyfill.js?features=default%2Ces5%2Ces6%2Ces2015%2Ces7%2Ces2016%2Ces2017%2Ces2018%2Ces2019%2CIntl%2Cblissfuljs%2CNumber.MIN_SAFE_INTEGER%2CNumber.MAX_SAFE_INTEGER%2CNumber.EPSILON%2CNumber.Epsilon%2CNumber.isNaN%2CNumber.isFinite%2CNumber.isInteger%2CNumber.isSafeInteger%2CNumber.parseInt%2CNumber.parseFloat",
        r"https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.js",
        r"https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.js",
        r"https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.js"
    ]
)

_app.layout = _dbc.Container(
    children = [
        _html.Header(
            children = [
                _dbc.Navbar(
                    _dbc.NavbarBrand(
                        children = [
                            _html.Img(
                                src = \
                                    r"https://upload.wikimedia.org/wikipedia/commons/0/05/Inkscape_radial_gradient_test%3B_red_displayed_as_green.svg",
                                alt = \
                                    "Example Business Company Logo – Image " +
                                        "Source: Wikimedia Commons <" +
                                        r"http://commons.wikimedia.org/" +
                                        ">, Author: Watchduck <" +
                                        r"http://commons.wikimedia.org/wiki/User:Watchduck" +
                                        ">",
                                title = \
                                    "Example Business Company Logo – Image " +
                                        "Source: Wikimedia Commons <" +
                                        r"http://commons.wikimedia.org/" +
                                        ">, Author: Watchduck <" +
                                        r"http://commons.wikimedia.org/wiki/User:Watchduck" +
                                        ">",
                                className = \
                                    'd-inline-block align-text-bottom me-3',
                                height = 42
                            ),
                            _html.H1(
                                'New Testing App',
                                className = 'd-inline-block align-text-center'
                            )
                        ],
                        href = r"#",
                        className = 'p-3'
                    ),
                    light = True
                )
            ],
            className = 'mb-4'
        ),

        _html.Section(
            children = [
                _html.H3('Input', id = 'input'),
                _dbc.Card(
                    children = [
                        _dbc.CardHeader(
                            _html.Span(
                                'Upload Table',
                                className = 'card-title'
                            )
                        ),
                        _dbc.CardBody(
                            _dbc.Form(
                                prevent_default_on_submit = True,
                                children = _dcc.Upload(
                                    id = 'data-frame-upload',
                                    children = [
                                        _html.Span('Drag and drop or '),
                                        _html.A('click to select'),
                                        _html.Span(' a file.')
                                    ],
                                    multiple = False,
                                    className = 'form-control form-control-lg'
                                )
                            )
                        )
                    ],
                    className = 'mb-3'
                ),

                _html.H3('Output', id = 'output'),
                _html.Table(
                    id = 'data-frame-table',
                    className = \
                        'table table-light table-striped table-bordered'
                ),
                _html.Figure(id = 'data-figure', className = 'figure container container-fluid')
            ],
            className = 'mt-4 mb-4'
        ),

        _html.Footer(
            _html.Div(
                children = [
                    "© 2022 Copyright: ",
                    _html.A(
                        'Example Business Company Ltd.',
                        href = r"http://localhost/",
                        title = 'Example Business Company Ltd.',
                        target = '_blank',
                        className = 'text-dark'
                    )
                ],
                className = 'p-3 text-center'
            ),
            className = 'mt-4 bg-light text-center text-lg-start text-muted'
        ),

        _dcc.Store(id = 'data-frame-store', storage_type = 'session')
    ]
)

@_app.callback(
    _dep.Output('data-frame-store', 'data'),
    _dep.Output('data-frame-table', 'children'),
    _dep.Output('data-figure', 'children'),

    _dep.Input('data-frame-upload', 'contents'),

    _dep.State('data-frame-store', 'data')
)
def _upload_data_frame (contents, df):
    if df is None:
        if not _dash.callback_context.triggered or contents is None:
            raise _exc.PreventUpdate()

        content_type, content_string = contents.split(',')
        content_type = content_type.split(';')
        content_decoded = _base64.b64decode(content_string)

        read = None
        if (
            "data:application/" \
                    "vnd.openxmlformats-officedocument.spreadsheetml.sheet" in
                content_type
        ):
            read = _functools.partial(
                _pd.read_excel,
                header = 0,
                index_col = 0
            )
        else:
            read = _functools.partial(
                _pd.read_csv,
                sep = ';',
                header = 0,
                index_col = 0,
                decimal = ',',
                encoding = 'utf-8'
            )

        with _io.BytesIO(content_decoded) as content_input:
            df = read(content_input)
    else:
        df = _pd.DataFrame.from_dict(df)

    table = [
        _html.Caption('The uploaded table', className = 'table-caption'),

        _html.Thead(
            children = _html.Tr(
                children = [
                    _html.Th(
                        children = df.index.name,
                        scope = 'col',
                        className = 'text-center'
                    )
                ] + list(
                    _html.Th(
                        children = col,
                        scope = 'col',
                        className = 'text-center'
                    ) for col in df.columns
                )
            ),
            className = 'thead thead-dark'
        ),
        _html.Tbody(
            children = list(
                _html.Tr(
                    children = [
                        _html.Th(
                            children = ind,
                            scope = 'row',
                            className = 'text-center'
                        )
                    ] + list(
                        _html.Td(
                            children = df.loc[ind, col],
                            className = \
                                'text-end' if _np.issubdtype(
                                    df[col].dtype,
                                    _np.number
                                ) else 'text-center'
                        ) for col in df.columns
                    )
                ) for ind in df.index
            )
        )
    ]

    figure = [
        _html.Figcaption('Graphical illustration of the uploaded table'),

        _dcc.Graph(
            figure = _px.bar(data_frame = df, title = 'Bar Plot'),
            className = 'figure-img img-fluid'
        )
    ]

    return (df.to_dict(), table, figure)

if __name__ == '__main__':
    _app.run_server(debug = True)
