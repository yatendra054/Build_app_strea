import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Mortgage Calcuator")

st.write("### Input data ")
col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value", min_value=0, max_value=5000000)
deposit = col1.number_input("Deposit", min_value=0, max_value=1000000)
interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, max_value=7.5)
long_term = col2.number_input("Long Term (in Year)",min_value=1, max_value=30)

loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate/100)/12
number_payments = long_term * 12
if monthly_interest_rate > 0:
    monthly_payments = (
            loan_amount
            * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_payments)
            / ((1 + monthly_interest_rate) ** number_payments - 1)
    )
else:
   monthly_payments = loan_amount/number_payments
total_payments = monthly_payments * number_payments
total_interest = total_payments-loan_amount
st.write("### Repayments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayment",value=f"${monthly_payments:,.2f}")
col2.metric(label="Total Repayment",value=f"${total_payments:,.0f}")
col3.metric(label="Total Interest",value=f"${total_interest:,.0f}")

schedule = []
remaining_balance = loan_amount
for i in range(1,number_payments+1):
    interest_payment = remaining_balance*monthly_interest_rate
    principal_payment = monthly_payments-interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i/12)
    schedule.append(
        [
            i,
            monthly_payments,
            principal_payment,
            interest_payment,
            remaining_balance,
            year
        ]
    )
df = pd.DataFrame(
    schedule, columns=['Monthly', 'Payment', 'Principal', 'Interest', 'Remaining balance', 'Year']
)
st.write("### Payment schedule")
payment_df = df[['Year','Remaining balance']].groupby('Year').min()
st.line_chart(payment_df)
