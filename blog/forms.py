from django import forms
from .models import Photo, Pet
from django.forms import  TextInput, Select, ClearableFileInput
from django.contrib.auth.forms import(
    AuthenticationForm, UserCreationForm
)
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory

User = get_user_model()


"""
class ModelFormWithFormSetMixin:

    def __init__(self, *args, **kwargs):
        super(ModelFormWithFormSetMixin, self).__init__(*args, **kwargs)
        self.formset = self.formset_class(
            instance=self.instance,
            data=self.data if self.is_bound else None,
        )

    def is_valid(self):
        return super(ModelFormWithFormSetMixin, self).is_valid() and self.formset.is_valid()

    def save(self, commit=True):
        saved_instance = super(ModelFormWithFormSetMixin, self).save(commit)
        self.formset.save(commit)
        return saved_instance
"""

class PhotoSubmitForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['image','is_primary','is_dispalyed']


PetPhotoSet = inlineformset_factory(
    parent_model = Pet,
    model = Photo,
    form = PhotoSubmitForm,
    extra=1,
    can_delete=False,
)


class PetCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Pet
        fields = ['name','sex','pet_type','together_with']

# これがモデルフォームセット
PetCreateFormSet = forms.modelformset_factory(
    Pet, form=PetCreateForm, extra=1
)
PhotoFormset = forms.inlineformset_factory(
    Pet, Photo, fields=['image','is_primary','is_dispalyed'],
    extra=1,can_delete=False
)



"""
class PetForm(ModelFormWithFormSetMixin, forms.ModelForm):

    formset_class = PetPhotoSet

    class Meta:
        model = Pet
        fields = ['name','sex','pet_type','together_with']

"""

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        if User.USERNAME_FIELD =='email':
            fields = ('email',)
        else:
            fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
