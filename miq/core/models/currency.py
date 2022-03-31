
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..utils import get_text_choices


class Currency(models.TextChoices):
    # BCEAO: Benin, CI, Burkina FAso,Guinea-Bissau, Mali, Niger, Senegal, Togo
    XOF = 'XOF', _('Franc CFA')
    # BEAC: Gabon, Cameroon, Central African Rep, Rep of Congo, Chad, Equ Guinea
    XAF = 'XAF', _('Franc CFA (BEAC)')
    GHC = 'GHC', _('Ghanaian Cedi')
    NGN = 'NGN', _('Nigerian Naira')
    EUR = 'EUR', _('Euro')
    USD = 'USD', _('United States Dollar')


Currencies = get_text_choices(Currency)
