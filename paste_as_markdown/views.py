from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown2 import Markdown
import uuid

from .forms import MarkdownForm

pastes = {}

def index(request):
    if request.method == 'POST':
        form = MarkdownForm(request.POST)
        if form.is_valid():
            alias = form.cleaned_data.get('alias')
            if alias == '' or alias in pastes:
                alias = uuid.uuid4()
            pastes[str(alias)] = form.cleaned_data.get('content')
            print(pastes)
            return HttpResponseRedirect(f'/paste-as-markdown/{alias}')
    else:
        form = MarkdownForm()
    return render(request, 'paste_as_markdown/index.html', { 'form': form })

def show(request, alias):
    return render(request, 'paste_as_markdown/show.html', {
        'content': Markdown().convert(str(pastes.get(alias)))
    })