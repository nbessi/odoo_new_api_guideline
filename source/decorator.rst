Method and decorator
====================

New decorators are just mapper around the new API.
The decorator are mandatory as webclient and HTTP controller are not compliant with new API.

``api`` namespace decorators will detect signature using variable name
and decide to match old signature or not.

Recognized variable names are:

``cr, cursor, uid, user, user_id, id, ids, context``


@api.returns
------------

This decorator guaranties unity of returned value.
It will return a RecordSet of specified model based on original returned value: ::

    @api.returns('res.partner')
    def afun(self):
        ...
        return x  # a RecordSet

And if an old API function calls a new API function it will
automatically convert it into a list of ids

All decorators inherits from this decorator to upgrade or downgrade the returned value.

@api.one
--------

This decorator loops automatically on Records of RecordSet for you.
Self is redefined as current record: ::

  @api.one
  def afun(self):
      self.name = 'toto'


.. note::
   Caution: the returned value is put in a list. This is not always supported by
   the web client, e.g. on button action methods. In that case, you should use
   ``@api.multi`` to decorate your method, and probably call `self.ensure_one()`
   in the method definition.


@api.multi
----------

Self will be the current RecordSet without iteration.
It is the default behavior: ::

   @api.multi
   def afun(self):
       len(self)

@api.model
----------

This decorator will convert old API calls to decorated function to new API signature.
It allows to be polite when migrating code. ::

    @api.model
    def afun(self):
        pass

@api.constrains
---------------

This decorator will ensure that decorated function will be called on create, write, unlink operation.
If a constraint is met the function should raise a `openerp.exceptions.Warning` with appropriate message.

@api.depends
------------

This decorator will trigger the call to the decorated function if any of the
fields specified in the decorator is altered by ORM or changed in the form: ::

    @api.depends('name', 'an_other_field')
    def afun(self):
        pass


.. note::
   when you redefine depends you have to redefine all @api.depends,
   so it loses some of his interest.

View management
###############
One of the great improvement of the new API is that the depends are automatically inserted into the form for you in a simple way.
You do not have to worry about modifying views anymore.



.. _@api.onchange:

@api.onchange
--------------
This decorator will trigger the call to the decorated function if any of the
fields specified in the decorator is changed in the form: ::

  @api.onchange('fieldx')
  def do_stuff(self):
     if self.fieldx == x:
        self.fieldy = 'toto'

In previous sample `self` corresponds to the record currently edited on the form.
When in on_change context all work is done in the cache.
So you can alter RecordSet inside your function without being worried about altering database.
That's the main difference with ``@api.depends``

At function return, differences between the cache and the RecordSet will be returned
to the form.

View management
###############
One of the great improvement of the new API is that the onchange are automatically inserted into the form for you in a simple way.
You do not have to worry about modifying views anymore.

Warning and Domain
##################
To change domain or send a warning just return the usual dictionary.
Be careful not to use ``@api.one`` in that case as it will mangle the
dictionary (put it in a list, which is not supported by the web client).


@api.noguess
------------

This decorator prevent new API decorators to alter the output of a method
