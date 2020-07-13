from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'photo']

        def __init__(self, *args, **kwargs):
            super.fields['photo'].required = False
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
        widgets = {
            'content' : forms.TextInput(attrs={'placeholder':'댓글을 입력하세요'})
        }
        