# ReFrame test suite for HPE Cray EX machines

To run the test suite you need first to clone and bootstrap ReFrame and then this repo:

## Install ReFrame
```
git clone https://github.com/reframe-hpc/reframe.git
pushd reframe
./bootstrap.sh
export PATH=$(pwd)/bin:$PATH
popd
```

## Clone the tests

```
https://github.com/douglas-shanks/hpe_cray_reframe.git
cd hpe_cray_reframe
```

You can then list all the tests on any HPE Cray supported machine as follows:

```
reframe -C config/* -c tests/ -R -l
```
