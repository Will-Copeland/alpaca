


def send_order(direction, bar):
  try:

    api.submit_order(
    symbol='AAPL',
    qty=100,
    side="buy",
    type='market',
    time_in_force='fok',
    order_class='simple',
    # stop_loss=dict(stop_price=str(sl)),
    # take_profit=dict(limit_price=str(tp)),
    client_order_id="0009"
    )
    print("Buy ord sent!")
    print(resp)