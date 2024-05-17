
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

#
# class CustomPagination:
#     def __init__(self, page_obj: Page, page_number: int, per_page: int):
#         self._page_number = page_number
#         self._per_page = per_page
#         self._page_obj = page_obj
#
#     def to_json(self):
#         page_obj = self._page_obj
#         return {
#             "page_number": self._page_number or 1,
#             "per_page": self._per_page or settings.REST_FRAMEWORK["PAGE_SIZE"],
#             "next_page": None if page_obj.number == page_obj.paginator.num_pages else page_obj.next_page_number(),
#             "prev_page": None if page_obj.number == 1 else page_obj.previous_page_number(),
#             "total_pages": page_obj.paginator.num_pages,
#             "total_count": page_obj.paginator.count,
#         }
