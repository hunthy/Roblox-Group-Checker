import os
import requests
import random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def checkGroup():
  proxyList = open("proxies.txt", "r").readlines()

  count = 0
  currentProxy = random.choice(proxyList).replace("\n","")

  while True:
    id = random.randint(1, 1255555)

    try:
      count += 1
      re = requests.get(f"https://groups.roblox.com/v1/groups/{id}", verify=False, proxies={"https":f'http://{currentProxy}'})

      if 'TooManyRequests' in re.text:
        oldproxy = currentProxy
        currentProxy = random.choice(proxyList).replace("\n","")
        print(f"[Info] Getting ratelimited, switching proxy [{oldproxy} -> {currentProxy}]")
      else:
          if not re.json()["owner"] and re.json()['publicEntryAllowed']:
            try:
              re.json()["isLocked"] # Will try to parse isLocked, if not found will error and so it will know it's not locked
              print(f"({count}) [{currentProxy}] [invalid] https://web.roblox.com/groups/{id} | Locked | [Writing to file]")
              f = open("unclaimable_groups.txt", "a")
              f.write(f"https://web.roblox.com/groups/{id}\n")
              f.close()
            except:
              print(f"({count}) [{currentProxy}] [hit] https://web.roblox.com/groups/{id} [Writing to file]")
              f = open("claimable_groups.txt", "a")
              f.write(f"https://web.roblox.com/groups/{id}\n")
              f.close()
          else:
              print(f"({count}) [{currentProxy}] [invalid] https://web.roblox.com/groups/{id}  [Writing to file]")
              f = open("unclaimable_groups.txt", "a")
              f.write(f"https://web.roblox.com/groups/{id}\n")
              f.close()
    
    except:
        oldproxy = currentProxy
        currentProxy = random.choice(proxyList).replace("\n","")
        print(f"[Info] Proxy error, switching proxy [{oldproxy} -> {currentProxy}]")

if __name__ ==  '__main__':
  print("Roblox Group Checker made by SirWeeb (https://www.novaline.xyz)")
  open("unclaimable_groups.txt", "w").close() # Will make the file if not there & clear them
  open("claimable_groups.txt", "w").close() # Will make the file if not there & clear them
  checkGroup()
