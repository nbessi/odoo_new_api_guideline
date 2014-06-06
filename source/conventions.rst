Conventions
===========


Class should use CamelCase
##########################

Imports
-------
Has disscussed with Raphael Collet
This convention should be the one to use after RC1.

Model
#####

from openerp import model

Fields
######

from openerp import fields

Translation
###########
from openerp import _

API
###
from openerp import api

Exceptions
##########
from openerp import exceptions

A typical module import would be: ::
  from openerp import Model, fields, api, _

Classes
-------
Class should be initialized like this: ::

class Toto(model.Model):
   pass

New Exceptions classes
----------------------

exceptions.except_orm/orm.except_orm is deprecated.
You should uses

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
""" Access rights error. """

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


Fields
------

Field should be done instanciante using new fields
Putting string key is better as explicit is better than implicit: ::

    class AClass(model.Model):
        name = fields.Char(strin
Default or compute
==================
TODO

Modifing self in method
=======================

Refer to env TODO

Do not do it.


Doing thing in dry run
======================
if you use the do_in_draft contenxt manager of Environnement
It will not be committed but only be done in cache.


Using Cursor
============

When using cursor you should use environnement cursor: ::
      self.env.cr
Then you cau use cursor like in previous API

Using thread
============
When using thread you have to create you own cursor
and initiate a new environnement for each thread.
committing is done by committing the cursor.

   with Environment.manage(): #class function
      env = Environnement(cr, uid, context)

Name get
========
_name_get is deprecated.
You should override the display_name fields compute fucntion:
compute key
inverse key


Constraint
==========
Should be done using @api.constraints decorator in
conjunction with the @api.one if performance allows it.

todo ref to @api.constraints


Qweb view or not Qweb view
=========================

If no advance behavior is needed on Model view,
standard view (non Qweb) should be the preferred choice.


Javascript and Website related code
===================================

General guideline should be found:

 * https://doc.openerp.com/trunk/web/guidelines/
 * https://doc.openerp.com/trunk/server/howto/howto_website/
Templating using Qweb
---------------------
When showing partner
