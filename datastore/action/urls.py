from django.urls import path

from action import views

app_name = "action"
urlpatterns = [
    path(
        "<uuid:action_uid>/action-auth-config/",
        views.ActionAuthConfigListView.as_view(),
        name="action-auth-config-list"
    ),
    path(
        "<uuid:action_uid>/action-auth-config/<uuid:uid>",
        views.ActionAuthConfigDetailView.as_view(),
        name="action-auth-config-detail"
    ),
]
