import argparse
from .. import run

def main():
    parser = argparse.ArgumentParser(description='Command line tool(CLI) for NORDIC Denoising')
    
    parser.add_argument('-i', '--magni_path', help='Path to the input magnitude image file')
    parser.add_argument('-o', '--output_path', help='Specifies the name of the output file')
    parser.add_argument('-p', '--phase_path', help='Path to the input phase image file')
    parser.add_argument('-m', '--modality', help='Indicates the image modality - "fMRI" or "dMRI"')
    parser.add_argument('-t', '--threshold_method', default='NORDIC', help='Determines the thresholding method - "NORDIC" or "MP"')
    parser.add_argument('-v', '--verbose', action='store_true', help="Print out the true injecting input arguments to NIFTI_NORDIC MATLAB function")
    parser.add_argument('--kernel_size_gfactor', nargs=3, type=int, default=[14, 14, 1], metavar=('sizex', 'sizey', 'sizez'), help='Specifies the kernel size for the g-factor')
    parser.add_argument('--kernel_size_pca', nargs=3, type=int, default=[5, 5, 5], metavar=('sizex', 'sizey', 'sizez'), help='Specifies the kernel size for PCA')
    parser.add_argument('--gfactor_path_overlap', nargs=1, type=int, default=None, help='overlap for gfactor patch')
    
    args, unknown_args = parser.parse_known_args()
    
    magni_path = args.magni_path
    output_path = args.output_path
    phase_path = args.phase_path
    modality = args.modality
    threshold_method = args.threshold_method
    kernel_size_gfactor = args.kernel_size_gfactor
    kernel_size_pca = args.kernel_size_pca
    gfactor_path_overlap = args.gfactor_path_overlap
    verbose = args.verbose
    
    # Collect remaining unknown arguments into a dictionary
    
    if len(unknown_args):
        argindice = [i for i, v in enumerate(unknown_args) if '--' in v]
        kwargs = dict()
        for i in argindice:
            key = unknown_args[i][2:]
            val = unknown_args[i+1]
            kwargs[key] = val
    
    run(magni_path, output_path, phase_path, modality, threshold_method, kernel_size_gfactor, kernel_size_pca, gfactor_path_overlap, verbose=verbose, **kwargs)
    
if __name__ == "__main__":
    main()