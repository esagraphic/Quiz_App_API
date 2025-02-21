from django.http import HttpResponseRedirect
from django.urls import resolve, reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # List of views that require login (this can be the view names defined in your URL configuration)
   

    

    def __call__(self, request):
        # Ensure that we have a resolved view name and check against the protected views list
        protected_views = [
            'create_subject', 'add_question', 'create_category', 'create_quiz'
        ]  # example views to protect
        current_url_target_name = resolve(request.path_info).url_name
        if current_url_target_name in protected_views and not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        response = self.get_response(request)
        return response
