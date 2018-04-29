import nsq
from emial_check import send_email

buf = []

def email_message(message):
    try:
        global buf
        message.enable_async()
        # cache the message for later processing
        buf.append(message)
        if len(buf) >= 3:
            for msg in buf:

                args = msg['keys']
                func = eval(msg['func'])
                func(*args)
                # print msg
                # msg.finish()
            buf = []
        else:
            print 'deferring processing'
    except Exception, e:
        raise e

r = nsq.Reader(message_handler=email_message,
                       lookupd_http_addresses=['http://127.0.0.1:4161'],
                       topic='log', channel='async', max_in_flight=9)

nsq.run()