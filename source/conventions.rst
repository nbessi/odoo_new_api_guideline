Conventions
===========

Snake_casing or CamelCasing
---------------------------
That was not clear.
But it seems that OpenERP SA will continue to use snake case

Imports
-------
Has disscussed with Raphael Collet
This convention should be the one to use after RC1.

Model
#####

:: 

  from openerp import models

Fields
######

from openerp import fields

Translation
###########

::

  from openerp import _

API
###

::

  from openerp import api

Exceptions
##########
from openerp import exceptions

A typical module import would be: ::
  
  from openerp import models, fields, api, _

Classes
-------
Class should be initialized like this: ::

    class Toto(models.Model):
       pass

New Exceptions classes
----------------------

``except_orm`` exception is deprecated.
We should use ``openerp.exceptions.Warning`` and subclasses instances

RedirectWarning
###############

Warning with a possibility to redirect the user instead of simply
diplaying the warning message.

Should receive as parameters:
:param int action_id: id of the action where to perform the redirection
:param string button_text: text to put on the button that will trigger
the redirection.

AccessDenied
############

Login/password error. No message, no traceback

AccessError
###########

Access rights error.

class MissingError:
###################

Missing record(s)

DeferredException:
##################

Exception object holding a traceback for asynchronous reporting.

Some RPC calls (database creation and report generation) happen with
an initial request followed by multiple, polling requests. This class
is used to store the possible exception occuring in the thread serving
the first request, and is then sent to a polling request.

('Traceback' is misleading, this is really a exc_info() triple.)


Compatibility
#############

When catching orm exception we should catch both type of exceptions: ::

    try:
        pass
    except(Waring, except_orm) as exc:
        pass


Fields
------

Fields should be declared using new fields API.
Putting string key is better than using  a long property name: ::

    class AClass(models.Model):

        name = fields.Char(string="This is a really long long name") # ok
        really_long_long_long_name = fields.char()

That said the property name must be meaningfull. Avoid name like 'nb' etc.


Default or compute
------------------

Compute option should not be used as a workaround to set default.
Defaut should only be used to provide property initialisation.

That said they may share same function

Modifing self in method
-----------------------

We should never alter self in a Model function.
It will break the correlation with current environement caches.


Doing thing in dry run
----------------------

if you use the do_in_draft contenxt manager of Environnement
It will not be committed but only be done in cache.


Using Cursor
------------

When using cursor you should use current environnement cursor: ::

      self.env.cr

except if you need to use threads: ::

    with Environment.manage(): #class function
        env = Environnement(cr, uid, context)

Displayed Name
--------------

`_name_get` is deprecated.

You should define the display_name field with options:

 * compute
 * inverse


Constraint
----------
Should be done using ``@api.constraints`` decorator in
conjunction with the ``@api.one`` if performance allows it.


Qweb view or not Qweb view
--------------------------

If no advance behavior is needed on Model view,
standard view (non Qweb) should be the preferred choice.


Javascript and Website related code
-----------------------------------

General guideline should be found:

 * https://doc.openerp.com/trunk/web/guidelines/
 * https://doc.openerp.com/trunk/server/howto/howto_website/
