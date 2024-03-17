from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django import forms

from . import util

from markdown2 import markdown
import random

class NewEntryForm(forms.Form):
    entry = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': 'search', 'placeholder': 'Title', 'readonly': 'readonly'}))
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'class': 'search', 'placeholder': 'Content'}))


def index(request):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as variable
        entry = request.POST["q"]

        # Check if the query matches the name of an encyclopedia entry
        content = util.get_entry(entry)

        # If entry exists
        if content:
            return HttpResponseRedirect(reverse('title', args=[entry]))
        # if entry doesnt not exist
        else:
            # Get a list of all entries (titles)
            titles = util.list_entries()
            entries = []
            # Add to a new list every title that has entry as substring
            for title in titles:
                if entry.lower() in title.lower():
                    entries.append(title)
            
            # Render the search page
            return render(request, "encyclopedia/search.html", {
                "entries": entries
            })

    # If request method is GET
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    # Check if the title matches the name of an encyclopedia entry
    content = util.get_entry(title)
    
    # If the content does not exist, render an error page showing an error message
    if not content:
        return render(request, "encyclopedia/error.html", {
            "error": 404,
            "message": "Requested page was not found."
        })
    # If the content exists, render a page showing that
    else:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": markdown(content)
        })


def create(request):
    # Check if method is POST
    if request.method == "POST":
        # Get the post values
        form = NewEntryForm(request.POST)
        
        # Check if form data is valid (server-side)
        if form.is_valid():
            title = form.cleaned_data["entry"]
            content = form.cleaned_data["content"]

        # Check if entry already exists
        for entry in util.list_entries():
            if title.lower() == entry.lower():
                # Render error message
                return render(request, "encyclopedia/error.html", {
                    "error": 409,
                    "message": "Entry already exists with the provided title."
                })
        else:
            # Save new entry
            util.save_entry(title, content)
            # Redirect to the new entry’s page
            return HttpResponseRedirect(reverse('title', args=[title]))

    # GET
    form = NewEntryForm()
    # Remove readonly from the entry input
    form.fields['entry'].widget.attrs.pop('readonly', None)
    return render(request, "encyclopedia/create.html", {
        "form": form
    })


def edit(request, title):
    # Check if method is POST
    if request.method == "POST":
         # Get the post values
        form = NewEntryForm(request.POST)
        
        # Check if form data is valid (server-side)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            content = form.cleaned_data["content"]
        
        # Replace entry
        util.save_entry(title, content)

        # Redirect to the entry’s page
        return HttpResponseRedirect(reverse('title', args=[title]))

    # GET
    content = util.get_entry(title.lower())
    # Create new form
    initial_data = {
        "entry":title,
        "content":content
        }
    form = NewEntryForm(initial=initial_data)
    # Render the edit.html page with a form
    return render(request, "encyclopedia/edit.html", {
        "form":form,
        "title":title
    })


def random_entry(request):
    # Get the list of entries
    entries = util.list_entries()
    
    # Get random number
    n = random.randint(0, len(entries)-1)

    # Try to redirect to this entry page
    try:
        return HttpResponseRedirect(reverse('title', args=[entries[n]]))
    except IndexError:
        return render(request, "encyclopedia/error.html", {
            "error": 500,
            "message": "List of entries is empty."
        })