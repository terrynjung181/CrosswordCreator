from typing import final
import PySimpleGUI as sg
import random
import string
from layout_solver.word_slot import WordSlot

def run_intro_gui():
    BOX_SIZE = 75
    CROSSWORD_SIZE = 450
    layout = [
        [sg.Text('Crossword Puzzle Using PySimpleGUI'), sg.Text('', key='-OUTPUT-')],
        [sg.Graph(canvas_size=(CROSSWORD_SIZE, CROSSWORD_SIZE), graph_bottom_left=(0,0), graph_top_right=(CROSSWORD_SIZE,CROSSWORD_SIZE), key='-GRAPH-',
                change_submits=True, drag_submits=False)],

        [sg.Button('Solve')]
    ]

    window = sg.Window('Window Title', layout, finalize=True)

    g = window['-GRAPH-']
    num_boxes = CROSSWORD_SIZE//BOX_SIZE
    rect_array = []
    for row in range(num_boxes):
        row_array = []
        for col in range(num_boxes):
            row_array.append([g.draw_rectangle((col * BOX_SIZE , row * BOX_SIZE), (col * BOX_SIZE + BOX_SIZE, row * BOX_SIZE + BOX_SIZE), line_color='white', fill_color="black"), 0])
        rect_array.append(row_array)

    while True:             # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Solve'):
            break
        mouse = values['-GRAPH-']

        if event == '-GRAPH-':
            if mouse == (None, None):
                continue
            box_x = mouse[0]//BOX_SIZE
            box_y = mouse[1]//BOX_SIZE
            if rect_array[box_y][box_x][1] == 0: #switch to white
                g.TKCanvas.itemconfig(rect_array[box_y][box_x][0], fill = "White", outline = "Black") 
                rect_array[box_y][box_x][1] = 1
            else:
                g.TKCanvas.itemconfig(rect_array[box_y][box_x][0], fill = "Black", outline = "White")
                rect_array[box_y][box_x][1] = 0 
        

    window.close()
    return convert_to_mat(rect_array, num_boxes)

def convert_to_mat(rect_array, num_boxes):
    final_mat = []
    for i in range(num_boxes):
        row = []
        for j in range(num_boxes):
            row.append(rect_array[i][j][1])

        final_mat.insert(0, row)

    return final_mat

def run_exit_gui(initial_crossword, word_slots, theme):
    BOX_SIZE = 75
    CROSSWORD_SIZE = 450
    max_ind = 0
    for i in range(len(word_slots)):
        if max_ind < word_slots[i].get_index():
            max_ind = word_slots[i].get_index()

    layout = [
        [sg.Text('Crossword Puzzle'), sg.Text('', key='-OUTPUT-')],
        [sg.Text("THEME: " + theme)],
        [sg.Graph(canvas_size=(CROSSWORD_SIZE, CROSSWORD_SIZE), graph_bottom_left=(0,0), graph_top_right=(CROSSWORD_SIZE,CROSSWORD_SIZE ), key='-GRAPH-', background_color="red",
                change_submits=True, drag_submits=False)],
        [sg.Text('ACROSS', size=(30,1)), sg.Text('DOWN', size=(30,1))],
        [[sg.Text('', size=(30,2), key='-ACROSS-'+str(i)), sg.Text('', size=(30,2), key='-DOWN-'+str(i))] for i in range(1, max_ind+ 2)],
    ]

    window = sg.Window('Window Title', layout, finalize=True)
    g = window['-GRAPH-']
    
    num_boxes = CROSSWORD_SIZE//BOX_SIZE
    rect_array = []
    for row in range(num_boxes):
        for col in range(num_boxes):
            row_array = []
            if initial_crossword[num_boxes - row - 1][col] == 0:
                row_array.append(g.draw_rectangle((col * BOX_SIZE , row * BOX_SIZE), (col * BOX_SIZE + BOX_SIZE, row * BOX_SIZE + BOX_SIZE), line_color='white', fill_color="black"))
            else:
                row_array.append(g.draw_rectangle((col * BOX_SIZE , row * BOX_SIZE), (col * BOX_SIZE + BOX_SIZE, row * BOX_SIZE + BOX_SIZE), line_color='black', fill_color="white"))
            
            rect_array.append(row_array)

    for word in word_slots:
        start_y, start_x = word.get_start()
        start_y = num_boxes - start_y - 1
        direction = word.get_direction()
        word_to_write = word.get_best_word()
        index_to_write = word.get_index()
        clue_to_write = word.get_clue()
        i = 0
        while i < len(word_to_write):
            g.draw_text(word_to_write[i].upper(), (start_x * BOX_SIZE + BOX_SIZE//2, start_y * BOX_SIZE + BOX_SIZE//2), font='Courier 15',color="black")
            if i == 0:
                g.draw_text(str(index_to_write), (start_x * BOX_SIZE + 0.1*(BOX_SIZE), start_y * BOX_SIZE + 0.8*(BOX_SIZE)), font='Courier 9',color="black")
            if direction == "ACROSS":
                start_x += 1
            else:
                start_y -= 1
            i += 1
        window['-' + direction + '-' + str(index_to_write)].update(str(index_to_write) + ". " + clue_to_write)
        

    while True:             # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Solve'):
            break    
        
    window.close()

    





if __name__ == "__main__":
    run_intro_gui()