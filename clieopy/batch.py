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
from omschrijving import Omschrijving
import datetime

class Batch:

    """Represents a single CLIEOP03 batch."""

    def __init__(self, transactiongroup, accountnumber,
            processingdate=datetime.date.today(), currency="EUR", clientname=""):
        """Construct a Batch.

        transactiongroup -- transaction group (payments or collections)
        accountnumber    -- account on our side (payed from or collected to)
        currency         -- currency to use

        """
        self.recordargs = {
            'transactiegroep': transactiongroup,
            'rekeningnummeropdrachtgever': accountnumber,
            'batchvolgnummer': 0,
            'aanleveringsmuntsoort': currency,
            'batchidentificatie': "",
            'nawcode': False,
            'gewensteverwerkingsdatum': processingdate,
            'naamopdrachtgever': clientname,
            'testcode': False,
        }
        self.description = None

    def add_default_description(self, lines):
        """Add a default description to every transaction in this batch.

        lines -- the description lines, array of max 4 strings of max 32 chars

        """
        desc = Omschrijving(lines, True)
        self.description = desc

    def write_to_file(self, f, index):
        """Write a Batch to a file object.
        
        f     -- the file to write to (needs to support write)
        index -- index number of this batch
        
        """

        recordargs = self.recordargs
        recordargs.update({
            'batchvolgnummer': index,
            'totaalbedrag': 0,
            'totaalrekeningen': 0,
            'aantalposten': 0,
        })

        write_record(f, RecordTypes.BATCHVOORLOOP, **recordargs)

        try:
            self.description.write_to_file(f)
        except AttributeError:
            pass

        write_record(f, RecordTypes.OPDRACHTGEVER, **recordargs)

        # TODO: Loop over transactions

        write_record(f, RecordTypes.BATCHSLUIT, **recordargs)
