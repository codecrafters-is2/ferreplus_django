
from django import forms
from .models import Barter
from posts.models import Post

class BarterForm(forms.ModelForm):
    class Meta:
        model = Barter
        fields = ['requesting_post']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        requested_post = kwargs.pop('requested_post')
        super().__init__(*args, **kwargs)
        self.fields['requesting_post'].queryset = Post.objects.filter(
            author=user,
            category=requested_post.category
        )
