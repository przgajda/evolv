'''
Created on 2011-05-21

@author: quermit
'''
import time


class Meeting(object):

    meetings = {}

    def __init__(self, agent1, agent2):
        self.handle(agent1, agent2)

    def handle(self, agent1, agent2):
        meeting_id = "%s:%s" % tuple(sorted([id(agent1), id(agent2)]))
        result = self.run(agent1, agent2, Meeting.meetings.get(meeting_id))
        Meeting.meetings[meeting_id] = {'time': time.time(), 'result': result}

    def run(self, agent1, agent2, last_info):
        pass


class RabbitPlantMeeting(Meeting):

    def run(self, rabbit, plant, last_info):
        if last_info is None:
            return

        time_diff = time.time() - last_info['time']
        energy_diff = time_diff * 10  # eating speed
        rabbit.update_energy(+energy_diff)
        plant.update_energy(-energy_diff)


class WolfRabbitMeeting(Meeting):

    def run(self, wolf, rabbit, last_info):
        if last_info is None:
            return

        time_diff = time.time() - last_info['time']

        if rabbit.health > 0.01:
            health_diff = time_diff * 30  # attack power
            rabbit.update_health(-health_diff)
            wolf.update_energy(+health_diff)
        else:
            energy_diff = time_diff * 10  # eating speed
            wolf.update_energy(+energy_diff)
            rabbit.update_energy(-energy_diff)


class RabbitRabbitMeeting(Meeting):

    def run(self, rabbit1, rabbit2, last_info):
        from controls.environ import Environ
        environment = Environ.instance

        if last_info is None:
            return 0

        if rabbit1.get_age() < 8.0 or rabbit2.get_age() < 8.0:
            return 0

        if rabbit1.health < 20.0 or rabbit2.health < 20.0:
            return 0

        if rabbit1.energy < 60 or rabbit2.energy < 60:
            return 0

        res = last_info['result']
        time_diff = time.time() - res

        if time_diff > 2.0:
            rabbit1.update_energy(-10.0)
            rabbit2.update_energy(-10.0)
            environment.born_rabbit(rabbit1, rabbit2)
            return time.time()
        else:
            return res


class WolfWolfMeeting(Meeting):

    def run(self, wolf1, wolf2, last_info):
        from controls.environ import Environ
        environment = Environ.instance

        if last_info is None:
            return 0

        if wolf1.get_age() < 25.0 or wolf2.get_age() < 25.0:
            return 0

        if wolf1.health < 20.0 or wolf2.health < 20.0:
            return 0

        if wolf1.energy < 60 or wolf2.energy < 60:
            return 0

        res = last_info['result']
        time_diff = time.time() - res

        if time_diff > 10.0:
            wolf1.update_energy(-25.0)
            wolf2.update_energy(-25.0)
            environment.born_wolf(wolf1, wolf2)
            return time.time()
        else:
            return res




