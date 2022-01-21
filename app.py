import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


df = pd.read_csv('df_final.csv')
df = df.drop(columns=['Unnamed: 0'])

df['quantity_purchased'] = df['quantity_purchased'].replace('-', '')
df['quantity_purchased'] = pd.to_numeric(df['quantity_purchased'])

top_products_overall = df.groupby('product').agg(
    {'quantity_purchased': 'sum'}).nlargest(5, 'quantity_purchased').reset_index()
bot_products_overall = df.groupby('product').agg(
    {'quantity_purchased': 'sum'}).nsmallest(5, 'quantity_purchased').reset_index()

top_products_region = df.groupby('region')['product'].value_counts().groupby(
    level=0).head(5).sort_values(ascending=False).to_frame('counts').reset_index()
bot_products_region = df.groupby('region')['product'].value_counts().groupby(
    level=0).tail(5).sort_values(ascending=False).to_frame('counts').reset_index()

top_products_county = df.groupby('county')['product'].value_counts().groupby(
    level=0).head(5).sort_values(ascending=False).to_frame('counts').reset_index()
bot_products_county = df.groupby('county')['product'].value_counts().groupby(
    level=0).tail(5).sort_values(ascending=False).to_frame('counts').reset_index()

merged_top = pd.concat([top_products_region, top_products_county]
                       ).reset_index().drop(columns=['index'])
merged_top = merged_top.fillna('')
merged_top['region/county'] = merged_top['region'] + merged_top['county']
merged_top = merged_top.drop(columns=['region', 'county'])

merged_bot = pd.concat([bot_products_region, bot_products_county]
                       ).reset_index().drop(columns=['index'])
merged_bot = merged_bot.fillna('')
merged_bot['region/county'] = merged_bot['region'] + merged_bot['county']
merged_bot = merged_bot.drop(columns=['region', 'county'])


top_cat_overall = df.groupby('category').agg(
    {'quantity_purchased': 'sum'}).nlargest(5, 'quantity_purchased').reset_index()
bot_cat_overall = df.groupby('category').agg(
    {'quantity_purchased': 'sum'}).nsmallest(5, 'quantity_purchased').reset_index()

top_cat_region = df.groupby('region')['category'].value_counts().groupby(
    level=0).head(5).sort_values(ascending=False).to_frame('counts').reset_index()
bot_cat_region = df.groupby('region')['category'].value_counts().groupby(
    level=0).tail(5).sort_values(ascending=False).to_frame('counts').reset_index()

top_cat_county = df.groupby('county')['category'].value_counts().groupby(
    level=0).head(5).sort_values(ascending=False).to_frame('counts').reset_index()
bot_cat_county = df.groupby('county')['category'].value_counts().groupby(
    level=0).tail(5).sort_values(ascending=False).to_frame('counts').reset_index()

merged_top_cat = pd.concat(
    [top_cat_region, top_cat_county]).reset_index().drop(columns=['index'])
merged_top_cat = merged_top_cat.fillna('')
merged_top_cat['region/county'] = merged_top_cat['region'] + \
    merged_top_cat['county']
merged_top_cat = merged_top_cat.drop(columns=['region', 'county'])

merged_bot_cat = pd.concat(
    [bot_cat_region, bot_cat_county]).reset_index().drop(columns=['index'])
merged_bot_cat = merged_bot_cat.fillna('')
merged_bot_cat['region/county'] = merged_bot_cat['region'] + \
    merged_bot_cat['county']
merged_bot_cat = merged_bot_cat.drop(columns=['region', 'county'])

top_branches_overall = df.groupby('branch_name').agg(
    {'amount_in_gbp': 'sum'}).nlargest(3, 'amount_in_gbp').reset_index()
bot_branches_overall = df.groupby('branch_name').agg(
    {'amount_in_gbp': 'sum'}).nsmallest(3, 'amount_in_gbp').reset_index()

top_branches_region = df.groupby(['branch_name', 'region']).agg(
    {'amount_in_gbp': 'sum'}).nlargest(3, 'amount_in_gbp').reset_index()
bot_branches_region = df.groupby(['branch_name', 'region']).agg(
    {'amount_in_gbp': 'sum'}).nsmallest(3, 'amount_in_gbp').reset_index()

top_branches_county = df.groupby(['branch_name', 'county']).agg(
    {'amount_in_gbp': 'sum'}).nlargest(3, 'amount_in_gbp').reset_index()
bot_branches_county = df.groupby(['branch_name', 'county']).agg(
    {'amount_in_gbp': 'sum'}).nsmallest(3, 'amount_in_gbp').reset_index()

merged_top_branches = pd.concat(
    [top_branches_region, top_branches_county]).reset_index().drop(columns=['index'])
merged_top_branches = merged_top_branches.fillna('')
merged_top_branches['region/county'] = merged_top_branches['region'] + \
    merged_top_branches['county']
merged_top_branches = merged_top_branches.drop(columns=['region', 'county'])

merged_bot_branches = pd.concat(
    [bot_branches_region, bot_branches_county]).reset_index().drop(columns=['index'])
merged_bot_branches = merged_bot_branches.fillna('')
merged_bot_branches['region/county'] = merged_bot_branches['region'] + \
    merged_bot_branches['county']
merged_bot_branches = merged_bot_branches.drop(columns=['region', 'county'])

colors = {
    'paper_bgcolor': '#1f2c56',
    'plot_bgcolor': '#1f2c56',
}


app = dash.Dash()
server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('Customer Behaviour'),
        ], className='one-Three column', id='title')

    ]),

    html.Div([
        html.Div([
            html.H3('Products Sold Overall', style={'margin-bottom': '30px'}),
            dcc.RadioItems(
                id='radio_item',
                options=[
                    {'label': 'Most Sold', 'value': str(
                        top_products_overall), },
                    {'label': 'Least Sold', 'value': str(
                        bot_products_overall)},

                ],
                value=str(top_products_overall),
                labelStyle={'display': 'inline-block'},
                inputStyle={'margin-right': '10px',
                            'margin-left': '20px', 'margin-bottom': '20px'}
            ),
            dcc.Graph(id='graph'),

        ], className='card-container six columns', id='title1', style={'padding-bottom' : '35px'}),

        html.Div([
            html.H3('Products Sold By Location',
                    style={'margin-bottom': '30px'}),
            dcc.RadioItems(
                id='top_products_radio_item',
                options=[
                    {'label': 'Most Sold', 'value': str(merged_top)},
                    {'label': 'Least Sold', 'value': str(merged_bot)},
                ],
                value=str(merged_top),
                labelStyle={'display': 'inline-block'},
                inputStyle={'margin-right': '10px',
                            'margin-left': '20px', 'margin-bottom': '20px'}
            ),
            dcc.Dropdown(
                id='top_products_dropdown',
                options=[
                    {'label': i, 'value': i} for i in merged_top['region/county'].unique()
                ],
                value='North West England',
            ),
            dcc.Graph(id='product_graph'),
        ], className='card-container six columns', id='title2')


    ]),
    html.Div([
        html.Div([
            html.H3('Categories Overall', style={'margin-bottom': '30px'}),
            dcc.RadioItems(
                id='cat_radio_item',
                options=[
                    {'label': 'Most Sold', 'value': str(top_cat_overall)},
                    {'label': 'Least Sold', 'value': str(
                        bot_cat_overall)},
                ],
                value=str(top_cat_overall),
                labelStyle={'display': 'inline-block'},
                inputStyle={'margin-right': '10px',
                            'margin-left': '20px', 'margin-bottom': '20px'}
            ),
            dcc.Graph(id='cat_graph'),

        ], className='card-container six columns', id='title3', style={'margin-top' : '30px', 'padding-bottom' : '35px'}),

        html.Div([
            html.H3('Categories By Location', style={'margin-bottom': '30px'}),
            dcc.RadioItems(
                id='top_cat_radio_item',
                options=[
                    {'label': 'Most Sold', 'value': str(merged_top_cat)},
                    {'label': 'Least Sold', 'value': str(merged_bot_cat)},
                ],
                value=str(merged_top_cat),
                labelStyle={'display': 'inline-block'},
                inputStyle={'margin-right': '10px',
                            'margin-left': '20px', 'margin-bottom': '20px'}
            ),
            dcc.Dropdown(
                id='top_cat_dropdown',
                options=[
                    {'label': i, 'value': i} for i in merged_top_cat['region/county'].unique()
                ],
                value='North West England'
            ),
            dcc.Graph(id='top_cat_graph'),
        ], className='card-container six columns', id='title4',style={'margin-top' : '30px'})
    ]),
    html.Div([
        html.Div([
            html.H3('Branches Overall', style={'margin-bottom': '30px'}),
            dcc.RadioItems(
                id='branches_radio_item',
                options=[
                    {'label': 'Most Sold', 'value': str(top_branches_overall)},
                    {'label': 'Least Sold', 'value': str(
                        bot_branches_overall)},
                ],
                value=str(top_branches_overall),
                labelStyle={'display': 'inline-block'},
                inputStyle={'margin-right': '10px',
                            'margin-left': '20px', 'margin-bottom': '20px'}
            ),
            dcc.Graph(id='branches_graph'),

        ], className='card-container six columns', id='title5', style={'margin-top' : '30px', 'padding-bottom' : '35px'}),

        html.Div([
            html.H3('Branches By Location', style={'margin-bottom': '30px'}),
            dcc.RadioItems(
                id='top_branches_radio_item',
                options=[
                    {'label': 'Most Sold', 'value': str(merged_top_branches)},
                    {'label': 'Least Sold', 'value': str(merged_bot_branches)},
                ],
                value=str(merged_top_branches),
                labelStyle={'display': 'inline-block'},
                inputStyle={'margin-right': '10px',
                            'margin-left': '20px', 'margin-bottom': '20px'}
            ),
            dcc.Dropdown(
                id='top_branches_dropdown',
                options=[
                    {'label': i, 'value': i} for i in merged_top_branches['region/county'].unique()
                ],
                value='East Midlands'
            ),
            dcc.Graph(id='top_branches_graph'),
        ], className='card-container six columns', id='title6',style={'margin-top' : '30px'})


    ])
])


@app.callback(
    Output('graph', 'figure'),
    [Input('radio_item', 'value')]
)
def update_product_data(radio_item):
    if radio_item == str(top_products_overall):
        fig = px.bar(top_products_overall,
            x='product', y='quantity_purchased', color='product', hover_data = ['quantity_purchased', 'product'])
        fig.update_layout(
            paper_bgcolor=colors['paper_bgcolor'], plot_bgcolor=colors['plot_bgcolor'], font_color = 'teal', showlegend = False)
        fig.update_xaxes(title_text = 'Products', title_font_color = 'teal', title_font_size = 16, showgrid=False, tickangle=90)
        fig.update_yaxes(showgrid=False, title_text = 'Quantity Sold', title_font_color = 'teal', title_font_size = 16,)
        fig.update_traces(width = 0.7)
        return fig

    if radio_item == str(bot_products_overall):
        fig = px.bar(bot_products_overall,
            x='product', y='quantity_purchased', color='product', hover_data = ['quantity_purchased', 'product'])
        fig.update_layout(
            paper_bgcolor=colors['paper_bgcolor'], plot_bgcolor=colors['plot_bgcolor'], font_color = 'teal', showlegend = False)
        fig.update_xaxes(title_text = 'Products', title_font_color = 'teal', title_font_size = 16, showgrid=False, tickangle=90)
        fig.update_yaxes(showgrid=False, title_text = 'Quantity Sold', title_font_color = 'teal', title_font_size = 16,)
        fig.update_traces(width = 0.7)
        return fig


@app.callback(
    Output('product_graph', 'figure'),
    [Input('top_products_radio_item', 'value'),
     Input('top_products_dropdown', 'value')]
)
def top_products_data(radio_item, selected_location):
    if radio_item == str(merged_top):
        df_by_location = merged_top[merged_top['region/county']
                                    == selected_location]
        fig = px.bar(df_by_location,
            x='product', y='counts', color='product', hover_data = ['counts', 'product'])
        fig.update_layout(
            paper_bgcolor=colors['paper_bgcolor'], plot_bgcolor=colors['plot_bgcolor'], font_color = 'teal', showlegend = False)
        fig.update_xaxes(title_text = 'Products', title_font_color = 'teal', title_font_size = 16, showgrid=False, tickangle=90)
        fig.update_yaxes(showgrid=False, title_text = 'Count', title_font_color = 'teal', title_font_size = 16,)
        fig.update_traces(width = 0.7)
        return fig

    if radio_item == str(merged_bot):
        df_by_location = merged_bot[merged_bot['region/county']
                                    == selected_location]
        fig = px.bar(df_by_location,
            x='product', y='counts', color='product', hover_data = ['counts', 'product'])
        fig.update_layout(
            paper_bgcolor=colors['paper_bgcolor'], plot_bgcolor=colors['plot_bgcolor'], font_color = 'teal', showlegend = False)
        fig.update_xaxes(title_text = 'Products', title_font_color = 'teal', title_font_size = 16, showgrid=False, tickangle=90)
        fig.update_yaxes(showgrid=False, title_text = 'Count', title_font_color = 'teal', title_font_size = 16,)
        fig.update_traces(width = 0.7)
        return fig


@app.callback(
    Output('cat_graph', 'figure'),
    [Input('cat_radio_item', 'value')]
)
def update_cat_data(radio_item):
    if radio_item == str(top_cat_overall):
        fig = px.bar(top_cat_overall,
            x='category', y='quantity_purchased', color='category', hover_data = ['quantity_purchased', 'category'])
        fig.update_layout(
            paper_bgcolor=colors['paper_bgcolor'], plot_bgcolor=colors['plot_bgcolor'], font_color = 'teal', showlegend = False)
        fig.update_xaxes(title_text = 'Categories', title_font_color = 'teal', title_font_size = 16, showgrid=False, tickangle=90)
        fig.update_yaxes(showgrid=False, title_text = 'Quantity Sold', title_font_color = 'teal', title_font_size = 16,)
        fig.update_traces(width = 0.7)
        return fig

    if radio_item == str(bot_cat_overall):
        fig = px.bar(bot_cat_overall,
            x='category', y='quantity_purchased', color='category', hover_data = ['quantity_purchased', 'category'])
        fig.update_layout(
            paper_bgcolor=colors['paper_bgcolor'], plot_bgcolor=colors['plot_bgcolor'], font_color = 'teal', showlegend = False)
        fig.update_xaxes(title_text = 'Categories', title_font_color = 'teal', title_font_size = 16, showgrid=False, tickangle=90)
        fig.update_yaxes(showgrid=False, title_text = 'Quantity Sold', title_font_color = 'teal', title_font_size = 16,)
        fig.update_traces(width = 0.7)
        return fig


@app.callback(
    Output('top_cat_graph', 'figure'),
    [Input('top_cat_radio_item', 'value'),
     Input('top_cat_dropdown', 'value')]
)
def top_cat_data(radio_item, selected_location):
    if radio_item == str(merged_top_cat):
        df_by_location = merged_top_cat[merged_top_cat['region/county']
                                        == selected_location]
        fig = px.bar(df_by_location,
            x='category', y='counts', color='category', hover_data = ['counts', 'category'])
        fig.update_layout(
            paper_bgcolor=colors['paper_bgcolor'], plot_bgcolor=colors['plot_bgcolor'], font_color = 'teal', showlegend = False)
        fig.update_xaxes(title_text = 'Categories', title_font_color = 'teal', title_font_size = 16, showgrid=False, tickangle=90)
        fig.update_yaxes(showgrid=False, title_text = 'Count', title_font_color = 'teal', title_font_size = 16,)
        fig.update_traces(width = 0.7)
        return fig

    if radio_item == str(merged_bot_cat):
        df_by_location = merged_bot_cat[merged_bot_cat['region/county']
                                        == selected_location]
        fig = px.bar(df_by_location,
            x='category', y='counts', color='category', hover_data = ['counts', 'category'])
        fig.update_layout(
            paper_bgcolor=colors['paper_bgcolor'], plot_bgcolor=colors['plot_bgcolor'], font_color = 'teal', showlegend = False)
        fig.update_xaxes(title_text = 'Categories', title_font_color = 'teal', title_font_size = 16, showgrid=False, tickangle=90)
        fig.update_yaxes(showgrid=False, title_text = 'Count', title_font_color = 'teal', title_font_size = 16,)
        fig.update_traces(width = 0.7)
        return fig


@app.callback(
    Output('branches_graph', 'figure'),
    [Input('branches_radio_item', 'value')]
)
def update_branches_data(radio_item):
    if radio_item == str(top_branches_overall):
        fig = px.bar(top_branches_overall,
            x='branch_name', y='amount_in_gbp', color='branch_name', hover_data = ['branch_name', 'amount_in_gbp'])
        fig.update_layout(
            paper_bgcolor=colors['paper_bgcolor'], plot_bgcolor=colors['plot_bgcolor'], font_color = 'teal', showlegend = False)
        fig.update_xaxes(title_text = 'Branch', title_font_color = 'teal', title_font_size = 16, showgrid=False, tickangle=90)
        fig.update_yaxes(showgrid=False, title_text = 'GBP', title_font_color = 'teal', title_font_size = 16,)
        fig.update_traces(width = 0.7)
        return fig

    if radio_item == str(bot_branches_overall):
        fig = px.bar(bot_branches_overall,
            x='branch_name', y='amount_in_gbp', color='branch_name', hover_data = ['branch_name', 'amount_in_gbp'])
        fig.update_layout(
            paper_bgcolor=colors['paper_bgcolor'], plot_bgcolor=colors['plot_bgcolor'], font_color = 'teal', showlegend = False)
        fig.update_xaxes(title_text = 'Branches', title_font_color = 'teal', title_font_size = 16, showgrid=False, tickangle=90)
        fig.update_yaxes(showgrid=False, title_text = 'GBP', title_font_color = 'teal', title_font_size = 16,)
        fig.update_traces(width = 0.7)
        return fig


@app.callback(
    Output('top_branches_graph', 'figure'),
    [Input('top_branches_radio_item', 'value'),
     Input('top_branches_dropdown', 'value')]
)
def top_branches_data(radio_item, selected_location):
    if radio_item == str(merged_top_branches):
        df_by_location = merged_top_branches[merged_top_branches['region/county']
                                             == selected_location]
        fig = px.bar(df_by_location,
            x='branch_name', y='amount_in_gbp', color='branch_name', hover_data = ['branch_name', 'amount_in_gbp'])
        fig.update_layout(
            paper_bgcolor=colors['paper_bgcolor'], plot_bgcolor=colors['plot_bgcolor'], font_color = 'teal', showlegend = False)
        fig.update_xaxes(title_text = 'Branches', title_font_color = 'teal', title_font_size = 16, showgrid=False, tickangle=90)
        fig.update_yaxes(showgrid=False, title_text = 'GBP', title_font_color = 'teal', title_font_size = 16,)
        fig.update_traces(width = 0.7)
        return fig

    if radio_item == str(merged_bot_branches):
        df_by_location = merged_bot_branches[merged_bot_branches['region/county']
                                             == selected_location]
        fig = px.bar(df_by_location,
            x='branch_name', y='amount_in_gbp', color='branch_name', hover_data = ['branch_name', 'amount_in_gbp'])
        fig.update_layout(
            paper_bgcolor=colors['paper_bgcolor'], plot_bgcolor=colors['plot_bgcolor'], font_color = 'teal', showlegend = False)
        fig.update_xaxes(title_text = 'Branches', title_font_color = 'teal', title_font_size = 16, showgrid=False, tickangle=90)
        fig.update_yaxes(showgrid=False, title_text = 'GBP', title_font_color = 'teal', title_font_size = 16,)
        fig.update_traces(width = 0.7)
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
