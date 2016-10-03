import requests
import re
import sys

# Fetch baby names for 2005 to 2016
year_regex = re.compile(r"<caption><b>Popularity in (\d\d\d\d)</b></caption>")

for year in range(2005, 2017):
	print("fetching data for year %s" % year)
	resp = requests.post("https://www.ssa.gov/cgi-bin/popularnames.cgi", data = {'year':year, 'top':100})

	res = year_regex.findall(resp.text)
	if not res or int(res[0]) != year:
		print("could not fetch data for year %s" % str(year))
		continue

	name_regex = re.compile(r'<tr align="right">\n\s+<td>(?P<rank>\d+)</td> <td>' \
				+ r'(?P<mname>[a-zA-Z]+)</td>\s+<td>(?P<fname>[a-zA-Z]+)</td>\n</tr>')
	l = name_regex.findall(resp.text)
	mnames = dict()
	fnames = dict()
	for t in l:
		mnames[t[1]] = t[0]
		fnames[t[2]] = t[0]

	mnames_items = mnames.items()
	mnames_items.sort(key = lambda t:t[0])
	fnames_items = fnames.items()
	fnames_items.sort(key = lambda t:t[0])
	f = open("mnames_" + str(year), "w")
	for i in mnames_items:
		f.write("%s, %s\n" % i)
	f.close()
 	f = open("fnames_" + str(year), "w")
	for i in fnames_items:
		f.write("%s, %s\n" % i)
	f.close()

