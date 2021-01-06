from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

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
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        """
        User the 'pygments' library to create a highlighted HTML representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linemos = 'table' if self.linemos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linemos=linemos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return str(self.title)
