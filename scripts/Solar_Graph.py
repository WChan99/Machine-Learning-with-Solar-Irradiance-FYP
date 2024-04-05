# Plot of Solar graph
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_graph0( x1, y1):
    
    # Create the plot 
    def create_plot(year, predicition):
        plt.plot( x1, y1, color='blue',marker='o')
        plt.title('Predicted Solar Power Vs Time of the Day', fontsize=18)
        plt.xlabel('Time of the Day', fontsize=14)
        plt.ylabel('Predicted Solar Power', fontsize=14)
        plt.grid(True)
        return plt.gcf()

    # Layout
    layout = [[sg.Text('Prediction Plot', font=("Times New Roman", 18))],
             [sg.Canvas(size=(500, 500), key='Solar Power')],
             [sg.Exit()]]

    # Position of the plot
    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
    
    # Window
    window = sg.Window('Plot of Solar Power', layout, finalize=True, element_justification='center', font=("Times New Roman", 18))
    
    # Drawing of figure
    draw_figure(window['Solar Power'].TKCanvas, create_plot(x1, y1))

    return(window)


def plot_graph1( x1, y1, areas):
    
    # Create the plot 
    def create_plot(year, predicition):
        plt.plot( x1, y1, color='blue', label=f'Solar Panel {areas[0]}m^2')
        plt.title('Predicted Solar Power Vs Time of the Day', fontsize=18)
        plt.xlabel('Time of the Day', fontsize=14)
        plt.ylabel('Predicted Solar Power (MWh)', fontsize=14)
        plt.grid(True)
        plt.legend(loc='upper right')
        return plt.gcf()

    # Layout
    layout = [[sg.Text('Prediction Plot', font=("Times New Roman", 18))],
             [sg.Canvas(size=(500, 500), key='Solar Power')],
             [sg.Exit()]]

    # Position of the plot
    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
    
    # Window
    window = sg.Window('Plot of Solar Power', layout, finalize=True, element_justification='center', font=("Times New Roman", 18))
    
    # Drawing of figure
    draw_figure(window['Solar Power'].TKCanvas, create_plot(x1, y1))

    return(window)


def plot_graph2( x1, y1, y2, areas):
    
    # Create the plot 
    def create_plot(year, predicition, prediction):
        plt.plot( x1, y1, color='blue', label=f'Solar Panel {areas[0]}')
        plt.plot( x1, y2, color='red', label=f'Solar Panel {areas[1]}')
        plt.title('Predicted Solar Power Vs Time of the Day', fontsize=18)
        plt.xlabel('Time of the Day', fontsize=14)
        plt.ylabel('Predicted Solar Power (MWh)', fontsize=14)
        plt.grid(True)
        plt.legend(loc='upper right')
        return plt.gcf()

    # Layout
    layout = [[sg.Text('Prediction Plot', font=("Times New Roman", 18))],
             [sg.Canvas(size=(500, 500), key='Solar Power')],
             [sg.Exit()]]

    # Position of the plot
    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
    
    # Window
    window = sg.Window('Plot of Solar Power', layout, finalize=True, element_justification='center', font=("Times New Roman", 18))
    
    # Drawing of figure
    draw_figure(window['Solar Power'].TKCanvas, create_plot(x1, y1, y2))

    return(window)


def plot_graph3( x1, y1, y2, y3, areas):

    # Create the plot 
    def create_plot(year, predicition, prediction2, prediction3):
        plt.plot( x1, y1, color='blue', label=f'Solar Panel {areas[0]}')
        plt.plot( x1, y2, color='red', label=f'Solar Panel {areas[1]}')
        plt.plot( x1, y3, color='green', label=f'Solar Panel {areas[2]}')
        plt.title('Predicted Solar Power Vs Time of the Day', fontsize=18)
        plt.xlabel('Time of the Day', fontsize=14)
        plt.ylabel('Predicted Solar Power (MWh)', fontsize=14)
        plt.grid(True)
        plt.legend(loc='upper right')
        return plt.gcf()

    # Layout
    layout = [[sg.Text('Prediction Plot', font=("Times New Roman", 18))],
             [sg.Canvas(size=(500, 500), key='Solar Power')],
             [sg.Exit()]]

    # Position of the plot
    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
    
    # Window
    window = sg.Window('Plot of Solar Power', layout, finalize=True, element_justification='center', font=("Times New Roman", 18))
    
    # Drawing of figure
    draw_figure(window['Solar Power'].TKCanvas, create_plot(x1, y1, y2, y3))

    return(window)
