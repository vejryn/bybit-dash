import sys
import pybybit
from auth import key, secret

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import plotly
import plotly.graph_objs as go

class bybitDash:
    def __init__(self, api_key, secret_key):
        client = pybybit.API(key=api_key, secret=secret_key, testnet=False)
        self.store = pybybit.DataStore()
        
        client.ws.add_callback(self.store.onmessage)
        client.ws.run_forever_inverse(topics=['order'])
        
        self.fig = go.Figure()

        self.fig.add_trace(go.Indicator(
            mode = "number",
            value = 0,
            title = {"text" : "<span style='font-size:0.8em;color:gray'>Active Buy Orders</span>"},
            domain = {'x': [0, 0.5], 'y': [0, 0]}
        ))

        self.fig.add_trace(go.Indicator(
            mode = "number",
            value = 0,
            title = {"text": "<span style='font-size:0.8em;color:gray'>Active Sell Orders</span>"},
            domain = {'x': [0.6, 1], 'y': [0, 0]}
        ))

        self.app = dash.Dash()
        self.app.layout = html.Div(
            [
                dcc.Graph(id='live-indicator', animate=False, figure=self.fig),
                dcc.Interval(
                    id='indicator-update',
                    interval=1000, # updating every 1 second
                    n_intervals=0
                )
            ]
        )
        self.app.callback(
            Output('live-indicator', 'figure'),
            [Input('indicator-update', 'n_intervals')],
            [State('live-indicator', 'figure')]
            )(self.update_graph)
    def update_graph(self, n, m):
        self.active_buy = []
        self.active_sell = []
        self.orders = []
        self.orders = self.store.order.getlist(symbol='BTCUSD')
        for i in range(len(self.orders)):
            if self.orders[i]['side'] == 'Buy':
                self.active_buy.append(i)
            if self.orders[i]['side'] == 'Sell':
                self.active_sell.append(i)

        # updating indicator based on domain
        self.fig.update_traces(value=len(self.active_buy), selector=dict(domain={'x': [0, 0.5], 'y': [0, 0]}))
        self.fig.update_traces(value=len(self.active_sell), selector=dict(domain ={'x': [0.6, 1], 'y': [0, 0]}))

        return self.fig

def Main():
    dashboard = bybitDash(key, secret)
    dashboard.app.run_server(debug=True, host='127.0.0.1', port = 8050)

if __name__ == '__main__':
    Main()