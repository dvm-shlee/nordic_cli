FROM sungholee/mcr:2023a

RUN git clone https://github.com/dvm-shlee/nordic_cli.git /src && pip3 install poetry && pip3 install -e /src && mkdir /workdir
WORKDIR /workdir

# For Interactive mode
CMD ["bash"]