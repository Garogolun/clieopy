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

class RecordTypes:
    """ Contains the different record types. """

    BESTANDSVOORLOOP, \
    BESTANDSSLUIT, \
    BATCHVOORLOOP, \
    VASTEOMSCHRIJVING, \
    OPDRACHTGEVER, \
    BATCHSLUIT, \
    TRANSACTIE, \
    NAAMBETALER, \
    BETALINGSKENMERK, \
    OMSCHRIJVING, \
    NAAMBEGUNSTIGDE = range(11)

    record_prefix = {
        BESTANDSVOORLOOP:  "0001A",
        BESTANDSSLUIT:     "9999A",
        BATCHVOORLOOP:     "0010B",
        VASTEOMSCHRIJVING: "0020A",
        OPDRACHTGEVER:     "0030B",
        BATCHSLUIT:        "9990A",
        TRANSACTIE:        "0100A",
        NAAMBETALER:       "0110B",
        BETALINGSKENMERK:  "0150A",
        OMSCHRIJVING:      "0160A",
        NAAMBEGUNSTIGDE:   "0170B",
    }

    record_format = {
        BESTANDSVOORLOOP: [
            ("date"    , 6, "aanmaakdatum"                ),
            ("string"  , 8, "bestandsnaam"                ),
            ("string"  , 5, "inzenderidentificatie"       ),
            ("string"  , 4, "bestandsidentificatie"       ),
            ("boolean" , 1, "duplicaatcode"               ),
        ],
        BESTANDSSLUIT: [],
        BATCHVOORLOOP: [
            ("string"  ,  2, "transactiegroep"            ),
            ("number"  , 10, "rekeningnummeropdrachtgever"),
            ("number"  ,  4, "batchvolgnummer"            ),
            ("string"  ,  3, "aanleveringsmuntsoort"      ),
            ("string"  , 16, "batchidentificatie"         ),
        ],
        VASTEOMSCHRIJVING: [
            ("string"  , 32, "omschrijving"               ),
        ],
        OPDRACHTGEVER: [
            ("boolean" ,  1, "nawcode"                    ),
            ("date"    ,  6, "gewensteverwerkingsdatum"   ),
            ("string"  , 35, "naamopdrachtgever"          ),
            ("testcode",  1, "testcode"                   ),
        ],
        BATCHSLUIT: [
            ("number"  , 18, "totaalbedrag"               ),
            ("number"  , 10, "totaalrekeningen"           ),
            ("number"  ,  7, "aantalposten"               ),
        ],
        TRANSACTIE: [
            ("string"  ,  4, "transactiesoort"            ),
            ("number"  , 12, "bedrag"                     ),
            ("number"  , 10, "rekeningnummerbetaler"      ),
            ("number"  , 10, "rekeningnummerbegunstigde"  ),
        ],
        NAAMBETALER: [
            ("string"  , 35, "naambetaler"                ),
        ],
        BETALINGSKENMERK: [
            ("string"  , 16, "betalingskenmerk"           ),
        ],
        OMSCHRIJVING: [
            ("string"  , 32, "omschrijving"               ),
        ],
        NAAMBEGUNSTIGDE: [
            ("string"  , 35, "naambegunstigde"            ),
        ],
    }

def to_string(recordtype, **kwargs):
    """Creates a record (as string)."""

    result = [RecordTypes.record_prefix[recordtype]]  # record prefix

    try:
        recordargs = RecordTypes.record_format[recordtype]
    except KeyError:
        raise ValueError("Record type is not valid.")

    for datatype, length, name in recordargs:
        result.append(_formatarg(recordtype, datatype, length, kwargs[name]))

    ret = "".join(result)

    if len(ret) > 50:
        raise ValueError("Length of record exceeds 50 characters.")
    
    ret += " "*(50 - len(ret))  # Fill up the record string to 50 chars

    return ret
        
def _formatarg(rectype, datatype, length, data):
    """Formats a piece of data."""
    if datatype == "number":
        ret = ("%0" + str(length) + "d") % data
    elif datatype == "string":
        ret = data + " "*(length - len(data))
    elif datatype == "date":
        ret = data.strftime("%d%m%y")
    elif datatype == "boolean":
        ret = "1" if data else "0"
    elif datatype == "testcode":
        ret = "T" if data else "P"
    else:
        raise ValueError("Invalid data type.")

    if len(ret) > length:
        raise ValueError("Length of argument exceeds max length.")

    return ret

def write_record(f, rectype, **kwargs):
    """Writes a record to a file."""
    f.write(to_string(rectype, **kwargs) + '\n')
