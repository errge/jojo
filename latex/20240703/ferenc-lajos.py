#!/usr/bin/python3

# Van 2 darab lajos aranyunk es 3 ferenc ezustunk.
# Hany felekeppen tudjuk oket sorbarakni, ha az azonos ermek megkulonboztethetetlenek?

def megold1():
  for a in ['F', 'L']:
    for b in ['F', 'L']:
      for c in ['F', 'L']:
        for d in ['F', 'L']:
          for e in ['F', 'L']:
            fek = 0
            lek = 0
            for i in [a,b,c,d,e]:
              if i == 'F':
                fek += 1
              else:
                lek += 1
            if not fek == 3: continue
            if not lek == 2: continue
            print(a,b,c,d,e)

# megold1()

def kiemelo(lista, il):
  output = []
  for i in il:
    output.append(lista[i])
    lista = lista[:i] + lista[i+1:]
  return "".join(output)

def megold2():
  retlist = []
  elemek = ('F', 'F', 'F', 'L', 'L')
  for a in range(5):
    for b in range(4):
      for c in range(3):
        for d in range(2):
          for e in range(1):
            indexek = [a,b,c,d,e]
            print(indexek)
            retlist.append(kiemelo(list(elemek), indexek))
  print(len(   (retlist)))
  print(len(set(retlist)))

# megold2()

def osszes_sorbateves(lista):
  if lista == []:
    yield []
  for i in range(len(lista)):
    e = lista[i]
    maradek = lista[:i] + lista[i+1:]
    for rest in osszes_sorbateves(maradek):
      yield([e] + rest)

def megold3():
  retlist = []
  elemek = ('F', 'F', 'F', 'L', 'L')
  for indexek in osszes_sorbateves(list(range(len(elemek)))):
    newretlist = []
    for i in indexek:
      newretlist.append(elemek[i])
    retlist.append("".join(newretlist))
  print(len(   (retlist)))
  print(len(set(retlist)))

megold3()
