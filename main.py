#---------------------Packages-----------------------------------------
from ast import Import
import os


import os

try:
    import requests
except ImportError:
    os.system('pip install requests')

try:
    import dash
except ImportError:
    os.system('pip install dash')

try:
    import dash_bootstrap_components as dbc
except ImportError:
    os.system('pip install dash_bootstrap_components')


import requests
from bs4 import BeautifulSoup
import dash_bootstrap_components as dbc
from dash import Input, Output, html
from turtle import width
import dash
from dash import dcc
from dash import html
#-------------------------------Initialisation------------------------------------
AllLinks = []
links = []
imgs = []
hrefTable = []
imgTableLinks = []
priceTable = []
augmentTable = []
paragraphs = []
newUrl = "https://coinmarketcap.com"
url = 'https://coinmarketcap.com/fr/'
nameSymbol = []

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
#----------------------------Scrapping------------------------------------------
if response.ok:
    result = soup.find('table',{'class':'cmc-table'}).find('tbody').find_all('tr')
    for elem in result :
        a = elem.find('a')
        href = a.get('href')
        hrefTable.append(href)


for urlTarget in hrefTable:
    table_all_img = []
    link = newUrl + urlTarget
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    img = soup.find_all('img')
    price = soup.find(class_ = 'priceValue')
    a = price.find('span')
    priceTable.append(str(a))
    body = soup.find(class_ = 'sc-1q9q90x-0 jCInrl h1')
    nameSymbol.append(str(body.find('small')))
    for imgTarget in img : 
        img_src = imgTarget.get('src')
        table_all_img.append(img_src)
    imgTableLinks.append(list(filter(lambda k :'.png' in k ,table_all_img))[0])

#------------------------------Prix des crypto-----------------------------------
conc=[]
conc2=[]
for k in range (len(priceTable)):
    d=''
    for i in range (len(str(priceTable[k]))):
        liste = ['0','1','2','3','4','5','6','7','8','9',',','.']
        if str(priceTable[k])[i] in liste:
            conc.append(str(priceTable[k][i]))
            d = d+ str(priceTable[k])[i]
    conc2.append(d)
    d = ''

#---------------------------------Diminutif des crypto-------------------------------
for i in range (len(nameSymbol)):
    nameSymbol[i] = nameSymbol[i][26] + nameSymbol[i][27] + nameSymbol[i][28]

#----------------------------Création du tableau pour l'onglet sur le site-------------------------
row=[]
for i in range (99):
    row.append(html.Tr([html.Img(src=imgTableLinks[i], style={'height':'64px', 'width':'64px'}), html.Td(nameSymbol[i]), html.Td(conc2[i])]))

table_header = [html.Thead(html.Tr([html.Th("Logo"), html.Th("Abréviation de la crypto"), html.Th("Prix en €")]))]

Prix = dbc.Table(table_header + row, bordered=True)

imgTableLinks[7] = 'https://seeklogo.com/images/S/solana-sol-logo-9AA58519FE-seeklogo.com.png'

#--------------------------------Menu------------------------------------------
Menu = dbc.Card(
    html.Div(
    children = [
    html.H1(children = "Marché des cryptomonnaies",
            style={"textAlign" : "center", "fontSize": "48px", "color": "white"}),
    dbc.CardImg(src="https://img.phonandroid.com/2017/12/bitcoin.jpg", style={'height':'500px', 'width':'1000px'}),
    html.H4("Sur ce site vous trouverez un onglet."),
    html.H4( "L'onglet vous indique le prix des cents cryptomonnaies les plus populaires aujourd'hui."),
    ]
    )
)
#----------------------------------Onglet--------------------------------------
Onglet = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Menu Principal", tab_id="tab-1"),
                    dbc.Tab(label="Prix", tab_id="tab-2"),
                ],
                id="card-tabs",
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(html.P(id="card-content", className="card-text")),
    ]
)

#-------------------------------App--------------------------------------------

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div(
    Onglet
    )

@app.callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)


def tab_content(active_tab):
    if active_tab == "tab-1":
        return Menu
    elif active_tab == "tab-2":
        return Prix


if __name__ == "__main__":
    app.run_server(debug=True)