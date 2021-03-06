from django import forms
from saaskit_profile.models import UserProfile
from django.utils.translation import ugettext_lazy as _
from uni_form.helpers import FormHelper 

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(label=_('Email'), help_text=_('Email'), required=True)
    real_name = forms.CharField(label=_("Real Field"), help_text=_("I am real"))

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        initial = kwargs.pop('initial', {})
        if instance:
            initial['email'] = instance.user.email
        super(UserProfileForm, self).__init__(
            initial=initial, instance=instance, *args, **kwargs
        )


    class Meta:
        model = UserProfile
        exclude = ('user', )

    def save(self, user=None):
        if not self.instance.pk:
            profile = super(UserProfileForm, self).save(commit=False)
            profile.user = user
            profile.save()
        else:
            profile = super(UserProfileForm, self).save()

        if self.cleaned_data['email']:
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
