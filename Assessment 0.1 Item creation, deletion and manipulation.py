from tkinter import *
from tkinter import ttk
import winsound
from datetime import timedelta, date

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
def issue_item(item_name, issuer_name, issue_days): #issues the item to a person after invalid name checks. - self explanitory
	if len(issuer_name) > 5 and len(issuer_name) < 25:
			try: #checks that the number of days is a valid integer
				issue_days = int(issue_days) #only having this statement in here rather than the whole block means that less code is being executed if this is unable to be executed
			except ValueError:
				print("Please Enter a Valid number of days")
				return #exits the issue_item command if the number of days is invalid

			for item_to_issue in item.items:
				if item_to_issue.title == item_name:
					break #this exits he loop and because it is not finished item_to_issue remains in the namespace

			item_to_issue.issue_item(issuer_name, issue_days) 
	else:
		print("Please enter a valid name") #eror message -- replace

def main():
	pass
main()
