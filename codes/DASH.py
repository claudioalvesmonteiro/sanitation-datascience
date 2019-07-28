import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

'''
df = pd.read_csv('http://dados.recife.pe.gov.br/dataset/99eea78a-1bd9-4b87-95b8-7e7bae8f64d4/resource/9afa68cf-7fd9-4735-b157-e23da873fef7/download/156diario.csv',
                sep = ';',
                header = 0,
                encoding = 'utf-8',
                error_bad_lines=False)
'''

app = dash.Dash()

#----------- BODY
app.layout = html.Div(children =[

    html.Div(children='''Dash tutorials'''),

    dcc.Graph(id='example-graph',
                figure={
                    'data': [
                        {'x': df.index, 'y': df.Close, 'type': 'line', 'name': stock},
                    ],
                    'layout': {
                        'title': stock
                    }
                }
    )


])

if __name__ == '__main__':
    app.run_server(debug=True)
