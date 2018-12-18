from django.shortcuts import render
from django.http import HttpResponse
from fusioncharts import FusionCharts
from AdminConsorcios.models import *

def chart(request):
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = { 
        "caption": "Estadisticas",
        "showValues": "0",
        "theme": "zune"
        }

    # Convert the data in the `Country` model into a format that can be consumed by FusionCharts. 
    # The data for the chart should be in an array where in each element of the array is a JSON object
    # having the `label` and `value` as keys.

    dataSource['data'] = []
    dataSource['linkeddata'] = []
    # Iterate through the data in `Country` model and insert in to the `dataSource['data']` list.
    for f in Factura.objects.all():
      data = {}
      data['label'] = f.tipo
      data['value'] = f.monto
      # Create link for each country when a data plot is clicked.
      data['link'] = 'newchart-json-'+ f.numero
      dataSource['data'].append(data)

      # Create the linkData for cities drilldown    
      linkData = {}
      # Inititate the linkData for cities drilldown
      linkData['id'] = f.numero
      linkedchart = {}
      linkedchart['chart'] = {
        "caption" : "Estadisticas de " + f.fechaVencimiento ,
        "showValues": "0",
        "theme": "zune"
        }

      # Convert the data in the `City` model into a format that can be consumed by FusionCharts.     
      linkedchart['data'] = []
      # Filtering the data base on the Country Code
      for f in CajaConsorcio.objects.all().filter(id=f.cajaConsorcio_id):
          arrDara = {}
        arrDara['label'] = f.tipoDeCaja
        arrDara['value'] = f.montoActual
        linkedchart['data'].append(arrDara)

      linkData['linkedchart'] = linkedchart
      dataSource['linkeddata'].append(linkData)

    # Create an object for the Column 2D chart using the FusionCharts class constructor                      
    column2D = FusionCharts("column2D", "ex1" , "600", "350", "chart-1", "json", dataSource)
    return render(request, 'index.html', {'output': column2D.render()}) 
