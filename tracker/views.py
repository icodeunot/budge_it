# Importing the required libraries'
import json
import calendar
from calendar import monthrange
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseRedirect
from .models import Project, Category, Expense
from django.views.generic import CreateView
from django.utils.text import slugify
from .forms import ExpenseForm


#------------------------ Views ------------------------#

def project_list(request):
    year = datetime.now().year

    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", 
              "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    days = ["M", "T", "W", "Th", "F", "Sa", "Su"]

    # Function to generate day and day-of-week pairs for a month
    def get_days_with_weekdays(year, month_num):
        first_day, num_days = calendar.monthrange(year, month_num)
        return [(day, days[(first_day + day - 1) % 7]) for day in range(1, num_days + 1)]

    # Generate data for all months
    month_days = [(month, get_days_with_weekdays(year, i + 1)) for i, month in enumerate(months)]

    return render(request, 'tracker/project-list.html', {
        'months': months,
        'month_days': month_days,  # Pass the dictionary of month-day data
        'year': year,
    })
		
# View for the project detail page
# It will return the details of the project and the list of expenses
def project_detail(request, project_slug):
	
	# Getting the project object
	project = get_object_or_404(Project,slug=project_slug)
	
	# Checking the request method
	# If the request method is GET, then it will return the project detail page
	if request.method == 'GET':
		category_list = Category.objects.filter(project=project)
		return render(request,'tracker/project-detail.html',{'project':project, 'expense_list': project.expenses.all(), 'category_list':category_list})
		
	# If the request method is POST, then it will create a new expense
	elif request.method == 'POST':
		# Getting the form data and checking that it is valid
		form = ExpenseForm(request.POST)
		if form.is_valid():
			
			# Getting the form data if it is valid
			title = form.cleaned_data['title']
			amount = form.cleaned_data['amount']
			category_name = form.cleaned_data['category']
			category = get_object_or_404(Category, project=project, name=category_name)
			
			# Creating the expense object and saving it
			Expense.objects.create(
				project=project,
				title=title,
				amount=amount,
				category=category
			).save()
			
	# If the request method is DELETE, then it will delete the expense
	elif request.method == 'DELETE':
	
		# Getting the expense id from the request body and deleting the expense
		id = json.loads(request.body)['id']
		expense = get_object_or_404(Expense,id=id)
		expense.delete()
		return HttpResponse('')
		
	# edirecting to the project detail page
	return HttpResponseRedirect(f'/{project_slug}/')
	
	
# View for the add project page
# It will create a new project
class ProjectCreateView(CreateView):
	
	# Defining the model, template, and fields
	model = Project
	template_name = 'tracker/add-project.html'
	fields = ['name','budget']
	
	# Defining the form_valid method to create the categories
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.save()
		
		
		categories = self.request.POST['categoriesString'].split(',')
		
		# Creating the categories and saving them
		for category in categories:
			Category.objects.create(
				project = self.object,
				name = category
			)
		return HttpResponseRedirect(self.get_success_url())
		
	# Defining the get_success_url method to redirect to the project detail page
	def get_success_url(self):
		return f'/{slugify(self.object.name)}/'
	