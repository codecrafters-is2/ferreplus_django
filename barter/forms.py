
from django import forms
from .models import Barter
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
        ).exclude(
            id__in=Barter.objects.filter(
                requested_post=requested_post
            ).values_list('requesting_post_id', flat=True)
        ).exclude(
            id__in=Barter.objects.filter(
                requesting_post=requested_post
            ).values_list('requested_post_id', flat=True)
        ).exclude(
            status='deleted'
        )
