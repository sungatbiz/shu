from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from shu import views
from users import views as user_views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    # path('register/', user_views.register, name='register'),
    # path('login/', user_views.LoginFormView.as_view(), name='login'),
    # path('profile/', user_views.Profile, name='profile'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # path('gozle/', user_views.gozle_user, name='gozle-user'),
    # path('', include('ezd.urls')),
]


urlpatterns += i18n_patterns(
    path('register/', user_views.register, name='register'),
    path('login/', user_views.LoginFormView.as_view(), name='login'),
    path('', user_views.LoginFormView.as_view(), name='login'),
    path('profile/', user_views.Profile, name='profile'),
    path('profile/<int:pk>/delete/', user_views.delete_oj, name='oj-delete'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('zakaz_users/', user_views.Zakaz_sanaw, name='zakaz-users'),
    path('zakazusers_detail/<int:pk>/', user_views.Zakaz_detail, name='zakazusers-detail'),
    path('zakaz_update/<int:pk>', user_views.load_zakupdate, name='zakaz_update'),
    path('zakaz_balans_edit/<int:pk>/', user_views.Zakaz_balans_edit, name='zakaz-balans-edit'),
    path('zakaz_balans/<int:pk>/delete/', views.delete_Zakaz_balans, name='zakaz-balans-delete'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_form.html'),name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'),name='password_reset_complete'),

    # path('gozle/', user_views.gozle_user, name='gozle-user'),
    # path('logs/', user_views.Loglar, name='my-logs'),
    path('', include('shu.urls')),
    prefix_default_language=False,
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)