from core_app.views import GuardianView
from django.views.generic import View
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
import json
import sys

class Authenticator(GuardianView):
    def post(self, request):
        pass

@method_decorator(csrf_exempt, name='dispatch')
class BitbucketHooker(View):
    def post(self, request):
        print('Payload:', request.POST, file=sys.stderr)
        # actor = request.POST['actor']

class SetupHooker(View):
    def post(self, request):
        pass
        # actor = request.POST['actor']


# from base64 import b64encode

# # Base class for taking an action on an event notification from a Git hosting
# class ConnectedIssueTracker(metaclass=abc.ABCMeta):
    # # In derived classes, I don't pass text=None when there is title.
    # # (I consider the text superfluous if there is title.)
    # # Is it OK or should it be changed?
    # @abc.abstractmethod
    # def action(self, event, object, id, title, text, url, user_login, user_fullname, user_url):
        # pass
# 
# 
# # Base class for connecting to a notification hooks of a Git hosting.
# # Don't use this class directly.
# class GitHostingController(metaclass=abc.ABCMeta):
    # def callback_url(self):
        # return reverse(self.callback_url_name())
# 
    # @abc.abstractclassmethod
    # def callback_url_name(self):
        pass

# This class performs authentication for BitBucket.
# Authentication can be done both by username/password or by OAuth.
# We can use any of the three methods:
# - Authorization: Bearer {access_token}
# - ?access_token={access_token}
# - HTTP user/password
# class Authenticator(models.Model, requests.auth.AuthBase):
    # # BitBucket API can be authenticated both as OAuth or as username/password
    # METHOD_NONE     = 1
    # METHOD_OAUTH    = 2
    # METHOD_PASSWORD = 3
    # method = models.SmallIntegerField(choices=((METHOD_NONE, _("None")),
                                               # (METHOD_OAUTH, _("OAuth")),
                                               # (METHOD_PASSWORD, _("Login and password"))))
    # token = models.ForeignKey('oauth_app.RefreshToken', null=True)
    # username = models.CharField()  # TODO: App passwords https://blog.bitbucket.org/2016/06/06/app-passwords-bitbucket-cloud/
    # password = models.CharField(widget=forms.PasswordInput)
# 
    # def __call__(self, r):
        # # modify and return the request
        # if self.method == Authenticator.METHOD_OAUTH:
            # r.headers['Authorization'] = 'Bearer ' + self.token.access_token
        # elif self.method == Authenticator.METHOD_PASSWORD:
            # r.headers['Authorization'] = _basic_auth_str(self.username, self.password)
        # return r

# Internal
# def my_parse_date(date_string):
    # if date_string:
        # return dateutil.parser.parse(date_string)
    # else:
        # return None
# 
# 
# # Internal
# def check_status(response):
    # if response.status_code == 403:
        # raise PermissionDenied()
    # elif response.status_code == 404:
        # raise ObjectDoesNotExist()
# 
# def _basic_auth_str(username, password):
    # """Returns a Basic Auth string."""
# 
    # return 'Basic ' + b64encode(('%s:%s' % (username, password)).encode('latin1')).strip()
# 
# # The class which responds to BitBucket webhook notifications calling the fire() Django view.
# class ConnectedBitBucketIssueTracker(base.ConnectedIssueTracker, Repository, metaclass=abc.ABCMeta):
    # server = models.CharField(default='https://api.bitbucket.org')
    # hook_uuid = models.CharField(db_index=True)
# 
    # # Remove the webhook (both from our DB and from BitBucket)
    # # Call this, don't call delete() manually
    # def disconnect(self, authenticator):
        # url = '%s/2.0/repositories/%s/%s/hooks/%s' %\
              # (self.server, self.repo_username, self.repo_slug, self.hook_uuid)
        # ctl = requests.Request()
        # response = ctl.delete(url, auth=authenticator)
        # if response.status_code == 403:
            # raise PermissionDenied()
        # elif response.status_code == 404:
            # raise ObjectDoesNotExist()
        # self.delete()
# 
    # # The function called from the callback view
    # @classmethod
    # def fire(cls, request):
        # if not request.is_secure():
            # raise PermissionDenied()
        # data = json.load(request.text)
        # # repo_fullname = data['repository']['full_name']
        # hook_uuid = request.META['X-Hook-UUID']
        # tracker = cls.objects.find(hook_uuid=hook_uuid)
        # new_username, new_slug = tuple(data['repository']['full_name'].split('/', 1))
        # # Update by the way:  # TODO: Update only on repository changes?
        # tracker.repo_username = new_username
        # tracker.repo_slug = new_slug
        # tracker.save()
        # funcs = {'issue:created': tracker.on_issue_created,
                 # 'issue:updated': tracker.on_issue_updated,
                 # 'issue:comment_created': tracker.on_issue_comment_created,
                 # 'pullrequest:created': tracker.on_pullrequest_created,
                 # 'pullrequest:updated': tracker.on_pullrequest_updated,
                 # 'pullrequest:rejected': tracker.on_pullrequest_rejected,
                 # 'pullrequest:fulfilled': tracker.on_pullrequest_fulfilled,
                 # 'pullrequest:approved': tracker.on_pullrequest_approved,
                 # 'pullrequest:unapproved': tracker.on_pullrequest_unapproved,
                 # 'pullrequest:comment_created': tracker.on_pullrequest_comment_created,
                 # 'pullrequest:comment_deleted': tracker.on_pullrequest_commen_deleted,
                 # 'pullrequest:comment_updated': tracker.on_pullrequest_comment_updated,
                 # 'repo:commit_status_created': tracker.on_repo_commit_status_created,
                 # 'repo:updated': tracker.on_repo_updated,
                 # 'project:updated': tracker.on_project_updated,
                 # 'repo:imported': tracker.on_repo_imported,
                 # 'repo:deleted': tracker.on_repo_deleted,
                 # 'repo:fork': tracker.on_repo_fork,
                 # 'repo:push': tracker.on_repo_push,
                 # 'repo:commit_comment_created': tracker.on_repo_commit_comment_created,
                 # 'repo:commit_status_created': tracker.on_repo_commit_status_created,
                 # }
        # func = funcs[request.META['X-Event-Key']]
        # func(data)
# 
# The class used to create (and store in our DB) a BitBucket webhook
# class BitBucketRepoHook(GitHostingController):
    # def __init__(self, repository, authenticator):
        # self.repository = repository
        # self.authenticator = authenticator
# 
    # # Do hooking and return the hook's PK
    # def hook_issue_tracker(self, server='https://api.bitbucket.org'):
        # # https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Busername%7D/%7Brepo_slug%7D/hooks
        # msg = {
            # "description": "Automatically created hook for Gnosis", # FIXME: Gnosis vs Labor
            # "url": self.callback_url(),
            # "active": True,
            # "events": [
                # 'issue:created',
                # 'issue:updated',
                # 'issue:comment_created',
                # 'pullrequest:created',
                # 'pullrequest:updated',
                # 'pullrequest:rejected',
                # 'pullrequest:fulfilled',
                # 'pullrequest:approved',
                # 'pullrequest:unapproved',
                # 'pullrequest:comment_created',
                # 'pullrequest:comment_deleted',
                # 'pullrequest:comment_updated',
                # 'repo:commit_status_created',
                # 'repo:updated',
                # 'project:updated', # missing in the docs
                # 'repo:imported',
                # 'repo:deleted',
                # 'repo:fork',
                # 'repo:push',
                # 'repo:commit_comment_created',
                # 'repo:commit_status_created'
            # ]
        # }
        # url = '%s/2.0/repositories/%s/%s/hooks' % (server, self.repository.repo_username, self.repository.repo_slug)
        # ctl = requests.Request()
        # response = ctl.post(url, msg, auth=self.authenticator)
        # if response.status_code == 403:
            # raise PermissionDenied()
        # elif response.status_code == 404:
            # raise ObjectDoesNotExist()
        # data = response.json()
        # tracker = ConnectedBitBucketIssueTracker.objects.create(server=server,
                                                                # repository=self.repository,
                                                                # hook_uuid=data['uuid'])
# 
        # return tracker.pk

