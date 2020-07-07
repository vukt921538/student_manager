from django import forms
from .models import *

class PostForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề'}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nội dung'}))

    class Meta:
        model = Post
        fields = ('title', 'content', 'author')

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.fields['author'].widget = forms.HiddenInput()

class CommentForm(forms.ModelForm):
    comment_box = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bình luận của bạn'}))
    class Meta:
        model = Comment
        fields = '__all__'
        
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['post'].widget = forms.HiddenInput()


class CtcForm(forms.ModelForm):
    class Meta:
        model = Comment_to_comment
        fields = '__all__'