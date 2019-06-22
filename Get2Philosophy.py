import requests
from bs4 import BeautifulSoup as bs
import time
def rm_brackets(input):
    output=""
    in_brackets=False
    open_angle_found=False
    a=False
    a_inside_brackets=False
    for i in range(0,len(input)):

        if input[i]=='<':
            open_angle_found=True

        elif input[i]=="a":
            a=True

        if input [i]=="a" and input [i-1]=='<' and in_brackets==True:
            a_inside_brackets=True

        elif input[i]==">":
            open_angle_found=False
        if input[i]=='(':
            in_brackets=True
        elif input[i-1]==')':
            in_brackets=False


        if a==True and open_angle_found==True and a_inside_brackets==False:
            output+=input[i]

        elif in_brackets==False:
            output+=input[i]

    return output
def get_link(link_list):

    for link in link_list:
        if link['href'][0:5]=="/wiki":
            return "https://en.wikipedia.org"+str(link['href']),str(link['title'])
        elif link['href'][0:5]=="https" and str(link['href']).find("/wiki")!=-1:
            return str(link['href']),str(link['title'])
    return None,None
def main():
    max_visited=100
    limit_reached=False
    valid_url="https://en.wikipedia.org/wiki/Special:Random"
    page_name=""
    loop=False
    #visited dictionary used to store visited links and to prevent loops
    visited={}
    has_valid_links=True

    while(page_name!='Philosophy' and loop==False and has_valid_links==True and limit_reached==False):

        page=requests.get(valid_url)
        time.sleep(.5)
        bs_object=bs(page.text,"html.parser")
        main_body=bs_object.find("div",attrs={'id':'bodyContent'})
        #deleting all tables from the main body article
        for item in main_body.find_all("table"):
            item.decompose()
        #get all paragraphs in main body article
        paragraphs=main_body.find_all("p", attrs={'class':""})
        unwanted=["i","sub","sup","span","b"]
        #deleting items that has no valid links
        for paragraph in paragraphs:
            for element in unwanted:
                for item in paragraph.find_all(element):
                    item.decompose()
            #removing anything between brackets if the brackets are not inside an a-tag
            paragraph_txt=rm_brackets(str(paragraph))
            #converting to beautifulsoup object again to get the links
            par_bs_object=bs(paragraph_txt,features="html5lib")
            links=par_bs_object.find_all("a", href=True)
            #getting the first valid link in links
            valid_url, page_name=get_link(links)
            if(valid_url!=None):
                break

        #condition for pages that doesn't lead to any other page.
        if(valid_url==None):
            has_valid_links=False
            print("article has no valid links")

        print(page_name, sep=' ', end='->', flush=True)

#To prevent loops
        if page_name in visited:
            visited[page_name]+=1
        else:
            visited[page_name]=1

        if visited[page_name] > 1:
            loop=True
            print('Loop Found!')
        if len(visited) > max_visited:
            limit_reached=True
            print("Max limit reached!")


if __name__=="__main__":
    main()
