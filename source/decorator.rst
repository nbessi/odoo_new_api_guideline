 Method and decorator
======================
mapper are just mapper around the new API.
As webclient and controler are not new api aware.

Decorator will detect signature using variable name.
Recognized values are:

cr, cursor, uid, user, user_id, id, ids, context


@api.depends
------------

Will trigger the call of the function if specified on a function.
This is done an the function not aon the fields.
!! when you redefine depends you have te redefine all @api.depends
So it looses a lot of his interest....

@api.returns
------------

Guaranties unity of returned value.
It will returns a record set what ever your returning: ::
  @api.returns('res.partner')

And if an old api function call a new api function it will
automatically convert it into a list of ids

@api.one
--------

Loop automatically record of record set for you and set self as current record.

The decorator will allow to call the function from a RecordSet and
 it will automagically loop
and call the function on Recordset records

@api.multi
----------

Self wil lbe the record set without iteration-
it is the default behavior.

@api.model
----------

Convert v7 call on new api allows to be polite when when migrating code.

@api.constaints
---------------

Means the function is a checker function called on create write
Should raise a exceptions.Waring Wwith message if constraint is met.

@api.on_change
--------------
bla : ::

  @api.on_change('fieldx'):
  def do_stuff(self):
     if self.fieldx == x
        self.fieldy = 'toto'

In this case self correspond to the record on the form
The magical part is that the content of the form is put in the cache.
So you can alter the values inside you function.
Then difference with the cache et the output of your function will be returned
to the form. The cache will not be written in database.

The onchange are automagically inserted into the form.
If there is depends between fields the onchange will be automatically
inserted into the view.

to change domain or send a warning just return the usual dictionnary.
