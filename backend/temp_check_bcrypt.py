from passlib.hash import bcrypt
h = bcrypt.hash('123456')
print(h)                     # deve começar com $
print(bcrypt.verify('123456', h))  # True
