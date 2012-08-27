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

class Batch:

    """Represents a single CLIEOP03 batch."""

    def __init__(self, transactiongroup, accountnumber, currency="EUR"):
        """Construct a Batch.

        transactiongroup -- transaction group (payments or collections)
        accountnumber    -- account on our side (payed from or collected to)
        currency         -- currency to use

        """
        self.transactiongroup = transactiongroup
        self.accountnumber = accountnumber
        self.currency = currency

    def write_to_file(self, f, index):
        """Write a BatchFile to a file object.
        
        f     -- the file to write to (needs to support write)
        index -- index number of this batch
        
        """

        # Write header
        # 0010 -- record type (batch header)
        # B    -- variant
        # %2s  -- transaction group (00 or 10)
        # %10s -- bank account number
        # %04d -- batch index number
        # %3s  -- currency
        # %16s -- batch identification
        f.write(FixedFormat("0010B%2s%10s%04d%3s%16s", 50).pack(
            self.transactiongroup, self.accountnumber, index, self.currency,
            "hoepladoepla") + '\n')

        # TODO: Loop over transacties-stuff

        # Write footer
        # 9990  -- record type (batch footer)
        # A     -- variant
        # %018d -- total sum (in cents)
        # %010d -- checksum of account numbers
        # %07d  -- amount of records in batch
        f.write(FixedFormat("9990A%018d%010d%07d", 50).pack(
            0, 0, 0) + '\n')
