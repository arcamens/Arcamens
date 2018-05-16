from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from core_app.models import  User, Event, Node
from django.db import models
from django.db.models import Q
from onesignal.models import GroupSignal
import datetime

class TimelineMixin(GroupSignal):
    class Meta:
        abstract = True

    @classmethod
    def get_user_timelines(cls, user):
        timelines = user.timelines.filter(
            organization=user.default)
        return timelines

    def get_link_url(self):
        return reverse('timeline_app:timeline-link', 
                    kwargs={'timeline_id': self.id})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.node = Node.objects.create()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def set_ownership(self, user):
        self.owner = user
        self.users.add(user)
        self.save()

class EUpdateTimelineMixin(object):
    pass

class EDeleteTimelineMixin(object):
    pass

class EUnbindTimelineUserMixin(object):
    pass

class ECreateTimelineMixin(object):
    pass

class EBindTimelineUserMixin(object):
    pass

class TimelinePinMixin(object):
    def get_absolute_url(self):
        return reverse('timeline_app:list-posts', 
            kwargs={'timeline_id': self.timeline.id})

class TimelinePin(TimelinePinMixin, models.Model):
    user = models.ForeignKey('core_app.User', null=True, blank=True)

    organization = models.ForeignKey('core_app.Organization', 
    blank=True, null=True)

    timeline = models.ForeignKey('timeline_app.Timeline', null=True, blank=True)

    class Meta:
        unique_together = ('user', 'organization', 'timeline')

class Timeline(TimelineMixin):
    users = models.ManyToManyField('core_app.User', null=True,  
    related_name='timelines', blank=True, symmetrical=False)
    organization = models.ForeignKey('core_app.Organization', 
    related_name='timelines', null=True, blank=True)

    name = models.CharField(null=True, blank=False,
    verbose_name=_("Name"), help_text='Example: /projects/labor/bugs, \
    Management, Blackdawn Team, ...', max_length=250)

    description = models.CharField(blank=True, default='', 
    verbose_name=_("Description"), help_text='Example: Deals with \
    labor bugs.', max_length=626)

    owner = models.ForeignKey('core_app.User', null=True, 
    blank=True, related_name='owned_timelines')

    created  = models.DateTimeField(auto_now_add=True, 
    null=True)

    node = models.OneToOneField('core_app.Node', 
    null=False, related_name='timeline')

class EDeleteTimeline(Event, EDeleteTimelineMixin):
    timeline_name = models.CharField(null=True,
    blank=False, max_length=250)

    html_template = 'timeline_app/e-delete-timeline.html'

class ECreateTimeline(Event, ECreateTimelineMixin):
    timeline = models.ForeignKey('Timeline', 
    related_name='e_create_timeline', blank=True)
    html_template = 'timeline_app/e-create-timeline.html'

class EUpdateTimeline(Event, EUpdateTimelineMixin):
    timeline = models.ForeignKey('Timeline', 
    related_name='e_update_timeline', blank=True)
    html_template = 'timeline_app/e-update-timeline.html'

class EBindTimelineUser(Event, EBindTimelineUserMixin):
    timeline = models.ForeignKey('Timeline', 
    related_name='e_bind_timeline_user', blank=True)

    peer = models.ForeignKey('core_app.User', null=True, blank=True)
    html_template = 'timeline_app/e-bind-timeline-user.html'

class EUnbindTimelineUser(Event, EUnbindTimelineUserMixin):
    timeline = models.ForeignKey('Timeline', 
    related_name='e_unbind_timeline_user', blank=True)

    peer = models.ForeignKey('core_app.User', null=True, blank=True)
    html_template = 'timeline_app/e-unbind-timeline-user.html'

class EPastePost(Event):
    timeline = models.ForeignKey('timeline_app.Timeline', 
    related_name='e_paste_post0', blank=True)

    posts = models.ManyToManyField('post_app.Post', null=True,  
    related_name='e_paste_post1', blank=True, symmetrical=False)
    html_template = 'timeline_app/e-paste-post.html'














