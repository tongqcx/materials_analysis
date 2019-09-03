import string
def names(aa):
    for i in aa:    
        i=i.strip()
        print(i)
        print('---')
        a=i.rstrip(string.digits)
        print (i)

if __name__=='__main__':
    f=open('name.txt','r')
    name=f.readlines()
    re=names(name)
