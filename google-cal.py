from __future__ import print_function
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2, os, datetime, json, csv

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python'


def get_credentials():
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')
	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials


def main():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)
	dt_lower = datetime.datetime.now().isoformat() + 'Z'
	dt_upper = (datetime.datetime.now() + datetime.timedelta(hours=240)).isoformat() + 'Z'
	eventsResult = service.events().list(calendarId='primary', timeMin=dt_lower, timeMax=dt_upper, singleEvents=True, orderBy='startTime').execute()
	google_cal = eventsResult.get('items', [])

	inpfile = open('michigan_events.csv', 'r')
	fread = csv.reader(inpfile, delimiter = ',')
	mich_events = [row for row in fread if row[2] != '' and row[3] != '' and row[4] != '' and row[5] != ''][1:]
	inpfile.close()

	final_events = []
	if len(google_cal) > 0:
		for m_event in mich_events:
			m_start_dt = datetime.datetime(int(m_event[2].split('-')[0]), int(m_event[2].split('-')[1]), int(m_event[2].split('-')[2]), int(m_event[4].split(':')[0]), int(m_event[4].split(':')[1]))
			m_end_dt = datetime.datetime(int(m_event[3].split('-')[0]), int(m_event[3].split('-')[1]), int(m_event[3].split('-')[2]), int(m_event[5].split(':')[0]), int(m_event[5].split(':')[1]))
			ctr_noclash = 0
			for g_entry in google_cal:
				g_start_dt = datetime.datetime(int(g_entry['start']['dateTime'][:4]), int(g_entry['start']['dateTime'][5:7]), int(g_entry['start']['dateTime'][8:10]), int(g_entry['start']['dateTime'][11:13]), int(g_entry['start']['dateTime'][11:13]), int(g_entry['start']['dateTime'][14:16]))
				g_end_dt = datetime.datetime(int(g_entry['end']['dateTime'][:4]), int(g_entry['end']['dateTime'][5:7]), int(g_entry['end']['dateTime'][8:10]), int(g_entry['end']['dateTime'][11:13]), int(g_entry['end']['dateTime'][11:13]), int(g_entry['end']['dateTime'][14:16]))
				if (m_start_dt < g_start_dt and m_end_dt <= g_start_dt) or (m_start_dt >= g_end_dt and m_end_dt > g_end_dt):
					ctr_noclash += 1
			if ctr_noclash == len(google_cal):
				final_events.append(m_event)

	outfile = open('michigan_filtered.csv', 'w')
	fwrite = csv.writer(outfile, delimiter = ',')
	fwrite.writerow(['title', 'description', 'startdate', 'enddate', 'timestart', 'timeend', 'tags'])
	for event in final_events:
		fwrite.writerow(event)
	outfile.close()

if __name__ == '__main__':
	main()
