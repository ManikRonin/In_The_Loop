import plotly.graph_objects as go

# TODO: move layout setting from functions and into a variable outside


def current_stock_performance(daily_data):
    """
    :param daily_data
    (type: pandas DataFrame)
    Accepts daily_data to determine the delta value for the current stock's performance
    yesterday

    :return: delta
    (type: float)
    returns the delta value to be used in the stock's graph's title
    """
    yesterday_open = float(daily_data["OPEN"][0])
    yesterday_close = float(daily_data["CLOSE"].iloc[-1])

    # Figuring out the delta % for the stock
    delta = round(((float(yesterday_close) - float(yesterday_open))/(float(yesterday_open)))*100, 3)
    return delta


def performance_colour(delta):
    """
    :param delta
    (type: float)

    :return: colour
    Change text colour in graph headings to correspond to tinker value +/-
    """

    if delta > 0:
        colour = "Green"
    else:
        colour = "Red"

    return colour

# ******************* PLOTLY GRAPHS ******************* #
# ----------------------------------------------------- #


# ******************* CANDLE GRAPH ******************* #
def presentation_daily_candle_graph(weekly_data, delta, colour, symbol):
    """
    :param weekly_data
    (type: pandas DataFrame)
    The data to be used for graphing

    :param delta
    (type: float)
    The value displayed by the graph to present value increase between yesterday's open and close

    :param colour
    (type: str)
    Depending on the delta, the graph will display the % delta in either red or green (neg- or pos+)

    :param symbol
    (type: str)
    The stock ticker symbol to be displayed by the graph

    :return:
    Plotly graph object
    Plotly Candle Graph (Red & Green Color) for the prior day in 30min intervals
    May be analysed to determine possible price movement based on past patterns
    Four price points: (open, high, low and close)
    """
    fig = go.Figure(data=[go.Candlestick(
        x=weekly_data['DATE'],
        open=weekly_data['OPEN'],
        high=weekly_data['HIGH'],
        low=weekly_data['LOW'],
        close=weekly_data['CLOSE']
        )])

    # Create Readable Date format for title
    relevant_date = weekly_data['DATE'].iloc[-1].date().strftime("%B %d, %Y")

    fig.update_layout(
        width=1100,
        height=400,
        title=f'{symbol} '
              + f'<span style="font-size: 18px; color: {colour}">{delta}%</span>'
              + f'<span style="font-size: 13px;"> {relevant_date}</span>',
        title_font={'size': 20, 'color': 'LightSeaGreen'},
        paper_bgcolor='rgba(0,0,0,1)',
        plot_bgcolor='rgba(0,0,0,0)',
        )

    fig.update_xaxes(
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            # dict(bounds=[17, 9.5], pattern="hour"),  # hide hours outside of 9.30am-5pm
            dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
        ],
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        linewidth=3,
        linecolor='rgba(52,61,70,1)',
        gridwidth=1,
        gridcolor='rgba(52,61,70,1)',
        showline=True,
        showgrid=True,
        title_text='Created With Weekly Data',
        title_font={'size': 15},
        color='LightSeaGreen',
        )

    fig.update_yaxes(
        linewidth=3,
        linecolor='rgba(52,61,70,1)',
        gridwidth=1,
        gridcolor='rgba(52,61,70,1)',
        showline=True,
        showgrid=True,
        title_text=f'{symbol} in USD',
        title_font={'size': 15},
        color='LightSeaGreen',

    )
    return fig


# ******************* MAIN PAGE DAILY GRAPH ******************* #
def presentation_daily_line_graph(daily_data, delta, colour, symbol):
    """
    :param daily_data
    (type: pandas DataFrame)
    The data to be used for graphing

    :param delta
    (type: float)
    The value displayed by the graph to present value increase between yesterday's open and close

    :param colour
    (type: str)
    Depending on the delta, the graph will display the % delta in either red or green (neg- or pos+)

    :param symbol
    (type: str)
    The stock ticker symbol to be displayed by the graph

    :return:
    Plotly line graph object ('Purple' Color graph with 'LightSeaGreen' labels) for the prior day
    Displays closing price for yesterday's market values in intervals of 5 minutes (extended to 8pm market close)
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily_data['DATE/TIME'],
        y=daily_data['CLOSE'],
        fill='tonexty',
        line={
            'color': 'purple'
        }
    ))

    # Create Readable Date format for title
    relevant_date = daily_data['DATE/TIME'].iloc[-1].date().strftime("%B %d, %Y")

    fig.update_layout(
        width=1100,
        height=400,
        autotypenumbers='convert types',
        title=f'{symbol} at Close '
              + f'<span style="font-size: 18px; color: {colour}">{delta}%</span>'
              + '<span style="font-size: 13px;"> (Extended Close Time)</span>' + '<br>'
              + f'<span style="font-size: 13px;">{relevant_date}</span>' + '<br>',
        title_font={'size': 20, 'color': 'LightSeaGreen'},
        paper_bgcolor='rgba(0,0,0,1)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    fig.update_xaxes(
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[17, 9.5], pattern="hour"),  # hide hours outside of 9.30am-5pm
            dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
        ],
        linewidth=3,
        linecolor='rgba(52,61,70,1)',
        gridwidth=1,
        gridcolor='rgba(52,61,70,1)',
        showline=True,
        showgrid=True,
        title_text='5-Minute Intervals',
        title_font={'size': 12},
        color='LightSeaGreen',
    )

    fig.update_yaxes(
        linewidth=3,
        linecolor='rgba(52,61,70,1)',
        gridwidth=1,
        gridcolor='rgba(52,61,70,1)',
        showline=True,
        showgrid=True,
        title_text=f'{symbol} in USD',
        title_font={'size': 12},
        color='LightSeaGreen',
        range=[round(float(daily_data.HIGH.min())-1), round(float(daily_data.HIGH.max()))],
    )
    return fig


# ******************* LONG TERM GRAPH ******************* #
def presentation_weekly_line_graph(weekly_data, delta, colour, symbol):
    """
    :param weekly_data
    (type: pandas DataFrame)
    The data to be used for graphing

    :param delta
    (type: float)
    The value displayed by the graph to present value increase between yesterday's open and close

    :param colour
    (type: str)
    Depending on the delta, the graph will display the % delta in either red or green (neg- or pos+)

    :param symbol
    (type: str)
    The stock ticker symbol to be displayed by the graph

    :return:
    Plotly graph object
    Plotly line Graph ('LightSeaGreen' Color graph with 'Purple' labels)
    This graph displays MTD, 6ttm, YTD & 1Year graphs using weekly_data from stock_canon_data.py
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=weekly_data['DATE'],
        y=weekly_data['CLOSE'],
        fill='tonexty',
        line={
            'color': 'cyan'
        }
    ))

    # Create Readable Date format for title
    relevant_date = weekly_data['DATE'].iloc[-1].date().strftime("%B %d, %Y")

    fig.update_layout(
        width=1100,
        height=400,
        autotypenumbers='convert types',
        title=f'{symbol} '
              + f'<span style="font-size: 18px; color: {colour}">{delta}%</span>'
              + '<span style="font-size: 13px;"> (Extended Close Time)</span>'
              + f'<span style="font-size: 13px;"> {relevant_date}</span>',
        title_font={'size': 20, 'color': 'purple'},
        paper_bgcolor='rgba(0,0,0,1)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    fig.update_xaxes(
        linewidth=3,
        linecolor='rgba(52,61,70,1)',
        gridwidth=1,
        gridcolor='rgba(52,61,70,1)',
        showline=True,
        showgrid=True,
        title_text='Created with Weekly Data',
        title_font={'size': 15},
        color='purple',
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig.update_yaxes(
        linewidth=3,
        linecolor='rgba(52,61,70,1)',
        gridwidth=1,
        gridcolor='rgba(52,61,70,1)',
        showline=True,
        showgrid=True,
        title_text=f'{symbol} Closing Price in USD',
        title_font={'size': 15},
        color='purple',
        range=[round(float(weekly_data.HIGH.min())-1), round(float(weekly_data.HIGH.max())+1)],
    )
    return fig
