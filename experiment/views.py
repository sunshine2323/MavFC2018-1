from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages import success, error
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.http import HttpResponse


from .utils import ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .models import *
from .forms import *

import csv


class ExperimentSearch(View):
    @method_decorator(login_required)
    def post(self, request, parent_template=None):
        q = request.POST['experimentQuery']
        if request.user.is_staff:
            experiments = Experiment.objects.filter(name__contains=q)
        else:
            experiments = Experiment.objects.filter(Q(name__contains=q) & (Q(pi__user__pk=request.user.pk) | Q(instances__instance_users__user__pk=request.user.pk)))
        return render(
            request,
            'experiment/experiment_list.html',
            {'experiments': experiments,
             'experimentQuery': q,
             'parent_template': parent_template})


class ExperimentList(View):
    @method_decorator(login_required)
    def get(self, request, parent_template=None):
        if request.user.is_staff:
            experiments = Experiment.objects.all()
        else:
            experiments = Experiment.objects.filter(Q(pi__user__pk=request.user.pk) | Q(instances__instance_users__user__pk=request.user.pk))
        return render(
            request,
            'experiment/experiment_list.html',
            {'experiments': experiments,
             'parent_template': parent_template})


class ExperimentDetail(View):
    model = Experiment
    model_name = 'Experiment'
    template_name = 'experiment/experiment_detail.html'
    parent_template = None

    @method_decorator(login_required)
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        if not (request.user.is_staff or request.user.pis.filter(pk=obj.pi.pk) or request.user.experiment_instances.filter(experiment_instance__experiment__pk=pk)):
            return HttpResponseForbidden()
        return render(
            request,
            self.template_name,
            {'obj': obj,
             'model_name': self.model_name,
             'parent_template': self.parent_template})


class ExperimentCreate(ObjectCreateMixin, View):
    form_class = ExperimentForm
    template_name = 'experiment/create_page.html'
    form_url = reverse_lazy('experiment:experiment_create')
    parent_template = None
    model_name = 'Experiment'


class ExperimentUpdate(ObjectUpdateMixin, View):
    form_class = ExperimentForm
    model = Experiment
    template_name = 'experiment/update_page.html'
    parent_template = None
    model_name = 'Experiment'


class ExperimentDelete(ObjectDeleteMixin, View):
    model = Experiment
    success_url = reverse_lazy('experiment:experiment_list')
    template_name = 'experiment/delete_confirm.html'
    parent_template = None
    model_name = 'Experiment'


class ExperimentRuleDetail(View):
    model = ExperimentRule
    model_name = 'Experiment Rule'
    template_name = 'experiment/experimentrule_detail.html'
    parent_template = None

    @method_decorator(login_required)
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        if not (request.user.is_staff or request.user.pis.filter(pk=obj.experiment.pi.pk) or request.user.experiment_instances.filter(experiment_instance__experiment__pk=obj.experiment.pk)):
            return HttpResponseForbidden()
        return render(
            request,
            self.template_name,
            {'obj': obj,
             'model_name': self.model_name,
             'parent_template': self.parent_template})


class ExperimentRuleCreate(View):
    form_class = ExperimentRuleForm
    parent_model = Experiment
    template_name = 'experiment/create_page.html'
    parent_template = None
    model_name = 'Experiment Rule'

    @method_decorator(login_required)
    def get(self, request, pk):
        parent = get_object_or_404(self.parent_model, pk=pk)
        if not (request.user.is_staff or request.user.pis.filter(pk=parent.pi.pk)):
            return HttpResponseForbidden()
        return render(
            request,
            self.template_name,
            {'form': self.form_class(pi_pk=parent.pi.pk, isupdate=False),
             'form_url': reverse('experiment:experimentrule_create', kwargs={'pk': pk}),
             'model_name': self.model_name,
             'parent_template': self.parent_template})

    @method_decorator(login_required)
    def post(self, request, pk):
        parent = get_object_or_404(self.parent_model, pk=pk)
        if not (request.user.is_staff or request.user.pis.filter(pk=parent.pi.pk)):
            return HttpResponseForbidden()
        bound_form = self.form_class(request.POST, pi_pk=parent.pi.pk, isupdate=False)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.experiment = parent
            new_obj.save()
            bound_form.save_m2m()
            success(request, self.model_name + ' was successfully added.')
            return redirect(new_obj)
        return render(
            request,
            self.template_name,
            {'form': bound_form,
             'form_url': reverse('experiment:experimentrule_create', kwargs={'pk': pk}),
             'model_name': self.model_name,
             'parent_template': self.parent_template})


class ExperimentRuleUpdate(ObjectUpdateMixin, View):
    form_class = ExperimentRuleUpdateForm
    model = ExperimentRule
    template_name = 'experiment/update_page.html'
    parent_template = None
    model_name = 'Experiment Rule'

    @method_decorator(login_required)
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        if not (request.user.is_staff or request.user.pis.filter(pk=obj.experiment.pi.pk)):
            return HttpResponseForbidden()
        return render(
            request,
            self.template_name,
            {'form': self.form_class(instance=obj, device_pk=obj.device.pk),
             'obj': obj,
             'model_name': self.model_name,
             'parent_template': self.parent_template})

    @method_decorator(login_required)
    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        if not (request.user.is_staff or request.user.pis.filter(pk=obj.experiment.pi.pk)):
            return HttpResponseForbidden()
        bound_form = self.form_class(request.POST, instance=obj, device_pk=obj.device.pk)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            success(request, self.model_name + ' was successfully updated.')
            return redirect(new_obj)
        return render(
            request,
            self.template_name,
            {'form': bound_form,
             'obj': obj,
             'model_name': self.model.__name__,
             'parent_template': self.parent_template})


class ExperimentRuleDelete(ObjectDeleteMixin, View):
    model = ExperimentRule
    success_url = reverse_lazy('experiment:experiment_list')
    template_name = 'experiment/delete_confirm.html'
    parent_template = None
    model_name = 'Experiment Rule'


class ExperimentInstanceDetail(View):
    model = ExperimentInstance
    model_name = 'Experiment Instance'
    template_name = 'experiment/experimentinstance_detail.html'
    parent_template = None

    @method_decorator(login_required)
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        if not (request.user.is_staff or request.user.pis.filter(pk=obj.experiment.pi.pk) or request.user.experiment_instances.filter(experiment_instance__experiment__pk=obj.experiment.pk)):
            return HttpResponseForbidden()
        return render(
            request,
            self.template_name,
            {'obj': obj,
             'model_name': self.model_name,
             'parent_template': self.parent_template})


class ExperimentInstanceCreate(ObjectCreateMixin, View):
    form_class = ExperimentInstanceForm
    template_name = 'experiment/create_page.html'
    form_url = reverse_lazy('experiment:experimentinstance_create')
    parent_template = None
    model_name = 'Experiment Instance'


class ExperimentInstanceUpdate(ObjectUpdateMixin, View):
    form_class = ExperimentInstanceForm
    model = ExperimentInstance
    template_name = 'experiment/update_page.html'
    parent_template = None
    model_name = 'Experiment Instance'


class ExperimentInstanceDelete(ObjectDeleteMixin, View):
    model = ExperimentInstance
    success_url = reverse_lazy('experiment:experiment_list')
    template_name = 'experiment/delete_confirm.html'
    parent_template = None
    model_name = 'Experiment Instance'


class ExperimentInstanceAdd(View):
    form_class = ExperimentInstanceAddForm
    parent_model = Experiment
    template_name = 'experiment/create_page.html'
    parent_template = None
    model_name = 'Experiment Instance'

    @method_decorator(login_required)
    def get(self, request, pk):
        parent = get_object_or_404(self.parent_model, pk=pk)
        if not (request.user.is_staff or request.user.pis.filter(pk=parent.pi.pk)):
            return HttpResponseForbidden()
        return render(
            request,
            self.template_name,
            {'form': self.form_class(experiment_pk=parent.pk),
             'form_url': reverse('experiment:experimentinstance_add', kwargs={'pk': pk}),
             'model_name': self.model_name,
             'breadcrumb_list': parent.get_add_inst_breadcrumbs(),
             'parent_template': self.parent_template
             })

    @method_decorator(login_required)
    def post(self, request, pk):
        parent = get_object_or_404(self.parent_model, pk=pk)
        if not (request.user.is_staff or request.user.pis.filter(pk=parent.pi.pk)):
            return HttpResponseForbidden()
        bound_form = self.form_class(request.POST, experiment_pk=parent.pk)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit = False)
            new_obj.experiment = parent
            new_obj.save()
            success(request, self.model_name + ' was successfully added.')
            return redirect(new_obj)
        return render(
            request,
            self.template_name,
            {'form': bound_form,
             'form_url': reverse('experiment:experimentinstance_add', kwargs={'pk': pk}),
             'model_name': self.model_name,
             'breadcrumb_list': parent.get_add_inst_breadcrumbs(),
             'parent_template': self.parent_template})


class ExperimentInstanceData(View):

    @method_decorator(login_required)
    def get(self, request, pk):
        expInst = get_object_or_404(ExperimentInstance, pk=pk)
        if not (request.user.is_staff or request.user.pis.filter(pk=expInst.experiment.pi.pk) or request.user.experiment_instances.filter(experiment_instance__experiment__pk=expInst.experiment.pk)):
            return HttpResponseForbidden()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="experiment_instance_data.csv"'
        writer = csv.writer(response)
        writer.writerow(['Device Name', 'Timestamp', 'Value', 'Is Anomily'])
        for device in expInst.experiment.pi.devices.all():
            for value in device.data.filter(timestamp__gte=expInst.start, timestamp__lte=expInst.end):
                writer.writerow([value.device.device_type.name, value.timestamp, value.data_value, value.is_anomaly])
        return response


class UserExperimentInstanceAdd(View):
    form_class = UserExperimentInstanceAddForm
    parent_model = ExperimentInstance
    template_name = 'experiment/create_page.html'
    parent_template = None
    model_name = 'User Experiment Instance'

    @method_decorator(login_required)
    def get(self, request, pk):
        parent = get_object_or_404(self.parent_model, pk=pk)
        if not (request.user.is_staff or request.user.pis.filter(pk=parent.experiment.pi.pk)):
            return HttpResponseForbidden()
        return render(
            request,
            self.template_name,
            {'form': self.form_class(parent=parent),
             'form_url': reverse('experiment:user_experimentinstance_add', kwargs={'pk': pk}),
             'model_name': self.model_name,
             'breadcrumb_list': parent.get_add_breadcrumbs(),
             'parent_template': self.parent_template
             })

    @method_decorator(login_required)
    def post(self, request, pk):
        parent = get_object_or_404(self.parent_model, pk=pk)
        if not (request.user.is_staff or request.user.pis.filter(pk=parent.experiment.pi.pk)):
            return HttpResponseForbidden()
        bound_form = self.form_class(request.POST, parent=parent)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.experiment_instance = parent
            new_obj.save()
            success(request, self.model_name + ' was successfully added.')
            return redirect(parent)
        return render(
            request,
            self.template_name,
            {'form': bound_form,
             'form_url': reverse('experiment:user_experimentinstance_add', kwargs={'pk': pk}),
             'model_name': self.model_name,
             'breadcrumb_list': parent.get_add_breadcrumbs(),
             'parent_template': self.parent_template})


class UserExperimentInstanceUpdate(ObjectUpdateMixin, View):
    form_class = UserExperimentInstanceForm
    model = UserExperimentInstance
    template_name = 'experiment/update_page.html'
    parent_template = None
    model_name = 'User Experiment Instance'
    cancel_url = ''


class UserExperimentInstanceDelete(ObjectDeleteMixin, View):
    model = UserExperimentInstance
    success_url = reverse_lazy('experiment:experiment_list')
    template_name = 'experiment/delete_confirm.html'
    parent_template = None
    model_name = 'User Experiment Instance'
    cancel_url = ''

