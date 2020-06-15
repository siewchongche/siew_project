import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from matplotlib.ticker import MultipleLocator
import schedule
import time

def main():
    data = pd.read_csv('~/siew_project/media/data.csv')

    data['date'] = pd.to_datetime(data['date'])
    data.sort_values('date', inplace=True)

    date = data['date']
    cases = data['cases']
    new_cases = data['new cases']
    deaths = data['deaths']
    new_deaths = data['new deaths']
    recoveries = data['recoveries']
    new_recoveries = data['new recoveries']
    active_cases = cases - recoveries - deaths

    def create_plot_date(ax, column, color, label):
        ax.plot_date(date, column, linestyle='solid', color=color, alpha=0.5, linewidth='1', markersize=1, fillstyle='full', label=label)
        return ax

    def create_stack_plot(ax, column1, column2, column3, labels, colors):
        ax.stackplot(date, column1, column2, column3, labels=labels, colors=colors, alpha=0.75)
        return ax

    def lineplot_fill_between(ax, xdf, yline1, yline2, color, label):
        ax.fill_between(xdf, yline1, yline2, color=color, alpha=0.25, label=label)
        return ax

    def create_bar_chart(ax, column, color):
        ax.bar(date, column, color=color, alpha=0.5)
        return ax

    def create_pie_chart():
        slices = [active_cases.iloc[-1], deaths.iloc[-1], recoveries.iloc[-1]]
        labels = ['Cases', 'Deaths', 'Recoveries']
        colors = ['#ff6666','#404040', '#7092ff']
        explode = [0, 0.1, 0]
        plt.pie(slices, labels=labels, colors=colors, autopct='%1.1f%%', explode=explode)
        plt.title('Latest Percentages for Covid19')
        return plt

    def create_group_bar_chart(data_month):
        data_month = data_month[['date', 'new cases', 'new recoveries', 'new deaths']].copy()
        data_month.set_index('date', inplace=True)

        color = ['red', 'blue', 'black']
        ax = data_month.plot.bar(color=color)
        ax = set_grid(ax, 'y')
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x(), p.get_height()), fontsize=4)

        ticks = [tick.get_text() for tick in ax.get_xticklabels()]
        ticks = pd.to_datetime(ticks).strftime('%b %d')
        ax.set_xticklabels(ticks, rotation=45)
        return ax

    def set_grid(ax, axis):
        ax.grid(axis=axis, which='both', alpha=0.25)
        return ax

    def set_mean_line(ax, dataframe, label):
        for index, value in dataframe.iteritems():
            if value == 0:
                dataframe.drop(index, inplace=True)
        ax.axhline(dataframe.mean(), color='#fc4f30', label=label, linewidth=1)
        return ax

    def set_date_formatter(ax, fig):
        date_format = mpl_dates.DateFormatter('%b, %d')
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        return ax, fig

    def set_locator(ax, major, minor):
        # x axis
        ax.xaxis.set_major_locator(mpl_dates.DayLocator(interval=2))
        ax.xaxis.set_minor_locator(MultipleLocator())
        #y axis
        ax.yaxis.set_major_locator(MultipleLocator(major))
        ax.yaxis.set_minor_locator(MultipleLocator(minor))
        return ax

    def set_tick_params(ax):
        ax.tick_params(axis='x', which='major', pad=0, labelsize=3)
        ax.tick_params(axis='y', which='both', right=True, labelright=True, labelsize=5)
        return ax

    def set_title(ax, title):
        ax.set_title(title, fontsize=10)
        return ax

    def set_axis_label(ax):
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('Amount', fontsize=10)
        return ax

    def set_legend(ax):
        ax.legend(fontsize='xx-small', loc=(0.02, 0.9))
        return ax

 
    # Pie chart: all
    chart = create_pie_chart()
    chart.savefig('siew_project/portfolio/static/portfolio/images/charts/cdr-perc.png', dpi=900)

    # Lineplot: all
    fig1, ax1 = plt.subplots() 
    ax1 = create_plot_date(ax1, cases, 'red', 'Cases')
    ax1 = create_plot_date(ax1, deaths, 'black', 'Deaths')
    ax1 = create_plot_date(ax1, recoveries, 'blue', 'Recoveries')
    ax1 = set_grid(ax1, 'both')
    ax1, fig1 = set_date_formatter(ax1, fig1)
    ax1 = set_locator(ax1, 500, 100)
    ax1 = set_tick_params(ax1)
    ax1 = set_title(ax1, 'Covid-19 Trend in Malaysia')
    ax1 = set_axis_label(ax1)
    ax1 = set_legend(ax1)
    plt.tight_layout() # For better image layout
    fig1.savefig('siew_project/portfolio/static/portfolio/images/charts/all-cdr.png', dpi=900)

    # Lineplot: cases only
    fig2, ax2 = plt.subplots() 
    ax2 = create_plot_date(ax2, cases, 'red', 'Cases')
    ax2 = set_grid(ax2, 'both')
    ax2, fig2 = set_date_formatter(ax2, fig2)
    ax2 = set_locator(ax2, 500, 100)
    ax2 = set_tick_params(ax2)
    ax2 = set_title(ax2, 'Covid-19 Trend in Malaysia - Cases')
    ax2 = set_axis_label(ax2)
    ax2 = set_legend(ax2)
    plt.tight_layout()
    fig2.savefig('siew_project/portfolio/static/portfolio/images/charts/all-cases.png', dpi=900)

    # Lineplot: deaths only
    fig3, ax3 = plt.subplots() 
    ax3 = create_plot_date(ax3, deaths, 'black', 'Deaths')
    ax3 = set_grid(ax3, 'both')
    ax3, fig3 = set_date_formatter(ax3, fig3)
    ax3 = set_locator(ax3, 10, 5)
    ax3 = set_tick_params(ax3)
    ax3 = set_title(ax3, 'Covid-19 Trend in Malaysia - Deaths')
    ax3 = set_axis_label(ax3)
    ax3 = set_legend(ax3)
    plt.tight_layout()
    fig3.savefig('siew_project/portfolio/static/portfolio/images/charts/all-deaths.png', dpi=900)

    # Lineplot: recoveries only
    fig4, ax4 = plt.subplots() 
    ax4 = create_plot_date(ax4, recoveries, 'blue', 'Recoveries')
    ax4 = set_grid(ax4, 'both')
    ax4, fig4 = set_date_formatter(ax4, fig4)
    ax4 = set_locator(ax4, 500, 100)
    ax4 = set_tick_params(ax4)
    ax = set_title(ax4, 'Covid-19 Trend in Malaysia - Recoveries')
    ax4 = set_axis_label(ax4)
    ax4 = set_legend(ax4)
    plt.tight_layout()
    fig4.savefig('siew_project/portfolio/static/portfolio/images/charts/all-recoveries.png', dpi=900)

    # Bar chart: daily new cases
    fig5, ax5 = plt.subplots()
    ax5 = create_bar_chart(ax5, new_cases, 'red')
    ax5 = set_grid(ax5, 'y')
    ax5 = set_mean_line(ax5, new_cases, 'Cases Mean (not include 0 case day)')
    ax5, fig5 = set_date_formatter(ax5, fig5)
    ax5 = set_locator(ax5, 10, 5)
    ax5 = set_tick_params(ax5)
    ax5 = set_title(ax5, 'Covid-19 Trend in Malaysia - Daily Cases')
    ax5 = set_axis_label(ax5)
    ax5 = set_legend(ax5)
    plt.tight_layout()
    fig5.savefig('siew_project/portfolio/static/portfolio/images/charts/new-cases.png', dpi=900)

    # Bar chart: daily new deaths
    fig6, ax6 = plt.subplots()
    ax6 = create_bar_chart(ax6, new_deaths, 'black')
    ax6 = set_grid(ax6, 'y')
    ax6 = set_mean_line(ax6, new_deaths, 'Deaths Mean (not include 0 case day)')
    ax6, fig6 = set_date_formatter(ax6, fig6)
    ax6 = set_locator(ax6, 1, 1)
    ax6 = set_tick_params(ax6)
    ax6 = set_title(ax6, 'Covid-19 Trend in Malaysia - Daily Death')
    ax6 = set_axis_label(ax6)
    ax6 = set_legend(ax6)
    plt.tight_layout()
    fig6.savefig('siew_project/portfolio/static/portfolio/images/charts/new-deaths.png', dpi=900)

    # Bar chart: daily new recoveries
    fig7, ax7 = plt.subplots()
    ax7 = create_bar_chart(ax7, new_recoveries, 'blue')
    ax7 = set_grid(ax7, 'y')
    ax7 = set_mean_line(ax7, new_cases, 'Cases Mean (not include 0 case day)')
    ax7, fig7 = set_date_formatter(ax7, fig7)
    ax7 = set_locator(ax7, 10, 5)
    ax7 = set_tick_params(ax7)
    ax7 = set_title(ax7, 'Covid-19 Trend in Malaysia - Daily Recoveries')
    ax7 = set_axis_label(ax7)
    ax7 = set_legend(ax7)
    plt.tight_layout()
    fig7.savefig('siew_project/portfolio/static/portfolio/images/charts/new-recoveries.png', dpi=900)

    # Lineplot: filling area of active cases
    fig8, ax8 = plt.subplots()
    ax8 = create_plot_date(ax8, cases, 'red', 'Cases')
    ax8 = create_plot_date(ax8, recoveries, 'blue', 'Recoveries')
    ax8 = lineplot_fill_between(ax8, date, cases, recoveries, 'orange', 'Active Cases')
    ax8 = set_grid(ax8, 'both')
    ax8, fig8 = set_date_formatter(ax8, fig8)
    ax8 = set_locator(ax8, 500, 100)
    ax8 = set_tick_params(ax8)
    ax8 = set_title(ax8, 'Covid-19 Trend in Malaysia - Active Cases')
    ax8 = set_axis_label(ax8)
    ax8 = set_legend(ax8)
    plt.tight_layout()
    fig8.savefig('siew_project/portfolio/static/portfolio/images/charts/active-cases.png', dpi=900)

# Run script every day at 8.30pm UTC+8
schedule.every().day.at("12:20").do(main)

#while True:
#    schedule.run_pending()
#    time.sleep(60)

if __name__ == "__main__":
    main()
