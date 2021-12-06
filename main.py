import json
import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
import utils.db_manager as db_manager
import services.wish_service as wish_service

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models.wish import Wish

def generate_statistics(gacha_type):
    wishes = wish_service.list(gacha_type)

    stats = {
        "pity count": 0,
        "wishes": {
            "5 star": {
                "total": 0,
                "colour": "#ffcc99",
                "list": []
                },
            "4 star":  {
                "total": 0,
                "colour": "#ffb3e6",
                "list": []
                },
            "3 star":  {
                "total": 0,
                "colour": "#66b3ff",
                "list": []
                },
            },
        }

    for wish in wishes:
        category = stats["wishes"]

        if wish.get_rank_type() == Wish.RANK_TYPES[3]:
            category = category["3 star"]
        elif wish.get_rank_type() == Wish.RANK_TYPES[4]:
            category = category["4 star"]
        elif wish.get_rank_type() == Wish.RANK_TYPES[5]:
            category = category["5 star"]

        category["total"] += 1

        if wish.get_rank_type() is not Wish.RANK_TYPES[3]:
            category["list"].append(
                {
                    "name": wish.get_name(),
                    "type": wish.get_item_type(),
                    "pulls": 0,
                }
            )

        for key in ["4 star", "5 star"]:
            if len(stats["wishes"][key]["list"]) > 0:
                stats["wishes"][key]["list"][-1]["pulls"] += 1

        if stats["wishes"]["5 star"]["total"] == 0:
            stats["pity count"] += 1

    # print(json.dumps(stats, indent = 4))
    print(90 - stats["pity count"], "pulls to next pity")

    return stats


def plot_graph(data):
    # plt.rcParams.update({'font.family':'sans-serif'})
    # plt.rcParams.update({'font.sans-serif':'Noto Emoji'})\

    background_colour = "#64778d"

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    # labels = "3 \N{White Medium Star}", "4 \N{White Medium Star}", "5 \N{White Medium Star}"
    labels = []
    sizes = [] 
    colours = []
    explode = []

    for key, value in data.items():
        if value["total"] == 0:
            continue

        labels.append(key)
        sizes.append(value["total"])
        explode.append(0.05) # "explode" slice

        # Add colours
        colours.append(value["colour"])
    
    # Set font colours on plots
    matplotlib.rcParams.update({"text.color" : "white", "axes.labelcolor" : "white"})
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%", startangle=90, pctdistance=0.5, colors=colours)
    fig1.set_facecolor(background_colour)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Draw circle
    centre_circle = plt.Circle((0,0), 0.70, fc=background_colour)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)# Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()

    matplotlib.use("TkAgg")

    return fig1

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

db_manager.initialize()
gacha_type = "character"
stats = generate_statistics(gacha_type)

# sg.theme("DarkGrey6")
menu_def = [
    [
        "&Banner", 
        [
            "!&Character", 
            "&Weapon", 
            "&Standard"
        ]
    ]
]

# Define the window layout
layout = [
    [sg.Menu(menu_def, key="-MENU-", disabled_text_color="grey", font=("Calibri", 11), pad=(5, 5))],
    # [sg.Text("Wish Counter")],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("Refresh")]
]

# Create the form and show it without the plot
window = sg.Window(
    "Wish Statistics",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
)

# Add the plot to the window
fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, plot_graph(stats["wishes"]))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break
    elif event in ("Character", "Weapon", "Standard"):
        for i in range(len(menu_def[0][1])):
            item = menu_def[0][1][i]
            if item[0] == '!':
                menu_def[0][1][i] = item[1:] 
            if item[1:] == event:
                menu_def[0][1][i] = '!' + item
                
        window["-MENU-"].update(menu_definition=menu_def)
        gacha_type = event.lower()
        stats = generate_statistics(gacha_type)
        fig_agg.get_tk_widget().forget()
        plt.close("all")
        fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, plot_graph(stats["wishes"]))
        window.refresh()
    elif event == "Refresh":
        try:
            wish_service.retrieve_history(gacha_type)
        except BaseException as e:
            print(e)
            continue
            
        stats = generate_statistics(gacha_type)
        fig_agg.get_tk_widget().forget()
        plt.close("all")
        fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, plot_graph(stats["wishes"]))
        window.refresh()

window.close()

