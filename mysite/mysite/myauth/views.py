from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from .models import Profile
from .forms import ProfileEditForm


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


# класс для редактирования аватарки в профиле пользователя-------------------------
class AvatarUpdateView(UserPassesTestMixin, UpdateView):
    """Аватарку может поменять администратор сайта или хозяин странички"""
    def test_func(self):
        # если пользователь из запроса совпадает с пользователем queryset то он может
        # сменить аватарку, или это админ
        if (self.request.user.id == self.get_object().user.profile.id
                or self.request.user.is_staff):
            return True

    model = Profile
    template_name = "myauth/avatar_update.html"
    form_class = ProfileEditForm

    def get_success_url(self):
        return reverse("myauth:list_users",)
# ---------------------------------------------------------------------------------


# --------------класс выводящий список пользователей------------------------------
class ListUsersView(ListView):
    template_name = 'myauth/list_users.html'
    # model = Product
    context_object_name = "list_users"
    queryset = User.objects.all()
# ---------------------------------------------------------------------------------


# ----------детальная информация о пользователе------------------------------------
class UserDetailsView(DetailView):
    template_name = 'myauth/user_details.html'
    queryset = User.objects.select_related("profile")
    context_object_name = "user"
# -----------------------------------------------------------------------------------


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
