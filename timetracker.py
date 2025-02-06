import datetime
import time


class TimeTracker:
    def __init__(self, speakers):
        self.speakers = {
            speaker["name"]:
                {"party": speaker["party"],
                 "color": speaker["color"],
                 "times": []
                 }
            for speaker in speakers
        }

    @staticmethod
    def speaker_total(speaker_times):
        total = 0
        for period in speaker_times:
            if len(period) == 2:
                total += period[1] - period[0]
            else:
                total += int(time.time()) - period[0]
        return total

    def colors(self):
        return [speaker["color"] for _, speaker in self.speakers.items()]

    def names(self):
        return [[name, speaker["party"]] for name, speaker in self.speakers.items()]

    def times_total(self):
        return [self.speaker_total(speaker["times"]) for _, speaker in self.speakers.items()]

    def times(self):
        # return [(speaker["times"]) for _, speaker in self.speakers.items()]
        ret = []
        for name, speaker in self.speakers.items():
            for period in speaker["times"]:
                if len(period) == 2:

                    t1 = datetime.datetime.fromtimestamp(period[0], datetime.UTC).strftime('%H:%M:%S')
                    t2 = datetime.datetime.fromtimestamp(period[1], datetime.UTC).strftime('%H:%M:%S')
                    dur = datetime.datetime.fromtimestamp(period[1] - period[0], datetime.UTC).strftime('%H:%M:%S')
                    ret.append([name, t1, t2, dur])
                else:
                    t1 = datetime.datetime.fromtimestamp(period[0], datetime.UTC).strftime('%H:%M:%S')

                    dur = datetime.datetime.fromtimestamp(int(time.time()) - period[0], datetime.UTC).strftime(
                        '%H:%M:%S')
                    ret.append([name, t1, "now", dur])

        return sorted(ret, key=lambda entry: entry[1])

    def active(self):
        return [len(speaker["times"]) != 0 and len(speaker["times"][-1]) == 1 for _, speaker in self.speakers.items()]

    def start(self, name):
        if self.speakers[name]["times"]:
            if len(self.speakers[name]["times"][-1]) == 1:
                # don't start if not empty and already running
                return False

        self.speakers[name]["times"].append([int(time.time())])
        return True

    def stop(self, name):
        if not self.speakers[name]["times"]:
            # don't stop if empty
            return False
        if len(self.speakers[name]["times"][-1]) == 2:
            # don't stop if not running
            return False

        self.speakers[name]["times"][-1].append(int(time.time()))
        return True
