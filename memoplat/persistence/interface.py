##############################################################################
# for command ################################################################
##############################################################################
class MemoRepository:
    def new(self, **kwargs):
        raise NotImplementedError

    def save(self, memo, update=False):
        raise NotImplementedError

    def remove(self, value, by='id'):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError
