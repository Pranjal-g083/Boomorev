from django import forms
from .models import Comment, Reply


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Comment here !',
            'rows': 4,
            'cols': 50
        }))

    class Meta:
        model = Comment
        fields = ['comment']


class CommentEditForm(forms.ModelForm):
    comment = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            # 'class': 'form-control comment_class',
            'placeholder': 'Comment here !',
            'rows': 4,
            'cols': 50
        }))

    class Meta:
        model = Comment
        fields = ['comment']


class ReplyForm(forms.ModelForm):
    reply = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Reply',
            'rows': 2,
        }))

    class Meta:
        model = Reply
        fields = ['reply']


class ReplyEditForm(forms.ModelForm):
    reply = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Reply',
            'rows': 2,
        }))

    class Meta:
        model = Reply
        fields = ['reply']
