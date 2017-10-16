import subprocess
import glob
import os
import nibabel as nib

def run_main():
    error_files = []
    for original_file in glob.glob("test_resample_predictions/*.gz"):
        only_fname = os.path.split(original_file)[1]
        
        fname = os.path.split(original_file)[1]
        target_space_name = fname.split("_")[0]
        target_space_name = target_space_name + "-image.nii.gz"
        target_space_name = os.path.join("test", target_space_name)
        
        nifile = nib.load(target_space_name)
        pixdim = nifile.header["pixdim"]
        
        cmd = ["sct_resample", "-i {}".format(original_file),
               "-o test_predictions/{}".format(only_fname),
               "-mm {}x{}x{}".format(pixdim[1], pixdim[2], pixdim[3])]

        output = subprocess.check_output(cmd)


    print error_files
    print len(error_files)

if __name__ == "__main__":
    run_main()
