from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.urls import reverse
from accounts.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Course(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=200, unique=True,
                            primary_key=True, auto_created=False, blank=False)
    short_description = models.TextField(blank=False, max_length=60)
    description = models.TextField(blank=False)
    outcome = models.CharField(max_length=400)
    prerequisite = models.CharField(max_length=400)
    language = models.CharField(max_length=200)
    price = models.IntegerField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    is_published = models.BooleanField(default=True)
    avg_rating = models.FloatField(
        validators=[MaxValueValidator(5.00)], default=0)
    num_of_rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:course-details', kwargs={"slug": self.slug})


class CourseModule(models.Model):
    serial_num = models.IntegerField(default=1)
    name = models.CharField(max_length=60)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return f'{self.course}:{self.serial_num}. {self.name}'


class CourseItem(models.Model):
    serial_num = models.IntegerField(default=1)
    course_module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='course_items')
    type = models.CharField(max_length=2, default='LS', choices=(
        ('LS', 'Lesson'),
        ('QZ', 'Quiz')
    ))

    def __str__(self):
        return f'{self.course_module}: Item {self.serial_num}'


class Lesson(models.Model):
    corres_course_item = models.OneToOneField(
        CourseItem, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    duration = models.FloatField(
        validators=[MinValueValidator(0.30), MaxValueValidator(30.00)])
    video_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    """Model definition for Quiz."""

    corres_course_item = models.OneToOneField(
        CourseItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    questions_count = models.IntegerField(default=0)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    label = models.TextField(max_length=1000)

    def __str__(self):
        return self.label


class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizTaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    correct_answers_num = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class SelectedChoice(models.Model):
    quiztaker = models.ForeignKey('QuizTaker', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE)

    def __str__(self):
        return self.question.label

# Course buying logic


class EnrolledCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='enrolls')
    buy_price = models.IntegerField(default=0)


class CourseOrder(models.Model):
    '''Model to keep track of courses enrolled at a "then" price.'''
    courses_enrolled = models.ManyToManyField(EnrolledCourse)
    datetime = models.DateTimeField(default=now)
    total = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=2, default='PN', choices=(
        ('PN', 'Pending'),
        ('SS', 'Successful'),
        ('FF', 'Failed')
    ))
    transaction_id = models.CharField(max_length=255, default="")
    bank_id = models.CharField(max_length=255, default="")
    transaction_date = models.DateTimeField(default=timezone.now)
    transaction_resp_code = models.CharField(max_length=50, default="")
    transaction_resp_msg = models.TextField(default="")


class Cart(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='course_cart')
    items_in_cart = models.ManyToManyField(Course, blank=True)
    number_of_items = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def has_course(self, course):
        course_slug = str(course.slug)
        return course_slug

    def __str__(self):
        return self.user.get_full_name() or str(self.user.id)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'{self.user.get_full_name()} rating : {self.rating} for course {self.course}'
