from tkinter import *
from tkinter import ttk
import winsound
from datetime import timedelta, date

item_details_root = None #this allows item_details_root to be referenced in an if statement even before the UI is created

class item:
	items = [] #this list is placed in here so that this object may be modified, moved and in general more flexible in future
	issued_items = []
	def __init__(self, title, description): #this sets the title and description of an item when it is first added
		self.title = title
		self.description = description
		self.issued = False
		self.items.append(self)
	def issue_item(self, issuer_name, issue_days): #this will issue the item to a person and set issue/return dates
		self.issuer_name = issuer_name
		self.issued = True
		self.date_issued = date.today()
		self.date_due = date.today() + timedelta(issue_days)
		self.issued_items.append(self)
	def return_item(self): #returns/unissues the item from a person
		self.issuer_name = None
		self.issued = False
		self.date_issued = None
		self.date_due = None
		self.issued_items.remove(self)
	def remove_item(self): #this will remove the last reference to this object in item.items, which leads to the object being garbage collected
		self.items.remove(self)
		
		if self in self.issued_items:
			self.issued_items.remove(self)
	def days_til_due(self):
		return (self.date_due - date.today()).days
	def get_info(self): #returns the required information about the item depending on whether it is issued or not.
		if self.issued == True:
			self_info = "Item Name: {}\nItem Description: {}\nCurrently Issued: {}\nIssuer Name: {}\nDate Issued: {}\nDate Due: {}\nDays til due: {}\n"
			self_info = self_info.format(self.title, self.description, self.issued, self.issuer_name, self.date_issued, self.date_due, self.days_til_due())
		else:
			self_info = "Item Name: {}\nItem Description: {}\nCurrently Issued: {}".format(self.title, self.description, self.issued)

		return self_info

def remove_item(item_name):
	for current_item in item.items:
		if current_item.title == item_name: #break the loop to keep current_item in namespace and able to be used to set the item info
			current_item.remove_item()
			break

	update_management_gui()
	update_issued_items()

def add_item(title, description, add_item_root): #will create the item in the catalog
	len_title = len(title.strip())
	if len_title > 5 and len_title < 30:
		len_description = len(description.strip())
		if len_description > 10 and len_description < 100:
			item(title.strip().title(), description.strip())
			add_item_root.destroy()
			update_issued_items()
			update_management_gui()
		else:
			print("Please enter a valid brief description")
	else:
		print("Please enter a valid title")
def add_item_gui():
	add_item_root = Tk()
	add_item_root.title("Add Item to Catalog")

	details_frame = ttk.LabelFrame(add_item_root, text="Item Details")
	details_frame.grid(row=0, column=0, padx=5, pady=5)

	name_label = ttk.Label(details_frame, text="Name:")
	name_label.grid(row=0,column=0, padx=5)

	name_entry = ttk.Entry(details_frame)
	name_entry.grid(row=0, column=1, columnspan=2, padx=5)

	description_label = ttk.Label(details_frame, text="Description:")
	description_label.grid(row=1, column=0, columnspan=3)

	description_entry = Text(details_frame, width=20, height=5)
	description_entry.grid(row=2, column=0, columnspan=3, pady=5)

	add_button = ttk.Button(add_item_root, text="Add Item", width=30, command=lambda:add_item(name_entry.get(), description_entry.get("1.0",END), add_item_root))
	add_button.grid(row=1,column=0)

def destroy_details():
	global item_details_root
	item_details_root.destroy()
	item_details_root = None
def view_item_details(item_id, open_override): #a window to view the selected item's details
	global item_details_root, details_info

	if item_details_root == None or open_override:
		item_details_root = Tk()
		item_details_root.title("Item Details")

		details_frame = ttk.LabelFrame(item_details_root, text="Item Details")
		details_frame.grid(row=0, column=0, padx=5, pady=5)

		details_info = StringVar(item_details_root)
		details_label = ttk.Label(details_frame, textvariable=details_info)
		details_label.grid(row=0, column=1)

		exit_button = ttk.Button(details_frame, text="Exit", width=20, command=lambda: item_details_root.destroy())
		exit_button.grid(row=1,column=0, columnspan=3)

		item_details_root.protocol("WM_DELETE_WINDOW", destroy_details)

	try: #this is to bypass an issue with ListBoxSelect firing on clicking another listbox
		item_name = item_id.get(item_id.curselection()[0])
	except IndexError:
		return

	for current_item in item.items:
		if current_item.title == item_name: #break the loop to keep current_item in namespace and able to be used to set the item info
			break

	item_info = current_item.get_info()
	details_info.set(item_info)

	item_details_root.mainloop()


def item_management_gui(): #the window created by this function allows for the creation, removal and general overview of items in the catalog
	global update_management_gui
	def update_management_gui():
		items_list.delete(0,END)
		for current_item in item.items:
			items_list.insert(0, current_item.title)
	items_root = Tk()
	items_root.title("Item Management")

	list_frame = ttk.LabelFrame(items_root, text="Item Catalog:")
	list_frame.grid(row=0, column=0, padx=10, pady=5)

	items_list = Listbox(list_frame, width=40)
	items_list.grid(row=0,column=0, columnspan=2, padx=5)

	details_button = ttk.Button(list_frame, width=39, text="View Details:", command=lambda: view_item_details(items_list, True))
	details_button.grid(row=1,column=0, pady=5)

	bot_frame = Frame(items_root)
	bot_frame.grid(row=1, column=0, pady=5)

	remove_button = ttk.Button(bot_frame, text="Remove Item", width=19, command=lambda: [remove_item(items_list.get(ACTIVE)), update_management_gui()])
	remove_button.grid(row=0,column=0)
	add_button = ttk.Button(bot_frame, text="Add Item", command=add_item_gui, width=19)
	add_button.grid(row=0,column=1)

	for current_item in item.items:
		items_list.insert(0, current_item.title)


def main(): #this runs the main GUI
	global update_issued_items
	def issue_item(item_name, issuer_name, issue_days, issue_item_root): #issues the item to a person after invalid name checks. - self explanitory
		if len(issuer_name) > 5 and len(issuer_name) < 25:
			try: #checks that the number of days is a valid integer
				issue_days = int(issue_days) #only having this statement in here rather than the whole block means that less code is being executed if this is unable to be executed
				if issue_days < 1:
					print("Please Enter a Valid number of days")
					return
			except ValueError:
				print("Please Enter a Valid number of days")
				return  #exits the issue_item command if the number of days is invalid

			for item_to_issue in item.items:
				if item_to_issue.title == item_name:
					break #this exits he loop and because it is not finished item_to_issue remains in memory

			item_to_issue.issue_item(issuer_name, issue_days) 
			issue_item_root.destroy()
			update_issued_items()
		else:
			print("Please enter a valid name") #eror message -- replace

	def return_item():
		item_name = items_open_list.get(ACTIVE)
		for current_item in item.issued_items:
			if current_item.title == item_name: #break the loop to keep current_item in namespace and able to be used to set the item info
				break

		current_item.return_item()
		update_issued_items()


	def issue_item_gui():
		issue_item_root = Tk()
		issue_item_root.title("Issue Item")

		issue_frame = ttk.LabelFrame(issue_item_root, text="Issue Item:")
		issue_frame.grid(row=0, column=0, padx=5, pady=3)

		item_title_label = ttk.Label(issue_frame, text="Item:")
		item_title_label.grid(row=0, column=0)

		item_name =items_open_list.get(ACTIVE)
		item_label = ttk.Label(issue_frame, text=item_name)
		item_label.grid(row=0, column=1)

		name_label = ttk.Label(issue_frame, text="Full name:")
		name_label.grid(row=1, column=0)

		issuer_name = StringVar(issue_item_root)
		name_entry = ttk.Entry(issue_frame, textvariable=issuer_name) #A StringVar is less efficient here and therefore it is not used :)
		name_entry.grid(row=1, column=1)

		days_label = ttk.Label(issue_frame, text="Days to Issue:")
		days_label.grid(row=2, column=0)

		issue_days = StringVar(issue_item_root)
		days_entry = ttk.Entry(issue_frame, textvariable=issue_days) #same as above
		days_entry.grid(row=2, column=1, pady=2)

		issue_button = ttk.Button(issue_item_root, text="Issue Item", width=33, command=lambda:issue_item(item_name, issuer_name.get(), issue_days.get(), issue_item_root))
		issue_button.grid(row=1, column=0)

	def update_issued_items(): #updates the listboxes of issued and returned items
		items_open_list.delete(0,END)
		items_issued_list.delete(0,END)
		for current_item in item.items:
			if not current_item in item.issued_items:
				items_open_list.insert(0, current_item.title)
			else:
				items_issued_list.insert(0, current_item.title)

	root = Tk()
	root.title("Bean's Phat Library")

	item("Big Oof", "A Big Phat Oof")

	top_frame = ttk.LabelFrame(root, text="Bean's Library System")
	top_frame.grid(row=0,column=0)

	title_label = ttk.Label(top_frame, text="Administrator")
	title_label.grid(row=0, column=0, columnspan=4)

	returned_label = ttk.Label(top_frame, text="Returned Items:")
	returned_label.grid(row=1, column=0, columnspan=2)

	items_open_list = Listbox(top_frame, width=40)
	items_open_list.grid(row=2,column=0)

	items_open_list.bind('<<ListboxSelect>>', lambda  event=None:view_item_details(items_open_list, False)) #ListboxSelect passes an event object

	issue_button = ttk.Button(top_frame, text="Issue Item", width=40, command=issue_item_gui)
	issue_button.grid(row=3, column=0, columnspan=2)

	issued_label = ttk.Label(top_frame, text="Items on loan:")
	issued_label.grid(row=1, column=2, columnspan=2)

	items_issued_list = Listbox(top_frame, width=40)
	items_issued_list.grid(row=2,column=2)
	items_issued_list.bind('<<ListboxSelect>>', lambda  event=None:view_item_details(items_issued_list, False)) #ListboxSelect passes an event object

	update_issued_items()

	return_button = ttk.Button(top_frame, text="Return Item", width=40, command=return_item)
	return_button.grid(row=3,column=2, columnspan=2)

	management_button = ttk.Button(top_frame, text="Item Management", width=82, command=item_management_gui)
	management_button.grid(row=4,column=0,columnspan=4)
	
	#view_item_details()
	root.mainloop()
main()