from django.db import models
from django.contrib.auth import get_user_model

from .quote import Quote

User = get_user_model()


class QuoteVote(models.Model):
    VOTE_CHOICES = ((1, 'лайк'), (-1, 'дизлайк'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="votes")
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'quote')