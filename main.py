from models import *


@Field.rpy("!name[str] -u", pk=True)
@Field.rpy("!list[ItemList]")
class Item(Model):
    pass


@ForeignKey.rpy("*items[Item]", key="list")
class ItemList(Model):
    pass


if __name__ == '__main__':
    l = ItemList()

    Item(list=l, name="item 1")
    Item(list=l, name="item 2")
    Item(list=l, name="item 3")
    Item(list=l, name="item 4")

    for item in Item.findall(name=lambda name: name.startswith("item 5")):
        print(item)
