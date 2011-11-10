#!/usr/bin/env python

import smtplib, time, urllib2, os


# first to check the correctness of mobile site
def is_available(debug = False):
    for i in range(3): # check for 3 times
        req = urllib2.Request('http://bbs.uwcssa.com/forum.php')
        req.add_header('User-agent', 'iPhone')
        result = urllib2.urlopen(req).read(1024)

        if "m.uwcssa.com" in result:
            if debug:
                print "found the target string in the reply"
            else:
                return True

        time.sleep(10) # wait for 10 seconds

    return False


# if problematic try to clean all the cache files
def clear_cache(debug = False):
    ROOT_DIR = "/var/www/html/data"

    template_files = ROOT_DIR + "/template/*.tpl.php"
    if debug:
        print template_files
    else:
        os.system("rm -f " + template_files)

    cache_php_files = ROOT_DIR + "/cache/*.php"
    if debug:
        print cache_php_files
    else:
        os.system("rm -f " + cache_php_files)

    # cannot use the updatedate() function in discuz
    # so there are still a large amount of cache files uncleaned


# and try to contact webmaster
def contact_webmaster(mail_title):
    recipient_list = ["uwcssa.it@gmail.com", "fan.gao1989@gmail.com"]

    mail_content = "From: it-support@uwcssa.com\n"                            \
                 + "To: " + ", ".join(recipient_list) + "\n"                \
                 + "Subject: " + mail_title + " (" + time.ctime() + ")\n"   \
                 + "as the title\n\n" + time.ctime()

    # print mail_content

    mail_server = smtplib.SMTP('localhost')
    mail_server.sendmail("it-support@uwcssa.com", recipient_list, mail_content)
    mail_server.quit()


if __name__ == '__main__':
    lock_file = "/tmp/lock_for_cache_cleaned"
    try:
	    # logging for testing
	    # logfile = open("log.txt", "a+")
	    # logfile.write(time.ctime() + '\n')
	    # logfile.close()

        if not is_available():
            if not os.path.isfile(lock_file):
                clear_cache()
                contact_webmaster("server might be down, and cache is partially cleaned")
                os.system("touch " + lock_file)
        else:
            if os.path.isfile(lock_file):
                os.remove(lock_file)
                contact_webmaster("server is up")

    except Exception, exc:
        contact_webmaster("Failed as " + str(exc))
