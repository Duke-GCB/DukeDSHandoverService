from django.db import IntegrityError
from django.test import TestCase
from d4s2_api.models import *
from django.contrib.auth.models import User


class TransferBaseTestCase(TestCase):

    def setUp(self):
        self.transfer_id = 'abcd-1234-efgh-6789'


class DeliveryTestCase(TransferBaseTestCase):
    DELIVERY_EMAIL_TEXT = 'delivery email message'
    ACCEPT_EMAIL_TEXT = 'delivery accepted'
    DECLINE_EMAIL_TEXT = 'delivery declined'

    def setUp(self):
        super(DeliveryTestCase, self).setUp()
        Delivery.objects.create(project_id='project1',
                                from_user_id='user1',
                                to_user_id='user2',
                                transfer_id=self.transfer_id)

    def test_initial_state(self):
        delivery = Delivery.objects.first()
        self.assertEqual(delivery.state, State.NEW, 'New deliveries should be in initiated state')

    def test_required_fields(self):
        with self.assertRaises(IntegrityError):
            Delivery.objects.create(project_id=None, from_user_id=None, to_user_id=None, transfer_id=None)

    def test_prohibits_duplicates(self):
        with self.assertRaises(IntegrityError):
            Delivery.objects.create(project_id='project1',
                                    from_user_id='user1',
                                    to_user_id='user2',
                                    transfer_id=self.transfer_id)

    def test_can_add_share_users(self):
        delivery = Delivery.objects.create(project_id='projectA',
                                           from_user_id='user1',
                                           to_user_id='user2',
                                           transfer_id='123-123')
        DeliveryShareUser.objects.create(delivery=delivery, dds_id='user3')
        DeliveryShareUser.objects.create(delivery=delivery, dds_id='user4')
        share_users = delivery.share_users.all()
        self.assertEqual(set([share_user.dds_id for share_user in share_users]),
                         set(['user3', 'user4']))

    def test_user_can_be_shared_multiple_deliveries(self):
        delivery1 = Delivery.objects.create(project_id='projectA',
                                            from_user_id='user1',
                                            to_user_id='user2',
                                            transfer_id='123-123')
        delivery2 = Delivery.objects.create(project_id='projectB',
                                            from_user_id='user3',
                                            to_user_id='user4',
                                            transfer_id='456-789')
        DeliveryShareUser.objects.create(delivery=delivery1, dds_id='user3')
        DeliveryShareUser.objects.create(delivery=delivery2, dds_id='user3')
        self.assertEqual(DeliveryShareUser.objects.count(), 2)
        self.assertEqual(set([share_user.dds_id for share_user in DeliveryShareUser.objects.all()]),
                         set(['user3']))

    def test_user_cannot_be_shared_delivery_twice(self):
        delivery = Delivery.objects.create(project_id='projectA',
                                           from_user_id='user1',
                                           to_user_id='user2',
                                           transfer_id='123-123')
        DeliveryShareUser.objects.create(delivery=delivery, dds_id='user3')
        with self.assertRaises(IntegrityError):
            DeliveryShareUser.objects.create(delivery=delivery, dds_id='user3')

    def test_mark_notified(self):
        delivery = Delivery.objects.first()
        self.assertEqual(delivery.state, State.NEW)
        delivery.mark_notified(DeliveryTestCase.DELIVERY_EMAIL_TEXT)
        self.assertEqual(delivery.state, State.NOTIFIED)

    def test_mark_accepted(self):
        performed_by = 'performer'
        delivery = Delivery.objects.first()
        self.assertEqual(delivery.state, State.NEW)
        delivery.mark_accepted(performed_by, DeliveryTestCase.ACCEPT_EMAIL_TEXT)
        self.assertEqual(delivery.state, State.ACCEPTED)
        self.assertEqual(delivery.performed_by, performed_by)
        self.assertEqual(delivery.completion_email_text, DeliveryTestCase.ACCEPT_EMAIL_TEXT)

    def test_mark_declined(self):
        performed_by = 'performer'
        delivery = Delivery.objects.first()
        self.assertEqual(delivery.state, State.NEW)
        delivery.mark_declined(performed_by, 'Wrong person.',  DeliveryTestCase.DECLINE_EMAIL_TEXT)
        self.assertEqual(delivery.state, State.DECLINED)
        self.assertEqual(delivery.decline_reason, 'Wrong person.')
        self.assertEqual(delivery.performed_by, performed_by)
        self.assertEqual(delivery.completion_email_text, DeliveryTestCase.DECLINE_EMAIL_TEXT)

    def test_is_complete(self):
        delivery = Delivery.objects.first()
        self.assertEqual(delivery.is_complete(), False)
        delivery.mark_notified('')
        self.assertEqual(delivery.is_complete(), False)
        delivery.mark_accepted('','')
        self.assertEqual(delivery.is_complete(), True)
        delivery.mark_declined('','','')
        self.assertEqual(delivery.is_complete(), True)
        delivery.state = State.FAILED
        delivery.save()
        self.assertEqual(delivery.is_complete(), True)

    def setup_incomplete_delivery(self):
        delivery = Delivery.objects.first()
        delivery.transfer_id = self.transfer_id
        delivery.save()
        self.assertFalse(delivery.is_complete())
        return delivery

    def test_updates_local_state_accepted(self):
        delivery = self.setup_incomplete_delivery()
        delivery.update_state_from_project_transfer({'id': self.transfer_id, 'status': 'accepted'})
        self.assertTrue(delivery.is_complete())
        self.assertEqual(delivery.state, State.ACCEPTED)
        self.assertEqual(delivery.decline_reason, '')

    def test_updates_local_state_rejected(self):
        delivery = self.setup_incomplete_delivery()
        delivery.update_state_from_project_transfer({'id': self.transfer_id, 'status': 'rejected', 'status_comment': 'Bad Data'})
        self.assertTrue(delivery.is_complete())
        self.assertEqual(delivery.state, State.DECLINED)
        self.assertEqual(delivery.decline_reason, 'Bad Data')

    def test_updates_local_state_pending(self):
        delivery = self.setup_incomplete_delivery()
        delivery.update_state_from_project_transfer({'id': self.transfer_id, 'status': 'pending'})
        self.assertFalse(delivery.is_complete())
        self.assertEqual(delivery.state, State.NEW)
        self.assertEqual(delivery.decline_reason, '')

    def test_update_without_changes(self):
        delivery = self.setup_incomplete_delivery()
        delivery.mark_declined('jsmith','Bad Data', DeliveryTestCase.DECLINE_EMAIL_TEXT)
        self.assertTrue(delivery.is_complete())
        delivery.update_state_from_project_transfer({'id': self.transfer_id, 'status': 'rejected', 'status_comment': 'Changed Comment'})
        self.assertTrue(delivery.is_complete())
        self.assertEqual(delivery.state, State.DECLINED)
        self.assertEqual(delivery.decline_reason, 'Bad Data', 'Should not change when status doesnt change')

    def test_user_message(self):
        delivery = Delivery.objects.first()
        self.assertIsNone(delivery.user_message)
        user_message = 'This is the final result of analysis xyz123'
        delivery.user_message = user_message
        delivery.save()
        delivery = Delivery.objects.first()
        self.assertEqual(delivery.user_message, user_message)


class ShareTestCase(TransferBaseTestCase):

    def setUp(self):
        super(ShareTestCase, self).setUp()
        Share.objects.create(project_id='project1', from_user_id='user1', to_user_id='user2')

    def test_initial_state(self):
        share = Share.objects.first()
        self.assertEqual(share.state, State.NEW, 'New shares should be in initiated state')
        self.assertEqual(share.role, ShareRole.DEFAULT, 'New shares should have default role')

    def test_prohibits_duplicates(self):
        with self.assertRaises(IntegrityError):
            Share.objects.create(project_id='project1', from_user_id='user1', to_user_id='user2')

    def test_allows_multiple_shares(self):
        user3 = DukeDSUser.objects.create(dds_id='user3')
        d = Share.objects.create(project_id='project1', from_user_id='user1', to_user_id='user3')
        self.assertIsNotNone(d)

    def test_allows_multiple_shares_different_roles(self):
        v = Share.objects.create(project_id='project1', from_user_id='user1', to_user_id='user2', role=ShareRole.VIEW)
        d = Share.objects.create(project_id='project1', from_user_id='user1', to_user_id='user2', role=ShareRole.EDIT)
        self.assertIsNotNone(v)
        self.assertIsNotNone(d)
        self.assertNotEqual(v, d)

    def test_user_message(self):
        share = Share.objects.first()
        self.assertIsNone(share.user_message)
        user_message = 'This is the preliminary result of analysis xyz123'
        share.user_message = user_message
        share.save()
        share = Share.objects.first()
        self.assertEqual(share.user_message, user_message)


class UserTestCase(TestCase):
    def setUp(self):
        DukeDSUser.objects.create(dds_id='abcd-1234-fghi-5678')

    def test_required_fields_dds_id(self):
        with self.assertRaises(IntegrityError):
            DukeDSUser.objects.create(dds_id=None)

    def test_prohibits_duplicates(self):
        with self.assertRaises(IntegrityError):
            DukeDSUser.objects.create(dds_id='abcd-1234-fghi-5678')


class EmailTemplateTypeTestCase(TestCase):

    def requires_unique_types(self):
        EmailTemplateType.objects.create(name='type1')
        with self.assertRaises(IntegrityError):
            EmailTemplateType.objects.create(name='type1')

    def test_initial_data(self):
        """
        Data for this is loaded by a migration, make sure it's there.
        :return:
        """
        for role in ShareRole.ROLES:
            self.assertIsNotNone(EmailTemplateType.objects.get(name='share_{}'.format(role)))
        self.assertIsNotNone(EmailTemplateType.objects.get(name='delivery'))
        self.assertIsNotNone(EmailTemplateType.objects.get(name='accepted'))
        self.assertIsNotNone(EmailTemplateType.objects.get(name='declined'))

    def test_from_share_role(self):
        role = 'project_viewer'
        e = EmailTemplateType.from_share_role(role)
        self.assertEqual(e.name, 'share_project_viewer')


class EmailTemplateTestCase(TestCase):

    def setUp(self):
        # email templates depend on groups and users
        self.template_set = EmailTemplateSet.objects.create(name='template_set')
        self.user = User.objects.create(username='test_user')
        UserEmailTemplateSet.objects.create(user=self.user, email_template_set=self.template_set)
        self.user_dds_id = 'user1'
        DukeDSUser.objects.create(user=self.user, dds_id=self.user_dds_id)
        self.default_type = EmailTemplateType.from_share_role(ShareRole.DEFAULT)
        self.download_type = EmailTemplateType.from_share_role(ShareRole.DOWNLOAD)
        self.view_type = EmailTemplateType.from_share_role(ShareRole.VIEW)
        self.transfer_id = 'abc-123'

    def test_create_email_template(self):
        template = EmailTemplate.objects.create(template_set=self.template_set,
                                                owner=self.user,
                                                template_type=self.default_type,
                                                subject='Subject',
                                                body='email body')
        self.assertIsNotNone(template)

    def test_prevent_duplicate_types(self):
        template1 = EmailTemplate.objects.create(template_set=self.template_set,
                                                 owner=self.user,
                                                 template_type=self.download_type,
                                                 subject='Subject',
                                                 body='email body 1')
        self.assertIsNotNone(template1)
        with self.assertRaises(IntegrityError):
            EmailTemplate.objects.create(template_set=self.template_set,
                                         owner=self.user,
                                         template_type=self.download_type,
                                         subject='Subject',
                                         body='email body 2')

    def test_allows_duplicate_types_outspide_group(self):
        template_set2 = EmailTemplateSet.objects.create(name='template_set2')
        template1 = EmailTemplate.objects.create(template_set=self.template_set,
                                                 owner=self.user,
                                                 template_type=self.download_type,
                                                 subject='Subject',
                                                 body='email body 1')
        self.assertIsNotNone(template1)
        template2 = EmailTemplate.objects.create(template_set=template_set2,
                                                 owner=self.user,
                                                 template_type=self.download_type,
                                                 subject='Subject',
                                                 body='email body 1')
        # assert different items but otherwise data is the same
        self.assertIsNotNone(template2)
        self.assertNotEqual(template1, template2)
        self.assertEqual(template1.owner, template2.owner)
        self.assertEqual(template1.subject, template2.subject)
        self.assertEqual(template1.body, template2.body)
        self.assertEqual(template1.template_type, template2.template_type)
        self.assertNotEqual(template1.template_set, template2.template_set)

    def test_for_share(self):
        # Create an email template
        EmailTemplate.objects.create(template_set=self.template_set,
                                     owner=self.user,
                                     template_type=self.download_type,
                                     subject='Subject',
                                     body='email body')
        share = Share.objects.create(project_id='project1',
                                     from_user_id='user1',
                                     to_user_id='user2',
                                     role=ShareRole.DOWNLOAD)
        t = EmailTemplate.for_share(share)
        self.assertIsNotNone(t)
        self.assertEqual(t.body, 'email body')

    def test_for_operation(self):
        # Create an email template
        delivery = Delivery.objects.create(project_id='project1',
                                           from_user_id='user1',
                                           to_user_id='user2',
                                           transfer_id=self.transfer_id)
        EmailTemplate.objects.create(template_set=self.template_set,
                                     owner=self.user,
                                     template_type=EmailTemplateType.objects.get(name='accepted'),
                                     subject='Acceptance Email Subject',
                                     body='Acceptance Email Body')
        t = EmailTemplate.for_operation(delivery, 'accepted')
        self.assertIsNotNone(t)
        self.assertEqual(t.subject, 'Acceptance Email Subject')

    def test_no_templates_in_template_set(self):
        share = Share.objects.create(project_id='project1',
                                     from_user_id='user1',
                                     to_user_id='user2',
                                     role=ShareRole.DOWNLOAD)
        with self.assertRaises(EmailTemplateException) as raised_exception:
            EmailTemplate.for_share(share)
        self.assertEqual(str(raised_exception.exception),
                         'Setup Error: Unable to find email template for type share_file_downloader')

    def test_no_template_set_for_user(self):
        share = Share.objects.create(project_id='project1',
                                     from_user_id='user2',
                                     to_user_id='user1',
                                     role=ShareRole.DOWNLOAD)
        with self.assertRaises(EmailTemplateException) as raised_exception:
            EmailTemplate.for_share(share)
        self.assertEqual(str(raised_exception.exception),
                         'Setup Error: Unable to find email template for type share_file_downloader')
        """        share = Share.objects.create(project_id='project1',
                                     from_user_id='user2',
                                     to_user_id='user1',
                                     role=ShareRole.DOWNLOAD)
        default_email_template_set = EmailTemplateSet.objects.create(name=DEFAULT_EMAIL_TEMPLATE_SET_NAME)
        some_email_template = EmailTemplate.objects.create(template_set=default_email_template_set,
                                                           owner=self.user,
                                                           template_type=self.download_type,
                                                           subject='Subject',
                                                           body='email body')
        email_template = EmailTemplate.for_share(share)
        self.assertEqual(email_template.id, some_email_template.id)"""

    def test_no_template_set_for_user_if_default_setup(self):
        share = Share.objects.create(project_id='project1',
                                     from_user_id='user2',
                                     to_user_id='user1',
                                     role=ShareRole.DOWNLOAD)
        default_email_template_set = EmailTemplateSet.objects.create(name=DEFAULT_EMAIL_TEMPLATE_SET_NAME)
        some_email_template = EmailTemplate.objects.create(template_set=default_email_template_set,
                                                           owner=self.user,
                                                           template_type=self.download_type,
                                                           subject='Subject',
                                                           body='email body')
        email_template = EmailTemplate.for_share(share)
        self.assertEqual(email_template.id, some_email_template.id)

    def test_user_not_found(self):
        # dds_user2 is not bound to a django user, so we can't find templates
        share = Share.objects.create(project_id='project1',
                                     from_user_id='user2',
                                     to_user_id='user1',
                                     role=ShareRole.DOWNLOAD)
        with self.assertRaises(EmailTemplateException) as raised_exception:
            EmailTemplate.for_share(share)
        self.assertEqual(str(raised_exception.exception),
                         'Setup Error: Unable to find email template for type share_file_downloader')

    def test_user_not_found_if_we_create_default(self):
        # dds_user2 is not bound to a django user, so we can't find templates
        share = Share.objects.create(project_id='project1',
                                     from_user_id='user2',
                                     to_user_id='user1',
                                     role=ShareRole.DOWNLOAD)
        default_email_template_set = EmailTemplateSet.objects.create(name=DEFAULT_EMAIL_TEMPLATE_SET_NAME)
        some_email_template = EmailTemplate.objects.create(template_set=default_email_template_set,
                                                           owner=self.user,
                                                           template_type=self.download_type,
                                                           subject='Subject',
                                                           body='email body')
        email_template = EmailTemplate.for_share(share)
        self.assertEqual(email_template.id, some_email_template.id)
