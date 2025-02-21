my_data = [
    {
        "question": "When is a middleware executed in Django?",
        "options": {
            "a": "Before the view processing only",
            "b": "After the view processing only",
            "c": "Both before and after the view processing",
            "d": "During the response rendering only"
        },
        "correct_answer": "c",
        "explanation": "Middleware in Django is executed both before and after the view processing. It can modify the request before the view and modify the response after the view.",
        "example": "class CustomMiddleware:\n    def __init__(self, get_response):\n        self.get_response = get_response\n\n    def __call__(self, request):\n        print('Before view')\n        response = self.get_response(request)\n        print('After view')\n        return response",
        "why_not": {
            "a": "Middleware is not just before the view; it also processes the response.",
            "b": "Middleware does not run only after the view, it runs both before and after.",
            "d": "Middleware can modify both request and response, not just during rendering."
        }
    },
    {
        "question": "Where do you add the middleware for Django in the project?",
        "options": {
            "a": "urls.py",
            "b": "views.py",
            "c": "models.py",
            "d": "settings.py"
        },
        "correct_answer": "d",
        "explanation": "Middleware is added in the 'MIDDLEWARE' list in the 'settings.py' file of a Django project. This allows Django to process requests and responses using the listed middleware classes.",
        "example": "MIDDLEWARE = [\n    'django.middleware.security.SecurityMiddleware',\n    'django.contrib.sessions.middleware.SessionMiddleware',\n    'django.middleware.common.CommonMiddleware',\n    'django.middleware.csrf.CsrfViewMiddleware'\n]",
        "why_not": {
            "a": "urls.py is for routing URLs, not for configuring middleware.",
            "b": "views.py contains the views, not middleware configurations.",
            "c": "models.py is for database models, not middleware."
        }
    },
    {
        "question": "In which order should AuthenticationMiddleware be placed in relation to SessionMiddleware?",
        "options": {
            "a": "Before",
            "b": "After",
            "c": "It doesn't matter",
            "d": "Both should be removed"
        },
        "correct_answer": "b",
        "explanation": "AuthenticationMiddleware should be placed after SessionMiddleware because it relies on session data to authenticate users.",
        "example": "MIDDLEWARE = [\n    'django.contrib.sessions.middleware.SessionMiddleware',\n    'django.contrib.auth.middleware.AuthenticationMiddleware'\n]",
        "why_not": {
            "a": "AuthenticationMiddleware needs session data, so it must run after SessionMiddleware.",
            "c": "The order matters, as AuthenticationMiddleware depends on sessions.",
            "d": "Both middlewares are necessary for proper authentication functionality."
        }
    },
    {
        "question": "What is the purpose of the get_response callable in custom middleware?",
        "options": {
            "a": "To handle the session",
            "b": "To process the next middleware or view",
            "c": "To generate the final response",
            "d": "To log the user in"
        },
        "correct_answer": "b",
        "explanation": "The `get_response` callable is used to process the next middleware or view in the middleware chain. It is passed when initializing the middleware and is called to continue the request processing flow.",
        "example": "class CustomMiddleware:\n    def __init__(self, get_response):\n        self.get_response = get_response\n\n    def __call__(self, request):\n        response = self.get_response(request)\n        return response",
        "why_not": {
            "a": "Session handling is handled by SessionMiddleware, not `get_response`.",
            "c": "`get_response` does not generate the final response, it passes control to the next middleware or view.",
            "d": "Logging in is handled by AuthenticationMiddleware, not `get_response`."
        }
    },
    {
        "question": "Which method in a class-based middleware is used to process each request?",
        "options": {
            "a": "handle_request",
            "b": "process_view",
            "c": "__call__",
            "d": "process_response"
        },
        "correct_answer": "c",
        "explanation": "The `__call__` method is used to process each request in class-based middleware. It is executed when the middleware is called with a request object.",
        "example": "class CustomMiddleware:\n    def __init__(self, get_response):\n        self.get_response = get_response\n\n    def __call__(self, request):\n        response = self.get_response(request)\n        return response",
        "why_not": {
            "a": "Django does not have a `handle_request` method for middleware.",
            "b": "`process_view` is for processing views before they are executed, not for handling requests directly.",
            "d": "`process_response` is used for modifying responses, not requests."
        }
    },
    {
        "question": "Which of the following is true about middleware in Django?",
        "options": {
            "a": "Middleware can modify only the request object",
            "b": "Middleware can modify only the response object",
            "c": "Middleware can access and modify both the request and the response",
            "d": "Middleware can only log requests and responses"
        },
        "correct_answer": "c",
        "explanation": "Middleware can access and modify both the request and the response. It can modify the request before passing it to the view and modify the response before sending it back to the client.",
        "example": "class CustomMiddleware:\n    def __init__(self, get_response):\n        self.get_response = get_response\n\n    def __call__(self, request):\n        response = self.get_response(request)\n        return response",
        "why_not": {
            "a": "Middleware can modify both the request and the response, not just the request.",
            "b": "Middleware can modify both the request and the response, not just the response.",
            "d": "Middleware can do much more than logging, like modifying request/response data."
        }
    },
    {
        "question": "Which model is used by Django’s authentication system to store user data?",
        "options": {
            "a": "Authentication",
            "b": "User",
            "c": "Profile",
            "d": "UserProfile"
        },
        "correct_answer": "b",
        "explanation": "Django’s authentication system uses the `User` model to store user data, which includes fields like username, password, and email for authentication.",
        "example": "from django.contrib.auth.models import User\n\nuser = User.objects.create_user(username='john', password='password123')",
        "why_not": {
            "a": "There is no `Authentication` model in Django.",
            "c": "The `Profile` model is used for additional user information, not for storing authentication data.",
            "d": "The `UserProfile` is not a built-in model in Django."
        }
    },
    {
        "question": "Which view is provided by Django to handle user registration by default?",
        "options": {
            "a": "CreateUserView",
            "b": "RegisterView",
            "c": "SignupView",
            "d": "Django does not provide a default registration view"
        },
        "correct_answer": "d",
        "explanation": "Django does not provide a default view for user registration. Developers need to create their own view or use third-party packages for registration.",
        "example": "def register(request):\n    if request.method == 'POST':\n        form = UserCreationForm(request.POST)\n        if form.is_valid():\n            form.save()\n            return redirect('login')\n    else:\n        form = UserCreationForm()\n    return render(request, 'register.html', {'form': form})",
        "why_not": {
            "a": "Django does not have a `CreateUserView`.",
            "b": "Django does not have a `RegisterView`.",
            "c": "Django does not have a `SignupView`."
        }
    },
    {
        "question": "How does Django store the authentication state for logged-in users?",
        "options": {
            "a": "In the session cookie",
            "b": "In the user profile model",
            "c": "In a custom authentication cookie",
            "d": "In the URL query parameters"
        },
        "correct_answer": "a",
        "explanation": "Django stores the authentication state in the session cookie. The session ID is stored in the `sessionid` cookie, which helps track the logged-in user across requests.",
        "example": "MIDDLEWARE = [\n    'django.contrib.sessions.middleware.SessionMiddleware',\n    'django.contrib.auth.middleware.AuthenticationMiddleware'\n]",
        "why_not": {
            "b": "The user profile model is not used for storing authentication state.",
            "c": "Django does not use custom authentication cookies by default.",
            "d": "Authentication state is not stored in URL query parameters."
        }
    }
]
