import json, sys, os

from cieloApi3 import  *

environment = Environment ( sandbox = True )

merchant = Merchant ( '889061f5-5deb-4593-b742-8ece89222bf6' , 'STXEDSMMRCLXBXOYWSUYYPOZGCJSFYAHYTZTPCET' )

sale = Sale ('123')

sale.customer = Customer ( 'Teste Holder' )

credit_card = CreditCard ( '123' , 'Visa' )

credit_card.expiration_date =  '12/2024'  

credit_card.card_number =  '1234123412341234'  

credit_card.holder =  'Teste Holder'
credit_card.return_url = 'http://10.6.7.88:9000'

sale.payment = Payment ( 15700 )

sale.payment.credit_card = credit_card

cielo_ecommerce = CieloEcommerce (merchant, environment)

response_create_sale = cielo_ecommerce.create_sale (sale)

print  '\n---------------------- response_create_sale --------- - ----------- '

print json.dumps (response_create_sale, indent = 2 )

print  '\n---------------------- response_create_sale - -------------------- '
payment_id = sale.payment.payment_id

response_capture_sale = cielo_ecommerce.capture_sale (payment_id, 15700 , 0 )

print  '\n---------------- - ---- response_capture_sale ---------------------- '

print json.dumps (response_capture_sale, indent = 2 )

print  '\n------- - ------------- response_capture_sale ---------------------- '

response_cancel_sale = cielo_ecommerce.cancel_sale (payment_id, 15700 )

print  '\n--------------------- response_cancel_sale ---- - --------------- '

print json.dumps (response_cancel_sale, indent = 2 )

print  '\n------------------- - response_cancel_sale --------------------- '






