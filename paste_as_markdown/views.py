from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import IntegrityError
import markdown2
import uuid

from .forms import MarkdownForm
from .models import Markdown

def index(request):
    # error = ''

    if request.method == 'POST':
        form = MarkdownForm(request.POST)
        if form.is_valid():
            alias = form.cleaned_data.get('alias')
            if alias == '':
                alias = uuid.uuid4()
            try: 
                markdown = Markdown(content=form.cleaned_data.get('content'), alias=alias)
                markdown.save()
                return HttpResponseRedirect(f'/paste-as-markdown/{alias}')
            except IntegrityError:
                error = 'This alias already exists. Please choose another one.'  
    else:
        form = MarkdownForm()
    
    return render(request, 'paste_as_markdown/index.html', {
        'form': form,
        'error_msg': error
    })

def show(request, alias):
    return render(request, 'paste_as_markdown/show.html', {
        'content': markdown2.Markdown().convert(str(Markdown.objects.get(alias=alias)))
    })