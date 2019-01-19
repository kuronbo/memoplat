##############################################################################
# for command ################################################################
##############################################################################
class MemoRepository:
    def save(self, memo, update=False):
        raise NotImplementedError

    def remove(self, id):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError


class TagRepository:
    def save_some(self, tags, memo_id):
        raise NotImplementedError

    def get_tags(self, values, by='id'):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError


class CategoryRepository:
    def save(self, category):
        raise NotImplementedError

    def get(self, value, by='id'):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError


##############################################################################
# for query ##################################################################
##############################################################################

