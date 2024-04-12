from django.shortcuts import render, redirect

from django.views.generic import View
from service_objects.services import ServiceOutcome

from photo_app.services.comment.comment_for_photo import CommentForPhotoService
from photo_app.services.comment.edit import EditCommentService
from photo_app.services.comment.delete import DeleteCommentService
from photo_app.services.comment.show_comments import ShowCommentsService


class CommentView(View):
    #permission_classes = (IsAuthenticated)
    template_name = 'photo_app/detail_comment.html'

    def get(self, request, **kwargs):
        outcome = ServiceOutcome(ShowCommentsService, request.GET.dict() | {'photo':self.kwargs['photo']})
        context = {
            "page_obj": outcome.result['page_obj'],
            "page_number": outcome.result['page_number'],
            "photo": outcome.result['photo']
            }
        return render(request, template_name=self.template_name, context = context)

    def post(self, request, **kwargs):
        if request.POST['_method'] == 'POST':
            outcome = ServiceOutcome(
                CommentForPhotoService, request.POST.dict() |
                {
                'user': request.user if self.request.user.is_authenticated else None,
                'photo':self.kwargs['photo']
                })

        if request.POST['_method'] == 'PATCH':
            outcome = ServiceOutcome(
                EditCommentService, request.POST.dict())
            

        elif request.POST['_method'] == 'DELETE':
            outcome = ServiceOutcome(
                DeleteCommentService, request.POST.dict())
        
        return redirect('photo_app:detail', photo = self.kwargs['photo']) 
    