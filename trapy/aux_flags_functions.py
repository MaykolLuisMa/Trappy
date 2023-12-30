def always(a):
    return True
def is_sync(flags):
    return ((flags & 2) > 0)
def is_ack(flags):
    return ((flags & 16) > 0)
def is_sync_ack(flags):
    return (is_ack(flags) and is_sync(flags))