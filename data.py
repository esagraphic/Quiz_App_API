my_data = [
    {'question': 'When is a middleware executed in Django?',
    'options': {
    'a': 'Before the view processing only', 
    'b': 'After the view processing only', 
    'c': 'Both before and after the view processing', 
    'd': 'During the response rendering only'
    }, 
    'correct_answer': 'c',
    'explanation': 'Middleware in Django is executed both before and after the view processing. It can modify the request before the vi',
    'example': "class CustomMiddleware:\\n    def __init__(self, get_response):\\n        self.get_response = get_response\\n\\n    def __call__(self, request):\\n        print('Before view')\\n        response = self.get_response(request)\\n        print('After view')\\n        return response", 
    'why_not': {
        'a': 'Middleware is not just before the view; it also processes the response.', 
        'b': 'Middleware does not run only after the view, it runs both before and after',
        'c': 'Middleware does not run only after the view, it runs both before and after', 
        'd': 'Middleware does not run only after the view, it runs both before and after'
        }
        },
          {
            'question': 'q 2', 'options': {'a': 'Before the view processing only', 'b': 'After the view processing only', 'c': 'Both before and after the view processing', 'd': 'During the response rendering only'}, 'correct_answer': 'c', 'explanation': 'Middleware in Django is executed both before and after the view processing. It can modify the request before the vi', 'example': "class CustomMiddleware:\\n    def __init__(self, get_response):\\n        self.get_response = get_response\\n\\n    def __call__(self, request):\\n        print('Before view')\\n        response = self.get_response(request)\\n        print('After view')\\n        return response", 'why_not': {'a': 'Middleware is not just before the view; it also processes the response.', 'b': 'Middleware does not run only after the view, it runs both before and after', 'c': 'Middleware does not run only after the view, it runs both before and after', 'd': 'Middleware does not run only after the view, it runs both before and after'}}, {'question': 'q3', 'options': {'a': 'Before the view processing only', 'b': 'After the view processing only', 'c': 'Both before and after the view processing', 'd': 'During the response rendering only'}, 'correct_answer': 'c', 'explanation': 'Middleware in Django is executed both before and after the view processing. It can modify the request before the vi', 'example': "class CustomMiddleware:\\n    def __init__(self, get_response):\\n        self.get_response = get_response\\n\\n    def __call__(self, request):\\n        print('Before view')\\n        response = self.get_response(request)\\n        print('After view')\\n        return response", 'why_not': {'a': 'Middleware is not just before the view; it also processes the response.', 'b': 'Middleware does not run only after the view, it runs both before and after', 'c': 'Middleware does not run only after the view, it runs both before and after', 'd': 'Middleware does not run only after the view, it runs both before and after'}}]