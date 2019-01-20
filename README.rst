========
MemoPlat
========
| 様々な知識をメモとして残すプログラム。


==========
how to use
==========
使用の前にsqliteのdb_file_pathを設定してください。

    from memoplat.config import configure

    db_file_path = 'tmp/.../sqlite.db'
    configure(db_file_path)
