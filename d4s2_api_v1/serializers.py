from django.contrib.auth.models import User
from rest_framework import serializers

from d4s2_api.models import DDSDelivery, Share, DDSDeliveryShareUser, EmailTemplateSet
SHARE_USERS_INVALID_MSG = "to_user cannot be part of share_to_users."


def validate_delivery_data(data):
    """
    Check that to_user_id is not accidentally included in share_user_ids
    """
    to_user_id = data['to_user_id']
    share_user_ids = data.get('share_user_ids', [])
    if share_user_ids:
        if to_user_id in share_user_ids:
            raise serializers.ValidationError(SHARE_USERS_INVALID_MSG)
    return data


class DeliverySerializer(serializers.HyperlinkedModelSerializer):
    share_user_ids = serializers.ListField(child=serializers.CharField(), required=False)
    email_template_set = serializers.PrimaryKeyRelatedField(queryset=EmailTemplateSet.objects.all(), required=False)

    def validate(self, data):
        return validate_delivery_data(data)

    def to_representation(self, instance):
        """
        Converts our object instance (DDSDelivery) into a dict of primitive datatypes.
        We add array of shared user ids to the resulting dict.
        :param instance: DDSDelivery: object to be serialized into a string.
        :return: dict
        """
        ret = super(DeliverySerializer, self).to_representation(instance)
        ret['share_user_ids'] = [share_user.dds_id for share_user in instance.share_users.all()]
        return ret

    def create(self, validated_data):
        def super_create(delivery_data):
            return super(DeliverySerializer, self).create(delivery_data)
        return self._save_delivery_data(validated_data, super_create)

    def update(self, instance, validated_data):
        def super_update(delivery_data):
            return super(DeliverySerializer, self).update(instance, delivery_data)
        return self._save_delivery_data(validated_data, super_update)

    def _save_delivery_data(self, validated_data, func):
        delivery_data = self._remove_share_user_ids_from_dict(validated_data)
        instance = func(delivery_data)
        if 'share_user_ids' in validated_data:
            self._update_share_users(validated_data['share_user_ids'], instance)
        return instance

    @staticmethod
    def _remove_share_user_ids_from_dict(validated_data):
        delivery_data = dict(validated_data)
        if 'share_user_ids' in delivery_data:
            delivery_data.pop('share_user_ids')
        return delivery_data

    @staticmethod
    def _update_share_users(share_user_ids, delivery):
        DDSDeliveryShareUser.objects.filter(delivery=delivery).delete()
        for share_user_id in share_user_ids:
            DDSDeliveryShareUser.objects.create(delivery=delivery, dds_id=share_user_id)

    class Meta:
        model = DDSDelivery
        resource_name = 'deliveries'
        fields = ('id', 'url', 'project_id', 'from_user_id', 'to_user_id', 'state', 'transfer_id', 'user_message',
                  'share_user_ids', 'decline_reason', 'performed_by', 'delivery_email_text', 'email_template_set')
        read_only_fields = ('decline_reason', 'performed_by', 'delivery_email_text', 'email_template_set')


class ShareSerializer(serializers.HyperlinkedModelSerializer):
    email_template_set = serializers.PrimaryKeyRelatedField(queryset=EmailTemplateSet.objects.all(), required=False)

    def validate(self, data):
        return validate_delivery_data(data)

    class Meta:
        model = Share
        fields = ('id', 'url', 'project_id', 'from_user_id', 'to_user_id', 'role', 'state', 'user_message',
                  'email_template_set')
        read_only_fields = ('email_template_set', )
