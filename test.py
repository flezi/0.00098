import tkinter as tk


window = tk.Tk()

word_cloud = tk.PhotoImage(file='./wordcloud.png')
lable_worldcloud = tk.Label(image=word_cloud)
lable = tk.Label(text='sdsdasd')
lable_worldcloud.pack(anchor='center')
lable.pack()
window.mainloop()