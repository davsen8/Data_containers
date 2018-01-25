
# Note that the [("A","value"),("B","value2"),...]  notation is used rather than the {"A":"value","B":"value2",.. }
# when assigning to the ordered dictionary since the later builds a 'regular' dictionary first then passes it to the
# OrderedDict, which mean that the Order IS NOT preserved, while the former passes each pair intot he ordered dict
# # one at  time preserving the ordering specified..


from collections import OrderedDict


class ODF_META():
    def __init__(self):
        pass


    # REQUIRED - SINGLE BLOCK PER FILE
    self.ODF_HEADER =  OrderedDict([
        ("FILE_SPECIFICATION", "'CTD_BCD2016666_001_01_DN'")
        ])

    # REQUIRED - SINGLE BLOCK PER FILE
    self.CRUISE_HEADER= OrderedDict ([
        ("COUNTRY_INSTITUTE_CODE", "1805"),  # CANADA  NAFC
        ("CRUISE_NUMBER", "'BCD2016666'"),
        ("ORGANIZATION", "'DFO NAFC'"),
        ("CHIEF_SCIENTIST", "'Alonzo Quilt'"),
        ("START_DATE", "'01-Jan-2016 00:00:00.00'"),
        ("END_DATE", "'31-Dec-2016 23:59:59.00'"),
        ("PLATFORM", "'PADDLE TO THE SEA'"),
        ("CRUISE_NAME", "'ARROUND THE BAY'"),
        ("CRUISE_DESCRIPTION", "'Atlantic Zone Monitoring Program (AZMP)'")
        ])

    # REQUIRED - SINGLE BLOCK PER FILE
    self.EVENT_HEADER= OrderedDict ([
        ("DATA_TYPE", "'CTD'"),
        ("EVENT_NUMBER", "'001'"),
        ("EVENT_QUALIFIER1", "'01'"),
        ("EVENT_QUALIFIER2", "'DN'"),
        ("CREATION_DATE", "'14-MAR-2017 10:48:58.19'"),
        ("ORIG_CREATION_DATE", "'11-JAN-2016 16:42:35.00'"),
        ("START_DATE_TIME", "'08-JAN-2016 14:12:09.00'"),
        ("END_DATE_TIME", "'17-NOV-1858 00:00:00.00'"),
        ("INITIAL_LATITUDE", "44.267500"),
        ("INITIAL_LONGITUDE", "-63.317500"),
        ("END_LATITUDE", "-99.900000"),
        ("END_LONGITUDE", "-999.900000"),
        ("MIN_DEPTH", "1.000000"),
        ("MAX_DEPTH", "163.500000"),
        ("SAMPLING_INTERVAL", "0.000000"),
        ("SOUNDING", "163.000000"),
        ("DEPTH_OFF_BOTTOM", "-0.500000"),
        ("EVENT_COMMENTS", list()) # repeat field !!!!!!!!!!!! so need to make a list
        ])

    # OPTIONAL - SINGLE BLOCK PER FILE
    METEO_HEADER = OrderedDict ([
        ("AIR_TEMPERATURE","-99.0"),
        ("ATMOSPHERIC_PRESURE","-9999.9"),
        ("WIND_SPEED","-99.9"),
        ("WIND_DIRECTION","-999.9"),
        ("SEA_STATE","-9"),
        ("CLOUD_COVER","-9"),
        ("ICE_THICKNESS","-99.9"),
        ("METEO_COMMENTS",list()) # repeat field !!!!!!!!!!!! so need to make a list
    ])


    # OPTIONAL - SINGLE BLOCK PER FILE
    INSTRUMENT_HEADER = OrderedDict ([
        ("INST_TYPE", "'Sea-Bird'"),
        ("MODEL", "'SBE25'"),
        ("SERIAL_NUMBER", "'258917-0116'"),
        ("DESCRIPTION", "'C:\\DFO-MPO\\Jeff-Spry\\Stn2\\2016\\CTDDATA\\16666101.hex C:\\DFO-MPO\\Jeff-Spry\\Stn2\\2016\\16666101.con'")
        ])

    # OPTIONAL - SINGLE BLOCK PER FILE
    QUALITY_HEADER = OrderedDict ([
        ("QUALITY_DATE", "'27-JAN-2017 16:38:07.61'"),
        ("QUALITY_TESTS",list()),   # repeat field !!!!!!!!!!!! so need to make a list
        ("QUALITY_COMMENTS",list()) # repeat field !!!!!!!!!!!! so need to make a list
        ])

    # OPTIONAL -  MULTIPLE BLOCKS PER FILE
    GENERAL_CAL_HEADER  = OrderedDict ([
        ("COUNT", 0),
        ("PARM", list())
        ])

    GENERAL_CAL_BLOCK = OrderedDict ([
        ("PARAMETER_CODE_TYPE","''"),
        ("CALIBRATION_TYPE","'"),
        ("CALIBRATION_DATE","''"),
        ("APPLICATION_DATE","''"),
        ("COEFFICIENTS","''"),
        ("CALIBRATION_EQUATION","''"),
        ("CALIBRATION_COMMENTS","''")
    ])

    # OPTIONAL -  MULTIPLE BLOCKS PER FILE
    POLYNOMIAL_CAL_HEADER  = OrderedDict ([
        ("COUNT", 0),
        ("PARM", list())
        ])

    POLYNOMIAL_CAL_BLOCK = OrderedDict ([
        ("PARAMETER_CODE","''"),
        ("CALIBRATION_DATE","''"),
        ("APPLICATION_DATE","''"),
        ("NUMBER_OF_COEFFICIENTS","-99")
        ("COEFFICIENTS","''"),
    ])

    # OPTIONAL -  MULTIPLE BLOCKS PER FILE
    COMPASS_CAL_HEADER  = OrderedDict ([
        ("COUNT", 0),
        ("PARM", list())
        ])

    COMPASS_CAL_BLOCK = OrderedDict ([
        ("PARAMETER_CODE","''"),
        ("CALIBRATION_DATE","''"),
        ("APPLICATION_DATE","''"),
        ("DIRECTIONS",list()),        # 4 values per line
        ("CORRECTIONS",list()),       # 4 values per line
    ])

    # OPTIONAL -  MULTIPLE BLOCKS PER FILE
    HISTORY_HEADER = OrderedDict ([
        ("COUNT",0),
        ( "HIST" , list ())
        ])

    HISTORY_BLOCK = OrderedDict ([
        ("CREATION_DATE,'06-FEB-2017 12:14:57.99'"),
        ("PROCESS",list())
    ])

#        HISTORY_HEADER[0] = OrderedDict ([
#               ("CREATION_DATE,'06-FEB-2017 12:14:57.99'"),
#                "PROCESS" = ['The following edits were completed by JEFF JACKSON.'"]
#                "PROCESS".append("PROCESS='Edit Record: Field \"Num_History\" has been changed from 6 to 7.'")

    # REQUIRED -  1 BLOCK PER PARAMETER
    PARAMETER_HEADER = OrderedDict([
        ("COUNT", 0),
        ("PARM", list())
        ])


    PARAMETER_BLOCK = OrderedDict ([
        ("TYPE", "'INTE'"),
        ("NAME", "'CNTR_01'"),
        ("UNITS", "'none'"),
        ("CODE", "'CNTR_01'"),
        ("NULL_VALUE", "'-99.00000000'"),
        ("PRINT_FIELD_WIDTH", "10"),
        ("PRINT_DECIMAL_PLACES", "1"),
        ("ANGLE_OF_SECTION", "0.000000"),
        ("MAGNETIC_VARIATION", "0.000000"),
        ("DEPTH", "0.000000"),
        ("MINIMUM_VALUE", "    1002.0"),
        ("MAXIMUM_VALUE", "    4706.0"),
        ("NUMBER_VALID", "326"),
        ("NUMBER_NULL", "0")
        ])

    # REQUIRED - SINGLE BLOCK PER FILE
    RECORD_HEADER = OrderedDict ([
        ("NUM_HISTORY", "9"),
        ("NUM_CYCLE", "326"),
        ("NUM_PARAM", "21")
        ])

