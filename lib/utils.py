
class Pagination(object):
    __slots__ = ['page', 'size', 'total', 'items']

    def __init__(self, page, size, total, items):
        self.page = page
        self.size = size
        self.total = total
        self.items = items

    def has_next(self):
        return self.total > self.page * self.size

    def to_dict(self):
        return {
            'page': self.page,
            'size': self.size,
            'total': self.total,
            'items': self.items,
        }