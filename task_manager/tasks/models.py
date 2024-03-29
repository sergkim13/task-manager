from django.db import models
from django.utils.translation import gettext_lazy

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name=gettext_lazy('name'))
    description = models.TextField(max_length=5000, blank=True,
                                   verbose_name=gettext_lazy('description'))
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               verbose_name=gettext_lazy('status'))
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=gettext_lazy('author'),
                               related_name='author_id')
    labels = models.ManyToManyField(Label, through='TaskLabel', through_fields=('task', 'label'),
                                    blank=True, verbose_name=gettext_lazy('labels'))
    executor = models.ForeignKey(User, on_delete=models.PROTECT,
                                 verbose_name=gettext_lazy('executor'),
                                 related_name='executor_id', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=gettext_lazy('created_at'))

    class Meta:
        verbose_name: str = gettext_lazy('task')
        verbose_name_plural: str = gettext_lazy('tasks')

    def __str__(self) -> str:
        return self.name


class TaskLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
