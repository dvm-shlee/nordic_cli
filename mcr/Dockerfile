FROM ubuntu:latest

# Update package lists
RUN apt update

# Install required packages
RUN apt install -q -y --no-install-recommends libxt6 libgl1-mesa-glx libpython3.10 python3.10 python3-pip git unzip wget curl gcc libstdc++6

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
    ./install -agreeToLicense yes -mode silent -destinationFolder /opt/mcr

# Clean up the installation files
RUN rm -rf /mcr-src

# Configure environment variables for MCR
ENV LD_LIBRARY_PATH /lib/x86_64-linux-gnu:/lib:/opt/mcr/R2023a/runtime/glnxa64:/opt/mcr/R2023a/bin/glnxa64:/opt/mcr/R2023a/sys/os/glnxa64du :/opt/mcr/R2023a/extern/bin/glnxa64