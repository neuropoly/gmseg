import subprocess
import glob
import os
import nibabel as nib

def run_main():
    error_files = []
    for original_file in glob.glob("training/*.gz"):

        if "fixed" in original_file:
            print "------> Skipping fixed"
            continue

        nifile = nib.load(original_file)
        pixdim = nifile.header["pixdim"][3]
        only_fname = os.path.split(original_file)[1]

        data = nifile.get_data()
        affine = nifile.get_affine()
        header = nifile.get_header()
        
        sform_code, qform_code = header["sform_code"], \
                                 header["qform_code"]
            
        if sform_code == 0 and qform_code == 0:
            sform = header.get_sform()
            qform = header.get_qform()

            header.set_sform(sform, "scanner")
            header.set_qform(qform, "scanner")
            
        if "mask" in original_file:
            data[data > 1] = 0

        ni_img = nib.Nifti1Image(data, affine, header)
        nib.save(ni_img, "training/fixed_{}".format(only_fname))
        original_file = "training/fixed_{}".format(only_fname)
           
        print
        print ">>>>>>>> Fixed file -> {}".format(original_file)
            
        cmd = ["sct_resample", "-i {}".format(original_file),
               "-o training_resample/{}".format(only_fname),
               "-mm 0.25x0.25x{:.1f}".format(pixdim)]

        output = subprocess.check_output(cmd)


    print error_files
    print len(error_files)

if __name__ == "__main__":
    run_main()
