import os

path = '/home/wallace/Downloads'
path2 = '/home/wallace/Extratos'

cnpj = ['031.544.217/0001-96', '032.295.244/0001-35', '016.542.170/0001-38', '030.144.066/0001-16', '027.927.468/0001-82',
'032.159.149/0001-04' ]

n=0
for filename in os.listdir(path):
  filename_without_ext = os.path.splitext(filename)[0]
  extension = os.path.splitext(filename)[1]
  
  x = cnpj[n].split("/")
  print(x)
  new_file_name = 'saldo_investimento_'+x[0]+'.'+x[1]+'.csv' 
  print(new_file_name)       
  try:
    os.rename(os.path.join(path, filename),
        os.path.join(path2, new_file_name))
    #todo: shutil.move(path, path2)                
  except:
    print("Socorro 01!" + filename)                    
  print(filename)

  n += 1
