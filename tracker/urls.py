# Description: This file contains the urls for the tracker app


# Importing libraries
from django.contrib import admin
from django.urls import path, include
from .import views


# Defining the url patterns
urlpatterns = [
	path('',views.project_list,name='list'),
	path('add/',views.ProjectCreateView.as_view(),name='add'),
	path('<slug:project_slug>/',views.project_detail,name='detail'),
]
