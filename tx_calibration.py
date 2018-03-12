import sys
import lib.ioreg
from time import sleep

def tx_impedance_calibration():

	segment_step = 1.0
	n_segment_count = 0
	n_pre_count = 0
	n_main_count = 0
	n_post_count = 0
	
	p_segment_count = 0
	p_pre_count = 0
	p_pre_seg = 0
	p_main_count = 0
	p_main_seg = 0
	p_post_count = 0
	p_post_seg = 0
	
	
	nseg_voltage_target = 750
	pseg_voltage_target = 750
	measured_voltage = 0
	
	tx_reg = lib.ioreg.Register("xml/registers.xml", "tx")
	
	tx_impedance_setup()
	tx_impedance_set_user_pattern()
	
	while measured_voltage < pseg_voltage_target:
		#how to enable n_pre_2R?
		
		#add segment
		if(p_main_count < 0xF0):
			p_main_seg = 1 | (p_main_count<<1)
			p_main_count += 1
			p_segment_count += segment_step
		else if (p_post_count < 0xF0):
			p_post_seg = 1 | (p_post_count<<1)
			p_post_count += 1
			p_segment_count += segment_step
		else if (p_pre_count < 0x20):
			p_pre_seg = 1 | (p_pre_count<<1)
			p_pre_count += 1
			p_segment_count += segment_step
		else
			print("we're out of places to add segments?")
	
		tx_impedance_fill_tx_register(tx_reg,n_main_seg,n_post_seg,n_pre_seg,p_main_seg,p_post_seg,p_pre_seg)
		tx_reg.write()
	
		measured_voltage = read_voltage()
		
	measured_voltage = 0
	p_pre_seg = 0
	p_main_seg = 0
	p_post_seg = 0
	
	while measured_voltage < nseg_voltage_target:
		
		#add segment
		if(n_main_count < 0xF0):
			n_main_seg = 1 | (n_main_count<<1)
			n_main_count += 1
			n_segment_count += segment_step
		else if (n_post_count < 0xF0):
			n_post_seg = 1 | (n_post_count<<1)
			n_post_count += 1
			n_segment_count += segment_step
		else if (n_pre_count < 0x20):
			n_pre_seg = 1 | (n_pre_count<<1)
			n_pre_count += 1
			n_segment_count += segment_step
		else
			print("we're out of places to add segments?")
	
		tx_impedance_fill_tx_register(tx_reg,n_main_seg,n_post_seg,n_pre_seg,p_main_seg,p_post_seg,p_pre_seg)
		tx_reg.write()
	
		sleep(0.02)
	
		measured_voltage = read_voltage()
		
		
	print ("Total P segments: " + p_segment_count)
	print (" p main segments: " + p_main_count)
	print (" p post segments: " + p_post_count)
	print (" p pre segments: " + p_pre_count)
	print ("")
	print ("Total N segments: " + n_segment_count)
	print (" n main segments: " + n_main_count)
	print (" n post segments: " + n_post_count)
	print (" n pre segments: " + n_pre_count)
	

	return


def read_voltage():
	#dummy read for now
	return random.randrange(0,1000)
	
def tx_impedance_setup():
	setup_reg = lib.ioreg.Register("xml/registers.xml", "setup")
	setup_reg.set("prbs_mode","00")
	setup_reg.set("use_udp","1")
	setup_reg.set("invert_unload","0")
	setup_reg.set("fast_read_en","0")
	setup_reg.set("test_out","000")
	setup_reg.set("tx_en","1")
	setup_reg.set("pll_en","0")
	setup_reg.set("ioo_en","0")
	setup_reg.set("iof_en","0")
	setup_reg.set("miso_alt","00")
	setup_reg.write()
	return
	
def tx_impedance_set_user_pattern():
	tx_udp_reg = lib.ioreg.Register("xml/registers.xml", "tx_udp")
	tx_udp_reg.set("udp","1111111111111111111111111111111111111111111111111111111111111111")
	tx_udp_reg.write()
	return
	
def tx_impedance_prefill_tx_register(tx_reg):
	tx_reg.set("bs_txc_reo",			"0")
	tx_reg.set("burnin_mode_dc",		"0")
	tx_reg.set("txc_dctest",			"0")
	tx_reg.set("en_nseg_main",			"0000000")
	tx_reg.set("en_nseg_marginpd",		"00000000")
	tx_reg.set("en_nseg_marginpu",		"00000000")
	tx_reg.set("en_nseg_post",			"0000000") 
	tx_reg.set("en_nseg_pre",			"00000") 
	tx_reg.set("en_pseg_main",			"0000000")
	tx_reg.set("en_pseg_marginpd",		"00000000")
	tx_reg.set("en_pseg_marginpu",		"00000000")
	tx_reg.set("en_pseg_post",			"0000000")  
	tx_reg.set("en_pseg_pre",			"00000")
	tx_reg.set("sel_nseg_marginpd",		"00000000")
	tx_reg.set("sel_nseg_post",			"0000000")
	tx_reg.set("sel_nseg_pre",			"00000")   
	tx_reg.set("sel_pseg_marginpu",		"00000000")
	tx_reg.set("sel_pseg_post",			"0000000")   
	tx_reg.set("sel_pseg_pre",			"00000")
	tx_reg.set("tdr_txc_enable_dc",		"0")
	tx_reg.set("tdr_txc_nref_dc",		"00000000")
	tx_reg.set("tdr_txc_pad_sel_dc",	"0")
	tx_reg.set("tdr_txc_pulse_iox16",	"0")
	tx_reg.set("txc_drv_boost_en",		"1")
	tx_reg.set("txc_drv_boost_tst_en",	"0")
	tx_reg.set("txc_drv_en_n",			"1")
	tx_reg.set("txc_drv_en_p",			"1")
	tx_reg.set("txc_prbs_clear",		"0")
	tx_reg.set("txc_prbs_enable",		"0")
	tx_reg.set("txc_rxcal",				"0")
	tx_reg.set("txc_sst_ctl",			"0")
	tx_reg.set("txc_unload_sel",		"000")
	tx_reg.set("txc_en_all",			"0")
	return
	
def tx_impedance_fill_tx_register(tx_reg,nmain,npost,npre,pmain,ppost,ppre):
	tx_reg.set("en_nseg_main",			"{0:07b}".format(nmain))
	tx_reg.set("en_nseg_post",			"{0:07b}".format(npost)) 
	tx_reg.set("en_nseg_pre",			"{0:05b}".format(npre)) 
	tx_reg.set("en_pseg_main",			"{0:07b}".format(pmain))
	tx_reg.set("en_pseg_post",			"{0:07b}".format(ppost)) 
	tx_reg.set("en_pseg_pre",			"{0:05b}".format(ppre)) 
	return
