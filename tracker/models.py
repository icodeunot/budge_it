# Importing the necessary libraries
from django.db import models
from django.utils.text import slugify

#-------------------------- Models --------------------------#


# Creating the project model to staore the project details lik name, slug, tracker
class Project(models.Model):
	
	# Defining the fields of the Poject model 
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100,unique=True,blank=True)
	budget = models.IntegerField()
	
	# Defining the save method to create the slug
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Project,self).save(*args, **kwargs)
		
	# Defining the budget_left method to calculate the budget left 
	# (Is this suuposed to mean budget reaining?)
	def budget_left(self):
		expense_list = Expense.objects.filter(project=self)
		total_expense_amount = 0
		for expense in expense_list:
			total_expense_amount += expense.amount	
		
		return self.budget - total_expense_amount
	 
	# Defining the total_transactions method to calculate the total number of transactions
	def total_transaction(self):
		expense_list = Expense.objects.filter(project=self)
		return len(expense_list)
		 
		 
# Creating the Category model to store the category details like name, project
class Category(models.Model):
	# Defining the fields of the Category model
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	
	
# Creating the Expense model to store the expense details like project, title, amount, category
class Expense(models.Model):
	# Defining the fields of the Expense model
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
	title = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=8, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	
	# Defining the Meta class to order the expenses by amount
	class Meta:
		ordering = ('-amount',)
