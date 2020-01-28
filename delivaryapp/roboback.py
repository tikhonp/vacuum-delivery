import miio
from time import sleep

def_places = {'Детская': 1, 'Гостинная': 2, 'Спальня': 3, 'Кухня': 4}
tokens = {'ip': '10.0.1.90', 'token': '850a90fa537738678e016a7c94e2686722c71448'}
terget_positions = {1: (28000, 24000), 4: (21800, 25000)}


class robocontrol:
    def __init__(self, token=tokens['token'], ip=tokens['ip']):
        self.token = token
        self.ip = ip
        self.tasks = {}
        self.now_completed = None
        self.errors = []
        self.connect()

    def connect(self):
        self.v = miio.vacuum.Vacuum(self.ip, token=self.token, start_id=0)

    def gohome(self):
        try:
            self.v.home()
        except:
            self.connect()

    def addtasks(self, destX, destY, id):
        self.tasks[id] = {'destX': destX, 'destY': destY,
                          'is_active': False, 'is_complite': False}

    def runtask(self, task_id):
        try:
            self.tasks[task_id]['is_active'] = True
            self.v.goto(self.tasks[task_id]['destX'],
                        self.tasks[task_id]['destX'])
            while self.v.status().state == 'Going to target':  # !!!!!!!!!!!!!!!!
                sleep(2)
            self.tasks[task_id]['is_active'] = False
            self.tasks[task_id]['is_complite'] = False
            return 'ok'
        except Exception as e:
            self.connect()
            return e.message

    def main(self):
        try:
            self.connect()
            while True:
                u = False
                for i in self.tasks:
                    if u:
                        runtask(i)
                        break
                    else:
                        if self.tasks[i]['is_complite'] == False:
                            u = True
                sleep(1)
        except Exception as e:
            self.errors.append(e)
            self.main()
