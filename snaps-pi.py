if __name__ == '__main__':
    import systemd.daemon, initio, redis, RPi.GPIO as GPIO, sys

    print('Startup')
    r = redis.Redis(host='192.168.0.1', port=6379, db=0)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('')
    print('Startup complete')
    systemd.daemon.notify('READY=1')

    try:
        for message in p.listen():
        
    except:
        p.close()
        print('Goodbye')