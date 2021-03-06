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
    DIRECTDEBIT_PURE        = "1001"
    DIRECTDEBIT_IMPURE      = "1002"

    def get_type(is_directdebit, is_pure, is_salary=False):
        """Return the correct transaction type for the given parameters.

        is_directdebit -- whether the transaction is a payment or direct debit
        is_pure        -- whether the transaction is pure
        is_salary      -- salary or creditor payment? (ignored for debits)

        """
        if is_directdebit:
            if is_pure:
                return DIRECTDEBIT_PURE
            else:
                return DIRECTDEBIT_IMPURE
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

    PAYMENTS     = "00"
    DIRECTDEBITS = "10"
    UNKNOWN      = None

    def is_valid_type(transactiongroup, transactiontype):
        """Check if the type is valid for the given group.
        
        Note: it is assumed that the transaction type itself is valid."""

        if transactiongroup == PAYMENTS:
            return transactiontype in [
                CREDITOR_PAYMENT_IMPURE,
                SALARY_PAYMENT_IMPURE,
                CREDITOR_PAYMENT_PURE,
                SALARY_PAYMENT_PURE]
        elif transactiongroup == DIRECTDEBITS:
            return transaction_type in [
                DIRECTDEBIT_PURE,
                DIRECTDEBIT_IMPURE]
        elif transactiongroup == UNKNOWN:
            return False  # you should not use UNKNOWN in applications
        else:
            raise ValueError("Transaction group not valid.")
