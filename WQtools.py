import work_queue

class WorkQueue:
    def __init__(self, port):
        work_queue.set_debug_flag('all')
        wq = work_queue.WorkQueue(port=port, exclusive=False, shutdown=False)
        wq.tasks_failed = 0 # Counter for tasks that fail at the application level
        wq.specify_keepalive_interval(8640000)
        wq.specify_name('dihedral')
        print('Work Queue listening on %d' % (wq.port))
        self.wq = wq

    
