import plotly.graph_objs as go
from plotly.subplots import make_subplots

from app.model import Prediction


class Visualization(Prediction):

    def __init__(self, exchange, interval, asset, indication, action_model, price_model, market=None):
        super().__init__(exchange, interval, asset, action_model, price_model, market)
        super(Visualization, self).get_prediction()
        super(Visualization, self).prediction_postprocessing(indication)

    def prediction_graph(self, equity=None):

        self.df_visualization = self.df_visualization.iloc[-450:]

        if equity == 'Index Fund' or equity == 'Futures & Commodities' or equity == 'Forex':
            prediction_title = f"{self.asset}."
        elif equity == 'Stock':
            prediction_title = f"{self.asset} to The {self.market}."
        else:
            prediction_title = f"{self.asset} to {self.market}."

        if self.df_visualization['Open'].iloc[-1] > self.df_visualization['Adj Close'].iloc[-1]:
            trace_color = 'rgba(255, 0, 0, 0.15)'
            price_tag = 'Bearish'
        else:
            trace_color = 'rgba(0, 128, 0, 0.15)'
            price_tag = 'Bullish'

        self.fig_action = make_subplots(specs=[[{"secondary_y": True}]])
        self.fig_action.add_trace(
            go.Scatter(x=self.df_visualization.index, y=self.df_visualization['Adj Close'], name=f"Price ({price_tag})",
                       connectgaps=False,
                       marker=dict(color='#000000'), fill='tozeroy', fillcolor=trace_color), secondary_y=False)

        self.fig_action.add_trace(
            go.Scatter(x=self.df_visualization.index, y=self.df_visualization['Price_Predictions'],
                       name="Predicted Price", connectgaps=False,
                       marker=dict(color='#A9A9A9'), visible="legendonly"), secondary_y=False)

        self.fig_action.add_trace(
            go.Scatter(x=self.df_visualization.index, y=self.df_visualization['Price_Buy'], mode='markers', name="Buy",
                       marker=dict(color='#32AB60', opacity=0.85, size=7.5)), secondary_y=False)
        self.fig_action.add_trace(
            go.Scatter(x=self.df_visualization.index, y=self.df_visualization['Price_Sell'], mode='markers',
                       name="Sell",
                       marker=dict(color='#DB4052', opacity=0.85, size=7.5)), secondary_y=False)
        self.fig_action.add_trace(
            go.Bar(x=self.df_visualization.index, y=self.df_visualization['Bullish Volume'], name="Bullish Volume",
                   opacity=0.2,
                   marker=dict(color='#008000')), secondary_y=True)
        self.fig_action.add_trace(
            go.Bar(x=self.df_visualization.index, y=self.df_visualization['Bearish Volume'], name="Bearish Volume",
                   opacity=0.2,
                   marker=dict(color='#D2042D')), secondary_y=True)

        self.fig_action.update_layout(autosize=False, height=750, dragmode=False, hovermode='x',
                                      plot_bgcolor='rgba(255, 255, 255, 0.88)',
                                      title=dict(text=prediction_title, y=0.95, x=0.5, xanchor='center', yanchor='top',
                                                 font=dict(size=20)),
                                      xaxis_range=(
                                      self.df_visualization.index.min(), self.df_visualization.index.max()),
                                      yaxis_range=(self.df_visualization['Adj Close'].min() - self.df_visualization[
                                          'Adj Close'].std() / 10,
                                                   self.df_visualization['Adj Close'].max() + self.df_visualization[
                                                       'Adj Close'].std() / 3))
        self.fig_action.update_xaxes(title_text="Date", zeroline=False, showline=False, showgrid=False, linewidth=2,
                                     rangeslider_visible=True)
        self.fig_action.update_yaxes(title_text="Price & Trading Action", secondary_y=False, showgrid=False,
                                     showline=False)
        self.fig_action.update_yaxes(title_text="Volume", secondary_y=True, showgrid=False, showline=False,
                                     visible=False)

        return self.fig_action

    def technical_analysis_graph(self):
        self.df_visualization_technical = self.df_visualization_technical.iloc[-450:]

        self.fig_analysis = make_subplots(rows=4, cols=1)
        self.fig_analysis.append_trace(
            go.Scatter(x=self.df_visualization_technical.index, y=self.df_visualization_technical['MACD'], name="MACD",
                       marker=dict(color='#2ECC71')), row=1, col=1)
        self.fig_analysis.append_trace(
            go.Scatter(x=self.df_visualization_technical.index, y=self.df_visualization_technical['MACDS'],
                       name="MACDS",
                       marker=dict(color='#E74C3C')), row=1, col=1)
        self.fig_analysis.append_trace(
            go.Bar(x=self.df_visualization_technical.index, y=self.df_visualization_technical['MACDH'], name="MACDH",
                   opacity=0.3,
                   marker=dict(color='#000000')), row=1, col=1)
        self.fig_analysis.add_shape(type='line', x0=self.df_visualization_technical.index.min(),
                                    x1=self.df_visualization_technical.index.max(),
                                    y0=0, y1=0, line=dict(color='#000000', width=0.5), row=1, col=1)

        self.fig_analysis.append_trace(
            go.Scatter(x=self.df_visualization_technical.index, y=self.df_visualization_technical['SR_RSI_K'],
                       name="Stochastic RSI K",
                       marker=dict(color='#F39C12')), row=2, col=1)
        self.fig_analysis.append_trace(
            go.Scatter(x=self.df_visualization_technical.index, y=self.df_visualization_technical['SR_RSI_D'],
                       name="Stochastic RSI D",
                       marker=dict(color='#3780BF')), row=2, col=1)
        self.fig_analysis.add_shape(type='line', x0=self.df_visualization_technical.index.min(),
                                    x1=self.df_visualization_technical.index.max(), y0=20, y1=20,
                                    line=dict(color='#008000', width=1), row=2, col=1)
        self.fig_analysis.add_shape(type='line', x0=self.df_visualization_technical.index.min(),
                                    x1=self.df_visualization_technical.index.max(), y0=80, y1=80,
                                    line=dict(color='#FF0000', width=1), row=2, col=1)

        self.fig_analysis.append_trace(
            go.Scatter(x=self.df_visualization_technical.index, y=self.df_visualization_technical['RSI'], name="RSI",
                       marker=dict(color='#A569BD')), row=3, col=1)
        self.fig_analysis.add_shape(type='line', x0=self.df_visualization_technical.index.min(),
                                    x1=self.df_visualization_technical.index.max(),
                                    y0=30, y1=30, line=dict(color='#008000', width=1), row=3, col=1)
        self.fig_analysis.add_shape(type='line', x0=self.df_visualization_technical.index.min(),
                                    x1=self.df_visualization_technical.index.max(),
                                    y0=70, y1=70, line=dict(color='#FF0000', width=1), row=3, col=1)

        self.fig_analysis.append_trace(
            go.Scatter(x=self.df_visualization_technical.index, y=self.df_visualization_technical['SR_K'],
                       name="Stochastic K",
                       marker=dict(color='#F39C12')), row=4, col=1)
        self.fig_analysis.append_trace(
            go.Scatter(x=self.df_visualization_technical.index, y=self.df_visualization_technical['SR_D'],
                       name="Stochastic D",
                       marker=dict(color='#3780BF')), row=4, col=1)
        self.fig_analysis.add_shape(type='line', x0=self.df_visualization_technical.index.min(),
                                    x1=self.df_visualization_technical.index.max(), y0=20, y1=20,
                                    line=dict(color='#008000', width=1), row=4, col=1)
        self.fig_analysis.add_shape(type='line', x0=self.df_visualization_technical.index.min(),
                                    x1=self.df_visualization_technical.index.max(), y0=80, y1=80,
                                    line=dict(color='#FF0000', width=1), row=4, col=1)

        self.fig_analysis.update_layout(autosize=False, height=750, dragmode=False, hovermode='x',
                                        plot_bgcolor='rgba(255, 255, 255, 0.88)',
                                        title=dict(text="Technical Indicators.", y=0.95, x=0.5, xanchor='center',
                                                   yanchor='top', font=dict(size=20)))
        self.fig_analysis.update_shapes(dict(opacity=0.7))
        self.fig_analysis.update_xaxes(showgrid=False, zeroline=False, showline=False)
        self.fig_analysis.update_xaxes(title_text="Date", row=4, col=1)
        self.fig_analysis.update_yaxes(showgrid=False, zeroline=False, showline=False)
        self.fig_analysis.update_yaxes(title_text="MACD", row=1, col=1)
        self.fig_analysis.update_yaxes(title_text="Stochastic RSI", range=[-1, 101], tickvals=[0, 20, 80, 100], row=2,
                                       col=1)
        self.fig_analysis.update_yaxes(title_text="RSI", range=[0, 100], tickvals=[0, 30, 70, 100], row=3, col=1)
        self.fig_analysis.update_yaxes(title_text="Slow Stochastic", range=[-1, 101], tickvals=[0, 20, 80, 100], row=4,
                                       col=1)

        return self.fig_analysis
