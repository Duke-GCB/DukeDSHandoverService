from mock import patch, Mock, MagicMock
from django.test import TestCase
from d4s2_api.utils import MessageDirection, Message, MessageFactory


class MessageDirectionTestCase(TestCase):

    def setUp(self):
        self.sender_email = 'sender@email.com'
        self.receiver_email = 'receiver@email.com'
        self.sender = Mock(email=self.sender_email)
        self.receiver = Mock(email=self.receiver_email)

    def test_default_order(self):
        ordered_addresses = MessageDirection.email_addresses(self.sender, self.receiver)
        self.assertEqual(ordered_addresses, (self.sender_email, self.receiver_email))

    def test_orders_forward(self):
        ordered_addresses = MessageDirection.email_addresses(self.sender, self.receiver, MessageDirection.ToRecipient)
        self.assertEqual(ordered_addresses, (self.sender_email, self.receiver_email))

    def test_orders_reverse(self):
        ordered_addresses = MessageDirection.email_addresses(self.sender, self.receiver, MessageDirection.ToSender)
        self.assertEqual(ordered_addresses, (self.receiver_email, self.sender_email))


class MessageTestCase(TestCase):
    def test_email_text(self):
        message = Message(from_email='bob@bob.com', to_email='joe@joe.com', template_subject='Hello',
                          template_body='Details for you {{value}}', context={'value':"123"})
        self.assertIn('From: bob@bob.com', message.email_text)
        self.assertIn('To: joe@joe.com', message.email_text)
        self.assertIn('Subject: Hello', message.email_text)
        self.assertIn('Details for you 123', message.email_text)

    @patch('d4s2_api.utils.generate_message')
    def test_send(self, mock_generate_message):
        message = Message(from_email='bob@bob.com', to_email='joe@joe.com', template_subject='Hello',
                          template_body='Details for you {{value}}', context={'value':"123"})
        message.send()
        self.assertTrue(mock_generate_message.return_value.send.called)
        mock_generate_message.assert_called_with('bob@bob.com', 'joe@joe.com', 'Hello',
                                                 'Details for you {{value}}', {'value': '123'})


class MessageFactoryTestCase(TestCase):
    def setUp(self):
        self.delivery_details = MagicMock()
        self.email_template_set = Mock()
        self.delivery_details.email_template_set = self.email_template_set
        self.email_template_set.template_for_name.return_value = Mock(subject='subject', body='body')
        self.delivery_details.get_from_user.return_value = Mock(email='bob@bob.com')
        self.delivery_details.get_to_user.return_value = Mock(email='joe@joe.com')
        self.delivery_details.get_email_context.return_value = {}

    @patch('d4s2_api.utils.Message')
    def test_make_share_message(self, mock_message):
        factory = MessageFactory(self.delivery_details)
        factory.make_share_message()
        mock_message.assert_called_with('bob@bob.com', 'joe@joe.com', 'subject', 'body', {})
        self.email_template_set.template_for_name.assert_called_with(
            self.delivery_details.delivery.email_template_name.return_value
        )

    @patch('d4s2_api.utils.Message')
    def test_make_delivery_message(self, mock_message):
        factory = MessageFactory(self.delivery_details)
        factory.make_delivery_message(accept_url='accept url')
        mock_message.assert_called_with('bob@bob.com', 'joe@joe.com', 'subject', 'body', {})
        self.email_template_set.template_for_name.assert_called_with('delivery')

    @patch('d4s2_api.utils.Message')
    def test_make_processed_message_to_sender(self, mock_message):
        factory = MessageFactory(self.delivery_details)
        factory.make_processed_message('accepted', MessageDirection.ToSender, warning_message='warning details')
        mock_message.assert_called_with('joe@joe.com', 'bob@bob.com', 'subject', 'body', {})
        self.delivery_details.get_email_context.assert_called_with(None, 'accepted', '', 'warning details')
        self.email_template_set.template_for_name.assert_called_with('accepted')

    @patch('d4s2_api.utils.Message')
    def test_make_processed_message_to_recipient(self, mock_message):
        factory = MessageFactory(self.delivery_details)
        factory.make_processed_message('accepted_recipient', MessageDirection.ToRecipient,
                                       warning_message='warning details')
        mock_message.assert_called_with('bob@bob.com', 'joe@joe.com', 'subject', 'body', {})
        self.delivery_details.get_email_context.assert_called_with(None, 'accepted_recipient', '', 'warning details')
        self.email_template_set.template_for_name.assert_called_with('accepted_recipient')

    @patch('d4s2_api.utils.Message')
    def test_make_canceled_message(self, mock_message):
        factory = MessageFactory(self.delivery_details)
        factory.make_canceled_message()
        mock_message.assert_called_with('bob@bob.com', 'joe@joe.com', 'subject', 'body', {})
        self.email_template_set.template_for_name.assert_called_with('delivery_canceled')
