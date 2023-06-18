import argparse
from .. import run

def main(input_file, output_file, uppercase):
    # Your code logic here
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Uppercase: {uppercase}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line tool(CLI) for NORDIC Denoising')
    
    parser.add_argument('magni_path', help='Path to the input magnitude image file')
    parser.add_argument('output_path', help='Specifies the name of the output file')
    parser.add_argument('-p', '--phase_path', help='Path to the input phase image file')
    parser.add_argument('-m', '--modality', help='Indicates the image modality - "fMRI" or "dMRI"')
    parser.add_argument('-t', '--threshold_method', default='NORDIC', help='Determines the thresholding method - "NORDIC" or "MP"')
    parser.add_argument('--kernel_size_gfactor', nargs=3, type=int, default=[14, 14, 1], help='Specifies the kernel size for the g-factor')
    parser.add_argument('--kernel_size_pca', nargs=3, type=int, help='Specifies the kernel size for PCA')
    
    args, unknown_args = parser.parse_known_args()
    
    magni_path = args.magni_path
    output_path = args.output_path
    phase_path = args.phase_path
    modality = args.modality
    threshold_method = args.threshold_method
    kernel_size_gfactor = args.kernel_size_gfactor
    kernel_size_pca = args.kernel_size_pca
    
    # Collect remaining unknown arguments into a dictionary
    kwargs = dict(arg.split('=') for arg in unknown_args)
    
    run(magni_path, output_path, phase_path, modality, threshold_method, kernel_size_gfactor, kernel_size_pca, **kwargs)