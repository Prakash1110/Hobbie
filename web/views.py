from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .forms import ContactForm
from .models import Team, Project
from courses.models import Course
from shop.models import Product
from django.contrib.postgres.search import SearchVector,SearchQuery
from django.template import RequestContext
from django.db.models import Q
# Create your views here.

# def handler404(request, *args, **argv):
#     response = render('404.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 404
#     return response


# def handler500(request, *args, **argv):
#     response = render('500.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 500
#     return response

def home(request):
    form = ContactForm()
    teams = Team.objects.all()
    projects = Project.objects.all()
    return render(request, 'website/index.html',
                  {
                      'form': form,
                      'teams': teams,
                      'hobbielobie_projects': projects,
                  })


def aboutus(request):
    teams = Team.objects.all()
    projects = Project.objects.all()
    return render(request, 'website/about-us.html', {
        'teams': teams,
        'hobbielobie_projects': projects,
    })


def contactus(request):
    return render(request, 'website/contact.html', {})


def privacy(request):
    return render(request, 'ui/privacy.html')


def contactview(request):
    print('Contact view initialized')
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect("web:home")

    else:
        return HttpResponseForbidden()


def community(request):
    return render(request, 'community/index.html')



def Find(request):
    if request.method =="POST":
        searched =request.POST.get('searched')
        rcourses = Course.objects.filter(Q(title__icontains=searched) | Q(category__title__icontains=searched))
        rproducts = Product.objects.filter(Q(title__icontains=searched)| Q(category__name__icontains=searched))
        return render(request, 'website/search.html',{
                    'searched':searched, 'rcourses':rcourses,'rproducts':rproducts
                    
                    })
    return render(request, 'website/search.html',{})

    