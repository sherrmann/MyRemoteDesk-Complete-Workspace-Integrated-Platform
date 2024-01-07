import time
import json
import sys
import mysql.connector
import datetime
from dateutil import parser

if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32gui
    import uiautomation as auto

# Establishing a connection with the Database
connectiondb = mysql.connector.connect(host="host", user="user",
                                       password="password",
                                       database="database", port=3306)
# Creating a cursor for executing the queries
cursordb = connectiondb.cursor()


class ActivityList:
    """
    A class used to create an ordered list of activities

    ...

    Attributes
    ----------
    activities : list
        a list holding the details for all the activities

    Methods
    -------
    initialize_me(self):
        Initialize the list of activities by reading from a JSON file
    get_activities_from_json(self, data):
        Get the list of activities from the supplied JSON data
    get_time_entries_from_json(self, data):
        Returns a list of time entries from the supplied JSON data
    serialize(self):
        Serializes the class instance to JSON
    activities_to_json(self):
        Converts the activities in activities list to JSON form
    """

    def __init__(self, activities):
        self.activities = activities

    def initialize_me(self):
        activity_list = ActivityList([])
        # Reading the data from 'activities.json' file
        with open('activities.json', 'r') as f:
            data = json.load(f)
            # Updating 'activity_list' with activities read from JSON file
            activity_list = ActivityList(
                activities=self.get_activities_from_json(data)
            )

        return activity_list

    # Returns activities list from JSON file
    def get_activities_from_json(self, data):
        return_list = []
        for activity in data['activities']:
            return_list.append(
                Activity(
                    name=activity['name'],
                    time_entries=self.get_time_entries_from_json(activity),
                )
            )
        self.activities = return_list
        return return_list

    # Returns time entries from JSON data
    def get_time_entries_from_json(self, data):
        return_list = []
        for entry in data['time_entries']:
            return_list.append(
                TimeEntry(
                    start_time=parser.parse(entry['start_time']),
                    end_time=parser.parse(entry['end_time']),
                    days=entry['days'],
                    hours=entry['hours'],
                    minutes=entry['minutes'],
                    seconds=entry['seconds'],
                )
            )
        self.time_entries = return_list
        return return_list

    # Serializing the 'activities' list to JSON
    def serialize(self):
        return {
            'activities': self.activities_to_json()
        }

    # Helps in Serializing 'activities' list to JSON
    def activities_to_json(self):
        activities_ = []
        for activity in self.activities:
            activities_.append(activity.serialize())

        return activities_


class Activity:
    """
    A class to represent an Activity

    ...

    Attributes
    ----------
    name : str
        the name of the activity
    time_entries : list
        a list holding the time entries for the activity

    Methods
    -------
    serialize(self):
        Serializes the class instance to JSON
    make_time_entries_to_json(self):
        Converts the time entries in the activity to JSON form
    """

    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    # Serializing 'activity' object to JSON
    def serialize(self):
        return {
            'name': self.name,
            'time_entries': self.make_time_entries_to_json()
        }

    # Helps in Serializing 'time_entries' list of an 'activity' object to JSON
    def make_time_entries_to_json(self):
        time_list = []
        for time in self.time_entries:
            time_list.append(time.serialize())

        return time_list


class TimeEntry:
    """
    A class to represent a Time Entry

    ...

    Attributes
    ----------
    start_time : datetime
        the start time of the activity
    end_time : datetime
        the end time of the activity
    days : int
        the number of days the activity lasted for
    hours : int
        the number of hours the activity lasted for
    minutes : int
        the number of minutes the activity lasted for
    seconds : int
        the number of seconds the activity lasted for

    Methods
    -------
    _get_specific_times(self):
        Calculates specific times in terms of days, hours, minutes & seconds
    serialize(self):
        Serializes the class instance to JSON
    """

    def __init__(self, start_time, end_time, days, hours, minutes, seconds):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    # Calculates specific times in terms of days, hours, minutes & seconds
    def _get_specific_times(self):
        self.days, self.seconds = self.total_time.days, self.total_time.seconds
        self.hours = self.days * 24 + self.seconds // 3600
        self.minutes = (self.seconds % 3600) // 60
        self.seconds = self.seconds % 60

    # Serializing 'time_entry' object to JSON
    def serialize(self):
        return {
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'days': self.days,
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds
        }


# Extracts the domain name from the URL
def url_to_name(url):
    string_list = url.split('/')
    return string_list[2]


# For Windows, returns active window name
def get_active_window():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name


# For Windows, gets chrome URL
def get_chrome_url():
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        return 'https://' + edit.GetValuePattern().Value
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return get_active_window()


# Display activities
def show_activity():
    b = list()
    d = list()
    try:
        with open('activities.json', 'r') as jsonfile:
            a = json.load(jsonfile)
            e = a['activities']
    except Exception:
        print("no json data")
        exit(0)

    for i in e:
        b.append(i['name'])

    tot = 0

    for i in e:
        sed = 0
        for j in i["time_entries"]:
            sed = sed + int(j["minutes"]) * 60 + int(j["seconds"]) + int(j["hours"]) * 3600
            tot = tot + sed
        d.append(sed)

    kek = time.strftime("%H:%M:%S", time.gmtime(tot))
    kek = "Time used : " + kek
    print(b)
    print(d)
    combineBD = zip(b, d)
    zipped_list = list(combineBD)

    return zipped_list


# Erases contents of 'activities.json'
def erase():
    open("activities.json", "w").close()


# Continuous monitoring and recording of activities
def record(active_window_name, activity_name, start_time, activeList, first_time, e_id, o_id):
    try:
        al = activeList.initialize_me()
    except Exception:
        print('No json')

    try:
        while True:
            previous_site = ""
            if sys.platform not in ['linux', 'linux2']:
                new_window_name = get_active_window()
                if 'Google Chrome' in new_window_name:
                    new_window_name = url_to_name(get_chrome_url())

            # If activity window changes
            if active_window_name != new_window_name:
                print(active_window_name)
                activity_name = active_window_name
                al = activity_name
                print(al)
                print(type(al))
                ct = datetime.datetime.now()
                sql = "INSERT INTO monitoring (m_title, m_log_ts, e_id_id, o_id_id) VALUES (%s, %s, %s, %s)"
                val = (al, ct, e_id, o_id)
                cursordb.execute(sql, val)
                connectiondb.commit()
                print(cursordb.rowcount, "record inserted.")

                if not first_time:
                    end_time = datetime.datetime.now()
                    time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                    time_entry._get_specific_times()

                    exists = False
                    for activity in activeList.activities:
                        if activity.name == activity_name:
                            exists = True
                            activity.time_entries.append(time_entry)

                    if not exists:
                        activity = Activity(activity_name, [time_entry])
                        activeList.activities.append(activity)
                    with open('activities.json', 'w') as json_file:
                        json.dump(activeList.serialize(), json_file,
                                  indent=4, sort_keys=True)
                        start_time = datetime.datetime.now()

                first_time = False
                active_window_name = new_window_name

            time.sleep(1)

    except KeyboardInterrupt:
        with open('activities.json', 'w') as json_file:
            json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)


# Starts recording of activities
def mainRecord(e_id, o_id):
    active_window_name = str()
    activity_name = ""
    start_time = datetime.datetime.now()
    activeList = ActivityList([])
    first_time = True
    record(active_window_name, activity_name, start_time, activeList, first_time, e_id, o_id)
