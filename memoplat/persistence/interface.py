class MemoRepository:
    def save(self, memo):
        raise NotImplementedError

    def remove(self, id_):
        raise NotImplementedError

    def get(self, id_):
        raise NotImplementedError


class CategoryRepository:
    def save(self, category):
        raise NotImplementedError

    def remove(self, id_):
        raise NotImplementedError

    def get(self, id_):
        raise NotImplementedError


class TagRepository:
    def save(self, tag):
        raise NotImplementedError

    def remove(self, id_):
        raise NotImplementedError

    def get(self, id_):
        raise NotImplementedError
