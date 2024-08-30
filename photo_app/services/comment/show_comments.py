from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from service_objects.services import ServiceWithResult

from models_app.models import Comment, Photo


class ShowCommentsService(ServiceWithResult):
    photo = forms.IntegerField(required=False)
    page = forms.IntegerField(min_value=1, initial=1, required=False)
    detail_photo = forms.BooleanField(initial=False, required=False)

    def process(self):
        if self.is_valid():
            self.result = self._get_page
        return self

    @property
    def _photo(self):
        photo = Photo.objects.get(id=self.cleaned_data["photo"])
        return photo

    @property
    def _get_page(self):

        qs = Comment.objects.filter(photo=self._photo)

        if self.cleaned_data["detail_photo"]:
            p = Paginator(qs, 3)
        else:
            p = Paginator(qs, 6)

        page_number = self.cleaned_data["page"]

        if page_number is None:
            page_number = self.fields["page"].initial

        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)

        return {"page_number": page_number, "page_obj": page_obj, "photo": self._photo}
