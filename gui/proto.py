import tkinter as tk
from tkinter import *
import PIL
from PIL import Image,ImageTk
import test

from test import *

test_image = "..//config//podcast_covers//Noble Blood.jpg"

image = PIL.Image.open(open(test_image,'rb'))

image.thumbnail((100,100))


def get():

    print(search_input.get())



root = tk.Tk()

root.geometry('600x600')

image_tk = PIL.ImageTk.PhotoImage(image)

info_frame = tk.Frame(root)

title = tk.Label(info_frame,text="Test podcast")

episode_num = tk.Label(info_frame,text="number of episodes 1")

podcast_cover = tk.Button(info_frame,image=image_tk)

lst_updated = tk.Label(info_frame,text='Test date')

search_input = tk.Entry(info_frame)

search_button = tk.Button(info_frame,text="Search",command=lambda:get())

download_que_button = tk.Button(info_frame,text="Add episode to download que")

description_button = tk.Button(info_frame,text="view episode description")

title.grid(sticky='snew',columnspan=2)

episode_num.grid(column=0,row=2,stick='snew',columnspan=2)

podcast_cover.grid(column=0,row=3,columnspan=2)

lst_updated.grid(column=0,row=4,columnspan=2)

search_input.grid(column=0,row=5,columnspan=2)

search_button.grid(column=1,row=5)

download_que_button.grid(column=0,row=6)

description_button.grid(column=1,row=6)

info_frame.pack(side=TOP)


# test listboxes

list_box_frame = tk.Frame(root)

podcast_list_box = tk.Listbox(list_box_frame,relief=SUNKEN)

podcast_list_box.config(width=0,height=0)

podcast_scrollbar = tk.Scrollbar(list_box_frame)

podcast_scrollbar.config(command=podcast_list_box.yview)

podcast_list_box.config(yscrollcommand=podcast_scrollbar.set)


podcast_index = 0

for key in podcast_data.keys():

    podcast_list_box.insert(podcast_index,podcast_data[key]['title'])

    podcast_index+=1

podcast_list_box.select_set(0)
    

podcast_scrollbar.pack(side=LEFT,fill=Y)

podcast_list_box.pack(side=LEFT,expand=YES,fill=BOTH)


episode_list_box = tk.Listbox(list_box_frame,relief=SUNKEN)

episode_list_box.config(width=0,height=0)

episode_scrollbar = tk.Scrollbar(list_box_frame)

episode_scrollbar.config(command=episode_list_box.yview)

episode_list_box.config(yscrollcommand=episode_scrollbar.set)

episode_scrollbar.pack(side=RIGHT,fill=Y)

episode_list_box.pack(side=RIGHT,expand=YES,fill=BOTH)


test_episodes = podcast_episode_data[0]

episode_index = 0

for episode in test_episodes:

    episode_list_box.insert(episode_index,episode[0])

    episode_index+=1


list_box_frame.pack(side=TOP)

#root.mainloop()


