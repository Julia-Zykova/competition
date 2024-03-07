from django.core.paginator import Page
from conf.settings import django as settings            

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



class CustomPagination:
    def __init__(self, page: Page, current_page: int, per_page: int):
        self._current_page = current_page
        self._per_page = per_page
        self._page = page

    def to_json(self):
        page = self._page
        return {
            "current_page": self._current_page or 1,
            "per_page": self._per_page or settings.REST_FRAMEWORK["PAGE_SIZE"],
            "next_page": None if page.number == page.paginator.num_pages else page.next_page_number(),
            "prev_page": None if page.number == 1 else page.previous_page_number(),
            "total_pages": page.paginator.num_pages,
            "total_count": page.paginator.count,
        }
