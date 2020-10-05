import os

import fs
from fs.errors import ResourceNotFound

from integrations import SavageRentals


class CouldntObtainFileHandle(Exception):
    pass


class FileInterface(object):

    def __init__(self, file_sys, num_fails_to_tolerate=10):
        self.file_sys = file_sys
        self.num_fails_to_tolerate = num_fails_to_tolerate

    def write_file(self, content, path):
        done = False
        num_fails = 0
        dest_dir = self.file_sys.makedirs(path)
        while not done:
            file_list = dest_dir.listdir(".")

            file_idx = max( (int(x.split('.')[0]) for x in file_list) ) if file_list else 1
            try:
                f = dest_dir.open('%s.txt'%file_idx, 'x')
                done = True
                f.write(content)
                f.close()
            except fs.errors.FileExists as e:
                num_fails += 1
                if num_fails >= self.num_fails_to_tolerate:
                    raise CouldntObtainFileHandle(content)


class AbsolutelyClassAirlines(object):

    def __init__(self, directory, client, file_sys):
        self.directory = directory
        self.client = client
        self.file_sys = file_sys
        self.path = os.path.join(directory, client)

    def store_chat(self, chat):
        content = SavageRentals.format_transcript(chat)
        content = content + "\nThis chat took %s seconds to handle."%(chat.handle_end-chat.handle_start).seconds

        self.file_sys.write_file(content, self.path)
