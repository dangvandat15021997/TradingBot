from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class coin_pair(Model):
    id = fields.UUIDField(pk=True)
    symbol = fields.CharField(max_length=30, nullable=False)
    interval = fields.CharField(max_length=30, nullable=False)
    
    class Meta:
        table = "coin_pair"
        unique_together = ("symbol", "interval")


coin_pair_pydantic = pydantic_model_creator(coin_pair, name="coin_pair")
coin_pair_pydanticIn = pydantic_model_creator(coin_pair, name="coin_pairIn", exclude_readonly=True)

class coin_price(Model):
    id = fields.UUIDField(pk=True)
    id_coin_pair = fields.ForeignKeyField('models.coin_pair', related_name='fk_coin_price_coin_pair')
    open_time = fields.DatetimeField(null=False)
    open = fields.FloatField(null = False)
    high = fields.FloatField(null = False)
    low  = fields.FloatField(null = False)
    close = fields.FloatField(null = False)
    volume = fields.FloatField(null = False)
    close_time = fields.DatetimeField(null = False)
    quote_asset_volume =  fields.FloatField(null = True)
    num_of_trades =  fields.FloatField(null = True)
    taker_buy_base =  fields.FloatField(null = True)
    taker_buy_quote =  fields.FloatField(null = True)
    
    
    class Meta:
        table = "coin_price"
        unique_together = ("id_coin_pair", "open_time")

coin_price_pydantic = pydantic_model_creator(coin_price, name="coin_price")
coin_price_pydanticIn = pydantic_model_creator(coin_price, name="coin_priceIn", exclude_readonly=True)

# just 2 table create