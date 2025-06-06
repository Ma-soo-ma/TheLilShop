from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from allauth.socialaccount.views import SignupView

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"), 
    path("contact/", views.contact, name="contact"),
    path("category/<slug:val>", views.categoryView.as_view(), name="category"),
    path("product-detail/<int:pk>", views.productDetail.as_view(), name="product-detail"),
    path("category-title/<val>", views.categoryTitle.as_view(), name="category-title"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path("updateAddress/<int:pk>", views.updateAddress.as_view(), name="updateAddress"),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('search/', views.search, name='search'),

    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('pluswishlist/', views.plus_wishlist, name='pluswishlist'),
    path('minuswishlist/', views.minus_wishlist, name='minuswishlist'),
    path('wishlist/', views.show_wishlist, name='wishlist'),

    #login authentication
    path("customer-registration/", views.customerRegistrationView.as_view(), name="customerregistration"),
    path("login/", auth_views.LoginView.as_view(template_name="app/login.html", authentication_form=LoginForm), name='login'),
    path("google-login/", SignupView.as_view(), name='google_login'),

    path("changepassword/", auth_views.PasswordChangeView.as_view(template_name="app/changepassword.html", form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='changepassword'),
    path("passwordchangedone/", auth_views.PasswordChangeDoneView.as_view(template_name="app/passwordchangedone.html"), name='passwordchangedone'),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="app/password_reset.html", form_class=MyPasswordResetForm), name='password_reset'),
    path("password-reset-done/", auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"), name='password_reset_done'),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html", form_class=MySetPasswordForm), name='password_reset_confirm'),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html"), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "TheLilShop"
admin.site.site_title = "TheLilShop"
admin.site.index_title = "Welcome to TheLilShop"



