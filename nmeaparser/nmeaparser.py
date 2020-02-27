"""
$ python nmeaparser.py --help
Usage: nmeaparser.py (options) [NMEA file]

Options:
-h, --help show this help message and exit
-d, --debug debug mode
-v, --verify verify mode
-m MODE, --mode=MODE specify MODE 0=signle color, 1=satellite, 2=colorful
-s TIME, --start=TIME
specify start TIME as 'hh:mm:ss' (default: no start
time)
-e TIME, --end=TIME specify end TIME as 'hh:mm:ss' (default: no end time)

From:
https://gist.github.com/tako2/cec19532691cda62a2f2df047e0029e4
"""

#!/usr/bin/env python
# coding: UTF-8

import sys
import StringIO

###############################################################################
class NMEAParser:
    # -------------------------------------------------------------------------
    def __init__(self):
        '''Initialize'''

    # -------------------------------------------------------------------------
    def trans_time(self, nmea_time):
        if nmea_time == '':
            return '00:00:00'
        return '%s:%s:%s' % (nmea_time[0:2], nmea_time[2:4], nmea_time[4:6])

    # -------------------------------------------------------------------------
    def trans_date(self, nmea_date):
        if nmea_date == '':
            return 'no date'
        return '20%s-%s-%s' % (nmea_date[4:6], nmea_date[2:4], nmea_date[0:2])

    # -------------------------------------------------------------------------
    def calc_lat(self, nmea_lat, nmea_dir):
        if nmea_lat == '':
            return 0.0
        gps_lat = float(nmea_lat[0:2])
        gps_lat += float(nmea_lat[2:9]) / 60.0
        return gps_lat

    # -------------------------------------------------------------------------
    def calc_lng(self, nmea_lng, nmea_dir):
        if nmea_lng == '':
            return 0.0
        gps_lng = float(nmea_lng[0:3])
        gps_lng += float(nmea_lng[3:10]) / 60.0
        return gps_lng

    # -------------------------------------------------------------------------
    def calc_alt(self, nmea_alt, nmea_alt_unit, wgs84, wgs84_unit):
        if nmea_alt == '':
            return 0.0
        gps_alt = float(nmea_alt)
        return gps_alt

    # -------------------------------------------------------------------------
    def calc_speed(self, nmea_knot):
        if nmea_knot == '':
            return 0.0
        # 1 knot = 0.5144 m/s
        return 0.5144 * float(nmea_knot)

    # -------------------------------------------------------------------------
    def parse(self, fp, stime, etime):
        gps_list = []
        gps_valid = 0

        for line in fp:
            if line[0] == '$':
                if line[1:6] == 'GPGGA':
                    # -------------------------------------- parse GGA data ---
                    try:
                        tag,time,lat,lat_d,lng,lng_d,gps_type,nr_sat,dop,alt,alt_m,wgs84,wgs84_m,dgps_sec,dgps_id = line.split(',')
                    except:
                        print "failed to parse GPGGA"
                        gps_data = None
                        continue

                    if gps_type != '0':
                        gps_data = {'type':int(gps_type), 'time':self.trans_time(time), 'lat':self.calc_lat(lat, lat_d), 'lng':self.calc_lng(lng, lng_d), 'alt':self.calc_alt(alt, alt_m, wgs84, wgs84_m)}
                        gps_data['satellite'] = int(nr_sat)
                        gps_data['dop'] = float(dop)
                        gps_valid = 1
                    else:
                        gps_data = {'type':int(gps_type), 'time':self.trans_time(time)}
                        gps_data['lng'] = 0.0
                        gps_data['lat'] = 0.0
                        gps_data['alt'] = 0.0
                        gps_data['satellite'] = 0
                        gps_data['dop'] = 100.0
                        gps_valid = 0

                    #TODO: Delete?
                    gps_list.append(gps_data)
                elif line[1:6] == 'GPRMC':
                    # -------------------------------------- parse RMC data ---
                    try:
                        tag,time,valid,lat,lat_d,lng,lng_d,knot,knot_d,date,mag,mag_d,method = line.split(',')
                    except:
                        print "failed to parse GPRMC"
                        continue
                    gps_data['date'] = self.trans_date(date)
                    gps_data['speed'] = self.calc_speed(knot)
                    gps_data['dir'] = float(knot_d)

                    if stime == '' or gps_data['time'] >= stime:
                        gps_list.append(gps_data)
                    if etime != '' and gps_data['time'] >= etime:
                        return gps_list
                elif line[1:6] == 'GPGSA':
                    '''GSA data'''
                elif line[1:6] == 'GPGSV':
                    '''GSV data'''

        return gps_list

    # -------------------------------------------------------------------------
    def parseFile(self, filename, stime, etime):
        '''Parse GPS NMEA format'''

        fp = open(filename, 'r')
        gps_list = self.parse(fp, stime, etime)
        fp.close()

        return gps_list

    # -------------------------------------------------------------------------
    def parseString(self, str):
        '''Parse GPS NMEA format'''

        fp = StringIO.StringIO(str)
        gps_list = self.parse(fp)
        fp.close()

        return gps_list

    # -------------------------------------------------------------------------
    def outputKML2(self, gps_list):
        print '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Paths</name>
    <description>This is GPS Line</description>
    <Style id="Line0">
      <LineStyle>
        <color>ccff0000</color>
        <width>4</width>
      </LineStyle>
    </Style>
    <Style id="Line1">
      <LineStyle>
        <color>ccffffff</color>
        <width>4</width>
      </LineStyle>
    </Style>'''
        first = 1
        num_paths = 0
        path_start = 0
        for data in gps_list:
            if data['type'] != 0:
                if path_start == 0:
                    path_start = 1
                    if first == 0:
                        print '%f,%f,%f' % (data['lng'], data['lat'], data['alt'])
                        print '''        </coordinates>
      </LineString>
    </Placemark>'''
                    print '''    <Placemark>
      <name>Path %d</name>
      <description></description>
      <styleUrl>#Line0</styleUrl>
      <LineString>
        <coordinates>''' % num_paths
                    num_paths += 1
            else:
                if path_start == 1:
                    path_start = 0
                    print '''        </coordinates>
      </LineString>
    </Placemark>'''
                    first = 0
                    print '''    <Placemark>
      <name>Path GPS None</name>
      <description></description>
      <styleUrl>#Line1</styleUrl>
      <LineString>
        <coordinates>'''
                    print '%f,%f,%f' % (prev['lng'], prev['lat'], prev['alt'])

            if path_start == 1:
                print '%f,%f,%f' % (data['lng'], data['lat'], data['alt'])
            prev = data

        if path_start == 1:
            path_start = 0
            print '''        </coordinates>
      </LineString>
    </Placemark>'''
        else:
            print '''        </coordinates>
      </LineString>
    </Placemark>'''

        print '''  </Document>
</kml>'''


    # -------------------------------------------------------------------------
    def get_line_no(self, data):
        if data['type'] == 0:
            line_no = 0
        elif data['dop'] < 0.9:
            line_no = 4
        elif data['dop'] < 1.0:
            line_no = 3
        elif data['dop'] < 1.1:
            line_no = 2
        else:
            line_no = 1

        return line_no

    # -------------------------------------------------------------------------
    def get_line_no_(self, data):
        if data['type'] == 0:
            line_no = 0
        elif data['satellite'] < 4:
            line_no = 1
        elif data['satellite'] < 8:
            line_no = 2
        elif data['satellite'] < 12:
            line_no = 3
        else:
            line_no = 4

        return line_no

    # -------------------------------------------------------------------------
    def outputKML_sat(self, gps_list):
        print '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Paths</name>
    <description>This is GPS Line</description>'''

        colors = [ 'ccffffff',
                   'cc0000ff',  # red
                   'cc00ffff',  # yellow
                   'cc00ff00',  # green
                   'ccffff00' ] # cyan
        idx = 0
        for color in colors:
            print '''    <Style id="Line%d">
      <LineStyle>
        <color>%s</color>
        <width>4</width>
      </LineStyle>
    </Style>''' % (idx, color)
            idx += 1

        skip_first = 1
        path_start = 0
        num_paths = 0
        prev_line_no = -1
        prev = None
        for data in gps_list:
            if skip_first == 1:
                if data['type'] == 0:
                    continue
                skip_first = 0

            # -----------------------------------------------------------------
            line_no = self.get_line_no(data)

            # -----------------------------------------------------------------
            if line_no != prev_line_no:
                if line_no > 0 and prev_line_no >= 0:
                    print '%f,%f,%f' % (data['lng'], data['lat'], data['alt']),
                    print '<!-- %s, %.2f m/s, %d -->' % (data['time'], data['speed'], int(data['dir']))
                    print '''        </coordinates>
      </LineString>
    </Placemark>'''
                elif line_no == 0:
                    print '''        </coordinates>
      </LineString>
    </Placemark>'''

                print '''    <Placemark>
      <name>Path %d</name>
      <description></description>
      <styleUrl>#Line%d</styleUrl>
      <LineString>
        <coordinates>''' % (num_paths, line_no)

                if line_no == 0:
                    print '%f,%f,%f' % (prev['lng'], prev['lat'], prev['alt']),
                    print '<!-- %s, %.2f m/s, %d -->' % (prev['time'], prev['speed'], int(prev['dir']))

                prev_line_no = line_no

            # -----------------------------------------------------------------
            if data['type'] != 0:
                print '%f,%f,%f' % (data['lng'], data['lat'], data['alt']),
                print '<!-- %s, %.2f m/s, %d -->' % (data['time'], data['speed'], int(data['dir']))
                prev = data

        if prev_line_no > 0 or prev is not None:
            print '''        </coordinates>
      </LineString>
    </Placemark>'''
        print '''  </Document>
</kml>'''


    # -------------------------------------------------------------------------
    def outputKML(self, gps_list):
        num_paths = 0
        path_start = 0
        for data in gps_list:
            if data['type'] != 0:
                if path_start == 0:
                    path_start = 1
                    num_paths += 1
            else:
                if path_start == 1:
                    path_start = 0

        print '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Paths</name>
    <description>This is GPS Line</description>'''

        color = [ 'ccff0000', 'cc0000ff', 'ccff00ff',
                  'cc00ff00', 'ccffff00', 'cc00ffff', 'ccffffff' ]
        for i in range(num_paths):
            print '''    <Style id="Line%d">
      <LineStyle>
        <color>%s</color>
        <width>4</width>
      </LineStyle>
    </Style>''' % (i, color[i % 6])

        print '''    <Style id="LineNo">
      <LineStyle>
        <color>ccffffff</color>
        <width>4</width>
      </LineStyle>
    </Style>'''

        first = 1
        num_paths = 0
        path_start = 0
        prev = None
        for data in gps_list:
            if options.etime != '' and data['time'] >= options.etime:
                #print data['time']
                break

            if data['type'] != 0:
                if path_start == 0:
                    path_start = 1
                    if first == 0:
                        print '%f,%f,%f' % (data['lng'], data['lat'], data['alt']),
                        print '<!-- %s, %.2f m/s, %d -->' % (data['time'], data['speed'], int(data['dir']))
                        print '''        </coordinates>
      </LineString>
    </Placemark>'''
                    print '''    <Placemark>
      <name>Path %d</name>
      <description></description>
      <styleUrl>#Line%d</styleUrl>
      <LineString>
        <coordinates>''' % (num_paths, num_paths)
                    num_paths += 1
            else:
                if path_start == 1:
                    path_start = 0
                    print '''        </coordinates>
      </LineString>
    </Placemark>'''
                    first = 0
                    print '''    <Placemark>
      <name>Path GPS None</name>
      <description></description>
      <styleUrl>#LineNo</styleUrl>
      <LineString>
        <coordinates>'''
                    print '%f,%f,%f' % (prev['lng'], prev['lat'], prev['alt'])

            if path_start == 1:
                if prev is None or data['lng'] != prev['lng'] or data['lat'] != prev['lat']:
                    print '%f,%f,%f' % (data['lng'], data['lat'], data['alt']),
                    print '<!-- %s, %.2f m/s, %d -->' % (data['time'], data['speed'], int(data['dir']))
            prev = data

        if path_start == 1:
            path_start = 0
            print '''        </coordinates>
      </LineString>
    </Placemark>'''
        else:
            print '''        </coordinates>
      </LineString>
    </Placemark>'''

        print '''  </Document>
</kml>'''

    # -------------------------------------------------------------------------
    def outputDebug(self, gps_list):
        output = ''
        for data in gps_list:
            # output += '%sT%sZ' % (data['date'], data['time'])
            output += '%sZ' % (data['time'])
            if data['type'] != 0:
                output += ' (%f, %f, %f)\n' % (data['lng'], data['lat'], data['alt'])
            else:
                output += '\n'
            output += '  speed=%fm/s, dir=%f\n' % (data['speed'], data['dir'])

        return output

###############################################################################
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser('usage: %prog (options) [NMEA file]')
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="debug mode")
    parser.add_option("-v", "--verify",
                      action="store_true", dest="verify", default=False,
                      help="verify mode")
    parser.add_option("-m", "--mode", type="int", dest="mode", default=0,
                      metavar="MODE",
                      help="specify MODE 0=signle color, 1=satellite, 2=colorful")
    parser.add_option("-s", "--start", type="string",
                      dest="stime", default="",
                      metavar="TIME",
                      help="specify start TIME as 'hh:mm:ss' (default: no start time)")
    parser.add_option("-e", "--end", type="string",
                      dest="etime", default="",
                      metavar="TIME",
                      help="specify end TIME as 'hh:mm:ss' (default: no end time)")

    (options, args) = parser.parse_args()

    #argvs = sys.argv
    #argc = len(argvs)

    if (len(args) != 1):
        parser.error("need to specify NMEA file")
        quit()

    nmea_parser = NMEAParser()
    gps_list = nmea_parser.parseFile(args[0], options.stime, options.etime)

    if options.verify is True:
        print "start time = %s" % gps_list[0]['time']
        print "end time = %s" % gps_list[-1]['time']
        quit()

    if options.debug is False:
        if options.mode == 0:
            nmea_parser.outputKML2(gps_list)
        elif options.mode == 1:
            nmea_parser.outputKML_sat(gps_list)
        else:
            nmea_parser.outputKML(gps_list)
    else:
        print nmea_parser.outputDebug(gps_list)