FROM debian:forky

# install the system python
RUN apt-get update && apt-get install -y --no-install-recommends python3.14 python3.14-venv

# create symlinks so python works
RUN ln -s /usr/bin/python3.14 /usr/bin/python3
RUN ln -s /usr/bin/python3 /usr/bin/python
