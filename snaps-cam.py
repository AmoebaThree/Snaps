if __name__ == '__main__':
    import systemd.daemon
    import redis
    import os

    print('Startup')

    root_dir = '~/snaps/cam/'
    os.makedirs(root_dir, exist_ok=True)

    r = redis.Redis(host='192.168.0.1', port=6379, db=0)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('snaps.pi')

    print('Startup complete')
    systemd.daemon.notify('READY=1')

    try:
        for message in p.listen():
            filename = message['data']
            os.system(
                'fswebcam --device v4l2:/dev/video0 --input 0 --no-banner --resolution 640x360 ' + root_dir + filename + '.jpg')
            p.publish('snaps.cam.capture', filename)
    except:
        p.close()
        print('Goodbye')
