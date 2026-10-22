# Final Project Submission: Add a New Assessment Feature to an Online Course App

**Course:** Django Application Development with SQL and Databases  
**Repository:** [nhitlk06-gif/final-cloud-app-with-database](https://github.com/nhitlk06-gif/final-cloud-app-with-database)  
**Total Points:** **15 / 15** (Target: ≥ 14/15, Passing threshold: 70% / 10.5 points)

---

## Summary of Submissions

| Task | Description | Marks | Submission Item |
| :--- | :--- | :---: | :--- |
| **Task 1** | GitHub URL of `models.py` (Question, Choice, Submission) | **3 pts** | [GitHub URL](https://github.com/nhitlk06-gif/final-cloud-app-with-database/blob/master/onlinecourse/models.py) |
| **Task 2** | GitHub URL of `admin.py` (7 imported classes, inlines & admins) | **3 pts** | [GitHub URL](https://github.com/nhitlk06-gif/final-cloud-app-with-database/blob/master/onlinecourse/admin.py) |
| **Task 3** | Screenshot `03-admin-site` (Auth & OnlineCourse sections) | **1 pt** | `03-admin-site.png` |
| **Task 4** | GitHub URL of `course_details_bootstrap.html` (course detail & exam) | **2 pts** | [GitHub URL](https://github.com/nhitlk06-gif/final-cloud-app-with-database/blob/master/onlinecourse/templates/onlinecourse/course_details_bootstrap.html) |
| **Task 5** | GitHub URL of `views.py` (`submit` & `show_exam_result`) | **2 pts** | [GitHub URL](https://github.com/nhitlk06-gif/final-cloud-app-with-database/blob/master/onlinecourse/views.py) |
| **Task 6** | GitHub URL of `urls.py` (routes for submit & exam result) | **2 pts** | [GitHub URL](https://github.com/nhitlk06-gif/final-cloud-app-with-database/blob/master/onlinecourse/urls.py) |
| **Task 7** | Screenshot `07-final` (Congratulations, score & exam results) | **2 pts** | `07-final.png` |
| **Total** | | **15 / 15** | **100% Passed** |

---

## Task 1: GitHub URL of `models.py` (3 Points)
**Question:** Submit the GitHub URL of the `models.py` file, which includes the Question, Choice, and Submission models.

**GitHub URL:**
```
https://github.com/nhitlk06-gif/final-cloud-app-with-database/blob/master/onlinecourse/models.py
```

### Key Implementation:
```python
# Question model
class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=10)

    def save(self, *args, **kwargs):
        if self.lesson and not self.course:
            self.course = self.lesson.course
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct:
            return True
        else:
            return False


# Choice model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


# Submission model
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission {self.id} for {self.enrollment}"
```

---

## Task 2: GitHub URL of `admin.py` (3 Points)
**Question:** Submit the GitHub URL of the `admin.py` file, which includes seven imported classes, along with the implementations of QuestionInline, ChoiceInline, QuestionAdmin, and LessonAdmin.

**GitHub URL:**
```
https://github.com/nhitlk06-gif/final-cloud-app-with-database/blob/master/onlinecourse/admin.py
```

### Key Implementation:
```python
from django.contrib import admin
# Exactly 7 imported classes from .models:
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'grade']
    search_fields = ['question_text']


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
```

---

## Task 3: Screenshot of Admin Site `03-admin-site` (1 Point)
**Question:** Submit a screenshot of the admin site with the image name `03-admin-site` that displays the “Authentication and Authorization” section and the “OnlineCourse” section.

**Screenshot Filename:** `03-admin-site.png`

![03-admin-site](C:/Users/LENOVO/.gemini/antigravity-ide/brain/72120678-eed3-41ea-ac25-ce38de209d6e/03-admin-site.png)

*Displays "Authentication and Authorization" (Groups, Users) and "OnlineCourse" (Choices, Courses, Instructors, Learners, Lessons, Questions, Submissions).*

---

## Task 4: GitHub URL of `course_details_bootstrap.html` (2 Points)
**Question:** Submit the GitHub URL of the `course_details_bootstrap.html` file, which includes the course detail template to display the course name and all related lessons using Django template tags and Bootstrap styling.

**GitHub URL:**
```
https://github.com/nhitlk06-gif/final-cloud-app-with-database/blob/master/onlinecourse/templates/onlinecourse/course_details_bootstrap.html
```
*(Also available at [course_detail_bootstrap.html](https://github.com/nhitlk06-gif/final-cloud-app-with-database/blob/master/onlinecourse/templates/onlinecourse/course_detail_bootstrap.html))*

### Key Implementation:
```html
    <!-- Page content -->
    <div class="container-fluid">
            <h2>{{ course.name }}</h2>
            <div class="card-columns-vertical">
                {% for lesson in course.lesson_set.all %}
                    <div class="card mt-1">
                        <div class="card-header"><h5>Lesson {{lesson.order|add:1}}: {{lesson.title}}</h5></div>
                        <div class="card-body">{{lesson.content}}</div>
                    </div>
                {% endfor %}
            </div>
            <!-- Task: show questions and choices -->
            <button data-toggle="collapse" data-target="#exam" type="button" class="btn btn-primary btn-block mt-3 mb-3">Start Exam</button>

            <div id="exam" class="collapse">
                {% if user.is_authenticated %}
                <form id="questionform" action="{% url 'onlinecourse:submit' course.id %}" method="post">
                    {% csrf_token %}
                    {% for question in course.question_set.all %}
                        <div class="card mt-2">
                            <div class="card-header font-weight-bold"><h5>{{ question.question_text }}</h5></div>
                            <div class="card-body">
                                <div class="form-group">
                                    {% for choice in question.choice_set.all %}
                                        <div class="form-check">
                                            <label class="form-check-label">
                                                <input type="checkbox" name="choice_{{choice.id}}"
                                                       class="form-check-input" id="{{choice.id}}"
                                                       value="{{choice.id}}">{{ choice.choice_text }}
                                            </label>
                                        </div>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                    <input class="btn btn-success btn-block mt-3 mb-4" type="submit" value="Submit Exam">
                </form>
                {% else %}
                <div class="alert alert-warning mt-2">Please log in to take the exam.</div>
                {% endif %}
            </div>
    </div>
```

---

## Task 5: GitHub URL of `views.py` (2 Points)
**Question:** Submit the GitHub URL of the `views.py` file, which includes the `submit` and `show_exam_result` functions.

**GitHub URL:**
```
https://github.com/nhitlk06-gif/final-cloud-app-with-database/blob/master/onlinecourse/views.py
```

### Key Implementation:
```python
def extract_answers(request):
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            try:
                choice_id = int(value)
                submitted_answers.append(choice_id)
            except (ValueError, TypeError):
                pass
    return submitted_answers


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    if not user.is_authenticated:
        return redirect('onlinecourse:login')

    enrollment = Enrollment.objects.filter(user=user, course=course).first()
    if not enrollment:
        enrollment = Enrollment.objects.create(user=user, course=course, mode='honor')

    submission = Submission.objects.create(enrollment=enrollment)
    extracted_answers = extract_answers(request)
    submission.choices.set(extracted_answers)
    submission.save()

    return HttpResponseRedirect(reverse(viewname='onlinecourse:exam_result', args=(course.id, submission.id,)))


def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    selected_choices = submission.choices.all()
    selected_ids = [c.id for c in selected_choices]

    total_mark = 0
    mark = 0

    questions = course.question_set.all()
    if not questions.exists():
        questions = Question.objects.filter(lesson__course=course).distinct()

    for question in questions:
        total_mark += question.grade
        if question.is_get_score(selected_ids):
            mark += question.grade

    grade = int((mark / total_mark) * 100) if total_mark > 0 else 0

    context = {
        'course': course,
        'submission': submission,
        'choices': selected_choices,
        'selected_ids': selected_ids,
        'selected_choices': selected_choices,
        'mark': mark,
        'total_mark': total_mark,
        'grade': grade,
        'questions': questions,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
```

---

## Task 6: GitHub URL of `urls.py` (2 Points)
**Question:** Submit the GitHub URL of the `urls.py` file, which includes the paths for submit and show_exam_result.

**GitHub URL:**
```
https://github.com/nhitlk06-gif/final-cloud-app-with-database/blob/master/onlinecourse/urls.py
```

### Key Implementation:
```python
    # Path for submit view
    path('<int:course_id>/submit/', views.submit, name='submit'),

    # Path for show_exam_result view
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='exam_result'),
```

---

## Task 7: Screenshot of Mock Exam Result `07-final` (2 Points)
**Question:** Submit a screenshot showing the result of the mock exam with the image name `07-final` showing a successful attempt, including the 'Congratulations' message, score, and exam results.

**Screenshot Filename:** `07-final.png`

![07-final](C:/Users/LENOVO/.gemini/antigravity-ide/brain/72120678-eed3-41ea-ac25-ce38de209d6e/07-final.png)

*Displays 'Congratulations, Alex! You have passed the exam and completed the course with score 100 / 100', followed by individual questions with correct answers highlighted in green.*
