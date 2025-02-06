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
        return [speaker["color"] for speaker in self.speakers.values()]

    def labels(self):
        return [[name, speaker["party"]] for name, speaker in self.speakers.items()]

    def names(self):
        return list(self.speakers.keys())

    def times_total(self):
        return [self.speaker_total(speaker["times"]) for speaker in self.speakers.values()]

    def times(self):
        ret = []
        for name, speaker in self.speakers.items():
            for period in speaker["times"]:
                if len(period) == 2:

                    t1 = datetime.datetime.fromtimestamp(period[0], datetime.UTC).strftime('%H:%M:%S')
                    t2 = datetime.datetime.fromtimestamp(period[1], datetime.UTC).strftime('%H:%M:%S')
                    dur = datetime.datetime.fromtimestamp(period[1] - period[0], datetime.UTC).strftime('%H:%M:%S')
                    identifier = [name, period[0]]
                    ret.append([name, t1, t2, dur, identifier])
                else:
                    t1 = datetime.datetime.fromtimestamp(period[0], datetime.UTC).strftime('%H:%M:%S')

                    dur = datetime.datetime.fromtimestamp(int(time.time()) - period[0], datetime.UTC).strftime(
                        '%H:%M:%S')
                    identifier = False
                    ret.append([name, t1, "now", dur, identifier])

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

    def delete(self, identifier):
        if identifier == "all":
            for name in self.speakers.keys():
                self.speakers[name]["times"] = []
        elif len(identifier) == 1:
            self.speakers[identifier[0]]["times"] = []
        elif len(identifier) == 2:
            for t in self.speakers[identifier[0]]["times"]:
                if t[0] == identifier[1]:
                    if len(t) == 2:
                        rem = t
                    break
            self.speakers[identifier[0]]["times"].remove(rem)
