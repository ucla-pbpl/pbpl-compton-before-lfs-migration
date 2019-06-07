# -*- coding: utf-8 -*-
import subprocess
import time
from tempfile import NamedTemporaryFile
import toml
import tqdm
import os

class Task:
    def __init__(self, conf, desc):
        self.conf = conf
        self.desc = desc

    def __del__(self):
        os.unlink(self.conf_filename)

    def start(self):
        with NamedTemporaryFile('w', delete=False) as f:
            self.conf_filename = f.name
            toml.dump(self.conf, f)
            f.close()
        self.proc = subprocess.Popen(
            ['pbpl-compton-mc', f.name],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def update_status(self):
        if self.proc.poll() is not None:
            self.bar.update(self.bar.total - self.bar.n)
            return False

        if len(self.proc.stderr.peek()) != 0:
            line = self.proc.stderr.readline().decode('utf-8')
            if line[:4] == 'TOT=':
                num_events = int(line[4:])
                fmt = ('{desc:>24s}:{percentage:3.0f}% ' +
                       '|{bar}| {n_fmt:>9s}/{total_fmt:<9s}')
                self.bar = tqdm.tqdm(
                    total=num_events, bar_format=fmt,
                    desc=self.desc)
            elif line[:4] == 'CUR=':
                current = int(line[4:])
                self.bar.update(current - self.bar.n)
        return True

class TaskRunner:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def run(self):
        for task in self.tasks:
            task.start()
        running_tasks = self.tasks
        while 1:
            for task in running_tasks:
                if task.update_status() == False:
                    running_tasks.remove(task)
            time.sleep(0.2)
            if len(running_tasks) == 0:
                break
