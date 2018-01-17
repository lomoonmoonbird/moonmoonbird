#--*-- coding:utf-8 --*--

import trafaret as T


TRAFARET = T.Dict({
    T.Key('mongodb'):
        T.Dict({
            'database': T.String(),
            'host': T.String(),
            'port': T.Int(),
            'max_pool_size': T.Int(),
        }),

    T.Key('mysql'):
        T.Dict({
            'database': T.String(),
            'host': T.String(),
            'port': T.Int(),
            'user': T.String(),
            'password': T.String(),
        }),

    T.Key('host'): T.IP,
    T.Key('port'): T.Int(),
}
)

