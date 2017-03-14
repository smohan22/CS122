import os
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import squarify

#install plotly and squarify on the VM inorder to make this treemap work.
#do localised testing for the demo

def treemap(dictionary):
    plotly.tools.set_credentials_file(username='igabr', api_key='X9WSMxsuICEbuSNKm20n')

    # uber_cost, hotel_cost, airfare_cost, bus_cost, food_cost
    uber_cost = int(dictionary["uber"])
    hotel_cost = dictionary["hotels"]

    if hotel_cost == []:
        hotel_cost = 0

    airfare_cost = dictionary["flights"]

    if airfare_cost == []:
        airfare_cost = 0

    bus_cost = dictionary["bus"]

    food_cost = dictionary["food"]

    x = 0.
    y = 0.
    width = 100.
    height = 100.

    if uber_cost != 0 and (hotel_cost) == 0 and (airfare_cost) == 0 and (bus_cost) == 0 and food_cost !=0:
        values = [uber_cost, food_cost]
        labels = ["Uberx: $" + str(uber_cost), "Food: $" + str(food_cost)]
        normed = squarify.normalize_sizes(values, width, height)
        rects = squarify.squarify(normed, x, y, width, height)

    elif uber_cost!=0 and hotel_cost!=0 and airfare_cost!=0 and bus_cost == 0 and food_cost != 0:
        values = [uber_cost, hotel_cost, airfare_cost, food_cost]
        labels = ["Uberx: $" + str(uber_cost) , "Hotel: $" + str(hotel_cost), "Airfare: $" + str(airfare_cost), "Food: $" + str(food_cost)]
        normed = squarify.normalize_sizes(values, width, height)
        rects = squarify.squarify(normed, x, y, width, height)

    elif uber_cost!= 0 and hotel_cost != 0 and airfare_cost == 0 and bus_cost!=0 and food_cost !=0:
        values = [uber_cost, hotel_cost, bus_cost, food_cost]
        labels = ["Uberx: $" + str(uber_cost) , "Hotel: $" + str(hotel_cost), "Bus: $" + str(bus_cost), "Food: $" + str(food_cost)]
        normed = squarify.normalize_sizes(values, width, height)
        rects = squarify.squarify(normed, x, y, width, height)

    elif uber_cost!=0 and (hotel_cost == 0) and (airfare_cost == 0) and bus_cost != 0 and food_cost != 0:
        values = [uber_cost, bus_cost, food_cost]
        labels = ["Uberx: $" + str(uber_cost), "Bus: $" + str(bus_cost), "Food: $" +str(food_cost)]
        normed = squarify.normalize_sizes(values, width, height)
        rects = squarify.squarify(normed, x, y, width, height)
    else:
        print("f")
        values = [uber_cost, hotel_cost, airfare_cost, bus_cost, food_cost]
        labels = ["Uberx: $" + str(uber_cost) , "Hotel: $" + str(hotel_cost), "Airfare: $" + str(airfare_cost), "Bus: $" + str(bus_cost), "Food: $" + str(food_cost)]
        normed = squarify.normalize_sizes(values, width, height)
        rects = squarify.squarify(normed, x, y, width, height)


    # Choose colors from http://colorbrewer2.org/ under "Export"
    color_brewer = ['rgb(166,206,227)','rgb(31,120,180)','rgb(178,223,138)',
                    'rgb(51,160,44)','rgb(251,154,153)','rgb(227,26,28)',
                    'rgb(253,191,111)','rgb(255,127,0)','rgb(202,178,214)',
                    'rgb(106,61,154)','rgb(255,255,153)','rgb(177,89,40)']
    shapes = []
    annotations = []
    counter = 0

    for r in rects:
        shapes.append( 
            dict(
                type = 'rect', 
                x0 = r['x'], 
                y0 = r['y'], 
                x1 = r['x']+r['dx'], 
                y1 = r['y']+r['dy'],
                line = dict( width = 2 ),
                fillcolor = color_brewer[counter]
            ) 
        )
        annotations.append(
            dict(
                x = r['x']+(r['dx']/2),
                y = r['y']+(r['dy']/2),
                text = labels[counter],
                showarrow = False
            )
        )
        counter = counter + 1
        if counter >= len(color_brewer):
            counter = 0

    # # For hover text
    trace0 = go.Scatter(
        x = [ r['x']+(r['dx']/2) for r in rects ], 
        y = [ r['y']+(r['dy']/2) for r in rects ],
        text = [ str(v) for v in values ], 
        mode = 'text',
    )
            
    layout = dict(
        height=700, 
        width=700,
        xaxis=dict(showgrid=False,zeroline=False),
        yaxis=dict(showgrid=False,zeroline=False),
        shapes=shapes,
        annotations=annotations,
        # hovermode='closest'
    )

    # With hovertext
    figure = dict(data=[trace0], layout=layout)

    # plot_url = plotly.offline.plot(figure, auto_open=False, image='png', image_filename='plot_image', link_text=None)
    current_directory = os.path.dirname(__file__)
    image_location = 'school_app/static/media/TreeMap.png'
    try:
        os.remove(image_location)
    except OSError:
        pass
    py.image.save_as(figure, os.path.join(current_directory, image_location), scale=3)

    # return plot_url


   