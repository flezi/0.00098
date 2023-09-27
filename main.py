import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import filedialog
from math import ceil
from analyser import TextAnalyser


def select_file(*events):
    '''
    TODO:
        активировать кнопку создания вордклауда
        только если все виджеты получили данные от пользователя
    '''
    file_path = filedialog.askopenfilename(
        initialdir="./",
        title="Выбирите файл с текстом",
        filetypes=files,
        defaultextension=files,
    )

    if file_path:
        file_path_lbl['text'] = file_path


def select_color(*events):
    color = colorchooser.askcolor()[1]
    wc_background_cnvs.configure(bg=color)


def run(*args):
    '''
        TODO:
            виджеты:
                destination_file
                wc_background
            выбор пути для картинки при вызове этой функции
            проверка на пустые виджеты, диалоги ошибок

        FIXME:
            картинка в два раза больше, чем указанные параметры!
    '''
    TextAnalyser(
        source_file=file_path_lbl['text'],
        words_ammount=int(words_ammount_entry.get()),
        wc_width=int(wc_width_entry.get()),
        wc_height=int(wc_height_entry.get()),
        wc_margin=int(wc_margin_entry.get()),
        wc_background=wc_background_cnvs['background'],
        parts_of_speech=[s.get() for s in pos_vars if s.get()],
    )


files = [
    ('Text Document', '*.txt')
]

window = tk.Tk()
window.title('Облако слов из текстового файла')

# source file selection
file_path_btn = tk.Button(window, text='выбрать файл', command=select_file)
file_path_lbl = tk.Label(window, text='Выбирите исходный файл с текстом')
file_path_lbl.bind("<Button-1>", select_file)

# words ammount
words_ammount_lbl = tk.Label(window, text='количество слов на картинке:')
words_ammount_entry = tk.Entry(window)  # TODO: только инты

# wordcloud image size
wc_width_lbl = tk.Label(window, text='ширина картинки в пискелях:')
wc_width_entry = tk.Entry(window)
wc_height_lbl = tk.Label(window, text='высота картинки в пискелях:')
wc_height_entry = tk.Entry(window)
wc_margin_lbl = tk.Label(window, text='отступ картинки от края в пискелях:')
wc_margin_entry = tk.Entry(window)

# wc background color selection
wc_background_lbl = tk.Label(window, text='выбирите цвет фона картинки:')
wc_background_cnvs = tk.Canvas(width=100, height=100)
wc_background_cnvs.configure(bg='#000000')
wc_background_cnvs.bind("<Button-1>", select_color)

# parts of speech selection
pos_lbl = tk.Label(window, text='части речи:')
pos_texts = [
    'имя существительное',
    'имя прилагательное (полное)',
    'имя прилагательное (краткое)',
    'компаратив',
    'глагол (личная форма)',
    'глагол (инфинитив)',
    'причастие (полное)',
    'причастие (краткое)',
    'деепричастие',
    'числительное',
    'наречие',
    'местоимение-существительное',
    'предикатив',
    'предлог',
    'союз',
    'частица',
    'междометие',
]
pos_values = [
    'NOUN',
    'ADJF',
    'ADJS',
    'COMP',
    'VERB',
    'INFN',
    'PRTF',
    'PRTS',
    'GRND',
    'NUMR',
    'ADVB',
    'NPRO',
    'PRED',
    'PREP',
    'CONJ',
    'PRCL',
    'INTJ',
]

pos_chckbtns = []
pos_vars = [tk.StringVar() for _ in pos_texts]

for i, _ in enumerate(pos_texts):
    chkbtn = tk.Checkbutton(
        window,
        text=pos_texts[i],
        onvalue=pos_values[i],
        offvalue='',
        variable=pos_vars[i],
    )
    pos_chckbtns.append(chkbtn)

# start button
start_btn = tk.Button(window, text='создать облако слов', command=lambda: run())

# widgets placement
file_path_btn.grid(row=0, column=0, sticky='e', padx=10, pady=10)
file_path_lbl.grid(row=0, column=1, sticky='w', pady=10)
words_ammount_lbl.grid(row=1, column=0, sticky='e', padx=10, pady=10)
words_ammount_entry.grid(row=1, column=1, sticky='w', pady=10)
wc_width_lbl.grid(row=2, column=0, sticky='e', padx=10, pady=10)
wc_width_entry.grid(row=2, column=1, sticky='w', pady=10)
wc_height_lbl.grid(row=3, column=0, sticky='e', padx=10, pady=10)
wc_height_entry.grid(row=3, column=1, sticky='w', pady=10)
wc_margin_lbl.grid(row=4, column=0, sticky='e', padx=10, pady=10)
wc_margin_entry.grid(row=4, column=1, sticky='w', pady=10)
wc_background_lbl.grid(row=5, column=0, sticky='e', padx=10, pady=10)
wc_background_cnvs.grid(row=5, column=1, sticky='w', pady=10)

pos_lbl.grid(row=6, columnspan=100)
start_row = 7
columns = 5
rows = ceil(len(pos_chckbtns) / columns)
for i, chkbtn in enumerate(pos_chckbtns):
    row = start_row + i // columns
    column = i % columns
    chkbtn.grid(row=row, column=column, sticky='w')

start_btn.grid(column=0, columnspan=100, pady=20)

window.mainloop()