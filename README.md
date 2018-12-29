halp: Hypergraph Algorithms Package<br>
==========

_halp_ is a Python software package that provides both a directed and an undirected hypergraph implementation, as well as several important and canonical algorithms that operate on these hypergraphs.

See [http://murali-group.github.io/halp/](http://murali-group.github.io/halp/) for documentation, code examples, and more information.

Development
===========
There is a docker container that the project can be run from inside of. We do this by mounting the project to a docker container that takes care of setting up the various dependencies the project has.

Build the container

```
$ docker build . -t halp
```

Run the container

```
$ docker run -it -v $(pwd):/root/halp halp bash
```

From within the container, we can check to see that tests pass

```
$ ./run_test.sh
```

Dependencies
===========
This project has dependencies on the following:
- [networkx](https://networkx.github.io/)
- [numpy](http://www.numpy.org/)
- [scipy](http://www.scipy.org/)
- [liblpsolve](http://lpsolve.sourceforge.net/5.5/)

These are (hopefully!) taken care of via use of a docker container. For more details see `dockerfile`.
