from django import forms
from .models import Post, User, Comment

class PostForm(forms.ModelForm):
 
    class Meta:
        model = Post
        fields = ['title', 'book_title', 'category', "tags", "content", "is_public"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトル'

        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['placeholder'] = '本文'

        self.fields['book_title'].widget.attrs['class'] = 'form-control'
        self.fields['book_title'].widget.attrs['placeholder'] = '使用している本の名前'

        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['placeholder'] = 'カテゴリー'

        self.fields['tags'].widget.attrs['class'] = 'form-control'
        self.fields['tags'].widget.attrs['placeholder'] = '細かい分野'

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'icon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = '名前'

        self.fields['icon'].widget.attrs['class'] = 'form-control'
        self.fields['icon'].widget.attrs['placeholder'] = 'アイコン'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def save_with_post(self, post_id, commit=True):
        comment = self.save(commit=False)
        comment.post = Post.objects.get(id=post_id)
        comment.no = Comment.objects.filter(post_id=post_id).count() + 1
        if commit:
            comment.save()
        return comment

    
