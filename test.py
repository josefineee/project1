def northsouth(arr, idx):
    if arr[idx+1] is "SOUTH" or arr[idx+1] is "NORTH":
        arr.pop(idx)
        arr.pop(idx+1)

def westeast(arr, idx):
    if arr[idx+1] is "WEST" or arr[idx+1] is "EAST":
        arr.pop(idx)
        arr.pop(idx+1)



def dirReduc(arr):
    print(len(arr))
    idx=0
    while idx <= (len(arr)-1):
      arr[idx].upper()
      print(idx+1)
      print("the len of arr is: {}".format(len(arr)))
      if idx+1 > len(arr)-1:
        print("Now we should breal for loop")
        break
      elif arr[idx] is "NORTH" or arr[idx] is "SOUTH":
        northsouth(arr, idx)
      elif arr[idx] is "WEST" or arr[idx] is "EAST":
        westeast(arr, idx)
      idx+=1
    print(arr)

a = ["NORTH", "SOUTH", "SOUTH", "EAST", "WEST", "NORTH", "WEST"]
dirReduc(a)

