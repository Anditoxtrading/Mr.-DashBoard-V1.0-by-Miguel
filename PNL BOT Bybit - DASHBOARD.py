from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from pybit.unified_trading import HTTP
from datetime import datetime
import config

# Configuración de la sesión de Bybit
session = HTTP(
    testnet=False,
    api_key=config.api_key,
    api_secret=config.api_secret,
)

# Inicialización de la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Bybit Futures Dashboard"

# Layout del Dashboard
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Mr. DashBoard"), className="mb-4")),
    dbc.Row([
        dbc.Col(dcc.Input(id="start-date", type="text", placeholder="Fecha inicial (YYYY-MM-DD)", className="mb-3")),
        dbc.Col(dcc.Input(id="end-date", type="text", placeholder="Fecha final (YYYY-MM-DD)", className="mb-3")),
        dbc.Col(dbc.Button("Consultar PnL", id="submit-button", color="primary", className="mb-3"))
    ]),
    dbc.Row(dbc.Col(html.Div(id="results"))),
    dbc.Row([
        dbc.Col(dcc.Graph(id="pnl-pie-chart"), width=6),
        dbc.Col(dcc.Graph(id="pnl-bar-chart"), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="top-coins-wheel"), width=6),
        dbc.Col(dcc.Graph(id="pnl-line-chart"), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="longest-trades"), width=6),
        dbc.Col(dcc.Graph(id="fastest-trades"), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="hourly-pnl-chart"), width=6),
        dbc.Col(dcc.Graph(id="weekday-pnl-chart"), width=6)
    ])
])

# Callback para manejar la consulta de PnL y actualizar los gráficos
@app.callback(
    [Output("results", "children"),
     Output("pnl-pie-chart", "figure"),
     Output("pnl-bar-chart", "figure"),
     Output("pnl-line-chart", "figure"),
     Output("top-coins-wheel", "figure"),
     Output("longest-trades", "figure"),
     Output("fastest-trades", "figure"),
     Output("hourly-pnl-chart", "figure"),
     Output("weekday-pnl-chart", "figure")],
    Input("submit-button", "n_clicks"),
    Input("start-date", "value"),
    Input("end-date", "value")
)
def update_dashboard(n_clicks, start_date, end_date):
    if n_clicks is None:
        return "", {}, {}, {}, {}, {}, {}, {}, {}

    if not start_date or not end_date:
        return dbc.Alert("Por favor, ingrese ambas fechas.", color="danger"), {}, {}, {}, {}, {}, {}, {}, {}

    try:
        start_time = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
        end_time = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)
    except ValueError:
        return dbc.Alert("Formato de fecha incorrecto. Use YYYY-MM-DD.", color="danger"), {}, {}, {}, {}, {}, {}, {}, {}

    total_pnl = 0
    total_pnl_positive = 0
    total_pnl_negative = 0
    won_trades = 0
    lost_trades = 0
    symbols_traded = set()
    pnl_by_symbol = {}
    cumulative_pnl_data = []
    trade_durations = []
    pnl_by_hour = {i: 0 for i in range(24)}
    pnl_by_weekday = {i: 0 for i in range(7)}

    while start_time < end_time:
        next_time = min(start_time + (7 * 24 * 60 * 60 * 1000), end_time)
        response = session.get_closed_pnl(category="linear", startTime=start_time, endTime=next_time, limit=100)
        
        if response["retCode"] != 0:
            return dbc.Alert(f"Error en la API: {response['retMsg']}", color="danger"), {}, {}, {}, {}, {}, {}, {}, {}
        
        trades = response["result"]["list"]

        for trade in trades:
            pnl = float(trade["closedPnl"])
            symbol = trade["symbol"]
            created_time = int(trade["createdTime"])
            updated_time = int(trade["updatedTime"])
            date = datetime.fromtimestamp(created_time / 1000)
            
            duration = (updated_time - created_time) / 60000
            trade_durations.append({
                "symbol": symbol,
                "duration": duration,
                "pnl": pnl,
                "entry_time": datetime.fromtimestamp(created_time / 1000).strftime("%Y-%m-%d %H:%M"),
                "exit_time": datetime.fromtimestamp(updated_time / 1000).strftime("%Y-%m-%d %H:%M")
            })

            cumulative_pnl_data.append({
                "date": date,
                "pnl": pnl
            })

            symbols_traded.add(symbol)
            total_pnl += pnl
            
            if pnl > 0:
                total_pnl_positive += pnl
                won_trades += 1
            else:
                total_pnl_negative += pnl
                lost_trades += 1

            if symbol in pnl_by_symbol:
                pnl_by_symbol[symbol] += pnl
            else:
                pnl_by_symbol[symbol] = pnl

            pnl_by_hour[date.hour] += pnl
            pnl_by_weekday[date.weekday()] += pnl

        start_time = next_time

    # Procesar datos para gráficos
    cumulative_pnl_data.sort(key=lambda x: x["date"])
    cumulative_pnl = []
    current_total = 0
    dates = []
    for entry in cumulative_pnl_data:
        current_total += entry["pnl"]
        cumulative_pnl.append(current_total)
        dates.append(entry["date"])

    # Crear tarjeta de resumen
    results = [
        dbc.Card([
            dbc.CardHeader("Resumen de PnL", style={'fontSize': '20px'}),
            dbc.CardBody([
                html.H4(f"Total PnL: {total_pnl:,.2f} USDT", className="card-title", style={'color': '#24b924'}),
                html.P(f"Operaciones ganadas: {won_trades}", className="card-text", style={'color': '#24b924'}),
                html.P(f"Operaciones perdidas: {lost_trades}", className="card-text", style={'color': '#ff4d4d'}),
                html.P(f"Monedas operadas: {', '.join(symbols_traded)}", className="card-text"),
                html.P(f"Suma PnL positivo: {total_pnl_positive:,.2f} USDT", style={'color': '#24b924'}),
                html.P(f"Suma PnL negativo: {total_pnl_negative:,.2f} USDT", style={'color': '#ff4d4d'})
            ])
        ], className="mb-4", style={'backgroundColor': '#1a1a1a'})
    ]

    # Crear gráfico de rueda
    sorted_coins = sorted(pnl_by_symbol.items(), key=lambda x: x[1], reverse=True)
    top_coins = [coin for coin in sorted_coins if coin[1] > 0][:10]
    wheel_labels = [coin[0] for coin in top_coins]
    wheel_values = [coin[1] for coin in top_coins]

    top_coins_wheel = px.pie(
        names=wheel_labels,
        values=wheel_values,
        title="Top 10 Monedas Más Rentables",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Plotly
    ).update_layout(
        template="plotly_dark",
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        font=dict(color='white'),
        title_font=dict(color='white', size=20),
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    top_coins_wheel.update_traces(
        textposition='inside',
        textinfo='label+value',
        hovertemplate="<b>%{label}</b><br>Ganancias: %{value:,.2f} USDT",
        texttemplate='%{label}<br>%{value:,.2f}',
        textfont=dict(color='white', size=14),
        marker=dict(line=dict(color='#000000', width=1.5)),
        insidetextorientation='horizontal'
    )

    # Gráfico de pastel de distribución
    pnl_pie_chart = px.pie(
        names=["Ganancias", "Pérdidas"],
        values=[total_pnl_positive, abs(total_pnl_negative)],
        title="Distribución de Ganancias y Pérdidas",
        color_discrete_sequence=["#24b924", "#ff4d4d"]
    ).update_layout(
        template="plotly_dark",
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        font=dict(color='white'),
        title_font=dict(color='white', size=20),
        legend=dict(
            font=dict(color='white', size=14),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    pnl_pie_chart.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Porcentaje: %{percent}<br>Valor: %{value:,.2f} USDT",
        textfont=dict(color='white', size=14),
        marker=dict(line=dict(color='#000000', width=2))
    )

    # Gráfico de barras
    pnl_bar_chart = go.Figure(
        data=[go.Bar(
            x=list(pnl_by_symbol.keys()),
            y=list(pnl_by_symbol.values()),
            marker_color=["#24b924" if pnl > 0 else "#ff4d4d" for pnl in pnl_by_symbol.values()]
        )],
        layout=go.Layout(
            title="PnL por Símbolo",
            xaxis=dict(title="Símbolo", color='white'),
            yaxis=dict(title="PnL (USDT)", color='white'),
            template="plotly_dark",
            paper_bgcolor='#000000',
            plot_bgcolor='#000000'
        )
    )

    # Gráfico de línea con área sombreada
    pnl_line_chart = go.Figure(
        data=[
            # Línea principal
            go.Scatter(
                x=dates,
                y=cumulative_pnl,
                mode='lines',
                line=dict(color='#24b924', width=3),
                name='PnL',
                hoverinfo='x+y'
            ),
            # Área sombreada
            go.Scatter(
                x=dates,
                y=cumulative_pnl,
                mode='none',
                fill='tozeroy',
                fillcolor='rgba(36, 185, 36, 0.5)',  # #24b924 con 50% de transparencia
                hoverinfo='skip',
                showlegend=False
            )
        ],
        layout=go.Layout(
            title="Evolución Acumulada del PnL",
            xaxis=dict(title="Fecha", color='white'),
            yaxis=dict(title="PnL Acumulado (USDT)", color='white'),
            template="plotly_dark",
            hovermode="x unified",
            paper_bgcolor='#000000',
            plot_bgcolor='#000000'
        )
    )

    # Gráficos de duración de operaciones
    sorted_by_duration = sorted(trade_durations, key=lambda x: x["duration"], reverse=True)
    top_longest = sorted_by_duration[:5]
    top_fastest = sorted(sorted_by_duration, key=lambda x: x["duration"])[:5]

    longest_trades_chart = go.Figure(
        data=[go.Bar(
            x=[f"{trade['symbol']}\n({trade['entry_time']})" for trade in top_longest],
            y=[trade['duration'] for trade in top_longest],
            text=[f"{trade['duration']:.1f} min" for trade in top_longest],
            textposition='auto',
            marker_color='#1a96ff',
            hovertext=[
                f"Símbolo: {trade['symbol']}<br>Duración: {trade['duration']:.1f} min<br>"
                f"Entrada: {trade['entry_time']}<br>Salida: {trade['exit_time']}<br>"
                f"PnL: {trade['pnl']:.2f} USDT"
                for trade in top_longest
            ]
        )],
        layout=go.Layout(
            title="Top 5 Operaciones Más Largas",
            xaxis=dict(title="Símbolo y Fecha de Entrada", color='white'),
            yaxis=dict(title="Duración (minutos)", color='white'),
            template="plotly_dark",
            paper_bgcolor='#000000',
            plot_bgcolor='#000000'
        )
    )

    fastest_trades_chart = go.Figure(
        data=[go.Bar(
            x=[f"{trade['symbol']}\n({trade['entry_time']})" for trade in top_fastest],
            y=[trade['duration'] for trade in top_fastest],
            text=[f"{trade['duration']:.1f} min" for trade in top_fastest],
            textposition='auto',
            marker_color='#f7a949',
            hovertext=[
                f"Símbolo: {trade['symbol']}<br>Duración: {trade['duration']:.1f} min<br>"
                f"Entrada: {trade['entry_time']}<br>Salida: {trade['exit_time']}<br>"
                f"PnL: {trade['pnl']:.2f} USDT"
                for trade in top_fastest
            ]
        )],
        layout=go.Layout(
            title="Top 5 Operaciones Más Rápidas",
            xaxis=dict(title="Símbolo y Fecha de Entrada", color='white'),
            yaxis=dict(title="Duración (minutos)", color='white'),
            template="plotly_dark",
            paper_bgcolor='#000000',
            plot_bgcolor='#000000'
        )
    )

    # Gráficos de rendimiento por hora y día de la semana
    hourly_pnl_chart = px.bar(
        x=list(pnl_by_hour.keys()),
        y=list(pnl_by_hour.values()),
        labels={'x': 'Hora del Día', 'y': 'PnL (USDT)'},
        title='Rendimiento por Hora del Día',
        color_discrete_sequence=['#a351c5']
    ).update_layout(template="plotly_dark", paper_bgcolor='#000000', plot_bgcolor='#000000')
    
    weekday_pnl_chart = px.bar(
        x=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
        y=[pnl_by_weekday[i] for i in range(7)],
        labels={'x': 'Día de la Semana', 'y': 'PnL (USDT)'},
        title='Rendimiento por Día de la Semana',
        color_discrete_sequence=['#ff4d4d']
    ).update_layout(template="plotly_dark", paper_bgcolor='#000000', plot_bgcolor='#000000')

    return (results, pnl_pie_chart, pnl_bar_chart, pnl_line_chart, 
            top_coins_wheel, longest_trades_chart, fastest_trades_chart,
            hourly_pnl_chart, weekday_pnl_chart)

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)