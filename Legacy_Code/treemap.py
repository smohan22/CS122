
# coding: utf-8

# In[28]:

# import plotly
# import plotly.plotly as py
# import plotly.graph_objs as go

# import squarify

# plotly.tools.set_credentials_file(username='igabr', api_key='API KEY')

# x = 0.
# y = 0.
# width = 100.
# height = 100.

# values = [500, 433, 78, 25]
# labels = ["Uberx", "hotel", "airfare", "bus"]
# normed = squarify.normalize_sizes(values, width, height)

# rects = squarify.squarify(normed, x, y, width, height)


# # Choose colors from http://colorbrewer2.org/ under "Export"
# color_brewer = ['rgb(166,206,227)','rgb(31,120,180)','rgb(178,223,138)',
#                 'rgb(51,160,44)','rgb(251,154,153)','rgb(227,26,28)',
#                 'rgb(253,191,111)','rgb(255,127,0)','rgb(202,178,214)',
#                 'rgb(106,61,154)','rgb(255,255,153)','rgb(177,89,40)']
# shapes = []
# annotations = []
# counter = 0

# for r in rects:
#     shapes.append( 
#         dict(
#             type = 'rect', 
#             x0 = r['x'], 
#             y0 = r['y'], 
#             x1 = r['x']+r['dx'], 
#             y1 = r['y']+r['dy'],
#             line = dict( width = 2 ),
#             fillcolor = color_brewer[counter]
#         ) 
#     )
#     annotations.append(
#         dict(
#             x = r['x']+(r['dx']/2),
#             y = r['y']+(r['dy']/2),
#             text = labels[counter],
#             showarrow = False
#         )
#     )
#     counter = counter + 1
#     if counter >= len(color_brewer):
#         counter = 0

# trace0 = go.Scatter(
#     x = [ r['x']+(r['dx']/2) for r in rects ], 
#     y = [ r['y']+(r['dy']/2) for r in rects ],
#     text = [ str(v) for v in values ], 
#     mode = 'text',
# )
        
# layout = dict(
#     height=700, 
#     width=700,
#     xaxis=dict(showgrid=False,zeroline=False),
#     yaxis=dict(showgrid=False,zeroline=False),
#     shapes=shapes,
#     annotations=annotations,
#     hovermode='closest'
# )

# # With hovertext
# figure = dict(data=[trace0], layout=layout)

# py.iplot(figure, filename='squarify-treemap') #this command is needed for Jupyter Notebook implementation.
# Differs for VM implementation


