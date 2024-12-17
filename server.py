#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
import json
import stripe
from flask import Flask, jsonify, redirect, request,render_template

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51PTl2QRu0n90tW5pJz9ojTwjBspu28uSVyFF6oYNbGapToHYTho5tGJ7qnIHyvWMnNHyOex1RwEvM612gL1rLVDN00hNe05VmN'
# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_a777d4d02796b2775f33fc51bdcfc3b043c6559c934103e9530730815135e026'

app = Flask(__name__)

# YOUR_DOMAIN = 'https://memoreal.shop'
YOUR_DOMAIN = 'http://localhost:4242'

@app.route('/')
def index():
    return render_template('checkout.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            ui_mode = 'embedded',
            billing_address_collection='auto',
            shipping_address_collection={
              'allowed_countries': ['JP', 'CA'],
            },
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1PTl7IRu0n90tW5pgbQFdqxp',
                    'quantity': 1,
                },
            ],
            mode='payment',
            return_url=YOUR_DOMAIN + '/return.html?session_id={CHECKOUT_SESSION_ID}',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return jsonify(clientSecret=session.client_secret)

@app.route('/session-status', methods=['GET'])
def session_status():
  session = stripe.checkout.Session.retrieve(request.args.get('session_id'))

  return jsonify(status=session.status, customer_email=session.customer_details.email)

@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
        # Handle the async payment failure
        print("Async payment failed:", json.dumps(session, ensure_ascii=False, indent=2))
    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']
        # Handle the async payment success
        print("Async payment succeeded:", json.dumps(session, ensure_ascii=False, indent=2))
    elif event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Handle the checkout session completion
        print("Checkout session completed:", json.dumps(session, ensure_ascii=False, indent=2))
    elif event['type'] == 'checkout.session.expired':
        session = event['data']['object']
        # Handle the checkout session expiration
        print("Checkout session expired:", json.dumps(session, ensure_ascii=False, indent=2))
    elif event['type'] == 'charge.updated':
        charge = event['data']['object']
        # Handle the charge update
        print("Charge updated:", json.dumps(charge, ensure_ascii=False, indent=2))
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)

@app.route('/return.html', methods=['GET'])
def return_html():
    session_id = request.args.get('session_id')
    return render_template('return.html', session_id=session_id)

if __name__ == '__main__':
    app.run(port=4242)