import PIL
from PIL import Image,ImageTk
import tkinter as tk
from tkinter import *
import textwrap
import gui_crud
import configparser
from gui_crud import *



class Podcast_Gui:

    def __init__(self,podcast_data,episode_data,cover_paths,download_path):

        self.podcast_data = podcast_data
        self.episode_data = episode_data
        self.cover_paths = cover_paths
        self.download_path = download_path
        self.tk_image_holder = []
        self.download_que = {}
        self.current_podcast_index = 0
    
    def gen_gui(self):

        # grabbing the first podcast , episode and podcast cover_path
        first_podcast_data = self.podcast_data[0]
        first_episode_data = self.episode_data[0][0]
        first_cover_image_path = self.cover_paths[0]
        self.root = tk.Tk()
        self.root.geometry("600x650")

        # creates the imagetk object for the first podcast cover image
        first_image_tk = PIL.Image.open(open(first_cover_image_path,'rb'))
        first_image_tk.thumbnail((100,100))
        first_image_tk = ImageTk.PhotoImage(first_image_tk)

        # info frame 
        self.info_frame = tk.Frame(self.root)
        self.title_label = tk.Label(self.info_frame,text=first_podcast_data['title'])
        self.episode_num_label = tk.Label(self.info_frame,text="There are "+str(first_podcast_data['episode_count'])+" episodes in total")
        self.podcast_cover_button = tk.Button(self.info_frame,image=first_image_tk)
        self.lst_updated_label = tk.Label(self.info_frame,text="Last pull the rss feed on "+first_podcast_data['lst_pull_date'])
        self.search_input = tk.Entry(self.info_frame)
        self.search_input_button = tk.Button(self.info_frame,text="Search")
        self.back_button_search = tk.Button(self.info_frame,text="Back")
        self.download_que_button = tk.Button(self.info_frame,text="Add episode to download que",command=self.add_episode_to_que)
        self.description_button = tk.Button(self.info_frame,text="Show episode description",command=self.show_episode_desc)

        # packing all the info frame elements
        self.title_label.grid(sticky='snew',columnspan=2)

        #self.episode_num_label.grid(column=0,row=2,stick='snew',columnspan=2)
        self.episode_num_label.grid(column=0,row=4,columnspan=2)
        self.podcast_cover_button.grid(column=0,row=3,columnspan=2)

        #self.lst_updated_label.grid(column=0,row=4,columnspan=2)
        self.lst_updated_label.grid(column=0,row=2,sticky='snew',columnspan=2)
        self.search_input.grid(column=0,row=5,columnspan=2)
        self.back_button_search.grid(column=1,row=5,sticky='e')
        self.search_input_button.grid(column=1,row=5)
        self.download_que_button.grid(column=0,row=6)
        self.description_button.grid(column=1,row=6)

        # packing info frame
        self.info_frame.pack(side=TOP)

        # creating podcast list_box
        self.list_box_frame = tk.Frame(self.root)
        self.podcast_list_box = tk.Listbox(self.list_box_frame,export=False)
        self.podcast_list_box.config(width=0,height=0)
        self.podcast_list_box.bind("<<ListboxSelect>>",self.change_podcast)
        podcast_scrollbar = tk.Scrollbar(self.list_box_frame)
        podcast_scrollbar.config(command=self.podcast_list_box.yview)
        self.podcast_list_box.config(yscrollcommand=podcast_scrollbar.set)

        # inserting podcast keys into podcast list_box
        for key in self.podcast_data.keys():

            podcast_title = podcast_data[key]['title']
            self.podcast_list_box.insert(key,podcast_title)

        self.podcast_list_box.select_set(0)
        podcast_scrollbar.pack(side=LEFT,fill=Y)
        self.podcast_list_box.pack(side=LEFT,expand=YES,fill=BOTH)

        # creates episode list_box
        self.episode_list_box = tk.Listbox(self.list_box_frame)
        self.episode_list_box.config(width=0,height=0)
        episode_scrollbar = tk.Scrollbar(self.list_box_frame)
        episode_scrollbar.config(command=self.episode_list_box.yview)
        self.episode_list_box.config(yscrollcommand=episode_scrollbar.set)
        episode_scrollbar.pack(side=RIGHT,fill=Y)
        self.episode_list_box.pack(side=RIGHT,expand=YES,fill=BOTH)
        self.episode_list_box.select_set(0)
        first_podcast_episodes = self.episode_data[0] 

        for key in first_podcast_episodes.keys():

            episode_title = first_podcast_episodes[key]['title']
            self.episode_list_box.insert(key,episode_title)


        self.list_box_frame.pack(side=TOP)

        for key in self.cover_paths:

            path = cover_paths[key]
            temp_image = PIL.Image.open(open(path,'rb'))
            temp_image.thumbnail((100,100))
            temp_tk_image = PIL.ImageTk.PhotoImage(temp_image)
            self.tk_image_holder.append(temp_tk_image)

        self.root.mainloop()

    def change_podcast(self,evt):

        podcast_listbox = evt.widget
        new_podcast_index = int(podcast_listbox.curselection()[0])

        if new_podcast_index!=self.current_podcast_index:

            new_episode_data = self.episode_data[new_podcast_index]
            new_podcast_data = self.podcast_data[new_podcast_index]

            # changing elements in the info frame
            self.title_label.config(text=new_podcast_data['title'])
            self.episode_num_label.config(text="There are "+str(new_podcast_data['episode_count'])+" in total")
            self.podcast_cover_button.config(image=self.tk_image_holder[new_podcast_index])
            self.lst_updated_label.config(text="Last pulled the rss feed on "+new_podcast_data['lst_pull_date'])

            # clears episode list_box
            self.episode_list_box.delete(0,END)

            for key in new_episode_data.keys():

                episode_title = new_episode_data[key]['title']
                self.episode_list_box.insert(key,episode_title)

            self.current_podcast_index = new_podcast_index


    def add_episode_to_que(self):

        current_episode_index = self.episode_list_box.curselection()

        if len(current_episode_index)!=0:

            que_item = []
            current_episode_index = current_episode_index[0]
            podcast_name = self.podcast_data[self.current_podcast_index]['title']
            episode_title = self.episode_data[self.current_podcast_index][current_episode_index]['title']
            episode_url = self.episode_data[self.current_podcast_index][current_episode_index]['episode_url']

            # seting que item values
            que_item.append(podcast_name)
            que_item.append(episode_url)
            que_item.append(self.download_path)

            if self.download_que.__contains__(episode_title) == False:

                print("Added the episode "+episode_title+" to the download que")
                self.download_que[episode_title] = que_item

    def add_episode_to_que_with_args(self,podcast_index,episode_index):

        que_item = []
        podcast_name = self.podcast_data[podcast_index]['title'] 
        episode_title = self.episode_data[podcast_index][episode_index]['title']
        episode_url = self.episode_data[podcast_index][episode_index]['episode_url']

        # setting que item values
        que_item.append(podcast_name)
        que_item.append(episode_url)
        que_item.append(self.download_path)

        if self.download_que.__contains__(episode_title) == False:

            print("Added the episode "+episode_title+" to the download que")
            self.download_que[episode_title] = que_item      

                
    def show_episode_desc(self):

        episode_index = self.episode_list_box.curselection()
        podcast_index = self.podcast_list_box.curselection()

        if len(episode_index) and len(podcast_index) !=0:

            episode_index = episode_index[0]
            podcast_index = podcast_index[0]
            episode_data = self.episode_data[podcast_index][episode_index]
            podcast_data = self.podcast_data[podcast_index]
            podcast_cover_path = self.cover_paths[podcast_index]

            # podcast runtime data
            runtime = episode_data['episode_runtime']

            # generate cover image
            temp_image = PIL.Image.open(open(podcast_cover_path,'rb'))
            temp_image.thumbnail((200,200))
            tk_image = PIL.ImageTk.PhotoImage(temp_image)

            # wrapping description text
            wrapper = textwrap.TextWrapper()
            episode_desc = wrapper.wrap(episode_data['desc'])

            # generates episode runtime strings
            episode_runtime = episode_data['episode_runtime']
            runtime_text = "Episode runtime:"
            runtime_string = ""

            if type(episode_runtime) == int:

                if episode_runtime == 0:

                    runtime_string = runtime_text+" undetermined"

                else:

                    runtime_string = runtime_text+" "+str(episode_runtime)+" minutes"

            else:

                if episode_runtime.find("{")==-1:

                    if episode_runtime!="0:00":

                        runtime_string = runtime_text+" "+episode_runtime

                    else:

                        runtime_string = runtime_text+" undetermined"

                if episode_runtime.find("{")!=-1:

                    runtime_string = runtime_text+" undetermined" 

                    
            # widget

            widget = tk.Toplevel()
            widget.geometry("500x500")
            podcast_title_label = tk.Label(widget,text=podcast_data['title'])
            cover_image_label = tk.Label(widget,image=tk_image)
            episode_title_label = tk.Label(widget,text=episode_data['title'])
            pub_date_label = tk.Label(widget,text="Pub Date: "+episode_data['pub_date'])
            episode_runtime_label = tk.Label(widget,text=runtime_string)
            divider_label = tk.Label(widget,text="---------------------------------------")
            close_button = tk.Button(widget,text="Close",command=lambda:widget.destroy())
            download_que_button = tk.Button(widget,text="Add episode to download que",command=lambda:self.add_episode_to_que_with_args(podcast_index,episode_index))

            # packing elements
            podcast_title_label.pack(side=TOP)
            cover_image_label.pack(side=TOP)
            episode_title_label.pack(side=TOP)
            pub_date_label.pack(side=TOP)
            episode_runtime_label.pack(side=TOP)
            download_que_button.pack(side=TOP)
            divider_label.pack(side=TOP)

            # creating desc label

            for wrap in episode_desc:

                temp_label = tk.Label(widget,text=wrap)
                temp_label.pack(side=TOP)
                
            
            close_button.pack(side=TOP)
            widget.mainloop()


# Running and creating the gui   
config_path = "..//config//podcast_sub.ini"
config_parser = configparser.ConfigParser()
config_parser.read(config_path)
download_path = config_parser['paths']['download_path']

# connecting to podcast db
con = create_connection(db_path)
cur = con.cursor()

# retriving data from db
podcast_data = return_podcast_data(cur,config_path,'podcast')
cover_paths = podcast_data['cover_paths']
podcast_data.pop('cover_paths')
episode_data = retrieve_episode_data(cur,'episode',len(podcast_data.keys()))

# Creating class instance
gui = Podcast_Gui(podcast_data,episode_data,cover_paths,download_path)
gui.gen_gui()




        
