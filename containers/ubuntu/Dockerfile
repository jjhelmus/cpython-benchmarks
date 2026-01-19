FROM ubuntu:25.10

# install the system python
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv

# create a symlink so python works
RUN ln -s /usr/bin/python3 /usr/bin/python
