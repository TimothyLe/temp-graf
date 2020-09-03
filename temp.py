import time
import logging
import subprocess

logging.basicConfig(filename='temperature.log', filemode='a', format='%(created)f %(message)s', level=logging.INFO) 

while True:
    # TEMPERATURE
    mt = "/opt/vc/bin/vcgencmd measure_temp"
    pt = subprocess.Popen(mt.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t_output, t_err = pt.communicate()
    temp = t_output.decode("utf-8").split('=')[1].split("'")[0]
    temp = float(temp) * 1.8 + 32.0

    # CPU FREQUENCY
    scf = "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
    cf = subprocess.Popen(scf.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    c_output, c_err = cf.communicate()
    cpu = int(c_output.decode("utf-8")) / 1000000

    # CLOCKS
    c_dict = {}
    mc = "vcgencmd measure_clock {0}"
    clknames = "arm core h264 isp v3d uart pwm emmc pixel vec hdmi dpi".split()
    for src in clknames:
        cn = subprocess.Popen(mc.format(src).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        c_output, c_err = cn.communicate()
        c_output = int(c_output.decode("utf-8").split('=')[1].rstrip())
        c_dict[src] = c_output    

    # VOLTAGE 
    v_dict = {}
    mv = "vcgencmd measure_volts {0}" 
    iv = "core sdram_c sdram_i sdram_p".split()
    for src in iv:
        v = subprocess.Popen(mv.format(src).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        v_output, v_err = v.communicate()
        v_output = float(v_output.decode("utf-8").split('=')[1].rstrip()[:-1])
        v_dict[src] = v_output

    logging.info('CPU_TEMP={0:0.1f} F CPU_FREQ={1} MHz CORE_CLK={2} MHz CORE_VOLTAGE={3} V'.format(temp,cpu,c_dict['core']/1000000,v_dict['core']))
    time.sleep(300)
