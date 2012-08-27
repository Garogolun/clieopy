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

from fixedformat import FixedFormat
from transactiontypes import TransactionGroups

class BatchFile:

    """Represents a CLIEOP03 file.

    The name is chosen instead of just File to avoid confusion with regular
    files.

    """

    # This generic class has no restriction on the transaction types
    transaction_type = TransactionGroups.UNKNOWN

    def __init__(self, date, indexnumber=1, duplicate=False):
        """Construct a BatchFile.

        date        -- a datetime or date object (supporting strftime)
        indexnumber -- used when creating more than one CLIEOP03 file per day
        duplicate   -- whether this file is a duplicate

        """
        self.date = date
        self.indexnumber = indexnumber
        self.duplicate = duplicate

    def write_to_file(self, f):
        """Write a BatchFile to a file object.
        
        f -- the file to write to (needs to support write)
        
        """

        # Write header
        fileheader = FixedFormat("0001A%6sCLIEOP03XXXXX%02d%02d%1d", 50)
        f.write(fileheader.pack(
            self.date.strftime("%d%m%y"), self.date.day, self.indexnumber,
            1 if self.duplicate else 0) + '\n')

        # TODO: Loop over batch-stuff

        # Write footer
        f.write(FixedFormat("9999A", 50).pack() + '\n')

class PaymentBatchFile(BatchFile):

    """Represents a CLIEOP03 file with payments.

    A CLIEOP03 file may only contain batches of the same transaction type
    (payment or collect).

    """

    # Only allow payment batches
    transaction_type = TransactionGroups.PAYMENTS

class CollectBatchFile(BatchFile):

    """Represents a CLIEOP03 file with collections.

    A CLIEOP03 file may only contain batches of the same transaction type
    (payment or collect).

    """

    # Only allow collect transactions
    transaction_type = TransactionGroups.COLLECTIONS
