from django.contrib.auth.models import User, AbstractUser
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)

class Category(models.Model):
    dd = 'DD'
    tank = 'TANK'
    heal = 'HEAL'
    td = 'TREADER'
    gm = 'GUILDMASTER'
    qg = 'QUESTGIVER'
    bs = 'BLACKSMITH'
    tn = 'TANNER'
    pn = 'POTIONEER'
    sm = 'SPELLMASTER'

    CATEGORY_TYPES = [
        (dd, 'ДД'),
        (tank, 'Танк'),
        (heal, 'Хил'),
        (td, 'Торговец'),
        (gm, 'Гилдмастер'),
        (qg, 'Квестгивер'),
        (bs, 'Кузнец'),
        (tn, 'Кожевник'),
        (pn, 'Зельевар'),
        (sm, 'Мастер заклинаний')
    ]

    name = models.CharField(max_length=11, choices=CATEGORY_TYPES, default=dd)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return dict(Category.CATEGORY_TYPES)[self.name]

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = RichTextUploadingField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=Category.dd)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/board/{self.id}'

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    #false - отклик не принят
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return f'/board/personal'
