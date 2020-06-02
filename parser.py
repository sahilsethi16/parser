import re
import datetime
from collections import Counter


def cal_uniq_ip(logfile):
    myregex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    with open(logfile) as f:
        log = f.read()
        my_iplist = re.findall(myregex, log)
        ipcount = Counter(my_iplist)
        return str(len(ipcount))


def apache_log_reader(logfile):
    regex1 = re.compile(
        r"(?P<ip>.*?) (?P<remote_log_name>.*?) (?P<userid>.*?) \[(?P<date>.*?)(?= ) (?P<timezone>.*?)\] \"(?P<request_method>.*?) (?P<path>.*?)(?P<request_version> HTTP/.*)?\" (?P<status>.*?) (?P<length>.*?) \"(?P<referrer>.*?)\" \"(?P<user_agent>.*?)\" ")

    uniqueVisitors = cal_uniq_ip(logfile)
    with open(logfile, "r") as in_file:

        counter = 0
        avg = 0
        total = 0
        tot = 0
        requestcounter = 0
        unsuccessfulcounter = 0
        rpm = []
        currentminute = 0
        for line in in_file:
            total += 1
            match = re.search(regex1, line)
            if match:
                s = match.group("date")
                d = datetime.datetime.strptime(s, "%d/%b/%Y:%H:%M:%S")
                newminute = d.minute

                if currentminute == 0:
                    currentminute = d.minute

                if currentminute != newminute:
                    rpm.append(requestcounter + 1)
                    requestcounter = 0
                    currentminute = newminute
                else:
                    requestcounter += 1

                avg += int(match.group("length"))
                if match.group("status") != "200" or match.group("status") != "204":
                    counter += 1
                else:
                    unsuccessfulcounter += 1
                    print(match.group("status"))

                if match.group("referrer").find("http") == -1:
                    tot += 1

        sum = 0
        for i in range(0, len(rpm)):
            sum = sum + rpm[i];
        avgrpm = sum / len(rpm)
        avg = avg / total
        print("No of HTTP request made: ", tot)
        print("No of successful requests: ", counter)
        print("No of unsuccessful requests: ", unsuccessfulcounter)
        print("No. of unique visitors : ", uniqueVisitors)
        print("average bandwidth: ", avg)
        print("Average Requests per minute: ", avgrpm)


# Entry Point
if __name__ == '__main__':
    apache_log_reader("sample.log")
