FROM mcr:2023a

ENV LANG=en_US.UTF-8

RUN git clone https://github.com/dvm-shlee/nordic_cli.git /app
WORKDIR /app
RUN pip3 install poetry
RUN pip3 install -e .

# For Interactive mode
CMD ["bash"]