Unittest
========
To get access to the new API in unittest inside common.TransactionCase and others: ::

    class test_partner_firstname(common.TransactionCase):

        def setUp(self):
            super(test_partner_firstname, self).setUp()
            self.user_model = self.env["res.users"]
            self.partner_model = self.env["res.partner"]

YAML
====
To get access to the new API in Python YAML tag: ::

    !python {model: account.invoice, id: account_invoice_customer0}: |
        self  # is now a new api record
        assert (self.move_id), "Move falsely created at pro-forma"
