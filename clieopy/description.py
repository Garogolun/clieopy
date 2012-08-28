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

class Description:

    """Represents a one to four description records."""

    def __init__(self, lines, default=False):
        """Construct a Description.

        lines   -- the description lines, list of max 4 strings max 32 chars
        default -- whether this is a default description for a batch

        """

        if len(lines) > 4:
            raise ValueError("Descriptions can't contain more than 4 strings.")

        for line in lines:
            if len(line) > 32:
                raise ValueError("Description lines are max 32 characters.")

        self.lines   = lines
        self.default = default

    def write_to_file(self, f):
        """Write description records to a file object.
        
        f     -- the file to write to (needs to support write)
        
        """
        # Write description records
        # 0020 -- record type (for default descriptions)
        # 0160 -- record type (for normal descriptions)
        # A    -- variant
        # %32s -- description line
        recordtype = "0020" if self.default else "0160"
        for line in self.lines:
            f.write(FixedFormat("%4sA%32s", 50).pack(recordtype, line) + '\n')
