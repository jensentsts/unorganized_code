import calculator
import ccd_processor as ccd_psr
import wit_processor as wit_psr

# debug
debug = False
if debug:
    last_data = 0
    this_data = 0
    ccd = ccd_psr.CcdProcessor('333')
    while True:
        ccd.select_file_path()
        if ccd.get_file_amount() == 0:
            exit(0)
        ccd.show_plot(show_data=False)
        this_data = ccd.get_min_height_index()
        print('[ccd]={0}    delta={1}'.format(this_data, this_data - last_data))
        last_data = this_data


if __name__ == '__main__':
    for i in range(1, 4):
        calc = calculator.Calculator(times=i)
        calc.select_data_directory_path()
        calc.work_out()
