from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from recipe.models import RecipeItem, Author
from recipe.forms import RecipeAddForm, AuthorAddForm, LoginForm


def loginview(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
    form = LoginForm()
    return render(request, 'generic_form.html', {'form': form})


def index(request):
    data = RecipeItem.objects.all()
    return render(request, 'index.html', {'data': data})


@login_required
def add_recipe(request):
    html = "generic_form.html"

    if request.method == "POST":
        form = RecipeAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            RecipeItem.objects.create(
                title=data['title'],
                description=data['description'],
                author=data['author']
            )
            return HttpResponseRedirect(reverse('homepage'))

    form = RecipeAddForm()

    return render(request, html, {"form": form})


@login_required
def add_author(request):
    html = "generic_form.html"

    if request.method == "POST":
        form = AuthorAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data['name'],
                bio=data['bio']
            )
        return HttpResponseRedirect(reverse('homepage'))

    form = AuthorAddForm()

    return render(request, html, {'form': form})


def author(request, id):
    author = Author.objects.get(id=id)
    recipe = RecipeItem.objects.filter(author=author)
    return render(request, 'authorinfo.html', {'author': author, 'recipe': recipe})


def recipe(request, id):
    recipe = RecipeItem.objects.get(id=id)
    return render(request, 'recipe.html', {'recipe': recipe})
