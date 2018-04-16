from django.contrib import admin
from d4s2_api.models import *
from gcb_web_auth.models import DukeDSSettings
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(EmailTemplate)


class ShareAdmin(SimpleHistoryAdmin):
    pass


admin.site.register(Share, ShareAdmin)


class DeliveryAdmin(SimpleHistoryAdmin):
    pass


admin.site.register(DDSDelivery, DeliveryAdmin)
admin.site.register(DDSDeliveryShareUser)
admin.site.register(DukeDSSettings)
admin.site.register(EmailTemplateSet)
admin.site.register(UserEmailTemplateSet)
admin.site.register(S3Endpoint)
admin.site.register(S3User)
admin.site.register(S3UserCredential)
admin.site.register(S3Bucket)
admin.site.register(S3Delivery)
