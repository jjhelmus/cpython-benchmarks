FROM fedora:43
FROM rockylinux/rockylinux:10

RUN dnf -y update && dnf clean all
RUN dnf -y install python3 && dnf clean all

# create a symlink so python works
RUN ln -s /usr/bin/python3 /usr/bin/python
