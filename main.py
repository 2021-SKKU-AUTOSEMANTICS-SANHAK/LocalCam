import os
import json
from receive_send import receive_send

'''
    
    Options are in arguments.json file.
    
    If you run on realtime,
    set "how_many" as "realtime".

'''


def main():
    with open('arguments.json', 'r') as f:
        args = json.load(f)
    credential_path = args['credential_path']
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    receive_send(args)


if __name__ == "__main__":
    main()
