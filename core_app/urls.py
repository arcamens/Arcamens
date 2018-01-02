from django.views.generic.base import RedirectView
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.Index.as_view(), name='index'),
    url(r'^switch-organization/(?P<organization_id>.+)/', views.SwitchOrganization.as_view(), name='switch-organization'),
    url(r'^update-user-information/', views.UpdateUserInformation.as_view(), name='update-user-information'),
    url(r'^create-organization/(?P<user_id>.+)/', views.CreateOrganization.as_view(), name='create-organization'),
    url(r'^e-invite-user/(?P<event_id>.+)/', views.EInviteUser.as_view(), name='e-invite-user'),
    url(r'^join-organization/(?P<organization_id>.+)/(?P<token>.+)/', views.JoinOrganization.as_view(), name='join-organization'),

    url(r'^update-organization/(?P<organization_id>.+)/', views.UpdateOrganization.as_view(), name='update-organization'),
    url(r'^delete-organization/(?P<organization_id>.+)/', views.DeleteOrganization.as_view(), name='delete-organization'),
    url(r'^list-users/(?P<organization_id>.+)', views.ListUsers.as_view(), name='list-users'),
    url(r'^manage-user-tags/(?P<user_id>.+)', views.ManageUserTags.as_view(), name='manage-user-tags'),
    url(r'^list-events/', views.ListEvents.as_view(), name='list-events'),
    url(r'^list-tags/', views.ListTags.as_view(), name='list-tags'),
    url(r'^bind-user-tag/(?P<user_id>.+)/(?P<tag_id>.+)/', views.BindUserTag.as_view(), name='bind-user-tag'),
    url(r'^unbind-user-tag/(?P<user_id>.+)/(?P<tag_id>.+)/', views.UnbindUserTag.as_view(), name='unbind-user-tag'),
    url(r'^create-tag/', views.CreateTag.as_view(), name='create-tag'),
    url(r'^delete-tag/(?P<tag_id>.+)/', views.DeleteTag.as_view(), name='delete-tag'),
    url(r'^event-queues/(?P<tag_id>.+)/', views.EventQueues.as_view(), name='event-queues'),
    url(r'^invite-organization-user/(?P<organization_id>.+)/', views.InviteOrganizationUser.as_view(), name='invite-organization-user'),

]



















