#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import argparse
import sys
import eccodes as ecc

from gribapi import *
gribapi.ENC = "unicode-escape"

# Synop land
SYNOP = {}

SYNOP['blockNumber'] =                             ('001001', 'wmo_block', 'WMO BLOCK NUMBER [NUMERIC]')
SYNOP['stationNumber'] =                           ('001002', 'wmo_station', 'WMO STATION NUMBER [NUMERIC]')
SYNOP['stationOrSiteName'] =                       ('001015', 'station_name', 'STATION OR SITE NAME [CCITTIA5]')
SYNOP['shipOrMobileLandStationIdentifier'] =       ('001011', 'mobile_station_name', 'SHIP OR MOBILE STATION OR SITE NAME [CCITTIA5]')
SYNOP['longStationName'] =                         ('001019', 'station_name', 'STATION OR SITE NAME [CCITTIA5]')
SYNOP['stationType'] =                             ('002001', 'type_of_station', 'TYPE OF STATION [CODE TABLE]')
SYNOP['year'] =                                    ('004001', 'obsyear', 'YEAR [A]')
SYNOP['month'] =                                   ('004002', 'obsmonth', 'MONTH [MON]')
SYNOP['day'] =                                     ('004003', 'obsday', 'DAY [D]')
SYNOP['hour'] =                                    ('004004', 'obshour', 'HOUR [H]')
SYNOP['minute'] =                                  ('004005', 'obsminute', 'MINUTE [MIN]')
SYNOP['latitude'] =                                ('005001', 'latitude', 'LATITUDE (HIGH ACCURACY) [DEG]')
SYNOP['longitude'] =                               ('006001', 'longitude', 'LONGITUDE (HIGH ACCURACY) [DEG]')
SYNOP['heightOfStation'] =                         ('007001', 'height_of_station', 'HEIGHT OF STATION [M]')
SYNOP['heightOfStationGroundAboveMeanSeaLevel'] =  ('007030', 'height_of_station', 'HEIGHT OF STATION GROUND ABOVE MEAN SEA LEVEL [M]')
#SYNOP['heightOfBarometerAboveMeanSeaLevel'] =      ('007031', 'height_of_barometer', 'HEIGHT OF BAROMETER ABOVE MEAN SEA LEVEL [M]')
SYNOP['nonCoordinatePressure'] =                   ('010004', 'P0', 'PRESSURE [PA]')
SYNOP['nonCoordinateGeopotentialHeight'] =         ('010009', 'GPH', 'GEOPOTENTIAL HEIGHT [GPM]')
SYNOP['pressureReducedToMeanSeaLevel'] =           ('010051', 'PSEA', 'PRESSURE REDUCED TO MEAN SEA LEVEL [PA]')
SYNOP['3HourPressureChange'] =                     ('010061', 'PPP', '3-HOUR PRESSURE CHANGE [PA]')
SYNOP['characteristicOfPressureTendency'] =        ('010063', 'Pa', 'CHARACTERISTIC OF PRESSURE TENDENCY [CODE TABLE]')
SYNOP['windDirection'] =                           ('011001', 'WD', 'WIND DIRECTION [DEGREETRUE]')
SYNOP['windSpeed'] =                               ('011002', 'WS', 'WIND SPEED [M/S]')
SYNOP['windDirectionAt10M'] =                      ('011011', 'WD', 'WIND DIRECTION AT 10 M [DEG]')
SYNOP['windSpeedAt10M'] =                          ('011012', 'WS', 'WIND SPEED AT 10 M [M/S]')
SYNOP['airTemperature'] =                          ('012001', 'TA', 'DRY BULB TEMPERATURE [K]')
SYNOP['dewpointTemperature'] =                     ('012003', 'TD', 'DEW POINT TEMPERATURE [K]')
SYNOP['airTemperatureAt2M'] =                      ('012004', 'TA', 'DRY BULB TEMPERATURE AT 2M [K]')
SYNOP['dewpointTemperatureAt2M'] =                 ('012006', 'TD', 'DEW POINT TEMPERATURE AT 2M [K]')
SYNOP['airTemperature'] =                          ('012101', 'TA', 'TEMPERATURE/AIR TEMPERATURE [K]')
SYNOP['dewpointTemperature'] =                     ('012103', 'TD', 'DEWPOINT TEMPERATURE [K]')
SYNOP['relativeHumidity'] =                        ('013003', 'RH', 'RELATIVE HUMIDITY [%]')
SYNOP['horizontalVisibility'] =                    ('020001', 'VV', 'HORIZONTAL VISIBILITY [M]')
SYNOP['verticalVisibility'] =                      ('020002', 'VEV', 'VERTICAL VISIBILITY [M]')
SYNOP['presentWeather'] =                          ('020003', 'WW', 'PRESENT WEATHER [CODE TABLE]')
SYNOP['pastWeather1'] =                            ('020004', 'W1', 'PAST WEATHER (1) [CODE TABLE]')
SYNOP['pastWeather2'] =                            ('020005', 'W2', 'PAST WEATHER (2) [CODE TABLE]')
SYNOP['cloudCoverTotal'] =                         ('020010', 'NH', 'CLOUD COVER (TOTAL) [%]')
SYNOP['verticalSignificanceSurfaceObservations'] = ('008002', 'vertical_significance', 'VERTICAL SIGNIFICANCE (SURFACE OBSERVATIONS) [CODE TABLE]')
SYNOP['cloudAmount'] =                             ('020011', 'CN', 'CLOUD AMOUNT [CODE TABLE]')
SYNOP['heightOfBaseOfCloud'] =                     ('020013', 'CH', 'HEIGHT OF BASE OF CLOUD [M]')
SYNOP['cloudType'] =                               ('020012', 'CT', 'CLOUD TYPE [CODE TABLE]')
SYNOP['totalPrecipitationOrTotalWaterEquivalent'] =('013011', 'PR', 'TOTAL PRECIPITATION/TOTAL WATER EQUIVALENT [KGM-2]')
SYNOP['totalPrecipitationPast1Hour'] =             ('013019', 'PR_1H', 'TOTAL PRECIPITATION PAST 1 HOUR [KGM-2]')
SYNOP['totalPrecipitationPast3Hours'] =            ('013020', 'PR_3H', 'TOTAL PRECIPITATION PAST 3 HOURS [KGM-2]')
SYNOP['totalPrecipitationPast6Hours'] =            ('013021', 'PR_6H', 'TOTAL PRECIPITATION PAST 6 HOURS [KGM-2]')
SYNOP['totalPrecipitationPast12Hours'] =           ('013022', 'PR_12H', 'TOTAL PRECIPITATION PAST 12 HOURS [KGM-2]')
SYNOP['totalPrecipitationPast24Hours'] =           ('013023', 'PR_24H', 'TOTAL PRECIPITATION PAST 24 HOURS [KGM-2]')
SYNOP['totalSnowDepth'] =                          ('013013', 'SD', 'TOTAL SNOW DEPTH [M]')
SYNOP['groundMinimumTemperaturePast12Hours'] =     ('012013', 'TGINST', 'GROUND MINIMUM TEMPERATURE, PAST 12 HOURS [K]')
SYNOP['groundMinimumTemperaturePast12Hours'] =     ('012113', 'TG', 'GROUND MINIMUM TEMPERATURE, PAST 12 HOURS [K]')
SYNOP['maximumTemperatureAtHeightAndOverPeriodSpecified'] =       ('012011', 'TAMAX', 'MAXIMUM TEMPERATURE AT 2M [K]')
SYNOP['minimumTemperatureAtHeightAndOverPeriodSpecified'] =       ('012012', 'TAMIN', 'MINIMUM TEMPERATURE AT 2M [K]')
SYNOP['maximumTemperatureAtHeightAndOverPeriodSpecified'] =       ('012111', 'TAMAX', 'MAXIMUM TEMPERATURE, AT HEIGHT AND OVER PERIOD SPECIFIED [K]')
SYNOP['minimumTemperatureAtHeightAndOverPeriodSpecified'] =       ('012112', 'TAMIN', 'MINIMUM TEMPERATURE, AT HEIGHT AND OVER PERIOD SPECIFIED [K]')
SYNOP['maximumTemperatureAt2MPast12Hours'] =       ('012014', 'TAMAX12H', 'MAXIMUM TEMPERATURE AT 2M, PAST 12 HOURS [K]')
SYNOP['minimumTemperatureAt2MPast12Hours'] =       ('012015', 'TAMIN12H', 'MINIMUM TEMPERATURE AT 2M, PAST 12 HOURS [K]')
SYNOP['maximumTemperatureAt2MPast24Hours'] =       ('012016', 'TAMAX24H', 'MAXIMUM TEMPERATURE AT 2M, PAST 24 HOURS [K]')
SYNOP['minimumTemperatureAt2MPast24Hours'] =       ('012017', 'TAMIN24H', 'MINIMUM TEMPERATURE AT 2M, PAST 24 HOURS [K]')
SYNOP['evapotranspiration'] =                      ('013031', 'EVAPOTRANSPIRATION', 'EVAPOTRANSPIRATION')
SYNOP['netRadiationIntegratedOver24Hours'] =       ('014015', 'NET', 'NET RADIATION INTEGRATED OVER 24HOURS')
SYNOP['totalSunshine'] =                           ('014031', 'SUNDUR', 'TOTAL SUNSHINE [MIN]')
SYNOP['stateOfGround'] =                           ('020062', 'E', 'STATE OF THE GROUND (WITH OR WITHOUT SNOW) [CODE TABLE]')
SYNOP['specialPhenomena'] =                        ('020063', 'SPECHEN', 'SPECIAL PHENOMENA')
SYNOP['maximumWindGustSpeed'] =                    ('011041', 'WG', 'MAXIMUM WIND GUST SPEED [M/S]')
#SYNOP['maximumWindGustDirection'] =                ('011043', 'WGD', 'MAXIMUM WIND GUST DIRECTION [DEG]')
#SYNOP['dataPresentIndicator'] =                    ('031031', '???', 'DATA PRESENT INDICATOR')
SYNOP['centre'] =                                  ('001031', '???', 'IDENTIFICATION OF ORIGINATING/GENERATING CENTRE')
SYNOP['generatingApplication'] =                   ('001032', '???', 'GENERATING APPLICATION')
#SYNOP['percentConfidence'] =                       ('033007', '???', '% CONFIDENCE')
#SYNOP['timePeriod'] =                              ('004024', 'hour', 'TIME PERIOD OR DISPLACEMENT [H]')
SYNOP['timePeriod'] =                              ('004025', 'timeperiod', 'TIME PERIOD OR DISPLACEMENT')

HEADERKEYS = (
    'edition',
    'masterTableNumber',
    'updateSequenceNumber',
    'dataCategory',
    'dataSubCategory',
    'internationalDataSubCategory',
    'bufrHeaderCentre',
    'bufrHeaderSubCentre',
    'masterTablesVersionNumber',
    'localTablesVersionNumber',
    'numberOfSubsets',
    'typicalYear',
    'typicalMonth',
    'typicalDay',
    'typicalHour',
    'typicalMinute',
    'typicalSecond',
    'typicalDate',
    'typicalTime',
    'numberOfSubsets',
    'observedData',
    'compressedData',
    'unexpandedDescriptors',
    )

DEBUG = False

def read_bufr_message(bufr_file):
    """
        Read the mess
    """
    with open(bufr_file, 'rb') as fp:
        while True:
            try:
                gid = ecc.codes_bufr_new_from_file(fp)
                if gid is None:
                    return
                yield gid
            except ecc.CodesInternalError as err:
                sys.stderr.write("Error reading BUFR: \n")
                sys.stderr.write(err.msg + '\n')


def decode(file):
    """
        Let's do this!
    """
    ibufr = ""
    for msg, ibufr in enumerate(read_bufr_message(file)):

        if args.header:
            print(f"***Message {msg+1}")
            print_header(ibufr)
            continue

        subsets_in_bufr = get_value(ibufr, "numberOfSubsets")

        compressed = False
        if get_value(ibufr, "compressedData") == 1:
            compressed = True

        ecc.codes_set(ibufr, 'unpack', 1)
        print(f"\nMessage {msg+1}")

        if compressed:
            do_compressed(ibufr, subsets_in_bufr)
        else: # the most common case
            do_uncompressed(ibufr, subsets_in_bufr)
 
    if not ibufr:
        print(f"Failed to read bufr from: {file}")
        sys.exit(0)
    else:
        ecc.codes_release(ibufr)


def print_header(ibufr):
    """
        Print header keys
    """
    for k in HEADERKEYS:
        print(f"#{k}--> {get_value(ibufr, k, array=True)}")


def get_parameter_description(key):
    """
        Get correct parameter description for output
    """
    return SYNOP[key][2]


def get_descriptor(ibufr, key, silent=True):
    """
        Get the actual descriptor value. Needed in timeperiods.
    """
    try:
        val = ecc.codes_get(ibufr, key + '->code')
    except ecc.CodesInternalError as err:
        if not silent:
            print(f'WARN: failed codes_get {key} , err: {err}')
        return None

    return val


def do_uncompressed(ibufr, subsets_in_bufr):
    """
        Uncompressed aka. "normal" BUFR handling. Just fetch
        the key and its value.
    """
    subset_cnt = 1
    iterid = ecc.codes_bufr_keys_iterator_new(ibufr)
    while ecc.codes_bufr_keys_iterator_next(iterid):
        key = ecc.codes_bufr_keys_iterator_get_name(iterid)

        if key in HEADERKEYS:
            continue

        val = get_value(ibufr, key)
        descr = get_descriptor(ibufr, key)
        if val is None:
            val = "missing"
            continue
        key = strip_key(key)
        # I <3 BUFR. No 'subsetNumber' -key in wigos BUFRS.
        #if key == "subsetNumber" or key == "wigosIdentifierSeries":
        if key in ("subsetNumber", "wigosIdentifierSeries"):
            number = subset_cnt if subsets_in_bufr != 1 else 1
            print(f"\nSubset {number}\n")
            subset_cnt += 1
            key_idx = 0
            continue

        if key not in SYNOP:
            if DEBUG:
                print("Missing definition of {}".format(key), file=sys.stderr)
            continue

        key_idx += 1
        text = get_parameter_description(key)
        print_bufr(key_idx, descr, val, text)

    ecc.codes_bufr_keys_iterator_delete(iterid)


def do_compressed(ibufr, subsets):
    """
        Compressed BUFR is a bit different, hence the separate handling:
        When the BUFR data is compressed _most_ of the elements(keys) in the
        data section is an array with size of numberOfSubsets.
        Therefore, a single subset can be accessed as an element of the array.
    """
    for msg in range(subsets):
        key_idx = 0
        print(f"\nSubset {msg+1}\n")
        iterid = ecc.codes_bufr_keys_iterator_new(ibufr)
        while ecc.codes_bufr_keys_iterator_next(iterid):
            key = ecc.codes_bufr_keys_iterator_get_name(iterid)

            if key in HEADERKEYS:
                continue

            val = get_value(ibufr, key, array=True)
            descr = get_descriptor(ibufr, key)
            if val is None:
                val = "missing"
                continue
            key = strip_key(key)

            if key not in SYNOP:
                continue
            #print(type(val))
            val = val[0] if len(val) == 1 else val[msg]
            # Strip station names
            if isinstance(val, str):
                val = val.strip()
            key_idx += 1
            text = get_parameter_description(key)
            print_bufr(key_idx, descr, val, text)

        ecc.codes_bufr_keys_iterator_delete(iterid)


def print_bufr(key_idx, descr, val, text):
    """
        Separate print method
    """
    if val == ecc.CODES_MISSING_LONG or val == ecc.CODES_MISSING_DOUBLE:
        val = 'missing'
    if isinstance(val, float):
        val = f"{val:.2f}"
    print(f'{key_idx:>6}  {descr:<8} {val:>29}  {text:<60}')


def get_value(ibufr, key, array=False, silent=True):
    """
        Wrapper for codes_get
    """
    if DEBUG:
        silent = False
    try:
        if array:
            val = ecc.codes_get_array(ibufr, key)
        else:
            val = ecc.codes_get(ibufr, key)
        return val
    except ecc.CodesInternalError as err:
        if not silent:
            print(f'WARN: failed codes_get {key} , err: {err}')
        return None
    except UnicodeDecodeError as err:
        if not silent:
            print(f'WARN: Unicode error with {key} , err: {err}')
        return None


def strip_key(k):
    """
        Strip possible hashtags from eccodes keys and return only the key name, example input: #4#blockNumber
    """
    #print("key: {}".format(k))
    value = k.split("#")
    retval = k if len(value) < 3 else value[2]
    return retval


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='BUFR file to decode')
    parser.add_argument('-d', '--header', help='Print the header info', default=False, action='store_true')

    args = parser.parse_args()

    if not args.file:
        print('--file option not specified')
        sys.exit(1)
    else:
        decode(args.file)
