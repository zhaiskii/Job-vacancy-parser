from bs4 import BeautifulSoup
import requests
import time

unknown = input("Enter the skills you are unfamiliar with: a comma should separate two skills, an excess space would ruin the program: ")

def form(item):
    bad=0
    res=""
    for i in item:
        val = ord(i)
        if val==10:
            continue
        if bad==0 and val==32:
            continue
        res+=i
        bad=1
    return res

def form_skills(item):
    bad=0
    res=""
    bd=0
    cnttt=0
    for num in range(0, len(item)):
        while num+1<len(item) and item[num]==' ' and item[num+1]==' ':
            num+=1
        if ord(item[num]) == 10:
            continue
        if num==len(item):
            break
        if num+1!=len(item) and item[num]==' ' and item[num+1]==',':
            continue
        if num != 0 and item[num] == ' ' and item[num - 1] == ',':
            continue
        if bd==0 and item[num]==' ':
            continue
        bd=1
        res+=item[num]
    cur=""
    arr = []
    for i in res:
        val = ord(i)
        if val==44:
            arr.append(cur)
            cur=""
            continue
        cur+=i
    last=""
    bdd=0
    for i in range(len(cur)-1, -1, -1):
        val =  ord(cur[i])
        if val==32 and bdd==0:
            continue
        bdd=1
        last+=cur[i]
    last = ''.join(reversed(last))
    arr.append(last)
    return arr

def find_jobs():

    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=Home_Search&from=submit&asKey=OFF&txtKeywords=&cboPresFuncArea=35').text

    soup = BeautifulSoup(html_text, 'lxml')

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')


    my_dict = {
        "@@#@!@#": 0
    }

    res = ""

    for i in unknown:
        if i==',':
            my_dict[res] = 1
            res=""
            continue
        res+=i

    my_dict[res]=1

    cnt=0

    for i in jobs:
        job_name = i.find('a').text
        skills = i.find('span', class_="srp-skills").text
        post_date = i.find('span', class_="sim-posted").span.text
        if post_date!="Posted today":
            continue
        link = i.find('header', class_="clearfix").h2.a['href']
        skills_arr = []
        job_name = form(job_name)
        skills_arr = form_skills(skills)
        badbad=0
        for j in skills_arr:
            bruh=""
            bruh=j
            if bruh in my_dict:
                badbad=1
                break
        if badbad==1:
            continue
        post_date = form(post_date)
        cnt+=1
        with open(f'information/{cnt}.txt', 'w') as f:
            f.write(link)
            f.write('\n')
            f.write(f"Jobs: {job_name}")
            f.write('\n')
            f.write(f"Post release date: {post_date}")
        print("file saved")


if __name__ == '__main__':
    while 1==1:
        find_jobs()
        time.sleep(600)
