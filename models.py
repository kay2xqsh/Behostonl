import peewee

db = peewee.SqliteDatabase('database.sqlite3')


class Shop(peewee.Model):
    name = peewee.CharField(unique=True)

    class Meta:
        database = db

    @classmethod
    def get_id_by_name(cls, name: str) -> int:
        return cls.get(Shop.name == name)

    def __str__(self):
        return 'Shop({name})'.format(name=self.name)


class Promotion(peewee.Model):
    shop = peewee.ForeignKeyField(Shop)
    product_name = peewee.CharField()
    old_price = peewee.FloatField()
    new_price = peewee.FloatField()
    url = peewee.CharField()
    code = peewee.CharField(null=True)

    def __init__(self, *args, **kwargs):
        if isinstance(kwargs['shop'], str):
            kwargs['shop'] = Shop.get(name=kwargs['shop'])
        super().__init__(*args, **kwargs)

    class Meta:
        database = db

    def __str__(self):
        return (
            'Promotion('
            '{shop_name}, '
            '{product_name}, '
            '{old_price}, '
            '{new_price}, '
            '{url}, '
            '{code})').format(
            shop_name=self.shop,
            product_name=self.product_name,
            old_price=self.old_price,
            new_price=self.new_price,
            url=self.url,
            code=self.code,
        )


if __name__ == '__main__':
    db.connect()
    db.create_tables([Shop, Promotion])
    Shop.insert_many([
        {'name': 'xkom'},
        {'name': 'alto'},
        {'name': 'morele'},
    ]).on_conflict_ignore().execute()
