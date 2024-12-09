import requests
import pandas as pd
from bs4 import BeautifulSoup, NavigableString, Tag
from flask import jsonify

def get_content_processamento(url, year):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extrair tbody      
        consulta = {"Processamento": []}
             
        #  Looking for the table with the classes 'wikitable' and 'sortable'
        table = soup.find('table', class_='tb_base tb_dados')
        
        # Defining of the dataframe
        df = pd.DataFrame(columns=['ano', 'categoria', 'item','quantidade'])
            
        #Initialize vars
        unidadeMedida = "Kilo"
        ano = year
        item = ""
        quantidade = ""
        categoria = ""
        
        # Collecting Ddata
        for row in table.tbody.find_all('tr'):    
           
            # Find all columns para categoria for each column
            columns = row.find_all('td', {"class":"tb_item"})
            if(columns != []):
                categoria = columns[0].text.rstrip('\n').replace("""""","").strip()
 
            else:
                columnsubItem = row.find_all('td', {"class":"tb_subitem"})
                
                if(columnsubItem != []):
                    item = columnsubItem[0].text.strip()
                    quantidade = columnsubItem[1].text.strip()
             
            if len(item) > 0:   
                #df = df.append({'ano': ano,  'categoria': categoria, 'item': item, 'quantidade': quantidade}, ignore_index=True)  
                consulta["Processamento"].append(
                                {
                                    "ano" : ano,
                                    "categoria": categoria,
                                    "item": item,
                                    "quantidade": quantidade,
                                    "medida" : unidadeMedida                                                                      
                                })          
                item = ""
        return jsonify(consulta)
                                    
    except Exception as e:
        return jsonify({"Error - Processamento": str(e)}), 500