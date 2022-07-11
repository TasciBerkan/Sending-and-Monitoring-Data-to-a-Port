import os
import random
from datetime import datetime
# pip install Faker
from faker import Faker
from time import sleep
from faker.providers import BaseProvider
import logging
# pip install pyzmq
import zmq

random.seed = 0
Faker.seed = 0

logging.basicConfig()
_logger = logging.getLogger('test')
_logger.setLevel(logging.DEBUG)


class ModuleProvider(BaseProvider):
    def module_name(self):
        return random.choice(['evse', 'ocpp', 'slac'])

    def module_state(self):
        # Random states are not really reasonable, but this is just for testing.
        return random.choice(['initializing', 'idle', 'charging', 'finalizing'])

    def module_output(self):
        # Make stdout have 2/3 probability.
        stream = random.choice(['stdout', 'stdout', 'stderr'])
        message = 'Something happened.'
        return (stream, message)


fake = Faker()
fake.add_provider(ModuleProvider)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")


def out():
    try:
        while True:
            log_output = fake.module_output()
            msg = {
                'module': fake.module_name(),
                'timestamp': datetime.now().isoformat(),
                'state': fake.module_state(),
                'log-stream': log_output[0],
                'log-message': log_output[1],
            }
            _logger.debug(msg)
            socket.send_json(msg)

            sleep(random.uniform(0, 0.5))

        #Only letting the user be able to stop the program fully in any other case of error program will tell you it occurred but continue generating logs.
    except KeyboardInterrupt:
        print("YOU PRESSED CTRL+C PROGRAM IS INTERRUPTED")
    except (RuntimeError,socket.error) as error:
        print("AN ERROR HAS OCCURRED AND HANDLED PROGRAM WILL CONTINUE")
        
        out()

out()