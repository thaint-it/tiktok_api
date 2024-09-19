from django.conf import settings
from django.db import models, transaction
from datetime import datetime


class AuthRefreshToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, default="", unique=True, db_index=True)  ## uuid
    # access_token = models.CharField(max_length=255, null=True, db_index=True)
    revoked = models.DateTimeField(null=True)

    class Meta:
        db_table = "auth_refresh_token"

    def revoke(self):
        """
        Mark this refresh token revoked
        """
        with transaction.atomic():
            self = AuthRefreshToken.objects.filter(pk=self.pk).select_for_update().first()
            if not self:
                return
            self.revoked = datetime.now()
            self.save()
