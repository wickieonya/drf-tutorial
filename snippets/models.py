from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    code = models.TextField()
    linemos = models.BooleanField(default=False)
    language = models.CharField(
        max_length=100, default="python", choices=LANGUAGE_CHOICES
    )
    style = models.CharField(max_length=100, default="friendly", choices=STYLE_CHOICES)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return str(self.title)
