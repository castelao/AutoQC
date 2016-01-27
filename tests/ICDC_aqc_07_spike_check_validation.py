import qctests.ICDC_aqc_07_spike_check as ICDC_sc

import util.testingProfile
import numpy as np

##### ICDC spike check.
##### --------------------------------------------------

def test_ICDC_spike_check():
    '''Make sure code processes data supplied by Viktor Gouretski
       correctly.
    '''

    lines = data.splitlines()
    for i, line in enumerate(lines):
        if line[0:2] == 'HH':
            header  = line.split()
            nlevels = int(header[-1][:-3])
            
            depths  = []
            temps   = []
            qctruth = []
            for j in range(nlevels):
                d = lines[i + j + 1].split()
                depths.append(float(d[0]))
                temps.append(float(d[1]))
                qctruth.append(int(d[2]) > 0)
            
            p  = util.testingProfile.fakeProfile(temps, depths)
            qc = ICDC_sc.test(p)

            assert np.array_equal(qc, qctruth), 'Failed profile with header ' + line

# Data provided by Viktor Gouretski, ICDC, University of Hamburg.
data = '''
HH    8836584    34.950   140.333 1968  1 19     10OSD
     .0    17.900 0
   10.0    18.090 0
   20.0    18.050 0
   30.0    10.030 1
   50.0    17.670 0
   75.0    16.150 0
  100.0    16.140 0
  150.0    15.510 0
  200.0    15.400 0
  300.0    13.330 0
HH    3230656    20.580  -156.100 1967  6 14    378CTD
     .0    26.370 0
    2.0    26.370 0
    4.0    26.370 0
    6.0    26.370 0
    8.0    26.370 0
   10.0    26.360 0
   12.0    26.350 0
   14.0    26.330 0
   16.0    26.240 0
   18.0    26.100 0
   20.0    25.960 0
   22.0    25.820 0
   24.0    25.670 0
   26.0    25.600 0
   28.0    25.580 0
   30.0    25.530 0
   32.0    25.440 0
   34.0    25.310 0
   36.0    25.170 0
   38.0    25.090 0
   40.0    25.060 0
   42.0    25.010 0
   44.0    24.940 0
   46.0    24.870 0
   48.0    24.810 0
   50.0    24.670 0
   52.0    24.390 0
   54.0    24.160 0
   56.0    24.050 0
   58.0    23.930 0
   60.0    23.750 0
   62.0    23.520 0
   64.0    23.320 0
   66.0    23.220 0
   68.0    23.090 0
   70.0    22.860 0
   72.0    22.650 0
   76.0    22.410 0
   78.0    22.220 0
   80.0    22.000 0
   82.0    21.880 0
   84.0    21.790 0
   86.0    21.650 0
   88.0    21.560 0
   90.0    21.460 0
   92.0    21.300 0
   94.0    22.520 0
   96.0    21.090 0
   98.0    21.060 0
  100.0    21.020 0
  102.0    20.970 0
  104.0    20.930 0
  106.0    20.870 0
  108.0    20.770 0
  110.0    20.690 0
  112.0    20.620 0
  114.0    15.960 1
  116.0    20.500 0
  118.0    20.460 0
  120.0    20.410 0
  122.0    20.290 0
  124.0    20.050 0
  126.0    19.770 0
  128.0    19.600 0
  130.0    19.480 0
  132.0    19.380 0
  134.0    20.560 0
  136.0    19.170 0
  138.0    19.090 0
  140.0    18.980 0
  142.0    18.830 0
  144.0    18.700 0
  146.0    18.580 0
  148.0    18.440 0
  150.0    18.250 0
  152.0    18.050 0
  154.0    19.270 0
  156.0    17.770 0
  158.0    17.630 0
  160.0    17.540 0
  162.0    17.490 0
  164.0    17.430 0
  166.0    17.310 0
  168.0    17.210 0
  170.0    17.160 0
  172.0    17.180 0
  174.0    17.900 0
  176.0    17.090 0
  178.0    17.030 0
  180.0    16.980 0
  182.0    16.880 0
  184.0    16.750 0
  186.0    16.620 0
  188.0    16.490 0
  190.0    16.350 0
  192.0    16.180 0
  194.0    17.170 0
  196.0    15.750 0
  198.0    15.610 0
  200.0    15.530 0
  202.0    15.470 0
  204.0    15.400 0
  206.0    15.340 0
  208.0    15.270 0
  210.0    15.190 0
  212.0    15.090 0
  214.0    15.010 0
  216.0    14.910 0
  218.0    14.790 0
  220.0    14.680 0
  222.0    14.550 0
  224.0    14.370 0
  226.0    14.150 0
  228.0    13.990 0
  230.0    13.940 0
  232.0    13.850 0
  234.0    13.650 0
  236.0    13.480 0
  238.0    13.390 0
  240.0    13.350 0
  242.0    13.320 0
  244.0    13.280 0
  246.0    13.210 0
  248.0    13.130 0
  250.0    13.030 0
  252.0    12.910 0
  254.0    12.760 0
  256.0    12.560 0
  258.0    12.270 0
  260.0    11.940 0
  262.0    11.740 0
  264.0    11.660 0
  266.0    11.590 0
  268.0    11.540 0
  270.0    11.500 0
  272.0    11.470 0
  274.0    11.440 0
  276.0    11.420 0
  278.0    11.400 0
  280.0    11.360 0
  282.0    11.290 0
  284.0    11.200 0
  286.0    11.100 0
  288.0    10.980 0
  290.0    10.840 0
  292.0    10.700 0
  294.0    10.580 0
  296.0    10.480 0
  298.0    10.410 0
  300.0    10.350 0
  302.0    10.250 0
  304.0    10.140 0
  306.0    10.070 0
  308.0    10.030 0
  310.0     9.990 0
  312.0     9.960 0
  314.0     9.910 0
  316.0     9.850 0
  318.0     9.780 0
  320.0     9.730 0
  322.0     9.700 0
  324.0     9.670 0
  326.0     9.650 0
  328.0     9.630 0
  330.0     9.610 0
  332.0     9.580 0
  334.0     9.490 0
  336.0     9.340 0
  338.0     9.230 0
  340.0     9.180 0
  342.0     9.150 0
  344.0     9.130 0
  346.0     9.120 0
  348.0     9.090 0
  350.0     9.010 0
  352.0     8.900 0
  354.0     8.770 0
  356.0     8.660 0
  358.0     8.570 0
  360.0     8.510 0
  362.0     8.470 0
  364.0     8.430 0
  366.0     8.370 0
  368.0     8.310 0
  370.0     8.280 0
  372.0     8.300 0
  374.0     8.330 0
  376.0     8.300 0
  378.0     8.260 0
  380.0     8.250 0
  382.0     8.250 0
  384.0     8.250 0
  386.0     8.240 0
  388.0     8.230 0
  390.0     8.220 0
  392.0     8.200 0
  394.0     8.190 0
  396.0     8.190 0
  398.0     8.190 0
  400.0     8.130 0
  402.0     8.000 0
  404.0     7.910 0
  406.0     7.860 0
  408.0     7.820 0
  410.0     7.810 0
  412.0     7.780 0
  414.0     7.710 0
  416.0     7.630 0
  418.0     7.570 0
  420.0     7.540 0
  422.0     7.510 0
  424.0     7.490 0
  426.0     7.460 0
  428.0     7.410 0
  430.0     7.380 0
  432.0     7.350 0
  434.0     7.320 0
  436.0     7.280 0
  438.0     7.240 0
  440.0     7.220 0
  442.0     7.190 0
  444.0     7.170 0
  446.0     7.160 0
  448.0     7.150 0
  450.0     7.100 0
  452.0     7.020 0
  454.0     6.980 0
  456.0     6.970 0
  458.0     6.960 0
  460.0     6.940 0
  462.0     6.900 0
  464.0     6.850 0
  466.0     6.820 0
  468.0     6.820 0
  470.0     6.840 0
  472.0     6.850 0
  474.0     6.830 0
  476.0     6.790 0
  478.0     6.740 0
  480.0     6.690 0
  482.0     6.660 0
  484.0     6.640 0
  486.0     6.610 0
  488.0     6.560 0
  490.0     6.540 0
  492.0     6.530 0
  494.0     6.520 0
  496.0     6.520 0
  498.0     6.530 0
  500.0     6.520 0
  502.0     6.530 0
  504.0     6.530 0
  506.0     6.530 0
  508.0     6.520 0
  510.0     6.520 0
  512.0     6.520 0
  514.0     6.510 0
  516.0     6.490 0
  518.0     6.470 0
  520.0     6.440 0
  522.0     6.410 0
  524.0     6.390 0
  526.0     6.390 0
  528.0     6.390 0
  530.0     6.400 0
  532.0     6.400 0
  534.0     6.400 0
  536.0     6.390 0
  538.0     6.390 0
  540.0     6.390 0
  542.0     6.380 0
  544.0     6.370 0
  546.0     6.360 0
  548.0     6.350 0
  550.0     6.310 0
  552.0     6.260 0
  554.0     6.220 0
  556.0     6.200 0
  558.0     6.170 0
  560.0     6.150 0
  562.0     6.140 0
  564.0     6.120 0
  566.0     6.100 0
  568.0     6.070 0
  570.0     6.060 0
  572.0     6.050 0
  574.0     6.040 0
  576.0     6.030 0
  578.0     6.010 0
  580.0     5.970 0
  582.0     5.940 0
  584.0     5.910 0
  586.0     5.900 0
  588.0     5.900 0
  590.0     5.880 0
  592.0     5.860 0
  594.0     5.850 0
  596.0     5.850 0
  598.0     5.840 0
  600.0     5.820 0
  602.0     5.790 0
  604.0     5.770 0
  606.0     5.760 0
  608.0     5.750 0
  610.0     5.740 0
  612.0     5.730 0
  614.0     5.720 0
  616.0     5.720 0
  618.0     5.710 0
  620.0     5.690 0
  622.0     5.660 0
  624.0     5.620 0
  626.0     5.610 0
  628.0     5.600 0
  630.0     5.590 0
  632.0     5.570 0
  634.0     5.550 0
  636.0     5.540 0
  638.0     5.540 0
  640.0     5.540 0
  642.0     5.530 0
  644.0     5.530 0
  646.0     5.520 0
  648.0     5.510 0
  650.0     5.510 0
  652.0     5.490 0
  654.0     5.470 0
  656.0     5.450 0
  658.0     5.440 0
  660.0     5.420 0
  662.0     5.420 0
  664.0     5.420 0
  666.0     5.400 0
  668.0     5.370 0
  670.0     5.340 0
  672.0     5.330 0
  674.0     5.310 0
  676.0     5.300 0
  678.0     5.300 0
  680.0     5.300 0
  682.0     5.290 0
  684.0     5.280 0
  686.0     5.280 0
  688.0     5.280 0
  690.0     5.270 0
  692.0     5.250 0
  694.0     5.240 0
  696.0     5.220 0
  698.0     5.210 0
  700.0     5.200 0
  702.0     5.190 0
  704.0     5.180 0
  706.0     5.180 0
  708.0     5.180 0
  710.0     5.170 0
  712.0     5.170 0
  714.0     5.150 0
  716.0     5.140 0
  718.0     5.140 0
  720.0     5.150 0
  722.0     5.160 0
  724.0     5.160 0
  726.0     5.160 0
  728.0     5.150 0
  730.0     5.140 0
  732.0     5.130 0
  734.0     5.120 0
  736.0     5.110 0
  738.0     5.100 0
  740.0     5.100 0
  742.0     5.100 0
  744.0     5.090 0
  746.0     5.090 0
  748.0     5.100 0
  750.0     5.100 0
  752.0     5.100 0
  754.0     5.100 0
  756.0     5.100 0
HH   10089075    55.981   -54.259 1997 10 13     54PFL
   28.1     8.175 0
   37.9     8.172 0
   47.8     8.172 0
   57.7     6.831 0
   67.5     5.484 0
   77.3     5.486 0
   96.9    46.647 0
  106.7    10.624 1
  116.5     5.531 0
  126.3     5.534 0
  136.1     5.520 0
  145.9     5.326 0
  155.7     5.495 0
  165.5     5.484 0
  175.3     5.456 0
  185.1     5.434 0
  199.9     5.417 0
  219.5     5.395 0
  239.1     5.335 0
  258.7     5.269 0
  278.4     5.212 0
  297.9     5.115 0
  317.5     5.099 0
  337.1     5.117 0
  356.7     5.107 0
  376.3     5.093 0
  395.9     5.072 0
  415.5     5.061 0
  435.1     5.034 0
  454.7     5.021 0
  459.6     5.016 0
  508.6     4.986 0
  557.5     4.938 0
  606.4     4.883 0
  655.4     4.859 0
  704.3     4.835 0
  753.2     4.827 0
  802.2     4.822 0
  851.0     4.799 0
  899.8     4.785 0
  948.8     4.778 0
  997.6     4.762 0
 1046.4     4.788 0
 1095.3     4.772 0
 1144.1     4.728 0
 1192.9     4.678 0
 1241.7     4.663 0
 1290.5     4.663 0
 1339.2     4.652 0
 1388.0     4.652 0
 1436.7     4.652 0
 1485.5     4.655 0
 1534.2     4.660 0
 1558.5     4.660 0
HH   10872380   -61.927    33.745 2004  7 12     20APB
    6.7    36.400 0
   71.4    36.400 0
   82.8    -1.921 0
   90.4     8.183 1
   94.2    -2.495 0
  116.9    -1.553 0
  120.8    -1.396 0
  139.8     -.611 0
  170.2      .644 0
  173.9      .644 0
  223.4      .644 0
  242.4      .644 0
  257.5      .644 0
  306.9      .798 0
  310.8      .798 0
  367.7      .798 0
  375.3      .792 0
  405.7      .770 0
  561.2      .656 0
  577.3      .644 0
HH    4364678    33.200   -53.650 1950  1  3     22MBT
     .0    19.900 0
    5.0    12.600 1
   10.0    27.300 1
   15.0    19.900 0
   20.0    19.900 0
   25.0    19.900 0
   30.0    35.100 0
   35.0    20.400 0
   40.0    19.700 0
   45.0    19.700 0
   50.0    19.700 0
   55.0    19.700 0
   60.0    19.700 0
   65.0    19.700 0
   70.0    19.600 0
   75.0    19.600 0
   80.0    19.600 0
   85.0    19.600 0
   90.0    19.600 0
   95.0    19.500 0
  100.0    19.500 0
  105.0    19.500 0
HH    9431483    42.000   -14.483 1968 10 28     18XBT
     .0    18.400 0
   18.0     8.400 1
   25.0    18.300 0
   44.0    18.300 0
   50.0    15.800 0
   61.0    13.800 0
   70.0    13.300 0
   75.0    13.100 0
  100.0    13.000 0
  110.0    12.800 0
  132.0    12.800 0
  150.0    12.600 0
  200.0    12.300 0
  250.0    12.100 0
  300.0    12.000 0
  350.0    11.800 0
  400.0    11.600 0
  450.0    11.400 0
'''
