from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.views.generic import View
from service_objects.services import ServiceOutcome

from photo_app.services.photo.detail import DetailPhotoService
from photo_app.services.photo.edit import EditPhotoService
from photo_app.services.photo.get_list_of_photos import ListOfPhotoService
from photo_app.services.photo.soft_delete import SoftDeletePhotoService
from photo_app.services.photo.restore import RestorePhotoService
from photo_app.services.photo.upload import UploadPhotoService

from photo_app.serializers import PhotoSerializer
from photo_app.utils import is_ajax

from models_app.models.photo.forms import UploadPhotoForm
from models_app.models.photo.models import Photo


class ListPhotoView(View):
    template_name = 'photo_app/list_of_photos.html'
    #permission_classes = (IsAuthenticatedOrReadOnly)

    def get(self, request, **kwargs):
        outcome = ServiceOutcome(
            ListOfPhotoService, request.GET.dict() | {
                'user': request.user if self.request.user.is_authenticated else None
            })

        if request.method == 'GET' and is_ajax(request):
            serialized_data = PhotoSerializer(outcome.result['page_obj'].object_list, many=True).data
            q_dict = {"posts": serialized_data, "page_number": outcome.result['page_number']}
            return JsonResponse(q_dict)

        elif request.method == 'GET' and not is_ajax(request):
            context = {"page_obj": outcome.result['page_obj'],
                       "page_number": outcome.result['page_number'],
                       "personal_list": outcome.result['personal_list'],
                       "personal_filter": outcome.result['personal_filter']}
            return render(request, template_name=self.template_name, context=context)


class DetailPhotoView(View):
    #permission_classes = (IsAuthenticatedOrReadOnly) 

    def get(self, request, **kwargs):
        outcome = ServiceOutcome(
            DetailPhotoService, request.GET.dict() | {"photo": self.kwargs["photo"], "detail_photo": True})

        context = {
            "photo": outcome.result['outcome_comments']['photo'],
            "page_obj": outcome.result['outcome_comments']['page_obj'],
            "page_number": outcome.result['outcome_comments']['page_number'],
        }

        return render(
            request, template_name='photo_app/detail_photo.html',
            context=context
        )


class UploadPhotoView(View):
    template_name = 'photo_app/upload_photos.html'
    #permission_classes = (IsAuthenticated)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={"form": UploadPhotoForm()})

    def post(self, request):
        outcome = ServiceOutcome(
            UploadPhotoService, request.POST.dict() | {
                'author': request.user if self.request.user.is_authenticated else None
            }, request.FILES.dict()
        )

        return redirect('photo_app:detail', photo=outcome.result.id)


class EditPhotoView(View):
    template_name = 'photo_app/edit_photo.html'
    #permission_classes = (IsAuthenticated)

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name,
            context={'photo': Photo.objects.get(id=self.kwargs['photo'])})

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            EditPhotoService, request.POST.dict() | {'photo': self.kwargs['photo']})
        return redirect('photo_app:detail', photo=self.kwargs['photo'])


class DeletePhotoView(View):
    #permission_classes = (IsAuthenticated)

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            SoftDeletePhotoService, request.POST.dict() | {'photo': self.kwargs['photo']})
        return redirect('photo_app:home')


class RestorePhotoView(View):
    #permission_classes = (IsAuthenticated)
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            RestorePhotoService, request.POST.dict() | {'photo': self.kwargs['photo']})
        return redirect('photo_app:detail', photo=self.kwargs['photo'])
