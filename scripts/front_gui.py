# Front User Interface
import PySimpleGUI as sg

layout = [[sg.Text("Seller (Other than solar power): "), sg.InputText()],
          [sg.Text("Seller (By solar power Max:3): "), sg.InputText()],
          [sg.Text("Consumers (Excluding EV-Consumers): "), sg.InputText()],
          [sg.Text("EV-Consumers: "), sg.InputText()],
          [sg.Button("Submit"), sg.Button("Exit")]]

window = sg.Window("Amount of Consumers and Prosumers", layout, font=("Times New Roman", 16))


while True:
    event, values = window.read()
    if event == "Exit":
        try:
            sg.popup("Bye. See you again.", font=("Times New Roman", 16))
            window.close()
            a = 0
            b = 0
            c = 0
            d = 0
            areas = []
            pass
        except:
            pass
    elif event == "Submit":
        try:
            a = int(values[0])
            b = int(values[1])
            c = int(values[2])
            d = int(values[3])
            if a + b != c + d:
                # To check if Prosumers = Consumers
                sg.popup("The total number of prosumers does not match the total number of consumers. Please check again.", font=("Times New Roman", 16))
            elif b > 3:
                # To prevent more than 3 PV-prosumers
                sg.popup("Unable to have more than 3 PV-prosumers. Please re-enter the amount of PV-prosumers.", font=("Times New Roman", 16))
            elif a < 0:
                # To prevent users to type negative amount
                sg.popup("Unable to have negative Prosumers (Excluding PV-Prosumers). Please enter positive integers.", font=("Times New Roman", 16))
            elif b < 0:
                # To prevent users to type negative amount
                sg.popup("Unable to have negative PV-prosumers. Please enter positive integers.", font=("Times New Roman", 16))
            elif c < 0:
                # To prevent users to type negative amount
                sg.popup("Unable to have negative Consumers (Excluding EV-Consumers). Please enter positive integers.", font=("Times New Roman", 16))
            elif d < 0:
                # To prevent users to type negative amount
                sg.popup("Unable to have negative EV-Consumers. Please enter positive integers.", font=("Times New Roman", 16))
            else:
                # Initialize empty list to store Solar panel area
                areas = []

                if b > 0:

                    for i in range(b):

                        while True:
                            # Allow users to enter
                            area = sg.popup_get_text("Enter the areas (m^2) for Solar PVs (eg:312Wp = 1.561m^2):", font=("Times New Roman", 16))
                            try:
                                # Append of areas
                                if int(area) > 0:
                                    areas.append(int(area))
                                    break
                                else:
                                    # Prevent negative numbers
                                    sg.popup("Invalid input. Please enter a positive integer.", font=("Times New Roman", 16))
                            except ValueError:
                                # Prevent other charactor being entered
                                sg.popup("Invalid input. Please enter a positive integer.", font=("Times New Roman", 16))
                else:
                    # To tell there is no PV-prosumers
                    sg.popup("There are no PV-prosumers.", font=("Times New Roman", 16))
                    
                # Popup window to show prosumers, pv-prosumers, consumers, ev-consumers, areas and the total numbers of prosumers/consumers    
                sg.popup(f"Prosumers: {a}\nPV-Prosumers: {b}\nConsumers: {c}\nEV-Consumers: {d}\nTotal Prosumers: {a + b}\nTotal Consumers: {c + d}\nAreas: {areas}\n", font=("Times New Roman", 18))
                #sg.popup(f"Areas: {areas}\n", font=("Times New Roman", 16))
                break
        except ValueError:
            sg.popup("Invalid input. Please enter positive integers for all fields.", font=("Times New Roman", 16))
    elif event == sg.WIN_CLOSED:
        a = 0
        b = 0
        c = 0
        d = 0
        areas = []
        break
window.close()
