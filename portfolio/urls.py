from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('msia-latest-covid-data/', views.msia_latest_covid_data, name='msia_latest_covid_data'),
    path('msia-covid-chart', views.msia_covid_chart, name='msia_covid_chart'),
    path('ebook-download', views.ebook_download, name='ebook_download'),
    path('sudoku-solver', views.sudoku, name='sudoku'),
]
