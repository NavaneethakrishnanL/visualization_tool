import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import pandas as pd
import base64
import io

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("Tableau-Like Dashboard"),

    # File upload
    dcc.Upload(
        id="upload-data",
        children=html.Button("Upload CSV/Excel"),
        multiple=False,
        accept=".csv,.xlsx"
    ),

    html.Div(id="file-info"),
    dcc.Store(id="stored-data"),

    # Column selection dropdowns
    html.Label("Select X-axis:"),
    dcc.Dropdown(id="x-axis-dropdown"),

    html.Label("Select Y-axis:"),
    dcc.Dropdown(id="y-axis-dropdown"),

    # Date range filter
    dcc.DatePickerRange(id="date-picker", start_date=None, end_date=None),

    # Visualization and table
    dcc.Graph(id="data-visualization"),
    dash_table.DataTable(id="data-table")
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    if filename.endswith(".csv"):
        return pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    elif filename.endswith(".xlsx"):
        return pd.read_excel(io.BytesIO(decoded))
    return None

@app.callback(
    [Output("file-info", "children"),
     Output("stored-data", "data"),
     Output("data-table", "data"),
     Output("data-table", "columns"),
     Output("x-axis-dropdown", "options"),
     Output("y-axis-dropdown", "options")],
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")]
)
def upload_and_process(contents, filename):
    if contents is None:
        return "", None, [], [], [], []
    df = parse_contents(contents, filename)
    columns = [{"name": col, "id": col} for col in df.columns]
    data = df.to_dict("records")
    options = [{"label": col, "value": col} for col in df.columns]
    return f"Uploaded: {filename}", df.to_dict(), data, columns, options, options

@app.callback(
    Output("data-visualization", "figure"),
    [Input("x-axis-dropdown", "value"),
     Input("y-axis-dropdown", "value"),
     Input("stored-data", "data")]
)
def update_chart(x_col, y_col, data):
    if x_col and y_col and data:
        df = pd.DataFrame(data)
        fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
        return fig
    return px.scatter()

if __name__ == "__main__":
    app.run(debug=True)
