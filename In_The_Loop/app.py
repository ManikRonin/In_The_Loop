import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from news import *
from stock_description import *
from stock_graphs import *
from stock_data_canon import *
from symbol import get_symbol

# ******************* SET UP ******************* #
# ---->Set up your personal API key from url = https://www.alphavantage.co/
my_alpha_vantage = 'ENTER YOUR ALPHA VANTAGE API KEY HERE'

# ---->Set up your personal API key from url = https://newsapi.org
my_news_api = 'ENTER YOUR NEWS API KEY HERE'  # Enter News API key

# ---->Set up your personal API key from url = https://financialmodelingprep.com/developer/docs/
my_financial_mp = 'ENTER YOUR FINANCIAL MP API KEY HERE'  # Enter FinancialModelingPrep API key

# ******************* GETTING DATA FOR GRAPHS ******************* #
symbol = get_symbol()

try:
    daily_data = presentation_daily_data(symbol=symbol, my_alpha_vantage=my_alpha_vantage)
    weekly_data = presentation_weekly_data(symbol, my_alpha_vantage)

except KeyError:
    raise Exception('Wait a full minute between changing the Stock Symbol on symbol.py \n'
                    'This is due to limitations set forth by the API')

delta = current_stock_performance(daily_data)
colour = performance_colour(delta)

# ******************* DRAWING GRAPHS ******************* #
candle = presentation_daily_candle_graph(weekly_data, delta, colour, symbol)
main = presentation_daily_line_graph(daily_data, delta, colour, symbol)
long = presentation_weekly_line_graph(weekly_data, delta, colour, symbol)

# Labels To Easily Add to Dash Layout
fig_candle = candle
fig_main = main
fig_long = long

# ******************* GETTING DATA FOR NEWS + OTHER INFO ******************* #
stock_news = new_report(symbol, my_news_api)
news_image = stock_news.Image
news_title = stock_news.Title
news_blurb = stock_news.Description
news_source = stock_news.URL
overview = company(symbol, my_financial_mp)
description = overview['Current'][13]  # Taken from last row of company()
overview.drop(overview.tail(1).index, inplace=True)  # Removes the description from df, to use the rest of table as is

# ******************* BUILDING A SEXY DASHBOARD ******************* #
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Mother Div
app.layout = html.Div(
    className='main',
    children=[

        # ************ START OF HEADER ************ #
        # --- Logo --- #

        html.Div(
            className='logo_container',
            children=[
                html.Img(src=app.get_asset_url('Title_Financial.png'),
                         style={
                             'height': '30%',
                             'width': '30%',
                             'margin-left': '30px',
                             'position': 'relative'
                         }),
            ]),

        html.H2(
            children=[f'{overview["Current"][0]}']),

        # --- Graph 1 and Quick Facts Table --- #
        html.Div(
            className='header row',

            children=[
                # --- Graph 1 --- #
                html.Div(
                    className='mainGraph col-lg-6 col-md-12',
                    children=[dcc.Graph(responsive=True, figure=fig_main)]
                ),

                # --- Quick Facts Table --- #
                html.Div(
                    className='stockData col-lg-6 col-md-12',
                    children=[
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in overview.columns],
                            data=overview.to_dict('records'),
                            style_cell=dict(
                                textAlign='left',
                                fontSize='20',
                                fontFamily='sans-serif',
                                color='White'
                            ),
                            style_header=dict(
                                backgroundColor="LightSeaGreen"
                            ),
                            style_data=dict(
                                backgroundColor="Black",
                            ),
                            style_table=dict(
                                border='1px solid LightSeaGreen',
                                borderRadius='15px',
                                overflow='hidden'
                            ),
                        ),
                    ]),

            ]),
        # ************</END> HEADER ************ #

        # ************ START OF NEWS SECTION 1 ************ #

        html.Div(
            style={
                'border-top': '3px dashed Purple',
                'border-bottom': '3px dashed LightSeaGreen',
                'backgroundColor': '#0B0522',
                'padding': '0px 200px'
            },
            children=[
                html.H2(
                    style={'color': 'white'},
                    children=['Latest News:']),

                # --- Latest News Section #1 --- #
                html.Div(
                    className='news_stand row',
                    style={
                        'backgroundColor': '#0B0522',
                    },
                    children=[
                        # --- Article #1 Container --- #
                        html.Div(
                            className='article_container',
                            children=[
                                # --- Article #1 --- #
                                html.Div(
                                    className='news_article',
                                    style={'border-color': '#1BFF1B'},
                                    children=[
                                        html.Tr(
                                            html.Img(
                                                src=f'{news_image[0]}',
                                                alt=f'Latest {symbol} News'
                                            )),
                                        html.Tr(
                                            html.A(
                                                href=news_source[0],
                                                target='_blank',
                                                children=f'{news_title[0][slice(48)]}...',
                                            )),
                                        html.Tr(
                                            html.P(
                                                className='news_text',
                                                children=f'{news_blurb[0][slice(120)]}...',
                                            )),
                                    ])
                                # --- </END> Article #1 --- #

                            ]),
                        # --- </END>Article #1 Container --- #

                        # --- Article #2 Container --- #
                        html.Div(
                            className='article_container',
                            children=[
                                # --- Article #2 --- #
                                html.Div(
                                    className='news_article',
                                    style={'border-color': '#0080FF'},
                                    children=[
                                        html.Tr(
                                            html.Img(
                                                src=f'{news_image[1]}',
                                                alt=f'Latest {symbol} News'
                                            )),
                                        html.Tr(
                                            html.A(
                                                href=news_source[1],
                                                target='_blank',
                                                children=f'{news_title[1][slice(48)]}...',
                                            )),
                                        html.Tr(
                                            html.P(
                                                className='news_text',
                                                children=f'{news_blurb[1][slice(120)]}...',
                                            )),
                                    ])
                                # --- </END> Article #2 --- #

                            ]),
                        # --- </END>Article #2 Container --- #

                        # --- Article #3 Container --- #
                        html.Div(
                            className='article_container',
                            children=[
                                # --- Article #3 --- #
                                html.Div(
                                    className='news_article',
                                    style={'border-color': '#FF74D3'},
                                    children=[
                                        html.Tr(
                                            html.Img(
                                                src=f'{news_image[2]}',
                                                alt=f'Latest {symbol} News'
                                            )),
                                        html.Tr(
                                            html.A(
                                                href=news_source[2],
                                                target='_blank',
                                                children=f'{news_title[2][slice(48)]}...',
                                            )),
                                        html.Tr(
                                            html.P(
                                                className='news_text',
                                                children=f'{news_blurb[2][slice(120)]}...',
                                            )),
                                    ])
                                # --- </END> Article #3 --- #

                            ]),
                        # --- </END>Article #3 Container --- #

                    ]),
            ]),
        # --- </END> Latest News Section #1 --- #
        # ************ </END> START OF NEWS SECTION 1 ************ #

        # ************ START OF DESCRIPTION AND TWO GRAPHS ************ #
        html.Div(
            children=[

                # --- Description --- #
                html.Div(
                    className='description',
                    children=[
                        # --- Description Title --- #
                        html.H3(
                            children=f'Quick Glance at "{overview["Current"][0]}":',

                        ),

                        # --- Description Text --- #
                        html.P(
                            children=f'{description}'
                        )
                    ]
                ),
                # --- </END> Description --- #

                # --- Graphs 2 & 3 --- #
                html.Div(
                    style={
                        'padding': '0px 60px 0px'
                    },
                    children=[
                        # --- Graph 2 --- #
                        html.Div(
                            children=[dcc.Graph(responsive=True, figure=fig_candle)]
                        ),
                        # --- Graph 3 --- #
                        html.Div(
                            children=[dcc.Graph(responsive=True, figure=fig_long)]
                        ),

                    ]),

                # --- </END> Graphs --- #

            ]),
        # ************ </END> START OF DESCRIPTION AND TWO GRAPHS ************ #

        # ************ START OF NEWS SECTION 2 ************ #

        html.Div(
            style={
                'border-top': '3px dashed Purple',
                'backgroundColor': '#0B0522',
                'padding': '0px 200px'
            },
            children=[
                html.H2(
                    style={
                        'color': 'white',
                    },
                    children=['Latest News:']),

                # --- Latest News Section #2 --- #
                html.Div(
                    className='news_stand row',
                    style={'backgroundColor': '#0B0522'},
                    children=[

                        # --- Article #4 Container --- #
                        html.Div(
                            className='article_container',
                            children=[
                                # --- Article #4 --- #
                                html.Div(
                                    className='news_article',
                                    style={'border-color': '#0080FF'},
                                    children=[
                                        html.Tr(
                                            html.Img(
                                                src=f'{news_image[3]}',
                                                alt=f'Latest {symbol} News'
                                            )),
                                        html.Tr(
                                            html.A(
                                                href=news_source[3],
                                                target='_blank',
                                                children=f'{news_title[3][slice(48)]}...',
                                            )),
                                        html.Tr(
                                            html.P(
                                                className='news_text',
                                                children=f'{news_blurb[3][slice(120)]}...',
                                            )),
                                    ])
                                # --- <END> Article #4 --- #

                            ]),
                        # --- <END>Article #4 Container --- #

                        # --- Article #5 Container --- #
                        html.Div(
                            className='article_container',
                            children=[
                                # --- Article #5 --- #
                                html.Div(
                                    className='news_article',
                                    style={'border-color': '#FF74D3'},
                                    children=[
                                        html.Tr(
                                            html.Img(
                                                src=f'{news_image[4]}',
                                                alt=f'Latest {symbol} News'
                                            )),
                                        html.Tr(
                                            html.A(
                                                href=news_source[4],
                                                target='_blank',
                                                children=f'{news_title[4][slice(48)]}...',
                                            )),
                                        html.Tr(
                                            html.P(
                                                className='news_text',
                                                children=f'{news_blurb[4][slice(120)]}...',
                                            )),
                                    ])
                                # --- <END> Article #5 --- #

                            ]),
                        # --- <END>Article #5 Container --- #

                        # --- Article #6 Container --- #
                        html.Div(
                            className='article_container',
                            children=[
                                # --- Article #6 --- #
                                html.Div(
                                    className='news_article',
                                    style={'border-color': '#1BFF1B'},
                                    children=[
                                        html.Tr(
                                            html.Img(
                                                src=f'{news_image[5]}',
                                                alt=f'Latest {symbol} News'
                                            )),
                                        html.Tr(
                                            html.A(
                                                href=news_source[5],
                                                target='_blank',
                                                children=f'{news_title[5][slice(48)]}...',
                                            )),
                                        html.Tr(
                                            html.P(
                                                className='news_text',
                                                children=f'{news_blurb[5][slice(120)]}...',
                                            )),
                                    ])
                                # --- <END> Article #6 --- #

                            ]),
                        # --- <END>Article #6 Container --- #

                    ]),
                # --- <END> Latest News Section #2 --- #
                # ************ </END>START OF NEWS SECTION 2 ************ #
            ]),
        html.Div(
            style={
                'textAlign': 'center',
                'backgroundColor': '#0f0f0f',
                'width': '100%',
                'position': 'relative'
            },
            children=[html.Img(src=app.get_asset_url('footer.png'),
                               style={
                                   'width': '15%',
                                   'height': '15%'
                               })
                      ],

        )

    ])

if __name__ == '__main__':
    app.run_server(debug=True)
