=======
Clieopy
=======

Clieopy is a module for accessing CLIEOP03_ files. This format is used by Dutch
bankers for batch payments.

.. _CLIEOP03: http://www.equens.com/Images/CLIEOP%20NL.pdf

-------
Example
-------

A quick example which shows how to make a batch follows. *Warning: this example
is not normative! The API may change in future versions.*

::

    from clieopy.batchfile import PaymentBatchFile
    import datetime

    # First construct the batch file
    batchfile = PaymentBatchFile(datetime.date.today())

    # Now we can add a batch to the file
    #batch = batchfile.create_batch(account_number)    # Not implemented yet

    # Write to file
    with open("clieop03.txt", "w") as file:
        batchfile.write_to_file(file)

--------------
Pure vs impure
--------------

Most Dutch banks use 9-digit account numbers, with one digit used for some sort
of checksum to prevent typing errors. One bank used shorter numbers (from 1 to 7
digits long). Instead of a checksum, they checked the name on the transaction
with the account holder.

With batches you don't have to provide the names if you are sure the numbers are
right. If for some reason you aren't sure, you can flag them as impure and
provide names. The bank will then check them before clearing.

**Still WIP!**
