from tkinter import * #main GUI package
from tkinter import ttk #allows OS-themed styling
from datetime import timedelta, date, datetime #handles issue/due dates
from sql import * #handles saving and loading of the data
import random #allows pseudo-random number generation

try: #enables cross-platform support
	import winsound #if on windows enables sounds
	def play_sound_async(sound): #plays a sound asynchronously - saves me having to create a new thread myself
		winsound.PlaySound(sound, winsound.SND_ALIAS | winsound.SND_ASYNC) #error sound - this will play the sound asynchronously so the function doesn't have to wait
except:
	def play_sound_async(sound): #Mac/Linux has no 'winsound' package. This avoids errors being thrown.
		pass

class MainWindow: #Python convention is to CamelCase classes
	item_details_root = None  #initialises item_details_root as reference type
	notification_window = None #initialises the notification window as reference type
	def __init__(self):
		item_controller.main_window = self #allows item_controller object to reference (as ref. type) the main_window object

		self.root = Tk()
		self.root.title("Bean's Phat Library")
		self.root.resizable(0,0) #locks the window to a certain size
		self.root.geometry("+100+100")

		self.top_frame = ttk.LabelFrame(self.root, text="Bean's Library System") #Main frame that content is contained within
		self.top_frame.grid(row=0,column=0)

		title_label = ttk.Label(self.top_frame, text="Administrator")
		title_label.grid(row=0, column=0, columnspan=4)

		returned_label = ttk.Label(self.top_frame, text="Returned Items:")
		returned_label.grid(row=1, column=0, columnspan=2)

		self.items_open_list = Listbox(self.top_frame, width=40) #listbox for unissued items
		self.items_open_list.grid(row=2,column=0)

		self.items_open_list.bind('<<ListboxSelect>>', lambda  event=None:self.view_item_details(self.items_open_list)) #ListboxSelect passes an event object

		issue_button = ttk.Button(self.top_frame, text="Issue Item", width=40, command=self.issue_item_gui) #issues an item
		issue_button.grid(row=3, column=0, columnspan=2)

		issued_label = ttk.Label(self.top_frame, text="Items on loan:")
		issued_label.grid(row=1, column=2, columnspan=2)

		self.items_issued_list = Listbox(self.top_frame, width=40) #listbox for issued items
		self.items_issued_list.grid(row=2,column=2)
		self.items_issued_list.bind('<<ListboxSelect>>', lambda  event=None:self.view_item_details(self.items_issued_list)) #ListboxSelect passes an event object

		return_button = ttk.Button(self.top_frame, text="Return Item", width=40, command=item_controller.return_item) #returns an item
		return_button.grid(row=3,column=2, columnspan=2)

		management_button = ttk.Button(self.top_frame, text="Item Management", width=82, command=self.item_management_gui)
		management_button.grid(row=4,column=0,columnspan=4)

		self.root.protocol("WM_DELETE_WINDOW", self.destroy_window) #closes daughter-windows if main window closed.
		
		#loads items from database and loads the GUI
		item_controller.init_items()
		self.update_issued_items()

		#starts the window and primary initalisation of the program
		self.root.mainloop()

	def issue_item_gui(self): #form to fill out to issue an item
		self.issue_item_root = Tk()
		self.issue_item_root.title("Issue Item")
		self.issue_item_root.geometry("+100+100")
 
		self.issue_frame = ttk.LabelFrame(self.issue_item_root, text="Issue Item:")
		self.issue_frame.grid(row=0, column=0, padx=5, pady=3)

		item_title_label = ttk.Label(self.issue_frame, text="Item:")
		item_title_label.grid(row=0, column=0)

		item_name = self.items_open_list.get(ACTIVE)
		item_label = ttk.Label(self.issue_frame, text=item_name)
		item_label.grid(row=0, column=1)

		name_label = ttk.Label(self.issue_frame, text="Full name:") 
		name_label.grid(row=1, column=0)

		issuer_name = StringVar(self.issue_item_root)

		#entry for user's name
		name_entry = ttk.Entry(self.issue_frame, textvariable=issuer_name) #A StringVar is less efficient here and therefore it is not used :)
		name_entry.grid(row=1, column=1)

		#days to issue the item for - must be >=0 and <999. 
		days_label = ttk.Label(self.issue_frame, text="Days to Issue:")
		days_label.grid(row=2, column=0)

		issue_days = StringVar(self.issue_item_root)
		days_entry = ttk.Entry(self.issue_frame, textvariable=issue_days) #same as above
		days_entry.grid(row=2, column=1, pady=2)

		#issues the item provided it passes invalid and boundary tests
		issue_button = ttk.Button(self.issue_item_root, text="Issue Item", width=33, command=lambda:item_controller.issue_item(item_name, issuer_name.get(), issue_days.get(), self.issue_item_root))
		issue_button.grid(row=1, column=0)


	def update_management_gui(self): 
		self.items_list.delete(0,END) #clears the list.
		for current_item in item_controller.items:
			self.items_list.insert(0, current_item.title)

	def add_item_gui(self): #Form for creating a new item
		self.add_item_root = Tk()
		self.add_item_root.title("Add Item to catalogue")
		self.add_item_root.resizable(0,0)

		self.details_frame = ttk.LabelFrame(self.add_item_root, text="Item Details")
		self.details_frame.grid(row=0, column=0, padx=5, pady=5)

		name_label = ttk.Label(self.details_frame, text="Name:")
		name_label.grid(row=0,column=0, padx=5)

		#entry for the name of the item
		self.name_entry = ttk.Entry(self.details_frame)
		self.name_entry.grid(row=0, column=1, columnspan=2, padx=5)

		description_label = ttk.Label(self.details_frame, text="Description:")
		description_label.grid(row=1, column=0, columnspan=3)

		#entry for a description of the item
		self.description_entry = Text(self.details_frame, width=20, height=5)
		self.description_entry.grid(row=2, column=0, columnspan=3, pady=5)

		#adds the item provided it passes invalid and boundary tests
		add_button = ttk.Button(self.add_item_root, text="Add Item", width=30, command=lambda:item_controller.add_item(self.name_entry.get(), self.description_entry.get("1.0",END), self.add_item_root))
		add_button.grid(row=1,column=0)

	def item_management_gui(self): #Window for adding new items or removing current items
		self.items_root = Tk()
		self.items_root.title("Item Management")
		self.items_root.geometry("+100+100")

		self.list_frame = ttk.LabelFrame(self.items_root, text="Item catalogue:")
		self.list_frame.grid(row=0, column=0, padx=10, pady=5)

		self.items_list = Listbox(self.list_frame, width=40)
		self.items_list.grid(row=0,column=0, columnspan=2, padx=5)

		#view the details of the item in the item_details_gui window
		details_button = ttk.Button(self.list_frame, width=39, text="View Details:", command=lambda: self.view_item_details(self.items_list)) #
		details_button.grid(row=1,column=0, pady=5)

		#two frames separate the layout of the window
		bot_frame = Frame(self.items_root)
		bot_frame.grid(row=1, column=0, pady=5)

		#remove selected item
		remove_button = ttk.Button(bot_frame, text="Remove Item", width=19, command=lambda: [item_controller.remove_item(self.items_list.get(ACTIVE)), self.update_management_gui()]) #
		remove_button.grid(row=0,column=0)
		
		#add new item - opens GUI to handle this 
		add_button = ttk.Button(bot_frame, text="Add Item", command=self.add_item_gui, width=19)
		add_button.grid(row=0,column=1)

		for current_item in item_controller.items: #adds the list of items to the listbox
			self.items_list.insert(0, current_item.title)

	def view_item_details(self, item_id):
		if self.item_details_root == None: #prevents menu from being opened twice - so rather it just replaces
			self.item_details_root = Tk()
			self.item_details_root.title("Item Details")
			self.item_details_root.resizable(0,0) #non-resizable
			self.item_details_root.geometry("+610+100")

			#details are stored in this frame
			self.details_frame = ttk.LabelFrame(self.item_details_root, text="Item Details")
			self.details_frame.grid(row=0, column=0, padx=5, pady=5)

			self.details_info = StringVar(self.item_details_root)
			details_label = ttk.Label(self.details_frame, textvariable=self.details_info)
			details_label.grid(row=0, column=1)


		try: #this is to bypass an issue with ListBoxSelect firing on clicking another listbox
			item_name = item_id.get(item_id.curselection()[0])
		except IndexError: #do nothing
			return

		for current_item in item_controller.items:
			if current_item.title == item_name: #break the loop to keep current_item in namespace and able to be used to set the item info
				break

		item_info = current_item.get_info() #gets the text for the active item
		self.details_info.set(item_info) #sets the text for the active item

		self.item_details_root.mainloop() #initialise the window

	def destroy_window(self):
		self.root.destroy() #destroys the main window
		try:
			self.item_details_root.destroy()
		except: #this just prevents a little error message if you close the main window before item_details_root is declared. No real problem with it though.
			pass

	def error_notif(self, message): #error notification window
		if not self.notification_window == None or message == "destroy": #this means that spamming an invalid option won't create multiple menus 
			self.notification_window.destroy()
			self.notification_window = None
			if message == "destroy":
				return None
		self.notification_window = Tk()
		self.notification_window.title("Error")
		self.notification_window.geometry("+450+250")

		notification_label = ttk.Label(self.notification_window, text=message)
		notification_label.grid(row=0,column=0)

		exit_button = ttk.Button(self.notification_window, text="Exit", command=lambda: self.error_notif("destroy")) #this prevents closing the menu from causing issues when opening it again in future
		exit_button.grid(row=0,column=1)

		self.notification_window.protocol("WM_DELETE_WINDOW", lambda: main_window.error_notif("destroy")) #this prevents closing the menu from causing issues when opening it again in future
		
		play_sound_async("SystemExit") #this is the default Windows 10 error sound

	def update_issued_items(self): #updates the listboxes of issued and returned items
		self.items_open_list.delete(0,END)
		self.items_issued_list.delete(0,END)
		for current_item in item_controller.items:
			if not current_item in item_controller.issued_items:
				self.items_open_list.insert(0, current_item.title)
			else:
				self.items_issued_list.insert(0, current_item.title)


class Item: #class for each individual item
	def __init__(self, title, description, uid=None): #this sets the title and description of an item when it is first added
		self.title = title
		self.description = description
		self.issued = False
		self.issuer_name = None
		self.issued = None
		self.date_issued = None
		self.date_due = None
		item_controller.item_names.append(self.title)
		if uid == None:
			while True: #assigns a unique id to the item - better to do it here than SQL for a small program
				self.uid = random.randint(0,100000)
				if not(self.uid in item_controller.item_uids):
					break
		else:
			self.uid = uid
		item_controller.items.append(self)
	def issue_item(self, issuer_name, issue_days): #this will issue the item to a person and set issue/return dates
		self.issuer_name = issuer_name
		self.issued = True
		self.date_issued = date.today()
		self.date_due = date.today() + timedelta(issue_days)
		sql_controller.update(self)
		item_controller.issued_items.append(self)
	def load_item(self, issuer_name, date_issued, date_due):
		self.issuer_name = issuer_name
		self.issued = True
		self.date_issued = date_issued
		self.date_due = date_due
		item_controller.issued_items.append(self)
	def return_item(self): #returns/unissues the item from a person
		self.issuer_name = None
		self.issued = False
		self.date_issued = None
		self.date_due = None
		sql_controller.update(self)
		item_controller.issued_items.remove(self)
	def remove_item(self): #this will remove the last reference to this object in item_controller.items, which leads to the object being garbage collected
		item_controller.items.remove(self)
		sql_controller.delete(self.uid)
		if self in item_controller.issued_items:
			item_controller.issued_items.remove(self)
	def days_til_due(self): #gets the days until the item is due
		return (self.date_due - date.today()).days
	def get_info(self): #returns the required information about the item depending on whether it is issued or not.
		if self.issued == True:
			self_info = "Item Name: {}\nItem Description: {}\nCurrently Issued: {}\nIssuer Name: {}\nDate Issued: {}\nDate Due: {}\nDays til due: {}\n"
			self_info = self_info.format(self.title, self.description, self.issued, self.issuer_name, self.date_issued, self.date_due, self.days_til_due())
		else:
			self_info = "Item Name: {}\nItem Description: {}\nCurrently Issued: {}".format(self.title, self.description, self.issued)

		return self_info

class ItemController: #a class for handling management actions on each item
	items = [] #python doesn't have property accessors..... :(
	issued_items = []
	item_names = []
	def __init__(self):
		self.item_uids = sql_controller.get_uids()
		#print(self.item_uids) #debug
	def init_items(self): #loads the items from the database on program start
		library_db = sql_controller.fetch()
		for current_item in library_db:
			item_details = list(current_item)

			new_item = Item(item_details[1], item_details[2].strip(), item_details[0])
			if (item_details[4] == "1"): #datetime.strptime(item_details[4].strip(), '%m-%d-%Y').date()
				new_item.load_item(item_details[3].strip(), datetime.strptime(item_details[5].strip(), '%Y-%m-%d').date(),datetime.strptime(item_details[6].strip(), '%Y-%m-%d').date())

	def return_item(self): #sets an item's status to returned
		item_name = self.main_window.items_open_list.get(ACTIVE)
		for current_item in item_controller.issued_items:
			if current_item.title == item_name: #break the loop to keep current_item in namespace and able to be used to set the item info
				break

		current_item.return_item()
		self.main_window.update_issued_items()

	def issue_item(self, item_name, issuer_name, issue_days, issue_item_root): #issues the item to a person after invalid name checks. - self explanitory
		if len(issuer_name) > 4 and len(issuer_name) < 25: 
			try: #checks that the number of days is a valid integer
				issue_days = int(issue_days) #only having this statement in here rather than the whole block means that less code is being executed if this is unable to be executed
				if issue_days <= 0 or issue_days > 999: # prevents issuing of item for a negative or >999 number of days 
					raise ValueError #throws ValueError
			except ValueError:
				self.main_window.error_notif("Please Enter a Valid number of days")
				return  #exits the issue_item command if the number of days is invalid

			for item_to_issue in item_controller.items:
				if item_to_issue.title == item_name:
					break #this exits he loop and because it is not finished item_to_issue remains in memory

			item_to_issue.issue_item(issuer_name, issue_days) 
			self.main_window.issue_item_root.destroy()
			self.main_window.update_issued_items()
		else:
			self.main_window.error_notif("Please enter a valid name") #eror message -- replace
		
	def remove_item(self, item_name): #removes an item from the catalogue
		for current_item in item_controller.items:
			if current_item.title == item_name: #break the loop to keep current_item in namespace and able to be used to set the item info
				current_item.remove_item()
				break

		self.main_window.update_management_gui()
		self.main_window.update_issued_items()

	def add_item(self, title, description, add_item_root): #will create the item in the catalogue
		len_title = len(title.strip())
		if len_title > 4 and len_title < 30: #boundary checks to make sure that the name is a valid length
			if title.strip() in self.item_names:
				self.main_window.error_notif("Item Titles must be unique")
			else:
				len_description = len(description.strip())
				if len_description > 5 and len_description < 100: #prevents the length of the description being too short or too long
					new_item = Item(title.strip().title(), description.strip())
					sql_controller.insert(new_item)
					add_item_root.destroy()
					self.main_window.update_issued_items()
					self.main_window.update_management_gui()

				else:
					self.main_window.error_notif("Please enter a valid brief description")
		else:
			self.main_window.error_notif("Please enter a valid title")

sql_controller = Sql() 
item_controller = ItemController()
main_window = MainWindow() #creates the MainWindow which handles primary flow of the progrea,