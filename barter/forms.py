
from django import forms
from .models import Barter, Branch
from posts.models import Post

class BarterForm(forms.ModelForm):
    class Meta:
        model = Barter
        fields = ['requesting_post']
        labels = {'requesting_post': 'Postular publicación'}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        requested_post = kwargs.pop('requested_post')
        super().__init__(*args, **kwargs)
        self.fields['requesting_post'].queryset = Post.objects.filter(
            author=user,
            category=requested_post.category
        )
