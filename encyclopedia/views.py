from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import util
from markdown2 import Markdown
from django.http import HttpResponseRedirect

from django.urls import reverse


from django import forms

import random

markdowner=Markdown()

class search_form(forms.Form):
    search_input=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'search'}))

class new_page(forms.Form):
    title=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'textarea',
            'placeholder': 'Enter title', 'id': 'new-entry-title'}))
    content=forms.CharField(label="", widget=forms.Textarea(attrs={'class':'textarea',
        'id': 'new-entry'}))
class edit_page(forms.Form):
    content_text=forms.CharField(label="edit",widget=forms.Textarea(attrs={'class':'textarea'}))



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),"form":search_form()
    })

                                        
def search(request):
    if request.method=="POST":
        forms=search_form(request.POST)

        if forms.is_valid():
            search_items=[]
            cl_form=forms.cleaned_data['search_input']
            entry_all=util.list_entries()
            for entry in entry_all:
                if cl_form.lower() == entry.lower():
                    page = util.get_entry(cl_form)
                    page_converted = markdowner.convert(page)
                    return render(request, "encyclopedia/title.html", {
                        "form": search_form(),
                        'title': cl_form,
                        'converted_page': page_converted}
                                  )

                if cl_form.lower() in entry.lower():
                    search_items.append(entry)

        return render(request,"encyclopedia/search.html",{
                "results":search_items,
                "query":cl_form,
                "form":search_form()
            })

def get_page(request,title):
    page= util.get_entry(title)
    if page is None:
        return render(request,"encyclopedia/error.html",{'form':search_form()})
    converted_page=markdowner.convert(page)
    return render(request,"encyclopedia/title.html",{
                  'title':title,
                  'converted_page':converted_page,
                  'form':search_form()
                })

def createpage(request):
    if request.method == "POST":
        form= new_page(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            entries=util.list_entries()
            if title in entries:
                return render(request,"encyclopedia/error.html",{'form':search_form()})
            else:
                util.save_entry(title,content)
                page=util.get_entry(title)
                page_converted=markdowner.convert(page)
                context={
                    'form':search_form(),
                    'converted_page':page_converted,
                    'title':title
                }
                return render(request,"encyclopedia/title.html",context)


    return render(request,"encyclopedia/new_page.html",{
        'form':search_form(),
        'content':new_page()
    })

def edit(request,title):
    if request.method=='GET':
        page=util.get_entry(title)
        context={
            'form':search_form(),
            'edit':edit_page(initial={'content_text':page}),
            'title':title
        }
        return render(request,"encyclopedia/edit.html",context)

    else:
        form=edit_page(request.POST)
        if form.is_valid():
            content_text=form.cleaned_data['content_text']
            util.save_entry(title,content_text)
            page=util.get_entry(title)
            page_converted=markdowner.convert(page)
            context={
                'form':search_form(),
                'converted_page':page_converted,
                'title':title
            }
            return render(request,"encyclopedia/title.html",context)

def random_page(request):
    entries=util.list_entries()
    title=random.choice(entries)
    page=util.get_entry(title)
    converted_page=markdowner.convert(page)
    context={
        'form':search_form(),
        'converted_page':converted_page,
        'title':title
    }

    return render(request,"encyclopedia/title.html",context)


