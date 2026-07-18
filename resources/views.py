from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Resource

def _approved(request):
    member = getattr(request.user, 'member', None)
    return member and member.is_approved

@login_required
def resource_list(request):
    if not _approved(request):
        return HttpResponseForbidden('Approved members only.')
    resources = Resource.objects.all()
    return render(request, 'resources/resource_list.html', {'resources': resources})

@login_required
def resource_detail(request, pk):
    if not _approved(request):
        return HttpResponseForbidden('Approved members only.')
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, 'resources/resource_detail.html', {'resource': resource})
