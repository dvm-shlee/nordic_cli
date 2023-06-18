FROM ubuntu:latest

# Update package lists
RUN apt update

# Install required packages
RUN apt install -q -y --no-install-recommends xorg python3 python3-pip git unzip wget curl

# Clean up package lists
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the MCR from MathWorks site
RUN mkdir /mcr-src && \
    cd /mcr-src && \
    wget --no-check-certificate -q https://ssd.mathworks.com/supportfiles/downloads/R2023a/Release/2/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2023a_Update_2_glnxa64.zip

# Extract the downloaded MCR
RUN cd /mcr-src && \
    unzip -q MATLAB_Runtime_R2023a_Update_2_glnxa64.zip && \
    rm -f MATLAB_Runtime_R2023a_Update_2_glnxa64.zip

# Install the MCR with silent mode and agree to the license
RUN cd /mcr-src && \
    ./install -agreeToLicense yes -mode silent -destinationFolder /usr/local/mcr

# Clean up the installation files
RUN rm -rf /mcr-src

# Configure environment variables for MCR
ENV LD_LIBRARY_PATH /usr/local/mcr/v914/runtime/glnxa64:/usr/local/mcr/v914/bin/glnxa64:/usr/local/mcr/v914/sys/os/glnxa64:/usr/local/mcr/v914/extern/bin/glnxa64
ENV PATH /usr/local/bin

RUN git clone https://github.com/dvm-shlee/nordic_cli.git /app
WORKDIR /app
RUN pip3 install poetry
RUN pip3 install -e .

# For Command Line Tool mode with input arguments provided
ENTRYPOINT [ "executable" ]

# For Interactive mode
CMD ["bash"]