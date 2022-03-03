from livevolpy.client import LiveVolClient, create_json_file
import time

client = LiveVolClient('client_id', 'client_secret')
client.authorize()
today = time.strftime('%Y-%m-%d')
symbol = 'SPY'
params = {'symbol':symbol,'root':symbol,'date':today}
breakdown = client.get_option_trades_breakdown(params)
create_json_file('breakdown.json', breakdown)
options = client.get_options_and_underlying_quotes(params)
create_json_file('options.json', options)
params['order_by'] = 'SIZE_DESC'
trades = client.get_trades(params)
create_json_file('trades.json', trades)