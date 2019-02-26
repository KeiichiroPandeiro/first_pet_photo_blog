from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
from django.views import generic
from .models import Photo, Good, Pet
from .forms import PhotoSubmitForm,  PetCreateForm, PhotoFormset
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import(
    LoginForm, UserCreateForm, UserUpdateForm
)
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.contrib import messages

User = get_user_model


def pet_edit(request, pet_id):
    user = request.user
    pet= Pet.objects.get(pk=pet_id)
    if request.method == "POST":
        form = PetCreateForm(request.POST, instance=pet)
        context = {'form':form}
        if form.is_valid():
            pet = form.save(commit=False)
            formset = PhotoFormset(request.POST, files=request.FILES, instance=pet)
            pet.owner = request.user
            pet.save()
            return redirect('index')
    else:
        form = PetCreateForm(instance=pet)
    return render(request, 'blog/pet_edit.html', {'form':form})


def create_pet(request):
    """
    Pet.objects.all.Count() => x
    どこかへreturn させる
    """
    user = request.user
    form = PetCreateForm(request.POST or None)
    context = {'form':form}
    if request.method == 'POST' and form.is_valid():
        pet = form.save(commit=False)
        formset = PhotoFormset(request.POST, files=request.FILES, instance=pet)
        if formset.is_valid():
            pet.owner = user
            pet.save()
            photo = Photo
            formset.save()

            return redirect('/')
        else:
            context['formset'] = formset
    else:
        context['formset'] = PhotoFormset
    return render(request, 'blog/create_pet.html', context)


def index(request):

    if request.method == 'GET':

        best_photos = Photo.objects.order_by('-good_count')[:2]
        photos = Photo.objects.order_by('-good_count')
        paginator = Paginator(photos, 30)
        page = request.GET.get('page', 1)
        photos =  paginator.page(page)

        user = request.user
        goods = Good.objects.all()

        return render(request, 'blog/index.html', {
                'goods':goods,
                'best_photos':best_photos,
                'photos': photos,
                'user': user})


def detail(request, photo_id):

    goods = Good.objects.all()
    photo = Photo.objects.get(pk=photo_id)

    return render(request, 'blog/index/detail.html',{
            'photo': photo,
            'goods':goods})


def pet_detail(request, pet_id):
    pet = Pet.objects.get(pk=pet_id)

    return render(request, 'blog/mypage/pet_detail.html',{
            'pet':pet
    })

def good(request,photo_id):

    photo = Photo.objects.get(pk=photo_id)
    user = request.user
    if photo.pet.owner == user:
        messages.success(request, 'kkkk')
        return redirect('index')

    elif Good.objects.filter(owner=user).filter(photo=photo).count() > 0:
        messages.success(request, 'kkkk')
        return redirect('index')

    else:
        photo.good_count += 1
        photo.save()
        good = Good()
        good.owner = user
        good.photo = photo
        good.save()

        return redirect('index')


def mypage(request, user_id):

    user = request.user
    pet = Pet.objects.filter(owner=user)
    pet_count = Pet.objects.filter(owner=user).count()
    if request.method == 'GET':
        form =  PhotoSubmitForm()
        if Pet.objects.filter(owner=user).count() <10:

            return render(request, 'blog/mypage.html', {
                'pet_count':pet_count,
                'pet':pet,
                'form': form,
                'user': user})

        else:
            return render(request, 'blog/mypage.html', {

                'user': user})

    elif request.method == 'POST':

        form = PhotoSubmitForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('invalid form')

        photo = form.save(commit=False)

        photo.image = form.cleaned_data['image']
        photo.pet = pet
        photo.save()

        return render(request, '/',{
            'form': form,
            'photo' :photo})


class Login(LoginView):

    form_class = LoginForm
    template_name = 'blog/login.html'


class Logout(LoginRequiredMixin, LogoutView):

    template_name = 'blog/index.html'


class UserCreate(generic.CreateView):

    template_name = 'blog/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol':'https' if self.request.is_secure() else 'http',
            'domain':domain,
            'token':dumps(user.pk),
            'user':user,
            }
        subject_template = get_template('blog/mail_template/create/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('blog/mail_template/create/message.txt')
        message = message_template.render(context)

        user.email_user(subject, messsage)

        return redirect('blog:user_create_done')



"""
class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'blog/user_form.html'

    def get_success_url(self):
        return redirect('index')

"""

"""

def good(request, photo_id):
    if request.method == 'POST':
        Good.objects.create(photo_id=photo_id)
    count

        def good(request, photo_id, user_id) すでにあった場合
            return ('2回目です！')
        else
            newする good.create.create(photo_id=photo_id,user_id=user_id)

        good count = count(good(photo_id))
            リレーションの貼り方やり方調べる
        good_countをindexに渡す

        photo_id に対するGoodの数を集計する、結果をindex表示させる

1.　templateで計算させる
2.1 goodで計算する
2.2 indexで計算するphotoに紐づいたgoodを呼び出して数を計算して、表示する。
3.　photoのgood_countを更新する
4.　Photoモデルで計算するメソッド追加して、Goodの数を集計して、indexで表示させる。


1で動かしてみる→２のどちらかで書き直してみる
マイページ

Views
    index
    mypage
    共通の計算したGoodを呼び出して表示する仕組み
        →good_couuntメソッド　を作って、呼び出す。



def upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = PhotoForm()
        return render(request, 'upload.html', {'form': form})



def good(request, pk):
    photo = Photo.objects.get(pk=pk)
    is_good = Good.objects.count()
    photo.good_count += 1
    photo.save()
    good = Good()
    good.photo = photo
    good.save()
    messages.success(request, 'いいね！しました')
    return redirect('/')
"""
