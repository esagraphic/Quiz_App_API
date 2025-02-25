#ModelViewSet

class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class QuizViewSet(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    
    def get_serializer_class(self):
        """Use different serializer for list/retrieve and create/update"""
        if self.action in ['list', 'retrieve']:
            return QuestionSerializer  # Read-only with answers
        return QuestionCreateSerializer  # Writable with nested answers

    def get_queryset(self):
        """Filter by quiz ID if provided"""
        quiz_pk = self.request.query_params.get('quiz_pk')
        if quiz_pk:
            return Question.objects.filter(quiz_id=quiz_pk).prefetch_related('answers')
        return super().get_queryset()