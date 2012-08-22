=======
Clieopy
=======

Clieopy is a module for accessing CLIEOP03 files. This format is used by Dutch
bankers for batch payments.

-------
Example
-------

A quick example which shows how to make a batch follows. **Warning: this is
not normative! The API may change in future versions.**

::

  import clieopy
  import datetime

  # This will return a clieopy.PaymentFile to which batches can be added.
  file = clieopy.create_payment_file(datetime.date.today(), "filename")

  # Now we create a clieopy.Batch instance.
  batch = file.create_batch(account_number)

**Still WIP!**
