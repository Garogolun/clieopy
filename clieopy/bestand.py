# Copyright (c) 2012, Timmy Weerwag
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * The names of its contributors may not be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from record import RecordTypes, write_record
from transactiontypes import TransactionGroups
from batch import Batch

class Bestand:

    """Represents a CLIEOP03 file."""

    # This generic class has no restriction on the transaction group (but
    # shouldn't be used in real life!)
    transactiongroup = TransactionGroups.UNKNOWN

    def __init__(self, date, index=1, duplicate=False, senderident=""):
        """Construct a BatchFile.

        date        -- a datetime or date object (supporting strftime)
        indexnumber -- used when creating more than one CLIEOP03 file per day
        duplicate   -- whether this file is a duplicate
        senderident -- a sender identification

        """
        self.recordargs = {
            'aanmaakdatum'         : date                          ,
            'bestandsnaam'         : "CLIEOP03"                    ,
            'inzenderidentificatie': senderident                   ,
            'bestandsidentificatie': "%02d%02d" % (date.day, index),
            'duplicaatcode'        : duplicate                     ,
        }
        self.batches = []

    def create_batch(self, accountnumber, currency="EUR"):
        """Create and add a batch to this file.

        accountnumber    -- account on our side (payed from or collected to)
        currency         -- currency to use

        Returns the created batch.

        """
        batch = Batch(self.transactiongroup, accountnumber, currency)
        self.batches.append(batch)
        return batch

    def write_to_file(self, f):
        """Write a BatchFile to a file object.
        
        f -- the file to write to (needs to support write)
        
        """
        write_record(f, RecordTypes.BESTANDSVOORLOOP, **self.recordargs)
        for i, batch in enumerate(self.batches):
            batch.write_to_file(f, i+1)  # i+1 -- people start counting at 1
        write_record(f, RecordTypes.BESTANDSSLUIT)

class BetalingBestand(Bestand):

    """Represents a CLIEOP03 file with payments.

    A CLIEOP03 file may only contain batches of the same transaction group
    (payment or direct debtits).

    """

    # Only allow payment batches
    transactiongroup = TransactionGroups.PAYMENTS

class IncassoBestand(Bestand):

    """Represents a CLIEOP03 file with direct debits.

    A CLIEOP03 file may only contain batches of the same transaction group
    (payment or direct debits).

    """

    # Only allow collect transactions
    transactiongroup = TransactionGroups.DIRECTDEBITS
