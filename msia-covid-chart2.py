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

    # Stack plot: Cases, Deaths and Recoveries
    fig9, ax9 = plt.subplots()
    colors = ['black', 'blue', 'red']
    labels = ['Deaths', 'Recoveries', 'Active Cases']
    ax9 = create_stack_plot(ax9, deaths, recoveries, active_cases, labels, colors)
    ax9 = set_grid(ax9, 'both')
    ax9, fig9 = set_date_formatter(ax9, fig9)
    ax9 = set_locator(ax9, 500, 100)
    ax9 = set_tick_params(ax9)
    ax9 = set_title(ax9, 'Covid-19 Trend in Malaysia in Stack Plot')
    ax9 = set_axis_label(ax9)
    ax9.legend(reversed(ax9.legend().legendHandles), reversed(labels),fontsize='xx-small', loc=(0.02, 0.9))
    plt.tight_layout()
    fig9.savefig('siew_project/portfolio/static/portfolio/images/charts/all-cdr-stack.png', dpi=900)

    # Grouped Bar chart: Cases, Deaths and Recoveries - April
    data_april = data[67:]
    ax13 = create_group_bar_chart(data_april)
    ax13 = set_axis_label(ax13)
    ax13 = set_tick_params(ax13)
    ax13.legend(labels=['Cases', 'Recoveries', 'Deaths'], fontsize='xx-small')
    ax13 = set_title(ax13, 'Grouped Bar Chart: Cases, Deaths and Recoveries - April')
    plt.tight_layout()
    fig13 = ax13.get_figure()
#    fig13.savefig('siew_project/portfolio/static/portfolio/images/charts/groupbarchart-apr.png', dpi=900)

    # Stacked bar chart: Cases, Deaths and Recoveries
    fig14, ax14 = plt.subplots()
    ax14.bar(date, deaths, label='Deaths', color='black')
    ax14.bar(date, recoveries, bottom=deaths, label='Recoveries', color='blue')
    ax14.bar(date, active_cases, bottom=recoveries, label='Active Cases', color='red')
    ax14 = set_grid(ax14, 'y')
    ax14, fig14 = set_date_formatter(ax14, fig14)
    ax14 = set_locator(ax14, 500, 100)
    ax14 = set_tick_params(ax14)
    ax14 = set_title(ax14, 'Stacked Bar Chart: Cases, Deaths and Recoveries')
    ax14 = set_axis_label(ax14)
    labels = ['Deaths', 'Recoveries', 'Active Cases']
    ax14.legend(reversed(ax14.legend().legendHandles), reversed(labels),fontsize='xx-small', loc=(0.02, 0.85))
    plt.tight_layout()
    fig14.savefig('siew_project/portfolio/static/portfolio/images/charts/stacked-bar-chart-cdr.png', dpi=900)

# Run script every day at 8.30pm UTC+8
schedule.every().day.at("12:25").do(main)

while True:
    schedule.run_pending()
    time.sleep(60)

if __name__ == "__main__":
    main()
