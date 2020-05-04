from django.shortcuts import render
from django.conf import settings
from . import utils
from . import sudokusolver

def home(request):
    return render(request, 'portfolio/index.html')

def msia_latest_covid_data(request):
    download_path = settings.MEDIA_ROOT 
    data_dict = utils.latest_data()
    context = {
        'date': data_dict['date'],
        'new_cases': data_dict['new_cases'],
        'confirmed_cases': data_dict['confirmed_cases'],
        'new_deaths': data_dict['new_deaths'],
        'confirmed_deaths': data_dict['confirmed_deaths'],
        'new_recoveries': data_dict['new_recoveries'],
        'recoveries': data_dict['recoveries'],
        'download_path': download_path
        }
    return render(request, 'portfolio/msia-latest-covid-data.html', context)

def msia_covid_chart(request):
    data_dict = utils.latest_data()
    context = {'date': data_dict['date']}
    return render(request, 'portfolio/msia-covid-chart.html', context)

def ebook_download(request):
    return render(request, 'portfolio/ebook-download.html')

def sudoku(request):
    if request.method == 'POST':
        # Send data to the function
        # Retrieve the data and send to template as context
        raw_data = request.POST['raw_data']
        raw_data_list, error = sudokusolver.sudokusolver(raw_data)
        context = {}
        if error:
            context['error_msg'] = 'This sudoku cannot be solved. Kindly check the number inserted if correct.'
        else:
            context['raw_data_list'] = raw_data_list
        return render(request, 'portfolio/sudoku-solver.html', context)
    else:
        return render(request, 'portfolio/sudoku-solver.html')
