from django import forms
import material as M
from .models import Article, ArticleComment


class ArticleForm(forms.ModelForm):
    layout = M.Layout(M.Row('title'),
                      M.Row('content'),
                      M.Row('image'),
                      )

    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'image',
        ]


class CommentForm(forms.ModelForm):
    layout = M.Layout(M.Row('text'))

    class Meta:
        model = ArticleComment
        fields = [
            'text'
        ]
