# without mapping
items = [1, 2, 3, 4, 5]

squared = []
for x in items:
    squared.append(x ** 2)
print squared




# with mapping

items = [1, 2, 3, 4, 5]

def sqr(x):
    if x % 2 == 0:
        return x ** 2
    else:
        return

result = map(sqr, items)

print result

evens = filter(lambda a: a != 0, result)

print evens