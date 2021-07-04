#https://github.com/m4ll0k/takeover thanks for great ideas and signatures
import pandas as pd
import concurrent.futures
import requests
import time
import os
import sys
import re
import json
requests.packages.urllib3.disable_warnings()


possible_takeovers = []
services = {}
services['Heroku'] = r'no-such-app\.html|<title>no such app<\/title>|herokucdn\.com\/error-pages\/no-such-app\.html'
services['AWS/S3'] = r'The specified bucket does not exist'
services['BitBucket'] = r'Repository not found'
services['Github'] = r'There isn\'t a Github Pages site here\.'
services['Shopify'] = r'Sorry\, this shop is currently unavailable\.'
services['Ghost'] = r'The thing you were looking for is no longer here\, or never was'
services['Pantheon'] = r'The gods are wise, but do not know of the site which you seek\.'
services['Tumbler'] = r'Whatever you were looking for doesn\'t currently exist at this address.'
services['Wordpress'] = r'Do you want to register'
services['TeamWork'] = r'Oops - We didn\'t find your site\.'
services['Helpjuice'] = r'We could not find what you\'re looking for\.'
services['Helpscout'] = r'No settings were found for this company:'
services['Cargo'] = r'<title>404 &mdash; File not found<\/title>'
services['Uservoice'] = r'This UserVoice subdomain is currently available!'
services['Surge'] = r'project not found'
services['Intercom'] =  r'This page is reserved for artistic dogs\.|Uh oh\. That page doesn\'t exist</h1>'
services['Webflow'] = r'<p class=\"description\">The page you are looking for doesn\'t exist or has been moved.</p>'
services['Kajabi'] = r'<h1>The page you were looking for doesn\'t exist.</h1>'
services['Tave'] = r'<h1>Error 404: Page Not Found</h1>'
services['Wishpond'] = r'<h1>https://www.wishpond.com/404?campaign=true'
services['Aftership'] = r'Oops.</h2><p class=\"text-muted text-tight\">The page you\'re looking for doesn\'t exist.'
services['Aha'] = r'There is no portal here \.\.\. sending you back to Aha!'
services['Tictail'] = r'to target URL: <a href=\"https://tictail.com|Start selling on Tictail.'
services['Brightcove'] = r'<p class=\"bc-gallery-error-code\">Error Code: 404</p>'
services['Bigcartel'] = r'<h1>Oops! We couldn&#8217;t find that page.</h1>'
services['ActiveCampaign'] = r'alt=\"LIGHTTPD - fly light.\"'
services['Campaignmonitor'] = r'Double check the URL or <a href=\"mailto:help@createsend.com'
services['Proposify'] = r'If you need immediate assistance, please contact <a href=\"mailto:support@proposify.biz'
services['Simplebooklet'] = r'We can\'t find this <a href=\"https://simplebooklet.com'
services['GetResponse'] = r'With GetResponse Landing Pages, lead generation has never been easier'
services['Vend'] = r'Looks like you\'ve traveled too far into cyberspace.'
services['Jetbrains'] = r'is not a registered InCloud YouTrack.'
services['Smartling'] = r'Domain is not configured'
services['Pingdom'] = r'pingdom'
services['Tilda'] = r'Domain has been assigned'
services['Surveygizmo'] = r'data-html-name'
services['Mashery'] = r'Unrecognized domain <strong>'
services['Divio'] = r'Application not responding'
services['feedpress'] = r'The feed has not been found.'
services['readme'] = r'Project doesnt exist... yet!'
services['statuspage'] = r'You are being <a href=\'https>'
services['zendesk'] = r'Help Center Closed'
services['worksites.net'] = r'Hello! Sorry, but the webs>'

proxies = {
  "http": "http://ilike2-rotate:reall3nots3cureguys@p.webshare.io:80",
}

out = []
CONNECTIONS = 20
TIMEOUT = 2

tlds = open(sys.argv[1]).read().splitlines()
results_location = sys.argv[2]
urls = [x for x in tlds[1:]]
takeovers = []
print(urls)



def check_takeover(url,timeoutin):
    response = requests.get(url,timeout=timeoutin,verify=False,proxies=proxies).text
 
    for service in services:
       test = re.findall(services[service],response)
       if test:
          print("{} takeover possible on {}".format(service,url))
          tmp_dict = {}
          tmp_dict['url'] = url
          tmp_dict['service'] = service
          possible_takeovers.append(tmp_dict)



with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    future_to_url = (executor.submit(check_takeover, url, TIMEOUT) for url in urls)
    time1 = time.time()
    for future in concurrent.futures.as_completed(future_to_url):
        try:
            data = future.result()
        except Exception as exc:
            data = str(type(exc))
        finally:
            out.append(data)

            print(str(len(out)),end="\r")

    time2 = time.time()

print(f'Took {time2-time1:.2f} s')
print(pd.Series(out).value_counts())


print(possible_takeovers)

if possible_takeovers:
   with open(results_location, 'w') as output_location:
       json.dump(possible_takeovers, output_location,indent=4)



    

