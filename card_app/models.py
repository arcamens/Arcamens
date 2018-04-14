from django.utils.translation import ugettext_lazy as _
from markdown.extensions.tables import TableExtension
from mdx_gfm import GithubFlavoredMarkdownExtension
from django.core.urlresolvers import reverse
from core_app.models import Event, User
from sqlike.parser import SqLike, SqNode
from board_app.models import Board
from django.db.models import Q
from django.db import models
from markdown import markdown
from functools import reduce
from operator import and_, or_

# Create your models here.

class CardMixin(object):
    def save(self, *args, **kwargs):
        self.html = markdown(self.data,
        extensions=[TableExtension(), GithubFlavoredMarkdownExtension()], safe_mode=True,  
        enable_attributes=False)
        super(CardMixin, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('card_app:view-data', 
                    kwargs={'card_id': self.id})

    def get_link_url(self):
        return reverse('card_app:card-link', 
                    kwargs={'card_id': self.id})

    def duplicate(self, list=None):
        card          = Card.objects.get(id=self.id)
        card.pk       = None
        card.ancestor = list
        card.save()

        for ind in self.filewrapper_set.all():
            ind.duplicate(list)
        return card

    @classmethod
    def get_allowed_cards(cls, user):
        """
        The user has access to all cards that he is a member
        of its board or an work of the card.
        """

        # boards = Board.get_user_boards(user)
        # cards  = Card.objects.none()
        # for indi in boards:
            # for indj in indi.lists.all():
                # cards = cards | indj.cards.all()

        cards = Card.objects.filter(Q(ancestor__ancestor__organization=user.default) &
            (Q(ancestor__ancestor__members=user) | Q(workers=user)))
        return cards

    @classmethod
    def from_sqlike(cls):
        owner   = lambda ind: Q(owner__name__icontains=ind) | Q(
        owner__email__icontains=ind)

        worker  = lambda ind: Q(workers__name__icontains=ind) | Q(    
        workers__email__icontains=ind)

        created = lambda ind: Q(created__icontains=ind)
        label   = lambda ind: Q(label__icontains=ind)
        data    = lambda ind: Q(data__icontains=ind)

        snippet = lambda ind: Q(snippets_label__icontains=ind) | Q(
        snippets_data__icontains=ind)

        note  = lambda ind: Q(note__data__icontains=ind)
        tag   = lambda ind: Q(tags__name__icontains=ind)
        list  = lambda ind: Q(ancestor__name__icontains=ind)
        board = lambda ind: Q(ancestor__ancestor__name__icontains=ind)
        default = lambda ind: Q(label__icontains=ind) | Q(data__icontains=ind) 

        sqlike = SqLike(SqNode(None, default),
        SqNode(('o', 'owner'), owner),
        SqNode(('w', 'worker'), worker, chain=True), 
        SqNode(('c', 'created'), created),
        SqNode(('l', 'label'), label),
        SqNode(('d', 'data'), data),
        SqNode(('s', 'snippet'), snippet),
        SqNode(('n', 'note'), note),
        SqNode(('t', 'tag'), tag, chain=True),
        SqNode(('i', 'list'), list),
        SqNode(('b', 'board'), board),)
        return sqlike

    @classmethod
    def collect_cards(cls, cards, pattern, done=False):
        sqlike = cls.from_sqlike()
        cards  = cards.filter(Q(done=done))

        sqlike.feed(pattern)
        cards = sqlike.run(cards)
        return cards

    def __str__(self):
        """
        """
        return self.label

class FileWrapperMixin(object):
    def duplicate(self, card=None):
        wrapper       = FileWrapper.objects.get(id=self.id)
        wrapper.pk    = None
        wrapper.card  = card
        wrapper.save()
        return wrapper

class Card(CardMixin, models.Model):
    """    
    """
    owner = models.ForeignKey('core_app.User', null=True, 
    blank=True)

    ancestor = models.ForeignKey('list_app.List', 
    null=True, related_name='cards', blank=True)

    created  = models.DateTimeField(auto_now_add=True, 
    null=True)

    label = models.CharField(null=True, blank=False, 
    verbose_name=_("Label"), help_text='Label, Priority, Deadline, ...', 
    max_length=626)

    data = models.TextField(blank=True, verbose_name=_("Data"), 
    help_text='Markdown content.', default='')

    workers = models.ManyToManyField('core_app.User', 
    null=True, related_name='tasks', blank=True, 
    symmetrical=False)

    relations = models.ManyToManyField('Card', 
    null=True, related_name='related', blank=True, 
    symmetrical=True)

    tags = models.ManyToManyField(
    'core_app.Tag', related_name='cards', 
    null=True, blank=True, symmetrical=False)
    done = models.BooleanField(blank=True, default=False)

    html = models.TextField(null=True, blank=True)

    parent = models.ForeignKey('self', null=True, related_name='forks',
    blank=True)

    parent_post = models.ForeignKey('post_app.Post', null=True, 
    related_name='card_forks', blank=True)

    # path = models.ManyToManyField('Card', 
    # null=True, related_name='children', blank=True, 
    # symmetrical=False)

class GlobalCardFilter(models.Model):
    pattern  = models.CharField(max_length=255, blank=True, 
    default='', help_text='tag:issue + owner:iury')

    organization = models.ForeignKey('core_app.Organization', 
    blank=True, null=True)

    user = models.ForeignKey('core_app.User', null=True, 
    blank=True)

    done = models.BooleanField(blank=True, 
    default=False, help_text='Done cards?.')

    class Meta:
        unique_together = ('user', 'organization', )

class GlobalTaskFilter(models.Model):
    pattern  = models.CharField(max_length=255, blank=True, 
    default='', help_text='Example: bug + rocket + engine')

    organization = models.ForeignKey('core_app.Organization', 
    blank=True, null=True)

    user = models.ForeignKey('core_app.User', null=True, 
    blank=True)

    done = models.BooleanField(blank=True, 
    default=False, help_text='Done cards?.')

    class Meta:
        unique_together = ('user', 'organization', )

class CardClipboard(models.Model):
    user = models.ForeignKey('core_app.User', null=True, 
    blank=True)

    card = models.OneToOneField('Card', null=True, 
    related_name='selected', blank=True)

class ImageWrapper(models.Model):
    """
    """
    
    card = models.ForeignKey('Card', null=True, 
    on_delete=models.CASCADE, blank=True)

    file = models.ImageField(
    verbose_name='', help_text='')

class FileWrapper(FileWrapperMixin, models.Model):
    """
    """

    card = models.ForeignKey('Card', null=True, 
    on_delete=models.CASCADE, blank=True)

    file = models.FileField(
    verbose_name='', help_text='')

class ERelateCard(Event):
    """
    """

    ancestor0 = models.ForeignKey('list_app.List', 
    related_name='e_relate_card0', blank=True)

    ancestor1 = models.ForeignKey('list_app.List', 
    related_name='e_relate_card1', blank=True)

    child0 = models.ForeignKey('Card', 
    related_name='e_relate_card2', blank=True)

    child1 = models.ForeignKey('Card', 
    related_name='e_relate_card3', blank=True)

    html_template = 'card_app/e-relate-card.html'

class EUnrelateCard(Event):
    """
    """

    ancestor0 = models.ForeignKey('list_app.List', 
    related_name='e_unrelate_card0', blank=True)

    ancestor1 = models.ForeignKey('list_app.List', 
    related_name='e_unrelate_card1', blank=True)

    child0 = models.ForeignKey('Card', 
    related_name='e_unrelate_card2', blank=True)

    child1 = models.ForeignKey('Card', 
    related_name='e_unrelate_card3', blank=True)

    def get_absolute_url(self):
        return reverse('card_app:e-unrelate-card', 
                    kwargs={'event_id': self.id})

    html_template = 'card_app/e-unrelate-card.html'

class ECreateCard(Event):
    """
    """

    ancestor = models.ForeignKey('list_app.List', 
    related_name='e_create_card0', blank=True)

    card = models.ForeignKey('Card', 
    related_name='e_create_card1', blank=True)

    html_template = 'card_app/e-create-card.html'

class EBindCardWorker(Event):
    """
    """

    ancestor = models.ForeignKey('list_app.List', 
    related_name='e_bind_card_worker0', blank=True)

    card = models.ForeignKey('Card', 
    related_name='e_bind_card_worker1', blank=True)

    peer = models.ForeignKey('core_app.User', 
    related_name='e_bind_card_worker2', blank=True)

    html_template = 'card_app/e-bind-card-worker.html'

class EUnbindCardWorker(Event):
    """
    """

    ancestor = models.ForeignKey('list_app.List', 
    related_name='e_unbind_card_worker0', blank=True)

    card = models.ForeignKey('Card', 
    related_name='e_unbind_card_worker1', blank=True)

    peer = models.ForeignKey('core_app.User', 
    related_name='e_unbind_card_worker2', blank=True)

    html_template = 'card_app/e-unbind-card-worker.html'

class ECreateFork(Event):
    """
    """

    ancestor = models.ForeignKey('list_app.List', 
    related_name='e_create_fork0', blank=True)

    card0 = models.ForeignKey('Card', 
    related_name='e_create_fork1', blank=True)

    card1 = models.ForeignKey('Card', 
    related_name='e_create_fork2', blank=True)

    html_template = 'card_app/e-create-fork.html'

class ECreatePostFork(Event):
    """
    """

    list = models.ForeignKey('list_app.List', 
    related_name='e_create_post_fork0', blank=True)

    card = models.ForeignKey('Card', 
    related_name='e_create_post_fork1', blank=True)

    post = models.ForeignKey('post_app.Post', 
    related_name='e_create_post_fork2', blank=True)

    timeline = models.ForeignKey('timeline_app.Timeline', 
    related_name='e_create_post_fork3', blank=True)

    html_template = 'card_app/e-create-post-fork.html'

class EUpdateCard(Event):
    """
    """

    ancestor = models.ForeignKey('list_app.List', 
    related_name='e_update_card0', blank=True)

    child = models.ForeignKey('Card', 
    related_name='e_update_card1', blank=True)

    html_template = 'card_app/e-update-card.html'

class EDeleteCard(Event):
    """
    """

    ancestor = models.ForeignKey('list_app.List', 
    related_name='e_delete_card0', blank=True)

    label = models.CharField(null=True, blank=False, 
    max_length=626)

    html_template = 'card_app/e-delete-card.html'

class CardFilter(models.Model):
    pattern  = models.CharField(
    max_length=255,  blank=True, default='', 
    help_text='Example: owner:oliveira  + tag:bug')

    organization = models.ForeignKey('core_app.Organization', 
    blank=True, null=True)

    board = models.ForeignKey('board_app.Board', blank=True,
    related_name='card_filter',
    null=True)

    list = models.ForeignKey('list_app.List', blank=True, 
    related_name='card_filter', null=True)

    status = models.BooleanField(blank=True, default=False, 
    help_text='Filter On/Off.')

    done = models.BooleanField(blank=True, 
    default=False, help_text='Done cards?.')

    user = models.ForeignKey('core_app.User', 
    null=True, blank=True)

    # It warrants there will exist only one user and organization
    # filter. If we decide to permit more filters..
    class Meta:
        unique_together = ('user', 'organization', 'board', 'list')

class ExternObject(models.Model):
    """
    Cards can be related to any kind of extern objects/events.
    Like github commits or even comments. This model provides
    an abstract approach for providing quick integration with
    other platforms.
    
    """

    card = models.ForeignKey('core_app.User', null=True, 
    blank=True)


class EBindTagCard(Event):
    """
    """

    ancestor = models.ForeignKey('list_app.List', 
    related_name='e_bind_tag_card0', blank=True)

    card = models.ForeignKey('Card', 
    related_name='e_bind_tag_card1', blank=True)

    tag = models.ForeignKey('core_app.Tag', 
    related_name='e_bind_tag_card2', blank=True)

    html_template = 'card_app/e-bind-tag-card.html'

class EUnbindTagCard(Event):
    """
    """

    ancestor = models.ForeignKey('list_app.List', 
    related_name='e_unbind_tag_card0', blank=True)

    card = models.ForeignKey('Card', 
    related_name='e_unbind_tag_card1', blank=True)

    tag = models.ForeignKey('core_app.Tag', 
    related_name='e_unbind_tag_card2', blank=True)

    html_template = 'card_app/e-unbind-tag-card.html'

class ECutCard(Event):
    """
    """

    ancestor = models.ForeignKey('list_app.List', 
    related_name='e_cut_card0', blank=True)

    child = models.ForeignKey('Card', 
    related_name='e_cut_card1', blank=True)

    html_template = 'card_app/e-cut-card.html'

class EArchiveCard(Event):
    ancestor = models.ForeignKey('list_app.List', 
    related_name='e_archive_card0', blank=True)

    child = models.ForeignKey('Card', 
    related_name='e_archive_card1', blank=True)

    html_template = 'card_app/e-archive-card.html'


class ECopyCard(Event):
    """
    """

    ancestor = models.ForeignKey('list_app.List', 
    related_name='e_copy_card0', blank=True)

    child = models.ForeignKey('card', 
    related_name='e_copy_card1', blank=True)

    html_template = 'card_app/e-copy-card.html'















