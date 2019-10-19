#Import packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash_table import DataTable
import pandas as pd
from plotly import tools
import xml.etree.cElementTree as et
import pandas as pd


#Declare application
app=dash.Dash(__name__)
application=app.server


tree=et.parse(r'data/ag_prodchange_ref_IRR_MGMT.xml')
root=tree.getroot()
r=[elem.tag for elem in root.iter()]

tree2=et.parse(r'data/ag_prodchange_ssp3_IRR_MGMT.xml')
root6=tree2.getroot()

tree3=et.parse(r'data/ag_prodchange_ssp5_IRR_MGMT.xml')
root7=tree3.getroot()

tree4=et.parse(r'data/ag_prodchange_ssp1_IRR_MGMT.xml')
root8=tree4.getroot()

tree5=et.parse(r'data/ag_prodchange_ssp5_IRR_MGMT.xml')
root9=tree5.getroot()


Countries=[]
for x in root.iter('region'):
       Countries.append(x.attrib['name'])



app.layout = html.Div([html.Div(
    [
        dcc.Markdown(
            '''
            ### Dashboard to explore year on year yield growth data parsed from a multi-layered xml.
            The below visualization parses through a multi-layered xml file and presents a dashboard where the user can
            explore the different layers and compare yield results by country,crop, basin for 3 SSPs. Finally, the dashboard allows
            the user to explore yield for different 'technologies' i.e. yields for rainfed and irrigated land which are further bifurcated
            by high and low scenarios. The table below shows the available basins for the selected country and crops.  
            The visualization uses outputs of the GCAM model which can be found [here]("https://github.com/JGCRI/gcamdata").
            '''.replace('  ', ''),
            className='eight columns offset-by-three'
        )
    ], className='row',
    style={'text-align': 'center', 'margin-bottom': '10px'}
),
html.Div([(dcc.Dropdown(id='region', options=[{'label': i
, 'value': i} for i in Countries],value='USA')),
        html.Div(id='container-button-basic',
             children='Please select a Country')],style={ 'width': '20%','float':'right'}),
html.Div([(dcc.Dropdown(id='Sup sector')),
        html.Div(id='container-button-basic1',
             children='Please select a supply sector (Crop)')],style={ 'width': '20%','float':'right'}),
html.Div([(dcc.Dropdown(id='sub-sector')),
        html.Div(id='container-button-basic2',
             children='Please select a basin')],style={ 'width': '20%','float':'right'}),
html.Div([(dcc.Dropdown(id='technology')),
        html.Div(id='container-button-basic3',
             children='Please select a technology')],style={ 'width': '20%','float':'right'}),


html.Div([dcc.Graph( id='graph')],style={'width': '80%','float':'left','height':'48%', 'display': 'inline-block'}),
html.Div(DataTable(id='table1',columns=[{"name": 'Country', "id": 'Country'},{"name": 'Crop selected', "id": 'Crop selected'},{"name": 'Basins available', "id": 'Basins available'}]),style={'display': 'inline-block', 'width': '60%', 'float': 'left', 'height': '150px'})
])

#Create drop down values

@app.callback(
    dash.dependencies.Output('Sup sector', 'value'),
    [dash.dependencies.Input('region', 'value')]
     )

def Crop_Dropdown_options(val):
    supsector=[]
    root1 = et.Element('root')

    for x in root.iter('region'):
        if x.attrib['name'] == str(val):
            root1.append(x)


    for s in root1.iter('AgSupplySector'):
        supsector.append(s.attrib['name'])

        supsector = list(set(supsector))

    return (supsector[0])

@app.callback(
    dash.dependencies.Output('sub-sector', 'value'),
    [dash.dependencies.Input('region', 'value'),
     dash.dependencies.Input('Sup sector','value')]
     )

def Crop_Dropdown_options(val,val2):
    subsec=[]
    root1 = et.Element('root')
    root2 = et.Element('root')
    for x in root.iter('region'):
        if x.attrib['name'] == str(val):
            root1.append(x)


    for s  in root1.iter('AgSupplySector'):
        if s.attrib['name'] == str(val2):
            root2.append(s)

    for sub in root2.iter('AgSupplySubsector'):
        subsec.append(sub.attrib['name'])

        subsec = list(set(subsec))

    return (subsec[0])

@app.callback(
    dash.dependencies.Output('technology', 'value'),
    [dash.dependencies.Input('region', 'value'),
     dash.dependencies.Input('Sup sector', 'value'),
     dash.dependencies.Input('sub-sector', 'value')]
     )

def Crop_Dropdown_options(val,val2,val3):
    tech=[]
    root1 = et.Element('root')
    root2 = et.Element('root')
    root3 = et.Element('root')

    for x in root.iter('region'):
        if x.attrib['name'] == str(val):
            root1.append(x)


    for s  in root1.iter('AgSupplySector'):
        if s.attrib['name'] == str(val2):
            root2.append(s)

    for sub in root2.iter('AgSupplySubsector'):
        if sub.attrib['name'] == str(val3):
            root3.append(sub)

    for t in root3.iter('AgProductionTechnology'):
        tech.append(t.attrib['name'])

        tech= list(set(tech))

    return (tech[0])

#Create drop down options
@app.callback(
    dash.dependencies.Output('Sup sector', 'options'),
    [dash.dependencies.Input('region', 'value')]
     )

def Crop_Dropdown_options(val):
    supsector=[]
    root1 = et.Element('root')

    for x in root.iter('region'):
        if x.attrib['name'] == str(val):
            root1.append(x)


    for s in root1.iter('AgSupplySector'):
        supsector.append(s.attrib['name'])

    return ([{'label': i
                 , 'value': i} for i in supsector])


@app.callback(
    dash.dependencies.Output('sub-sector', 'options'),
    [dash.dependencies.Input('region', 'value'),
     dash.dependencies.Input('Sup sector','value')]
     )

def Crop_Dropdown_options(val,val2):
    subsec=[]
    root1 = et.Element('root')
    root2 = et.Element('root')
    for x in root.iter('region'):
        if x.attrib['name'] == str(val):
            root1.append(x)


    for s  in root1.iter('AgSupplySector'):
        if s.attrib['name'] == str(val2):
            root2.append(s)

    for sub in root2.iter('AgSupplySubsector'):
        subsec.append(sub.attrib['name'])

    return ([{'label': i
                 , 'value': i} for i in subsec])

@app.callback(
    dash.dependencies.Output('technology', 'options'),
    [dash.dependencies.Input('region', 'value'),
     dash.dependencies.Input('Sup sector', 'value'),
     dash.dependencies.Input('sub-sector', 'value')]
     )

def Crop_Dropdown_options(val,val2,val3):
    tech=[]
    root1 = et.Element('root')
    root2 = et.Element('root')
    root3 = et.Element('root')

    for x in root.iter('region'):
        if x.attrib['name'] == str(val):
            root1.append(x)

    for s  in root1.iter('AgSupplySector'):
        if s.attrib['name'] == str(val2):
            root2.append(s)

    for sub in root2.iter('AgSupplySubsector'):
        if sub.attrib['name'] == str(val3):
            root3.append(sub)

    for j in root3.iter('AgProductionTechnology'):
        tech.append(j.attrib['name'])



    return (([{'label': i
                 , 'value': i} for i in tech]))


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('region', 'value'),
     dash.dependencies.Input('Sup sector', 'value'),
     dash.dependencies.Input('sub-sector', 'value'),
     dash.dependencies.Input('technology', 'value')])

def create_graph(val,val2,val3,val4):
    Year = []
    Value = []

    root1 = et.Element('root')
    root2 = et.Element('root')
    root3 = et.Element('root')
    root4=et.Element('root')
    root5=et.Element('root')

    for x in root.iter('region'):
        if x.attrib['name'] == str(val):
            root1.append(x)

    for s in root1.iter('AgSupplySector'):
        if s.attrib['name'] == str(val2):
            root2.append(s)

    for sub in root2.iter('AgSupplySubsector'):
        if sub.attrib['name'] == str(val3):
            root3.append(sub)

    for t in root3.iter('AgProductionTechnology'):
          if t.attrib['name']==str(val4):
              root4.append(t)

    for y in root4.iter('period'):

        root5=y
        for ag in root5.iter('agProdChange'):

            Value.append(ag.text)
            Year.append(y.attrib['year'])





    test_df = pd.DataFrame({'Year': Year, 'Value': Value})
    test_df['Value']=test_df['Value'].astype(float)
    test_df['Value']=test_df['Value']*100

    Year2 = []
    Value2 = []

    root1 = et.Element('root')
    root2 = et.Element('root')
    root3 = et.Element('root')
    root4 = et.Element('root')
    root5 = et.Element('root')

    for x in root6.iter('region'):
        if x.attrib['name'] == str(val):
            root1.append(x)

    for s in root1.iter('AgSupplySector'):
        if s.attrib['name'] == str(val2):
            root2.append(s)

    for sub in root2.iter('AgSupplySubsector'):
        if sub.attrib['name'] == str(val3):
            root3.append(sub)

    for t in root3.iter('AgProductionTechnology'):
        if t.attrib['name'] == str(val4):
            root4.append(t)

    for y in root4.iter('period'):

        root5 = y
        for ag in root5.iter('agProdChange'):

            Value2.append(ag.text)
            Year2.append(y.attrib['year'])

    test_df2 = pd.DataFrame({'Year': Year2, 'Value': Value2})
    test_df2['Value'] = test_df2['Value'].astype(float)
    test_df2['Value'] = test_df2['Value']*100



    Year2 = []
    Value2 = []

    root1 = et.Element('root')
    root2 = et.Element('root')
    root3 = et.Element('root')
    root4 = et.Element('root')
    root5 = et.Element('root')

    for x in root7.iter('region'):
        if x.attrib['name'] == str(val):
            root1.append(x)

    for s in root1.iter('AgSupplySector'):
        if s.attrib['name'] == str(val2):
            root2.append(s)

    for sub in root2.iter('AgSupplySubsector'):
        if sub.attrib['name'] == str(val3):
            root3.append(sub)

    for t in root3.iter('AgProductionTechnology'):
        if t.attrib['name'] == str(val4):
            root4.append(t)

    for y in root4.iter('period'):

        root5 = y
        for ag in root5.iter('agProdChange'):

            Value2.append(ag.text)
            Year2.append(y.attrib['year'])

    test_df3 = pd.DataFrame({'Year': Year2, 'Value': Value2})
    test_df3['Value'] = test_df3['Value'].astype(float)
    test_df3['Value'] = test_df3['Value'] * 100

    root1 = et.Element('root')
    root2 = et.Element('root')
    root3 = et.Element('root')
    root4 = et.Element('root')
    root5 = et.Element('root')

    Year2=[]
    Value2=[]
    for x in root8.iter('region'):
        if x.attrib['name'] == str(val):
            root1.append(x)

    for s in root1.iter('AgSupplySector'):
        if s.attrib['name'] == str(val2):
            root2.append(s)

    for sub in root2.iter('AgSupplySubsector'):
        if sub.attrib['name'] == str(val3):
            root3.append(sub)

    for t in root3.iter('AgProductionTechnology'):
        if t.attrib['name'] == str(val4):
            root4.append(t)

    for y in root4.iter('period'):

        root5 = y
        for ag in root5.iter('agProdChange'):

            Value2.append(ag.text)
            Year2.append(y.attrib['year'])

    test_df4 = pd.DataFrame({'Year': Year2, 'Value': Value2})
    test_df4['Value'] = test_df4['Value'].astype(float)
    test_df4['Value'] = test_df4['Value'] * 100


    trace1 = go.Scatter(
        x=test_df['Year'],
        y=test_df['Value'],
        mode='lines',
        name='SSP2',
        marker=dict(
            color='#3D9970'
        ))

    trace2 = go.Scatter(
        x=test_df2['Year'],
        y=test_df2['Value'],
        mode='lines',
        name='SSP3',
        marker=dict(
            color='rgba(152, 0, 0, .8)'
        ))



    trace4 = go.Scatter(
        x=test_df4['Year'],
        y=test_df4['Value'],
        mode='lines',
        name='SSP1',
        marker=dict(
            color='rgba(225, 171, 251, 1)'
        ))

    data = [trace1]
    fig = tools.make_subplots(rows=1, cols=1, specs=[[{}]],
                              shared_xaxes=True, shared_yaxes=True,
                              vertical_spacing=0.001)

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 1)
    fig.append_trace(trace4, 1, 1)
    fig['layout'].update(
        title='Yield for the selected country, for the selected crop,in the selected basin for different technologies under the SSPs',
        yaxis=dict(title='Percent Yield'),
        xaxis=dict(title='Year')

    )

    return fig


@app.callback(dash.dependencies.Output('table1', 'data'),
    [dash.dependencies.Input('region', 'value'),
     dash.dependencies.Input('Sup sector', 'value')
     ])

def Update_Table(val,val2):
    Country= []
    Crop = []
    subsector=[]

    root1 = et.Element('root')
    root2 = et.Element('root')
    root3 = et.Element('root')
    root4 = et.Element('root')
    root5 = et.Element('root')

    for x in root.iter('region'):
        if x.attrib['name'] == str(val):
            root1.append(x)



    for s in root1.iter('AgSupplySector'):
        if s.attrib['name'] == str(val2):
            root2.append(s)

    for sub in root2.iter('AgSupplySubsector'):
        subsector.append(sub.attrib['name'])
        Country.append(val)
        Crop.append(val2)


    Country=pd.Series(Country,name='Country')
    Crop=pd.Series(Crop,name='Crop selected')
    subsector=pd.Series(subsector,name='Basins available')

    #subsector = list(set(subsector))
    #Country=list(set(Country))

    test_df5 = pd.concat([Country,Crop,subsector],axis=1)


    test_df5=test_df5.to_dict('records')
    print(test_df5)
    return (test_df5)




if __name__ == '__main__':
    application.run_server(debug=True)









