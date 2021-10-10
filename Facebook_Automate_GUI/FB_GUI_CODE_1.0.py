from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
import os
from selenium import webdriver
import time

def login(chrome, fb_login_page, username, pswd, login_sleep_time = 30):
    #print(login_sleep_time, type(login_sleep_time))
    # accessing login page
    chrome.get(fb_login_page)

    # accessing the email input box
    email = chrome.find_element_by_xpath('//div[@class="clearfix _5466 _44mg"]/input')
    email.send_keys(username)

    # accessing the password input box
    password = chrome.find_element_by_xpath('//div[@class="_55r1 _1kbt"]/input')
    password.send_keys(pswd)

    # clicking on log in button
    chrome.find_element_by_xpath('//div[@class="_xkt"]/button').click()
    
    # letting login page to successfully load if there is dual authentication set up
    time.sleep(login_sleep_time)
    
def post_man(chrome, group_links, post_text, image, sleep_time = 10):
    i = 0
    for link in group_links:
        #print(link)
        try:
            time.sleep(sleep_time)
            chrome.get(link)

            # fetching page name
            page_name = chrome.find_element_by_xpath('//meta[@property="og:title"]').get_attribute('content')
            #page_list.append(page_name)
            
            try:
                # uploading image to the post
                input_image = chrome.find_element_by_xpath('//input[@type = "file"]')
                input_image.send_keys(image)
            except:
                write_something_button = chrome.find_element_by_xpath('//div[@class="oajrlxb2 b3i9ofy5 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 j83agx80 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x cxgpxx05 d1544ag0 sj5x9vvc tw6a2znq i1ao9s8h esuyzwwr f1sip0of lzcic4wl orhb3f3m czkt41v7 fmqxjp7s emzo65vh l9j0dhe7 abiwlrkh p8dawk7l bp9cbjyn btwxx1t3 buofh1pr idiwt2bm jifvfom9 kbf60n1y"]')
                write_something_button.click() 
                
            # accessing the text box
            text_box = chrome.find_element_by_xpath('//div[@class="notranslate _5rpu"][@role="textbox"]')
            text_box.send_keys(post_text)

            # clicking on post
            chrome.find_element_by_xpath('//div[@aria-label="Post"]').click()
            
            #print(f"Post on {page_name} successfull")
            display_log.insert(END, f"* Post on {page_name} successfull \n")
                
            i += 1
            
        except:
            #print(f"Error while posting on {page_name}")
            display_log.insert(END, f"* Error while posting on {page_name} \n")
            
    time.sleep(sleep_time)
    chrome.close()
    return i

image_file_path = ""
def start_post():
    username = enter_user.get()
    pswd = enter_pswd.get()
    filename = variable.get() + ".txt"
    try:
        fr = open('./Group_Files/'+filename,"r")
        group_links = fr.read()
        group_links = group_links.split(",")
        fr.close()
        post_text = enter_post.get("1.0",END)
        image = image_file_path

        # creating a webdriver
        options = webdriver.ChromeOptions() 
        options.add_argument("--disable-notifications") 
        options.add_argument("--start-maximized")
        #chrome = webdriver.Chrome(os.getcwd()+"\\chromedriver_1.exe",options=options)
        chrome = webdriver.Chrome("chromedriver_1.exe",options=options)
        # applying implicit wait
        chrome.implicitly_wait(30)
        fb_login_page = 'https://www.facebook.com/login'

        # calling login function
        if sleep_time2.get() != "":
            login_sleep_time = int(sleep_time2.get())
            login(chrome, fb_login_page, username, pswd, login_sleep_time = login_sleep_time)
        else:
            login(chrome, fb_login_page, username, pswd)

        # calling post_man function
        if sleep_time1.get() != "":
            sleep_time = int(sleep_time1.get())
            number_of_groups = post_man(chrome, group_links, post_text, image, sleep_time = sleep_time)
        else:
            number_of_groups = post_man(chrome, group_links, post_text, image)

        # printing "Posting Successfull on n Groups"
        messagebox.showinfo("Info", f"Posting successful on {number_of_groups} groups")

        #print(username)
        #print(pswd)
        #print(filename)
        #print(group_links)
        #print(post_text)
        #print(image)
        
    except:
        messagebox.showwarning("Warning", "Please select a valid Group File")      

    
def main():
    global group_files
    
    group_files = [""]

    try:
        for file in os.listdir("./Group_Files"):
            if file.endswith(".txt"):
                group_files.append(file.replace(".txt",""))
        #print(group_files)
    except:
        os.mkdir('./Group_Files')

def get_group_links():
    # getting the group link list entered by the user
    group_link_list = text_box2.get("1.0",END).strip("\n")
    
    # getting the filename 
    filename = text_box1.get()
    #print(filename)
    
    if group_link_list == "":
        # message that please enter group link
        messagebox.showwarning("Warning", "Please enter the group links")
        
    elif filename == "":
        # message that please enter filename
        messagebox.showwarning("Warning", "Please enter the filename")
    
    # makes sure that user has enteres a filename and is not pressing the Save Groups button by mistake
    if filename != "" and group_link_list != "":
        # deleting the contents of text_box2 (filename)
        text_box2.delete("1.0",END)
        
        # deleting the contents of text_box1 (group links)
        text_box1.delete("0",END)
    
        fr = open('./Group_Files/'+filename+".txt", "w")
        fr.write(group_link_list)
        fr.close()

        group_files.append(filename)
        #print(group_files)

        # clearing the menu of our dropdown
        dropdown['menu'].delete(0, 'end')

        # Insert list of new options (tk._setit hooks them up to var)
        for file in group_files:
            #print(file)
            dropdown['menu'].add_command(label=file, command = lambda value=file:variable.set(value))

main()
###############################################################################################################



###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
win = Tk()
win.title("Automate Facebook")
win.geometry('1100x600')
win.configure(bg='black')
win.resizable(False, False)
win.iconbitmap('GUI_icon.ico')
# for opening the window in the center of the screen
#win.eval('tk::PlaceWindow . center')

############################################################################################################################
# Class for adding right click functionality
class RightClicker:
    def __init__(self, e):
        commands = ["Cut","Copy","Paste"]
        menu = Menu(None, tearoff=0, takefocus=0)

        for txt in commands:
            menu.add_command(label=txt, command=lambda e=e,txt=txt:self.click_command(e,txt))

        menu.tk_popup(e.x_root + 40, e.y_root + 10, entry="0")

    def click_command(self, e, cmd):
        e.widget.event_generate(f'<<{cmd}>>')
############################################################################################################################
        
        
############################################################################################################################
# Entry box for username
enter_user = Entry(font=("arial",15))
enter_user.place(x = 5, y = 5)
enter_user.config(width=20)

# Label for username
username  = Label(win, text = "Enter Mobile or Email", font = ("Times New Roman", 13), background = 'white', foreground = "grey")
username.place(x = 5, y = 7) #placing label over entry box
username.config(width=24, height=1)

def reset_user(event):
    #global enter_user
    username.destroy()
    enter_user.focus_set()
    
# deletes text from enter_user entry box as soon as we click on it
# binds mouse click to the enter_user entry widget
username.bind("<Button-1>", reset_user)


def back_to_initial(event):
    global username
    if len(enter_user.get()) == 1 or len(enter_user.get()) == 0:
        username  = Label(win, text = "Enter Mobile or Email", font = ("Times New Roman", 13), background = 'white', foreground = "grey")
        username.place(x = 5, y = 7)
        username.bind("<Button-1>", reset_user)
        username.config(width=24, height=1)
        username.focus_set()
        
# binds backspace to enter_user entry widget
# gets back the initial_text1 when enter_user entry widget us empty
enter_user.bind("<BackSpace>", back_to_initial)

# binding right click event to enter_user
enter_user.bind("<Button-3>", RightClicker)
############################################################################################################################



############################################################################################################################
# Entry for password
enter_pswd = Entry(font=("arial",15))
enter_pswd.place(x = 5, y = 45)
enter_pswd.config(width=20, show="*")

# Label for password
pswd  = Label(win, text = "Enter Password", font = ("Times New Roman", 13), background = 'white',foreground = "grey")
pswd.place(x = 5, y = 47)
pswd.config(width=24, height=1)

def reset_pswd(event):
    #global enter_pswd
    pswd.destroy()
    enter_pswd.focus_set()
    
# deletes text from enter_user entry box as soon as we click on it
# binds mouse click to the enter_user entry widget
pswd.bind("<Button-1>", reset_pswd)


def back_to_initial2(event):
    global pswd
    if len(enter_pswd.get()) == 1 or len(enter_pswd.get()) == 0:
        pswd  = Label(win, text = "Enter Password", font = ("Times New Roman", 13), background = 'white', foreground = "grey")
        pswd.place(x = 5, y = 47)
        pswd.bind("<Button-1>", reset_pswd)
        pswd.config(width=24, height=1)
        pswd.focus_set()
        
# binds backspace to enter_user entry widget
# gets back the initial_text1 when enter_user entry widget us empty
enter_pswd.bind("<BackSpace>", back_to_initial2)
############################################################################################################################



############################################################################################################################
# Label for dropdown menu
file = Label(win, text = "Select Groups", font = ("Times New Roman", 15), background = 'black', foreground = "white")
file.place(x = 5, y = 85)

# creating dropdown menu for already available group lists
# setting variable for Strings
variable = StringVar()
variable.set(group_files[0])

dropdown = OptionMenu(
    win,
    variable,
    *group_files)

dropdown.place(x = 185, y = 85)
############################################################################################################################


############################################################################################################################
# Label for entering file name
file = Label(win, text = "Enter Filename", font = ("Times New Roman", 15), background = 'black', foreground = "white")
file.place(x = 5, y = 125)

# text box for entering file name for group links
text_box1 = Entry(font=("arial",15))
text_box1.place(x = 185, y = 125)

# binding right click event to text_box1
text_box1.bind("<Button-3>", RightClicker)
############################################################################################################################


############################################################################################################################
# Label for adding group links
add_group_links = Label(win, text = "Enter Group Links",font = ("Times New Roman", 15), background = 'black', foreground = "white")
add_group_links.place(x = 5,y = 165)

# text box for adding group links
text_box2 = scrolledtext.ScrolledText(win, wrap = WORD, width = 40, height = 5, font = ("Times New Roman",15))
text_box2.place(x = 185, y = 165)

# binding right click event to text_box2
text_box2.bind("<Button-3>", RightClicker)
############################################################################################################################



############################################################################################################################
# Label for adding Post text
post_text = Label(win, text = "Enter Post Text",font = ("Times New Roman", 15), background = 'black', foreground = "white")
post_text.place(x = 5,y = 325)

# Text Box for adding Post text
enter_post = Text(font=("arial",13), width=45, height = 4)
enter_post.place(x = 185, y = 325)

# binding right click event to enter_post
enter_post.bind("<Button-3>", RightClicker)
############################################################################################################################


############################################################################################################################
# Label for adding image
img = Label(win, text = "Add Image",font = ("Times New Roman", 15), background = 'black', foreground = "white")
img.place(x = 5,y = 425)

# Label for adding the name of the selected image
selected_img = Label(win, text = "",font = ("Times New Roman", 13), background = 'white', foreground = "black", width = 45)
selected_img.place(x = 185,y = 425)

supported_formats = r"*.png *.jpg *.jpeg"
def browseFiles():
    global image_file_path
    image_file_path = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = [("Image files", supported_formats)])
    selected_img.config(text = image_file_path)
    
button3 = Button(win, text = "Browse Files", font = ("Times New Roman", 10, "bold"), bg = 'white', fg = 'black', command = browseFiles).place(x = 185, y = 455)
############################################################################################################################


############################################################################################################################
# Creating a frame for displaying log
frame = Frame(win, borderwidth = 5)
frame.place(x = 854, y= 0, anchor = N)

l1 = Label(frame, text = "LOG", font = ("Times New Roman", 15), background = 'black', foreground = "white", width = 40)
l1.pack(side = TOP, fill = X, padx = 5, pady =5)

# scrolled text box for diaplaying log links
display_log = scrolledtext.ScrolledText(frame, wrap = WORD, width = 45, height = 20, font = ("Times New Roman",15))
display_log.pack(fill = X, side = LEFT, padx = 5, pady =5)


############################################################################################################################


############################################################################################################################
# Show Hide password button
def showHidePswd():  
    global status
    if status == 0:
        enter_pswd.config(show="")
        status = 1
    elif status ==  1:
        enter_pswd.config(show="*")
        status = 0

show_hide_pswd = Button(win, text = "Show Password", font = ("Times New Roman", 10, "bold"), bg = 'white', fg = 'black', command = showHidePswd).place(x = 255, y = 45)
status = 0
############################################################################################################################


############################################################################################################################
# button for fetching group links
button1 = Button(win, text = "Save Groups", font = ("Times New Roman", 10, "bold"), bg = 'white', fg = 'black', command = get_group_links).place(x = 515, y = 285)
############################################################################################################################


############################################################################################################################
# button for start posting
button2 = Button(win, text = "Start Post", font = ("Times New Roman", 15, "bold"), 
                 command = start_post, bg = 'white', fg = 'black', borderwidth = 5).place(x = 800, y = 510)
############################################################################################################################


############################################################################################################################
# labels and entry boxes for sleep_time1 and sleep_time2 
sl1 = Label(win, text = "Sleep 1", font = ("Times New Roman", 10), background = 'black', foreground = "white", width = 5)
sl1.place(x = 1000, y = 550)
sleep_time1 = Entry(font=("arial",10), width = 3)
sleep_time1.place(x = 1048, y = 550)

sl2 = Label(win, text = "Sleep 2", font = ("Times New Roman", 10), background = 'black', foreground = "white", width = 5)
sl2.place(x = 1000, y = 575)
sleep_time2 = Entry(font=("arial",10), width = 3)
sleep_time2.place(x = 1048, y = 575)
############################################################################################################################

win.mainloop()