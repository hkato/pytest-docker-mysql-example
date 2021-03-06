import multiprocessing

from gunicorn.app.base import BaseApplication


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def run(host, port):
    options = {
        'bind': '%s:%s' % (host, port),
        'workers': number_of_workers(),
        'worker_class': 'uvicorn.workers.UvicornWorker',
        'accesslog': '-',
        'errorlog': '-'
    }

    import myapp.main

    StandaloneApplication(myapp.main.app, options).run()
