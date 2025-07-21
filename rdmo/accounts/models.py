from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from rdmo.core.models import Model as RDMOTimeStampedModel
from rdmo.core.models import TranslationMixin
from rdmo.core.utils import parse_date_from_string

CONSENT_SESSION_KEY = "user_has_consented"


class AdditionalField(models.Model, TranslationMixin):

    TYPE_CHOICES = (
        ('text', 'Text'),
        ('textarea', 'Textarea'),
    )

    key = models.SlugField()
    type = models.CharField(max_length=11, choices=TYPE_CHOICES)

    text_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (primary)'),
        help_text=_('The text for this additional field (in the primary language).')
    )
    text_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (secondary)'),
        help_text=_('The text for this additional field (in the secondary language).')
    )
    text_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (tertiary)'),
        help_text=_('The text for this additional field (in the tertiary language).')
    )
    text_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (quaternary)'),
        help_text=_('The text for this additional field (in the quaternary language).')
    )
    text_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Text (quinary)'),
        help_text=_('The text for this additional field (in the quinary language).')
    )
    help_lang1 = models.TextField(
        blank=True,
        verbose_name=_('Help (primary)'),
        help_text=_('The help text to be displayed next to the input element (in the primary language).')
    )
    help_lang2 = models.TextField(
        blank=True,
        verbose_name=_('Help (secondary)'),
        help_text=_('The help text to be displayed next to the input element (in the secondary language).')
    )
    help_lang3 = models.TextField(
        blank=True,
        verbose_name=_('Help (tertiary)'),
        help_text=_('The help text to be displayed next to the input element (in the tertiary language).')
    )
    help_lang4 = models.TextField(
        blank=True,
        verbose_name=_('Help (quaternary)'),
        help_text=_('The help text to be displayed next to the input element (in the quaternary language).')
    )
    help_lang5 = models.TextField(
        blank=True,
        verbose_name=_('Help (quinary)'),
        help_text=_('The help text to be displayed next to the input element (in the quinary language).')
    )
    required = models.BooleanField(
        verbose_name=_('Required'),
        help_text=_('Designates whether this additional field is required.')
    )

    class Meta:
        ordering = ('key',)
        verbose_name = _('Additional field')
        verbose_name_plural = _('Additional fields')

    def __str__(self):
        return self.text

    @property
    def text(self):
        return self.trans('text')

    @property
    def help(self):
        return self.trans('help')


class AdditionalFieldValue(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='additional_values')
    field = models.ForeignKey(AdditionalField, on_delete=models.CASCADE, related_name='+')
    value = models.CharField(max_length=256)

    class Meta:
        ordering = ('user', 'field')

        verbose_name = _('Additional field value')
        verbose_name_plural = _('Additional field values')

    def __str__(self):
        return self.user.username + '/' + self.field.key


class ConsentFieldValue(RDMOTimeStampedModel):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    consent = models.BooleanField(
        default=False,
        help_text='Designates whether the user has agreed to the terms of use.',
        verbose_name='Consent'
    )

    class Meta:
        ordering = ('user', )
        verbose_name = _('Consent field value')
        verbose_name_plural = _('Consent field values')

    def __str__(self):
        return self.user.username

    @classmethod
    def create_consent(cls, user, session=None) -> bool:
        obj, _created = cls.objects.update_or_create(user=user, defaults={"consent": True})

        # Validate consent before storing in session
        has_valid_consent = (
            obj.is_consent_valid()
            if settings.ACCOUNT_TERMS_OF_USE_DATE is not None
            else True  # If terms update date is not enforced, any consent is valid
        )

        if has_valid_consent:
            if session:
                session[CONSENT_SESSION_KEY] = True
            return True

        obj.delete()  # Remove when consent is outdated
        return False

    @classmethod
    def has_accepted_terms(cls, user, session) -> bool:
        if not settings.ACCOUNT_TERMS_OF_USE:
            return True  # If terms are disabled, assume accepted.

        # Check session cache first
        if CONSENT_SESSION_KEY in session:
            return session[CONSENT_SESSION_KEY]

        consent = cls.objects.filter(user=user).only("updated").first()
        has_valid_consent = (
            consent.is_consent_valid()
            if consent and settings.ACCOUNT_TERMS_OF_USE_DATE is not None
            else bool(consent)
        )

        session[CONSENT_SESSION_KEY] = has_valid_consent  # Cache result
        return has_valid_consent

    def is_consent_valid(self) -> bool:
        # optionally check if the terms are outdated
        latest_terms_version_date = parse_date_from_string(settings.ACCOUNT_TERMS_OF_USE_DATE)
        # Compare only dates (ignores time)
        return self.updated and (self.updated.date() >= latest_terms_version_date)


class Role(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    member = models.ManyToManyField(
        Site, related_name='members', blank=True,
        verbose_name=_('Member'),
        help_text=_('The sites for which this user is a member.')
    )
    manager = models.ManyToManyField(
        Site, related_name='managers', blank=True,
        verbose_name=_('Manager'),
        help_text=_('The sites for which this user is manager.')
    )
    editor = models.ManyToManyField(
        Site, related_name='editors', blank=True,
        verbose_name=_('Editor'),
        help_text=_('The sites for which this user is an editor.')
    )
    reviewer = models.ManyToManyField(
        Site, related_name='reviewers', blank=True,
        verbose_name=_('Reviewer'),
        help_text=_('The sites for which this user is a reviewer.')
    )

    class Meta:
        ordering = ('user', )
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_user(sender, **kwargs):
    if not kwargs.get('raw', False):
        user = kwargs['instance']
        current_site = Site.objects.get_current()

        try:
            role = user.role
        except Role.DoesNotExist:
            role = Role(user=user)
            role.save()

        if current_site not in role.member.all():
            role.member.add(current_site)
