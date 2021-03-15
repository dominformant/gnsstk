#!/usr/env python

import unittest, sys, os
sys.path.insert(0, os.path.abspath(".."))
from gpstk.test_utils import args,run_unit_tests

import gpstk

class TestNavLibrary(unittest.TestCase):
    def test_getXvt(self):
        navLib = gpstk.NavLibrary()
        ndf = gpstk.RinexNavDataFactory()
        navLib.addFactory(ndf)
        ndf.addDataSource(args.input_dir+'/arlm2000.15n')
        sat = gpstk.NavSatelliteID(5, 5, gpstk.SatelliteSystem.GPS,
                                   gpstk.CarrierBand.L1,
                                   gpstk.TrackingCode.CA, gpstk.NavType.GPSLNAV)
        ct = gpstk.CivilTime(2015,7,19,2,0,35,
                             gpstk.TimeSystem.GPS).toCommonTime()
        # test getXvt (first signature)
        xvt = gpstk.Xvt()
        rv = navLib.getXvt(sat, ct, xvt, False)
        self.assertEqual(True, rv)
        self.assertEqual(  9345531.5274733770639, xvt.x[0]);
        self.assertEqual(-12408177.088141856715,  xvt.x[1]);
        self.assertEqual( 21486320.848036296666,  xvt.x[2]);
        self.assertEqual(2081.276961058104007,    xvt.v[0]);
        self.assertEqual(1792.4445008638492709,   xvt.v[1]);
        self.assertEqual( 148.29209115082824155,  xvt.v[2]);
        self.assertEqual(-0.00021641018042870913346, xvt.clkbias);
        self.assertEqual(4.3200998334200003381e-12, xvt.clkdrift);
        self.assertEqual(-8.8197758101551758427e-09, xvt.relcorr);
        self.assertEqual(gpstk.Xvt.Healthy, xvt.health)
        # test getXvt (second signature)
        xvt2 = gpstk.Xvt()
        rv = navLib.getXvt(sat, ct, xvt2, gpstk.SVHealth.Any)
        self.assertEqual(True, rv)
        self.assertEqual(  9345531.5274733770639, xvt.x[0]);
        self.assertEqual(-12408177.088141856715,  xvt.x[1]);
        self.assertEqual( 21486320.848036296666,  xvt.x[2]);
        self.assertEqual(2081.276961058104007,    xvt.v[0]);
        self.assertEqual(1792.4445008638492709,   xvt.v[1]);
        self.assertEqual( 148.29209115082824155,  xvt.v[2]);
        self.assertEqual(-0.00021641018042870913346, xvt.clkbias);
        self.assertEqual(4.3200998334200003381e-12, xvt.clkdrift);
        self.assertEqual(-8.8197758101551758427e-09, xvt.relcorr);
        self.assertEqual(gpstk.Xvt.Healthy, xvt.health)

    def test_getHealth(self):
        navLib = gpstk.NavLibrary()
        ndf = gpstk.RinexNavDataFactory()
        navLib.addFactory(ndf)
        ndf.addDataSource(args.input_dir+'/arlm2000.15n')
        sat = gpstk.NavSatelliteID(10, 10, gpstk.SatelliteSystem.GPS,
                                   gpstk.CarrierBand.L1,
                                   gpstk.TrackingCode.CA, gpstk.NavType.GPSLNAV)
        ct = gpstk.CivilTime(2015,7,19,2,0,35,
                             gpstk.TimeSystem.GPS).toCommonTime()
        rv,health = navLib.getHealth(sat, ct, gpstk.SVHealth.Any);
        self.assertEqual(False, rv)
        ct = gpstk.CivilTime(2015,7,19,12,35,35,
                             gpstk.TimeSystem.GPS).toCommonTime()
        rv,health = navLib.getHealth(sat, ct, gpstk.SVHealth.Any);
        self.assertEqual(False, rv)
        ct = gpstk.CivilTime(2015,7,19,12,35,36,
                             gpstk.TimeSystem.GPS).toCommonTime()
        rv,health = navLib.getHealth(sat, ct, gpstk.SVHealth.Any);
        self.assertEqual(True, rv)
        self.assertEqual(gpstk.SVHealth.Unhealthy, health)
        sat = gpstk.NavSatelliteID(2, 2, gpstk.SatelliteSystem.GPS,
                                   gpstk.CarrierBand.L1,
                                   gpstk.TrackingCode.CA, gpstk.NavType.GPSLNAV)
        ct = gpstk.CivilTime(2015,7,19,2,0,0,
                             gpstk.TimeSystem.GPS).toCommonTime()
        rv,health = navLib.getHealth(sat, ct, gpstk.SVHealth.Any);
        self.assertEqual(True, rv)
        self.assertEqual(gpstk.SVHealth.Healthy, health)

    def test_getOffset(self):
        navLib = gpstk.NavLibrary()
        ndf = gpstk.RinexNavDataFactory()
        navLib.addFactory(ndf)
        ndf.addDataSource(args.input_dir+
                           '/test_input_rinex_nav_RinexNavExample.99n')
        self.assertEqual(5, ndf.size())
        ct = gpstk.GPSWeekSecond(1025, 410500).toCommonTime()
        # test getOffset with NavDataPtr
        rv,nd = navLib.getOffset(gpstk.TimeSystem.GPS, gpstk.TimeSystem.UTC, ct)
        # time range of ct is going to fail to find the time offset
        self.assertEqual(False, rv)
        ct2 = gpstk.GPSWeekSecond(1025,552970).toCommonTime()
        rv,nd = navLib.getOffset(gpstk.TimeSystem.GPS,gpstk.TimeSystem.UTC,ct2)
        self.assertEqual(True, rv)
        self.assertEqual(13.0, nd.deltatLS)

    def test_find(self):
        navLib = gpstk.NavLibrary()
        ndf = gpstk.RinexNavDataFactory()
        navLib.addFactory(ndf)
        ndf.addDataSource(args.input_dir+'/arlm2000.15n')
        sat = gpstk.NavSatelliteID(10, 10, gpstk.SatelliteSystem.GPS,
                                   gpstk.CarrierBand.L1,
                                   gpstk.TrackingCode.CA, gpstk.NavType.GPSLNAV)
        ct = gpstk.CivilTime(2015,7,19,2,0,35,
                             gpstk.TimeSystem.GPS).toCommonTime()
        nmide = gpstk.NavMessageID(sat, gpstk.NavMessageType.Ephemeris)
        nmida = gpstk.NavMessageID(sat, gpstk.NavMessageType.Almanac)
        rv,nd = navLib.find(nmide, ct, gpstk.SVHealth.Any,
                            gpstk.NavValidityType.ValidOnly,
                            gpstk.NavSearchOrder.User)
        self.assertEqual(False, rv)
        ct = gpstk.CivilTime(2015,7,19,12,35,48,
                             gpstk.TimeSystem.GPS).toCommonTime()
        rv,nd = navLib.find(nmide, ct, gpstk.SVHealth.Any,
                            gpstk.NavValidityType.ValidOnly,
                            gpstk.NavSearchOrder.User)
        self.assertEqual(True, rv)
        self.assertEqual(64, nd.iode)
        rv,nd = navLib.find(nmida, ct, gpstk.SVHealth.Any,
                            gpstk.NavValidityType.ValidOnly,
                            gpstk.NavSearchOrder.User)
        self.assertEqual(False, rv)
        sat = gpstk.NavSatelliteID(2, 2, gpstk.SatelliteSystem.GPS,
                                   gpstk.CarrierBand.L1,
                                   gpstk.TrackingCode.CA, gpstk.NavType.GPSLNAV)
        nmide = gpstk.NavMessageID(sat, gpstk.NavMessageType.Ephemeris)
        ct = gpstk.CivilTime(2015,7,19,2,0,0,
                             gpstk.TimeSystem.GPS).toCommonTime()
        rv,nd = navLib.find(nmide, ct, gpstk.SVHealth.Any,
                            gpstk.NavValidityType.ValidOnly,
                            gpstk.NavSearchOrder.User)
        self.assertEqual(True, rv)
        self.assertEqual(7, nd.iode)

    def test_setValidityFilter(self):
        navLib = gpstk.NavLibrary()
        ndf = gpstk.RinexNavDataFactory()
        navLib.addFactory(ndf)
        # rudimentary test of setValidityFilter, just make sure it doesn't die
        navLib.setValidityFilter(gpstk.NavValidityType.ValidOnly)

    def test_setTypeFilter(self):
        navLib = gpstk.NavLibrary()
        ndf = gpstk.RinexNavDataFactory()
        navLib.addFactory(ndf)
        # rudimentary test of setTypeFilter
        # nmts = gpstk.NavMessageTypeSet()
        # nmts.add(gpstk.NavMessageType.Almanac)
        # navLib.setTypeFilter(nmts)

    def test_getTime(self):
        navLib = gpstk.NavLibrary()
        ndf = gpstk.RinexNavDataFactory()
        navLib.addFactory(ndf)
        ndf.addDataSource(args.input_dir+'/arlm2000.15n')
        expIni = gpstk.CivilTime(2015,7,19,0,0,0,
                                 gpstk.TimeSystem.GPS).toCommonTime()
        expFin = gpstk.CivilTime(2015,7,20,2,0,0,
                                 gpstk.TimeSystem.GPS).toCommonTime()
        self.assertEqual(expIni, navLib.getInitialTime())
        self.assertEqual(expFin, navLib.getFinalTime())

    def test_editClear(self):
        navLib = gpstk.NavLibrary()
        ndf = gpstk.RinexNavDataFactory()
        navLib.addFactory(ndf)
        ndf.addDataSource(args.input_dir+'/arlm2000.15n')
        self.assertEqual(337, ndf.size())
        navLib.clear()
        self.assertEqual(0, ndf.size())
        ndf.addDataSource(args.input_dir+'/arlm2000.15n')
        self.assertEqual(337, ndf.size())
        navLib.edit(gpstk.GPSWeekSecond(0,0).toCommonTime(),
                    gpstk.GPSWeekSecond(1854,28700).toCommonTime())
        self.assertEqual(229, ndf.size())
        sat = gpstk.NavSatelliteID(1, 1, gpstk.SatelliteSystem.GPS,
                                   gpstk.CarrierBand.L1,
                                   gpstk.TrackingCode.CA, gpstk.NavType.GPSLNAV)
        navLib.clear()
        self.assertEqual(0, ndf.size())
        ndf.addDataSource(args.input_dir+'/arlm2000.15n')
        self.assertEqual(337, ndf.size())
        navLib.edit(gpstk.GPSWeekSecond(0,0).toCommonTime(),
                    gpstk.GPSWeekSecond(1854,28700).toCommonTime(), sat)
        self.assertEqual(335, ndf.size())
        navLib.clear()
        self.assertEqual(0, ndf.size())
        ndf.addDataSource(args.input_dir+'/arlm2000.15n')
        self.assertEqual(337, ndf.size())
        sig = gpstk.NavSignalID(gpstk.SatelliteSystem.GPS, gpstk.CarrierBand.L1,
                                gpstk.TrackingCode.Y, gpstk.NavType.GPSLNAV)
        navLib.edit(gpstk.GPSWeekSecond(0,0).toCommonTime(),
                    gpstk.GPSWeekSecond(1854,28700).toCommonTime(), sig)
        self.assertEqual(337, ndf.size())
        sig = gpstk.NavSignalID(gpstk.SatelliteSystem.GPS, gpstk.CarrierBand.L1,
                                gpstk.TrackingCode.CA, gpstk.NavType.GPSLNAV)
        navLib.edit(gpstk.GPSWeekSecond(0,0).toCommonTime(),
                    gpstk.GPSWeekSecond(1854,28700).toCommonTime(), sig)
        self.assertEqual(229, ndf.size())

if __name__ == '__main__':
    run_unit_tests()
