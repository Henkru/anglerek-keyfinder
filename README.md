# anglerek-keyfinder
Pohlig-Hellman implementation to crack the DH key that Angler EK uses. This software is part of my Bachelor's thesis and the implementation base on [this](https://securelist.com/blog/research/72097/attacking-diffie-hellman-protocol-implementation-in-the-angler-exploit-kit/) article.

# Arguments
```
  -Y Public part
  -g Generator
  -p Modulo
```

# Example
```
anglerek-keyfinder.py -Y 7892150445281019518426774740123123083 -g 85913745537567961602381383355882121637 -p 35948145881546650497425055363061529726
```
