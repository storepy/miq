
# class SearchTerm(BaseModelMixin):
#     session = models.CharField(max_length=300)
#     value = models.CharField(_("Term"), max_length=99)
#     count = models.PositiveIntegerField(_("Count"), default=1)

#     class Meta:
#         verbose_name = _('Search Term')
#         verbose_name_plural = _('Search Terms')
#         ordering = ('-updated', '-created',)


# class Campaign(BaseModelMixin):
#     key = models.CharField(max_length=99)
#     value = models.CharField(_("Term"), max_length=99)
#     ip = models.GenericIPAddressField(
#         unpack_ipv4=True, verbose_name=_('Ip address'),
#         null=True, blank=True)

#     class Meta:
#         verbose_name = _('Campaign')
#         verbose_name_plural = _('Campaigns')
#         ordering = ('-updated', '-created',)


# class HitRangeUnit(models.TextChoices):
#     HOUR = 'HOUR', _('Hour')
#     DAY = 'DAY', _('Day')
#     WEEK = 'DAY', _('Day')
#     MONTH = 'DAY', _('Day')
#     YEAR = 'YEAR', _('Year')


# class HitRange:
#     unit = models.CharField(
# _("Type"), choices=HitRangeUnit.choices max_length=10)
#     unit_count = models.PositiveIntegerField(_("Unit count"), default=1)
#     start_dt = models.DateTimeField(_("Starts at"),)
#     end_dt = models.DateTimeField(_("Ends at"),)
#     hits = models.ManyToManyField(
# "Hit", verbose_name=_("Hits"), reverse_name="ranges")


# class IpAddress(models.Model):
#     class Meta:
#         ordering = ('value', )
#         verbose_name = _('IP Address')
#         verbose_name_plural = _('IP Addresses')

#     def __str__(self):
#         return f'{self.value}'

#     value = models.GenericIPAddressField(
#         unpack_ipv4=True, null=True,
#         verbose_name=_('Ip address'), blank=True)
#     is_blacklisted = models.BooleanField(default=False)
