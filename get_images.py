
from typing import List
import requests

GITHUB_API_CONTRIBUTORS = f"https://api.github.com/repos/OWNER/REPO/contributors?page="
MAX_COUNT = 50

def get_contributors(url:str,result_list:List,page_number:int,current_count:int)->bool:
    current_url = f"{url}{page_number}"
    r = requests.get(current_url)
    if r.status_code == 200:
        contributer_list = r.json()
        if len(contributer_list):
            for contributer in contributer_list:
                if current_count == MAX_COUNT:
                    return True # ends the loop.
                result_list.append(contributer)
                current_count += 1
            return get_contributors(url,result_list,page_number+1,current_count)
        else:
            return True # reached the end, true.
    else:
        # it should never hit this stage ?
        # if it does github endpoint may have some issues
        # since github will return an empty list.
        return False

if __name__ == "__main__":
    result_list = []
    api_url = GITHUB_API_CONTRIBUTORS.replace('OWNER','BoostIO')
    api_url = api_url.replace('REPO','Boostnote')
    if get_contributors(api_url,result_list,1,0):
        print(len(result_list))
        for contributor in result_list:
            print(contributor.get("login"))
    else:
        print("Failed")