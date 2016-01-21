git interpret
=============

translations
============

* nikola

One way versus two way
======================

Functions which are hard to reverse.

Functions which are easy to reverse.

Information.

Interpretters aka Babelfish
===========================

.. python::

   class Foo:

       def interpret(self, msg, other):
           """ Interpret a message from other

           May be passed via others.

           >>> foo.interpret(msg, [fred, dick, harry])
           42

           Message is from fred via dick and harry

           If you want to know what dick said harry might know.

           If you want to know what fred said, fred might know.
           """
           return 42

