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

class TransactionTypes:

    """Contains the possible transaction types."""

    CREDITOR_PAYMENT_IMPURE = "0000"
    SALARY_PAYMENT_IMPURE   = "0003"
    CREDITOR_PAYMENT_PURE   = "0005"
    SALARY_PAYMENT_PURE     = "0008"
    COLLECTION_PURE         = "1001"
    COLLECTION_IMPURE       = "1002"

    def get_type(is_collection, is_pure, is_salary=False):
        """Return the correct transaction type for the given parameters.

        is_collection -- whether the transaction is a payment or collection
        is_pure       -- whether the transaction is pure
        is_salary     -- salary or creditor payment? (ignored for collections)

        """
        if is_collection:
            if is_pure:
                return COLLECTION_PURE
            else:
                return COLLECTION_IMPURE
        else:
            if is_pure:
                if is_salary:
                    return SALARY_PAYMENT_PURE
                else:
                    return CREDITOR_PAYMENT_PURE
            else:
                if is_salary:
                    return SALARY_PAYMENT_IMPURE
                else:
                    return CREDITOR_PAYMENT_IMPURE

class TransactionGroups:

    """Contains the possible transaction groups. """

    PAYMENTS, COLLECTIONS, UNKNOWN = range(3)

    def is_valid_type(transaction_group, transaction_type):
        """Check if the type is valid for the given group.
        
        Note: it is assumed that the transaction type itself is valid."""

        if transaction_group not in range(3):
            raise ValueError

        if transaction_group == PAYMENTS:
            return transaction_type in [
                CREDITOR_PAYMENT_IMPURE,
                SALARY_PAYMENT_IMPURE,
                CREDITOR_PAYMENT_PURE,
                SALARY_PAYMENT_PURE]
        elif transaction_group == COLLECTIONS:
            return transaction_type in [
                COLLECTION_PURE,
                COLLECTION_IMPURE]
        else:  # transaction_group == UNKNOWN
            return False  # you should not use UNKNOWN in applications
