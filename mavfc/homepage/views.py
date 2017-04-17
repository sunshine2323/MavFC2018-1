from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages import success
from django.http import HttpResponse

from foodcomputer.models import *
from experiment.models import *


# def home(request):
#     # return HttpResponse("<h2>Hey!</h2>");
#     return render(request, 'homepage/Justpage.html')


class Homepage(View):

    #@method_decorator(login_required)
    def get(self, request, parent_template=None):
        if request.user.is_authenticated():
            if request.user.is_staff:
                pis = Pi.objects.all()
            else:
                pis = Pi.objects.filter(user = request.user)
            return render(
                request,
                'homepage/dashboard.html',
                {'pis': pis,
                 'parent_template': parent_template})
        else:
            return render(request, 'homepage/Justpage.html', {'parent_template': parent_template})

