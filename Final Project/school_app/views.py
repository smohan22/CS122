from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django import forms
import sys
import csv
import os
from django.forms.extras.widgets import SelectDateWidget
from final_result import *
from .models import Choice
from main_function import *
from treemap import *
from final_result import *

##############################PAGE 1 DETAILS#####################################

glob_result = {}
FLIGHTS = {}
HOTELS = {}

def load_column(filename, col=0):
    """Loads single column from csv file"""
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.split(current_directory)[0]
    filename = os.path.join(parent_directory, filename)
    with open(filename) as f:
        col = list(zip(*csv.reader(f)))[0]
    column = [{"name": x} for x in col]    
    return column


SCHOOLS = load_column(filename = 'CPS_Final_Data_Pandas.csv')
HOTEL_PREFERENCE = [{"cost": "$"},{"cost":'$$'},{"cost":'$$$'}]
glob_args = {}

def index(request):
    '''
    Populates the school names in the drop down for schools in page 1 of HTML
    '''
    template = loader.get_template('school_app/index.html')
    schools = SCHOOLS
    hotel_pref_context = HOTEL_PREFERENCE
    context = {
        'schools': schools,
        'hotel_pref_context': hotel_pref_context
    }
    return HttpResponse(template.render(context, request))

class SearchForm(forms.Form):
    '''
    Creates the form for page 1 of HTML. Contains like number of people travelling, school name to visit
    '''
    num_travelling = forms.IntegerField(label='Number of people travelling', required=False)
    home_addr = forms.CharField(label='Start Address', required=False)
    school1 = forms.CharField(label='School1', \
            widget=forms.widgets.Select(choices=SCHOOLS), required=True)
    depart_home = forms.DateField(widget=SelectDateWidget(\
                empty_label=("Choose Year", "Choose Month", "Choose Day"),), 
                required = True)
    depart_school1 = forms.DateField(widget=SelectDateWidget(
                     empty_label=("Choose Year", "Choose Month", "Choose Day"),), \
                    required = True)
    hotel_pref = forms.CharField(label='Hotel Preferences', \
            widget=forms.widgets.Select(choices=HOTEL_PREFERENCE), required=False)
    
    # school2 = forms.CharField(label='School2', \
    #         widget=forms.widgets.Select(choices=SCHOOLS), required=False)
    # depart_school2 = forms.DateField(widget=SelectDateWidget(
    #          empty_label=("Choose Year", "Choose Month", "Choose Day"),), required = False)
        

def helper_page1(request):
    '''
    Create a form and populate it with data from request.
    Sends the data across to main function to get itenarary details.
    Checks if we need to go to the page 2 to get choices for school/flight
    '''
    context = {}
    result = None
    global glob_result 
    global glob_args
    global FLIGHTS
    global HOTELS

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        
        # check whether it's valid:
        if form.is_valid():
            # Convert form data to an args dictionary for find_courses
            args = {}
            if form.cleaned_data['num_travelling']:
                args['num_travelling'] = form.cleaned_data['num_travelling']
            if form.cleaned_data['school1']:
                args['school1'] = form.cleaned_data['school1']
            if form.cleaned_data['depart_home']:
                args['depart_home'] = form.cleaned_data['depart_home']
            if form.cleaned_data['depart_school1']:
                args['depart_school1'] = form.cleaned_data['depart_school1']
            if form.cleaned_data['hotel_pref']:
                args['hotel_pref'] = str(len(form.cleaned_data['hotel_pref']))
            if form.cleaned_data['home_addr']:
                args['home_addr'] = form.cleaned_data['home_addr']
            #school2 made temporarily
            args['school2'] = "Name of College"
            #Hashed out code for school2
            # if form.cleaned_data['school2']:
            #     args['school2'] = form.cleaned_data['school2']
            # if form.cleaned_data['depart_school2']:
            #     args['depart_school2'] = form.cleaned_data['depart_school2']
            # else:
            #     args['depart_school2'] = None    
            
            try:
                result = get_itinerary(args)
            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """An exception was thrown during search:
                <pre>{}{}</pre>""".format(e, '\n'.join(bt))
                result = None
                #go to error page if we get an error
                return render(request, 'school_app/errors.html', context )
        else:
            #go to error page if we get an error
            return render(request, 'school_app/errors.html', context )
    else:
        form = SearchForm()
    
    if result is None:
        #go to error page if the result is none
        context['result'] = "None"        
    else:
        context['result'] = result[0]
        
    context['form'] = form
    
    if result[0].get('hotels', []) == []:
        #directly go to treemap page if we do not have to make selections
        treemap(result[0])
        return render(request, 'school_app/result.html', context )
    else:
        #go to page two to choose flight/hotel
        glob_result = result[0]
        glob_args = result[1]
        FLIGHTS, HOTELS = index_result(glob_result['flights'],glob_result['hotels'])
        
        return render(request, 'school_app/choice.html', context )

############################PAGE 2 DETAILS###################################

def index_result(flight, hotel):
    '''
    Populates the flights/hotel details in the drop down in page 2 of HTML
    '''
    flight_details = []
    hotel_details = []
    
    if flight != None:
        flight_details = [{"flights": x} for x in glob_result['flights']]
    if hotel != None:
        hotel_details = [{"hotels": x} for x in glob_result['hotels']]
    
    return flight_details, hotel_details


class SelectForm(forms.Form):
    '''
    Creates the form for page 2 of HTML. Contains flights/hotel details
    '''
    flights = forms.CharField(label='flight_details', \
            widget=forms.widgets.Select(choices=FLIGHTS), required=False)
    
    hotels = forms.CharField(label='hotel_details', \
            widget=forms.widgets.Select(choices=HOTELS), required=False)
    

def result(request):
    '''
    Create a form and populate it with data from request.
    Sends the data across to make treemap funcction to create the treemap.
    Sends us to the final page  of the HTML
    '''
    context = {}
    result = None
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SelectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Convert form data to an args dictionary for find_courses
            args = {}
            if form.cleaned_data['flights']:
                args['flight'] = form.cleaned_data['flights']
            if form.cleaned_data['hotels']:
                args['hotel'] = form.cleaned_data['hotels']
            try:
                #calculates cost based on hotel/flight selection
                #creates treemap
                calc_cost = get_rest_itin(glob_args, args)
                result = treemap(calc_cost)
            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """An exception was thrown during search:
                <pre>{}{}</pre>""".format(e, '\n'.join(bt))
                result = None
                return render(request, 'school_app/errors.html', context )
        else:
            result = None
            return render(request, 'school_app/errors.html', context )
    else:
        form = SearchForm()
    
    if result is None:
        context['result'] = "None"        
    else:
        context['result'] = result
        
    context['form'] = form
    
    return render(request, 'school_app/result.html', context )