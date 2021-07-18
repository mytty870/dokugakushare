from django import forms
from .models import Post, User, Comment, CommentReply

class PostForm(forms.ModelForm):
 
    class Meta:
        model = Post
        fields = ['title', 'book_title', 'category', "tags", "content"]

        labels = {
            'category':"カテゴリー"
        }

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
        fields = ['username', 'icon', 'background_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = '名前'

        self.fields['icon'].widget.attrs['class'] = 'form-control'
        self.fields['icon'].widget.attrs['placeholder'] = 'アイコン'

        self.fields['background_image'].widget.attrs['class'] = 'form-control'
        self.fields['background_image'].widget.attrs['placeholder'] = 'ヘッダー画像'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ['comment_reply']

    
