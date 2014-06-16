Compatibility
=============
There is some pattern to know during the transition period to keep code base
compatible with both old and newe API.

Access old API
--------------

By default, bz using new API your are going to working on self will use new RecordSet class.
But old context and model are still available using: ::

    self.pool
    self._model


How to  be polite with old code base
------------------------------------
If your code must be used by old API code base,
It should be decorated by:

 * `@api.return` to ensure adapted returned values
 * `@api.model` to ensure that new signature support old api calls
