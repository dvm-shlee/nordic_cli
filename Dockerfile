FROM mcr:2023a

RUN git clone https://github.com/dvm-shlee/nordic_cli.git /app
WORKDIR /app
RUN pip3 install poetry
RUN pip3 install -e .

# For Command Line Tool mode with input arguments provided
ENTRYPOINT [ "nordic" ]

# For Interactive mode
CMD ["bash"]