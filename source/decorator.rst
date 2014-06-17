Method and decorator
====================

New decorators are just mapper around the new API.
The decorator are mandatory as webclient and HTTP controller are not new API aware.

``api`` namspace decorators will detect signature using variable name
and decide to match old signature or not.

Recognized variable names are:

`cr, cursor, uid, user, user_id, id, ids, context`


@api.returns
------------

This decorator guaranties unity of returned value.
It will returns a record set of sepcified model basef on original returned value: ::

    @api.returns('res.partner')
    def afun(self):
        ...
        return x # can be id, list of ids, recordset or void

And if an old api function call a new api function it will
automatically convert it into a list of ids

@api.one
--------

This decorator loop automatically on Records of RecordSet for you.
So by doing this self is redefined  as current record: ::

  @api.one
  def afun(self):
      self.name = 'toto'


@api.multi
----------

Self will be the record set without iteration.
it is the default behavior: ::

   @api.multi
   def afun(self):
       len(self)

@api.model
----------

This decorator will convert old api call to decorated function to new api signature.
It allows to be polite when when migrating code. ::

    @api.model
    def afun(self):
        pass

@api.constraints
----------------

This decorator will ensure that decorated function will be called on create, write, unlink operation.
If a constraint is met the function should raise an `exceptions.Warning` with apropriate message.

@api.depends
------------

This decorator will trigger the call to the decorated function if any of the
fields specified in the decorator is altered by ORM or changed in the form: ::

    @pid.depends('name', 'an_other_field')
    def afun(self):
        pass


!! when you redefine depends you have te redefine all @api.depends
So it looses some of his interest.

View management
###############
One of the greate improvement of the new API is that the depends are automatically inserted into the form for you in a simple way. You do not have to worry about modifing views anymore.



@api.on_change
--------------
This decorator will trigger the call to the decorated function if any of the
fields specified in the decorator is changed in the form: ::

  @api.one       
  @api.on_change('fieldx'):
  def do_stuff(self):
     if self.fieldx == x
        self.fieldy = 'toto'

In previous sample `self` corresponds to the record currently edited on the form.
When in on change context all work is done in the cache.
So you can alter RecordSet inside your function without worried about alter database.

At function return, difference between the cache and the RecordSet will be returned
to the form.

View management
###############
One of the greate improvement of the new API is that the onchange are automatically inserted into the form for you in a simple way. You do not have to worry about modifing views anymore.

Warning and Domain
##################
To change domain or send a warning just return the usual dictionnary.
